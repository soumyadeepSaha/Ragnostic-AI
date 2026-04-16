from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class VerifyInput(BaseModel):
    query: str
    answer: str

@router.post("/")
def verify(v: VerifyInput):
    # simple version
    return {"final_answer": v.answer}