from fastapi import APIRouter
from app.api.v1 import chat

api_router = APIRouter()

# Chat/Agent 관련 API
api_router.include_router(chat.router, prefix="/agent", tags=["agent"])
# 예: POST /api/v1/agent/chat
