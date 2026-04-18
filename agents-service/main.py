import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

from agents.planner.planner import router as planner_router
from agents.retrieval.retriever import router as retriever_router
from agents.reasoning.reasoning import router as reasoning_router
from agents.verifier.verifier import router as verifier_router
from agents.tool.tool_agent import router as tool_router
from mcp.mcp_server import router as mcp_router
from agents.improver.improver import router as improver_router
app = FastAPI(title="Ragnostic Agent Service")

# Prometheus Metrics
request_count = Counter('agent_requests_total', 'Total requests', ['endpoint'])
request_duration = Histogram('agent_request_duration_seconds', 'Request duration', ['endpoint'])

# Middleware for metrics
@app.middleware("http")
async def add_metrics(request, call_next):
    endpoint = request.url.path
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    request_count.labels(endpoint=endpoint).inc()
    request_duration.labels(endpoint=endpoint).observe(duration)
    return response

app.include_router(retriever_router, prefix="/retrieve", tags=["retrieval"])
app.include_router(planner_router, prefix="/planner", tags=["planner"])
app.include_router(reasoning_router, prefix="/reason", tags=["reasoning"])
app.include_router(verifier_router, prefix="/verify", tags=["verifier"])
app.include_router(tool_router, prefix="/tool", tags=["tool"])
app.include_router(mcp_router)

app.include_router(improver_router)

@app.get("/")
def root():
    return {"status": "ok", "service": "agents-service"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain; charset=utf-8")
