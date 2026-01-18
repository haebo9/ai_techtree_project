from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import Legacy API Router (from interfaces)
from app.interfaces.api.v1.router import api_router as api_router_v1

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Unified Backend for Web Client (REST) and PlayMCP (Agent)",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include Legacy API Router (Stateful CRUD)
# -> http://localhost:8000/api/v1/...
app.include_router(api_router_v1, prefix=settings.API_V1_STR)



@app.get("/")
async def root():
    return {
        "message": "Welcome to AI TechTree Nexus", 
        "docs": {
            "mcp": "/mcp/docs",
            "api_v1": "/docs"
        }
    }
