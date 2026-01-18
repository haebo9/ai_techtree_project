from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 필수 환경 변수 (값 없으면 에러 발생)
    OPENAI_API_KEY: str
    MONGODB_URL: str | None = None
    DB_NAME: str = "ai_techtree"  # 기본값 설정
    
    # 선택적 환경 변수 (기본값 제공)
    PROJECT_NAME: str = "AI TechTree"
    API_V1_STR: str = "/api/v1"
    
    # .env 파일 로드 설정
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # .env에 모르는 변수 있어도 에러 안 냄
    )

settings = Settings()
