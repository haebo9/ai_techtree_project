from typing import Dict, Any

# AI Tech Tree Curriculum Data
# Based on track.md v1.2
# 구조: Track -> Tier -> (Option) -> Subject -> Concepts (List[str])

AI_TECH_TREE: Dict[str, Any] = {
    "Track 0: The Origin": {
        "description": "공통 필수 기반 (Python, DevOps, Math)",
        "tiers": {
           "Tier 1: Core Python Mastery": {
                "Python Syntax & Types": [
                    "변수 할당과 명명 규칙 (Snake Case)",
                    "기본 자료형 (int, float, str, bool)의 특징",
                    "문자열 슬라이싱(Slicing)과 인덱싱 기초",
                    "조건문 (if-elif-else)과 반복문 (for, while) 사용법",
                    "함수 정의 (def)와 return문의 역할",
                    "Module import 방법 (import, from-import)",
                    "변수, 자료형, 기초 문법 및 연산자 우선순위",
                    "Mutable(List, Dict) vs Immutable(String, Tuple) 객체의 차이와 메모리 구조",
                    "GIL (Global Interpreter Lock)의 개념과 멀티스레딩 성능에 미치는 영향",
                    "Shallow Copy(얕은 복사) vs Deep Copy(깊은 복사)의 동작 차이",
                    "Type Hinting (Generic, Union, Optional, Callable) 활용과 Static Analysis (mypy)",
                    "String Formatting Evolution (%-formatting vs .format() vs f-string)",
                    "Module과 Package의 차이, __init__.py의 역할"
                ],
                "Data Structure Core": [
                    "List의 주요 메서드 (append, extend, pop) 사용법",
                    "Dictionary의 Key-Value 구조 이해 및 기본 조작",
                    "Set의 중복 제거 특성과 교집합/합집합 연산",
                    "Tuple의 불변성(Immutability)과 사용 이유",
                    "List, Dict, Set의 Time Complexity (Big-O) 분석 (Insert, Delete, Search)",
                    "Hash Map의 동작 원리와 Hash Collision 해결 방식 (Open Addressing vs Chaining)",
                    "NamedTuple vs Dataclass: 불변성과 메모리 효율성 비교",
                    "Heapq 모듈을 이용한 Priority Queue 구현 및 활용",
                    "Deque(Double-ended Queue)의 활용과 List와의 성능 차이"
                ],
                "OOP & Functional": [
                    "Class 정의와 Instance 생성 방법",
                    "self 키워드의 의미와 역할",
                    "Lambda 함수(익명 함수)의 기본 문법과 활용",
                    "List Comprehension의 기본 문법과 장점",
                    "Class 상속(Inheritance), 다형성(Polymorphism), 캡슐화(Encapsulation)",
                    "Decorator의 동작 원리 (@func syntax vs func = deco(func))와 활용 (Logging, Timing)",
                    "Generator와 Iterator의 차이, `yield`와 `yield from`의 동작",
                    "Closure와 Scope (Global, Local, Enclosing - LEGB Rule)",
                    "Metaclass의 개념과 Singleton 패턴 구현 시 활용",
                    "Dunder(Magic) Methods 활용 (__init__, __str__, __repr__, __call__, __getitem__)",
                    "Context Manager (__enter__, __exit__)와 `with` statement의 안전한 자원 관리",
                    "Abstract Base Class (abc 모듈)를 이용한 인터페이스 설계",
                    "Method Resolution Order (MRO)와 Diamond Inheritance 문제"
                ]
           },
           "Tier 2: Core DevOps Foundations": {
                "Linux CLI": [
                    "디렉토리 이동 (cd)과 목록 확인 (ls) 명령어",
                    "파일 생성 (touch), 복사 (cp), 이동 (mv), 삭제 (rm) 기초",
                    "파일 내용 확인 (cat, head, tail)",
                    "현재 경로 확인 (pwd)과 화면 지우기 (clear)",
                    "파일 시스템(File System) 구조와 권한 관리 (chmod, chown, chgrp)",
                    "표준 입출력 (stdin, stdout, stderr)과 Pipe(|), Redirection(>, >>)",
                    "프로세스 관리: ps, top, htop, kill, nohup, background(&) 실행",
                    "SSH Key 생성 및 원격 서버 접속 설정 (authorized_keys)",
                    "Package Manager (apt, yum, brew) 동작 원리",
                    "Soft Link vs Hard Link의 차이 (Inode 개념)"
                ],
                "Git Version Control": [
                    "Git 저장소 초기화 (init)와 상태 확인 (status)",
                    "파일 스테이징 (add)과 커밋 (commit) 기초",
                    "원격 저장소 연결 (remote add)과 푸시 (push)",
                    "브랜치 생성 (branch)과 이동 (checkout/switch)",
                    "Git의 3가지 영역 (Working Directory, Staging Area, Repository)",
                    "Commit Convention (feat, fix, refactor 등)과 메시지 작성법",
                    "Git Branching Strategies (Git Flow, GitHub Flow, Trunk-based)",
                    "Merge vs Rebase: 히스토리 관리 차이점과 사용 시기",
                    "Reset (Soft, Mixed, Hard)의 차이와 되돌리기 전략",
                    "Cherry-pick을 이용한 특정 커밋 가져오기",
                    ".gitignore 패턴 작성법과 관리"
                ]
           },
           "Tier 3: Core Math & Logic": {
                "Linear Algebra & Statistics": [
                    "평균(Mean)과 중앙값(Median)의 차이",
                    "벡터(Vector)와 행렬(Matrix)의 기본 생김새",
                    "기초 확률 (동전 던지기, 주사위 확률)",
                    "로그(Log)와 지수(Exponential)의 기본 그래프 형태",
                    "Scalar, Vector, Matrix, Tensor의 개념과 차이",
                    "Matrix Multiplication (Dot Product)의 기하학적 의미",
                    "Eigenvalue와 Eigenvector의 의미와 PCA(Principal Component Analysis) 활용",
                    "확률 변수(Random Variable), 확률 분포(Normal, Uniform, Bernoulli 등)",
                    "Bayes' Theorem (베이즈 정리)와 조건부 확률",
                    "Variance, Standard Deviation의 의미",
                    "Correlation vs Causation (상관관계와 인과관계)"
                ]
           }
        }
    },
    "Track 1: AI Engineer": {
        "description": "시스템 구축가 (FastAPI, Docker, GPU Serving)",
        "tiers": {
            "Tier 1: Core System Foundation": {
                "FastAPI Essentials": [
                    "GET, POST 요청 메서드의 차이",
                    "Path Parameter(`/items/{id}`) 사용법",
                    "Query Parameter(`?skip=0`) 사용법",
                    "JSON 요청과 응답 구조 이해",
                    "Path Parameter vs Query Parameter vs Request Body의 차이",
                    "Pydantic BaseModel을 이용한 엄격한 데이터 유효성 검사 및 Serialization",
                    "FastAPI의 Dependency Injection 시스템 (Depends, Security, Singleton)",
                    "APIRouter를 이용한 대규모 애플리케이션 라우팅 및 모듈화 전략",
                    "Middleware의 동작 순서와 Custom Middleware 구현 (CORS, Logging, Gzip)",
                    "Exception Handler 구현과 Global Error Handling",
                    "Lifespan Events (Startup/Shutdown) 처리"
                ],
                "Dependency Injection": [
                    "함수 인자로 객체 전달하기 (DI의 기초)",
                    "Global 변수 사용의 문제점",
                    "Inversion of Control (IoC)와 DI의 개념",
                    "DB Session 관리 (SQLAlchemy SessionLocal)와 Transaction Scope",
                    "Unit Test 작성을 위한 Dependency Overrides 활용",
                    "Singleton Pattern vs Request Scoped Dependency"
                ],
                "Async Architecture": [
                    "동기(Sync) 처리의 개념 (순차 실행)",
                    "비동기(Async) 함수의 정의 (async def)",
                    "await 키워드의 기본 역할",
                    "Sync(동기) vs Async(비동기) vs Parallel(병렬)의 개념적 차이",
                    "Python `async`/`await` 문법과 Event Loop의 동작 원리",
                    "Blocking I/O 호출이 Event Loop에 미치는 악영향과 해결책 (run_in_executor)",
                    "Asyncio Task와 Future 객체의 이해",
                    "Coroutine Concurrency: `asyncio.gather` vs `asyncio.wait`",
                    "ASGI (Asynchronous Server Gateway Interface) vs WSGI 차이"
                ],
                "Docker Basics": [
                    "Docker 이미지와 컨테이너의 개념 차이",
                    "Dockerfile 기본 명령어 (FROM, RUN, CMD)",
                    "Docker 컨테이너 실행 (run)과 중지 (stop)",
                    "포트 포워딩 (-p 옵션)의 이해",
                    "Docker Image Layer Cache 원리와 효율적인 Dockerfile 작성 (Multi-stage Build)",
                    "Container vs VM (Virtual Machine) 구조적 차이",
                    "ENTRYPOINT vs CMD의 차이점",
                    "Volume Mount (Bind Mount, Named Volume)를 이용한 데이터 영속성",
                    "Docker Compose를 이용한 다중 컨테이너 오케스트레이션",
                    "Docker Network (Bridge, Host, Overlay) 모드 이해"
                ]
            },
            "Tier 2: Branching Point": {
                "Option 1: Serving Specialist (추론 최적화)": {
                    "Model Serialization": [
                        "모델 파일 저장과 불러오기 기초",
                        "Pickle 모듈 기본 사용법",
                        "Pickle의 보안 위험성과 Safetensors의 장점",
                        "ONNX (Open Neural Network Exchange) 포맷의 구조와 변환 과정",
                        "PyTorch `torch.save` vs `torch.jit.save` (TorchScript)"
                    ],
                    "Inference Optimization": [
                        "모델 경량화의 필요성 이해",
                        "Python 코드 실행 시간 측정 방법",
                        "TensorRT Engine 빌드 과정과 Layer Fusion",
                        "Quantization Types (PTQ vs QAT, INT8 vs FP16 vs BF16)",
                        "Pruning (가지치기) 기법과 희소성(Sparsity) 활용"
                    ],
                    "Serving Frameworks": [
                        "REST API로 모델 결과 반환하기",
                        "Batch Processing(일괄 처리)의 개념",
                        "Triton Inference Server 아키텍처 (Model Repository, Backend)",
                        "Dynamic Batching의 원리와 Latency/Throughput 트레이드오프",
                        "gRPC vs HTTP/REST 프로토콜 성능 비교"
                    ]
                },
                "Option 2: App Architect (서비스 아키텍처)": {
                    "Database Design": [
                        "Table, Row, Column의 개념",
                        "Primary Key(PK)와 Foreign Key(FK)의 역할",
                        "RDBMS Indexing (B-Tree) 원리와 Composite Index 전략",
                        "N+1 Problem의 원인과 해결 (Eager Loading vs Lazy Loading)",
                        "DB Replication (Master-Slave) vs Sharding",
                        "ACID 트랜잭션 속성과 Isolation Level"
                    ],
                    "Caching Strategy": [
                        "캐시(Cache)의 기본 개념과 필요성",
                        "Key-Value 저장소의 특징",
                        "Cache-Aside(Lazy Loading) vs Write-Through 패턴",
                        "Redis Eviction Policies (LRU, LFU, TTL)",
                        "Cache Stampede(Thundering Herd) 문제와 해결책"
                    ],
                    "Message Queue": [
                        "Producer와 Consumer의 개념",
                        "비동기 작업(백그라운드 처리)의 필요성 예시",
                        "Message Broker Pattern (Pub/Sub vs Point-to-Point)",
                        "Celery와 Redis/RabbitMQ 연동 아키텍처",
                        "Idempotency(멱등성) 보장과 At-least-once vs Exactly-once 전달",
                        "Dead Letter Queue (DLQ) 활용 전략"
                    ]
                }
            },
            "Tier 3: Core Infrastructure Mastery": {
                "Container Orchestration": [
                    "여러 컨테이너를 관리해야 하는 이유",
                    "Kubernetes의 역할 (오케스트레이션) 개요",
                    "Kubernetes 기본 Object: Pod, ReplicaSet, Deployment, Service",
                    "Cluster Networking: Service Discovery, Ingress Controller",
                    "ConfigMap과 Secret을 이용한 설정 관리",
                    "Pod Lifecycle과 Liveness/Readiness Probe 설정"
                ],
                "GPU Scaling": [
                    "GPU가 CPU보다 딥러닝에 유리한 이유",
                    "NVIDIA Driver와 CUDA의 개념",
                    "NVIDIA Device Plugin for Kubernetes 동작 원리",
                    "Kubernetes Resource Requests/Limits (CPU vs Memory vs GPU)",
                    "HPA (Horizontal Pod Autoscaler) 및 Cluster Autoscaler 설정",
                    "Multi-Instance GPU (MIG) 기술 이해"
                ]
            }
        }
    },
    "Track 2: AI Modeler / Researcher": {
        "description": "알고리즘 술사 (Deep Learning, Vision, NLP)",
        "tiers": {
            "Tier 1: Core Deep Learning Engine": {
                "Tensor Operations": [
                    "텐서(Tensor)란 무엇인가? (다차원 배열)",
                    "텐서의 크기(Shape) 확인하기",
                    "Tensor Shape 조작 (view vs reshape vs permute vs transpose)",
                    "Broadcasting Rules: 차원이 다른 텐서 간 연산 원리",
                    "Contiguous Tensor 개념과 메모리 레이아웃",
                    "Vector/Matrix/Tensor Multiplication (@, matmul, bmm)"
                ],
                "AutoGrad & Backprop": [
                    "미분(Derivative)과 기울기(Gradient)의 의미",
                    "Loss Function(손실 함수)의 역할",
                    "Computational Graph (Dynamic vs Static)",
                    "Chain Rule을 이용한 Gradient 계산 과정",
                    "requires_grad 속성과 `.detach()` `with torch.no_grad()`의 차이",
                    "Gradient Accumulation 구현 원리"
                ],
                "Training Loop": [
                    "학습 데이터(Training Set)와 테스트 데이터(Test Set) 분리 이유",
                    "Epoch와 Batch의 개념",
                    "Custom Dataset (`__len__`, `__getitem__`) 구현",
                    "DataLoader의 `num_workers`, `collate_fn`, `pin_memory` 옵션 최적화",
                    "Training Step vs Validation Step vs Test Step 구조",
                    "Epoch vs Batch Size vs Iteration 용어 정의"
                ]
            },
            "Tier 2: Branching Point": {
                "Option 1: Vision Sage (시각 지능)": {
                    "CNN Backbones": [
                        "이미지가 픽셀(Pixel)로 표현되는 방식",
                        "RGB 채널의 이해",
                        "Convolution Operation: Kernel/Filter, Stride, Padding",
                        "Pooling Layers (Max vs Average)와 Downsampling의 의미",
                        "ResNet의 Residual Block과 Gradient Vanishing 해결",
                        "EfficientNet의 Compound Scaling Method"
                    ],
                    "Object Detection": [
                        "Classification과 Detection의 차이",
                        "Bounding Box (x, y, w, h) 표현 방식",
                        "IoU (Intersection over Union) 계산",
                        "NMS (Non-Maximum Suppression) 알고리즘 동작 원리",
                        "One-stage (YOLO) vs Two-stage (Faster R-CNN) Detector 차이",
                        "Anchor Box의 개념과 역할"
                    ],
                    "Generative Vision": [
                        "이미지 생성 모델의 개념",
                        "노이즈(Noise)에서 이미지를 만드는 기본 원리",
                        "Diffusion Model의 Forward(Noise adding) / Reverse(Denoising) process",
                        "Latent Diffusion Model (LDM) 구조와 VAE의 역할",
                        "U-Net Architecture와 Cross-Attention (Text Conditioning)"
                    ]
                },
                "Option 2: Language Sage (언어 지능)": {
                    "Transformer Arch": [
                        "단어를 숫자로 바꾸는 이유 (임베딩)",
                        "RNN과 LSTM의 한계점",
                        "Self-Attention Mechanism (Query, Key, Value) 수식 이해",
                        "Multi-Head Attention의 장점과 동작 방식",
                        "Positional Encoding (Sinusoidal vs Rotary/RoPE)",
                        "Encoder-only (BERT), Decoder-only (GPT), Encoder-Decoder (T5) 비교"
                    ],
                    "Tokenization": [
                        "문장을 공백으로 나누기 vs 형태소 분석",
                        "Subword Tokenization (BPE, WordPiece, Unigram) 알고리즘",
                        "Special Tokens ([CLS], [SEP], [PAD], [EOS])의 역할",
                        "Vocabulary Size가 모델 성능과 메모리에 미치는 영향"
                    ],
                    "PEFT": [
                        "파인튜닝(Fine-tuning)의 개념",
                        "모델의 모든 파라미터를 학습할 때의 문제점",
                        "LoRA (Low-Rank Adaptation)의 행렬 분해 원리",
                        "QLoRA: 4-bit Quantization + LoRA",
                        "Prompt Tuning vs Prefix Tuning vs Adapter Layers"
                    ]
                }
            },
            "Tier 3: Core Advanced Training": {
                "Distributed Training": [
                    "GPU 하나의 메모리 부족 문제",
                    "Data Parallel (DP) vs Distributed Data Parallel (DDP) 차이",
                    "Parameter Server vs All-Reduce 알고리즘",
                    "FSDP (Fully Sharded Data Parallel)의 메모리 절감 전략 (Zero Redundancy)"
                ],
                "Memory Optimization": [
                    "Out of Memory (OOM) 에러의 의미",
                    "Mixed Precision Training (FP16/BF16)과 Loss Scaling",
                    "Gradient Checkpointing (Activation Checkpointing)을 통한 메모리 절약",
                    "CPU Offloading 기술"
                ]
            }
        }
    },
    "Track 3: LLM Application Engineer": {
        "description": "에이전트 소환사 (Prompting, RAG, Agent)",
        "tiers": {
            "Tier 1: Core Context Integration": {
                "Prompting Basics": [
                    "프롬프트(Prompt)란 무엇인가?",
                    "LLM에게 역할 부여하기 (Role Playing)",
                    "Zero-shot vs Few-shot Learning의 차이와 In-context Learning",
                    "System Prompt의 역할과 중요성",
                    "Prompt Injection 공격 유형과 방어 전략",
                    "LLM Hyperparameters: Temperature, Top-p(Nucleus), Top-k의 의미"
                ],
                "Chain of Thought": [
                    "단계별로 생각하라고 지시하기",
                    "Standard Prompting vs Chain of Thought (CoT) 성능 차이 원인",
                    "Zero-shot CoT ('Let's think step by step')",
                    "Tree of Thoughts (ToT)와 추론 탐색 과정"
                ],
                "Embeddings": [
                    "텍스트 유사도(Similarity)의 개념",
                    "단어의 의미를 벡터 공간에 표현하기",
                    "Dense Vector vs Sparse Vector (Keyword) 차이",
                    "Cosine Similarity vs Euclidean Distance vs Dot Product",
                    "Embedding Model (OpenAI ada-002, BGE, E5) 선정 기준"
                ],
                "Vector DB": [
                    "벡터 데이터베이스의 필요성",
                    "HNSW (Hierarchical Navigable Small World) 알고리즘 개요",
                    "Vector Indexing 후 Search Latency와 Recall의 트레이드오프",
                    "Metadata Filtering의 동작 방식 (Pre-filtering vs Post-filtering)"
                ]
            },
            "Tier 2: Branching Point": {
                "Option 1: Agentic Workflow (자율 에이전트)": {
                    "ReAct Pattern": [
                        "LLM이 행동(Action)을 결정하는 방식",
                        "Thought-Action-Observation Loop 구조 이해",
                        "Reasoning Traces가 모델 성능에 미치는 영향"
                    ],
                    "Tool Use": [
                        "LLM이 계산기나 검색을 사용하는 이유",
                        "OpenAI Function Calling API 구조 및 JSON Schema 정의",
                        "Tool 실행 결과 파싱 및 에러 핸들링 전략",
                        "Parallel Function Calling 처리"
                    ],
                    "Multi-Agent": [
                        "한 명의 에이전트 vs 여러 명의 에이전트",
                        "Single Agent vs Multi-Agent Systems (MAS) 장단점",
                        "Orchestrator-Workers 패턴 vs Peer-to-Peer 패턴",
                        "LangGraph의 StateGraph, Node, Edge 개념"
                    ]
                },
                "Option 2: Reliability & Eval (신뢰성 및 평가)": {
                    "Advanced RAG": [
                        "RAG (Retrieval-Augmented Generation) 기본 개념",
                        "Hybrid Search (Keyword + Semantic) 구현과 Weighting",
                        "Reranking Model (Cross-Encoder)을 이용한 정확도 향상",
                        "HyDE (Hypothetical Document Embeddings) 기법",
                        "Multi-Query / Query Expansion 전략"
                    ],
                    "Chunking Strategy": [
                        "문서를 나누는 이유 (Token Limit)",
                        "Fixed-size Chunking vs Semantic Chunking",
                        "Recursive Character Text Splitter 동작 원리",
                        "Small-to-Big Retrieval (Parent Document Retriever)"
                    ],
                    "LLM Evaluation": [
                        "LLM 답변을 평가하는 어려움",
                        "Reference-based (BLEU, ROUGE) vs Model-based (LLM-as-a-Judge) 평가",
                        "RAGAS Framework의 주요 지표 (Faithfulness, Answer Relevance, Context Recall)",
                        "Hallucination 유형 (Factuality vs Faithfulness)과 탐지"
                    ]
                }
            },
            "Tier 3: Core Production Excellence": {
                "Prompt Management": [
                    "프롬프트 관리의 중요성",
                    "Prompt Versioning 및 변경 이력 관리",
                    "A/B Testing 설계: 프롬프트 변형에 따른 사용자 반응 측정"
                ],
                "Feedback Loop": [
                    "사용자 피드백 수집 방법",
                    "Implicit Feedback (체류 시간, 재요청) vs Explicit Feedback (좋아요/싫어요)",
                    "DPO (Direct Preference Optimization)를 위한 데이터셋 구축"
                ]
            }
        }
    },
    "Track 4: Data Engineer": {
        "description": "데이터 대장장이 (SQL, Big Data, Streaming)",
        "tiers": {
            "Tier 1: Core Data Flow": {
                "SQL Mastery": [
                    "SELECT, FROM, WHERE 기본 문법",
                    "GROUP BY와 집계 함수 (COUNT, SUM, AVG)",
                    "JOIN Types (Inner, Left, Right, Full, Cross)와 성능 이슈",
                    "Window Functions (RANK, DENSE_RANK, ROW_NUMBER, LAG, LEAD) 활용",
                    "Common Table Expressions (CTE)와 Recursive CTE",
                    "Subquery vs Join 성능 비교"
                ],
                "Data Modeling": [
                    "데이터 중복을 피해야 하는 이유 (정규화 기초)",
                    "OLTP vs OLAP 시스템 차이",
                    "Star Schema vs Snowflake Schema 장단점 비교",
                    "Fact Table vs Dimension Table의 역할",
                    "SCD (Slowly Changing Dimensions) Type 1, 2, 3 처리 전략"
                ],
                "Workflow Orchestration": [
                    "크론탭(Crontab)과 스케줄링",
                    "Airflow DAG 구조 (Task, Operator, Sensor) 이해",
                    "Airflow Scheduler 동작 원리와 Backfill 개념",
                    "Task Idempotency(멱등성) 확보의 중요성",
                    "XCom을 이용한 Task 간 데이터 공유"
                ]
            },
            "Tier 2: Branching Point": {
                "Option 1: Big Data Master (대용량 처리)": {
                    "Distributed Concept": [
                        "데이터가 한 컴퓨터에 다 안 들어갈 때 해결법",
                        "HDFS (Hadoop Distributed File System) Block 단위 저장 원리",
                        "MapReduce 프로그래밍 모델 (Map -> Shuffle -> Reduce)",
                        "CAP Theorem (Consistency, Availability, Partition Tolerance)"
                    ],
                    "Spark Logic": [
                        "메모리 기반 처리가 빠른 이유",
                        "RDD vs DataFrame vs Dataset",
                        "Spark Lazy Evaluation과 Action vs Transformation",
                        "Wide Dependency (Shuffle) vs Narrow Dependency",
                        "Broadcast Variable과 Accumulator 활용"
                    ]
                },
                "Option 2: Real-time Master (실시간 처리)": {
                    "Event Streaming": [
                        "실시간 데이터 전송의 필요성",
                        "Kafka Broker, Topic, Partition, Offset 개념",
                        "Consumer Group과 Rebalancing 과정",
                        "Kafka Replication Factor와 Leader/Follower",
                        "Log Compaction 전략"
                    ],
                    "Stream Processing": [
                        "스트림 데이터란 무엇인가?",
                        "Processing Time vs Event Time vs Ingestion Time",
                        "Watermark 개념과 Late Data 처리",
                        "Tumbling Window vs Sliding Window vs Session Window"
                    ]
                }
            },
            "Tier 3: Core Data Architecture": {
                "Modern Data Stack": [
                    "데이터 웨어하우스(Data Warehouse)의 개념",
                    "Data Lake vs Data Warehouse vs Data Lakehouse",
                    "Table Formats (Delta Lake, Apache Iceberg, Hudi) 비교",
                    "ELT (Extract-Load-Transform) vs ETL 차이와 dbt의 역할"
                ]
            }
        }
    },
    "Track 5: MLOps Engineer": {
        "description": "운영의 지배자 (CI/CD, Monitoring, FinOps)",
        "tiers": {
            "Tier 1: Core Automation Core": {
                "Docker & Registry": [
                    "도커 이미지를 저장하는 곳 (Registry)",
                    "Image Tagging 전략 (Semantic Versioning vs Git Hash)",
                    "Docker Registry (ECR, Docker Hub) 권한 관리",
                    "Image Size 최적화 (Alpine/Distroless 이미지 활용)"
                ],
                "CI/CD Pipelines": [
                    "코드를 자동으로 배포해야 하는 이유",
                    "CI/CD 단계별 구성 (Lint -> Build -> Unit Test -> Integration Test -> Deploy)",
                    "GitHub Actions Workflow Syntax (on, jobs, steps, uses)",
                    "Blue-Green Deployment vs Canary Deployment 전략"
                ],
                "Model Logging": [
                    "실험 기록을 남겨야 하는 이유",
                    "Experiment Tracking (Hyperparams, Metrics, Artifacts)",
                    "Model Registry와 Staging/Production 단계 관리",
                    "Reproducibility(재현성) 확보를 위한 시드 및 환경 고정"
                ]
            },
            "Tier 2: Branching Point": {
                "Option 1: FinOps (비용 최적화)": {
                    "Resource Mgmt": [
                        "클라우드 비용이 발생하는 원인",
                        "Spot Instance 활용 전략 및 중단 시 처리 방안",
                        "GPU Utilization 모니터링 및 병목 현상 분석",
                        "Multi-Tenancy 환경에서의 Resource Quota 설정"
                    ],
                    "IaC": [
                        "코드로 인프라를 관리하면 좋은 점",
                        "Infrastructure as Code (IaC)의 장점과 선언적 구성",
                        "Terraform State File 관리와 Backend 설정 (S3, DynamoDB)",
                        "Terraform Module을 이용한 리소스 재사용"
                    ]
                },
                "Option 2: Model Health (품질 모니터링)": {
                    "Drift Detection": [
                        "모델 성능이 시간이 지나면 떨어지는 이유",
                        "Data Drift (Feature 분포 변화) vs Concept Drift (Target 관계 변화)",
                        "Lable Shift vs Prediction Drift",
                        "KS Test, PSI (Population Stability Index) 등 통계적 감지 기법"
                    ],
                    "Observability": [
                        "서버 로그를 확인하는 이유",
                        "Logging vs Tracing vs Metrics 차이",
                        "Prometheus Pull 방식 vs Push Gateway",
                        "Grafana Dashboard 패널 구성 및 Alert Rule 설정"
                    ]
                },
                "Tier 3: Core Monitoring Mastery": {
                    "Continuous Training": [
                        "모델을 주기적으로 다시 학습시키는 이유",
                        "CT Pipeline Trigger 조건 (Drift 감지 시, 주기적, 성능 저하 시)",
                        "Data Validation (TFDV) 및 Model Validation (TFMA) 단계",
                        "Online Learning vs Batch Learning"
                    ]
                }
            }
        }
    }
}
