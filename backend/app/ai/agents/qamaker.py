from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from app.core.config import settings

# 1. 생성될 문제의 구조 정의 (Pydantic)
class GeneratedQuestion(BaseModel):
    skill: str = Field(description="Target skill name (e.g., Python)")
    topic: str = Field(description="Specific topic within the skill (e.g., Generator)")
    level: str = Field(description="Difficulty level (e.g., Basic, Intermediate, Advanced)")
    question_text: str = Field(description="The interview question text")
    model_answer: str = Field(description="A comprehensive model answer")
    evaluation_criteria: List[str] = Field(description="List of key points to check in user's answer")

# 2. 모델 설정
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.5, # 다양한 문제를 위해 약간의 창의성 허용
    api_key=settings.OPENAI_API_KEY
)

parser = JsonOutputParser(pydantic_object=GeneratedQuestion)

# 3. 프롬프트 정의
GENERATOR_SYSTEM_PROMPT = """
당신은 IT 기술 면접 문제 출제 위원입니다.
주어진 주제와 난이도에 맞춰 고품질의 기술 면접 문제를 1개 생성하세요.

[요구사항]
1. 질문은 실무적이고 깊이 있는 내용을 다뤄야 합니다.
2. 모범 답안은 핵심 개념과 예시를 포함하여 명확하게 작성하세요.
3. 평가 기준은 채점자가 답변을 보고 바로 판단할 수 있는 키워드 위주로 3~5개 작성하세요.

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
    """),
])

# 4. 체인 생성
generator_chain = prompt | llm | parser

# 5. 실행 함수
async def generate_single_question(skill: str, topic: str, level: str = "Intermediate") -> dict:
    """
    조건에 맞는 면접 문제를 1개 생성하여 반환합니다.
    Ref: GeneratedQuestion schema
    """
    result = await generator_chain.ainvoke({
        "skill": skill,
        "topic": topic,
        "level": level,
        "format_instructions": parser.get_format_instructions()
    })
    
    return result

# 6. DB 저장 및 일괄 생성 로직
from motor.motor_asyncio import AsyncIOMotorClient
from app.ai.source.topics import TARGET_TOPICS

LEVEL_MAP = {"Basic": 1, "Intermediate": 2, "Advanced": 3}

async def save_question_to_db(question_data: dict):
    """생성된 질문 데이터를 DB에 저장"""
    if not settings.MONGODB_URL:
        print("❌ MONGODB_URL is missing.")
        return

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client.get_database("ai_techtree")
    
    # DB 스키마에 맞게 변환
    db_document = {
        "skill_slug": question_data["skill"].lower(),
        "level": LEVEL_MAP.get(question_data["level"], 2),
        "topic": question_data["topic"],
        "question_text": question_data["question_text"],
        "model_answer": question_data["model_answer"],
        "evaluation_criteria": question_data["evaluation_criteria"]
    }
    
    # 중복 방지를 위해 topic과 skill_slug로 확인 (Optional)
    # 여기서는 단순 Insert
    await db.questions.insert_one(db_document)
    print(f"✅ Saved: {question_data['topic']} ({question_data['skill']})")
    
    client.close()

async def generate_and_save_questions_bulk():
    """TARGET_TOPICS에 정의된 모든 주제에 대해 문제를 생성하고 DB에 저장"""
    print("🏭 Bulk Question Generation Started...")
    
    for skill, topics in TARGET_TOPICS.items():
        print(f"\n📂 Skill: {skill}")
        for topic in topics:
            try:
                # 1. 문제 생성 (AI)
                q_data = await generate_single_question(skill, topic)
                
                # 2. DB 저장
                await save_question_to_db(q_data)
                
            except Exception as e:
                print(f"   ❌ Failed {topic}: {e}")
                
    print("\n✨ Bulk Generation Completed.")
