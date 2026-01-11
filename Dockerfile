# Base Image
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (필요시 git 등 추가)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 의존성 패키지 설치
# backend 폴더의 requirements.txt를 먼저 복사해서 캐시 활용
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 프로젝트 코드 복사 (frontend, backend, docs 등 모두 포함)
COPY . .

# PYTHONPATH 설정
# 이렇게 하면 frontend/App.py 에서도 "from backend.app..." 처럼 접근 가능합니다.
ENV PYTHONPATH=/app/backend

# 포트 노출 (문서화 용도)
# 8000: FastAPI, 8501: Streamlit
EXPOSE 8000 8501
