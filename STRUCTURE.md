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
│       ├── main.py                 # FastAPI Entrypoint
│       ├── __init__.py
│       ├── ai/                     # AI Logic
│       │   ├── agents/             # AI Agents
│       │   │   ├── evaluator_agent.py
│       │   │   ├── interviewer_agent.py
│       │   │   ├── main_agent.py
│       │   │   └── qamaker_agent.py
│       │   ├── graphs/             # LangGraph Workflows
│       │   │   └── workflow.py
│       │   └── prompts/            # Agent Prompts
│       │       └── default.py
│       ├── api/                    # REST API
│       │   ├── deps.py
│       │   └── v1/
│       │       ├── router.py
│       │       └── endpoints/
│       ├── core/                   # Core Configuration
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── exceptions.py
│       │   └── logging.py
│       ├── mcp/                    # MCP Server
│       │   ├── mcp_server.py
│       │   ├── tools.py            # Tool Definitions
│       │   ├── tools_functions.py  # Tool Implementations
│       │   └── tools_pydantic.py   # Tool Schemas
│       ├── schemas_api/            # API Pydantic Models
│       │   ├── common.py
│       │   ├── interview.py
│       │   └── user.py
│       ├── schemas_db/             # DB Pydantic Models
│       │   ├── common.py
│       │   ├── concept.py
│       │   ├── interview.py
│       │   ├── question.py
│       │   ├── track.py
│       │   ├── trend.py
│       │   └── user.py
│       ├── services/               # Business Logic / CRUD
│       │   ├── crud_base.py
│       │   ├── crud_interview.py
│       │   └── crud_user.py
│       └── source/                 # Static Data
│           ├── surveys.json
│           └── tracks.json
├── frontend/                       # Frontend Root
│   ├── main.py                     # Streamlit Application
│   └── requirements.txt
├── docs/                           # Documentation
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
