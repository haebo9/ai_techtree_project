from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from .common import MongoDBModel

class Trend(MongoDBModel):
    """
    [Collection]: trends
    웹 검색 에이전트가 수집한 최신 기술 동향
    Source Data for 'get_techtree_trend' tool.
    """
    title: str
    link: str
    summary: str
    category: str  # tech_news, engineering, research, k_blog
    tags: List[str] = []
    source_domain: str
    
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    
    # [Internal] 서비스 내 사용자 조회수 (인기 트렌드 랭킹용)
    view_count: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "title": "2025년을 위한 7개의 데이터베이스",
                "link": "https://news.hada.io/weekly/202451",
                "summary": "AI 시대에 주목받는 DB 7선 정리...",
                "category": "tech_news",
                "tags": ["데이터베이스", "Backend", "2025_Trend"],
                "source_domain": "news.hada.io",
                "view_count": 10
            }
        }
