from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/")
def planner(q: Query):
    # Check if query is asking for calculations
    query_lower = q.query.lower()
    if any(word in query_lower for word in ["calculate", "math", "+", "-", "*", "/", "add", "subtract", "multiply", "divide", "sum", "total"]):
        return {"action": "TOOL"}
    
    # Otherwise use reasoning for general knowledge questions
    prompt = f"""Respond with ONLY one word: RAG or REASON

Query: {q.query}

RAG = needs external knowledge/documents
REASON = general knowledge/reasoning
"""

    decision = generate(prompt).strip().upper()
    
    # Simple binary choice
    if "RAG" in decision and "REASON" not in decision:
        return {"action": "RAG"}
    else:
        return {"action": "REASON"}