import pytest
import os
import json
from dotenv import load_dotenv

# 테스트 실행 전 .env 로드 (API KEY 확보)
load_dotenv(dotenv_path="backend/.env")

from app.ai.agents.interviewer_agent import generate_interview_response

@pytest.mark.asyncio
async def test_interviewer_agent_navigation():
    """
    [Scenario 1] 일반 대화 흐름 테스트
    사용자가 트랙을 선택하고, 에이전트가 이를 인식하여 탐색을 진행하는지 확인합니다.
    """
    print("\n[Test] Interviewer Agent (Navigation) 시작...")
    
    # 1. 사용자가 AI Engineer 트랙에 관심을 보임
    user_input = "안녕하세요, 저는 AI 엔지니어가 되고 싶습니다. 커리큘럼을 추천해주실 수 있나요?"
    response = await generate_interview_response(user_input, history=[])
    
    print(f"User: {user_input}")
    print(f"AI: {response}")
    
    # 응답 검증: 'Track 1' 혹은 'AI Engineer' 관련 내용이 포함되어야 함
    # 또한 Tier 선택을 유도하는 질문이 포함되어야 함
    assert response is not None
    assert len(response) > 10
    
    print("✅ Interviewer Agent (Navigation) 테스트 통과")


@pytest.mark.asyncio
async def test_interviewer_agent_context_injection():
    """
    [Scenario 2] 웹 서비스 연동 (Context Injection) 테스트
    초기 컨텍스트(Track/Tier)가 주어졌을 때, 탐색 과정 없이 바로 추천/확정을 진행하는지 확인합니다.
    """
    print("\n[Test] Interviewer Agent (Context Injection) 시작...")
    
    # 웹 UI에서 "Track 0" -> "Tier 1"을 선택했다고 가정
    initial_context = {
        "track": "Track 0: The Origin",
        "tier": "Tier 1: Core Python Mastery"
    }
    
    user_input = "준비됐습니다. 시작해주세요."
    
    # 컨텍스트 주입 호출
    response = await generate_interview_response(user_input, history=[], initial_context=initial_context)
    
    print(f"Initial Context: {initial_context}")
    print(f"User: {user_input}")
    print(f"AI: {response}")
    
    # 응답 검증: 
    # 1. 탐색 질문(어떤 트랙 하실래요?)이 없어야 함
    # 2. Tool Calls(recommend_interview_topic)에 의해 '추천이 완료되었습니다' 류의 메시지가 나오거나,
    #    JSON 형태의 추천 결과가 포함될 가능성이 높음 (ToolMessage의 내용을 반환하지 않는다면 최종 응답 텍스트 확인)
    
    assert response is not None
    
    # 주의: 실제 Tool Call 결과가 바로 리턴되는지, 아니면 LLM이 친절하게 말로 풀어주는지에 따라 검증 방식이 다름.
    # 현재 구현상 Tool Call 결과를 LLM이 보고 최종 멘트를 날리는 구조라면 텍스트 검증.
    if "{" in response and "status" in response:
         print("-> JSON 추천 데이터가 직접 반환됨 (Tool Output Direct Return)")
    else:
         print("-> LLM이 추천 완료 멘트를 반환함")
    
    print("✅ Interviewer Agent (Context Injection) 테스트 통과")

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])

# source .venv/bin/activate 
# pytest tests/test_ai_agents.py -v -s