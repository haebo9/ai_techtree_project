# AI TechTree

> **<h3>"개발자의 성장이 게임이 되는 곳, AI TechTree"</h3>**

> **AI TechTree**는 **AI 면접관**과 실시간으로 대화하며 기술 역량을 증명하고, RPG 게임처럼 **스킬 트리**를 채워나가는 서비스입니다.
> 단순한 문제 풀이가 아닌, **꼬리에 꼬리를 무는 심층 인터뷰(LangGraph)** 를 통해 당신의 '진짜 실력'을 진단합니다.
>
> * **🕵️ AI 심층 면접**: 답변에 따라 달라지는 동적 질문 생성
> * **🌳 라이브 스킬 트리**: 내 강점과 약점을 한눈에 보여주는 시각화
> * **⚔️ 커리어 RPG**: '전직' 시스템으로 즐기는 성장
>
> ---
>
> 💡 **Engineering Philosophy**
> 본 프로젝트는 **1인 개발자**로서 **기획(PRD)부터 배포(CI/CD)** 까지의 **전체 엔지니어링 사이클**을 현업 수준으로 수행했습니다.
> **"AI 코어의 고도화(Deep-Dive)"** 와 **"인프라의 효율성(Lean)"** 을 동시에 달성하기 위한 전략적 선택들을 문서화했습니다.

1.  [Documentation](#documentation)
2.  [Tech Stack](#tech-stack)
3.  [Architecture](#architecture)
4.  [Git & Deployment](#git--deployment)
5.  [Roadmap](#roadmap)
6.  [Getting Started](#getting-started)

---

## Documentation

> 프로젝트의 모든 기획 및 설계 문서는 `docs` 디렉토리 내에서 코드와 함께 관리됩니다.

### 📂 Documentation Structure

| Directory | Description | Key Documents |
| --- | --- | --- |
| [**1_prd**](docs/1_prd) | **기획 (Product Spec)**<br>요구사항 및 서비스 흐름 정의 | • [핵심 기능 명세](docs/1_prd/product_spec.md)<br>• [페르소나 정의](docs/1_prd/personas.md)<br>• [서비스 흐름도](docs/1_prd/user_flow.md)<br>• [스프린트 로드맵](docs/1_prd/sprint_roadmap.md) |
| [**2_design**](docs/2_design) | **설계 (System Design)**<br>시스템 아키텍처 및 기술 설계 | • [시스템 아키텍처](docs/2_design/architecture.md)<br>• [AI 에이전트 설계](docs/2_design/agent_workflow.md)<br>• [DB 스키마](docs/2_design/db_schema.md)<br>• [MCP 서버 설계](docs/2_design/mcp_server.md)<br> |
| [**3_knowledge**](docs/3_knowledge) | **지식 (Knowledge Base)**<br>기술 의사결정 및 참고 자료 | • [기술 스택 선정](docs/3_knowledge/tech_decisions.md)<br>• [참고 자료](docs/3_knowledge/references.md) |

👉 [전체 문서 목록 보기](docs/README.md)

---

## Tech Stack

> 프로젝트에 사용된 핵심 기술 및 인프라 구성입니다.

| Category | Technology | Description |
| --- | --- | --- |
| **Frontend** | ![Next.js](https://img.shields.io/badge/Next.js-black?style=flat-square&logo=next.js&logoColor=white) ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square) | UI/UX & Client Deployment |
| **Backend** | ![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)  | Server API & Cloud Hosting |
| **AI / LLM** | ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white) ![LangGraph](https://img.shields.io/badge/LangGraph-FF4B4B?style=flat-square) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white) | AI Agents & Workflow Orchestration |
| **Database** | ![MongoDB Atlas](https://img.shields.io/badge/MongoDB%20Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white) | Cloud NoSQL Database |

## Architecture

- **Frontend**: `Next.js`로 구축되어 **Vercel**을 통해 배포됩니다.(자동배포)
- **Backend**: FastAPI 서버를 **Docker** 컨테이너로 빌드하여 **AWS (EC2)** 에서 실행합니다.
- **Database**: **MongoDB Atlas (Cloud)** 를 사용하여 데이터 안정성을 확보합니다.
- **AI Engine**: LangGraph 기반의 Multi-Agent 시스템이 코드 분석 및 평가를 수행합니다.

---
## Git & Deployment

> 본 프로젝트는 1인 개발의 효율성과 서비스 안정성을 위해 **GitHub Flow**를 변형한 **3-Tier 전략**을 따릅니다.
> **로컬 중심의 개발**과 **Vercel/AWS의 무료 티어**를 적극 활용하여 비용 '0원'의 인프라를 구축했습니다.

| Branch | Action & Role | Frontend | Backend | Database |
| :--- | :--- | :--- | :--- | :--- |
| **`feature/*`** | **Develop**<br/>기능 단위 개발 | **Localhost :3000**<br/>(Hot Reloading) | **Localhost :8000**<br/>(Docker Compose) | **MongoDB Atlas<br/>**(Dev) |
| **`main`** | **Staging**<br/>PR 통합 및 테스트 | **Vercel Preview**<br/>(PR 시 자동 배포) | **Local Docker**<br/>(Prod simulation) | **MongoDB Atlas<br/>**(Dev) |
| **`Tag`** | **Release**<br/>실제 사용자 배포 | **Vercel Prod**<br/>(Edge Network + CDN) | **AWS EC2**<br/>(t3.small + Docker) | **MongoDB Atlas<br/>**(Prod) |

---

## Roadmap
> 상세한 개발 일정과 스프린트 계획은 [Sprint Roadmap](docs/1_prd/sprint_roadmap.md) 문서를 참고하세요.


| Phase | Focus & Sprints | Period |
| :--- | :--- | :--- |
| **Phase 0** | **Planning & Design**<br>(Sprint 0) 기획 및 기술 조사 | 2025.12 초 ~ 중순 |
| **Phase 1** | **Core Logic & MCP Server**<br>(Sprint 1-4) Agent 기능 및 MCP 서버 구현 | 2025.12 말 ~ 2026.01 중순 |
| **Phase 2** | **Web Service Integration**<br>(Sprint 5-7) 웹 프론트엔드 통합 및 MVP 런칭 | 2026.01 말 ~ 02 말 |
| **Phase 3** | **Iteration & Scale-up**<br>(Sprint 8-9) 성능 개선 및 고도화 | 2026.03 ~ 04 |
| **Phase 4** | **Polish & Stabilization**<br>(Sprint 10) 안정성 확보 및 유지보수 | 2026.05 ~ |

---

## Getting Started
> `docs/README.md`를 참고하여 개발 환경을 구축할 수 있습니다.

### Prerequisites
- Python 3.13.11
- Node.js v22.12.0
- Docker & Docker Compose
- OpenAI API Key
- AWS EC2 Instance (Amazon Linux 2023)
- MongoDB Atlas 

### 1. Environment Setup
Create a `.env` file in the project root. You can refer to `.env.example` if it exists, or ensure the following keys are present.

```bash
# .env Configuration
OPENAI_API_KEY=sk-...
MONGODB_URL=mongodb+srv://...
# Add other necessary environment variables
```

### 2. Run Local Server (Docker)
This is the recommended way to run the full stack locally (Backend + Frontend + MCP + Nginx).

```bash
# 1. Build & Run (Force Rebuild)
docker-compose -f docker-compose.local.yml up -d --build

# 2. Check Logs
docker-compose -f docker-compose.local.yml logs -f

# 3. Stop Server
docker-compose -f docker-compose.local.yml down
```
> **Access Points:**
> - Frontend (Next.js v2): http://localhost:8100
> - Backend Docs: http://localhost:8000/docs
> - MCP Server: http://localhost:8200/mcp

### 3. Deploy to AWS
For production deployment on AWS EC2.

> **1. For AWS (Local Mac)**: Build image, push to Hub, and deploy config.
```bash
docker build --no-cache --platform linux/amd64 -t haebo/ai-techtree:v1 .
docker push haebo/ai-techtree:v1
scp -r nginx techtree-server:~/
scp docker-compose.yml .env techtree-server:~/
```

> **2. In AWS (Server)**: Pull and run services.
```bash
# Local terminal: 
ssh techtree-server
# AWS terminal:
docker-compose pull
docker-compose down
docker-compose up -d --remove-orphans
docker-compose logs -f
```
> **Access Points:**
> - Frontend: https://haebo.pro
> - MCP Server: https://haebo.pro/mcp

### 4. Deploy Frontend to Vercel
For the **Next.js (v2)** frontend deployment.

1.  **Import Project**:
    *   Go to Vercel Dashboard → **Add New Project**.
    *   Select `ai-techtree-project` repository.

2.  **Configure Settings**:
    *   **Root Directory**: `frontend/v2`
    *   **Framework Preset**: Next.js

3.  **Environment Variables**:
    *   `NEXT_PUBLIC_API_URL`: `https://haebo.pro/api`
    *   *(Depending on implementation)* `NEXT_PUBLIC_MCP_URL`: `https://haebo.pro/mcp`


