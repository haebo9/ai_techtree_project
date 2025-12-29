from typing import Dict, List

# 커리큘럼 소스 데이터
# 추후에는 DB에서 관리하거나, 외부 API에서 가져오는 형태로 확장 가능
TARGET_TOPICS: Dict[str, List[str]] = {
    "python": [
        "GIL (Global Interpreter Lock)의 개념과 영향",
        "Decorator의 동작 원리와 활용",
        "Generator와 Iterator의 차이",
        "Memory Management (Garbage Collection & Reference Counting)",
        "Asyncio vs Threading vs Multiprocessing",
        "Context Manager (with statement)",
        "Metaclass의 개념과 사용 시점",
        "Shallow Copy vs Deep Copy",
        "Closure와 Scope (LEGB Rule)",
        "Dunder(Magic) Methods 활용"
    ],
    "fastapi": [
        "Dependency Injection의 개념과 장점",
        "Pydantic을 이용한 데이터 유효성 검사",
        "FastAPI의 비동기 처리(Async/Await) 아키텍처",
        "Middleware 구현과 활용",
        "APIRouter를 이용한 라우팅 구조화",
        "OAuth2 및 JWT 인증 구현",
        "Background Tasks 활용",
        "Starlette과의 관계"
    ],
    "java": [
        "JVM 구조 (Heap, Stack, Method Area)",
        "Garbage Collection 알고리즘 (Serial, Parallel, G1, ZGC)",
        "Java Memory Model (JMM)",
        "Thread Pool과 ExecutorService",
        "Spring DI(Dependency Injection)와 IoC Container",
        "Spring Boot Auto Configuration 원리",
        "JPA(Hibernate) N+1 문제와 해결책",
        "Optional 활용법",
        "Stream API와 Lambda Expression"
    ]
}
