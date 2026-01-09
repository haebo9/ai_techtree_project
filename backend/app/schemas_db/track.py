from datetime import datetime
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field
from .common import MongoDBModel, PyObjectId

# --- Nested Structures for Track ---

class TrackSubject(BaseModel):
    """
    개별 학습 주제 (Subject)
    Levels를 포함하는 실제 학습 단위
    """
    title: str  # e.g., "FastAPI Essentials"
    # Key: "Lv1", "Lv2", "Lv3" -> Value: List of concept strings
    levels: Dict[str, List[str]] = Field(default_factory=dict)

class TrackBranchOption(BaseModel):
    """
    선택 분기점의 각 옵션 (Option)
    """
    option_name: str  # e.g., "Option 1: Serving Specialist"
    subjects: List[TrackSubject]

class TrackStep(BaseModel):
    """
    커리큘럼의 단계 (Step)
    필수(Fixed) 또는 분기(Branch) 타입을 가짐
    """
    step_name: str      # e.g., "Step 1: Core System Foundation"
    type: Literal["FIXED", "BRANCH"]
    
    # type == FIXED 인 경우 사용
    subjects: List[TrackSubject] = []
    
    # type == BRANCH 인 경우 사용
    options: List[TrackBranchOption] = []

# --- Main Model ---

class Track(MongoDBModel):
    """
    [Collection]: tracks
    직무별 로드맵 전체 구조 정의 (Source Data)
    복잡한 계층(Track > Step > Option > Subject > Level > Concept)을 포함
    """
    title: str          # e.g., "Track 1: AI Engineer"
    description: str
    order: int = 1
    
    steps: List[TrackStep] = []
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Track 1: AI Engineer",
                "description": "AI 엔지니어링 마스터 코스",
                "steps": [
                    {
                        "step_name": "Step 1: Basic",
                        "type": "FIXED",
                        "subjects": [
                            {
                                "title": "FastAPI Essentials",
                                "levels": {"Lv1": ["Concept A"], "Lv2": ["Concept B"]}
                            }
                        ]
                    }
                ]
            }
        }
