from typing import Dict, List, Any, Optional
import asyncio

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

from app.ai.agents import qamaker_agent, interviewer_agent, evaluator_agent
# from app.core.config import settings

# -------------------------------------------------------------------------
# MCP Tools Definition
# Main Agent acts as a provider/registry of these tools.
# -------------------------------------------------------------------------

@tool("generate_questions", description="Generate interview questions based on topic and difficulty level.")
async def generate_questions(topic: str, level: str, count: int = 1) -> List[Dict[str, Any]]:
    """
    Generate interview questions based on a topic and difficulty level.
    Use this tool when the user wants to start a new quiz or interview session.
    """
    print(f"🕵️‍♂️ [Tool:generate_questions] Generating {count} questions for {topic} ({level})...")
    
    tasks = [
        qamaker_agent.generate_single_question(skill=topic, topic=topic, level=level) 
        for _ in range(count)
    ]
    
    results = await asyncio.gather(*tasks)
    return results


@tool("evaluate_answer", description="Evaluate user Answer and decide Next Action (PASS/DEEP_DIVE).")
async def evaluate_answer(question: str, user_answer: str, level: str) -> Dict[str, Any]:
    """
    Evaluate the user's answer and decide the next course of action.
    Use this tool immediately after the user provides an answer to an interview question.
    """
    print(f"🤔 [Tool:evaluate_answer] Evaluating answer for {level}...")

    # Reuse evaluator agent logic
    eval_result = await evaluator_agent.evaluate_answer(
        question=question,
        user_answer=user_answer,
        model_answer="N/A", 
        evaluation_criteria=[f"Level: {level}"]
    )
    
    is_pass = eval_result.get("is_passed", False)
    next_action = "PASS" if is_pass else "DEEP_DIVE"
    
    return {
        "score": eval_result.get("score", 0),
        "feedback": eval_result.get("feedback", ""),
        "is_pass": is_pass,
        "next_action": next_action
    }


@tool("generate_followup", description="Generate a sharp follow-up question for deep dive.")
async def generate_followup(previous_question: str, user_answer: str, level: str) -> str:
    """
    Generate a follow-up (deep dive) question when the user's answer requires further probing.
    Use this tool when 'evaluate_answer' returns 'next_action' as 'DEEP_DIVE'.
    """
    context_prompt = f"""
    [상황]
    - 이전 질문: {previous_question}
    - 사용자 답변: {user_answer}
    - 레벨: {level}
    
    사용자의 답변이 부족하거나 더 검증이 필요합니다. 
    관련된 개념의 트레이드오프나 엣지 케이스를 묻는 날카로운 '꼬리 질문(Follow-up)'을 하나만 생성하세요.
    """
    
    followup_q = await interviewer_agent.generate_interview_response(
        user_input=context_prompt,
        history=[] 
    )
    
    return followup_q


@tool("summarize_result", description="Analyze conversation logic and generate a final report.")
async def summarize_result(conversation_history: List[str]) -> str:
    """
    Analyze the full conversation history and generate a comprehensive final report.
    Use this tool when the interview session is finished.
    """
    full_log = "\n".join(conversation_history)
    
    report_prompt = f"""
    당신은 AI TechTree의 최종 평가관입니다.
    다음 인터뷰 로그를 바탕으로 종합 리포트를 작성해주세요.
    
    [로그]
    {full_log}
    
    [출력 형식]
    Markdown 포맷으로 다음 내용을 포함:
    1. 종합 점수 및 등급
    2. 강점 (Strengths)
    3. 보완점 (Weaknesses)
    4. 향후 학습 가이드
    """
    
    # Direct invocation of Evaluator LLM
    response = await evaluator_agent.llm.ainvoke([HumanMessage(content=report_prompt)])
    
    return response.content

# List of tools exported for easy registration
TOOLS = [generate_questions, evaluate_answer, generate_followup, summarize_result]

