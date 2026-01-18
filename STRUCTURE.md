# Project Structure

```
.
├── STRUCTURE.md                    # Project Structure
├── docker-compose.yml              # Docker compose config
├── Dockerfile                      # Backend Dockerfile
├── README.md                       # Project README
├── dev_log.md                      # Development Log
├── backend/                        # Backend Root
│   ├── requirements.txt
│   ├── scripts/                    # Utility Scripts
│   │   ├── init_db.py              # DB Initialization
│   │   └── sync_track_to_db.py     # Sync JSON tracks to DB
│   ├── tests/                      # Tests
│   │   ├── __init__.py
│   │   ├── test_ai_agents.py
│   │   ├── test_integration_flow.py
│   │   └── test_mcp.py
│   └── app/                        # Application Code
│       ├── __init__.py
│       ├── main.py                 # App Entrypoint
│       │
│       ├── engine/                 # [CORE LOGIC] Pure AI Business Logic (No dependencies on interfaces)
│       │   ├── agents/             # [Brain] LLM Agents (Interviewer, Evaluator)
│       │   ├── graphs/             # [Flow] LangGraph Orchestration & State
│       │   ├── tools/              # [Skills] Core capabilities (Search, TechTree)
│       │   └── prompts/            # [Context] System prompts & Templates
│       │
│       ├── interfaces/             # [ADAPTERS] Communication Layers (Depends on Engine)
│       │   ├── mcp/                # MCP Server (for Kakao/Claude)
│       │   └── api/                # REST API (for Web Frontend)
│       │       ├── v1/             # Legacy Stateless API
│       │       └── v2/             # New Stateful Chat API
│       │
│       ├── core/                   # [INFRA] Configuration, DB, Logging
│       ├── services/               # [DAO] Database Access & CRUD
│       ├── schemas_api/            # [DTO] API Request/Response Models
│       ├── schemas_db/             # [MODEL] Database Models
│       └── source/                 # [STATIC] Data Files (Surveys, Tracks)
|
├── frontend/                       # Frontend Root
│   ├── v1/                         # Streamlit App
│   │   ├── main.py
│   │   └── requirements.txt
│   └── v2/                         # Next.js App
|
└── docs/                           # Documentation
│   ├── README.md
│   ├── 1_prd/                      # Product Requirements
│   │   ├── personas.md
│   │   ├── product_spec.md
│   │   ├── sprint_roadmap.md
│   │   └── user_flow.md
│   ├── 2_design/                   # System Design
│   │   ├── agent_workflow.md
│   │   ├── architecture.md
│   │   ├── db_schema.md
│   │   ├── mcp_server.md
│   │   └── track.md
│   └── 3_knowledge/                # Knowledge Base
│       ├── references.md
│       └── tech_decisions.md
└── nginx/                          # Nginx Config
    └── default.conf
```
