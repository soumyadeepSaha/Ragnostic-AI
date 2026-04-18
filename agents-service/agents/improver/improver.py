from fastapi import APIRouter
from pydantic import BaseModel
from llm.ollama_client import generate

router = APIRouter()

class ImproveInput(BaseModel):
    query: str
    answer: str
    feedback: str


@router.post("/improve")
def improve(i: ImproveInput):
    prompt = f"""
    Improve the answer based on feedback.

    Question: {i.query}

    Current Answer:
    {i.answer}

    Feedback:
    {i.feedback}

    Provide a better, more accurate answer.
    """

    improved = generate(prompt)

    return {"answer": improved}