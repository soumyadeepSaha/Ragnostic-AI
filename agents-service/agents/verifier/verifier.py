# agents/verifier/verifier.py

from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate

router = APIRouter()

class VerifyInput(BaseModel):
    query: str
    answer: str

@router.post("/")
def verify(v: VerifyInput):
    prompt = f"""
    Check if the answer correctly addresses the question.

    Question: {v.query}
    Answer: {v.answer}

    Respond ONLY with:
    VALID or INVALID
    """

    verdict = generate(prompt)

    if "INVALID" in verdict:
        return {"status": "RETRY"}

    return {"status": "OK", "final_answer": v.answer}