from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr
from .common import MongoDBModel

# --- Sub Models (Embedded Documents) ---

class AuthInfo(BaseModel):
    email: EmailStr
    provider: str  # e.g., 'kakao', 'google'
    uid: str       # Provider's unique user ID

class UserProfile(BaseModel):
    nickname: str
    avatar_url: Optional[str] = None
    job_title: Optional[str] = None

class UserStats(BaseModel):
    total_stars: int = 0
    completed_tracks: List[str] = []

class SubjectProgress(BaseModel):
    """
    사용자의 과목(Subject)별 진행 상황
    """
    level: int = 0  # 0: Locked, 1: Basic, 2: Adv, 3: Master
    stars: int = 0
    last_tested_at: Optional[datetime] = None

# --- Main Collection Model ---

class User(MongoDBModel):
    """
    [Collection]: users
    사용자 정보 및 학습 상태(Skill Tree)를 저장
    """
    auth: AuthInfo
    profile: UserProfile
    stats: UserStats = Field(default_factory=UserStats)
    
    # [User State] 학습 진행도
    # Key: Subject Title (e.g., 'FastAPI Essentials') -> 빠른 조회를 위해 Map 구조 사용
    skill_tree: Dict[str, SubjectProgress] = Field(default_factory=dict)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "auth": {
                    "email": "user@example.com",
                    "provider": "kakao",
                    "uid": "12345"
                },
                "profile": {
                    "nickname": "AI_Master"
                },
                "skill_tree": {
                    "FastAPI Essentials": {"level": 2, "stars": 2}
                }
            }
        }
