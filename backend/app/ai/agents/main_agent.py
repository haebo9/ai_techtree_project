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
    
    # QAMaker에게 한 번에 요청 (중복 방지 및 최적화)
    try:
        results = await qamaker_agent.generate_questions(
            skill=topic, 
            topic=topic, 
            level=level, 
            count=count
        )
        
        if not results:
            return [{"error": "Failed to generate questions. Please try again."}]
            
        return results
        
    except Exception as e:
        print(f"Error in generate_questions tool: {e}")
        return [{"error": f"An error occurred: {str(e)}"}]


@tool("evaluate_answer", description="Evaluate user Answer and decide Next Action (PASS/DEEP_DIVE).")
async def evaluate_answer(question: str, user_answer: str, level: str) -> Dict[str, Any]:
    """
    Evaluate the user's answer and decide the next course of action.
    Use this tool immediately after the user provides an answer to an interview question.
    """
    print(f"🤔 [Tool:evaluate_answer] Evaluating answer for {level}...")

    # 1. Evaluator: 점수 및 팩트 체크 (Judge)
    eval_result = await evaluator_agent.evaluate_answer(
        question=question,
        user_answer=user_answer,
        model_answer="N/A", 
        evaluation_criteria=[f"Level: {level}"]
    )
    
    score = eval_result.get("score", 0)
    is_pass = eval_result.get("is_passed", False)
    eval_feedback = eval_result.get("feedback", "")
    
    # 2. Interviewer: 피드백 멘트 및 꼬리 질문 생성 (Persona/Writer)
    final_message = await interviewer_agent.generate_feedback_message(
        question=question,
        user_answer=user_answer,
        score=score,
        is_pass=is_pass,
        feedback=eval_feedback
    )

    # 3. Next Action 결정
    # 점수가 낮거나(Fail), 점수는 높지만 검증이 더 필요하다는 뉘앙스(꼬리질문)가 있다면 DEEP_DIVE
    next_action = "PASS" if is_pass else "DEEP_DIVE"
    
    return {
        "score": score,
        "feedback": final_message, # 단순 Fact가 아닌 Interviewer가 가공한 친절한 멘트
        "is_pass": is_pass,
        "next_action": next_action
    }

@tool("start_interview", description="Initiate the interview session and recommend topics.")
async def start_interview(user_input: str) -> str:
    """
    Start the interview session.
    Use this tool when the user greets or asks for an interview without a specific ongoing topic.
    It will analyze the user's intent and recommend suitable interview topics from the curriculum.
    """
    print(f"👋 [Tool:start_interview] User Input: {user_input}")
    
    # Interviewer에게 커리큘럼 기반 추천 멘트 생성을 요청
    response = await interviewer_agent.recommend_topic_response(user_input)
    
    return response


@tool("summarize_result", description="Analyze conversation logic and generate a final report.")
async def summarize_result(conversation_history: List[str]) -> str:
    """
    Analyze the full conversation history and generate a comprehensive final report.
    Use this tool when the interview session is finished.
    """
    full_log = "\n".join(conversation_history)
    
    # 1. Evaluator: 로직 분석
    report_prompt = f"""
    [로그]
    {full_log}
    
    위 로그를 분석하여 강점, 약점, 종합 점수를 도출하세요.
    """
    raw_analysis = await evaluator_agent.llm.ainvoke([HumanMessage(content=report_prompt)])
    
    # 2. Interviewer: 최종 리포트 포맷팅
    final_report = await interviewer_agent.format_final_report(raw_analysis.content)
    
    return final_report

# List of tools exported for easy registration
TOOLS = [start_interview, generate_questions, evaluate_answer, summarize_result]

