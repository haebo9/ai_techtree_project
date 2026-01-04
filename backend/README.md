# Backend

## Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI 진입점 (MCP 및 Legacy API 마운트)
│   ├── core/                           # 핵심 설정 (환경변수, DB 연결)
│   ├── api/                            # Legacy REST API (Stateful)
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── api.py
│   ├── mcp/                            # MCP Server (Stateless)
│   │   ├── __init__.py
│   │   └── server.py                       # LangServe 기반 MCP 엔드포인트 설정
│   ├── ai/                             # AI Core Logic (Shared)
│   │   ├── agents/                         # AI Agents (As Pure Tools)
│   │   │   ├── main_agent.py                   # [Facade] MCP Tool Provider & Router
│   │   │   ├── qamaker_agent.py                # [Tool] 질문 생성 (Async)
│   │   │   ├── interviewer_agent.py            # [Tool] 대화 및 꼬리질문
│   │   │   └── evaluator_agent.py              # [Tool] 평가 및 리포트 작성
│   │   ├── source/                           # AI Agent Source Code    
│   │   └── prompts/                          # AI Agent Prompts
│   ├── schemas_db/                     # MongoDB Schemas (Used by Legacy API)
│   ├── schemas_api/                    # API DTO Schemas
│   └── services/                       # Business Logic & CRUD
├── tests/                              # Unit Tests
├── .env
├── .gitignore
├── Dockerfile
└── requirements.txt
```