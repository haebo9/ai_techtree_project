# MCP Folder Structure

```
backend/app/mcp/
├── __init__.py
├── server.py           # [Server] FastAPI/LangServe 진입점 및 도구 등록
├── tools.py            # [Interface] LLM이 호출하는 Tool 정의 (@tool)
└── tools_functions.py  # [Logic] 실제 비즈니스 로직 (Embedding, Search, Tree Traversal)
```

## Key Components

### 1. tools.py
- **Roles**: LLM Interface
- Contains `@tool` decorated functions.
- Delegates actual logic to `functions.py`.
- **Tools**:
  - `get_ai_track`: Recommends a track based on interests.
  - `get_ai_path`: Returns curriculum roadmap.
  - `get_ai_trends`: Searches for latest AI trends.

### 2. functions.py
- **Roles**: Core Business Logic
- **Features**:
  - OpenAI Embedding generation & Similarity search.
  - Tavily Web Search integration.
  - Lazy initialization of heavy models.
- **Data Source**: Uses `backend/app/ai/source/topics.py` as the Single Source of Truth.