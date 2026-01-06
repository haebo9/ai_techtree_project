import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env (Try looking in parent dirs if needed, but assuming backend/.env based on execution path)
load_dotenv()
# If .env inside backend/.env
load_dotenv("backend/.env")

# -------------------------------------------------------------------------
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool

# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------
MCP_SERVER_URL = "http://localhost:8100"
st.set_page_config(page_title="AI TechTree MCP", page_icon="🌳", layout="wide")

st.title("🤖 AI TechTree MCP")
st.caption("독립된 MCP 서버(Port 8100)와 통신하며 스스로 도구를 선택하여 답변하는 에이전트입니다.")

# -------------------------------------------------------------------------
# Remote Tool Definitions (Client Side Proxies)
# -------------------------------------------------------------------------
# 에이전트가 "이 도구를 써야겠다"고 판단하면, 실제 실행은 MCP 서버로 요청을 보냅니다.

@tool
def client_get_ai_track(interests: list[str], experience_level: str) -> dict:
    """
    사용자의 관심사와 경력 수준을 기반으로 적합한 AI 커리큘럼 트랙을 추천합니다.
    Args:
        interests: 관심 분야 리스트 (예: ["데이터 분석", "웹 개발"])
        experience_level: 경력 수준 ("beginner", "intermediate", "expert")
    """
    payload = {"input": {"interests": interests, "experience_level": experience_level}}
    try:
        # MCP Server Call
        response = requests.post(f"{MCP_SERVER_URL}/get_ai_track/invoke", json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("output", {})
    except Exception as e:
        return {"error": str(e)}

@tool
def client_get_ai_path(track_name: str) -> dict:
    """
    특정 AI 트랙의 상세 커리큘럼(로드맵/공부 순서)을 조회합니다.
    Args:
        track_name: 트랙 이름 (예: "Track 1: AI Engineer")
    """
    payload = {"input": {"track_name": track_name}}
    try:
        response = requests.post(f"{MCP_SERVER_URL}/get_ai_path/invoke", json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("output", {})
    except Exception as e:
        return {"error": str(e)}

@tool
def client_get_ai_trend(keywords: list[str], category: str = "tech_news") -> list:
    """
    최신 AI 기술 트렌드나 뉴스를 웹에서 검색합니다.
    Args:
        keywords: 검색할 키워드 리스트
        category: 검색할 카테고리 ("tech_news", "engineering", "research", "k_blog")
    """
    payload = {"input": {"keywords": keywords, "category": category}}
    try:
        response = requests.post(f"{MCP_SERVER_URL}/get_ai_trend/invoke", json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("output", [])
    except Exception as e:
        return [{"error": str(e)}]

# Available Tools for the Agent
tools = [client_get_ai_track, client_get_ai_path, client_get_ai_trend]

# -------------------------------------------------------------------------
# Agent Setup
# -------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        AIMessage(content="안녕하세요! AI 커리큘럼 추천, 로드맵 조회, 최신 트렌드 검색을 도와드릴 수 있습니다. 무엇을 도와드릴까요?")
    ]

# Initialize LLM with Tools
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
llm_with_tools = llm.bind_tools(tools)

# -------------------------------------------------------------------------
# Chat Interface Logic
# -------------------------------------------------------------------------

# Display Chat History
for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)
    elif isinstance(msg, ToolMessage):
        with st.expander(f"🛠️ Tool Output: {msg.name}"):
            st.code(msg.content, language="json")

# Handle User Input
if prompt := st.chat_input("예: 데이터 분석에 관심 있는 초보자인데 공부 순서 알려줘"):
    # 1. User Message
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append(HumanMessage(content=prompt))

    # 2. Agent Reasoning loop
    with st.chat_message("assistant"):
        with st.spinner("AI가 생각 중입니다..."):
            # First LLM Call (Decide Tool)
            response = llm_with_tools.invoke(st.session_state["messages"])
            st.session_state["messages"].append(response)
            
            # Check if tool usage is requested
            if response.tool_calls:
                # Execute Tools
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_id = tool_call["id"]
                    
                    st.toast(f"🛠️ {tool_name} 도구를 실행합니다...", icon="🔧")
                    
                    # Find matching client tool
                    selected_tool = next((t for t in tools if t.name == tool_name), None)
                    if selected_tool:
                        tool_result = selected_tool.invoke(tool_args)
                        
                        # Show Tool Output (Intermediate)
                        with st.expander(f"⚡ Tool Execution: {tool_name}"):
                            st.json(tool_result)
                            
                        # Append Tool Message to History
                        tool_msg = ToolMessage(
                            tool_call_id=tool_id,
                            name=tool_name,
                            content=str(tool_result)  # Must be string
                        )
                        st.session_state["messages"].append(tool_msg)
                
                # Final LLM Call (Generate Answer based on Tool Output)
                # Use streaming for better UX
                stream_handler = st.chat_message("assistant").empty()
                final_content = ""
                
                for chunk in llm_with_tools.stream(st.session_state["messages"]):
                    if isinstance(chunk, AIMessage) and chunk.content:
                         final_content += chunk.content
                         stream_handler.markdown(final_content + "▌")
                
                stream_handler.markdown(final_content)
                st.session_state["messages"].append(AIMessage(content=final_content))
                
            else:
                # No tool needed, just chat
                st.chat_message("assistant").write(response.content)
