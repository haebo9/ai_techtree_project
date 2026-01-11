from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from .common import MongoDBModel

class Trend(BaseModel):
    """
    기술 관련 정보 검색을 위한 컬랙션 스키마 
    """
    title: str
    link: str
    summary: str
    tags: List[str] = []
    source_domain: str
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    view_count: int = 0

class TrendCategory(MongoDBModel):
    """
    [Collection]: trends
    카테고리별로 트렌드를 묶어서 저장하는 구조
    """
    category: str  # e.g., "tech_news", "engineering"
    items: List[Trend] = Field(default_factory=list)
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "category": "tech_news",
                "items": [
                    {
                        "title": "2025년을 위한 7개의 데이터베이스",
                        "link": "https://news.hada.io/weekly/202451",
                        "summary": "AI 시대에 주목받는 DB 7선 정리...",
                        "tags": ["데이터베이스", "Backend"],
                        "source_domain": "news.hada.io",
                        "view_count": 10
                    }
                ]
            }
        }
