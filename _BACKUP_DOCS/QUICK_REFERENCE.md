# 🚀 Quick Reference - Simplified TODO System

## Commands at a Glance

### `/todo` - Submit TODO
```
/todo feature:"..." date:"DD/MM/YYYY" [must_do:"..."] [can_do:"..."] [dont_do:"..."] [attachment:file]
```
- ✅ Posts publicly to channel
- ✅ File upload visible like /msz
- ✅ Immediate posting

### `/atodo` - Owner Assign  
```
/atodo user:@member feature:"..." date:"DD/MM/YYYY" [must_do:"..."] [can_do:"..."] [dont_do:"..."] [attachment:file]
```
- ✅ Owner-only access
- ✅ Gold color in channel
- ✅ Target verification

### `/listtodo` - View Current
```
/listtodo
```
- Shows your current TODO

### `/deltodo` - Delete
```
/deltodo
```
- Removes your TODO

### `/todostatus` - Check Status
```
/todostatus [user:@member]  (owner can check others)
```
- Shows last submit time
- Shows ping status

---

## File Support
```
Images:    PNG, JPG, JPEG, GIF, WEBP, BMP, TIFF
Documents: PDF, TXT, DOC, DOCX, XLSX, PPT, PPTX, CSV
Max Size:  8MB
```

---

## What's Different

| Old | New |
|-----|-----|
| Modal form | Slash command |
| Hidden buttons | Visible parameters |
| 10-min wait | Immediate |
| Confusing | Simple |
| Like nothing else | Like /msz |

---

## Error Messages

```
❌ Not authorized
   → Add yourself with /addh command

❌ Invalid date. Use DD/MM/YYYY format
   → Use date like: 29/01/2026

❌ Provide content or attachment
   → Add text OR file

❌ File too large (max 8MB)
   → Reduce file size

❌ File type not supported
   → Use PNG, JPG, PDF, DOCX, etc.
```

---

## Database Info

Stores in MongoDB:
- `feature_name` - What it is
- `date` - When (DD/MM/YYYY)
- `must_do` - Required (or "N/A")
- `can_do` - Optional (or "N/A")
- `dont_do` - Restrictions (or "N/A")
- `attachment` - File details (if uploaded)
- `submitted_at` - Timestamp
- `submitted_by` - Owner name (if /atodo)

---

## Ping System

- Runs every 3 hours
- Pings if 24+ hours no submit
- Only pings once per 3 hours (no spam)
- Removes role after 5 days inactive
- Resets on `/todo` submission

---

## Key Features

✅ Direct attachment upload (visible)
✅ Public posting (everyone sees)
✅ Simple command structure
✅ File validation (type & size)
✅ Database persistence
✅ Error handling
✅ Owner-only assignment
✅ Authorization checks
✅ Beautiful embeds
✅ Image previews

---

## Status

✅ Syntax validated
✅ Ready for production
✅ Backward compatible
✅ All documentation included

Deploy and test! 🚀
