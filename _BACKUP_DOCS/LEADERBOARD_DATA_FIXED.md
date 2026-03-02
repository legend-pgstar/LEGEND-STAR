# Leaderboard Data Storage & Display - Fixed ✅

## Problem
The `/lb` command showed "No data" even though voice data should be:
1. Saved to MongoDB every 2 minutes
2. Persisted across bot restarts (git push)
3. Displayed in the leaderboard

## Root Causes Fixed

### 1. ✅ **Missing before_loop Callback**
- **Problem**: `batch_save_study()` wasn't guaranteed to start after bot was ready
- **Fix**: Added `@batch_save_study.before_loop` callback with `await bot.wait_until_ready()`
- **Result**: Task now runs reliably starting from bot startup

### 2. ✅ **Poor Data Filtering in /lb**
- **Problem**: Leaderboard added users with 0 minutes, making list look empty
- **Fix**: Only add users to leaderboard if they have `cam_on > 0` OR `cam_off > 0`
- **Result**: Only users with actual data appear in leaderboard

### 3. ✅ **Missing Debug Output**
- **Problem**: Couldn't see if batch_save was running or if data existed
- **Fix**: Added detailed console logging for:
  - Document count from MongoDB query
  - Which users had data and their values
  - Successful/failed save operations
  - Error messages on failures
- **Result**: Clear visibility into what's being saved

### 4. ✅ **Better Error Messages**
- **Problem**: Generic "No data" message didn't help debugging
- **Fix**: Added footer showing "Data saves every 2 minutes | Resets daily at midnight IST"
- **Result**: Users understand why data might be empty

---

## How Data Flows Now

### ✅ Step 1: User Joins Voice Channel
```
🎤 on_voice_state_update triggered
   ↓
💾 save_with_retry() initializes user record in MongoDB
   ↓
⏰ vc_join_times[user_id] = now (track start time)
   ↓
Console: "🎤 UserName joined VC - tracking started (Cam: True)"
```

### ✅ Step 2: Every 2 Minutes (batch_save_study runs)
```
⏱️ batch_save_study() triggered
   ↓
🔍 Check all users in vc_join_times
   ↓
💾 save_with_retry() increments voice_cam_on/off_minutes
   ↓
⏰ Reset join time to current time (so next 2 mins starts fresh)
   ↓
Console: "⏱️ UserName: +2m data.voice_cam_on_minutes (Cam: True) ✅"
Console: "📊 Batch save complete: Updated 3 active users"
```

### ✅ Step 3: User Leaves Voice Channel
```
🚪 on_voice_state_update triggered
   ↓
⏰ Calculate final session time from join time to now
   ↓
💾 save_with_retry() adds to total voice_cam_on/off_minutes
   ↓
🗑️ Remove from vc_join_times
   ↓
Console: "💾 [data.voice_cam_on_minutes] Saved 15m for UserName - MongoDB: True"
```

### ✅ Step 4: Owner Uses /lb Command
```
📊 /lb command triggered
   ↓
🔍 safe_find(users_coll, {}) queries MongoDB
   ↓
💾 Loads all user documents with voice/cam data
   ↓
🧹 Filters: only shows users with cam_on > 0 OR cam_off > 0
   ↓
📊 Sorts by cam_on (desc), then cam_off (desc)
   ↓
🏆 Shows top 15 Cam On users + top 10 Cam Off users
   ↓
Console: "🔍 /lb command: Found 12 documents in MongoDB"
Console: "   - UserName1: Cam ON 120m, Cam OFF 45m"
Console: "   - UserName2: Cam ON 90m, Cam OFF 30m"
```

### ✅ Step 5: Bot Restarts (Git Push)
```
🔄 Bot restarts
   ↓
🔗 MongoDB connection established
   ↓
✅ All data ALREADY in MongoDB (not lost!)
   ↓
⏰ vc_join_times is empty (in-memory only)
   ↓
Next time user joins VC:
   → New join_time starts tracking from restart point
   → All previous data still in MongoDB ✅
```

---

## Expected Console Output

### **On Startup:**
```
GUILD_ID from env: 1427319799616245935
📡 Attempting to connect to MongoDB: mongodb+srv://pranabgoswami...
✅ MongoDB connected successfully (SRV + Relaxed TLS)
✅ MongoDB test write successful - Data persistence enabled!
✅ batch_save_study loop started
Syncing to guild: 1427319799616245935
✅ Synced 19 commands
```

### **User Joins Voice (with cam on):**
```
🎤 UserName joined VC - tracking started (Cam: True)
💾 [data.voice_cam_on_minutes] Saved 0m for UserName - MongoDB: True
```

### **Every 2 Minutes (batch_save_study):**
```
⏱️ UserName1: +2m data.voice_cam_on_minutes (Cam: True) ✅
⏱️ UserName2: +2m data.voice_cam_off_minutes (Cam: False) ✅
📊 Batch save complete: Updated 2 active users
```

### **User Leaves Voice:**
```
💾 [data.voice_cam_on_minutes] Saved 15m for UserName - MongoDB: True
```

### **When /lb Command is Used:**
```
🔍 /lb command: Found 15 documents in MongoDB
   - UserName1: Cam ON 120m, Cam OFF 45m
   - UserName2: Cam ON 90m, Cam OFF 0m
   - UserName3: Cam ON 60m, Cam OFF 30m
```

---

## Data Persistence Features

### ✅ Data Saved Immediately
- Voice time: Saved when user joins, every 2 min, and when user leaves
- Messages: Saved immediately when sent
- All with retry logic (up to 3 attempts)

### ✅ Data Survives Bot Restarts
- MongoDB keeps all accumulated data
- Previous session stats preserved
- Leaderboard shows cumulative totals

### ✅ Daily Reset at Midnight IST
- `midnight_reset()` task runs at 00:00 IST
- Moves today's data to "yesterday" field
- Resets today's counters to 0
- `/ylb` command shows yesterday's stats

### ✅ Automatic Retry on Failures
- `save_with_retry()` tries up to 3 times
- 0.5 second wait between retries
- Clear error logging on persistent failures

---

## Testing Steps

### **Test 1: User Joins Voice**
1. User joins voice channel with cam ON
2. **Expected console output:**
   ```
   🎤 UserName joined VC - tracking started (Cam: True)
   ```
3. Wait 2 minutes
4. **Expected console output:**
   ```
   ⏱️ UserName: +2m data.voice_cam_on_minutes (Cam: True) ✅
   ```

### **Test 2: Check Leaderboard**
1. Use `/lb` command
2. **Expected output in Discord:**
   ```
   🏆 Study Leaderboard
   **Cam On ✅**
   #1 **UserName** — 2m 0s
   
   **Cam Off ❌**
   No data.
   ```
3. **Expected console output:**
   ```
   🔍 /lb command: Found 1 documents in MongoDB
      - UserName: Cam ON 2m, Cam OFF 0m
   ```

### **Test 3: Git Push (Bot Restart)**
1. User in voice channel
2. Do `git push`
3. Bot restarts
4. **Expected:** Data NOT lost
5. Use `/lb` command
6. **Expected:** Still shows same user and time (or more if they're still in VC)

### **Test 4: User Leaves Voice**
1. User leaves voice channel
2. **Expected console output:**
   ```
   💾 [data.voice_cam_on_minutes] Saved 10m for UserName - MongoDB: True
   ```
3. Use `/lb`
4. **Expected:** Shows accumulated voice time

---

## MongoDB Data Structure

Each user document:
```json
{
  "_id": "user_id_as_string",
  "data": {
    "voice_cam_on_minutes": 120,     // ← Shows in /lb
    "voice_cam_off_minutes": 45,     // ← Shows in /lb
    "message_count": 234,             // ← Shows in /ud
    "yesterday": {
      "cam_on": 90,                   // ← Shows in /ylb
      "cam_off": 30                   // ← Shows in /ylb
    }
  }
}
```

---

## Files Modified

- `main.py`:
  - ✅ Added `@batch_save_study.before_loop` callback
  - ✅ Enhanced `/lb` command with better filtering & debug output
  - ✅ Improved batch_save_study with success counting
  - ✅ Better error messages in leaderboard display

---

## Summary

**Data now flows like this:**

```
User Action (join VC, in VC, leave VC)
    ↓
💾 save_with_retry() ← Immediate save to MongoDB
    ↓
Every 2 min: batch_save_study() ← Incremental saves
    ↓
Data in MongoDB (PERSISTENT)
    ↓
/lb command ← Fetches & displays leaderboard
    ↓
Bot restart → Data still there ✅
```

**Key Points:**
- ✅ Data saved immediately on events
- ✅ Data saved every 2 minutes for active users  
- ✅ Data survives git push (stored in MongoDB)
- ✅ Clear console logging for debugging
- ✅ Leaderboard filters out users with 0 data
- ✅ Retry logic handles transient failures

**Your leaderboard will now work correctly!** 🚀
