from fastapi import FastAPI, APIRouter, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


# ─── Models ────────────────────────────────────────────────────────────────────

class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class LeaderboardCreate(BaseModel):
    name: str
    score: int
    level: int
    mode: str = 'story'

class LeaderboardEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    score: int
    level: int
    mode: str = 'story'
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ─── Status Routes ─────────────────────────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Aqua Quest API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks


# ─── Leaderboard Routes ────────────────────────────────────────────────────────

@api_router.post("/leaderboard", response_model=LeaderboardEntry)
async def submit_score(payload: LeaderboardCreate):
    # Sanitize name: uppercase, max 6 chars
    name = payload.name.strip().upper()[:6] or "AAA"
    entry = LeaderboardEntry(
        name=name,
        score=payload.score,
        level=payload.level,
        mode=payload.mode,
    )
    doc = entry.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.leaderboard.insert_one(doc)
    return entry

@api_router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    mode: Optional[str] = Query(default=None),
    limit: int = Query(default=10, le=50),
):
    query = {}
    if mode:
        query['mode'] = mode
    entries = await db.leaderboard.find(query, {"_id": 0}).sort('score', -1).limit(limit).to_list(limit)
    for e in entries:
        if isinstance(e.get('timestamp'), str):
            e['timestamp'] = datetime.fromisoformat(e['timestamp'])
    return entries


# ─── App Setup ─────────────────────────────────────────────────────────────────

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
