import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.retrieval.vector_store import vector_store

docs = [
    "RAG stands for Retrieval Augmented Generation.",
    "LLMs can hallucinate without grounding.",
    "FAISS is used for similarity search.",
    "Microservices architecture improves scalability.",
    "Kafka enables event-driven systems."
]

vector_store.create_index(docs)

print("Vector DB initialized")