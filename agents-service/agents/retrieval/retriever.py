# agents/retrieval/retriever.py

from fastapi import APIRouter
from pydantic import BaseModel
from agents.retrieval.vector_store import vector_store
from llm.ollama_client import generate

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/")
def retrieve(q: Query):
    docs = vector_store.search(q.query)

    context = "\n".join(docs)

    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {q.query}
    """

    answer = generate(prompt)

    return {"answer": answer}