from app.mcp.tools import mcp

if __name__ == "__main__":
    # The mcp.run() method from FastMCP handles execution modes (stdio, sse, etc.) based on CLI arguments.
    # To run with SSE on a specific port, you might use:
    # python -m app.mcp.mcp_server --transport sse --port 8200
    # Or simply:
    mcp.run()

# run streamlit
# streamlit run frontend/App.py
