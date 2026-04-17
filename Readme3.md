# 🧠 Ragnostic AI - Intelligent Multi-Agent System

An intelligent agent system that orchestrates multiple specialized AI agents to handle different types of queries. It uses a smart routing system to decide whether to retrieve documents, use pure reasoning, or execute tools based on the query type.

## 📋 Table of Contents
- [What is Ragnostic AI?](#what-is-ragnostic-ai)
- [Architecture](#-architecture)
- [Core Features](#-core-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [How Each Agent Works](#-how-each-agent-works)
- [Query Flow Examples](#-query-flow-examples)
- [Setup & Running](#-setup--running)
- [Current Status](#-current-status)
- [Future Enhancements](#-future-enhancements)

---

## What is Ragnostic AI?

**Ragnostic AI** is a production-ready foundation for an intelligent agent system that demonstrates:
- ✅ Microservices architecture with independent services
- ✅ Multi-agent AI orchestration with specialized roles
- ✅ Intelligent query routing based on query semantics
- ✅ Local LLM inference with Ollama
- ✅ RAG (Retrieval-Augmented Generation) with FAISS vector store
- ✅ Response verification to prevent hallucinations
- ✅ Tool execution capabilities for calculations

Think of it as a **multi-agent AI system** where each agent is specialized for a specific task, and a planner decides which agent should handle each query.

---

## 🏗️ Architecture

```
User Query (Port 3000)
    ↓
Node.js Gateway
    ↓
Planner Agent (Ollama decides routing)
    ├→ RAG (Retrieval-Augmented Generation)
    ├→ REASON (Pure LLM reasoning)
    └→ TOOL (Execute calculations/tools)
    ↓
Verifier Agent (Quality & hallucination check)
    ↓
Final Response
```

**Core Flow:**
```
User → Gateway → Planner → (RAG / REASON / TOOL) → Verifier → Response
```

---

## 🎯 Core Features

### 1. **Smart Query Routing** (Planner Agent)
The planner uses Ollama LLM to intelligently route queries to the right agent:

- **TOOL Routes** → For calculations ("calculate 15 + 25" → Result: 40)
- **RAG Routes** → For document-based questions (retrieves relevant info from vector store)
- **REASON Routes** → For general knowledge (pure LLM reasoning without documents)

**How it works:**
- Checks for calculation keywords: `+`, `-`, `*`, `/`, "calculate", "math"
- Uses Ollama to decide between RAG vs REASON for other queries
- Supports flexible routing based on query semantics

### 2. **Retrieval-Augmented Generation (RAG)**
- Uses **FAISS vector store** for semantic document search
- Embeds documents and queries using `sentence-transformers/all-MiniLM-L6-v2`
- Retrieves relevant documents before passing to LLM
- Great for knowledge bases and document Q&A

### 3. **LLM Reasoning Agent**
- Direct reasoning without document retrieval
- Uses Ollama (llama3 model) for inference
- Good for general knowledge questions
- Generates detailed, comprehensive responses

### 4. **Tool Agent** 🧮
- Executes calculations and tools
- Supports math expressions: `15 + 25`, `100 * 2`, etc.
- Extensible for database queries, API calls, etc.
- Routes calculation queries instantly (~3-4 seconds)

### 5. **Verifier Agent** ✓
- Checks response quality and factual accuracy
- Prevents hallucinations
- Can trigger retries if answer is unreliable
- Validates before returning final response

---

## 📊 Technology Stack

| Component | Technology | Port | Purpose |
|-----------|-----------|------|---------|
| **Gateway** | Node.js + Express | 3000 | API entry point, orchestration |
| **Agent Service** | FastAPI + Python | 8000 | Runs all AI agents |
| **LLM** | Ollama + llama3 | 11434 | Language model inference |
| **Vector DB** | FAISS | (in-memory) | Document embeddings storage |
| **Embeddings** | sentence-transformers | (built-in) | Text embeddings |
| **Monitoring** | Prometheus | (in-progress) | Request metrics |

---

## 📁 Project Structure

```
Ragnostic-AI/
├── gateway/                    # Node.js API Gateway
│   ├── server.js              # Express app, metrics
│   ├── routes/query.js         # /query endpoint
│   └── services/orchestrator.js # Query orchestration
│
├── agents-service/            # Python FastAPI service
│   ├── main.py               # FastAPI app, router registration
│   ├── agents/
│   │   ├── planner/          # Smart routing agent ⭐
│   │   ├── reasoning/        # LLM reasoning agent
│   │   ├── retrieval/        # RAG agent (FAISS)
│   │   ├── tool/             # Tool execution agent
│   │   └── verifier/         # Quality verification agent
│   ├── llm/
│   │   └── ollama_client.py   # Ollama API interface
│   └── config/settings.py     # Configuration
│
└── docker-compose.yml         # Docker orchestration
```

---

## 🚀 How Each Agent Works

### **Planner** (`/planner/`) ⭐
Intelligent query router that decides which agent handles the query.

```python
Input:  {"query": "calculate 10 + 5"}
Output: {"action": "TOOL"}

Input:  {"query": "what is AI?"}
Output: {"action": "REASON"}

Input:  {"query": "find documents about XYZ"}
Output: {"action": "RAG"}
```

**Logic:**
- Keyword-based detection for TOOL (calculations)
- LLM-based decision for RAG vs REASON (general queries)

### **Retrieval** (`/retrieve/`) 📚
Retrieval-Augmented Generation agent.

```python
Input:  {"query": "what is in the document?"}
Output: {"answer": "Retrieved documents + context from FAISS"}
```

**Process:**
1. Embeds query using sentence transformers
2. Searches FAISS vector store
3. Returns relevant documents + LLM answer

### **Reasoning** (`/reason/`) 💭
Pure LLM reasoning agent without retrieval.

```python
Input:  {"query": "what is machine learning?"}
Output: {"answer": "Detailed LLM-generated response..."}
```

**Process:**
1. Sends query to Ollama llama3
2. Generates comprehensive answer
3. Returns full response

### **Tool** (`/tool/`) 🧮
Tool execution agent for calculations and operations.

```python
Input:  {"query": "calculate 15 + 25"}
Output: {"answer": "Result: 40"}
```

**Capabilities:**
- Math expressions: `+`, `-`, `*`, `/`
- Extensible for DB queries, APIs, etc.

### **Verifier** (`/verify/`) ✓
Response quality verification agent.

```python
Input:  {"query": "...", "answer": "..."}
Output: {"status": "OK", "final_answer": "..."}
```

**Process:**
1. Checks response validity
2. Detects hallucinations
3. Can return "RETRY" to trigger RAG fallback

---

## 📊 Query Flow Examples

### Example 1: General Knowledge Question

**Query:** `"What is machine learning?"`

```
1. User → Gateway /query endpoint
2. Planner → "This needs REASON (general knowledge)"
3. Reasoning Agent → Calls Ollama llama3
4. Ollama → Generates detailed response
5. Verifier → Validates response quality
6. Gateway → Returns final answer to user

Performance: ~13.8 seconds end-to-end
```

**Sample Response:**
```
"Machine learning is a subfield of artificial intelligence that enables computers 
to learn and improve their performance on a task without being explicitly programmed, 
by recognizing patterns and making predictions based on data."
```

---

### Example 2: Calculation Query

**Query:** `"Calculate 15 + 25"`

```
1. User → Gateway /query
2. Planner → Detects "+" keyword → Routes to TOOL
3. Tool Agent → Evaluates expression → Result: 40
4. Verifier → Confirms valid answer
5. Gateway → Returns result instantly

Performance: ~3.8 seconds
```

**Response:**
```json
{"result": "Result: 40"}
```

---

### Example 3: Document Retrieval

**Query:** `"Tell me about company history"`

```
1. User → Gateway /query
2. Planner → Routes to REASON (no specific docs)
3. Reasoning Agent → Generates answer from general knowledge
4. Verifier → Validates
5. Gateway → Returns response

Performance: ~50+ seconds (full reasoning)
```

---

## ⚙️ Setup & Running

### Prerequisites
- Node.js 16+
- Python 3.8+
- Ollama (for LLM)

### Installation

1. **Install dependencies:**
```bash
# Python dependencies
cd agents-service
pip install -r requirements.txt

# Node dependencies
cd ../gateway
npm install
```

2. **Start Ollama:**
```bash
# Run with CPU only (stable)
$env:OLLAMA_CUDA_VISIBLE_DEVICES = ''
& 'C:\Users\dante\AppData\Local\Programs\Ollama\ollama.exe' serve

# Or with GPU (CUDA)
$env:OLLAMA_CUDA_VISIBLE_DEVICES = '0'
& 'C:\Users\dante\AppData\Local\Programs\Ollama\ollama.exe' serve
```

3. **Start Agent Service:**
```bash
cd agents-service
uvicorn main:app --port 8000 --reload
```

4. **Start Gateway:**
```bash
cd gateway
node server.js
```

### Test the System

```bash
# General knowledge query
curl -X POST http://localhost:3000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"what is machine learning?"}'

# Calculation query
curl -X POST http://localhost:3000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"calculate 15 + 25"}'
```

---

## 🏆 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Planner routing | ✅ Working perfectly | Keyword + LLM-based decisions |
| Ollama integration | ✅ Running on CPU | Stable, reliable inference |
| Calculation queries | ✅ Fast (3-4s) | Math expressions work |
| LLM reasoning | ✅ Quality responses (13-15s) | Detailed, comprehensive |
| RAG retrieval | ✅ FAISS vector store | Document search working |
| Response verification | ✅ Hallucination checks | Prevents bad responses |
| Full pipeline | ✅ End-to-end working | All agents coordinated |
| Monitoring | 🟡 In progress | Prometheus metrics setup |

---

## 🔮 Future Enhancements

### Step 1: Better Retry Logic
- Verifier can trigger RAG retry on low confidence
- Chain multiple agents for complex queries
- Confidence scoring in responses

### Step 2: Observability
- Prometheus + Grafana dashboards
- Track: request count, RAG vs REASON decisions, retries, latency
- Real-time monitoring of system health

### Step 3: Advanced Retrieval
- Better document chunking strategies
- Hybrid search (keyword + semantic)
- Multi-document ranking

### Step 4: More Tools
- Database query execution
- API integrations
- File operations
- Web search

### Step 5: Plugin System
- Slack bot integration
- REST API for third-party apps
- Custom agent templates

---

## 🧠 Mental Model (Important)

Think of the system like this:

```
Client → Node Gateway → Python Agents Service → Response
```

Each agent is independent and can be scaled separately.

---

## 🏆 Interview Gold

**Q: "Why did you separate services?"**

A: *"To isolate LLM-heavy workloads from API orchestration, improving scalability and enabling independent deployment and optimization. The gateway handles HTTP and orchestration, while the agent service focuses on AI inference."*

---

## 📚 References

- Original inspiration: https://github.com/NirDiamant/controllable-RAG-Agent
- Ollama: https://ollama.ai/
- FAISS: https://github.com/facebookresearch/faiss
- FastAPI: https://fastapi.tiangolo.com/
- Express.js: https://expressjs.com/

---

**Built with ❤️ for intelligent AI systems**
