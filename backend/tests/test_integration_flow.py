import pytest
import os
import json
from dotenv import load_dotenv

# 테스트 실행 전 .env 로드
load_dotenv(dotenv_path="backend/.env")

# Agent 모듈 Import
from app.ai.agents import main_agent

@pytest.mark.asyncio
async def test_integration_flow():
    """
    [Integration Test] MCP Server Main Flow
    1. start_interview: 주제 추천
    2. generate_questions: 문제 생성
    3. evaluate_answer: 답변 평가 (Pass & Fail 시나리오)
    4. summarize_result: 결과 리포트
    """
    print("\n🚀 [Integration Test] Starting MCP Agents Integration Flow...")

    # --- Step 1: Start Interview (Topic Recommendation) ---
    print("\n📝 [Step 1] Testing start_interview...")
    user_greet = "안녕하세요, 저는 백엔드 개발자인데 AI 지식을 테스트해보고 싶어요."
    
    # Tool 객체는 직접 호출이 불가능하므로 .ainvoke 사용
    recommendation = await main_agent.start_interview.ainvoke({"user_input": user_greet})
    
    print(f"User: {user_greet}")
    print(f"AI Recommendation: {recommendation}")
    
    assert recommendation is not None
    assert len(recommendation) > 20

    # --- Step 2: Generate Questions ---
    print("\n📝 [Step 2] Testing generate_questions...")
    topic = "Python"
    level = "Basic"
    count = 2
    
    questions = await main_agent.generate_questions.ainvoke({
        "topic": topic, 
        "level": level, 
        "count": count
    })
    
    print(f"Generated {len(questions)} questions on {topic} ({level})")
    print(json.dumps(questions[0], indent=2, ensure_ascii=False))
    
    assert isinstance(questions, list)
    assert len(questions) == count
    assert "question_text" in questions[0]
    assert "model_answer" in questions[0]
    
    # 테스트를 위해 첫 번째 문제 가져오기
    target_question = questions[0]
    q_text = target_question["question_text"]

    # --- Step 3: Evaluate Answer (Fail / Deep Dive Scenario) ---
    print("\n📝 [Step 3] Testing evaluate_answer (Weak Answer)...")
    user_weak_answer = "잘 모르겠습니다. 그냥 리스트 같은 거 아닌가요?"
    
    eval_result_weak = await main_agent.evaluate_answer.ainvoke({
        "question": q_text,
        "user_answer": user_weak_answer,
        "level": level
    })
    
    print(f"Weak Answer Result: {json.dumps(eval_result_weak, indent=2, ensure_ascii=False)}")
    
    assert eval_result_weak["is_pass"] is False
    assert eval_result_weak["score"] < 70
    assert eval_result_weak["next_action"] == "DEEP_DIVE"
    # Interviewer가 생성한 친절한 피드백 메시지가 있는지 확인
    assert len(eval_result_weak["feedback"]) > 10

    # --- Step 5: Summarize Result ---
    print("\n📝 [Step 5] Testing summarize_result...")
    
    history_log = [
        f"Q: {q_text}",
        f"A: {user_weak_answer}",
        f"Eval: {eval_result_weak['score']}점, {eval_result_weak['feedback']}"
    ]
    
    report = await main_agent.summarize_result.ainvoke({"conversation_history": history_log})
    
    print("Final Report:")
    print(report)
    
    assert report is not None
    assert len(report) > 50
    # Markdown 형식 체크 (Rough)
    # assert "#" in report or "-" in report

    print("\n✅ [Success] All agents are communicating correctly!")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

# source .venv/bin/activate
# pytest tests/test_integration_flow.py -v -s