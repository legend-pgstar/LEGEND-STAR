#!/usr/bin/env python3
"""
Rebuild main.py with simplified TODO commands
Keep the first 1108 lines (everything before TODO system)
Then add new simplified /todo and /atodo commands
"""

# Read the original file
with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep the first 1108 lines (everything is good before TODO system)
keep_lines = lines[:1108]

# Find where ADMIN COMMANDS section starts in the original
admin_cmd_start = None
for i, line in enumerate(lines):
    if '# ==================== ADMIN COMMANDS ====================' in line:
        admin_cmd_start = i
        break

if admin_cmd_start is None:
    print("ERROR: Could not find ADMIN COMMANDS section")
    exit(1)

print(f"ADMIN COMMANDS starts at line {admin_cmd_start + 1}")

# Get ADMIN COMMANDS section and everything after it
admin_section = lines[admin_cmd_start:]

# Build new TODO section
todo_section = '''# ==================== TODO SYSTEM ====================
# Simple command-based TODO with direct attachment support

@tree.command(name="todo", description="Submit daily TODO with tasks and file", guild=GUILD)
@app_commands.describe(
    feature="Feature name (required)",
    date="Date DD/MM/YYYY",
    must_do="Must Do tasks",
    can_do="Can Do tasks",
    dont_do="Don't Do restrictions",
    attachment="File/Screenshot (max 8MB)"
)
async def todo(
    interaction: discord.Interaction,
    feature: str,
    date: str,
    attachment: discord.Attachment = None,
    must_do: str = None,
    can_do: str = None,
    dont_do: str = None
):
    """Submit daily TODO with feature name, date, and categories"""
    await interaction.response.defer()
    
    uid = str(interaction.user.id)
    
    # Auth check
    if not safe_find_one(active_members_coll, {"_id": uid}) and interaction.user.id != OWNER_ID:
        await interaction.followup.send("❌ Not authorized", ephemeral=True)
        return
    
    # Date validation
    try:
        date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        await interaction.followup.send(f"❌ Invalid date. Use DD/MM/YYYY format", ephemeral=True)
        return
    
    # Content check
    if not any([must_do, can_do, dont_do]) and not attachment:
        await interaction.followup.send("❌ Provide content or attachment", ephemeral=True)
        return
    
    # Validate attachment if provided
    attachment_data = None
    if attachment:
        # Size check
        if attachment.size > 8 * 1024 * 1024:
            await interaction.followup.send(f"❌ File too large (max 8MB)", ephemeral=True)
            return
        
        # Type check
        ext = attachment.filename.rsplit('.', 1)[-1].lower() if '.' in attachment.filename else ''
        valid_exts = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff', 'pdf', 'txt', 'doc', 'docx', 'xlsx', 'ppt', 'pptx', 'csv']
        
        if ext not in valid_exts:
            await interaction.followup.send(f"❌ File type not supported", ephemeral=True)
            return
        
        # Detect type
        file_type = 'image' if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff'] else 'document'
        
        attachment_data = {
            "url": attachment.url,
            "filename": attachment.filename,
            "file_type": file_type,
            "uploaded_at": datetime.datetime.now(KOLKATA).isoformat()
        }
    
    # Save to DB
    now = datetime.datetime.now(tz=KOLKATA)
    todo_data = {
        "feature_name": feature,
        "date": date,
        "must_do": must_do or "N/A",
        "can_do": can_do or "N/A",
        "dont_do": dont_do or "N/A",
        "submitted_at": now.isoformat()
    }
    if attachment_data:
        todo_data["attachment"] = attachment_data
    
    safe_update_one(todo_coll, {"_id": uid}, {
        "$set": {
            "last_submit": time.time(),
            "last_ping": 0,
            "todo": todo_data,
            "updated_at": now.isoformat()
        }
    })
    
    # Create embed for channel
    embed = discord.Embed(title=f"📋 {feature}", color=discord.Color.from_rgb(0, 150, 255), timestamp=now)
    embed.add_field(name="👤 By", value=interaction.user.mention, inline=False)
    embed.add_field(name="📅 Date", value=date, inline=True)
    
    if must_do:
        embed.add_field(name="✔️ MUST DO", value=f"```{must_do}```", inline=False)
    if can_do:
        embed.add_field(name="🎯 CAN DO", value=f"```{can_do}```", inline=False)
    if dont_do:
        embed.add_field(name="❌ DON'T DO", value=f"```{dont_do}```", inline=False)
    
    if attachment_data:
        emoji = "🖼️" if attachment_data['file_type'] == 'image' else "📄"
        embed.add_field(name=f"{emoji} File", value=f"[{attachment.filename}]({attachment.url})", inline=False)
        if attachment_data['file_type'] == 'image':
            embed.set_image(url=attachment.url)
    
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
    
    # Send to TODO channel (PUBLIC)
    try:
        guild = bot.get_guild(GUILD_ID)
        if guild:
            channel = guild.get_channel(TODO_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)
    except:
        pass
    
    await interaction.followup.send("✅ TODO posted for everyone!")


@tree.command(name="atodo", description="Assign TODO to user (Owner only)", guild=GUILD)
@app_commands.describe(
    user="Target user",
    feature="Feature name",
    date="Date DD/MM/YYYY",
    must_do="Must Do tasks",
    can_do="Can Do tasks",
    dont_do="Don't Do restrictions",
    attachment="File/Screenshot"
)
async def atodo(
    interaction: discord.Interaction,
    user: discord.Member,
    feature: str,
    date: str,
    attachment: discord.Attachment = None,
    must_do: str = None,
    can_do: str = None,
    dont_do: str = None
):
    """Owner-only: Assign TODO to another user"""
    await interaction.response.defer()
    
    # Owner check
    if interaction.user.id != OWNER_ID:
        await interaction.followup.send("❌ Owner only", ephemeral=True)
        return
    
    uid = str(user.id)
    
    # Target auth check
    if not safe_find_one(active_members_coll, {"_id": uid}):
        await interaction.followup.send(f"❌ {user.mention} not authorized", ephemeral=True)
        return
    
    # Date validation
    try:
        date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        await interaction.followup.send(f"❌ Invalid date", ephemeral=True)
        return
    
    # Content check
    if not any([must_do, can_do, dont_do]) and not attachment:
        await interaction.followup.send("❌ Provide content", ephemeral=True)
        return
    
    # Validate attachment
    attachment_data = None
    if attachment:
        if attachment.size > 8 * 1024 * 1024:
            await interaction.followup.send(f"❌ File too large", ephemeral=True)
            return
        
        ext = attachment.filename.rsplit('.', 1)[-1].lower() if '.' in attachment.filename else ''
        valid_exts = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'txt', 'doc', 'docx', 'xlsx', 'ppt', 'pptx', 'csv']
        
        if ext not in valid_exts:
            await interaction.followup.send(f"❌ File type not supported", ephemeral=True)
            return
        
        file_type = 'image' if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff'] else 'document'
        
        attachment_data = {
            "url": attachment.url,
            "filename": attachment.filename,
            "file_type": file_type,
            "uploaded_at": datetime.datetime.now(KOLKATA).isoformat()
        }
    
    # Save to DB
    now = datetime.datetime.now(tz=KOLKATA)
    todo_data = {
        "feature_name": feature,
        "date": date,
        "must_do": must_do or "N/A",
        "can_do": can_do or "N/A",
        "dont_do": dont_do or "N/A",
        "submitted_at": now.isoformat(),
        "submitted_by": interaction.user.name,
        "submitted_by_id": interaction.user.id
    }
    if attachment_data:
        todo_data["attachment"] = attachment_data
    
    safe_update_one(todo_coll, {"_id": uid}, {
        "$set": {
            "last_submit": time.time(),
            "last_ping": 0,
            "todo": todo_data,
            "updated_at": now.isoformat()
        }
    })
    
    # Create embed - GOLD color for owner submission
    embed = discord.Embed(title=f"📋 {feature}", color=discord.Color.from_rgb(255, 165, 0), timestamp=now)
    embed.add_field(name="👤 Assigned To", value=user.mention, inline=False)
    embed.add_field(name="👨‍💼 By Owner", value=interaction.user.mention, inline=False)
    embed.add_field(name="📅 Date", value=date, inline=True)
    
    if must_do:
        embed.add_field(name="✔️ MUST DO", value=f"```{must_do}```", inline=False)
    if can_do:
        embed.add_field(name="🎯 CAN DO", value=f"```{can_do}```", inline=False)
    if dont_do:
        embed.add_field(name="❌ DON'T DO", value=f"```{dont_do}```", inline=False)
    
    if attachment_data:
        emoji = "🖼️" if attachment_data['file_type'] == 'image' else "📄"
        embed.add_field(name=f"{emoji} File", value=f"[{attachment.filename}]({attachment.url})", inline=False)
        if attachment_data['file_type'] == 'image':
            embed.set_image(url=attachment.url)
    
    # Send to TODO channel (PUBLIC)
    try:
        guild = bot.get_guild(GUILD_ID)
        if guild:
            channel = guild.get_channel(TODO_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)
    except:
        pass
    
    await interaction.followup.send(f"✅ TODO assigned to {user.mention}!")


@tasks.loop(hours=3)
async def todo_checker():
    """Ping users who haven't submitted TODO in 24 hours"""
    if GUILD_ID <= 0:
        return
    
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return
    
    channel = guild.get_channel(TODO_CHANNEL_ID)
    if not channel:
        return
    
    now = time.time()
    one_day = 24 * 3600
    three_hours = 3 * 3600
    five_days = 5 * 86400
    
    for doc in safe_find(todo_coll, {}):
        try:
            uid = int(doc["_id"])
            member = guild.get_member(uid)
            
            if not member or member.bot:
                continue
            
            last_submit = doc.get("last_submit", 0)
            last_ping = doc.get("last_ping", 0)
            elapsed = now - last_submit
            
            # Remove role if inactive 5+ days
            if elapsed >= five_days:
                role = guild.get_role(ROLE_ID)
                if role and role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
            
            # Ping if inactive 24+ hours AND haven't pinged in 3+ hours
            elif elapsed >= one_day and (now - last_ping) >= three_hours:
                days = int(elapsed // 86400)
                hours = int((elapsed % 86400) // 3600)
                time_str = f"{days}d {hours}h" if days > 0 else f"{hours}h"
                
                embed = discord.Embed(
                    title="⏰ TODO Reminder!",
                    description=f"{member.mention}\nLast submitted: **{time_str} ago**",
                    color=discord.Color.gold()
                )
                embed.add_field(name="Action", value="Use `/todo` to submit", inline=False)
                
                try:
                    await channel.send(embed=embed)
                    await member.send(embed=embed)
                except:
                    pass
                
                # Update ping timestamp
                safe_update_one(todo_coll, {"_id": str(uid)}, {"$set": {"last_ping": now}})
        except:
            pass


@todo_checker.before_loop
async def before_todo_checker():
    """Ensure todo_checker starts"""
    await bot.wait_until_ready()


@tree.command(name="listtodo", description="View your current TODO", guild=GUILD)
async def listtodo(interaction: discord.Interaction):
    """View your current TODO submission"""
    await interaction.response.defer(ephemeral=True)
    try:
        doc = safe_find_one(todo_coll, {"_id": str(interaction.user.id)})
        if not doc or "todo" not in doc:
            return await interaction.followup.send("No TODO submitted yet. Use `/todo`", ephemeral=True)
        
        todo = doc["todo"]
        embed = discord.Embed(title=f"📋 {todo.get('feature_name', 'N/A')}", color=discord.Color.blue())
        embed.add_field(name="📅 Date", value=todo.get('date', 'N/A'), inline=True)
        embed.add_field(name="✔️ Must Do", value=f"```{todo.get('must_do', 'N/A')}```", inline=False)
        embed.add_field(name="🎯 Can Do", value=f"```{todo.get('can_do', 'N/A')}```", inline=False)
        embed.add_field(name="❌ Don't Do", value=f"```{todo.get('dont_do', 'N/A')}```", inline=False)
        
        if "attachment" in todo:
            att = todo["attachment"]
            embed.add_field(name="📎 File", value=f"[{att.get('filename', 'File')}]({att.get('url', 'N/A')})", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)[:100]}", ephemeral=True)


@tree.command(name="deltodo", description="Delete your TODO", guild=GUILD)
async def deltodo(interaction: discord.Interaction):
    """Delete your current TODO submission"""
    await interaction.response.defer(ephemeral=True)
    try:
        result = safe_delete_one(todo_coll, {"_id": str(interaction.user.id)})
        if result:
            await interaction.followup.send("✅ TODO deleted", ephemeral=True)
        else:
            await interaction.followup.send("❌ No TODO to delete", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)[:100]}", ephemeral=True)


@tree.command(name="todostatus", description="Check TODO status", guild=GUILD)
@app_commands.describe(user="Optional: Check another user (Owner only)")
async def todostatus(interaction: discord.Interaction, user: discord.Member = None):
    """Check your or another user's TODO status"""
    await interaction.response.defer(ephemeral=True)
    
    target = user if user else interaction.user
    
    # If checking another user, owner check
    if user and interaction.user.id != OWNER_ID:
        return await interaction.followup.send("❌ Owner only", ephemeral=True)
    
    try:
        doc = safe_find_one(todo_coll, {"_id": str(target.id)})
        last_submit = doc.get("last_submit", 0) if doc else 0
        
        now = time.time()
        elapsed = now - last_submit
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        embed = discord.Embed(title="📊 TODO Status", color=discord.Color.green())
        embed.add_field(name="User", value=target.mention)
        embed.add_field(name="Last Submit", value=f"{time_str} ago")
        embed.add_field(name="Status", value="✅ Safe" if elapsed < 86400 else "⏰ Pending ping")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)[:100]}", ephemeral=True)

'''

# Combine all parts
new_content = ''.join(keep_lines) + '\n' + todo_section + '\n' + ''.join(admin_section)

# Write the new file
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ main.py rebuilt successfully!")
print(f"   - Kept first 1108 lines (working code)")
print(f"   - Added new simplified TODO system")
print(f"   - Kept ADMIN COMMANDS section")
print(f"   - Total lines: {len(new_content.splitlines())}")
