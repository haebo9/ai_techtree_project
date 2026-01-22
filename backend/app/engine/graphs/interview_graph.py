from typing import TypedDict, List, Annotated, Optional, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.engine.agents.qamaker_agent import generate_questions
from app.engine.agents.evaluator_agent import evaluate_answer, analyze_interview_result
from app.engine.agents.interviewer_agent import generate_feedback_message, format_final_report, recommend_topic_response
from app.services.interview_service import interview_service

# 1. State Definition
class InterviewState(TypedDict):
    # Standard LangChain/LangGraph message history
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Session Context
    user_id: str
    user_db_id: str
    track: str
    topic: str
    level: str
    
    # Internal State
    generated_questions: List[dict]  # Queue of questions
    current_question: Optional[dict] # Currently active question
    evaluation_result: Optional[dict] # Result of the last evaluation
    star_gained: bool # Flag to check if star was gained in parsing turn
    
    # Progress
    question_count: int
    max_questions: int
    interview_complete: bool

# 2. Nodes

async def consult_curriculum_node(state: InterviewState):
    """
    [Phase 1] Consultation Node
    Analyzes user input to recommend a track or topic using MCP tools.
    Decides whether to stay in consultation or start the interview.
    """
    last_message = state["messages"][-1] if state["messages"] else None
    user_input = last_message.content if isinstance(last_message, HumanMessage) else "Help me choose a topic."
    
    # Simple Heuristic for Demo:
    # If input contains "start" or "begin" and we have a topic, we proceed.
    # Otherwise, we treat it as consultation.
    # In a real agent, we would use an LLM classifier here.
    
    if "start" in user_input.lower() or "시작" in user_input:
        # Assuming the topic was set in previous turns or defaults
        return {"messages": [AIMessage(content="네, 면접을 시작합니다!")]}

    # Call Interviewer Agent (Consultant Mode)
    recommendation = await recommend_topic_response(user_input)
    
    return {
        "messages": [AIMessage(content=recommendation)]
    }

async def generate_question_node(state: InterviewState):
    """
    [Phase 2] Generate Question Node
    Generates a question if needed, or pops one from the queue.
    Also handles User Initialization on first run.
    """
    # 0. DB Initialization (One-time)
    if not state.get("user_db_id"):
        # For prototype, use a fixed guest email or derive from user_id if possible
        email = f"guest_{state.get('user_id', 'anon')}@techtree.com"
        nickname = f"User_{state.get('user_id', 'anon')}"
        
        user = await interview_service.get_or_create_user(email, nickname)
        state["user_db_id"] = str(user.id)

    # Initialize defaults if missing
    track = state.get("track", "Python")
    topic = state.get("topic", "General")
    level = state.get("level", "Intermediate")
    
    # If no questions in queue, generate a batch (or just 1)
    if not state.get("generated_questions"):
        new_questions = await generate_questions(skill=track, topic=topic, level=level, count=1)
        
        if not new_questions:
             return {
                "messages": [AIMessage(content="질문 생성에 실패했습니다. 다시 시도해주세요.")],
             }
        
        # Save Generated Questions to Asset DB (Added Requirement)
        # TODO: Implement bulk save in InterviewService
        # await interview_service.save_questions(new_questions)
        
        state["generated_questions"] = new_questions
    
    # Pop the next question
    questions = state["generated_questions"]
    if not questions:
        return {
            "messages": [AIMessage(content="더 이상 질문을 생성할 수 없습니다. 면접을 종료합니다.")],
            "interview_complete": True
        }
    
    next_q = questions.pop(0)
    current_q_text = next_q.get("question_text", "")
    
    return {
        "user_db_id": state["user_db_id"],
        "generated_questions": questions,
        "current_question": next_q,
        "current_answer": None, 
        "star_gained": False,
        "messages": [AIMessage(content=current_q_text)]
    }

async def evaluate_answer_node(state: InterviewState):
    """
    [Phase 2] Evaluate Answer Node
    """
    current_q = state.get("current_question")
    if not current_q:
        return {"messages": [AIMessage(content="현재 진행 중인 질문이 없습니다. 새로운 질문을 준비하겠습니다.")]}
        
    last_message = state["messages"][-1]
    user_answer = last_message.content
        
    # 1. AI Evaluation
    eval_result = await evaluate_answer(
        question=current_q.get("question_text", ""),
        user_answer=user_answer,
        model_answer=current_q.get("model_answer", "N/A"),
        evaluation_criteria=current_q.get("evaluation_criteria", [])
    )
    
    # 2. DB Update (Skill & Stars)
    star_gained = False
    if state.get("user_db_id"):
        subject = current_q.get("topic", state.get("topic", "General"))
        is_passed = eval_result.get("is_passed", False)
        score = eval_result.get("score", 0)
        
        star_gained = await interview_service.update_skill_status(
            user_id=state["user_db_id"], 
            subject=subject, 
            passed=is_passed, 
            score=score
        )
    
    return {
        "evaluation_result": eval_result,
        "question_count": state.get("question_count", 0) + 1,
        "star_gained": star_gained
    }

async def feedback_node(state: InterviewState):
    """
    [Phase 2] Feedback Node
    """
    eval_result = state.get("evaluation_result", {})
    current_q = state.get("current_question", {})
    star_gained = state.get("star_gained", False)
    
    if not eval_result:
        return {"messages": [AIMessage(content="평가 결과를 불러오지 못했습니다.")]}

    feedback_msg = await generate_feedback_message(
        question=current_q.get("question_text", ""),
        user_answer=state["messages"][-1].content,
        score=eval_result.get("score", 0),
        is_pass=eval_result.get("is_passed", False),
        feedback=eval_result.get("feedback", "")
    )
    
    final_output = feedback_msg
    if star_gained:
        final_output = f"🎉 **[별 획득!]** 축하합니다! 해당 주제({current_q.get('topic', 'General')})의 숙련도가 상승했습니다. ⭐\n\n" + final_output
    
    return {
        "messages": [AIMessage(content=final_output)]
    }

async def final_report_node(state: InterviewState):
    """
    [Phase 3] Final Report Node
    """
    history = [f"{m.type}: {m.content}" for m in state["messages"]]
    analysis_data = await analyze_interview_result(history)
    analysis_str = str(analysis_data) 
    final_report = await format_final_report(analysis_str)
    
    return {
        "messages": [AIMessage(content=final_report)],
        "interview_complete": True
    }

# 3. Conditional Logic

def route_input(state: InterviewState) -> Literal["consult_curriculum", "evaluate_answer", "generate_question"]:
    """
    Determines the entry point based on state and message.
    """
    messages = state.get("messages", [])
    
    # Case 1: Start of Session -> Go to Consultation
    if not messages:
        return "consult_curriculum"
    
    last_msg = messages[-1]
    
    # Case 2: User reply
    if isinstance(last_msg, HumanMessage):
        # Case 2-A: If we have an active question, evaluate the answer
        if state.get("current_question"):
            return "evaluate_answer"
            
        # Case 2-B: No active question -> It's a consultation turn
        # But wait, if user said "Start", we should have handled it in consult_curriculum?
        # Graph logic: After consult_curriculum, we wait for user. Next human msg comes here.
        # We need to check if user wants to start.
        if "start" in last_msg.content.lower() or "시작" in last_msg.content:
            return "generate_question"
            
        return "consult_curriculum"
    
    # Case 3: AI message (Transition check)
    return "consult_curriculum"

def check_consult_result(state: InterviewState) -> Literal["generate_question", "__end__"]:
    """
    After consultation response, do we start interview or wait for user?
    """
    messages = state["messages"]
    last_ai_msg = messages[-1].content
    
    # If the AI itself decided to start (e.g., "Starting interview..."), we could auto-route.
    # But usually we wait for user confirmation.
    
    # For now, always wait for user input after consultation.
    return "__end__"

def check_next_step(state: InterviewState) -> Literal["generate_question", "final_report"]:
    count = state.get("question_count", 0)
    max_q = state.get("max_questions", 3)
    
    if count >= max_q:
        return "final_report"
    else:
        return "generate_question"

# 4. Graph Construction

workflow = StateGraph(InterviewState)

# Add Nodes
workflow.add_node("consult_curriculum", consult_curriculum_node)
workflow.add_node("generate_question", generate_question_node)
workflow.add_node("evaluate_answer", evaluate_answer_node)
workflow.add_node("provide_feedback", feedback_node)
workflow.add_node("final_report", final_report_node)

# Entry Point
workflow.set_conditional_entry_point(
    route_input,
    {
        "consult_curriculum": "consult_curriculum",
        "generate_question": "generate_question",
        "evaluate_answer": "evaluate_answer",
    }
)

# Edges

# Phase 1: Consultation
workflow.add_conditional_edges(
    "consult_curriculum",
    check_consult_result,
    {
        "generate_question": "generate_question",
        "__end__": END
    }
)

# Phase 2: Interview Loop
workflow.add_edge("generate_question", END) # Wait for answer
workflow.add_edge("evaluate_answer", "provide_feedback")
workflow.add_conditional_edges(
    "provide_feedback",
    check_next_step,
    {
        "generate_question": "generate_question",
        "final_report": "final_report"
    }
)

# Phase 3: Conclusion
workflow.add_edge("final_report", END)

# Compile
app = workflow.compile()
