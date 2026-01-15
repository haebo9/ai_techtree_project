# MCP Server Design: AI TechTree Navigator

이 문서는 **Kakao PlayMCP** 등록을 위한 AI TechTree Navigator의 핵심 정보 및 도구 명세서입니다.
등록 화면에 필요한 **MCP 설명**, **대화 예시**, **도구 정보**를 최적화하여 정리했습니다.

## 📌 PlayMCP 등록용 핵심 요약 (Registration Essentials)

### 1. MCP 설명 (Description)
*(MCP 정보 > 설명 란에 입력)*
> **"막막한 AI 공부, 길을 찾아드립니다."** 
> AI TechTree는 사용자 맞춤형 커리어 로드맵과 실시간 기술 트렌드를 제공하는 전문 네비게이터입니다. <br/>
> <br/>
> **[주요 기능 및 도구]** <br/>
> 🩺 **적성 진단 (Survey)**: 사용자의 개발 경력과 관심사를 파악하기 위한 인터랙티브 질문을 제공합니다. <br/>
> 🎯 **트랙 추천 (Track)**: 분석된 성향을 바탕으로 'System Engineer', 'Modeler' 등 최적의 AI 직무 트랙을 추천합니다. <br/>
> 🗺️ **로드맵 안내 (Path)**: 선택한 트랙의 기초부터 심화까지, 단계별 학습 커리큘럼(Step-by-Step)을 상세히 안내합니다. <br/>
> 📚 **개념 상세 (Subject)**: 로드맵의 각 항목에 대해 무엇을 공부해야 하는지, 핵심 키워드와 개념(Level)을 설명합니다. <br/>
> 📈 **트렌드 검색 (Trend)**: "최신 RAG 사례" 등 급변하는 AI 기술 트렌드와 한국 기업의 도입 사례(K-Blog)를 실시간으로 브리핑합니다.

### 2. 대화 예시 (Conversation Examples)
*(MCP 정보 > 대화 예시 란에 각각 입력)*
1. AI 공부를 시작해보고 싶은데 뭐부터 해야 할지 모르겠어.
2. AI 엔지니어 되려면 어떤 무슨 순서로 공부해야해?
3. LLM Agent와 관련된 한국어 정보 찾아줘.

---

## 🛠️ 도구 상세 명세 (Tool Specifications)
*(참고: 아래의 'LLM 지침' 내용은 실제 구현 시 Tool의 `description` 필드나 `docstring`에 포함되어야 LLM이 인식할 수 있습니다.)*

### `❗get_techtree_survey`
*   **활성 조건 (Trigger Condition)**
    *   **대화 시작 시** 혹은 사용자의 배경 정보(경력, 관심사)가 부족할 때 사용합니다.
    *   **주의(Negative Constraint)**: 사용자가 이미 본인의 경력("난 시니어 자바 개발자야")과 관심사("LLM 서비스 만들고 싶어")를 구체적으로 언급했다면 이 도구를 사용하지 않고 바로 `get_techtree_track`을 호출합니다.
*   **입력 (Input)**
    *   None
*   **출력 (Output)**
    *   `interests`와 `experience_level`을 파악하기 위한 **핵심 질문(객관식)**을 반환합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "intro_message": "string",
      "questions": [
        {
          "id": "string",
          "text": "string (질문 내용)",
          "options": [
            {
              "label": "string (선택지 텍스트)",
              "value": {
                 "level": "string" // or "track": "string"
              }
            }
          ]
        }
      ]
    }
    ```

### `❗get_techtree_track`
*   **활성 조건 (Trigger Condition)**
    *   사용자의 관심사(`interests`)와 경력(`experience_level`)이 파악되었을 때, 혹은 사용자가 "어떤 트랙들이 있어?"라고 물었을 때 사용합니다.
*   **입력 (Input)**
    *   `interests: list[str]` (관심 키워드 리스트. **전체 목록을 보려면 `["ALL"]`을 전달합니다.**)
    *   `experience_level: string` (사용자 경력 수준: "beginner", "intermediate", "expert")
*   **출력 (Output)**
    *   사용자 입력을 분석하여 가장 적합한 Track을 추천하거나, 모든 사용 가능한 Track 리스트를 제공합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "recommended_track": "string (Track Name)",
      "description": "string",
      "matching_score": float,
      "reason": "string (Why this track fits based on input)",
      "track_content": { 
          "track_name": "string",
          "description": "string",
          "key_steps": [ { "step": "string", "description": "string", "topics": ["string"] } ]
      },
      "message": "string (만약 전체 목록을 요청한 경우)",
      "available_tracks": [ { "track_name": "string", "description": "string" } ]
    }
    ```

### `❗get_techtree_path`
*   **활성 조건 (Trigger Condition)**
    *   사용자가 특정 Track을 선택하고 **구체적인 학습 단계(Steps)**나 **로드맵**을 보고 싶어할 때 사용합니다.
*   **입력 (Input)**
    *   `track_name: string` (Track의 정확한 명칭, 예: 'Track 1: AI Engineer')
*   **출력 (Output)**
    *   해당 Track의 전체 계층적 커리큘럼 로드맵(단계별 Subject 목록)을 조회합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "track": "string",
      "description": "string",
      "roadmap": {
        "Step 1": [ { 
                      "subject": "string",
                      "category": "string",
                      "description": "string",
                      "importance": "string" 
                    } ],
        "Step 2": [ ... ]
      },
      "note": "string"
    }
    ```

### `❗get_techtree_subject`
*   **활성 조건 (Trigger Condition)**
    *   사용자가 로드맵의 특정 항목(Subject)에 대해 "이게 뭐야?", "상세 개념(Level) 알려줘"라고 물을 때 사용합니다.
*   **입력 (Input)**
    *   `subject_name: string` (Subject의 정확한 명칭, 예: 'Vector DB', 'Python Syntax')
*   **출력 (Output)**
    *   특정 Subject의 상세 학습 개념(Lv1, Lv2, Lv3)을 조회합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "subject": "string",
      "track": "string",
      "category": "string",
      "details": {
        "Lv1": ["string (concept)"],
        "Lv2": ["string (concept)"],
        "Lv3": ["string (concept)"]
      }
    }
    ```

### `❗get_techtree_trend`
*   **활성 조건 (Trigger Condition)**
    *   최신 기술 뉴스, 엔지니어링 팁, 연구 사례 등을 요청할 때 사용합니다.
    *   **한국어 질문(국내 사례, 블로그 등)에는 반드시 `category="k_blog"`를 사용합니다.**
*   **입력 (Input)**
    *   `keywords: list[str]` (검색할 핵심 기술 키워드 3-5개)
    *   `category: string` (기본값: "k_blog". 옵션: "tech_news", "engineering", "research", "k_blog")
*   **출력 (Output)**
    *   입력된 키워드와 카테고리를 기반으로 웹시장의 최신 정보를 요약하여 링크와 함께 제공합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "answer": "string (질문에 대한 종합 요약 답변)",
      "items": [
        { "title": "string",
          "link": "string (URL)",
          "summary": "string",
          "tags": ["string"]
        }
      ],
      "category": "string"
    }
    ```

---

## 🔬 ReAct 동작 예시 (Execution Trace)
LLM이 실제 추론(Reasoning)과 행동(Acting)을 통해 응답을 생성하는 과정입니다.

### Scenario: 적성 진단 및 트랙 추천
**Step 1: 초기 진단 (Survey)**
**User**: "AI 공부를 시작해보고 싶어."

**Agent**:
1.  **Thought**: 사용자가 막연하게 AI 학습을 시작하려 한다. 사용자의 배경지식과 관심사를 파악하기 위해 `get_techtree_survey`를 호출해야 한다.
2.  **Action**: `get_techtree_survey()`
3.  **Observation**:
    ```json
    {
      "intro_message": "반갑습니다! 딱 맞는 AI 로드맵을 찾기 위해 몇 가지만 여쭤볼게요.",
      "questions": [
        "현재 어떤 개발 경험이 있으신가요? (예: 웹 프론트엔드, 백엔드, 비전공 등)",
        "AI 기술 중 특별히 흥미로운 분야가 있나요? (예: 챗봇, 데이터 분석, 자동화 등)"
      ]
    }
    ```
4.  **Final Answer**: "반갑습니다! 딱 맞는 AI 로드맵을 찾아드리기 위해 몇 가지만 먼저 여쭤볼게요. \n1. 현재 어떤 개발 경험이나 직무에 계신가요? (예: 웹 백엔드 3년차)\n2. AI 기술 중에서 특별히 관심 가는 분야가 있으신가요?"

**Step 2: 트랙 추천 (Recommendation)**
**User**: "웹 백엔드 개발을 3년 정도 했고, 챗봇이나 시스템 구축 쪽에 관심이 있어."

**Agent**:
1.  **Thought**: 사용자의 답변에서 '웹 백엔드 3년차(Intermediate)', '챗봇/시스템(Backend/System Interest)' 정보를 추출했다. 이를 바탕으로 트랙을 추천한다.
2.  **Action**: `get_techtree_track(interests=["web", "backend", "chatbot"], experience_level="intermediate")`
3.  **Observation**:
    ```json
    {
      "recommended_track": "Track 1: AI Engineer",
      "reason": "웹 백엔드 경험을 살려 LLM 애플리케이션 및 서빙 시스템을 구축하기에 최적의 트랙입니다.",
      "track_content": { ... }
    }
    ```
4.  **Final Answer**: "웹 백엔드 3년 경력을 보유하고 계시군요! 그렇다면 **Track 1: AI Engineer** 과정을 강력히 추천합니다. \n\n이 트랙은 기존의 백엔드 역량 위에 AI 모델을 서빙하고 애플리케이션을 구축하는 기술을 더해, 가장 빠르게 실무형 AI 엔지니어로 성장할 수 있는 경로입니다. \n\n첫 단계인 **Tier 1: Core System Foundation**부터 살펴보시겠어요?"

### Scenario: 기술 트렌드 파악 (한국 기업 사례)
**User**: "요즘 한국 기업들은 RAG 기술을 실무에 어떻게 적용하고 있어?"

**Agent (ReAct Loop)**:
1.  **Thought**: 사용자가 'RAG' 기술에 대해 묻고 있으며, 특히 '한국 기업 실무 사례'를 원한다. 이는 `k_blog` 카테고리에 적합하다.
2.  **Action**: `get_techtree_trend(keywords=["RAG", "실무", "적용"], category="k_blog")`
3.  **Observation**:
    ```json
    {
      "answer": "우아한형제들과 당근마켓 등 주요 기술 기업들이 RAG를 실제 서비스에 도입하고 있습니다.",
      "items": [
        { "title": "우아한형제들: LLM을 활용한 메뉴 추천 시스템", "link": "https://techblog.woowahan.com/...", "summary": "..." },
        { "title": "당근: RAG 기반 검색 품질 개선기", "link": "https://medium.com/daangn/...", "summary": "..." }
      ],
      "category": "k_blog"
    }
    ```
4.  **Final Answer**: "한국의 주요 테크 기업들은 RAG를 다음과 같이 활용하고 있습니다: \n- **우아한형제들**: LLM을 활용해 배달 메뉴를 추천하는 시스템을 구축했습니다. [상세보기](https://techblog.woowahan.com/...)\n- **당근**: 검색 품질을 높이기 위해 RAG 기술을 도입하여 사용자 의도를 더 정확히 파악하고 있습니다. [상세보기](https://medium.com/daangn/...)"
