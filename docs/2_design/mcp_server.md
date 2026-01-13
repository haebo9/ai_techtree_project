# MCP Server Design: AI TechTree Navigator

이 문서는 **Kakao PlayMCP** 등록을 위한 AI TechTree Navigator의 핵심 정보 및 도구 명세서입니다.
등록 화면에 필요한 **MCP 설명**, **대화 예시**, **도구 정보**를 최적화하여 정리했습니다.

## 📌 PlayMCP 등록용 핵심 요약 (Registration Essentials)

### 1. MCP 설명 (Description)
*(MCP 정보 > 설명 란에 입력)*
> AI TechTree Navigator는 AI 엔지니어 지망생에게 개인화된 직무 추천과 체계적인 학습 로드맵을 제공합니다. <br/>
> ▶ **적성 진단**: 사용자의 관심사와 경험을 분석하여 가장 적합한 AI 커리어 트랙을 진단해줍니다. <br/>
> ▶ **로드맵 제공**: 'System Engineer'부터 'Modeler'까지, 검증된 단계별 학습 커리큘럼을 상세히 안내합니다. <br/>
> ▶ **트렌드 브리핑**: 최신 AI 기술 트렌드와 관련 뉴스를 실시간으로 수집하여 정확한 정보를 전달합니다.

### 2. 대화 예시 (Conversation Examples)
*(MCP 정보 > 대화 예시 란에 각각 입력)*
1. AI 공부를 시작해보고 싶어. 
2. AI Engineer가 되려면 뭐부터 공부해야돼? 
3. LLM Agent 관련된 한국어 정보 찾아줘.

---

## 🛠️ 도구 상세 명세 (Tool Specifications)
*(참고: 아래의 'LLM 지침' 내용은 실제 구현 시 Tool의 `description` 필드나 `docstring`에 포함되어야 LLM이 인식할 수 있습니다.)*

### `❗get_techtree_survey`
*   **활성 조건 (Trigger Condition)**
    *   **대화 시작 시** 혹은 사용자의 배경 정보가 없을 때 사용합니다.
*   **입력 (Input)**
    *   None
*   **출력 (Output)**
    *   `interests`와 `experience_level`을 파악하기 위한 **두 가지 핵심 질문(객관식)**을 제공합니다.
    *   각 선택지(Option)는 특정 **Track**이나 **Level** 정보와 매핑되어 있습니다.
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
    *   사용자의 `interests`와 `experience_level`이 파악되었을 때 사용합니다 (예: `get_techtree_survey` 등을 통해).
*   **입력 (Input)**
    *   `interests: list[str]` (관심 키워드 리스트. 모든 트랙을 보려면 `["ALL"]` 전달.)
    *   `experience_level: string` (사용자 경력 수준: "beginner", "intermediate", "expert")
*   **출력 (Output)**
    *   사용자 입력을 분석하여 가장 적합한 Track을 추천하거나, 모든 사용 가능한 Track 리스트를 제공합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "recommended_track": "string (Track Name)",
      "reason": "string (Why this track fits based on input)",
      "starting_point": "string (Immediate next step)"
    }
    ```

### `❗get_techtree_path`
*   **활성 조건 (Trigger Condition)**
    *   사용자가 특정 Track을 선택하고 로드맵을 보고 싶어할 때 사용합니다.
*   **입력 (Input)**
    *   `track_name: string` (Track의 정확한 명칭, 예: 'Track 1: AI Engineer')
*   **출력 (Output)**
    *   해당 Track의 전체 계층적 커리큘럼 로드맵(Subjects & Concepts)을 조회합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "roadmap": [
        { "tier": "string", "subjects": ["string"] }
      ],
      "next_milestone": "string"
    }
    ```

### `❗get_techtree_detail`
*   **활성 조건 (Trigger Condition)**
    *   사용자가 "X가 뭐야?", "X에서 뭘 공부해야 해?"라고 묻거나 특정 로드맵 항목의 상세 정보를 요청할 때 사용합니다.
*   **입력 (Input)**
    *   `subject_name: string` (Subject의 정확한 명칭, 예: 'Vector DB', 'Python Syntax')
*   **출력 (Output)**
    *   특정 Subject의 상세 학습 개념(Lv1, Lv2, Lv3)을 조회합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "subject": "string",
      "concepts": {
        "Lv1": ["concept1", "concept2"],
        "Lv2": ["concept3"],
        "Lv3": ["concept4"]
      }
    }
    ```

### `❗get_techtree_trend`
*   **활성 조건 (Trigger Condition)**
    *   최신 뉴스, 트렌드, 사례 등을 요청할 때 사용합니다 (한국어 질문에는 'k_blog' 사용).
*   **입력 (Input)**
    *   `keywords: list[str]` (3-5개의 관련 기술 키워드 리스트)
    *   `category: string` (기본값: "k_blog")
*   **출력 (Output)**
    *   키워드를 기반으로 웹 검색을 수행하여 최신 AI 기술 트렌드와 뉴스를 제공합니다.
*   **출력 형식 (Output Format)**
    ```json
    {
      "trend_brief": [
        { "title": "string", "link": "string (URL)", "summary": "string" }
      ]
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
      "starting_point": "Tier 1: Core System Foundation"
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
      "trend_brief": [
        { "title": "우아한형제들: LLM을 활용한 메뉴 추천 시스템", "link": "https://techblog.woowahan.com/...", "summary": "..." },
        { "title": "당근: RAG 기반 검색 품질 개선기", "link": "https://medium.com/daangn/...", "summary": "..." }
      ]
    }
    ```
4.  **Final Answer**: "한국의 주요 테크 기업들은 RAG를 다음과 같이 활용하고 있습니다: \n- **우아한형제들**: LLM을 활용해 배달 메뉴를 추천하는 시스템을 구축했습니다. [상세보기](https://techblog.woowahan.com/...)\n- **당근**: 검색 품질을 높이기 위해 RAG 기술을 도입하여 사용자 의도를 더 정확히 파악하고 있습니다. [상세보기](https://medium.com/daangn/...)"
