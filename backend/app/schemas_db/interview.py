from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from .common import MongoDBModel, PyObjectId

class InterviewStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class InterviewMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class InterviewResult(BaseModel):
    is_passed: bool
    score: int  # 0~100
    feedback: str # Renamed from feedback_message to match db_schema.md
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)

class InterviewMeta(BaseModel):
    subject: str            # 대상 과목 (renamed from skill_slug)
    track: Optional[str] = None # (Optional) 문맥 트랙 (renamed from track_slug)
    target_level: int       # 도전 레벨 (1, 2, 3)
    status: InterviewStatus = InterviewStatus.IN_PROGRESS
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

class Interview(MongoDBModel):
    """
    [Collection]: interviews
    면접 세션 로그 및 평가 Snapshot
    """
    user_id: PyObjectId  # users._id 참조
    
    meta: InterviewMeta
    messages: List[InterviewMessage] = []
    result: Optional[InterviewResult] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "60d5ecb8...",
                "meta": {
                    "subject": "Python Syntax & Types",
                    "target_level": 2,
                    "status": "IN_PROGRESS"
                },
                "messages": [
                    {"role": "assistant", "content": "질문..."}
                ]
            }
        }
