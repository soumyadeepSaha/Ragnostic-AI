from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate
import json

router = APIRouter()

class Query(BaseModel):
    query: str


@router.post("/")
def planner(q: Query):

    prompt = f"""
You are a planning agent.

Break the query into steps.

Query:
{q.query}

Available actions:
- retrieve (use external knowledge)
- reason (explain or analyze)
- tool (calculation or external action)

Respond ONLY in JSON:

{{
  "steps": [
    {{"action": "retrieve", "description": "..."}},
    {{"action": "reason", "description": "..."}}
  ]
}}
"""

    result = generate(prompt)

    try:
        plan = json.loads(result)
    except:
        # fallback to single-step
        plan = {
            "steps": [
                {"action": "reason", "description": "fallback"}
            ]
        }

    return plan