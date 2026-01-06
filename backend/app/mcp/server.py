from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from app.mcp.tools import MCP_TOOLS
# from app.ai.agents.main_agent import TOOLS # Deprecated


# MCP Server as a sub-app or router
mcp_app = FastAPI(
    title="TechTree MCP Server",
    version="1.0",
    description="Stateless MCP Server for AI TechTree"
)

# Tools Binding (LangServe 방식 활용)
# 각 툴을 개별 엔드포인트로 노출하여 PlayMCP가 호출할 수 있게 함
# 예: /mcp/generate_questions/invoke

for tool in MCP_TOOLS:
    add_routes(
        mcp_app,
        RunnableLambda(tool),
        path=f"/{tool.name}",
        enable_feedback_endpoint=False,
    )

# Health Check
@mcp_app.get("/health")
async def health_check():
    return {"status": "ok", "mode": "stateless_mcp"}
