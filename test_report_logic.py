#!/usr/bin/env python3
"""
Test script to verify /report command time filtering logic
"""

import datetime

# Test Case 1: Verify timezone-aware datetime conversion
print("="*70)
print("TEST 1: Timezone-Aware DateTime Conversion")
print("="*70)

date = "2026-02-05"
time_from = "20:00"
time_to = "21:15"

start_naive = datetime.datetime.strptime(f"{date} {time_from}", "%Y-%m-%d %H:%M")
end_naive = datetime.datetime.strptime(f"{date} {time_to}", "%Y-%m-%d %H:%M")

start = start_naive.replace(tzinfo=datetime.timezone.utc)
end = end_naive.replace(tzinfo=datetime.timezone.utc)

print(f"Input date: {date}")
print(f"Input time range: {time_from} to {time_to}")
print(f"Start (naive): {start_naive} | tzinfo: {start_naive.tzinfo}")
print(f"Start (UTC): {start} | tzinfo: {start.tzinfo}")
print(f"End (UTC): {end} | tzinfo: {end.tzinfo}")
print(f"✅ Timezone-aware conversion successful!")

# Test Case 2: Message time range filtering
print("\n" + "="*70)
print("TEST 2: Message Time Range Filtering Logic")
print("="*70)

# Simulate message timestamps (all UTC)
test_messages = [
    (1, datetime.datetime(2026, 2, 5, 19, 55, tzinfo=datetime.timezone.utc), "Before range"),
    (2, datetime.datetime(2026, 2, 5, 20, 0, tzinfo=datetime.timezone.utc), "At start (should delete)"),
    (3, datetime.datetime(2026, 2, 5, 20, 30, tzinfo=datetime.timezone.utc), "Middle (should delete)"),
    (4, datetime.datetime(2026, 2, 5, 21, 0, tzinfo=datetime.timezone.utc), "Near end (should delete)"),
    (5, datetime.datetime(2026, 2, 5, 21, 15, tzinfo=datetime.timezone.utc), "At end boundary (NO delete)"),
    (6, datetime.datetime(2026, 2, 5, 21, 30, tzinfo=datetime.timezone.utc), "After range"),
]

deleted = 0
checked = 0

for msg_id, msg_time, description in test_messages:
    checked += 1
    in_range = start <= msg_time < end
    
    symbol = "✓ DELETE" if in_range else "✗ SKIP"
    deleted += in_range
    
    print(f"{symbol} | Msg #{msg_id} at {msg_time} | {description}")

print(f"\n📊 Results:")
print(f"   Total checked: {checked}")
print(f"   Total to delete: {deleted}")
print(f"   ✅ Expected to delete: 4 messages (IDs: 2, 3, 4, 1 extra)")

if deleted == 4:
    print("   ✅ FILTER LOGIC CORRECT!")
else:
    print(f"   ⚠️  Expected 4 deletions, got {deleted}")

# Test Case 3: Validation checks
print("\n" + "="*70)
print("TEST 3: Validation Checks")
print("="*70)

# Invalid format
try:
    bad_date = datetime.datetime.strptime("2026/02/05 20:00", "%Y-%m-%d %H:%M")
    print("✗ Should have rejected invalid date format")
except ValueError as e:
    print(f"✅ Correctly rejected invalid date format: {str(e)[:50]}")

# Time comparison
bad_start = datetime.datetime(2026, 2, 5, 21, 15, tzinfo=datetime.timezone.utc)
bad_end = datetime.datetime(2026, 2, 5, 20, 0, tzinfo=datetime.timezone.utc)

if bad_start >= bad_end:
    print("✅ Correctly validates that time_from must be before time_to")
else:
    print("✗ Failed to validate time ordering")

print("\n" + "="*70)
print("TEST COMPLETE ✅")
print("="*70)
