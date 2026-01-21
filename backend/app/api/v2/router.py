from fastapi import APIRouter
from app.api.v2 import chat

api_router = APIRouter()

# Chat/Agent 관련 API (v2)
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

