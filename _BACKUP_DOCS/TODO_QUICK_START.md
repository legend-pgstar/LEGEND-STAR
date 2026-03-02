# 🚀 QUICK START GUIDE - Advanced TODO System

**Last Updated**: January 29, 2026  
**Status**: ✅ PRODUCTION READY  
**Version**: 4.0

---

## ⚡ 30-SECOND OVERVIEW

The **Advanced TODO System** provides:
- ✅ `/todo` command for users to submit daily tasks
- ✅ `/atodo @user` command for owner to assign TODOs
- ✅ Three-category task system (Must Do, Can Do, Don't Do)
- ✅ Automatic posting to TODO channel
- ✅ Optional file attachment support
- ✅ Smart authorization and validation

---

## 🎯 FOR USERS

### Using /todo

**Step 1: Open Command**
```
Type: /todo
Press: Enter
```

**Step 2: Fill Form**
```
Feature Name: "Backend API Implementation"
Date: 29/01/2026 (DD/MM/YYYY format)
Must Do: "Implement endpoints, write tests"
Can Do: "Add rate limiting" (optional)
Don't Do: "Don't use deprecated libs" (optional)
```

**Step 3: Submit**
```
Click: Submit button
Result: Posted to #todo-channel automatically
```

**Step 4: Optional - Add Attachment**
```
Click: "📸 Upload Screenshot" button
Reply: With your file (PNG, JPG, PDF, DOCX, etc.)
Limit: 8 MB, 10 minute window
```

**Step 5: Complete (Optional)**
```
Click: "✅ Complete" button
Shows: Summary of your submission
```

---

## 👨‍💼 FOR OWNER

### Using /atodo

**Step 1: Open Command**
```
Type: /atodo @developer
Press: Enter
```

**Step 2: Fill Form**
```
(Same as /todo)
Feature Name: "Database Optimization"
Date: 29/01/2026
Must Do: "Optimize queries"
Can Do: "Add monitoring" (optional)
Don't Do: "Don't modify schema" (optional)
```

**Step 3: Submit**
```
Click: Submit button
Result: Assigned to @developer
        Posted to #todo-channel (gold color)
        Their ping timer is RESET
```

**Step 4: Optional - Add Attachment**
```
Same as user (10 min window)
```

---

## 🔑 KEY FEATURES

### ✔️ Must Do (Required)
Essential tasks that MUST be completed
```
Example: "Implement API endpoints and write unit tests"
```

### 🎯 Can Do (Optional)
Nice-to-have features if time permits
```
Example: "Add caching layer, optimize performance"
```

### ❌ Don't Do (Restrictions)
Things to AVOID doing
```
Example: "Don't modify database schema"
```

---

## 📎 FILE ATTACHMENT

### Supported Formats
```
📷 Images: PNG, JPG, JPEG, GIF, WEBP, BMP, TIFF
📄 Documents: PDF, TXT, DOCX, XLSX, PPTX, CSV
```

### Limits
```
Maximum File Size: 8 MB
Upload Window: 10 minutes after submission
```

### Process
```
1. Submit /todo without file
2. Click "📸 Upload Screenshot"
3. Reply to message with attachment
4. File is validated and stored
```

---

## ✅ CHECKING STATUS

### View Your Current TODO
```
Command: /listtodo
Shows: Your submitted TODO
```

### Check Submission Status
```
Command: /todostatus
Shows: When you last submitted
       How long since submission
       Current status
```

### Owner: Check Another User
```
Command: /todostatus @user
Shows: Their submission status (owner only)
```

---

## 🗑️ DELETING TODO

### Remove Your Current TODO
```
Command: /deltodo
Result: Your TODO is deleted
        Timer is unchanged
```

---

## 📅 DATE FORMAT

### Correct Format
```
DD/MM/YYYY
├─ DD: Day (01-31)
├─ MM: Month (01-12)
└─ YYYY: Year (2026)

Examples:
✅ 29/01/2026 (January 29, 2026)
✅ 01/02/2026 (February 1, 2026)
✅ 15/12/2025 (December 15, 2025)

❌ 01/29/2026 (Wrong - American format)
❌ 2026-01-29 (Wrong - ISO format)
❌ January 29, 2026 (Wrong - Text format)
```

---

## 🔐 WHO CAN USE WHAT

### /todo (User Submission)
```
✅ Active members (added by owner with /addh)
✅ Owner (automatically authorized)
❌ Others → "Not authorized" error
```

### /atodo (Owner Assignment)
```
✅ Owner ONLY (OWNER_ID: 1406313503278764174)
❌ Everyone else → "Owner only" message
```

### /addh (Owner Management)
```
Owner adds user: /addh 123456789
User can then use /todo
```

### /remh (Owner Management)
```
Owner removes user: /remh 123456789
User can no longer use /todo
```

---

## 🔔 AUTO-PING SYSTEM

### When You Get Pinged
```
If you haven't submitted TODO for 24+ hours:
├─ Channel mention (public)
└─ DM notification (private)

Happens: Every 3 hours until you submit
Stops: When you submit /todo or owner uses /atodo
```

### How to Avoid Pings
```
Method 1: Submit /todo regularly
Method 2: Owner assigns /atodo to reset timer
```

### Role Removal
```
If inactive 5+ days:
├─ TODO role is automatically removed
├─ You can rejoin with /todo
└─ Owner can re-add with /addh
```

---

## 🎨 WHAT SHOWS IN CHANNEL

### Example: User Submission
```
📋 Backend API Implementation
👤 Submitted By: @developer
📅 Date: 29/01/2026
⏰ Submitted: 2:30 PM today

✔️ MUST DO (Required)
```
Implement API endpoints, write tests
```

🎯 CAN DO (Optional)
```
Add rate limiting
```

❌ DON'T DO (Restrictions)
```
Don't use deprecated libraries
```

Footer: Submission ID | Status: Submitted
```

### Example: Owner Assignment
```
(Same format but with:)
👨‍💼 Submitted By: @Owner
👤 Assigned To: @developer
(Gold color instead of green)
```

---

## 💡 TIPS & TRICKS

### Tip 1: Use Clear Descriptions
```
❌ Bad: "Do stuff"
✅ Good: "Implement authentication system with JWT tokens"
```

### Tip 2: Include Success Criteria
```
❌ Bad: "Write code"
✅ Good: "Write 100% unit test coverage for auth module"
```

### Tip 3: Use Bullet Points
```
✅ Good: 
- Implement endpoint
- Write tests
- Update documentation
```

### Tip 4: Set Realistic Goals
```
✅ Good: Tasks completable in 24 hours
❌ Bad: Month-long project in single TODO
```

### Tip 5: Include Restrictions
```
✅ Include "Don't Do" to prevent mistakes:
- Don't use external APIs
- Don't modify database schema
```

---

## ❌ COMMON MISTAKES

### Mistake 1: Wrong Date Format
```
❌ 01/29/2026 (American)
❌ 2026-01-29 (ISO)
✅ 29/01/2026 (DD/MM/YYYY)
```

### Mistake 2: Leaving All Fields Empty
```
❌ Submitting with no content
✅ Fill at least one category or attach file
```

### Mistake 3: Unsupported File Type
```
❌ Trying to upload .exe or .zip
✅ Use PNG, JPG, PDF, DOCX, etc.
```

### Mistake 4: File Too Large
```
❌ Uploading 20 MB video
✅ Keep files under 8 MB
```

### Mistake 5: Forgetting to Submit
```
❌ Filling form but closing without submit
✅ Click Submit button to save
```

---

## 🆘 TROUBLESHOOTING

### "Modal doesn't open"
```
Check: Can you use slash commands in this channel?
Fix: Ask admin to enable app commands
```

### "Not authorized"
```
Check: Are you in active members list?
Fix: Contact owner to use /addh with your ID
```

### "Invalid Date Format"
```
Check: Using DD/MM/YYYY format?
Fix: Use 29/01/2026 not 01/29/2026
```

### "Empty Submission"
```
Check: Did you fill at least one category?
Fix: Fill Must Do, Can Do, or Don't Do (or attach file)
```

### "File too large"
```
Check: Is file under 8 MB?
Fix: Compress or choose smaller file
```

### "Unsupported file type"
```
Check: Is file PNG, JPG, PDF, DOCX, etc.?
Fix: Use supported format
```

### "Didn't post to channel"
```
Check: Is bot in TODO channel with message permission?
Fix: Contact admin to verify permissions
```

---

## 📞 GETTING HELP

### For Users
```
Contact: Owner or Admin
Questions: How to use /todo, can't access, etc.
```

### For Owner/Admin
```
Issues: User not in active members, can't post to channel
Solution: Use /tododebug to check status
```

### Emergency
```
If system is broken:
1. Check bot is online
2. Verify MongoDB connection
3. Check channel permissions
4. Review logs for errors
```

---

## ⚙️ SYSTEM REQUIREMENTS

### For Bot
```
✅ Discord.py library
✅ MongoDB connection
✅ Bot permissions in channel
✅ Access to guild/channel IDs
```

### For Users
```
✅ Discord account
✅ Access to server
✅ Permission to use slash commands
```

---

## 🎓 COMPLETE WORKFLOW EXAMPLE

### Scenario: Implementing New Feature

**Monday 9 AM:**
```
1. Owner: /atodo @developer
   Feature: "User Profile API"
   Must Do: "Implement GET/POST/PUT endpoints"
   Can Do: "Add validation, rate limiting"
   Don't Do: "Don't expose internal IDs"
   
2. System: Posts to #todo-channel
           Resets dev's ping timer
```

**Monday 2 PM:**
```
Developer: /todo (submitted already, no ping)
```

**Tuesday 9 AM:**
```
Developer: /listtodo
           Shows current TODO
```

**Tuesday 5 PM:**
```
Developer: /deltodo (if starting new task)
           Then: /todo (new task for next day)
```

---

## 🏆 BEST PRACTICES

### ✅ DO

```
✅ Submit /todo daily
✅ Use specific descriptions
✅ Include success criteria
✅ Set realistic goals
✅ Include "Don't Do" to prevent issues
✅ Update before moving to new task
✅ Attach evidence/screenshots
✅ Use clear language
```

### ❌ DON'T

```
❌ Submit vague descriptions
❌ Set unrealistic goals
❌ Ignore ping reminders
❌ Forget to submit
❌ Use unsupported file formats
❌ Upload very large files
❌ Procrastinate on submitting
❌ Leave TODO stale for 5+ days
```

---

## 📚 RELATED COMMANDS

### User Commands
```
/todo             - Submit daily TODO
/todostatus       - Check status
/listtodo         - View current TODO
/deltodo          - Delete current TODO
```

### Owner Commands
```
/atodo @user      - Assign TODO to user
/addh <user_id>   - Add user to system
/remh <user_id>   - Remove user from system
/members          - List all users
/tododebug        - Debug system
```

---

## 🔄 AUTOMATIC FEATURES

### Ping System
```
Runs: Every 3 hours automatically
Pings: Users inactive 24+ hours
Stops: When user submits /todo
```

### Role Removal
```
Runs: Automatically in background
Removes: Role after 5 days inactivity
Restores: Owner can re-add with /addh
```

### Channel Posting
```
Runs: Immediately on submission
Posts: /todo and /atodo to channel
Format: Professional embed with all info
```

---

## ✨ FEATURES AT A GLANCE

| Feature | User | Owner |
|---------|------|-------|
| /todo | ✅ | ✅ |
| /atodo | ❌ | ✅ |
| Auto-send | ✅ | ✅ |
| Attachments | ✅ | ✅ |
| Check status | ✅ | ✅ (others) |
| Manage users | ❌ | ✅ |
| View all | ❌ | ✅ |
| Debug | ❌ | ✅ |

---

## 🎯 QUICK REFERENCE

```
/todo              → Open form and submit
/atodo @user       → Assign to user (owner only)
/todostatus        → Check your status
/listtodo          → View your TODO
/deltodo           → Delete your TODO
/addh <id>         → Add user (owner only)
/remh <id>         → Remove user (owner only)
/members           → List users (owner only)
/tododebug         → Debug system (owner only)
```

---

## 🚀 YOU'RE READY!

The system is ready to use:
- ✅ All features working
- ✅ All validations in place
- ✅ All safeguards enabled
- ✅ Documentation complete

**Start submitting TODOs today!** 💪

---

## 📞 SUPPORT

**For questions or issues:**
```
Contact: Owner/Admin
Resources: Check /tododebug
Logs: Available in bot console
```

**Happy tasking!** 🎉
