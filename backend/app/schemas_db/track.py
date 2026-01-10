from datetime import datetime
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field
from .common import MongoDBModel, PyObjectId

# --- Nested Structures for Track ---

class LevelsContent(BaseModel):
    """
    학습 난이도별 개념 리스트
    Lv1: 기초 / Lv2: 심화 / Lv3: 전문가
    """
    Lv1: List[str] = Field(default_factory=list)
    Lv2: List[str] = Field(default_factory=list)
    Lv3: List[str] = Field(default_factory=list)

class TrackSubject(BaseModel):
    """
    개별 학습 주제 (Subject)
    Levels를 포함하는 실제 학습 단위
    """
    title: str  # e.g., "FastAPI Essentials"
    levels: LevelsContent = Field(default_factory=LevelsContent)

class TrackBranchOption(BaseModel):
    """
    선택 분기점의 각 옵션 (Option)
    """
    option_name: str  # e.g., "Option 1: Serving Specialist"
    subjects: List[TrackSubject]

class TrackStep(BaseModel):
    """
    커리큘럼의 단계 (Step)
    모든 단계는 Option을 가짐 (Unified Structure)
    분기가 없는 경우 "Option 1" 하나만 존재
    """
    step_name: str      # e.g., "Step 1: Core System Foundation"
    type: Literal["FIXED", "BRANCH"]
    
    # Unified Structure: Subjects are always inside Options
    options: List[TrackBranchOption] = []

# --- Main Model ---

class Track(MongoDBModel):
    """
    [Collection]: tracks
    직무별 로드맵 전체 구조 정의 (Source Data)
    Hierarchy: Track > Step > Option > Subject > Level > Concept
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
                        "options": [
                            {
                                "option_name": "Option 1: Core Curriculum",
                                "subjects": [
                                    {
                                        "title": "FastAPI Essentials",
                                        "levels": {"Lv1": ["Concept A"], "Lv2": ["Concept B"]}
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
