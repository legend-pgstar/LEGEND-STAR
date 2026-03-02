# Critical MongoDB Conflict Fix - All Issues Resolved

## Problems Found & Fixed

### 🔴 **Problem 1: MongoDB Update Conflict**

**Error Message:**
```
⚠️ Save attempt failed: Updating the path 'data' would create a conflict at 'data'
```

**Root Cause:**
Using both `$inc` and `$setOnInsert` on the same 'data' path in one operation:
```python
# BROKEN: This causes conflict
result = save_with_retry(users_coll, {"_id": str(uid)}, {
    "$inc": {data.field: mins},        # Modify existing 'data'
    "$setOnInsert": {data: {...}}      # Try to create entire 'data' object
})
```

MongoDB sees two conflicting operations on the same path!

**Solution:**
Split into **two separate operations**:
```python
# FIXED: Do one operation at a time
# Step 1: Create document with default values if it doesn't exist
users_coll.update_one(
    {"_id": str(uid)},
    {"$setOnInsert": {"data": {...}}},
    upsert=True
)

# Step 2: Then increment the specific field
result = save_with_retry(users_coll, {"_id": str(uid)}, {
    "$inc": {field: mins}
})
```

Now:
- First operation creates document with initial values
- Second operation increments the field (no conflict!)

---

### 🔴 **Problem 2: Async/Await Bug**

**Error Message:**
```
RuntimeWarning: coroutine 'sleep' was never awaited
  asyncio.sleep(0.5)  # Wait before retry
```

**Root Cause:**
Using `asyncio.sleep()` (async function) in synchronous code without `await`:
```python
# BROKEN: asyncio.sleep is a coroutine, needs await
asyncio.sleep(0.5)
```

**Solution:**
Use `time.sleep()` for synchronous code:
```python
# FIXED: time.sleep works in synchronous code
import time
time.sleep(0.5)
```

---

### 🔴 **Problem 3: Test Document in Leaderboard**

**Error Message:**
```
⚠️ Error processing doc: invalid literal for int() with base 10: 'mongodb_test'
```

**Root Cause:**
The test document created during startup (`mongodb_test`) was being queried as a user:
```python
# Leaderboard tries to convert string "mongodb_test" to int
user_id = int(doc["_id"])  # Crashes! "mongodb_test" is not a number
```

**Solution:**
Filter out the test document before processing:
```python
# FIXED: Skip the test document
for doc in docs:
    if doc["_id"] == "mongodb_test":
        continue
    
    user_id = int(doc["_id"])  # Now safe!
```

---

## Impact of Fixes

### Before Fix:
```
⚠️ Save attempt 1 failed: Updating the path 'data' would create a conflict
⚠️ Save attempt 2 failed: Updating the path 'data' would create a conflict
⚠️ Save attempt 3 failed: Updating the path 'data' would create a conflict
❌ Failed to save after 3 attempts

Result: Data NOT saved to MongoDB ❌
Only 1 user shows in leaderboard instead of 5 ❌
```

### After Fix:
```
⏱️ SuMyth: +2m data.voice_cam_on_minutes (Cam: True) ✅
⏱️ Unspoken Archieve: +2m data.voice_cam_on_minutes (Cam: True) ✅
⏱️ T O R O: +2m data.voice_cam_on_minutes (Cam: True) ✅
⏱️ ! Mitochondria: +2m data.voice_cam_on_minutes (Cam: True) ✅
⏱️ SHAKTI VAKT: +2m data.voice_cam_on_minutes (Cam: True) ✅
📊 Batch save complete: Updated 5 active members in voice

Result: All 5 users' data saved successfully! ✅
All 5 users appear in leaderboard! ✅
```

---

## Technical Details

### MongoDB Operation Separation Pattern

**Pattern for document creation with data accumulation:**

```python
# Step 1: Ensure document exists with default structure
collection.update_one(
    query,
    {"$setOnInsert": {
        "field1": default_value_1,
        "field2": default_value_2,
        ...
    }},
    upsert=True
)

# Step 2: Update specific fields
collection.update_one(
    query,
    {"$inc": {
        "field1": increment_amount
    }}
)
```

This avoids MongoDB's "conflict on path" error by:
1. Not trying to do both operations at once
2. Letting `$setOnInsert` handle initial creation
3. Then using `$inc` for cumulative updates

---

## Files Modified

- **`main.py`**:
  - ✅ Fixed `batch_save_study()` - Separated MongoDB operations
  - ✅ Fixed `save_with_retry()` - Changed `asyncio.sleep()` to `time.sleep()`
  - ✅ Fixed leaderboard query - Filter out test document

---

## Console Output Now Shows

```
✅ safe_find returned 5 documents
🔍 /lb command: Found 5 total documents in MongoDB
   ℹ️  Fetching data from all 5 users...
   Guild has 104 members
   - Unspoken Archieve: Cam ON 73m, Cam OFF 0m (Total: 73m)
   - SHAKTI VAKT: Cam ON 0m, Cam OFF 0m (Total: 0m)
   - SuMyth: Cam ON 65m, Cam OFF 0m (Total: 65m)
   - T O R O: Cam ON 64m, Cam OFF 0m (Total: 64m)
   - ! Mitochondria: Cam ON 63m, Cam OFF 0m (Total: 63m)
   ✅ Processed 5 documents, 5 have data
```

✅ **All users tracked, all data saved, all showing in leaderboard!**

---

## Testing Checklist

- [x] No more MongoDB conflict errors
- [x] No more asyncio warnings
- [x] Test document filtered from leaderboard
- [x] All 5 users' data saved successfully
- [x] All 5 users appear in `/lb` leaderboard
- [x] Batch save runs every 2 minutes successfully
- [x] `/mystatus` shows correct stats for each user

---

## Summary

✅ **All 3 critical issues fixed and deployed!**

The bot now:
- ✅ Saves all user voice data without MongoDB conflicts
- ✅ Properly handles async operations (no more warnings)
- ✅ Shows accurate leaderboard data for all active users
- ✅ Runs stable every 2 minutes

**Live and working!** 🚀
