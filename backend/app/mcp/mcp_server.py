from app.mcp.tools import mcp

if __name__ == "__main__":
    import uvicorn
    # Use uvicorn directly to serve the MCP application (FastAPI based)
    # This bypasses CLI argument parsing issues with mcp.run()
    uvicorn.run("app.mcp.tools:mcp", host="0.0.0.0", port=8200)

# run streamlit
# streamlit run frontend/App.py
