# Database Schema Design (MongoDB)

- **[1. Overview](#1-overview)**
- **[2. Collections Specification](#2-collections-specification)**
  - [2.1 users (사용자/학습현황)](#21-users-사용자-및-학습-현황)
  - [2.2 interviews (면접/평가)](#22-interviews-면접-로그-및-평가)
  - [2.3 tracks (커리큘럼 원본)](#23-tracks-커리큘럼-원본-데이터)
  - [2.4 trends (기술 트렌드)](#24-trends-기술-트렌드-데이터)
  - [2.5 questions (면접 질문 은행)](#25-questions-면접-질문-은행)
  - [2.6 concepts (상세 개념 사전)](#26-concepts-상세-개념-사전)

---

## 1. Overview
> 본 문서는 **AI TechTree** 프로젝트의 **전체 데이터 모델**을 정의합니다.
> 기존의 정적 파일(`track.py`, `trend.json`)로 관리되던 **Source Data**를 DB로 이관하여, 실시간 업데이트와 관리가 가능한 구조로 전환하는 것을 목표로 합니다.

> **핵심 설계 원칙 (MongoDB)**
> 1.  **Source Data Centralization**: 커리큘럼(`tracks`)과 트렌드(`trends`) 정보를 DB에서 통합 관리.
> 2.  **Rich Document Structure**: 복잡한 계층 구조(Track -> Step -> Subject -> Level -> Concept)를 하나의 문서에 내장(Embedding)하여 조회 효율성 극대화.
> 3.  **Real-time Updates**: 크롤링된 트렌드 데이터나 수정된 커리큘럼이 즉시 서비스에 반영되도록 설계.

---

## 2. Collections Specification

### 2.1 `users` (사용자 및 학습 현황)
> 사용자의 계정 정보와 **기술 트리 진행 상황**을 관리합니다.

* **Index**: `{"auth.email": 1}` (Unique), `{"auth.uid": 1}`

```javascript
{
  "_id": ObjectId("..."), // [PK] MongoDB 자동 생성 ID
  "auth": {
    "email": "user@example.com",     // 로그인 ID
    "provider": "kakao",             // 소셜 로그인 제공자
    "uid": "123456789"               // 제공자 측 고유 ID
  },
  "profile": {
    "nickname": "AI_Master",
    "avatar_url": "https://...",
    "job_title": "Student"
  },
  "stats": {
    "total_stars": 12,               // 획득한 총 별 개수
    "completed_tracks": ["AI Engineer"]
  },
  /**
   * [User State] 학습 진행도
   * Subject 이름을 Key로 사용하여 O(1) 접근
   */
  "skill_tree": {
    "Python Syntax & Types": {
      "level": 2,                    // 현재 레벨 (0:Locked, 1:Basic, 2:Adv, 3:Master)
      "stars": 2,                    // 획득한 별
      "last_tested_at": ISODate("...")
    },
    "FastAPI Essentials": {
      "level": 1,
      "stars": 1,
      "last_tested_at": ISODate("...")
    }
  },
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

### 2.2 `interviews` (면접 로그 및 평가)
> AI 면접관과의 대화 기록 및 최종 평가 결과(Snapshot)입니다.

* **Index**: `{"user_id": 1}`, `{"meta.status": 1}`

```javascript
{
  "_id": ObjectId("..."), // [PK] MongoDB 자동 생성 ID
  "user_id": ObjectId("..."),
  "meta": {
    "subject": "Python Syntax & Types", // 대상 과목
    "track": "Track 0: The Origin",     // (Optional) 문맥 트랙
    "target_level": 2,                  // 시도한 레벨
    "status": "COMPLETED",              // IN_PROGRESS, COMPLETED, FAILED
    "started_at": ISODate("..."),
    "ended_at": ISODate("...")
  },
  "messages": [                         // 대화 로그
    { "role": "assistant", "content": "..." },
    { "role": "user", "content": "..." }
  ],
  "result": {                           // 평가 결과
    "is_passed": true,
    "score": 85,
    "feedback": "...",
    "evaluated_at": ISODate("...")
  }
}
```

### 2.3 `tracks` (커리큘럼 원본 데이터)
> **[Source Data]** 기존 `track.py`의 `AI_TECH_TREE` 내용을 대체합니다.
> 복잡한 계층(Track > Step > Subject > Level > Concept)을 모두 포함합니다.

* **Index**: `{"title": 1}` (Unique)

```javascript
{
  "_id": ObjectId("..."), // [PK] MongoDB 자동 생성 ID
  "title": "Track 1: AI Engineer",    // 트랙명 (ID 역할)
  "description": "모델을 실제 서비스 환경에 이식하고 가동합니다.",
  "order": 1,                         // 트랙 표시 순서
  
  /**
   * [Structure] 커리큘럼 계층 구조
   * Steps -> (Options) -> Subjects -> Levels
   */
  "steps": [
    {
      "step_name": "Step 1: Core System Foundation",
      "type": "FIXED",                // FIXED(필수), BRANCH(분기/선택)
      "subjects": [
        {
          "title": "FastAPI Essentials",
          "levels": {
            "Lv1": ["GET vs POST", "Path/Query Params", ...],
            "Lv2": ["Pydantic", "Dependency Injection", ...],
            "Lv3": ["Middleware", "OAuth2", ...]
          }
        },
        {
          "title": "Docker Basics",
          "levels": { "Lv1": [...], "Lv2": [...], "Lv3": [...] }
        }
      ]
    },
    {
      "step_name": "Step 2: Branching Point",
      "type": "BRANCH",               // 선택 분기점
      "options": [
        {
          "option_name": "Option 1: Serving Specialist",
          "subjects": [
            { "title": "Model Serialization", "levels": { ... } },
            { "title": "Inference Optimization", "levels": { ... } }
          ]
        },
        {
          "option_name": "Option 2: App Architect",
          "subjects": [
            { "title": "Database Design", "levels": { ... } },
            { "title": "Caching Strategy", "levels": { ... } }
          ]
        }
      ]
    }
  ],
  "last_updated": ISODate("...")
}
```

### 2.4 `trends` (기술 트렌드 데이터)
> **[Source Data]** 기존 `trend.json`을 대체하며, 웹 검색 에이전트가 수집한 최신 기술 동향을 주제별로 그룹화하여 저장합니다.

* **Index**: `{"category": 1}` (Unique per category ID), `{"items.link": 1}` (Embedded Index - 카테고리 내 중복 방지)

```javascript
{
  "_id": ObjectId("..."), // [PK] MongoDB 자동 생성 ID
  "category": "tech_news",             // tech_news, engineering, research, k_blog
  
  /**
   * [Grouped Items] 해당 카테고리에 속한 트렌드 리스트
   * 개별 문서로 나뉘지 않고 하나의 카테고리 문서 내에 임베딩됨
   */
  "items": [
    {
      "title": "2025년을 위한 7개의 데이터베이스 | GeekNews",
      "link": "https://news.hada.io/weekly/202451",
      "summary": "AI 시대에 주목받는 DB 7선 정리...",
      "tags": ["데이터베이스", "Backend", "2025_Trend"],
      "source_domain": "news.hada.io",
      "collected_at": ISODate("2026-01-08T12:00:00Z"),
      "view_count": 0
    },
    {
      "title": "State of AI Report 2025",
      "link": "...",
      ...
    }
  ],
  
  "last_updated": ISODate("...")
}
```

### 2.5 `questions` (면접 질문 은행)
> 각 Subject 및 Level에 해당하는 면접 질문과 모범 답안을 관리합니다.

* **Index**: `{"subject": 1, "level": 1}`

```javascript
{
  "_id": ObjectId("..."), // [PK] MongoDB 자동 생성 ID
  "subject": "FastAPI Essentials",    // tracks.steps.subjects.title 과 매핑
  "level": "Lv2",                     // Lv1, Lv2, Lv3
  "topic": "Dependency Injection",    
  "question_text": "FastAPI에서 Dependency Injection이 가지는 장점은 무엇인가요?",
  "model_answer": "코드 재사용성을 높이고, 테스트 시 모의 객체(Mock) 주입을 용이하게 합니다...",
  "keywords": ["IoC", "Testability", "Decoupling"],
  "created_at": ISODate("...")
```

### 2.6 `concepts` (상세 개념 & RAG 원본)
> **Track -> Levels -> Concept List**에 명시된, 가장 작은 단위의 개념(Concept)에 대한 **원본 지식(Knowledge Base)** 을 저장합니다.
> 이 데이터는 **면접 문제 생성(Question Generation)** 이나 **RAG(검색 증강 생성)** 의 원천 소스로 활용됩니다.

* **Index**: `{"subject": 1, "level": 1}`, `{"name": 1}`

```javascript
{
  "_id": ObjectId("..."), // [PK] MongoDB 자동 생성 ID
  "subject": "FastAPI Essentials",    // Parent Subject
  "level": "Lv1",                     // Lv1, Lv2, Lv3
  "name": "GET vs POST 요청 메서드의 차이", // tracks의 Lv 리스트에 있는 텍스트와 정확히 일치
  
  "summary": "GET은 데이터 조회를 위해 URL에 파라미터를 포함하여 요청을 보내는 방식이고 POST는 리소스 생성 및 수정을 위해 HTTP Body에 데이터를 포함하여 보내는 방식입니다.",

  /**
   * [RAG Source] 문제 생성의 원천이 되는 순수 텍스트 지식
   * 줄바꿈, 탭, 마크다운 등의 포맷팅을 최대한 배제한 문장 나열 형태
   */
  "description": "GET 요청은 서버로부터 데이터를 조회할 때 사용하며 요청 데이터가 URL의 Query String에 포함되어 전송되므로 보안이 중요한 데이터 전송에는 적합하지 않습니다 반면 POST 요청은 데이터를 생성하거나 서버의 상태를 변경할 때 사용하며 데이터가 HTTP Body에 포함되어 전송되므로 길이 제한이 없고 GET보다 상대적으로 안전합니다 또한 GET은 멱등성(Idempotent)을 가지지만 POST는 멱등성을 가지지 않는다는 중요한 차이점이 있습니다...",
  
  "references": [
    "https://developer.mozilla.org/ko/docs/Web/HTTP/Methods/GET",
    "https://developer.mozilla.org/ko/docs/Web/HTTP/Methods/POST"
  ],
  "updated_at": ISODate("...")
}
```

> **데이터 흐름 (Data Flow)**
> 1.  **`tracks`**: 커리큘럼 뼈대와 개념의 **이름**("GET vs POST...")을 정의.
> 2.  **`concepts`**: 해당 이름에 대한 **상세 지식(텍스트)** 을 저장.
> 3.  **`questions`**: `concepts`의 텍스트를 바탕으로 LLM이 생성한 **면접 문제**를 저장.

