from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import MCP Server App
from app.mcp.server import mcp_app

# Import Legacy API Router (추후 구현 시 활성화)
# from app.api.v1.api import api_router

app = FastAPI(
    title="AI TechTree Backend",
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

# 1. Mount MCP Server (Stateless Logic)
# -> http://localhost:8000/mcp/... 경로로 접근 가능
app.mount("/mcp", mcp_app)

# 2. Include Legacy API Router (Stateful CRUD)
# -> http://localhost:8000/api/v1/...
# app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI TechTree Nexus", 
        "docs": {
            "mcp": "/mcp/docs",
            "api_v1": "/docs"
        }
    }
