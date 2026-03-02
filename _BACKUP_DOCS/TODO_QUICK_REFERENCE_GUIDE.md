# 🚀 ADVANCED TODO SYSTEM - QUICK REFERENCE

## ⚡ COMMANDS AT A GLANCE

### User Commands
```
/todo                    → Submit daily TODO (feature, date, tasks)
/todostatus             → Check submission status
/listtodo               → View current TODO
/deltodo                → Delete current TODO
```

### Owner Commands
```
/atodo @user            → Assign TODO to user
/addh <user_id>         → Add user to active members
/remh <user_id>         → Remove user from active members
/members                → List all active members
/tododebug              → Debug TODO system
```

---

## 📋 /TODO FORM FIELDS

| Field | Required | Format | Max Length |
|-------|----------|--------|------------|
| Feature Name | ✅ Yes | Text | 100 chars |
| Date | ✅ Yes | DD/MM/YYYY | 10 chars |
| Must Do | ❌ No | Text or "Attaching file" | 1024 chars |
| Can Do | ❌ No | Text or "Attaching file" | 1024 chars |
| Don't Do | ❌ No | Text or "Attaching file" | 1024 chars |

**Validation**: At least one field (Must/Can/Don't) must have content OR attachment

---

## 🎯 /ATODO SPECIAL FEATURES

```
Owner-Only Command: /atodo @target_user

Features:
✅ Owner can assign TODO to any active member
✅ Marks as "Owner Assignment" in channel
✅ Resets target user's ping timer
✅ Gold color embed (vs green for user submissions)
✅ Records owner info in database

Security:
⚠️ STRICT owner-only (OWNER_ID only)
⚠️ Target must be in active_members
⚠️ Authorization checked at two levels
```

---

## 📎 ATTACHMENT SUPPORT

### Supported Formats

**Images** (Recommended for quick evidence)
```
.png .jpg .jpeg .gif .webp .bmp .tiff
```

**Documents** (For detailed reports)
```
.pdf .txt .docx .xlsx .pptx .csv
```

### Size Limit
```
Maximum: 8 MB per file
```

### Upload Process
```
1. Submit /todo form (without file)
2. Click "📸 Upload Screenshot" button
3. Follow instructions
4. Reply to message with attachment
5. File is validated and stored
6. Database updated with metadata
```

---

## ✅ SUBMISSION WORKFLOW

### User Submission (/todo)
```
1. /todo → Modal opens
2. Fill form (feature, date, categories)
3. Submit
   ├─ Check authorization
   ├─ Validate date format
   ├─ Check content (≥1 category)
   ├─ Save to database
   ├─ Create embed
   ├─ Post to #todo-channel
   └─ Send confirmation
4. Optional: Add attachment (10 min window)
5. Optional: Click "✅ Complete" button
```

### Owner Assignment (/atodo)
```
1. /atodo @user → Modal opens
2. Fill form (feature, date, categories)
3. Submit
   ├─ Check owner authorization
   ├─ Verify target user in active_members
   ├─ Validate date format
   ├─ Check content
   ├─ Save to database (target user)
   ├─ Reset target's ping timer
   ├─ Create GOLD embed
   ├─ Post to #todo-channel
   └─ Send confirmation to owner
4. Optional: Owner can add attachment
```

---

## 📊 CATEGORY BREAKDOWN

### ✔️ Must Do (Required)
- Essential tasks that MUST be completed
- Primary focus area
- Mandatory deliverables
- Example: "Implement API endpoints, write unit tests"

### 🎯 Can Do (Optional)
- Nice-to-have features
- Extra work if time permits
- Performance improvements
- Example: "Add caching layer, optimize queries"

### ❌ Don't Do (Restrictions)
- Things to AVOID doing
- Constraints and limitations
- Deprecated approaches
- Example: "Don't modify database schema, don't use deprecated libraries"

---

## 💾 DATABASE STRUCTURE

```json
{
  "_id": "user_id",
  "last_submit": 1706511234.567,
  "last_ping": 0,
  "todo": {
    "feature_name": "Backend API",
    "date": "29/01/2026",
    "must_do": "Implement endpoints",
    "can_do": "Add rate limiting",
    "dont_do": "Don't modify schema",
    "submission_type": "text_only",
    "submitted_at": "2026-01-29T14:30:45+05:30",
    "submission_id": "user_id_1706511234567"
  }
}
```

**With Attachment:**
```json
{
  "attachment": {
    "url": "https://cdn.discordapp.com/...",
    "filename": "screenshot.png",
    "file_type": "image",
    "uploaded_at": "2026-01-29T14:30:45+05:30"
  }
}
```

---

## 🔐 AUTHORIZATION

### /todo
```
✅ Active members (in active_members collection)
✅ Owner (OWNER_ID override)
❌ Others → Error message
```

### /atodo
```
✅ Owner ONLY (strict OWNER_ID check)
❌ Non-owners → "Owner only" message
+ Target must be in active_members
```

---

## 📤 CHANNEL AUTO-SEND

### When it Happens
```
✅ After /todo submission
✅ After /atodo submission
✅ Automatic (non-blocking)
```

### Channel Details
```
Guild: GUILD_ID
Channel: TODO_CHANNEL_ID (#todo-channel)
```

### Message Format
```
Embed:
├─ Title: Feature name
├─ User info (submitter / assigned to)
├─ Date & timestamp
├─ Three categories (with code blocks)
├─ Attachment info (if present)
├─ Footer with submission ID
└─ Author info with avatar
```

---

## 🔔 AUTO-PING SYSTEM

### When Pings Trigger
```
Inactive 24+ hours → Ping every 3 hours
├─ Channel mention (public)
└─ DM notification (direct)
```

### Ping Content
```
⏰ TODO Reminder!
📊 Status: Last submitted X hours ago
📝 Action: Please share /todo
⚠️ Frequency: Every 3 hours until submitted
```

### How to Stop Pings
```
Submit /todo → Reset ping timer immediately
           or
Owner /atodo @user → Reset target's ping timer
```

### Role Removal
```
5+ days of inactivity → Role automatically removed
→ User must rejoin with /todo
→ Owner can re-add with /addh
```

---

## 🛠️ ADMIN COMMANDS

### Add Member to TODO System
```
/addh 123456789
→ Adds user to active_members
→ Enables /todo command for user
→ Logged to TODO channel
```

### Remove Member from TODO System
```
/remh 123456789
→ Removes user from active_members
→ Disables /todo command
→ Logged to TODO channel
```

### List All Members
```
/members
→ Shows all users in active_members
→ Displays names (owner only)
```

### Debug System
```
/tododebug
→ Shows all active members
→ Lists all submissions
→ Verifies authorization
→ Owner only
```

---

## 🐛 COMMON ISSUES & FIXES

### "You must be in the active members list"
**Fix**: Contact owner to use `/addh <your_id>`

### "Invalid Date Format"
**Fix**: Use DD/MM/YYYY format (e.g., 29/01/2026)

### "Empty Submission"
**Fix**: Fill at least one category or attach a file

### File upload not working
**Fix**: Check file type is supported (images/documents only) and < 8MB

### Channel post didn't appear
**Fix**: Check bot has message send permission in TODO channel

### Ping timer not resetting
**Fix**: Ensure /todo/atodo submission was successful (check database)

---

## 📈 STATISTICS & TRACKING

### Tracked Data
```
✅ User ID
✅ Submission timestamp
✅ Feature name
✅ Date assigned
✅ Task categories
✅ Attachment metadata
✅ Submission ID
✅ Last ping time
✅ Owner assignment info
```

### Queries Available
```
/todostatus      → Personal status
/listtodo        → Current TODO details
/tododebug       → Full system status (owner)
```

---

## 🎓 EXAMPLES

### Example Submission 1: Text-Only
```
/todo
Feature: "User Dashboard UI"
Date: 29/01/2026
Must Do: "Create responsive layout, implement all widgets"
Can Do: "Add dark mode toggle"
Don't Do: "Don't use deprecated React APIs"
→ Submitted and posted to #todo-channel
```

### Example Submission 2: With Attachment
```
/todo
Feature: "Database Optimization"
Date: 29/01/2026
Must Do: "Attaching file"
[Upload: query_analysis.pdf]
→ Submitted with PDF attachment
→ Posted to channel with file link
```

### Example Submission 3: Owner Assignment
```
/atodo @developer
Feature: "API Rate Limiting"
Date: 29/01/2026
Must Do: "Implement token bucket algorithm"
Can Do: "Add monitoring dashboard"
Don't Do: "Don't block valid requests"
→ Posted as "Owner Assignment" (gold color)
→ Developer's ping timer reset
```

---

## ⚙️ TECHNICAL NOTES

### Timezone
```
All timestamps: Asia/Kolkata (IST)
+05:30 UTC offset
```

### Retry Logic
```
Database saves: 3 attempts
Delay between attempts: 0.5 seconds
Non-blocking channel sends
```

### Submission ID Format
```
user_id_timestamp_milliseconds[_atodo]
Example: "123456789_1706511234567"
Example: "123456789_1706511234567_atodo"
```

### Ping Timer
```
Reset value: 0
Set on: /todo or /atodo submission
Checked: Every 3 hours by todo_checker task
```

---

## 🚀 FEATURES SUMMARY

### ✅ Implemented
- Three-category form system
- Advanced validation
- Database persistence
- Auto-channel posting
- Owner assignment (/atodo)
- Attachment support
- Smart ping timer
- Comprehensive logging
- Error handling
- Authorization checks
- Unique submission tracking
- Timestamp recording

### 🎯 User Experience
- Clean modal form
- Clear error messages
- Responsive feedback
- Optional attachments
- 10-minute upload window
- Confirmation messages
- Easy next steps

### 🔒 Security
- Authorization validation
- Input validation
- File type checking
- Size limits
- Owner-only commands
- Database safety

---

## 📞 SUPPORT

### For Users
- Use `/todostatus` to check status
- Contact owner if blocked
- Upload evidence within 10 minutes

### For Owner
- Use `/tododebug` to diagnose issues
- Check database directly if needed
- Use `/addh` to authorize users

---

## 🎉 YOU'RE ALL SET!

The advanced TODO system is ready to use with:
- ✅ /todo command
- ✅ /atodo command
- ✅ Auto-channel posting
- ✅ Attachment support
- ✅ Owner assignment
- ✅ Smart authorization

**Happy tasking!** 🚀
