from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/")
def reason(q: Query):
    answer = generate(q.query)
    return {"answer": answer}