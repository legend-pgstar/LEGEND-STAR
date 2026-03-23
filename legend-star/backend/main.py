import os
import uvicorn
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Header, HTTPException, Request, Query, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
API_KEY = os.getenv("API_KEY")
PORT = int(os.getenv("PORT", "8000"))

if not MONGO_URL:
    raise RuntimeError("MONGO_URL should be set in environment")
if not API_KEY:
    raise RuntimeError("API_KEY should be set in environment")

app = FastAPI(title="Legend Star Monitoring API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient(MONGO_URL)
db = client["legend_star"]
logs_collection = db["logs"]
control_collection = db["control"]


class LogItem(BaseModel):
    type: str = Field(..., regex="^(message|command|error|user|system)$")
    user: Optional[str] = None
    user_id: Optional[int] = None
    guild: Optional[str] = None
    content: Optional[str] = None
    command: Optional[str] = None
    error: Optional[str] = None
    time: Optional[str] = None


class ControlAction(BaseModel):
    action: str = Field(..., regex="^(send_message|get_status)$")
    channel_id: Optional[int] = None
    message: Optional[str] = None


def validate_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)


manager = ConnectionManager()


@app.post("/log", dependencies=[Depends(validate_api_key)])
async def create_log(log: LogItem, request: Request):
    record = log.dict(exclude_none=True)
    record["received_from"] = request.client.host
    record["time"] = datetime.now(timezone.utc).isoformat()

    inserted = await logs_collection.insert_one(record)
    doc = {**record, "id": str(inserted.inserted_id)}
    await manager.broadcast(doc)

    return {"status": "ok", "id": str(inserted.inserted_id), "time": record["time"]}


@app.post("/control", dependencies=[Depends(validate_api_key)])
async def control_endpoint(action_data: ControlAction):
    if action_data.action == "get_status":
        return {"status": "ok", "bot_online": True, "detail": "Bot is running"}

    if action_data.action == "send_message":
        if not action_data.channel_id or not action_data.message:
            raise HTTPException(status_code=400, detail="channel_id and message are required")

        control_doc = {
            "action": "send_message",
            "channel_id": action_data.channel_id,
            "message": action_data.message,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        inserted = await control_collection.insert_one(control_doc)

        return {"status": "ok", "action_id": str(inserted.inserted_id), "detail": "queued"}

    raise HTTPException(status_code=400, detail="Unsupported action")


@app.get("/control", dependencies=[Depends(validate_api_key)])
async def get_control_actions():
    pending = []
    cursor = control_collection.find({"status": "pending"}).sort("created_at", 1).limit(10)
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        pending.append(doc)
    return pending


@app.post("/control/ack", dependencies=[Depends(validate_api_key)])
async def ack_control_action(action_id: str, status: str = "done"):
    if status not in ["done", "failed"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    try:
        oid = ObjectId(action_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid action_id")

    updated = await control_collection.update_one(
        {"_id": oid},
        {"$set": {"status": status, "updated_at": datetime.now(timezone.utc).isoformat()}},
    )
    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail="Action not found")

    return {"status": "ok", "action_id": action_id, "new_status": status}


@app.get("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/logs")
async def get_logs(limit: int = Query(100, ge=1, le=100), skip: int = Query(0, ge=0)):
    cursor = logs_collection.find().sort("time", -1).skip(skip).limit(limit)
    docs = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        docs.append(doc)
    return docs


@app.get("/analytics")
async def get_analytics():
    total_messages = await logs_collection.count_documents({"type": "message"})
    total_commands = await logs_collection.count_documents({"type": "command"})
    total_errors = await logs_collection.count_documents({"type": "error"})
    active_users = len([u for u in await logs_collection.distinct("user_id") if u is not None])

    return {
        "total_messages": total_messages,
        "total_commands": total_commands,
        "total_errors": total_errors,
        "active_users": active_users,
    }


@app.get("/errors")
async def get_errors(limit: int = Query(100, ge=1, le=100), skip: int = Query(0, ge=0)):
    cursor = logs_collection.find({"type": "error"}).sort("time", -1).skip(skip).limit(limit)
    docs = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        docs.append(doc)
    return docs


@app.get("/users")
async def get_users(limit: int = Query(100, ge=1, le=1000), skip: int = Query(0, ge=0)):
    pipeline = [
        {"$match": {"user_id": {"$ne": None}}},
        {"$group": {"_id": {"user_id": "$user_id", "user": "$user"}, "actions": {"$sum": 1}}},
        {"$sort": {"actions": -1}},
        {"$skip": skip},
        {"$limit": limit},
    ]
    users = []
    async for doc in logs_collection.aggregate(pipeline):
        users.append({"user_id": doc["_id"]["user_id"], "user": doc["_id"]["user"], "actions": doc["actions"]})
    return users


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
