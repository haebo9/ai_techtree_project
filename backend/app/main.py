from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import API Routers (New Flattened Structure)
from app.api.v1.router import api_router as api_router_v1
from app.api.v2.router import api_router as api_router_v2

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Unified Backend for Web Client (REST) and PlayMCP (Agent)",
    version="0.2.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include API Routers
# -> http://localhost:8000/api/v1/... (Legacy/Stable)
app.include_router(api_router_v1, prefix="/api/v1")
# -> http://localhost:8000/api/v2/... (New/Dev)
app.include_router(api_router_v2, prefix="/api/v2")



@app.get("/")
async def root():
    return {
        "message": "Welcome to AI TechTree Nexus", 
        "docs": {
            "mcp": "/mcp/docs",
            "api_v1": "/docs"
        }
    }
