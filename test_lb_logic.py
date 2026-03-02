#!/usr/bin/env python3
"""Test the leaderboard logic with real MongoDB data"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    print("❌ MONGODB_URI not set in .env")
    exit(1)

# Import leaderboard formatter
from leaderboard import generate_leaderboard_text

try:
    print("="*80)
    print("LEADERBOARD TESTER - Simulating /lb command")
    print("="*80)
    
    print("\n🔗 Connecting to MongoDB...")
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=20000,
        connectTimeoutMS=20000,
        socketTimeoutMS=20000,
        tlsAllowInvalidCertificates=True,
        retryWrites=True,
        directConnection=False
    )
    client.admin.command('ping')
    print("✅ Connected to MongoDB")
    
    db = client["legend_star"]
    users_coll = db["users"]
    
    # Fetch documents like /lb does
    docs = list(users_coll.find({}, limit=100))
    print(f"\n🔍 Found {len(docs)} total documents in MongoDB")
    
    # Process data like /lb does
    active = []
    
    for idx, doc in enumerate(docs):
        try:
            # Get user ID (handle both string and int)
            user_id_str = str(doc.get("_id", "")).strip()
            
            # Skip invalid IDs (like "mongodb_test")
            if not user_id_str or not user_id_str.isdigit():
                print(f"   ⚠️ Skipping invalid ID: {user_id_str}")
                continue
            
            user_id = int(user_id_str)
            data = doc.get("data", {})
            cam_on = data.get("voice_cam_on_minutes", 0)
            cam_off = data.get("voice_cam_off_minutes", 0)
            
            # Skip users with no data
            if cam_on == 0 and cam_off == 0:
                continue
            
            # Use user ID as display name (simulating fallback)
            display_name = f"User_{user_id}"
            
            active.append({"name": display_name, "cam_on": cam_on, "cam_off": cam_off})
            print(f"   ✅ {display_name}: CAM_ON={cam_on}min, CAM_OFF={cam_off}min")
                
        except Exception as e:
            print(f"   ⚠️ Error processing doc {idx}: {str(e)[:80]}")

    print(f"\n   📊 Total active users with data: {len(active)}")
    
    if not active:
        print(f"   ℹ️  No users with study time found")
        leaderboard_text = generate_leaderboard_text([], [])
    else:
        sorted_on = sorted(active, key=lambda x: x["cam_on"], reverse=True)
        sorted_off = sorted(active, key=lambda x: x["cam_off"], reverse=True)

        cam_on_data = [(u["name"], u["cam_on"]) for u in sorted_on]
        cam_off_data = [(u["name"], u["cam_off"]) for u in sorted_off]

        print(f"   CAM_ON sorted: {cam_on_data}")
        print(f"   CAM_OFF sorted: {cam_off_data}")

        leaderboard_text = generate_leaderboard_text(cam_on_data, cam_off_data)
    
    if leaderboard_text is None:
        print(f"⚠️ ERROR: generate_leaderboard_text returned None!")
    else:
        print("\n" + "="*80)
        print("LEADERBOARD OUTPUT:")
        print("="*80)
        print(leaderboard_text)
        print("="*80)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
