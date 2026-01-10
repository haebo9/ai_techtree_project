from pymongo import MongoClient
import sys

# 설정 파일 가져오기
# (scripts 등에서 실행 시 경로 문제 해결을 위해 try-except 또는 절대 import 사용)
try:
    from app.core.config import settings
except ImportError:
    # 단순 스크립트 실행 시 경로 문제 발생 가능성 대비
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
    from app.core.config import settings

class MongoDB:
    client: MongoClient = None
    db = None

    def connect(self):
        if not settings.MONGODB_URL:
            print("⚠️ MONGODB_URL is not set in .env file.")
            sys.exit(1)
            
        self.client = MongoClient(settings.MONGODB_URL)
        
        # .env의 DB_NAME 또는 config.py의 기본값 사용
        target_db = settings.DB_NAME
        try:
            self.db = self.client.get_database(target_db)
            print(f"✅ Connected to MongoDB: {self.db.name}")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise e

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

# 싱글톤 인스턴스
mongodb = MongoDB()

def get_db():
    """
    FastAPI Dependency 또는 직접 호출용 DB 접근 함수.
    연결이 안 되어 있으면 연결을 시도함.
    """
    if mongodb.db is None:
        mongodb.connect()
    return mongodb.db
