#!/usr/bin/env python3
"""Diagnostic script to check MongoDB data structure and contents"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    print("❌ MONGODB_URI not set in .env")
    exit(1)

try:
    print("🔗 Connecting to MongoDB...")
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
    
    # Count documents
    doc_count = users_coll.count_documents({})
    print(f"\n📊 Total documents in users collection: {doc_count}")
    
    if doc_count == 0:
        print("⚠️ No documents found!")
        exit(0)
    
    # Show first document structure
    first_doc = users_coll.find_one({})
    print(f"\n📄 First document sample:")
    print(f"   _id: {first_doc.get('_id')} (type: {type(first_doc.get('_id')).__name__})")
    print(f"   Keys: {list(first_doc.keys())}")
    
    # Check data structure
    data = first_doc.get("data", {})
    print(f"\n   data keys: {list(data.keys())}")
    print(f"   voice_cam_on_minutes: {data.get('voice_cam_on_minutes', 'NOT FOUND')}")
    print(f"   voice_cam_off_minutes: {data.get('voice_cam_off_minutes', 'NOT FOUND')}")
    
    # Show all documents with their cam times
    print(f"\n📋 All documents summary:")
    print("=" * 80)
    for doc in users_coll.find({}, limit=100):
        user_id = doc.get('_id')
        data = doc.get('data', {})
        cam_on = data.get('voice_cam_on_minutes', 0)
        cam_off = data.get('voice_cam_off_minutes', 0)
        print(f"  ID: {user_id} | CAM_ON: {cam_on:4}min | CAM_OFF: {cam_off:4}min")
    
    print("=" * 80)
    print(f"\n✅ Database check complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
