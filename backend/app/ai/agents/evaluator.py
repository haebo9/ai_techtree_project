from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.config import settings

# 1. 평가 결과 구조 정의 (JSON 응답용)
class EvaluationResult(BaseModel):
    score: int = Field(description="0 to 100 score based on accuracy and logic")
    is_passed: bool = Field(description="True if score >= 70, else False")
    reason: str = Field(description="Technical reason for the score")
    feedback: str = Field(description="Constructive feedback for the user")
    better_answer: Optional[str] = Field(description="A better implementation or explanation if applicable")

# 2. 모델 및 파서 설정
llm = ChatOpenAI(
    model="gpt-5-nano",  # 평가에는 정확도가 중요하므로 고성능 모델 권장 
    temperature=0,   # 일관된 평가를 위해 창의성(temperature)을 0으로 설정
    api_key=settings.OPENAI_API_KEY
)

parser = JsonOutputParser(pydantic_object=EvaluationResult)

# 3. 프롬프트 템플릿
EVALUATOR_SYSTEM_PROMPT = """
당신은 시니어 개발자 면접관입니다.
주어진 면접 질문과 지원자의 답변을 기술적으로 평가하세요.

[평가 기준]
1. 기술적 정확성
2. 논리적 설명
3. 구체적인 예시 사용 여부

다음의 JSON 형식으로만 응답하세요:
{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", EVALUATOR_SYSTEM_PROMPT),
    ("human", """
    [질문]: {question}
    [지원자 답변]: {user_answer}
    
    위 내용을 평가해주세요.
    """),
])

# 4. 체인 생성
# 프롬프트 -> LLM -> JSON 파서 (결과는 dict 형태)
evaluator_chain = prompt | llm | parser

# 5. 실행 함수
async def evaluate_answer(question: str, user_answer: str) -> dict:
    """
    질문과 답변을 받아 평가 결과(JSON Dict)를 반환합니다.
    Ref: EvaluationResult schema
    """
    result = await evaluator_chain.ainvoke({
        "question": question,
        "user_answer": user_answer,
        "format_instructions": parser.get_format_instructions()
    })
    
    return result
