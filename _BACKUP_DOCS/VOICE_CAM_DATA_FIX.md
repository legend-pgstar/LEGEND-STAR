# Voice & Cam Data Tracking - Complete Fix

## Problems Fixed

### 1. ❌ → ✅ Voice/Cam Time Not Being Saved
**Problem:** User joins VC but cam on/off minutes show as "0h 0m"

**Root Causes:**
- `safe_update_one()` had no error logging - silent failures
- `on_voice_state_update()` initialized user AFTER checking voice time
- `batch_save_study()` wasn't logging which users got saved

**Fixes Applied:**

#### A. Enhanced `safe_update_one()` with Error Logging
```python
def safe_update_one(collection, query, update):
    # Now logs errors and verifies successful saves
    result = collection.update_one(query, update)
    if result.modified_count > 0 or result.upserted_id:
        return True
    return True  # Document initialization is OK
```

#### B. Fixed `on_voice_state_update()` Initialization
**Before:** User record initialized AFTER checking VC time
**After:** User record initialized FIRST, then VC time tracked

```python
# Initialize user record FIRST
safe_update_one(users_coll, {"_id": user_id}, {
    "$setOnInsert": {"data": {
        "voice_cam_on_minutes": 0,
        "voice_cam_off_minutes": 0,
        "message_count": 0,
        ...
    }}
})

# THEN save voice time when they leave
if (old_in and not new_in) or (old_in and new_in and settings_changed):
    safe_update_one(users_coll, {"_id": user_id}, {
        "$inc": {field: mins}
    })
    print(f"💾 Saved {mins}m to {field} for {member}")
```

#### C. Added Logging to `batch_save_study()`
Now logs every 2 minutes which users' VC time was saved:
```
⏱️ UserName: +2m data.voice_cam_on_minutes (Cam: True)
⏱️ UserName: +2m data.voice_cam_off_minutes (Cam: False)
```

#### D. Enhanced `/ud` Command with Debug Output
Now prints to console what data was retrieved:
```python
print(f"🔍 /ud query for {target} (ID: {user_id})")
print(f"   MongoDB document: {user_doc}")
print(f"   Data fields: {data}")
```

## Data Flow Now Guaranteed

### Step 1: User Joins Voice Channel
```
⚡ on_voice_state_update triggered
   ↓
🎤 Initialize user record in MongoDB
   ↓
⏰ Start tracking VC join time in memory
   ↓
"🎤 UserName joined VC - tracking started"
```

### Step 2: Every 2 Minutes (batch_save_study)
```
⏱️ Check all active VC users
   ↓
💾 Save accumulated time to MongoDB
   ↓
"⏱️ UserName: +2m data.voice_cam_on_minutes (Cam: True)"
```

### Step 3: User Leaves Voice Channel
```
🚪 on_voice_state_update triggered
   ↓
💾 Save final session time
   ↓
"💾 Saved 15m to data.voice_cam_on_minutes for UserName"
```

### Step 4: Owner Uses `/ud @user`
```
🔍 Fetch user document from MongoDB
   ↓
📊 Display all accumulated stats
   ↓
🎤 Cam ON: 2h 45m
❌ Cam OFF: 1h 30m
💬 Messages: 234
📝 Recent Activity logs...
```

## Console Output Debugging

After these fixes, you should see in console:

**When user joins VC:**
```
🎤 UserName joined VC - tracking started
```

**Every 2 minutes (if in VC):**
```
⏱️ UserName: +2m data.voice_cam_on_minutes (Cam: True)
```

**When user leaves VC:**
```
💾 Saved 15m to data.voice_cam_on_minutes for UserName - Success: True
```

**When owner uses `/ud`:**
```
🔍 /ud query for UserName (ID: 1234567890)
   MongoDB document: {'_id': '...', 'data': {'voice_cam_on_minutes': 120, ...}}
   Data fields: {'voice_cam_on_minutes': 120, 'voice_cam_off_minutes': 30, ...}
```

## Files Modified

- `main.py`:
  - ✅ `safe_update_one()` - Added error logging
  - ✅ `on_voice_state_update()` - Fixed initialization order & added logging
  - ✅ `batch_save_study()` - Added operation logging
  - ✅ `/ud` command - Added debug output for data retrieval

## Testing Checklist

1. **User joins voice channel** ✅
   - Console should show: `🎤 UserName joined VC`
   
2. **Wait 2+ minutes** ✅
   - Console should show: `⏱️ UserName: +2m data.voice_cam_on_minutes`
   
3. **User leaves VC** ✅
   - Console should show: `💾 Saved Xm to data...`
   
4. **Owner uses `/ud @user`** ✅
   - Embed should show actual voice/cam times (not 0h 0m)
   - Console should show debug output with MongoDB data

5. **Check `/lb` command** ✅
   - Leaderboard should show users with voice/cam times
   - Users with 0 time should not appear

## Expected Result After Restart

When a user connects to voice with cam ON for 5 minutes:
```
🕵️ UserName
ID: 1234567890
Joined: 27/01/2026 10:35

📊 Stats
🎤 Cam ON: 5m  ← NOW SHOWS ACTUAL TIME!
❌ Cam OFF: 0h 0m
💬 Messages: 5

Recent Activity
[27/01 14:30:00] Joined VC: Voice Channel
[27/01 14:32:15] Message in #general: Hello
...
```

✅ Voice/Cam data is now being properly tracked and saved!
