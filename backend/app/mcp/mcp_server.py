from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import uvicorn

# Load Environment Variables from backend/.env
# Note: When running this file directly, ensure you are in the project root or backend root.
load_dotenv()

from app.mcp.tools import MCP_TOOLS

# Independent MCP Server
app = FastAPI(
    title="AI TechTree MCP Server",
    version="1.0",
    description="Stand-alone MCP Server for AI TechTree Project"
)

# Register Tools
for tool in MCP_TOOLS:
    add_routes(
        app,
        tool,
        path=f"/{tool.name}",
        enable_feedback_endpoint=False,
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "mode": "standalone_mcp_server"}

if __name__ == "__main__":
    # Allow running directly with python backend/app/mcp/mcp_server.py
    uvicorn.run("app.mcp.mcp_server:app", host="0.0.0.0", port=8100, reload=True)


# run streamlit
# streamlit run app/mcp/streamlit.py
