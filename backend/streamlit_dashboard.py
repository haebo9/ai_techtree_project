import streamlit as st
import requests
import uuid
import json

# --- Configuration ---
API_URL = "http://localhost:8000/api/v2/chat/message"

st.set_page_config(page_title="AI TechTree Interviewer", page_icon="🤖", layout="wide")

# --- Session State Init ---
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]  # Demo용 임시 ID
if "messages" not in st.session_state:
    st.session_state.messages = []
if "topic" not in st.session_state:
    st.session_state.topic = "General"

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.write(f"User ID: `{st.session_state.user_id}`")
    
    # Track & Topic Selection
    track = st.selectbox("Track", ["Python", "JavaScript", "Java", "AI/ML"], index=0)
    topic = st.text_input("Detailed Topic", value=st.session_state.topic)
    level = st.select_slider("Level", options=["Basic", "Intermediate", "Advanced"], value="Intermediate")
    
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()

# --- Main Interface ---
st.title("🤖 AI TechTree: Tech Interviewer")
st.markdown("LangGraph Agent v1.1와 실시간으로 인터뷰를 진행하세요.")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if user_input := st.chat_input("답변을 입력하세요..."):
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Call Backend API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("생각 중..."):
                payload = {
                    "user_id": st.session_state.user_id,
                    "message": user_input,
                    "track": track,
                    "topic": topic,
                    "level": level
                }
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_text = data.get("response", "")
                    ui_action = data.get("ui_action")
                    
                    # Display Response
                    message_placeholder.markdown(ai_text)
                    full_response = ai_text
                    
                    # Store to history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    # Handle UI Actions (Simple Demo)
                    if ui_action and ui_action.get("type") == "SHOW_CONFETTI":
                        st.balloons()
                        st.toast("🎉 별을 획득했습니다!", icon="⭐")
                        
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
        except Exception as e:
            message_placeholder.error(f"Connection Failed: {e}")
