from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import MongoDBModel

class Concept(MongoDBModel):
    """
    [Collection]: concepts
    Track -> Levels -> Concept List에 명시된 원자 단위 개념(Atomic Concept)의 상세 지식.
    RAG(Retrieval-Augmented Generation) 및 면접 문제 생성의 원천 데이터.
    """
    subject: str        # Parent Subject Title (e.g. "FastAPI Essentials")
    level: str          # "Lv1", "Lv2", "Lv3"
    name: str           # Concept Name (e.g. "GET vs POST 요청 메서드의 차이")
    
    summary: Optional[str] = None # 개념 요약
    
    # [RAG Source] 문제 생성의 원천이 되는 순수 텍스트 지식
    description: str    
    
    references: List[str] = []
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "FastAPI Essentials",
                "level": "Lv1",
                "name": "GET vs POST 요청 메서드의 차이",
                "summary": "GET은 조회를, POST는 생성을 위한 메서드입니다.",
                "description": "GET 요청은 서버로부터 데이터를 조회할 때 사용하며...",
                "references": ["https://developer.mozilla.org/ko/docs/Web/HTTP/Methods/GET"]
            }
        }
