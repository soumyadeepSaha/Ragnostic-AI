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
def chunk_text(text, chunk_size=100):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

docs = [
    "Long document about RAG and LLMs..."
]

chunks = []
for doc in docs:
    chunks.extend(chunk_text(doc))


vector_store.create_index(docs)

print("Vector DB initialized")