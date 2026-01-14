from app.mcp.tools import mcp

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # print(f"✅ [MCP] Starting FastMCP (SSE Mode) using uvicorn on port 8200...", flush=True)
    
    # 'sse_app' is the Starlette/FastAPI application exposed by FastMCP
    # We run it directly to ensure stability and control over the port
    uvicorn.run(mcp.sse_app, host="0.0.0.0", port=8200)

# run streamlit
# streamlit run frontend/main.py
