# MCP Server Design: AI TechTree Navigator

이 문서는 **Kakao PlayMCP** 환경에서 구동될 AI TechTree Navigator의 도구(Tool) 설계서입니다.
이 도구들은 사용자가 AI 엔지니어로서 성장하는 과정을 돕기 위해 설계되었으며, LLM의 도움 없이도 Python 로직만으로 정확하고 구조화된 정보를 제공합니다.

## 1. 설계 원칙 (Design Principles)
1.  **Source of Truth**: 모든 정보는 `backend/app/ai/source/topics.py`에 정의된 정형 데이터를 기반으로 합니다. (No Hallucination)
2.  **Educational Growth**: 사용자가 자신의 위치를 파악하고, 다음 학습 목표를 설정하도록 돕습니다.
3.  **Deterministic Logic**: 추천 및 검색 로직은 결정론적 알고리즘을 사용하여 일관된 결과를 보장합니다.

---

## 2. 도구 상세 명세 (Tool Specifications)


---

## 3. PlayMCP 시나리오 예시


## 4. 향후 확장성 (Future)
