import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI

from agents.planner.planner import router as planner_router
from agents.retrieval.retriever import router as retriever_router
from agents.reasoning.reasoning import router as reasoning_router
from agents.verifier.verifier import router as verifier_router
from agents.tool.tool_agent import router as tool_router
from mcp.mcp_server import router as mcp_router

app = FastAPI(title="Ragnostic Agent Service")

app.include_router(retriever_router, prefix="/retrieve", tags=["retrieval"])
app.include_router(planner_router, prefix="/planner", tags=["planner"])
app.include_router(reasoning_router, prefix="/reason", tags=["reasoning"])
app.include_router(verifier_router, prefix="/verify", tags=["verifier"])
app.include_router(tool_router, prefix="/tool", tags=["tool"])
app.include_router(mcp_router)

@app.get("/")
def root():
    return {"status": "ok", "service": "agents-service"}
