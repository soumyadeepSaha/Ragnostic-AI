from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/")
def planner(q: Query):
    prompt = f"""
    Decide how to answer the query.

    Options:
    - RAG (needs external knowledge)
    - REASON (general reasoning)
    - TOOL (calculation, database, or external action)

    Query: {q.query}

    Answer ONLY one: RAG / REASON / TOOL
    """

    decision = generate(prompt)

    if "TOOL" in decision:
        return {"action": "TOOL"}
    elif "RAG" in decision:
        return {"action": "RAG"}
    return {"action": "REASON"}