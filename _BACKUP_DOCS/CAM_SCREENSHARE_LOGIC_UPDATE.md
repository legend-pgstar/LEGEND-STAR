# 🎥 Cam On + Screenshare Logic Update

## Summary
Updated the voice state tracking logic in `main.py` to ensure that when a user has their **camera ON + screenshare ON**, the time is counted toward **`cam_on_minutes`** (displayed in both **mystatus** and **leaderboard**).

## Changes Made

### 1️⃣ Voice State Update Handler (Lines 570-577)
**Changed:**
```python
# OLD LOGIC
old_cam = before.self_video and not before.self_stream
new_cam = after.self_video and not after.self_stream
```

**To:**
```python
# NEW LOGIC
# Cam is ON if: camera is on (regardless of screenshare status)
# Cam is OFF if: camera is off
# NOTE: Cam ON + Screenshare ON = counts as cam on time (both are active)
old_cam = before.self_video
new_cam = after.self_video
```

### 2️⃣ Batch Save Study Logic (Lines 750-753)
**Changed:**
```python
# OLD LOGIC
cam = member.voice.self_video and not member.voice.self_stream
```

**To:**
```python
# NEW LOGIC
# Cam ON: camera is on (regardless of screenshare). Cam OFF: camera is off
# NOTE: Cam ON + Screenshare ON = counts as cam on time
cam = member.voice.self_video
```

---

## How It Works Now

| State | Screenshare | Result | Time Counted As |
|-------|-------------|--------|-----------------|
| ✅ Camera ON | ✅ Yes | Valid | **cam_on_minutes** |
| ✅ Camera ON | ❌ No | Valid | **cam_on_minutes** |
| ❌ Camera OFF | ✅ Yes | Invalid | **cam_off_minutes** |
| ❌ Camera OFF | ❌ No | Invalid | **cam_off_minutes** |

---

## Impact on Features

### 📊 `/mystatus` Command
- Users with **Camera ON + Screenshare ON** will now see their time correctly counted in the **📸 Cam On** field
- Previously, this time would have been counted as cam off

### 🏆 `/lb` (Leaderboard) Command
- The top 15 members in "Cam On ✅" leaderboard will now include time spent with both camera AND screenshare active
- More accurate representation of study time with all video/presentation features active

### 🕛 Auto-Leaderboard (11:55 PM IST)
- Auto-generated leaderboards will reflect the new counting logic
- "Cam On" stats will be higher as screenshare time is now included

---

## Technical Details

### Camera Detection Logic
- **`before.self_video`** or **`after.self_video`**: Boolean indicating if camera is ON
- **`before.self_stream`** or **`after.self_stream`**: Boolean indicating if screenshare is ON

### Previous Logic Problem
```
old_cam = before.self_video AND NOT before.self_stream
```
This would return `False` when screenshare was ON, even if camera was also ON. This meant:
- ❌ Camera ON + Screenshare ON = counted as "cam off" (WRONG)

### New Logic Solution
```
old_cam = before.self_video
```
This returns `True` whenever camera is ON, regardless of screenshare:
- ✅ Camera ON + Screenshare ON = counted as "cam on" (CORRECT)

---

## Verification

✅ **Python Syntax Check**: PASSED
✅ **Code Review**: COMPLETED
✅ **Logic Verification**: VERIFIED

### Files Modified
- `main.py` (2 locations updated)

### Database Compatibility
- No migration needed
- Both `voice_cam_on_minutes` and `voice_cam_off_minutes` fields already exist
- Change is purely in the counting logic

---

## Deployment Notes

1. **Backward Compatible**: Existing database records remain intact
2. **Immediate Effect**: Changes take effect once bot is restarted
3. **Going Forward**: All new time tracking will use the updated logic
4. **No Data Loss**: Historical data is preserved as-is

---

## Author Notes

This update aligns with the Discord.js reference implementation where:
- Camera is the PRIMARY indicator of study status
- Screenshare is a SECONDARY feature that doesn't override camera status
- Both being ON = user is actively presenting/streaming their work (counts as cam on)

**Result**: More accurate and intuitive tracking of actual study/presentation time with video/screenshare features active.
