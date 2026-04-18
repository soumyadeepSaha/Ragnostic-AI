from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate
import re

router = APIRouter()

class VerifyInput(BaseModel):
    query: str
    answer: str


def parse_output(text: str):
    """
    Extract STATUS, CONFIDENCE, REASON safely
    """
    status_match = re.search(r"STATUS:\s*(OK|RETRY)", text, re.IGNORECASE)
    conf_match = re.search(r"CONFIDENCE:\s*(0\.\d+|1\.0)", text)
    reason_match = re.search(r"REASON:\s*(.*)", text, re.IGNORECASE)

    status = status_match.group(1).upper() if status_match else "RETRY"
    confidence = float(conf_match.group(1)) if conf_match else 0.5
    reason = reason_match.group(1).strip() if reason_match else "No reason provided"

    return status, confidence, reason


@router.post("/")
def verify(v: VerifyInput):
    prompt = f"""
You are a strict evaluator.

Evaluate the answer quality.

Question: {v.query}
Answer: {v.answer}

Criteria:
- Correctness
- Relevance
- Logical consistency

Respond STRICTLY in this format:

STATUS: OK or RETRY
CONFIDENCE: number between 0 and 1
REASON: short explanation
"""

    result = generate(prompt)

    status, confidence, reason = parse_output(result)

    return {
        "status": status,
        "confidence": confidence,
        "reason": reason,
        "final_answer": v.answer
    }