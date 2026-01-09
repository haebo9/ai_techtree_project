from typing import List, Optional
from pydantic import BaseModel, Field
from .common import MongoDBModel

class Question(MongoDBModel):
    """
    [Collection]: questions
    면접 질문 은행 (Static Data)
    각 Subject 및 Level에 해당하는 면접 질문과 모범 답안
    """
    subject: str            # e.g., 'FastAPI Essentials' (Category/Subject Title)
    level: str              # e.g., 'Lv2' (String per db_schema.md example, though mostly int in usage. MD example says "Lv2". sticking to MD)
                            # Wait, MD example says "level": "Lv2". But concepts say "level": "Lv1". 
                            # Question schema in MD -> "level": "Lv2".
    topic: str              # e.g., 'Dependency Injection'
    
    question_text: str
    model_answer: str       # 모범 답안
    
    # 채점 및 검색용 키워드
    keywords: List[str] = []
    
    created_at: str = "" # ISO Date string or datetime? MD says ISODate. Let's use datetime.
    
from datetime import datetime
class Question(MongoDBModel):
    """
    [Collection]: questions
    면접 질문 은행 (Static Data)
    각 Subject 및 Level에 해당하는 면접 질문과 모범 답안
    """
    subject: str            # tracks.steps.subjects.title 과 매핑
    level: str              # 'Lv1', 'Lv2', 'Lv3'
    topic: str              # e.g., 'Dependency Injection'
    
    question_text: str
    model_answer: str       # 모범 답안
    
    keywords: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "FastAPI Essentials",
                "level": "Lv2",
                "topic": "Dependency Injection",
                "question_text": "FastAPI에서 DI의 장점은?",
                "model_answer": "...",
                "keywords": ["IoC", "Testability"]
            }
        }
