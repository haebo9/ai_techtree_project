import json
from typing import List, Optional, Dict, Any, TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages

from app.core.config import settings
from app.ai.source.topics import AI_TECH_TREE

# 1. 모델 초기화
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.5,
    api_key=settings.OPENAI_API_KEY
)

# 2. Tool 정의: 에이전트가 호출할 수 있는 함수
@tool
def get_curriculum_context(track: Optional[str] = None, tier: Optional[str] = None) -> str:
    """
    Retrieves specific curriculum data from the AI Tech Tree.
    Call this tool to navigate the curriculum hierarchy: Track -> Tier -> (Option).
    
    Args:
        track: The name of the track (e.g., "Track 1: AI Engineer").
        tier: The name of the tier (e.g., "Tier 1: System Foundation").
    """
    # 1. Track 미선택: 전체 Track 목록 반환
    if not track:
        summary = {k: v.get("description", "") for k, v in AI_TECH_TREE.items()}
        return f"[Available Tracks]\n{json.dumps(summary, ensure_ascii=False, indent=2)}"

    track_data = AI_TECH_TREE.get(track)
    if not track_data:
        return "Selected Track information not found."

    # 2. Tier 미선택: 해당 Track의 Tier 목록 반환
    if not tier:
        tiers_summary = list(track_data.get("tiers", {}).keys())
        return f"[Selected Track: {track}]\nAvailable Tiers: {json.dumps(tiers_summary, ensure_ascii=False, indent=2)}"
    
    tiers = track_data.get("tiers", {})
    tier_data = tiers.get(tier)
    
    if not tier_data:
        return f"Selected Tier '{tier}' not found in {track}."
    
    # 3. Tier 선택됨: 
    # 만약 "Option"으로 시작하는 키가 있다면, 옵션 목록을 반환하여 선택 유도.
    # 옵션이 없다면, 해당 Tier의 전체 Subject 목록을 반환하여 Tier 확정 유도.
    
    # Check for Options
    options = [k for k in tier_data.keys() if k.startswith("Option")]
    
    if options:
        # 옵션들이 있으면, 그 옵션들의 키만 보여줌 (내부 Subject는 아직 숨김)
        return f"[Selected Tier: {tier}]\nThis Tier has Options. Please ask user to select one:\n{json.dumps(options, ensure_ascii=False, indent=2)}"
    
    # 옵션이 없으면 (공통 Tier), 해당 Tier의 내용을 통째로 보여주며 "이 범위로 진행하시겠습니까?" 유도
    context_data = {
        "track": track,
        "tier": tier,
        "contents": list(tier_data.keys()) # Subject 목록만 보여줌
    }
    return f"[Current Focus: {tier}]\nNo separate options. Ready to recommend this Tier.\n{json.dumps(context_data, ensure_ascii=False, indent=2)}"


@tool
def recommend_interview_topic(track: str, tier: str, option: Optional[str] = None, reason: str = "") -> str:
    """
    Finalizes the interview scope selection.
    Call this tool when the user agrees on a specific Track and Tier (and Option if applicable).
    
    Args:
        track: The selected track name.
        tier: The selected tier name.
        option: The selected option name (e.g., "Option 1: FastAPI"). Only if the Tier has options.
        reason: Brief reason for recommendation.
    """
    recommendation = {
        "status": "TOPIC_SELECTED",
        "track": track,
        "tier": tier,
        "option": option,
        "reason": reason
    }
    return json.dumps(recommendation, ensure_ascii=False)


# 3. State 정의
class InterviewerState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# 4. Graph Node 정의
def interviewer_node(state: InterviewerState):
    messages = state["messages"]
    # Tool Binding: Navigating, Recommending
    tools = [get_curriculum_context, recommend_interview_topic]
    llm_with_tools = llm.bind_tools(tools)
    return {"messages": [llm_with_tools.invoke(messages)]}

# 5. Graph 구축
workflow = StateGraph(InterviewerState)

# 노드 추가
workflow.add_node("interviewer", interviewer_node)
workflow.add_node("tools", ToolNode([get_curriculum_context, recommend_interview_topic]))

# 엣지 연결
workflow.add_edge(START, "interviewer")
workflow.add_conditional_edges("interviewer", tools_condition) # Tool 호출 여부 판단
workflow.add_edge("tools", "interviewer") # Tool 결과 받고 다시 LLM으로

# 컴파일
interviewer_app = workflow.compile()


# 6. 실행 함수 (Interface)
async def generate_interview_response(
    user_input: str, 
    history: List[BaseMessage] = [],
    initial_context: Optional[Dict[str, str]] = None
) -> str:
    """
    사용자의 입력과 대화 내역을 받아, 에이전트가 스스로 필요한 커리큘럼을 조회(Tool Call)하고 응답을 생성합니다.
    """
    
    # 기본 시스템 프롬프트
    base_prompt = """
        당신은 AI TechTree의 IT 기술 면접관입니다.

        [행동 지침]
        1. 사용자의 의도를 파악하고, `get_curriculum_context`를 사용하여 'Track'과 'Tier'를 확정하세요.
        2. 만약 해당 Tier에 'Option'(선택지)이 있다면, 반드시 사용자에게 하나를 선택하게 하세요.
        3. 세부적인 'Subject' 단위까지 내려가지 마세요. Tier(혹은 Option) 단위에서 범위를 정하는 것이 목표입니다.
        4. 범위가 확정되면 `recommend_interview_topic` 도구를 호출하여 추천을 확정하고 대화를 종료하세요.
        5. 항상 정중한 존댓말을 사용하세요.
        """

    messages = [SystemMessage(content=base_prompt)]

    # 웹 서비스 연동: 초기 컨텍스트가 주입된 경우
    if initial_context:
        # 1. 컨텍스트 내용을 로드 (Tool을 직접 사용하여 내용 확보)
        context_str = get_curriculum_context.invoke(input=initial_context)
        
        # 2. System 프롬프트에 컨텍스트 강제 주입 & 지시사항 추가
        context_injection = f"""
            [Current Interview Context]
            사용자가 웹 UI를 통해 이미 다음 주제를 선택했습니다. 즉시 `recommend_interview_topic` 도구를 호출하여 해당 주제를 추천하세요.

            {context_str}
            """
        messages.append(SystemMessage(content=context_injection))

    # 히스토리 및 사용자 입력 추가
    messages.extend(history)
    messages.append(HumanMessage(content=user_input))
    
    inputs = {"messages": messages}
    
    # 그래프 실행
    final_state = await interviewer_app.ainvoke(inputs)
    
    # 마지막 응답 추출 (ToolMessage 등이 섞여있을 수 있음)
    last_message = final_state["messages"][-1]
    
    return last_message.content




## 사용법 예시 
# from app.ai.agents.interviewer import generate_interview_response
# # 사용자가 "안녕하세요" 라고 했을 때
# ai_reply = await generate_interview_response("안녕하세요", history=[])
# print(ai_reply) # "반갑습니다. 혹시 주로 사용하는 언어가 무엇인가요?"