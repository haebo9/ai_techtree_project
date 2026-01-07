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
from app.mcp.tools import MCP_TOOLS

# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------
st.set_page_config(page_title="AI TechTree MCP", page_icon="🌳", layout="wide")

st.title("🤖 AI TechTree MCP")
st.caption("tools.py에 정의된 도구들을 직접 사용하여 답변하는 에이전트입니다.")

# -------------------------------------------------------------------------
# Tool Definitions
# -------------------------------------------------------------------------
# tools.py 에서 정의된 실제 도구들을 그대로 사용합니다.
tools = MCP_TOOLS

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
            # Agent Loop (supports multiple tool calls)
            while True:
                # Decide Tool or Answer
                response = llm_with_tools.invoke(st.session_state["messages"])
                
                # Check if tool usage is requested
                if response.tool_calls:
                    st.session_state["messages"].append(response) # Add the AIMessage with tool calls
                    
                    # Execute Tools
                    for tool_call in response.tool_calls:
                        tool_name = tool_call["name"]
                        tool_args = tool_call["args"]
                        tool_id = tool_call["id"]
                        
                        st.toast(f"🛠️ {tool_name} 도구를 실행합니다...", icon="🔧")
                        
                        # Find matching tool
                        selected_tool = next((t for t in tools if t.name == tool_name), None)
                        if selected_tool:
                            try:
                                tool_result = selected_tool.invoke(tool_args)
                            except Exception as e:
                                tool_result = {"error": str(e)}
                            
                            # Show Tool Output (Intermediate)
                            with st.expander(f"⚡ Tool Execution: {tool_name}"):
                                st.json(tool_result)
                                
                            # Append Tool Message to History
                            tool_msg = ToolMessage(
                                tool_call_id=tool_id,
                                name=tool_name,
                                content=str(tool_result)
                            )
                            st.session_state["messages"].append(tool_msg)
                    
                    # Loop continues to next LLM call with updated history
                    continue
                    
                else:
                    # Final Answer (Content)
                    # Use streaming for better UX
                    stream_handler = st.chat_message("assistant").empty()
                    final_content = ""
                    
                    # We need to stream the content of THIS response, but since we already invoked it above without streaming to check tool_calls,
                    # simply outputting response.content is enough. 
                    # BUT to support streaming UX, we can re-stream or just print. 
                    # For simplicity and correctness with the loop structure, we just print the content we already got.
                    
                    # (Optional) If you want true streaming for the final answer, you'd need to use .stream() in the loop 
                    # and detect tool_calls from chunks, which is more complex.
                    # For now, let's just write the content we have.
                    if response.content:
                        st.write(response.content)
                        st.session_state["messages"].append(AIMessage(content=response.content))
                    else:
                        # Sometimes LLM returns empty content with no tool calls if it's confused, but rare.
                        pass
                    
                    break

