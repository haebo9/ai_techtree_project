# Backend

## Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI 진입점 (Lifespan 관리)
│   ├── core/                           # 핵심 설정 (환경변수, DB 연결)
│   ├── api/                            # Legacy REST API (Stateful)
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── api.py
│   ├── mcp/                            # MCP Server (Agent Interface)
│   │   ├── tools.py                        # MCP 도구(Tool) 정의 및 등록
│   │   ├── tools_functions.py              # 도구별 실제 비즈니스 로직
│   │   └── tools_pydantic.py               # 도구 입출력 Pydantic 스키마
│   ├── ai/                             # AI Core Logic (Shared)
│   │   ├── agents/                         # AI Agents
│   │   └── prompts/                        # AI Agent Prompts
│   ├── source/                         # Data Source Files (GitOps Master Data)
│   │   ├── tracks.json                     # 커리큘럼 원본 데이터
│   │   └── surveys.json                    # 설문조사 데이터
│   ├── schemas_db/                     # MongoDB Pydantic Schemas
│   │   ├── user.py                         # 사용자 및 학습 현황
│   │   ├── track.py                        # 커리큘럼/로드맵 구조
│   │   ├── question.py                     # 면접 질문 은행
│   │   ├── interview.py                    # 면접 기록
│   │   ├── trend.py                        # 기술 트렌드
│   │   └── concept.py                      # 상세 개념 및 RAG 원본
│   ├── schemas_api/                    # API DTO Schemas
│   └── services/                       # Business Logic & CRUD
├── scripts/                            # 유틸리티 스크립트
│   ├── init_db.py                          # DB 초기화 및 인덱스 생성
│   └── sync_track_to_db.py                 # JSON 데이터 -> DB 동기화
├── tests/                              # Unit Tests
├── .env
├── .gitignore
├── Dockerfile
└── requirements.txt
```
