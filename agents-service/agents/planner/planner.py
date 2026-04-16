from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/")
def planner(q: Query):
    prompt = f"""
    Decide whether the query needs external knowledge.
    Answer ONLY 'RAG' or 'REASON'.

    Query: {q.query}
    """

    decision = generate(prompt)

    if "RAG" in decision:
        return {"action": "RAG"}
    return {"action": "REASON"}