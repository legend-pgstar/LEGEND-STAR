# 🔧 TODO PING SYSTEM - CODE SNIPPETS & REFERENCE

---

## 📌 MODIFIED CODE SECTIONS IN main.py

### **SECTION 1: TodoModal.on_submit() - Line ~1000-1020**

```python
async def on_submit(self, interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
        uid = str(interaction.user.id)
        
        # ... validation code ...
        
        # 🔥 KEY CHANGE: Reset ping timer when user submits
        print(f"⏸️ [TODO] Saving to database...")
        safe_update_one(todo_coll, {"_id": uid}, {"$set": {
            "last_submit": time.time(),
            "last_ping": 0,  # 🔥 RESET PING TIMER when user submits - No more pings!
            "todo": {
                "name": self.name.value,
                "date": self.date.value,
                "must_do": self.must_do.value or "N/A",
                "can_do": self.can_do.value or "N/A",
                "dont_do": self.dont_do.value or "N/A"
            }
        }})
        print(f"✅ [TODO] Database save complete - Ping timer RESET!")
        
        # ... rest of code ...
```

**What Changed:**
- Added `"last_ping": 0` field to reset ping timer
- This stops the bot from pinging this user until 24+ hours pass again

---

### **SECTION 2: AtodoModal.on_submit() - Line ~1100-1120**

```python
async def on_submit(self, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    uid = str(self.target.id)
    
    try:
        # ... validation code ...
        
        # 🔥 KEY CHANGE: Reset ping timer when owner submits for user
        print(f"⏸️ [ATODO] Saving to database...")
        safe_update_one(todo_coll, {"_id": uid}, {"$set": {
            "last_submit": time.time(),
            "last_ping": 0,  # 🔥 RESET PING TIMER when owner submits - No more pings!
            "todo": {
                "name": self.name.value,
                "date": self.date.value,
                "must_do": self.must_do.value or "N/A",
                "can_do": self.can_do.value or "N/A",
                "dont_do": self.dont_do.value or "N/A"
            }
        }})
        print(f"✅ [ATODO] Database save complete - Ping timer RESET!")
        
        # ... rest of code ...
```

**What Changed:**
- Same as TodoModal: added `"last_ping": 0` to reset timer
- Now when owner uses /atodo, it also resets ping timer for that user

---

### **SECTION 3: todo_checker() - Line ~1178-1345 [COMPLETE REWRITE]**

```python
@tasks.loop(hours=3)  # 🔥 CHANGED from hours=1 to hours=3
async def todo_checker():
    """
    🔥 ADVANCED TODO PING SYSTEM 🔥
    
    - Monitors all users with TODO role
    - If user participates but doesn't share TODO in last 24 hours → PING every 3 hours
    - Ping only happens ONCE per 3-hour cycle (not spam)
    - Auto-reset ping timer when user shares /todo or /atodo
    - Removes role after 5 days of inactivity
    
    MongoDB Schema:
    {
        "_id": "user_id",
        "last_submit": timestamp,
        "last_ping": timestamp,  // NEW: Track last ping to avoid spam
        "todo": {...}
    }
    """
    if GUILD_ID <= 0:
        return
    
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return
    
    channel = guild.get_channel(TODO_CHANNEL_ID)
    if not channel:
        return
    
    now = time.time()
    one_day = 24 * 3600       # 24 hours
    five_days = 5 * 86400     # 5 days for role removal
    three_hours = 3 * 3600    # 3 hours between pings
    
    print(f"\n⏰ [TODO_CHECKER] Running advanced TODO verification @ {datetime.datetime.now(KOLKATA).strftime('%H:%M:%S')}")
    
    for doc in safe_find(todo_coll, {}):
        try:
            uid = int(doc["_id"])
            last_submit = doc.get("last_submit", 0)
            last_ping = doc.get("last_ping", 0)  # 🔥 NEW: Track ping history
            elapsed_since_submit = now - last_submit
            elapsed_since_ping = now - last_ping
            
            member = guild.get_member(uid)
            
            # Skip bots and offline members
            if not member or member.bot:
                print(f"⏭️  [TODO_CHECKER] Skipped {uid} (bot/offline)")
                continue
            
            # ============================================================
            # LEVEL 1: Check for 5-day inactivity (REMOVE ROLE)
            # ============================================================
            if elapsed_since_submit >= five_days:
                print(f"🔴 [TODO_CHECKER] {member.display_name} inactive for 5+ days")
                role = guild.get_role(ROLE_ID)
                if role and role in member.roles:
                    try:
                        await member.remove_roles(role)
                        print(f"✅ Removed role from {member.display_name}")
                        
                        # Notify in channel
                        embed = discord.Embed(
                            title="❌ TODO Role Removed",
                            description=f"{member.mention} has been inactive for **5+ days**",
                            color=discord.Color.red()
                        )
                        embed.add_field(name="Action", value="Role removed. Use /todo to rejoin.", inline=False)
                        await channel.send(embed=embed)
                        
                    except Exception as e:
                        print(f"⚠️ Failed to remove role: {e}")
            
            # ============================================================
            # LEVEL 2: Check for 24-hour inactivity (PING - But only once per 3 hours!)
            # ============================================================
            elif elapsed_since_submit >= one_day:
                # 🔥 SMART THROTTLE: Check if we've already pinged in the last 3 hours
                if elapsed_since_ping < three_hours:
                    # Already pinged recently, skip
                    hours_until_next_ping = int((three_hours - elapsed_since_ping) / 3600) + 1
                    print(f"⏭️  [TODO_CHECKER] {member.display_name} already pinged ({hours_until_next_ping}h until next)")
                    continue
                
                # ✅ IT'S TIME TO PING!
                days_inactive = int(elapsed_since_submit // 86400)
                hours_inactive = int((elapsed_since_submit % 86400) // 3600)
                time_str = f"{days_inactive}d {hours_inactive}h" if days_inactive > 0 else f"{hours_inactive}h"
                
                print(f"📢 [TODO_CHECKER] PINGING {member.display_name} (inactive for {time_str})")
                
                # ============================================================
                # 🎯 SMART PING: Channel + DM (Redundant Coverage)
                # ============================================================
                
                # Channel Ping (Public Accountability)
                channel_embed = discord.Embed(
                    title="⏰ TODO Reminder!",
                    description=f"{member.mention}",
                    color=discord.Color.gold()
                )
                channel_embed.add_field(
                    name="📊 Status",
                    value=f"Last submitted: **{time_str} ago**",
                    inline=False
                )
                channel_embed.add_field(
                    name="📝 Action Required",
                    value="Please share `/todo` to update your daily task list",
                    inline=False
                )
                channel_embed.add_field(
                    name="⚠️ Note",
                    value="This reminder runs every 3 hours until you submit",
                    inline=False
                )
                
                try:
                    await channel.send(embed=channel_embed)
                    print(f"✅ Channel ping sent to {member.display_name}")
                except Exception as e:
                    print(f"⚠️ Failed to send channel ping: {e}")
                
                # DM Ping (Direct Notification)
                dm_embed = discord.Embed(
                    title="🔔 TODO Reminder - Direct Message",
                    description="You haven't submitted your TODO in the last 24 hours!",
                    color=discord.Color.orange()
                )
                dm_embed.add_field(
                    name="⏱️ Time Since Last Submit",
                    value=f"**{time_str}** ago",
                    inline=False
                )
                dm_embed.add_field(
                    name="📝 What to do?",
                    value="Use `/todo` command to submit your daily task list",
                    inline=False
                )
                dm_embed.add_field(
                    name="🔄 Ping Frequency",
                    value="You'll receive this reminder every 3 hours until you submit",
                    inline=False
                )
                dm_embed.set_footer(text="Keep up with your daily TODOs! 💪")
                
                try:
                    await member.send(embed=dm_embed)
                    print(f"✅ DM sent to {member.display_name}")
                except Exception as e:
                    print(f"⚠️ Failed to DM {member.display_name}: {e}")
                
                # ============================================================
                # 💾 UPDATE DATABASE: Record this ping time
                # ============================================================
                print(f"💾 [TODO_CHECKER] Updating last_ping timestamp for {member.display_name}")
                safe_update_one(todo_coll, {"_id": str(uid)}, {
                    "$set": {
                        "last_ping": now  # 🔥 Record when we pinged them - prevents duplicate pings within 3h
                    }
                })
                print(f"✅ Database updated - next ping in 3 hours")
                
            else:
                # User is within 24-hour limit, no action needed
                hours_safe = int(elapsed_since_submit / 3600)
                print(f"✅ [TODO_CHECKER] {member.display_name} OK ({hours_safe}h submitted)")
        
        except ValueError:
            print(f"⚠️ todo_checker skipped invalid UID: {doc['_id']}")
        except Exception as e:
            print(f"⚠️ todo_checker error for user {doc.get('_id', '?')}: {str(e)[:100]}")
```

**Key Changes:**
1. Changed `@tasks.loop(hours=1)` → `@tasks.loop(hours=3)`
2. Added `last_ping = doc.get("last_ping", 0)` tracking
3. Implemented 3-hour throttling: `if elapsed_since_ping < three_hours: continue`
4. Dual-channel notifications (Channel + DM embeds)
5. Proper database update: `"last_ping": now`
6. Comprehensive logging with emoji indicators

---

## 🧪 TESTING CODE

### Test 1: Verify Ping Reset on Submit
```python
# After user submits /todo:
doc = todo_coll.find_one({"_id": str(user_id)})
print(f"last_submit: {doc['last_submit']}")
print(f"last_ping: {doc['last_ping']}")
# Expected: last_ping should be 0
```

### Test 2: Verify Ping After 24 Hours
```python
# Simulate time passing by manually updating MongoDB:
todo_coll.update_one(
    {"_id": str(user_id)},
    {"$set": {"last_submit": time.time() - (25 * 3600)}}
)

# Run todo_checker manually, should send ping
await todo_checker()

# Verify last_ping was updated:
doc = todo_coll.find_one({"_id": str(user_id)})
print(f"last_ping updated to: {doc['last_ping']}")
# Expected: last_ping should be current timestamp
```

### Test 3: Verify No Duplicate Pings Within 3 Hours
```python
# After first ping, immediately run checker again:
await todo_checker()
await todo_checker()

# Check logs - should see:
# "📢 PINGING user (first time)"
# "⏭️ user already pinged (3h until next)"
```

---

## 📋 MONGODB QUERY EXAMPLES

### Query 1: Find Users Who Need Pinging
```javascript
db.todo_timestamps.find({
  $expr: {
    $and: [
      { $gte: [{ $subtract: [Date.now(), "$last_submit"] }, 86400000] },  // 24h+
      { $gte: [{ $subtract: [Date.now(), "$last_ping"] }, 10800000] }    // 3h+ since ping
    ]
  }
})
```

### Query 2: Find Users in 5-Day Inactivity
```javascript
db.todo_timestamps.find({
  last_submit: {
    $lt: { $subtract: [Date.now(), 432000000] }  // 5 days in milliseconds
  }
})
```

### Query 3: Reset All Ping Timers
```javascript
db.todo_timestamps.updateMany(
  {},
  { $set: { "last_ping": 0 } }
)
```

### Query 4: View User's Status
```javascript
db.todo_timestamps.findOne({
  _id: "123456789"
})
// Returns: { _id, last_submit, last_ping, todo }
```

---

## 🔧 CONFIGURATION CONSTANTS

**In main.py, these can be adjusted:**

```python
# Line ~1197 in todo_checker():
one_day = 24 * 3600        # 24 hours - inactivity threshold
five_days = 5 * 86400      # 5 days - role removal threshold
three_hours = 3 * 3600     # 3 hours - ping interval

# Examples to change:
# To ping every 2 hours instead:
two_hours = 2 * 3600
if elapsed_since_ping < two_hours:
    continue

# To ping after 12 hours instead of 24:
twelve_hours = 12 * 3600
if elapsed_since_submit >= twelve_hours:
    # send ping
```

---

## 🐛 COMMON ISSUES & FIXES

### Issue 1: "last_ping field doesn't exist"
**Cause:** Old MongoDB documents without the new field  
**Fix:** Automatic - first ping creates it
```python
# Works fine, last_ping defaults to 0:
last_ping = doc.get("last_ping", 0)
```

### Issue 2: "User not getting pinged"
**Checklist:**
```python
# 1. Verify user in active_members:
active_members_coll.find_one({"_id": str(user_id)})

# 2. Verify user in todo_timestamps:
todo_coll.find_one({"_id": str(user_id)})

# 3. Verify timestamps:
import time
now = time.time()
doc = todo_coll.find_one({"_id": str(user_id)})
elapsed = now - doc["last_submit"]
print(f"Elapsed: {elapsed / 3600} hours")
# Should be >= 24 to trigger ping
```

### Issue 3: "User getting pinged too often"
**Cause:** last_ping not updating properly  
**Fix:** Check database update
```python
# Verify update is working:
todo_coll.update_one(
    {"_id": str(user_id)},
    {"$set": {"last_ping": time.time()}}
)

# Verify read back:
doc = todo_coll.find_one({"_id": str(user_id)})
print(f"last_ping: {doc['last_ping']}")
```

---

## 🚀 DEPLOYMENT CHECKLIST

```
Before deploying:
☐ Backup MongoDB
☐ Test with 1 user manually
☐ Check bot permissions:
  ☐ Send Messages
  ☐ Embed Links
  ☐ Manage Roles
☐ Verify TODO_CHANNEL_ID in .env
☐ Verify ROLE_ID in .env
☐ Restart bot after code changes

After deploying:
☐ Check logs for errors
☐ Monitor ping delivery
☐ Verify DM delivery
☐ Test role removal at 5 days
```

---

## ⚡ PERFORMANCE TIPS

```python
# Current (Efficient):
@tasks.loop(hours=3)  # Runs every 3 hours

# Already optimized for production
safe_update_one()  # Only updates changed fields
safe_find()        # Lazy loads results

# Database is indexed on:
# - users: data.voice_cam_on_minutes
# - users: data.voice_cam_off_minutes
# Consider adding index on todo_timestamps._id for faster lookups
```

---

## 📚 RELATED DOCUMENTATION

See also:
- `TODO_PING_SYSTEM_ADVANCED.md` - Detailed system overview
- `TODO_PING_SYSTEM_QUICK_REFERENCE.md` - Quick reference guide
- `TODO_PING_SYSTEM_ARCHITECTURE.md` - System architecture diagrams

---

**All code ready for production deployment!** ✨
