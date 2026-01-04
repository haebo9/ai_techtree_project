# 🎮 AI Tech Tree: The Path of Mastery (v1.2)

이 문서는 AI 엔지니어로 성장하기 위한 계층적 스킬 트리를 정의합니다. 모든 모험가는 **Tier 0**에서 시작하며, 이후 전직을 통해 자신만의 전문화된 경로(Option)를 선택할 수 있습니다.

> **Maturity Evaluation Criteria**:
> * **Lv.1 (Novice)**: **Accuracy** (용어와 정의를 정확히 아는가?)
> * **Lv.2 (Proficient)**: **Problem Solving** (코드로 현실적인 문제를 해결하는가?)
> * **Lv.3 (Expert)**: **Architecture** (설계, 확장성, 트레이드오프를 고려하는가?)

---

## 🏁 Track 0: The Origin (공통 필수 기반)

**모든 AI 클래스로 전직하기 위한 선행 조건입니다.**

* **[Tier 1: Core] Python Mastery**
  * 🔹 `Python Syntax & Types` : 변수, 자료형, 기초 문법
  * 🔹 `Data Structure Core` : List, Dict, Set의 메모리 구조 및 효율성
  * 🔹 `OOP & Functional` : Class, Decorator, Generator, Lambda

* **[Tier 2: Core] DevOps Foundations**
  * 🔹 `Linux CLI` : 파일 시스템, 권한, 프로세스 관리
  * 🔹 `Git Version Control` : Commit, Branch, Merge, Rebase

* **[Tier 3: Core] Math & Logic**
  * 🔹 `Linear Algebra & Statistics` : 선형대수, 기초 통계학 (AI 구동 원리 이해)

---

## 🛠️ Track 1: AI Engineer (시스템 구축가)

**모델을 실제 서비스 환경에 이식하고 가동합니다.**

* **[Tier 1: Core] System Foundation**
  * 🔹 `FastAPI Essentials` : Path/Query Param, Pydantic Schema
  * 🔹 `Dependency Injection` : Depends, DB Session 관리, Testability
  * 🔹 `Async Architecture` : async/await, Event Loop, Coroutine
  * 🔹 `Docker Basics` : Image Build, Container Run, Dockerfile

* **[Tier 2: Branching Point] 전문 분야 선택**
  * **Option 1: Serving Specialist (추론 최적화)**
    * 🔸 `Model Serialization`: Pickle, Safetensors, ONNX Export
    * 🔸 `Inference Optimization`: TensorRT 변환, Quantization (INT8)
    * 🔸 `Serving Frameworks`: Triton Inference Server, BentoML
  * **Option 2: App Architect (서비스 아키텍처)**
    * 🔸 `Database Design`: Indexing, N+1 Problem, Migration
    * 🔸 `Caching Strategy`: Redis Caching, TTL, Eviction Policy
    * 🔸 `Message Queue`: Celery/RabbitMQ 비동기 작업 처리

* **[Tier 3: Core] Infrastructure Mastery**
  * 💎 `Container Orchestration`: Kubernetes Pod, Deployment, Service
  * 💎 `GPU Scaling`: NVIDIA Plugin, Resource Limit, Autoscaling

---

## 🧠 Track 2: AI Modeler / Researcher (알고리즘 술사)

**데이터를 지능으로 변환하는 핵심 모델을 설계합니다.**

* **[Tier 1: Core] Deep Learning Engine**
  * 🔹 `Tensor Operations` : PyTorch Tensor Shape, Broadcasting
  * 🔹 `AutoGrad & Backprop` : Computational Graph, Gradient Flow
  * 🔹 `Training Loop` : Dataset, DataLoader, Custom Training Step

* **[Tier 2: Branching Point] 도메인 특화**
  * **Option 1: Vision Sage (시각 지능)**
    * 🔸 `CNN Backbones`: ResNet, EfficientNet 구조
    * 🔸 `Object Detection`: YOLO, Faster R-CNN 원리
    * 🔸 `Generative Vision`: Diffusion Model (Stable Diffusion) 원리
  * **Option 2: Language Sage (언어 지능)**
    * 🔸 `Transformer Arch`: Attention Mechanism, Encoder-Decoder
    * 🔸 `Tokenization`: BPE, WordPiece, SentencePiece
    * 🔸 `PEFT`: LoRA, QLoRA, Adapter 튜닝

* **[Tier 3: Core] Advanced Training**
  * 💎 `Distributed Training`: DDP (Data Parallel), FSDP
  * 💎 `Memory Optimization`: Mixed Precision (FP16/BF16), Gradient Checkpointing

---

## ⚡ Track 3: LLM Application Engineer (에이전트 소환사)

**LLM을 활용하여 지능형 앱과 자율 에이전트를 개발합니다.**

* **[Tier 1: Core] Context Integration**
  * 🔹 `Prompting Basics` : Zero-shot, Few-shot, Role Prompting
  * 🔹 `Chain of Thought` : CoT, Tree of Thoughts (Reasoning steps)
  * 🔹 `Embeddings` : Vector Representation 의미와 활용
  * 🔹 `Vector DB` : Pinecone/Milvus Indexing & Search

* **[Tier 2: Branching Point] 시스템 고도화**
  * **Option 1: Agentic Workflow (자율 에이전트)**
    * 🔸 `ReAct Pattern`: Reasoning + Acting Loop
    * 🔸 `Tool Use`: Function Calling, API Schema 정의
    * 🔸 `Multi-Agent`: Orchestrator, Worker 구조 (LangGraph)
  * **Option 2: Reliability & Eval (신뢰성 및 평가)**
    * 🔸 `Advanced RAG`: Hybrid Search (Keyword+Vector), Reranking
    * 🔸 `Chunking Strategy`: Semantic Chunking, Parent Document
    * 🔸 `LLM Evaluation`: RAGAS Metrics, LLM-as-a-Judge

* **[Tier 3: Core] Production Excellence**
  * 💎 `Prompt Management`: Versioning, A/B Testing
  * 💎 `Feedback Loop`: User Feedback 반영 자동화 (LLMOps)

---

## 🏗️ Track 4: Data Engineer (데이터 대장장이)

**안정적인 데이터 파이프라인과 대규모 데이터 인프라를 관리합니다.**

* **[Tier 1: Core] Data Flow**
  * 🔹 `SQL Mastery` : Complex Join, Window Function, CTE
  * 🔹 `Data Modeling` : Star/Snowflake Schema, Normalization
  * 🔹 `Workflow Orchestration` : Airflow DAG 작성, Idempotency

* **[Tier 2: Branching Point] 기술 스택 특화**
  * **Option 1: Big Data Master (대용량 처리)**
    * 🔸 `Distributed Concept`: MapReduce, Shuffle, Partitioning
    * 🔸 `Spark Logic`: DataFrame API, Lazy Evaluation
  * **Option 2: Real-time Master (실시간 처리)**
    * 🔸 `Event Streaming`: Kafka Topic, Partition, Consumer Group
    * 🔸 `Stream Processing`: Windowing, Watermark

* **[Tier 3: Core] Data Architecture**
  * 💎 `Modern Data Stack`: Data Lakehouse (Delta/Iceberg), dbt

---

## ♾️ Track 5: MLOps Engineer (운영의 지배자)

**전체 ML 생명 주기를 자동화하고 운영 효율을 극대화합니다.**

* **[Tier 1: Core] Automation Core**
  * 🔹 `Docker & Registry` : Image Tagging, Registry 관리
  * 🔹 `CI/CD Pipelines` : GitHub Actions Runner, Test Automation
  * 🔹 `Model Logging` : MLflow/WandB Log Param & Metric

* **[Tier 2: Branching Point] 운영 집중 분야**
  * **Option 1: FinOps (비용 최적화)**
    * 🔸 `Resource Mgmt`: GPU Quota, Spot Instance 활용
    * 🔸 `IaC`: Terraform State, Module, Provider
  * **Option 2: Model Health (품질 모니터링)**
    * 🔸 `Drift Detection`: Covariate Shift, Label Shift 감지
    * 🔸 `Observability`: Prometheus Exporter, Grafana Dashboard

* **[Tier 3: Core] Monitoring Mastery**
  * 💎 `Continuous Training`: 재학습(Retraining) Trigger 파이프라인 설계

---

## 🗺️ Summary Map (Visual Overview)
```
root/
│
├── 🏁 Tier 0: The Origin
│   ├── 🐍 Python Mastery
│   │   ├── 🔹 Syntax & Types
│   │   ├── 🔹 Data Structure Core
│   │   └── 🔹 OOP & Functional
│   ├── ♾️ DevOps Foundations
│   │   ├── 🔹 Linux CLI
│   │   └── 🔹 Git Version Control
│   └── 📐 Math & Logic
│       └── 🔹 Linear Algebra & Statistics
│
├── 🛠️ Track 1: AI Engineer 
│   ├── 📦 Tier 1: System Foundation (FastAPI, Docker, Async)
│   ├── 🌿 Tier 2: Branching Point
│   │   ├── 🔸 Option 1: Serving Specialist (ONNX, TensorRT, Triton)
│   │   └── 🔸 Option 2: App Architect (DB Design, Redis, MQ)
│   └── 💎 Tier 3: Infrastructure Mastery (K8s, GPU Scaling)
│
├── 🧠 Track 2: AI Modeler / Researcher 
│   ├── 🚂 Tier 1: Deep Learning Engine (PyTorch, AutoGrad, Training Loop)
│   ├── 🌿 Tier 2: Branching Point
│   │   ├── 🔸 Option 1: Vision Sage (CNN, YOLO, Diffusion)
│   │   └── 🔸 Option 2: Language Sage (Transformer, Tokenization, PEFT)
│   └── 💎 Tier 3: Advanced Training (DDP, FSDP, Mixed Precision)
│
├── ⚡ Track 3: LLM Application Engineer 
│   ├── 🔗 Tier 1: Context Integration (Prompting, CoT, Vector DB)
│   ├── 🌿 Tier 2: Branching Point
│   │   ├── 🔸 Option 1: Agentic Workflow (ReAct, Tool Use, LangGraph)
│   │   └── 🔸 Option 2: Reliability & Eval (Adv-RAG, RAGAS, Chunking)
│   └── 💎 Tier 3: Production Excellence (LLMOps, A/B Testing)
│
├── 🏗️ Track 4: Data Engineer 
│   ├── 🌊 Tier 1: Data Flow (SQL, Data Modeling, Airflow)
│   ├── 🌿 Tier 2: Branching Point
│   │   ├── 🔸 Option 1: Big Data Master (Spark, MapReduce)
│   │   └── 🔸 Option 2: Real-time Master (Kafka, Stream Processing)
│   └── 💎 Tier 3: Data Architecture (Lakehouse, dbt)
│
└── ♾️ Track 5: MLOps Engineer 
    ├── 🤖 Tier 1: Automation Core (CI/CD, MLflow/WandB)
    ├── 🌿 Tier 2: Branching Point
    │   ├── 🔸 Option 1: FinOps (Terraform, Resource Mgmt)
    │   └── 🔸 Option 2: Model Health (Drift Detection, Observability)
    └── 💎 Tier 3: Monitoring Mastery (Continuous Training)
```