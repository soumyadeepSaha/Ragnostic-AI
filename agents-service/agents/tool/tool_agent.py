from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Query(BaseModel):
    query: str

@router.post("/")
def tool(q: Query):
    query = q.query.lower()

    # 🧮 Simple calculator tool
    if any(word in query for word in ["calculate", "+", "-", "*", "/"]):
        try:
            expression = query.replace("calculate", "")
            result = eval(expression)
            return {"answer": f"Result: {result}"}
        except:
            return {"answer": "Invalid calculation"}

    # 📊 Dummy DB tool
    if "database" in query:
        return {"answer": "Fetched data from database"}

    return {"answer": "No suitable tool found"}