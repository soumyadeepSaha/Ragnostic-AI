# Ragnostic-AI
Inspired by controllable RAG architectures, I designed a hybrid multi-agent system with extended capabilities

# 🚀 Ragnostic AI

Ragnostic AI is a controllable multi-agent Generative AI system that dynamically switches between Retrieval-Augmented Generation (RAG) and RAG-less reasoning.

## 🧠 Features
- Hybrid RAG + RAG-less architecture
- Multi-agent system (Planner, Retriever, Reasoner, Verifier)
- MCP-style orchestration
- Verification loop to reduce hallucination
- Plugin-ready API architecture

## 🏗️ Architecture
User → Gateway → Planner → (RAG / RAG-less) → Verifier → Response

## ⚙️ Tech Stack
- Node.js (Gateway)
- Python FastAPI (Agents)
- Ollama (LLM)
- FAISS (Vector DB - upcoming)
- Prometheus + Grafana (observability - upcoming)

## 🚀 Run
```bash
uvicorn main:app --reload
node gateway/server.js# 🚀 Ragnostic AI

Ragnostic AI is a controllable multi-agent Generative AI system that dynamically switches between Retrieval-Augmented Generation (RAG) and RAG-less reasoning.

## 🧠 Features
- Hybrid RAG + RAG-less architecture
- Multi-agent system (Planner, Retriever, Reasoner, Verifier)
- MCP-style orchestration
- Verification loop to reduce hallucination
- Plugin-ready API architecture

## 🏗️ Architecture
User → Gateway → Planner → (RAG / RAG-less) → Verifier → Response

## ⚙️ Tech Stack
- Node.js (Gateway)
- Python FastAPI (Agents)
- Ollama (LLM)
- FAISS (Vector DB - upcoming)
- Prometheus + Grafana (observability - upcoming)

## 🚀 Run
```bash
uvicorn main:app --reload
node gateway/server.js
