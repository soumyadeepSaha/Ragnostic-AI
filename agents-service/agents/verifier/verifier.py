from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate
import re

router = APIRouter()

class VerifyInput(BaseModel):
    query: str
    answer: str
    context: str = ""


def parse_output(text: str):
    """
    Extract STATUS, CONFIDENCE, REASON safely
    """

    status_match = re.search(r"STATUS:\s*(OK|RETRY)", text, re.IGNORECASE)
    conf_match = re.search(r"CONFIDENCE:\s*(0(?:\.\d+)?|1(?:\.0)?)", text)
    reason_match = re.search(r"REASON:\s*(.*)", text, re.IGNORECASE | re.DOTALL)

    status = status_match.group(1).upper() if status_match else "RETRY"

    try:
        confidence = float(conf_match.group(1)) if conf_match else 0.5
    except:
        confidence = 0.5

    reason = reason_match.group(1).strip() if reason_match else "No reason provided"

    return status, confidence, reason


@router.post("/")
def verify(v: VerifyInput):

    has_context = bool(v.context and v.context.strip())

    # 🔥 STRONGER PROMPT (grounded + strict)
    prompt = f"""
You are a STRICT AI evaluator.

Question:
{v.query}

Answer:
{v.answer}
"""

    if has_context:
        prompt += f"""

Context:
{v.context}

STRICT RULES:
- The answer MUST be supported by the context
- If ANY part of the answer is not in the context → RETRY
- If the answer adds extra facts not in context → RETRY
- If the answer contradicts the context → RETRY
"""
    else:
        prompt += """

STRICT RULES:
- The answer must be logically correct
- The answer must be relevant to the question
"""

    prompt += """

Evaluate:
1. Correctness
2. Relevance
3. Logical consistency

Respond EXACTLY in this format:

STATUS: OK or RETRY
CONFIDENCE: number between 0 and 1
REASON: short explanation
"""

    result = generate(prompt)

    status, confidence, reason = parse_output(result)

    # 🔥 Extra safety: enforce stricter grounding penalty
    if has_context and confidence < 0.4:
        status = "RETRY"

    return {
        "status": status,
        "confidence": confidence,
        "reason": reason,
        "final_answer": v.answer
    }