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
1. 웹 개발 3년차인데 AI 쪽으로 커리어를 전환하고 싶어. 내 경험에 맞는 트랙을 추천해줘.
2. AI Engineer 트랙의 학습 로드맵을 단계별로 자세히 보여줘.
3. 요즘 주목받는 LLM Agent와 RAG 기술의 최신 트렌드를 알려줘.

---

## 🛠️ 도구 상세 명세 (Tool Specifications)
*(참고: 아래의 'LLM 지침' 내용은 실제 구현 시 Tool의 `description` 필드나 `docstring`에 포함되어야 LLM이 인식할 수 있습니다.)*

### `get_ai_track`
*   **용도 및 지침 (Description & Instruction)**
    Analyzes user interests and experience to recommend the most suitable AI career track.
    
    [Instruction for LLM]
    1. **Thought**: Analyze the user's input to extract technical interests and experience level.
    2. **Response**: Use the `reason` field from the result to explain why this track is a good match, and encourage them to start at the `starting_point`.
*   **파라미터 (Parameters)**
    *   `interests: list[str]`
    *   `experience_level: string`
*   **출력 형식 (Observation)**
    ```json
    {
      "recommended_track": "string (Track Name)",
      "reason": "string (Why this track fits based on input)",
      "starting_point": "string (Immediate next step)"
    }
    ```

### `get_ai_path`
*   **용도 및 지침 (Description & Instruction)**
    Retrieves a structured learning roadmap (Subjects & Concepts) for a specific AI track.

    [Instruction for LLM]
    1. **Thought**: Identify the specific track name the user is interested in.
    2. **Response**: Present the `roadmap` from the result in a clear, hierarchical list. Highlight the `next_milestone` as the immediate goal.
*   **파라미터 (Parameters)**
    *   `track_name: string`
*   **출력 형식 (Observation)**
    ```json
    {
      "roadmap": [
        { "tier": "string", "subjects": ["string"] }
      ],
      "next_milestone": "string"
    }
    ```

### `get_ai_trend`
*   **용도 및 지침 (Description & Instruction)**
    Fetches real-time AI technology trend and news based on keywords with specific content categories.

    [Instruction for LLM]
    1. **Thought**: Extract key technical terms from the user's query and DETERMINE the appropriate content `category`.
       - Use "k_blog" if the user query is in Korean or asks for Korean content. (Primary choice for Korean users)
       - Use "tech_news" for Global/English news updates.
       - Use "engineering" for implementation details, code, or GitHub repos.
       - Use "research" for academic papers, Arxiv, or deep research.
    2. **Response**: Summarize the `trend_brief` items from the result. Ensure all URLs in `link` are clickable Markdown links.
*   **파라미터 (Parameters)**
    *   `keywords: list[str]`
    *   `category: string` ("tech_news", "engineering", "research", "k_blog")
*   **출력 형식 (Observation)**
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

### Scenario: 적성 진단
**User**: "웹 개발 3년차인데 AI 쪽으로 커리어를 전환하고 싶어."

**Agent (ReAct Loop)**:
1.  **Thought**: 사용자가 '웹 개발 3년차(Web, Intermediate)' 경험과 'AI 전환' 의사를 밝혔다. 적합한 트랙 추천을 위해 `get_ai_track` 도구를 사용해야 한다.
2.  **Action**: `get_ai_track(interests=["web", "backend"], experience_level="intermediate")`
3.  **Observation**:
    ```json
    {
      "recommended_track": "Track 1: AI Engineer",
      "reason": "웹 개발 경험을 살려 API 서빙 및 시스템 구축 분야로 확장하기 좋습니다.",
      "starting_point": "Tier 1: Core System Foundation"
    }
    ```
4.  **Final Answer**: "웹 개발 3년차 경력을 살려 **Track 1: AI Engineer**로 시작해보시는 것을 추천합니다! 이 트랙은 백엔드 경험을 바탕으로 시스템 구축 역량을 확장하기에 가장 적합합니다. 첫 단계인 **Tier 1: Core System Foundation**부터 학습을 시작해보세요."

### Scenario: 기술 트렌드 파악 (한국 기업 사례)
**User**: "요즘 한국 기업들은 RAG 기술을 실무에 어떻게 적용하고 있어?"

**Agent (ReAct Loop)**:
1.  **Thought**: 사용자가 'RAG' 기술에 대해 묻고 있으며, 특히 '한국 기업 실무 사례'를 원한다. 이는 `k_blog` 카테고리에 적합하다.
2.  **Action**: `get_ai_trend(keywords=["RAG", "실무", "적용"], category="k_blog")`
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
