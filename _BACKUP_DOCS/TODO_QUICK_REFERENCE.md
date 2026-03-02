# ⚡ TODO/ATODO Attachment Feature - Quick Reference

## 🎯 What's New?

### Option 1: Original (Still Works!)
```
/todo form with:
✔️ Must Do
🎯 Can Do  
❌ Don't Do
```

### Option 2: NEW - Add Screenshots! 📸
```
/todo with optional attachment
    ↓
[📸 Upload Screenshot] [✅ Done]
    ↓
Attach proof/evidence to your TODO
```

---

## 🚀 How to Use

### For Regular Users: `/todo`

**Step 1**: Type `/todo`
```
/todo → Opens form
```

**Step 2**: Fill the form
```
Name:       John Doe
Date:       29/01/2026
Must Do:    Complete project documentation
Can Do:     Add extra features
Don't Do:   Skip code review
```

**Step 3**: Get attachment options
```
After submit, you'll see:
[📸 Upload Screenshot]  ← Click to add image
[✅ Done]               ← Click when done
```

**Step 4**: Done! ✅
```
Final summary shows:
- All your tasks
- Attached screenshot (if added)
- Timestamp
```

---

### For Owner: `/atodo @user`

**Step 1**: Type `/atodo @username`
```
/atodo @john → Opens form
```

**Step 2**: Fill the form
```
(Same as /todo form)
```

**Step 3**: Submit with optional screenshot
```
[📸 Upload Screenshot]  ← Owner can add proof
[✅ Done]               ← Mark assignment complete
```

**Step 4**: User gets the TODO
```
User sees:
- Assigned by owner
- All task details
- Any attached screenshot
```

---

## 📸 Supported Files

| Format | Support | Size Limit |
|--------|---------|-----------|
| PNG    | ✅      | 8 MB      |
| JPG    | ✅      | 8 MB      |
| JPEG   | ✅      | 8 MB      |
| GIF    | ✅      | 8 MB      |
| WEBP   | ✅      | 8 MB      |

---

## 🎨 What Shows in TODO Channel?

```
═══════════════════════════════════════
✅ New TODO Submitted

👤 Submitted By: @John
📅 Date: 29/01/2026
📝 Name: John Doe

✔️ Must Do:
   Complete project documentation

🎯 Can Do:
   Optimize performance

❌ Don't Do:
   Skip testing

📎 Attachment: screenshot.png
   [IMAGE PREVIEW SHOWN]

Status: Submitted | User: 123456789
═══════════════════════════════════════
```

---

## ⚙️ Database (Behind the Scenes)

When you submit with attachment:
```json
{
  "todo": {
    "name": "John Doe",
    "date": "29/01/2026",
    "must_do": "...",
    "can_do": "...",
    "dont_do": "...",
    "attachment": {
      "url": "https://cdn.discordapp.com/...",
      "filename": "screenshot.png",
      "uploaded_at": "2026-01-29T14:30:00+05:30"
    }
  }
}
```

---

## 🔄 Ping System Reset

✅ **When you submit TODO** → Ping timer RESETS  
✅ **No pings for 3 hours after submit**  
✅ **Owner can reset ping via /atodo**

---

## ✨ Key Features

- ✅ **Backward Compatible**: Old TODOs still work
- ✅ **Optional Attachment**: Don't need to add one
- ✅ **Automatic Preview**: Images show in embeds
- ✅ **Secure Storage**: Uses Discord CDN
- ✅ **Time Tracking**: Timestamp in Kolkata timezone
- ✅ **Error Handling**: Clear messages if something goes wrong

---

## 🧪 Testing Commands

### Check it works:
```bash
python -m py_compile main.py
# Should show: ✅ Syntax check passed!
```

### Then run bot:
```bash
python main.py
# Should connect without errors
```

---

## 📋 Feature Comparison

| Feature | Before | After |
|---------|--------|-------|
| Must/Can/Don't Do | ✅ | ✅ |
| Attachment Support | ❌ | ✅ NEW |
| Image Preview | ❌ | ✅ NEW |
| Upload Screenshots | ❌ | ✅ NEW |
| Owner Todo (/atodo) | ✅ | ✅ Enhanced |
| Ping Reset | ✅ | ✅ |
| Database Storage | ✅ | ✅ Enhanced |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Button not showing | Refresh discord |
| Can't upload file | Check file size (< 8MB) |
| Image doesn't preview | Ensure it's PNG/JPG/GIF/WEBP |
| Not authorized | Ensure you're in active members |
| Owner only error | Use correct discord account |

---

## 💡 Pro Tips

1. **Screenshot Pro**: Use Windows + Shift + S for quick screenshots
2. **Multiple Tasks**: Each field can have multiple lines
3. **Date Format**: Always use DD/MM/YYYY format
4. **Owner Power**: Owners can submit on behalf of anyone
5. **Evidence**: Attach proof of work for accountability

---

## 🚀 Version Info

**Update**: TODO & ATODO with Attachment Support  
**Version**: 2.0  
**Date**: January 29, 2026  
**Status**: ✅ Production Ready  

---

**Need help?** Check the full documentation in `TODO_ATTACHMENT_UPDATE.md`
