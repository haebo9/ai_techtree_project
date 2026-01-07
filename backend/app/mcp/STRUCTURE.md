# MCP Folder Structure
 
 ```
 backend/app/mcp/
 ├── __init__.py
 ├── mcp_server.py       # [Server] MCP Protocol-compliant Server (FastAPI)
 ├── streamlit.py        # [Client/Agent] Streamlit UI & Agent Execution Loop
 ├── tools.py            # [Interface] LangChain @tool definitions (LLM-facing)
 └── tools_functions.py  # [Logic] Core Business Logic (Search, Embeddings, Tree Traversal)
 ```
 
 ## Key Components
 
 ### 1. tools.py
 - **Role**: LLM Tool Interface
 - Defines function signatures and docstrings optimized for LLM understanding.
 - **Registered Tools**:
   - `get_ai_track`: Recommends a specific track based on user interests using semantic search.
   - `get_ai_path`: Retrieves the full hierarchical roadmap (Tier -> Subject) for a given track.
   - `get_ai_trend`: Web searches for latest tech trends with domain filtering.
   - `get_techtree_detail`: (Optional) deep dive into specific subject concepts.
 
 ### 2. tools_functions.py
 - **Role**: Implementation Layer
 - **Features**:
   - `perform_search_similarity`: OpenAI Embedding & Cosine Similarity for track recommendation.
   - `perform_web_search`: Tavily API integration with Category-based Domain Filtering.
   - `lazy_loading`: Initializes heavy models (ChatOpenAI, Embeddings) on demand.
 - **Data Source**: Imports `AI_TECH_TREE` from `app.ai.source.track`.
 
 ### 3. streamlit.py
 - **Role**: Agent Playground
 - **Features**:
   - Direct import and usage of `MCP_TOOLS`.
   - Multi-turn Agent Loop (While True) to handle sequential tool calls.
   - Displays tool outputs in expandable UI components.
 
 ### 4. mcp_server.py
 - **Role**: MCP Protocol Server
 - Exposes tools as API endpoints for external MCP clients (e.g., Cursor, Claude Desktop).