from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.core.config import settings

# 1. 모델 초기화
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.7,
    api_key=settings.OPENAI_API_KEY
)

# 2. 프롬프트 템플릿
INTERVIEWER_SYSTEM_PROMPT = """
당신은 IT 기술 면접관입니다.
사용자의 기술 수준을 파악하기 위해 핵심적인 질문을 던지세요.
한 번에 하나의 질문만 하세요.
존댓말을 사용하세요.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", INTERVIEWER_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"), # 이전 대화 내용
    ("human", "{input}"),                         # 사용자의 현재 답변
])

# 3. 체인 생성
interviewer_chain = prompt | llm

# 4. 단순 실행 함수 (No LangGraph)
async def generate_interview_response(user_input: str, history: List[BaseMessage] = []) -> str:
    """
    사용자의 입력과 대화 내역을 받아 면접관(AI)의 다음 대사를 반환합니다.
    """
    response = await interviewer_chain.ainvoke({
        "history": history, 
        "input": user_input
    })
    
    return response.content


## 사용법 예시 
# from app.ai.agents.interviewer import generate_interview_response
# # 사용자가 "안녕하세요" 라고 했을 때
# ai_reply = await generate_interview_response("안녕하세요", history=[])
# print(ai_reply) # "반갑습니다. 혹시 주로 사용하는 언어가 무엇인가요?"