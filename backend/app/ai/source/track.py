from typing import Dict, Any

# AI Tech Tree Curriculum Data
# Based on track.md v1.2
# 구조: Track -> Step -> (Option) -> Subject -> Level (Lv1, Lv2, Lv3) -> Concepts

AI_TECH_TREE: Dict[str, Any] = {
    "Track 0: The Origin": {
        "description": "모든 AI 클래스로 전직하기 위한 선행 조건입니다.",
        "steps": {
            "Step 1: Core Python Mastery": {
                "Python Syntax & Types": {
                    "Lv1": [
                        "변수 할당과 명명 규칙 (Snake Case)",
                        "기본 자료형 (int, float, str, bool)의 특징",
                        "문자열 슬라이싱(Slicing)과 인덱싱 기초",
                        "조건문 (if-elif-else)과 반복문 (for, while) 사용법",
                        "함수 정의 (def)와 return문의 역할",
                        "Module import 방법 (import, from-import)"
                    ],
                    "Lv2": [
                        "Mutable(List, Dict) vs Immutable(String, Tuple) 객체의 차이",
                        "Shallow Copy(얕은 복사) vs Deep Copy(깊은 복사)의 동작 차이",
                        "String Formatting Evolution (%-formatting vs .format() vs f-string)",
                        "Module과 Package의 차이, __init__.py의 역할"
                    ],
                    "Lv3": [
                        "GIL (Global Interpreter Lock)의 개념과 멀티스레딩 성능에 미치는 영향",
                        "Type Hinting (Generic, Union, Optional)과 Static Analysis (mypy)",
                        "Memory Management (Reference Counting & Garbage Collection)",
                        "Weakref 모듈을 이용한 순환 참조(Circular Reference) 해결",
                        "Python 3.11+ Adaptive Interpreter와 성능 개선 원리"
                    ]
                },
                "Data Structure Core": {
                    "Lv1": [
                        "List의 주요 메서드 (append, extend, pop) 사용법",
                        "Dictionary의 Key-Value 구조 이해 및 기본 조작",
                        "Set의 중복 제거 특성과 교집합/합집합 연산",
                        "Tuple의 불변성(Immutability)과 사용 이유"
                    ],
                    "Lv2": [
                        "List, Dict, Set의 Time Complexity (Big-O) 분석 (Insert, Delete, Search)",
                        "Hash Map의 동작 원리와 Hash Collision 해결 방식 (Open Addressing vs Chaining)",
                        "Deque(Double-ended Queue)의 활용과 List와의 성능 차이"
                    ],
                    "Lv3": [
                        "NamedTuple vs Dataclass: 불변성과 메모리 효율성 비교",
                        "Heapq 모듈을 이용한 Priority Queue 구현 및 내부 동작 (Binary Heap)",
                        "Python Dict의 내부 구조 변화 (Compact Dict, 3.6+)",
                        "__slots__ 매직 메서드를 이용한 클래스 메모리 최적화"
                    ]
                },
                "OOP & Functional": {
                    "Lv1": [
                        "Class 정의와 Instance 생성 방법",
                        "self 키워드의 의미와 역할",
                        "Lambda 함수(익명 함수)의 기본 문법과 활용",
                        "List Comprehension의 기본 문법과 장점"
                    ],
                    "Lv2": [
                        "Class 상속(Inheritance), 다형성(Polymorphism), 캡슐화(Encapsulation)",
                        "Decorator의 동작 원리 (@func syntax)와 활용 (Logging)",
                        "Generator와 Iterator의 차이, `yield`문의 동작",
                        "Closure와 Scope (Global, Local, Enclosing - LEGB Rule)"
                    ],
                    "Lv3": [
                        "Metaclass의 개념과 Singleton 패턴 구현 시 활용",
                        "Dunder(Magic) Methods 활용 (__new__ vs __init__, __call__)",
                        "Context Manager (__enter__, __exit__)와 `with` statement의 원리",
                        "Method Resolution Order (MRO)와 Diamond Inheritance 문제",
                        "Descriptor Protocol (__get__, __set__, __delete__) 구현"
                    ]
                }
            },
            "Step 2: Core DevOps Foundations": {
                "Linux CLI": {
                    "Lv1": [
                        "디렉토리 이동 (cd)과 목록 확인 (ls) 명령어",
                        "파일 생성 (touch), 복사 (cp), 이동 (mv), 삭제 (rm) 기초",
                        "파일 내용 확인 (cat, head, tail)",
                        "현재 경로 확인 (pwd)과 화면 지우기 (clear)"
                    ],
                    "Lv2": [
                        "파일 시스템(File System) 구조와 권한 관리 (chmod, chown, chgrp)",
                        "표준 입출력 (stdin, stdout, stderr)과 Pipe(|), Redirection(>, >>)",
                        "프로세스 관리: ps, top, htop, kill, background(&) 실행",
                        "SSH Key 생성 및 원격 서버 접속 설정 (authorized_keys)"
                    ],
                    "Lv3": [
                        "Package Manager (apt, yum, brew) 동작 원리",
                        "Soft Link vs Hard Link의 차이 (Inode 개념)",
                        "Shell Scripting 기초 (Variables, Loops, If conditions)",
                        "Systemd Service 등록 및 관리 (systemctl)",
                        "rsync를 이용한 효율적인 파일 동기화"
                    ]
                },
                "Git Version Control": {
                    "Lv1": [
                        "Git 저장소 초기화 (init)와 상태 확인 (status)",
                        "파일 스테이징 (add)과 커밋 (commit) 기초",
                        "원격 저장소 연결 (remote add)과 푸시 (push)",
                        "브랜치 생성 (branch)과 이동 (switch)"
                    ],
                    "Lv2": [
                        "Git의 3가지 영역 (Working Directory, Staging Area, Repository)",
                        "Merge vs Rebase: 히스토리 관리 차이점",
                        "Reset (Soft, Mixed, Hard)의 차이와 되돌리기 전략",
                        ".gitignore 패턴 작성법과 관리"
                    ],
                    "Lv3": [
                        "Git Flow vs GitHub Flow vs Trunk-based Development",
                        "Cherry-pick을 이용한 특정 커밋 가져오기",
                        "Interactive Rebase (`git rebase -i`)를 이용한 커밋 정리",
                        "Git Hooks (pre-commit) 활용",
                        "Git Submodule 활용 및 주의사항"
                    ]
                }
            },
            "Step 3: Core Math & Logic": {
                "Linear Algebra & Statistics": {
                    "Lv1": [
                        "평균(Mean)과 중앙값(Median)의 차이",
                        "벡터(Vector)와 행렬(Matrix)의 기본 생김새",
                        "기초 확률 (동전 던지기, 주사위 확률)",
                        "로그(Log)와 지수(Exponential)의 기본 그래프 형태"
                    ],
                    "Lv2": [
                        "Scalar, Vector, Matrix, Tensor의 개념과 차이",
                        "Matrix Multiplication (Dot Product)의 기하학적 의미",
                        "Variance, Standard Deviation(표준편차)의 의미",
                        "Correlation(상관관계) vs Causation(인과관계)"
                    ],
                    "Lv3": [
                        "Eigenvalue와 Eigenvector의 의미와 PCA(주성분 분석) 활용",
                        "확률 분포(Normal, Uniform, Bernoulli)의 특징 및 활용",
                        "Bayes' Theorem (베이즈 정리)와 조건부 확률",
                        "Gradient Descent(경사하강법)의 수학적 원리 (미분)",
                        "SVD (Singular Value Decomposition)의 AI 활용"
                    ]
                }
            }
        }
    },
    "Track 1: AI Engineer": {
        "description": "모델을 실제 서비스 환경에 이식하고 가동합니다.",
        "steps": {
            "Step 1: Core System Foundation": {
                "FastAPI Essentials": {
                    "Lv1": [
                        "GET vs POST 요청 메서드의 차이",
                        "Path Parameter(`/items/{id}`)와 Query Parameter(`?skip=0`) 사용법",
                        "JSON 요청과 응답 구조 이해",
                        "FastAPI 기본 앱 생성 및 실행"
                    ],
                    "Lv2": [
                        "Pydantic BaseModel을 이용한 데이터 유효성 검사",
                        "FastAPI의 Dependency Injection (Depends) 활용",
                        "APIRouter를 이용한 라우팅 모듈화",
                        "Exception Handler 구현과 에러 처리"
                    ],
                    "Lv3": [
                        "Middleware 구현 (CORS, Logging) 및 동작 순서",
                        "Lifespan Events (Startup/Shutdown) 처리",
                        "Background Tasks vs Celery 비동기 작업",
                        "FastAPI Security (OAuth2, JWT) 인증 흐름 구현",
                        "WebSocket 구현 및 Connection 관리"
                    ]
                },
                "Dependency Injection": {
                    "Lv1": [
                        "함수 인자로 객체 전달하기 (DI의 기초)",
                        "Global 변수 사용의 문제점"
                    ],
                    "Lv2": [
                        "Inversion of Control (IoC)와 DI의 개념",
                        "DB Session 관리 (SessionLocal)와 Depends 연결",
                        "Singleton Pattern vs Request Scoped Dependency"
                    ],
                    "Lv3": [
                        "Unit Test 작성을 위한 Dependency Overrides 활용",
                        "Container (e.g. library) 없이 DI 패턴 구현하기",
                        "Circular Dependency 문제 해결",
                        "AsyncSession (SQLAlchemy) 사용 시 주의점 및 Transaction 관리"
                    ]
                },
                "Async Architecture": {
                    "Lv1": [
                        "동기(Sync) vs 비동기(Async) 개념 차이",
                        "Python `async def`와 `await` 키워드 기본 문법"
                    ],
                    "Lv2": [
                        "Sync 함수 내에서 Async 함수 호출 불가 이유",
                        "Event Loop의 동작 원리 (Single Thread)",
                        "Blocking I/O가 서버 성능에 미치는 영향"
                    ],
                    "Lv3": [
                        "Coroutine Concurrency: `asyncio.gather` 활용",
                        "Blocking Code를 Non-blocking으로 실행하기 (run_in_executor)",
                        "ASGI vs WSGI 차이와 비동기 서버(Uvicorn)의 역할",
                        "FastAPI의 ThreadPoolExecutor 동작 방식"
                    ]
                },
                "Docker Basics": {
                    "Lv1": [
                        "Docker 이미지와 컨테이너의 차이",
                        "Dockerfile 기본 명령어 (FROM, RUN, CMD)",
                        "컨테이너 실행 (run), 중지 (stop), 로그 확인 (logs)"
                    ],
                    "Lv2": [
                        "포트 포워딩 (-p)과 볼륨 마운트 (-v) 설정",
                        "Docker Compose를 이용한 멀티 컨테이너 실행",
                        "Container vs VM (Virtual Machine) 구조적 차이"
                    ],
                    "Lv3": [
                        "Docker Image Layer Cache 원리와 Multi-stage Build 최적화",
                        "ENTRYPOINT vs CMD의 차이점 및 활용",
                        "Docker Network Mode (Bridge, Host) 이해",
                        "Distroless Image 사용을 통한 보안 강화"
                    ]
                }
            },
            "Step 2: Branching Point": {
                "Option 1: Serving Specialist": {
                    "Model Serialization": {
                        "Lv1": [
                            "모델 파일 저장(.pt, .pkl)과 불러오기 기초",
                            "Pickle 모듈 기본 사용법"
                        ],
                        "Lv2": [
                            "PyTorch `state_dict` 저장 방식 권장 이유",
                            "ONNX (Open Neural Network Exchange) 포맷의 필요성",
                            "Safetensors 포맷의 장점 (보안, 속도)"
                        ],
                        "Lv3": [
                            "TorchScript (`torch.jit.trace` vs `script`) 변환",
                            "Pickle의 보안 취약점 (RCE) 원리"
                        ]
                    },
                    "Inference Optimization": {
                        "Lv1": [
                            "모델 경량화의 필요성 이해",
                            "Python 코드 실행 시간 측정 (time 모듈)"
                        ],
                        "Lv2": [
                            "Quantization (양자화) 개념: FP32 -> INT8",
                            "Pruning (가지치기) 개념: 불필요한 가중치 제거",
                            "Batch Processing을 통한 Throughput 향상"
                        ],
                        "Lv3": [
                            "TensorRT Engine 빌드 및 Layer Fusion 원리",
                            "Quantization Aware Training (QAT) vs Post Training Quantization (PTQ)",
                            "Kernel Fusion과 Memory access 최적화",
                            "vLLM / TGI 프레임워크의 PagedAttention 기술"
                        ]
                    },
                    "Serving Frameworks": {
                        "Lv1": [
                            "Flask/FastAPI로 모델 결과 반환하기",
                            "REST API 기본 구조 설계"
                        ],
                        "Lv2": [
                            "gRPC vs HTTP 프로토콜 성능 비교",
                            "Triton Inference Server의 기본 아키텍처",
                            "Model Repository 구조 관리"
                        ],
                        "Lv3": [
                            "Dynamic Batching 동작 원리와 Latency 트레이드오프",
                            "Ensemble Model Serving 파이프라인 구성",
                            "Concurrent Model Execution (Multi-instance GPU)"
                        ]
                    }
                },
                "Option 2: App Architect": {
                    "Database Design": {
                        "Lv1": [
                            "Table, Row, Column 개념",
                            "PK (Primary Key)와 FK (Foreign Key)의 역할"
                        ],
                        "Lv2": [
                            "Indexing (B-Tree)의 원리와 검색 성능 향상",
                            "N+1 Problem의 원인과 Eager Loading 해결법",
                            "ACID 트랜잭션 속성의 의미"
                        ],
                        "Lv3": [
                            "Composite Index (복합 인덱스) 설계 전략",
                            "DB Replication (Master-Slave) vs Sharding 차이",
                            "Isolation Level (Read Committed vs Repeatable Read)",
                            "Time-Series DB (InfluxDB) vs RDBMS 차이"
                        ]
                    },
                    "Caching Strategy": {
                        "Lv1": [
                            "캐시(Cache)의 기본 개념과 필요성",
                            "Key-Value 저장소(Redis)의 특징"
                        ],
                        "Lv2": [
                            "Cache-Aside Pattern (Look-aside) 구현 흐름",
                            "TTL (Time To Live) 설정의 중요성"
                        ],
                        "Lv3": [
                            "Write-Through vs Write-Back 캐싱 패턴 비교",
                            "Redis Eviction Policies (LRU, LFU) 선택 기준",
                            "Cache Stampede (Thundering Herd) 문제와 해결책",
                            "Distributed Lock (Redlock) 구현"
                        ]
                    },
                    "Message Queue": {
                        "Lv1": [
                            "Producer와 Consumer의 개념",
                            "비동기 작업이 필요한 상황 예시"
                        ],
                        "Lv2": [
                            "Celery 기본 구조 (Broker, Worker, Result Backend)",
                            "Pub/Sub 패턴 vs Point-to-Point 패턴"
                        ],
                        "Lv3": [
                            "Message Durability와 Persistence",
                            "Idempotency(멱등성) 보장 전략",
                            "Dead Letter Queue (DLQ) 활용 및 Retry 정책",
                            "Kafka vs RabbitMQ 아키텍처 비교"
                        ]
                    }
                }
            },
            "Step 3: Core Infrastructure Mastery": {
                "Container Orchestration": {
                    "Lv1": [
                        "컨테이너 하나로는 부족한 이유 (Scaling)",
                        "Kubernetes(K8s)란 무엇인가?"
                    ],
                    "Lv2": [
                        "Pod, ReplicaSet, Deployment의 관계",
                        "Service (ClusterIP, NodePort, LoadBalancer) 타입 이해",
                        "ConfigMap과 Secret 활용"
                    ],
                    "Lv3": [
                        "Ingress Controller와 Path Routing",
                        "Liveness Probe vs Readiness Probe 설정",
                        "Helm Chart를 이용한 패키지 관리",
                        "Affinity/Anti-Affinity 및 Taint/Toleration 스케줄링"
                    ]
                },
                "GPU Scaling": {
                    "Lv1": [
                        "GPU가 딥러닝에 유리한 이유 (병렬 처리)",
                        "CUDA와 cuDNN의 역할"
                    ],
                    "Lv2": [
                        "Kubernetes Resource Requests/Limits (GPU 할당)",
                        "Node Selector와 Taint/Toleration 활용"
                    ],
                    "Lv3": [
                        "NVIDIA Device Plugin 동작 원리",
                        "HPA (Horizontal Pod Autoscaler) 설정 (Custom Metrics)",
                        "MIG (Multi-Instance GPU) 기술과 활용"
                    ]
                }
            }
        }
    },
    "Track 2: AI Modeler / Researcher": {
        "description": "데이터를 지능으로 변환하는 핵심 모델을 설계합니다.",
        "steps": {
            "Step 1: Core Deep Learning Engine": {
                "Tensor Operations": {
                    "Lv1": [
                        "Tensor(텐서)의 정의와 Rank(차원)",
                        "Tensor Shape 확인 및 기본 생성 (`torch.tensor`)"
                    ],
                    "Lv2": [
                        "Reshape vs View 차이점 (Contiguous 개념)",
                        "Tensor Broadcasting Rule 이해 및 예제",
                        "Element-wise 연산 vs Matrix Multiplication"
                    ],
                    "Lv3": [
                        "Permute vs Transpose 차이와 메모리 레이아웃",
                        "Fancy Indexing과 Masking 활용",
                        "`torch.einsum`을 이용한 복잡한 연산 표현"
                    ]
                },
                "AutoGrad & Backprop": {
                    "Lv1": [
                        "미분(Derivative)과 기울기(Gradient)의 의미",
                        "Loss Function(손실 함수)의 역할"
                    ],
                    "Lv2": [
                        "Chain Rule(연쇄 법칙)의 개념",
                        "Computational Graph (Forward vs Backward Pass)",
                        "`requires_grad=True`의 의미"
                    ],
                    "Lv3": [
                        "`with torch.no_grad()`와 `.detach()`의 차이",
                        "Dynamic Computational Graph (PyTorch) vs Static (TensorFlow v1)",
                        "Gradient Accumulation 원리 및 구현"
                    ]
                },
                "Training Loop": {
                    "Lv1": [
                        "Epoch, Batch Size, Iteration 용어 정의",
                        "Train / Validation / Test 데이터셋 분리 이유"
                    ],
                    "Lv2": [
                        "Dataset 클래스 (`__len__`, `__getitem__`) 구현",
                        "DataLoader 및 `batch_size`, `shuffle` 옵션 활용",
                        "Optimizer (`step`, `zero_grad`)의 역할"
                    ],
                    "Lv3": [
                        "Custom Collate Function (`collate_fn`) 구현",
                        "DataLoader의 `num_workers`와 `pin_memory` 최적화",
                        "Learning Rate Scheduler (Warmup, Cosine decay) 활용 전략"
                    ]
                }
            },
            "Step 2: Branching Point": {
                "Option 1: Vision Sage": {
                    "CNN Backbones": {
                        "Lv1": [
                            "픽셀(Pixel)과 RGB 채널의 이해",
                            "Convolution 연산의 기본 개념"
                        ],
                        "Lv2": [
                            "Kernel(Filter), Stride, Padding의 역할",
                            "Pooling (Max, Average)의 의미와 차원 축소",
                            "CNN이 위치 불변성(Translation Invariance)을 가지는 이유"
                        ],
                        "Lv3": [
                            "ResNet의 Residual Connection (Skip Connection)과 Vanishing Gradient 해결",
                            "Receptive Field의 개념과 계산",
                            "ViT (Vision Transformer)의 Patch Embedding 및 구조",
                            "EfficientNet의 Compound Scaling 전략"
                        ]
                    },
                    "Object Detection": {
                        "Lv1": [
                            "Image Classification vs Object Detection 차이",
                            "Bounding Box (x, y, w, h) 표현 방식"
                        ],
                        "Lv2": [
                            "IoU (Intersection over Union) 계산 방법",
                            "One-stage (YOLO) vs Two-stage (R-CNN) Detector 구조 차이",
                            "Anchor Box의 개념"
                        ],
                        "Lv3": [
                            "NMS (Non-Maximum Suppression) 알고리즘 상세 과정",
                            "Focal Loss (Class Imbalance 문제 해결)",
                            "mAP (mean Average Precision) 측정 방식"
                        ]
                    },
                    "Generative Vision": {
                        "Lv1": [
                            "생성 모델(Generative Model)의 목표",
                            "Noise에서 이미지를 생성하는 기본 아이디어"
                        ],
                        "Lv2": [
                            "VAE (Variational AutoEncoder)와 Latent Space 개념",
                            "Diffusion Model의 Forward vs Reverse Process 개요"
                        ],
                        "Lv3": [
                            "Stable Diffusion의 Latent Diffusion 구조 (Pixel Space vs Latent Space)",
                            "U-Net Architecture와 Cross-Attention (Text Conditioning) 연결",
                            "CLIP 모델을 이용한 Text-Image Alignment 원리",
                            "DDPM vs DDIM Sampling 차이"
                        ]
                    }
                },
                "Option 2: Language Sage": {
                    "Transformer Arch": {
                        "Lv1": [
                            "단어 임베딩(Embedding)의 필요성",
                            "RNN/LSTM의 장기 의존성(Long-term Dependency) 문제"
                        ],
                        "Lv2": [
                            "Attention Mechanism의 직관적 설명 (Query, Key, Value)",
                            "Self-Attention vs Cross-Attention 차이",
                            "Positional Encoding이 필요한 이유"
                        ],
                        "Lv3": [
                            "Multi-Head Attention의 수식적 이해와 장점",
                            "Encoder-only (BERT), Decoder-only (GPT), Encoder-Decoder (T5) 구조 비교",
                            "RoPE (Rotary Positional Embedding) 등 최신 위치 인코딩",
                            "Flash Attention의 I/O Aware 최적화 원리"
                        ]
                    },
                    "Tokenization": {
                        "Lv1": [
                            "공백 기준 분절 vs 형태소 분석",
                            "Token ID와 Decoding 개념"
                        ],
                        "Lv2": [
                            "Subword Tokenization (BPE, WordPiece) 알고리즘 원리",
                            "Special Token ([CLS], [SEP], [PAD])의 역할",
                            "OOV (Out of Vocabulary) 문제 해결법"
                        ],
                        "Lv3": [
                            "Byte-level BPE (BBPE)의 동작 방식",
                            "Vocabulary Size와 모델 파라미터/메모리 관계",
                            "Dynamic Padding을 통한 배치 처리 최적화"
                        ]
                    },
                    "PEFT": {
                        "Lv1": [
                            "Pre-training vs Fine-tuning 차이",
                            "모델 전체 학습(Full Fine-tuning)의 비용 문제"
                        ],
                        "Lv2": [
                            "Parameter Efficient Fine-Tuning (PEFT) 개념",
                            "LoRA (Low-Rank Adaptation)의 기본 아이디어",
                            "Adapter Layer의 구조"
                        ],
                        "Lv3": [
                            "LoRA의 Rank(r)와 Alpha값의 의미",
                            "QLoRA (Quantized LoRA)와 4-bit Normal Float (NF4)",
                            "Prompt Tuning vs Prefix Tuning 차이"
                        ]
                    }
                }
            },
            "Step 3: Core Advanced Training": {
                "Distributed Training": {
                    "Lv1": [
                        "배치 사이즈를 키우기 위해 여러 GPU가 필요한 이유",
                        "GPU 메모리 부족 (OOM) 현상"
                    ],
                    "Lv2": [
                        "Data Parallel (DP) 구조와 한계 (Master Node 병목)",
                        "Distributed Data Parallel (DDP)의 개선점 (All-Reduce)"
                    ],
                    "Lv3": [
                        "Model Parallelism (Tensor Parallel vs Pipeline Parallel)",
                        "FSDP (Fully Sharded Data Parallel)의 메모리 분산 원리",
                        "ZeRO (Zero Redundancy Optimizer) Stage 1, 2, 3 비교"
                    ]
                },
                "Memory Optimization": {
                    "Lv1": [
                        "모델 파라미터 외에 메모리를 차지하는 것들 (Optimizer State, Gradient)",
                        "Batch Size 조절의 영향"
                    ],
                    "Lv2": [
                        "Mixed Precision Training (FP16/BF16) 개념",
                        "Gradient Checkpointing (Activation Checkpointing) 원리"
                    ],
                    "Lv3": [
                        "FP16 학습 시 Loss Scaling이 필요한 이유 (Underflow 방지)",
                        "KV Cache 최적화 (PagedAttention)",
                        "CPU Offloading의 장단점 (속도 vs 메모리)"
                    ]
                }
            }
        }
    },
    "Track 3: LLM Application Engineer": {
        "description": "LLM을 활용하여 지능형 앱과 자율 에이전트를 개발합니다.",
        "steps": {
            "Step 1: Core Context Integration": {
                "Prompting Basics": {
                    "Lv1": [
                        "Prompt Engineering이란?",
                        "System Prompt vs User Prompt 차이"
                    ],
                    "Lv2": [
                        "Zero-shot vs Few-shot Learning (In-context Learning)",
                        "Role Playing 기법의 효과",
                        "Prompt Injection 공격과 방어"
                    ],
                    "Lv3": [
                        "LLM Hyperparameters (Temperature, Top-p) 튜닝 전략",
                        "Chain of Thought (CoT) 프롬프팅 원리",
                        "Structured Output (JSON Mode) 강제화 기법"
                    ]
                },
                "Chain of Thought": {
                    "Lv1": [
                        "생각의 사슬(Chain of Thought) 직관적 이해",
                        "Step-by-step으로 생각하라고 지시하기"
                    ],
                    "Lv2": [
                        "Zero-shot CoT ('Let's think step by step')의 효과",
                        "Few-shot CoT 예제 작성법"
                    ],
                    "Lv3": [
                        "Tree of Thoughts (ToT) 탐색 알고리즘 (BFS/DFS)",
                        "Self-Consistency (Majority Voting) 기법",
                        "Least-to-Most Prompting 전략"
                    ]
                },
                "Embeddings": {
                    "Lv1": [
                        "텍스트를 벡터로 변환하는 이유",
                        "유사도(Similarity) 개념"
                    ],
                    "Lv2": [
                        "Sparse Vector (Keyword) vs Dense Vector (Semantic) 차이",
                        "Cosine Similarity vs Euclidean Distance 비교",
                        "OpenAI Embedding Model 활용"
                    ],
                    "Lv3": [
                        "MTEB (Massive Text Embedding Benchmark) 이해",
                        "Cross-Encoder vs Bi-Encoder 아키텍처 차이",
                        "Matryoshka Embedding (차원 축소 지원) 개념"
                    ]
                },
                "Vector DB": {
                    "Lv1": [
                        "일반 DB와 Vector DB의 차이점",
                        "Nearest Neighbor Search 개념"
                    ],
                    "Lv2": [
                        "Vector Indexing의 필요성 (속도 문제)",
                        "Metadata Filtering 개념 (Pre vs Post filtering)",
                        "Pinecone/Milvus 기본 사용법"
                    ],
                    "Lv3": [
                        "HNSW (Hierarchical Navigable Small World) 알고리즘 원리",
                        "IVF (Inverted File Index) 구조",
                        "HNSW 파라미터 튜닝 (M, ef_construction, ef_search)",
                        "Search Latency vs Recall(재현율) 트레이드오프 튜닝"
                    ]
                }
            },
            "Step 2: Branching Point": {
                "Option 1: Agentic Workflow": {
                    "ReAct Pattern": {
                        "Lv1": [
                            "AI Agent 정의: 생각하고 행동하는 AI",
                            "ReAct (Reasoning + Acting) 약어 의미"
                        ],
                        "Lv2": [
                            "ReAct Loop 구조: Thought -> Action -> Observation",
                            "Planning 단계의 중요성"
                        ],
                        "Lv3": [
                            "ReAct 프롬프트 템플릿 설계",
                            "Hallucination during reasoning 문제 해결",
                            "Reflexion (Self-reflection) 패턴 추가"
                        ]
                    },
                    "Tool Use": {
                        "Lv1": [
                            "LLM이 외부 도구(계산기, 검색)를 쓰는 이유",
                            "Function Calling 개념"
                        ],
                        "Lv2": [
                            "OpenAI Function Calling JSON Schema 정의",
                            "Tool 실행 결과 LLM에 다시 주입하기"
                        ],
                        "Lv3": [
                            "Parallel Function Calling 처리",
                            "Tool Output 에러 핸들링 및 재시도 전략",
                            "Tool RAG (많은 도구 중 선택하기)"
                        ]
                    },
                    "Multi-Agent": {
                        "Lv1": [
                            "Single Agent vs Multi-Agent 차이",
                            "역할 분담의 필요성"
                        ],
                        "Lv2": [
                            "Orchestrator-Workers (Manager-Subordinates) 패턴",
                            "LangGraph의 State 및 Node/Edge 개념"
                        ],
                        "Lv3": [
                            "Autonomous Agents 간의 Communication Protocol",
                            "Multi-Agent Debate/Consensus 패턴",
                            "Hierarchical Planning 구조 구현"
                        ]
                    }
                },
                "Option 2: Reliability & Eval": {
                    "Advanced RAG": {
                        "Lv1": [
                            "RAG(검색 증강 생성) 기본 개념",
                            "Context Window 한계 극복"
                        ],
                        "Lv2": [
                            "Hybrid Search (Keyword + Semantic) 구현",
                            "Reranking (Cross-Encoder)을 통한 정확도 향상",
                            "Multi-Query (Query Expansion) 전략"
                        ],
                        "Lv3": [
                            "HyDE (Hypothetical Document Embeddings) 기법",
                            "Parent Document Retriever 구조",
                            "GraphRAG: Knowledge Graph를 이용한 검색 증강",
                            "Contextual Compression 및 Filtering"
                        ]
                    },
                    "Chunking Strategy": {
                        "Lv1": [
                            "문서를 쪼개는 (Chunking) 이유",
                            "Token 개수 제한"
                        ],
                        "Lv2": [
                            "Fixed-size Chunking vs Recursive Character Splitting",
                            "Overlap 설정의 중요성"
                        ],
                        "Lv3": [
                            "Semantic Chunking (의미 기반 분할) 알고리즘",
                            "Markdown/Structure Aware Chunking",
                            "Small-to-Big Retrieval 전략"
                        ]
                    },
                    "LLM Evaluation": {
                        "Lv1": [
                            "LLM 답변 평가가 어려운 이유",
                            "정성 평가 vs 정량 평가"
                        ],
                        "Lv2": [
                            "Reference-based Metrics (BLEU, ROUGE)의 한계",
                            "LLM-as-a-Judge 개념 (GPT-4로 평가하기)"
                        ],
                        "Lv3": [
                            "RAGAS Framework 평가지표 (Faithfulness, Answer Relevance, Context Recall)",
                            "G-Eval 논문의 평가 방식",
                            "Hallucination Detection 기법 (Self-CheckGPT)"
                        ]
                    }
                }
            },
            "Step 3: Core Production Excellence": {
                "Prompt Management": {
                    "Lv1": [
                        "프롬프트를 코드처럼 관리해야 하는 이유",
                        "Prompt Template 개념"
                    ],
                    "Lv2": [
                        "Prompt Versioning 및 Git 관리",
                        "A/B Testing 설계 (Prompt A vs Prompt B)"
                    ],
                    "Lv3": [
                        "Prompt Optimization 자동화 (DSPy 개념)",
                        "Prompt Registry 시스템 구축"
                    ]
                },
                "Feedback Loop": {
                    "Lv1": [
                        "사용자 피드백 수집 (좋아요/싫어요)",
                        "데이터 플라이휠 개념"
                    ],
                    "Lv2": [
                        "Implicit Feedback (체류시간, 복사) vs Explicit Feedback",
                        "Feedback 데이터 DB 스키마 설계"
                    ],
                    "Lv3": [
                        "RLHF (Reinforcement Learning from Human Feedback) 개요",
                        "DPO (Direct Preference Optimization) 데이터셋 구축",
                        "Online Learning 파이프라인"
                    ]
                }
            }
        }
    },
    "Track 4: Data Engineer": {
        "description": "안정적인 데이터 파이프라인과 대규모 데이터 인프라를 관리합니다.",
        "steps": {
            "Step 1: Core Data Flow": {
                "SQL Mastery": {
                    "Lv1": [
                        "SELECT, WHERE, ORDER BY, LIMIT 기본 문법",
                        "GROUP BY와 집계 함수 (COUNT, SUM, AVG)"
                    ],
                    "Lv2": [
                        "JOIN (Inner, Left, Outer)의 차이와 활용",
                        "Subquery vs JOIN 성능 차이",
                        "CASE WHEN 구문 활용"
                    ],
                    "Lv3": [
                        "Window Functions (RANK, ROW_NUMBER, LAG, LEAD) 활용",
                        "CTE (Common Table Expression)와 재귀 쿼리",
                        "Query Execution Plan 분석 및 인덱스 최적화"
                    ]
                },
                "Data Modeling": {
                    "Lv1": [
                        "ERD (Entity Relationship Diagram) 읽는 법",
                        "정규화(Normalization)의 목적 (중복 제거)"
                    ],
                    "Lv2": [
                        "Star Schema vs Snowflake Schema 구조 비교",
                        "Fact Table vs Dimension Table 개념",
                        "Denormalization(비정규화)을 하는 이유"
                    ],
                    "Lv3": [
                        "SCD (Slowly Changing Dimensions) Type 1, 2, 3 구현",
                        "Data Mart 설계 전략",
                        "Columnar Storage (Parquet) vs Row-based Storage (CSV) 차이"
                    ]
                },
                "Workflow Orchestration": {
                    "Lv1": [
                        "작업 스케줄링 (Cron)의 개념",
                        "Airflow DAG과 Task 정의"
                    ],
                    "Lv2": [
                        "Airflow Operator 활용 (Bash, Python)",
                        "Task Dependency 설정 (>>)",
                        "Idempotency(멱등성)의 중요성"
                    ],
                    "Lv3": [
                        "Airflow Scheduler와 Executor 동작 원리",
                        "Backfill과 Catchup 개념 및 주의점",
                        "XCom을 이용한 데이터 공유와 한계"
                    ]
                }
            },
            "Step 2: Branching Point": {
                "Option 1: Big Data Master": {
                    "Distributed Concept": {
                        "Lv1": [
                            "분산 처리의 필요성 (Scale-out vs Scale-up)",
                            "HDFS (하둡 분산 파일 시스템) 기본 개념"
                        ],
                        "Lv2": [
                            "MapReduce 모델 (Split -> Map -> Shuffle -> Reduce)",
                            "CAP Theorem (Consistency, Availability, Partition Tolerance)"
                        ],
                        "Lv3": [
                            "Data Skewness (데이터 쏠림) 현상과 해결책",
                            "Data Partitioning 전략",
                            "Replication Factor와 Fault Tolerance"
                        ]
                    },
                    "Spark Logic": {
                        "Lv1": [
                            "Spark가 Hadoop MapReduce보다 빠른 이유 (In-memory)",
                            "PySpark 기본 DataFrame 조작"
                        ],
                        "Lv2": [
                            "RDD vs DataFrame vs Dataset 차이",
                            "Lazy Evaluation과 Action/Transformation",
                            "Spark Job, Stage, Task 계층 구조"
                        ],
                        "Lv3": [
                            "Wide Dependency (Shuffle) vs Narrow Dependency",
                            "Broadcast Join vs Shuffle Hash Join",
                            "Spark Memory Management (Storage vs Execution)"
                        ]
                    }
                },
                "Option 2: Real-time Master": {
                    "Event Streaming": {
                        "Lv1": [
                            "배치(Batch) vs 스트리밍(Streaming) 차이",
                            "Kafka 기본 용어 (Topic, Producer, Consumer)"
                        ],
                        "Lv2": [
                            "Kafka Partition과 Parallelism",
                            "Consumer Group과 Offset 관리",
                            "Replication Factor와 Leader/Follower"
                        ],
                        "Lv3": [
                            "Kafka Delivery Semantics (At-least-once, Exactly-once)",
                            "ACK 설정 (0, 1, all)과 데이터 내구성",
                            "Log Compaction 동작 원리"
                        ]
                    },
                    "Stream Processing": {
                        "Lv1": [
                            "Stateless vs Stateful 스트림 처리",
                            "Windowing 개념 (시간 단위 묶기)"
                        ],
                        "Lv2": [
                            "Tumbling vs Sliding vs Session Window 차이",
                            "Event Time vs Processing Time 개념",
                            "Late Data 처리 (Watermark)"
                        ],
                        "Lv3": [
                            "Stream-Stream Join 시의 문제점과 해결",
                            "Exactly-once Processing 구현 원리 (Checkpointing)",
                            "Backpressure 처리 메커니즘"
                        ]
                    }
                }
            },
            "Step 3: Core Data Architecture": {
                "Modern Data Stack": {
                    "Lv1": [
                        "Data Warehouse vs Data Lake 개념",
                        "ETL vs ELT 차이"
                    ],
                    "Lv2": [
                        "Data Lakehouse 아키텍처 (Delta Lake, Iceberg)",
                        "dbt (data build tool)의 역할과 장점"
                    ],
                    "Lv3": [
                        "Table Format (ACID on Data Lake) 기술 비교",
                        "Data Mesh / Data Fabric 개념",
                        "Lambda vs Kappa Architecture"
                    ]
                }
            }
        }
    },
    "Track 5: MLOps Engineer": {
        "description": "전체 ML 생명 주기를 자동화하고 운영 효율을 극대화합니다.",
        "steps": {
            "Step 1: Core Automation Core": {
                "Docker & Registry": {
                    "Lv1": [
                        "이미지 레지스트리(ECR, DockerHub) 역할",
                        "Image Build 기본 명령어"
                    ],
                    "Lv2": [
                        "Semantic Versioning을 이용한 Image Tagging 전략",
                        "Dockerfile Layer Caching을 이용한 빌드 속도 향상"
                    ],
                    "Lv3": [
                        "Multi-stage Build를 통한 Image Size 최소화",
                        "Distroless/Alpine 이미지 활용 및 보안 이점",
                        "Private Registry 인증 및 권한 관리"
                    ]
                },
                "CI/CD Pipelines": {
                    "Lv1": [
                        "CI(지속적 통합)와 CD(지속적 배포)의 의미",
                        "GitHub Actions 기본 YAML 구조"
                    ],
                    "Lv2": [
                        "CI 파이프라인 단계 (Lint -> Test -> Build)",
                        "Secrets 관리 및 환경변수 주입",
                        "CD 전략: Rolling Update"
                    ],
                    "Lv3": [
                        "Blue-Green vs Canary Deployment 구현 차이",
                        "Self-hosted Runner 구축 및 활용",
                        "GitOps 개념 (ArgoCD)"
                    ]
                },
                "Model Logging": {
                    "Lv1": [
                        "실험 관리(Experiment Tracking)의 필요성",
                        "모델의 Hyperparameter와 Metric 기록"
                    ],
                    "Lv2": [
                        "MLflow/WandB 기본 사용법",
                        "Model Artifact (가중치 파일) 저장 및 버전 관리"
                    ],
                    "Lv3": [
                        "Model Registry의 Stage 관리 (Staging -> Production)",
                        "Reproducibility(재현성)를 위한 Random Seed 및 환경 고정",
                        "Model Card 작성 및 메타데이터 관리"
                    ]
                }
            },
            "Step 2: Branching Point": {
                "Option 1: FinOps": {
                    "Resource Mgmt": {
                        "Lv1": [
                            "클라우드 비용 구성 요소 (Compute, Storage, Network)",
                            "Unused Resource 찾기"
                        ],
                        "Lv2": [
                            "Spot Instance 활용 및 중단 처리 전략",
                            "Auto Scaling Group (ASG) 설정",
                            "GPU Sharing (MIG, Time-slicing) 기술"
                        ],
                        "Lv3": [
                            "Kubernetes Resource Quota 및 LimitRange 설정",
                            "FinOps 프레임워크 및 비용 할당(Tagging) 전략",
                            "Reserved Instance (RI) / Savings Plan 활용"
                        ]
                    },
                    "IaC": {
                        "Lv1": [
                            "IaC (Infrastructure as Code) 개념",
                            "Terraform 기본 문법 (HCL)"
                        ],
                        "Lv2": [
                            "Terraform `plan` vs `apply` 차이",
                            "State File의 역할과 관리 (S3 Backend)",
                            "Resource Dependency 처리"
                        ],
                        "Lv3": [
                            "Terraform Module을 이용한 코드 재사용성",
                            "State Locking을 이용한 협업 안전성 확보",
                            "Drift Detection (실제 인프라와 코드의 차이 감지)"
                        ]
                    }
                },
                "Option 2: Model Health": {
                    "Drift Detection": {
                        "Lv1": [
                            "Model Decay (성능 저하) 현상 이해",
                            "Training 데이터와 Serving 데이터의 차이"
                        ],
                        "Lv2": [
                            "Data Drift (Covariate Shift) 개념",
                            "Concept Drift (Target Shift - P(y|x) 변화) 개념",
                            "기본 통계적 감지 (Mean, Variance 변화)"
                        ],
                        "Lv3": [
                            "KS Test, PSI (Population Stability Index) 활용",
                            "KL Divergence, JS Divergence 측정",
                            "Label Delay 문제와 해결 전략"
                        ]
                    },
                    "Observability": {
                        "Lv1": [
                            "Logging의 중요성 (Access Log, Error Log)",
                            "Metrics (CPU, Memory) 모니터링"
                        ],
                        "Lv2": [
                            "Logging vs Metrics vs Tracing (3 Pillars)",
                            "Prometheus Pull 방식 아키텍처",
                            "Grafana Dashboard 패널 생성"
                        ],
                        "Lv3": [
                            "Distributed Tracing (OpenTelemetry, Jaeger)",
                            "Prometheus AlertManager Rule 설정",
                            "Custom Metric Exporter 개발 (FastAPI middleware)"
                        ]
                    }
                }
            },
            "Step 3: Core Monitoring Mastery": {
                "Continuous Training": {
                    "Lv1": [
                        "재학습(Retraining) 프로세스 개요",
                        "Manual Retraining vs Automated Retraining"
                    ],
                    "Lv2": [
                        "CT Pipeline 구성 요소 (Data Val -> Train -> Eval -> Deploy)",
                        "Retraining Trigger 조건 (시간 기반 vs 성능 기반)"
                    ],
                    "Lv3": [
                        "TFDV (TensorFlow Data Validation) 활용",
                        "TFMA (TensorFlow Model Analysis) 슬라이싱 평가",
                        "Online Learning vs Batch Learning 시스템 아키텍처"
                    ]
                }
            }
        }
    }
}
