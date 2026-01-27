from typing import List, Optional
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 1. 평가 및 리포트 데이터 구조 정의
class EvaluationResult(BaseModel):
    score: int = Field(description="0 to 100 score based on accuracy and logic")
    is_passed: bool = Field(description="True if score >= 70, else False")
    reason: str = Field(description="Technical reason for the score")
    feedback: str = Field(description="Constructive feedback for the user")
    better_answer: Optional[str] = Field(description="A better implementation or explanation if applicable")

class InterviewResult(BaseModel):
    total_score: int = Field(description="Overall technical capability score (0-100)")
    tier_level: str = Field(description="Estimated skill tier (e.g., Junior, Intermediate, Senior)")
    strengths: List[str] = Field(description="List of user's technical strengths found in interview")
    weaknesses: List[str] = Field(description="List of user's technical weaknesses found in interview")
    study_guide: str = Field(description="Recommendations for future learning")

# 2. 모델 및 파서 설정
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0,  # 분석 및 평가는 엄격하게 (Zero Temperature)
    api_key=api_key
)

eval_parser = PydanticOutputParser(pydantic_object=EvaluationResult)
report_parser = PydanticOutputParser(pydantic_object=InterviewResult)

# 3. 단일 답변 평가 프롬프트
EVALUATOR_SYSTEM_PROMPT = """
당신은 시니어 개발자 면접관입니다.
주어진 면접 질문과 지원자의 답변을 기술적으로 평가하세요.

[필수 평가 항목]
1. 기술적 정확성 (가장 중요)
2. 논리적 설명
3. 구체적인 예시 사용 여부

다음의 JSON 형식으로만 응답하세요:
{format_instructions}
"""

eval_prompt = ChatPromptTemplate.from_messages([
    ("system", EVALUATOR_SYSTEM_PROMPT),
    ("human", """
    [질문]: {question}
    [평가 기준]: {evaluation_criteria}
    [지원자 답변]: {user_answer}
    
    위 내용을 바탕으로 냉정하게 평가해주세요.
    """),
])

evaluator_chain = eval_prompt | llm | eval_parser

# 4. 전체 리포트 분석 프롬프트
REPORT_SYSTEM_PROMPT = """
당신은 AI TechTree의 최종 평가관입니다.
지원자의 전체 인터뷰 로그를 분석하여 종합적인 실력을 검증하세요.

[분석 포인트]
1. 답변의 일관성과 깊이를 보았을 때, 어느 정도의 Tier(Junior/Middle/Senior)에 해당하는지 판단하세요.
2. 잘 아는 분야(강점)와 모르는 분야(약점)를 명확히 구분하세요.
3. 점수는 후하게 주지 말고, 냉정하고 객관적으로 산출하세요.

다음의 JSON 형식으로만 응답하세요:
{format_instructions}
"""

report_prompt = ChatPromptTemplate.from_messages([
    ("system", REPORT_SYSTEM_PROMPT),
    ("human", """
    [전체 인터뷰 로그]
    {full_log}
    """),
])

report_chain = report_prompt | llm | report_parser


# 5. 실행 함수
async def evaluate_answer(
    question: str, 
    user_answer: str, 
    model_answer: str = "N/A", 
    evaluation_criteria: list = []
) -> dict:
    """
    단일 질문에 대한 평가를 수행합니다.
    """
    try:
        criteria_text = ", ".join(evaluation_criteria) if evaluation_criteria else "없음"
        
        result = await evaluator_chain.ainvoke({
            "question": question,
            "user_answer": user_answer,
            "evaluation_criteria": criteria_text,
            "format_instructions": eval_parser.get_format_instructions()
        })
        return result.model_dump()
        
    except Exception as e:
        print(f"⚠️ [Evaluator] Error evaluating answer: {e}")
        return {"score": 0, "is_passed": False, "feedback": "평가 중 오류가 발생했습니다."}

async def analyze_interview_result(conversation_history: List[str]) -> dict:
    """
    전체 대화 내용을 분석하여 종합 리포트 데이터를 생성합니다.
    """
    try:
        full_log = "\n".join(conversation_history)
        
        result = await report_chain.ainvoke({
            "full_log": full_log,
            "format_instructions": report_parser.get_format_instructions()
        })
        return result.model_dump()
        
    except Exception as e:
        print(f"⚠️ [Evaluator] Error analyzing report: {e}")
        return {
            "total_score": 0, 
            "tier_level": "Unknown", 
            "strengths": [], 
            "weaknesses": [], 
            "study_guide": "평가 데이터를 생성하지 못했습니다."
        }
