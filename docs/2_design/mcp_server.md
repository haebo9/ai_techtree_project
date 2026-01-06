# MCP Server Design: AI TechTree Navigator

이 문서는 **Kakao PlayMCP** 환경에서 구동될 AI TechTree Navigator의 도구(Tool) 설계서입니다.
이 도구들은 사용자가 AI 엔지니어로서 성장하는 과정을 돕기 위해 설계되었으며, LLM의 도움 없이도 Python 로직만으로 정확하고 구조화된 정보를 제공합니다.

## 1. 설계 원칙 (Design Principles)
1.  **Source of Truth**: 모든 정보는 `backend/app/ai/source/topics.py`에 정의된 정형 데이터를 기반으로 합니다. (No Hallucination)
2.  **Educational Growth**: 사용자가 자신의 위치를 파악하고, 다음 학습 목표를 설정하도록 돕습니다.
3.  **Deterministic Logic**: 추천 및 검색 로직은 결정론적 알고리즘을 사용하여 일관된 결과를 보장합니다.



## 2. 도구 상세 명세 (Tool Specifications)

### 🟡 1. AI 적성 진단 (`get_ai_track`)
- **Description**: 사용자의 관심사와 경험 수준을 분석하여 가장 적합한 AI 기술 트랙(Track)을 진단하고 추천합니다.
- **Input**:
    - `interests` (list[str]): 관심 분야 키워드 리스트 (예: `["web", "data", "math", "service"]`).
    - `experience_level` (str): 현재 개발 경험 수준 (예: `"beginner"`, `"intermediate"`, `"expert"`).
- **Logic**:
    1. 입력된 키워드와 `topics.py`의 각 Track별 `description` 및 내부 키워드를 임베딩하여 유사도를 계산합니다.
    2. 경험 수준에 따라 추천할 Track의 시작 진입점(Tier 0 vs Tier 1)을 조정합니다.
    3. 가장 높은 유사도를 획득한 Track을 선정합니다.
- **Output**:
    - `recommended_track` (str): 추천 트랙 이름 (예: `"Track 1: AI Engineer"`).
    - `reason` (str): 해당 트랙을 추천한 논리적 근거.
    - `starting_point` (str): 학습을 시작해야 할 구체적인 Tier 또는 Subject.

### 🟡 2. AI 개발자 공부과정 추천 (`get_ai_path`)
- **Description**: 사용자의 관심 트랙을 기반으로 학습해야 할 순서대로 정렬된 Subject 및 Concept 정보를 제공합니다.
- **Input**:
    - `track_name` (str): 조회할 트랙의 정확한 이름 (예: `"Track 2: AI Modeler / Researcher"`).
- **Logic**:
    1. `topics.py`라는 Source of Truth에서 지정된 `track_name`의 하위 트리(Tree) 데이터를 조회합니다.
    2. 계층형 구조(Tier -> Subject -> Concepts)를 유지하며 학습 로드맵을 구성합니다.
- **Output**:
    - `roadmap` (list): 학습해야 할 순서대로 정렬된 Subject 및 Concept 정보.
    - `next_milestone` (str): 단기적으로 달성해야 할 다음 주요 목표.

### 🟡 3. AI 트랜드 정보 (`get_ai_trends`)
- **Description**: 사용자의 관심 기술 키워드를 기반으로 웹 검색을 수행하여 최신 AI 트렌드, 뉴스, 관련 GitHub 저장소 정보를 실시간으로 수집 및 제공합니다.
- **Input**:
    - `keywords` (list[str]): 검색할 기술 키워드 리스트 (예: `["LLM", "Agent", "RAG"]`).
- **Logic**:
    1. 입력된 키워드와 "trends", "latest news", "github" 등의 단어를 조합하여 검색 쿼리를 생성합니다.
    2. 외부 검색 API (예: Tavily, Google 등)를 호출하여 관련성 높은 최신 웹 문서와 문맥을 수집합니다.
    3. 수집된 정보를 기반으로 핵심 트렌드 요약을 생성합니다.
- **Output**:
    - `trend_brief` (list[dict]): 검색된 트렌드 정보 리스트 (Title, Link, Summary 포함).

---

## 3. PlayMCP 시나리오 예시


## 4. 향후 확장성 (Future)
