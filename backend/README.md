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
│   │   ├── mcp_server.py                   # LangServe 기반 MCP 엔드포인트
│   │   ├── tools.py                        # MCP 도구(Tool) 정의 및 등록
│   │   ├── tools_functions.py              # 도구별 실제 비즈니스 로직
│   │   └── streamlit.py                    # MCP Playground (Testing UI)
│   ├── ai/                             # AI Core Logic (Shared)
│   │   ├── agents/                         # AI Agents (As Pure Tools)
│   │   │   ├── main_agent.py                   # [Facade] MCP Tool Provider & Router
│   │   │   ├── qamaker_agent.py                # [Tool] 질문 생성 (Async)
│   │   │   ├── interviewer_agent.py            # [Tool] 대화 및 꼬리질문
│   │   │   └── evaluator_agent.py              # [Tool] 평가 및 리포트 작성
│   │   ├── graphs/                         # LangGraph Workflow Definitions
│   │   └── prompts/                        # AI Agent Prompts
│   ├── source/                         # Data Source Files (GitOps Master Data)
│   │   ├── track.py                        # 커리큘럼 원본 데이터
│   │   └── trend.json                      # 트렌드 검색 결과 아카이브
│   ├── schemas_db/                     # MongoDB Pydantic Schemas
│   │   ├── user.py                         # 사용자 및 학습 현황
│   │   ├── track.py                        # 커리큘럼/로드맵 구조
│   │   ├── question.py                     # 면접 질문 은행
│   │   ├── interview.py                    # 면접 기록
│   │   ├── trend.py                        # 기술 트렌드
│   │   └── concept.py                      # 상세 개념 및 RAG 원본
│   ├── schemas_api/                    # API DTO Schemas
│   └── services/                       # Business Logic & CRUD
├── tests/                              # Unit Tests
├── .env
├── .gitignore
├── Dockerfile
└── requirements.txt
```
