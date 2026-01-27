from typing import List
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 1. 생성될 문제의 구조 정의 (Pydantic)
class GeneratedQuestion(BaseModel):
    skill: str = Field(description="Target skill name (e.g., Python)")
    topic: str = Field(description="Specific topic within the skill (e.g., Generator)")
    level: str = Field(description="Difficulty level (e.g., Basic, Intermediate, Advanced)")
    question_text: str = Field(description="The interview question text")
    model_answer: str = Field(description="A comprehensive model answer")
    evaluation_criteria: List[str] = Field(description="List of 3-5 key points to check in user's answer")

class QuestionList(BaseModel):
    questions: List[GeneratedQuestion] = Field(description="List of generated interview questions")

# 2. 모델 설정
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o",  # Using gpt-4o as 'gpt-5-mini' might not be available or valid alias in this context yet
    temperature=0.7,     # 다양한 문제를 위해 창의성 허용
    api_key=api_key
)

parser = PydanticOutputParser(pydantic_object=QuestionList)

# 3. 프롬프트 정의
GENERATOR_SYSTEM_PROMPT = """
당신은 IT 기술 면접 문제 출제 위원입니다.
주어진 주제와 난이도에 맞춰 고품질의 기술 면접 문제를 {count}개 생성하세요.

[요구사항]
1. 각 문제는 서로 다른 세부 개념을 다루거나, 다른 측면(저장소, 성능, 보안 등)을 물어봐야 합니다. (중복 금지)
2. 질문은 실무적이고 깊이 있는 내용을 다뤄야 합니다.
3. 모범 답안은 핵심 개념과 예시를 포함하여 명확하게 작성하세요.
4. 평가 기준은 채점자가 답변을 보고 바로 판단할 수 있는 키워드 위주로 3~5개 작성하세요.

다음의 JSON 형식으로만 응답하세요:
{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", GENERATOR_SYSTEM_PROMPT),
    ("human", """
    [출제 요청]
    - 기술 스택: {skill}
    - 세부 주제: {topic}
    - 난이도: {level}
    - 문제 수: {count}개
    """),
])

# 4. 체인 생성
generator_chain = prompt | llm | parser

# 5. 실행 함수
async def generate_questions(skill: str, topic: str, level: str = "Intermediate", count: int = 1) -> List[dict]:
    """
    조건에 맞는 면접 문제를 지정된 수만큼 생성하여 리스트로 반환합니다.
    """
    try:
        result = await generator_chain.ainvoke({
            "skill": skill,
            "topic": topic,
            "level": level,
            "count": count,
            "format_instructions": parser.get_format_instructions()
        })
        
        # Pydantic 모델을 dict 리스트로 변환
        return [q.model_dump() for q in result.questions]
        
    except Exception as e:
        print(f"⚠️ [QAMaker] Error generating questions: {e}")
        # 에러 발생 시 빈 리스트 반환 (Main Agent에서 처리)
        return []
