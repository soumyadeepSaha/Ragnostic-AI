# agents-service/mcp/mcp_server.py

from fastapi import APIRouter
from pydantic import BaseModel
import requests

router = APIRouter()

BASE_URL = "http://localhost:8000"

# 🧠 MCP Request Schema
class MCPRequest(BaseModel):
    action: str
    input: dict


# 🔥 Action Registry (extensible)
ACTION_MAP = {
    "planner": "/planner",
    "retrieve": "/retrieve",
    "reason": "/reason",
    "verify": "/verify",
    "tool": "/tool"
}


# 🔹 Generic dispatcher
def dispatch(action: str, payload: dict):
    if action not in ACTION_MAP:
        return {"error": f"Unknown action: {action}"}

    endpoint = ACTION_MAP[action]

    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# 🚀 MCP Entry Point
@router.post("/mcp")
def handle_mcp(req: MCPRequest):
    action = req.action
    payload = req.input

    result = dispatch(action, payload)

    return {
        "action": action,
        "result": result
    }