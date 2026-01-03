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
# 3. 프롬프트 템플릿
EVALUATOR_SYSTEM_PROMPT = """
당신은 시니어 개발자 면접관입니다.
주어진 면접 질문과 지원자의 답변을 기술적으로 평가하세요.

[필수 평가 항목]
1. 기술적 정확성
2. 논리적 설명
3. 구체적인 예시 사용 여부

참고할 모범 답안과 평가 기준이 있다면 이를 적극 반영하여 채점하세요.

다음의 JSON 형식으로만 응답하세요:
{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", EVALUATOR_SYSTEM_PROMPT),
    ("human", """
    [질문]: {question}
    
    [모범 답안 (참고용)]:
    {model_answer}
    
    [평가 기준 (키워드)]:
    {evaluation_criteria}

    [지원자 답변]: {user_answer}
    
    위 내용을 바탕으로 냉정하게 평가해주세요.
    """),
])

# 4. 체인 생성
# 프롬프트 -> LLM -> JSON 파서 (결과는 dict 형태)
evaluator_chain = prompt | llm | parser

# 5. 실행 함수
async def evaluate_answer(question: str, user_answer: str, model_answer: str = "없음", evaluation_criteria: list = []) -> dict:
    """
    질문과 답변을 받아 평가 결과(JSON Dict)를 반환합니다.
    Ref: EvaluationResult schema
    """
    
    criteria_text = ", ".join(evaluation_criteria) if evaluation_criteria else "없음"
    
    result = await evaluator_chain.ainvoke({
        "question": question,
        "user_answer": user_answer,
        "model_answer": model_answer,
        "evaluation_criteria": criteria_text,
        "format_instructions": parser.get_format_instructions()
    })
    
    return result
