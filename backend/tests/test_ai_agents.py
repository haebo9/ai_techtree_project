import pytest
import os
from dotenv import load_dotenv

# 테스트 실행 전 .env 로드 (API KEY 확보)
load_dotenv(dotenv_path="backend/.env")

from app.ai.agents.interviewer import generate_interview_response
from app.ai.agents.evaluator import evaluate_answer

@pytest.mark.asyncio
async def test_interviewer_agent():
    """면접관 에이전트가 정상적으로 응답하는지 테스트"""
    print("\n[Test] Interviewer Agent 시작...")
    
    user_input = "안녕하세요, 저는 3년차 백엔드 개발자입니다."
    response = await generate_interview_response(user_input, history=[])
    
    print(f"User: {user_input}")
    print(f"AI: {response}")
    
    assert response is not None
    assert len(response) > 5
    print("✅ Interviewer Agent 테스트 통과")

@pytest.mark.asyncio
async def test_evaluator_agent_good_answer():
    """평가자 에이전트가 정답에 대해 높은 점수를 주는지 테스트"""
    print("\n[Test] Evaluator Agent (Good Answer) 시작...")
    
    question = "Python의 List와 Tuple의 차이점은 무엇인가요?"
    good_answer = "List는 가변(Mutable)적이라 수정이 가능하지만, Tuple은 불변(Immutable)이라 생성 후 수정이 불가능합니다."
    
    result = await evaluate_answer(question, good_answer)
    
    print(f"Result: {result}")
    
    assert result['score'] >= 70
    assert result['is_passed'] is True
    print("✅ Evaluator Agent (Good Answer) 테스트 통과")

@pytest.mark.asyncio
async def test_evaluator_agent_bad_answer():
    """평가자 에이전트가 오답에 대해 낮은 점수를 주는지 테스트"""
    print("\n[Test] Evaluator Agent (Bad Answer) 시작...")
    
    question = "Python의 List와 Tuple의 차이점은 무엇인가요?"
    bad_answer = "둘 다 똑같습니다. 그냥 괄호 모양만 달라요."
    
    result = await evaluate_answer(question, bad_answer)
    
    print(f"Result: {result}")
    
    assert result['score'] < 50
    assert result['is_passed'] is False
    print("✅ Evaluator Agent (Bad Answer) 테스트 통과")
