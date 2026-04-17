# 🧪 ThunderClient Testing - Quick Visual Guide

## 📋 Files You Need

1. **ThunderClient_Collection.json** - Import this into ThunderClient
2. **HOW_TO_TEST_IN_THUNDERCLIENT.md** - Step-by-step testing guide  
3. **THUNDERCLIENT_TESTING_GUIDE.md** - Request examples & expected responses
4. **CONFIG_EXAMPLES.js** - Configuration reference
5. **gateway/config.js** - The actual toggle file

---

## 🎬 TL;DR - Quick Start (3 minutes)

### Step 1: Start Services
```bash
# Terminal 1
cd agents-service && python -m uvicorn main:app --port 8000

# Terminal 2  
cd gateway && npm start
```

### Step 2: Import Collection in ThunderClient
- Open ThunderClient
- Click Collections menu
- Import `ThunderClient_Collection.json`

### Step 3: Test REST Mode
- Edit `gateway/config.js`:
  ```javascript
  module.exports = { USE_MCP: false };
  ```
- Restart gateway
- In ThunderClient: Run all tests under "🔵 REST Mode Tests"

### Step 4: Switch to MCP Mode
- Edit `gateway/config.js`:
  ```javascript
  module.exports = { USE_MCP: true };
  ```
- Restart gateway
- In ThunderClient: Run all tests under "🟢 MCP Mode Tests"

### Step 5: Compare Results
- Look at response differences
- Notice `/mcp` endpoint vs individual endpoints
- Check timing differences

---

## 🔀 Architecture Visualization

```
┌─────────────────────────────────────────────────────────┐
│                    ThunderClient                        │
│              (Send HTTP Requests)                       │
└────────────┬────────────────────────┬──────────────────┘
             │                        │
        REST mode              MCP mode
        USE_MCP: false        USE_MCP: true
             │                        │
    ┌────────▼──────────┐    ┌───────▼─────────────┐
    │  Gateway Port 3000 │    │  Gateway Port 3000  │
    │  /query endpoint   │    │  /query endpoint    │
    └────────┬──────────┘    └───────┬─────────────┘
             │                       │
    ┌────────▼──────────────┐    ┌──▼──────────────────┐
    │ Orchestrator.js       │    │ Orchestrator.js     │
    │ (REST routing)        │    │ (MCP routing)       │
    │                       │    │                     │
    │ Calls:                │    │ Calls:              │
    │ - /planner/           │    │ - /mcp (action:     │
    │ - /reason/            │    │   planner)          │
    │ - /verify/            │    │ - /mcp (action:     │
    │                       │    │   reason)           │
    └────────┬──────────────┘    │ - /mcp (action:     │
             │                    │   verify)           │
    ┌────────▼──────────────┐    └──┬──────────────────┘
    │ Agents Service        │       │
    │ Port 8000             │       │
    │                       │    ┌──▼──────────────────┐
    │ /planner/             │    │ MCP Dispatcher      │
    │ /reason/              │    │ /mcp endpoint       │
    │ /retrieve/            │    │                     │
    │ /verify/              │    │ Maps action to:     │
    │ /tool/                │    │ - /planner/         │
    │                       │    │ - /reason/          │
    └───────────────────────┘    │ - /verify/          │
                                 │ - /retrieve/        │
                                 │ - /tool/            │
                                 └─────────────────────┘
```

---

## 📊 Request/Response Comparison

### REST Mode
```
REQUEST:
POST http://localhost:3000/query
{
  "query": "Calculate 5 + 3"
}

GATEWAY CALLS (visible in logs):
POST /planner/ → {"action": "TOOL"}
POST /tool/ → {"result": "8"}
POST /verify/ → {"verified": true}

RESPONSE:
{
  "result": "8"
}
```

### MCP Mode
```
REQUEST (same as above):
POST http://localhost:3000/query
{
  "query": "Calculate 5 + 3"
}

GATEWAY CALLS (visible in logs):
POST /mcp {"action": "planner", ...} → {"action": "planner", "result": {"action": "TOOL"}}
POST /mcp {"action": "tool", ...} → {"action": "tool", "result": {"result": "8"}}
POST /mcp {"action": "verify", ...} → {"action": "verify", ...}

RESPONSE (same format):
{
  "result": "8"
}
```

---

## 🎯 Key Testing Points

### 1. Gateway Query Endpoint (Both Modes)
- **URL:** `http://localhost:3000/query`
- **Method:** POST
- **Body:** `{ "query": "..." }`
- **Expected:** 200 OK, result in response
- **Time:** 3-30s depending on query

### 2. Direct REST Agents (REST Mode Only)
- **URLs:** `/planner/`, `/reason/`, `/retrieve/`, `/verify/`, `/tool/`
- **Method:** POST
- **Note:** Not accessible in MCP mode (requests go through /mcp)

### 3. MCP Dispatcher (MCP Mode Only)
- **URL:** `http://localhost:8000/mcp`
- **Method:** POST
- **Body:** `{ "action": "...", "input": {...} }`
- **Response:** `{ "action": "...", "result": {...} }`

### 4. Health Checks
- **URL:** `http://localhost:8000/` (agents service)
- **URL:** `http://localhost:8000/openapi.json` (API docs)
- **URL:** `http://localhost:3000/` (gateway health)

---

## ⚡ Performance Comparison

### Math Query: "Calculate 15 + 25"

**REST Mode:**
- Gateway (0.1s) → Planner (0.5s) → Tool (0.2s) → Verify (0.1s) = **~0.9s**

**MCP Mode:**
- Gateway (0.1s) → MCP /planner (0.5s) → MCP /tool (0.2s) → MCP /verify (0.1s) = **~0.9s**

**Result:** Should be identical (MCP adds minimal overhead)

---

## 📝 Testing Checklist

### REST Mode ✅
- [ ] Gateway query endpoint works
- [ ] Direct /planner/ call works
- [ ] Direct /reason/ call works
- [ ] Direct /retrieve/ call works
- [ ] Direct /tool/ call works
- [ ] Direct /verify/ call works
- [ ] Query routing works (follows decision tree)

### MCP Mode ✅
- [ ] Gateway query endpoint works
- [ ] /mcp endpoint responds
- [ ] MCP planner action works
- [ ] MCP reason action works
- [ ] MCP retrieve action works
- [ ] MCP tool action works
- [ ] MCP verify action works
- [ ] Response format is wrapped: `{ "action": "...", "result": {...} }`

### Switching ✅
- [ ] Config change from REST to MCP works
- [ ] Config change from MCP to REST works
- [ ] Gateway restart applies changes
- [ ] Services don't need restart
- [ ] Both modes produce same results

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 404 on /mcp | MCP mode disabled or route not registered | Check config.js, restart gateway |
| Connection refused | Services not running | Start FastAPI and Gateway |
| Timeout (30s+) | FAISS retrieval or LLM slow | Normal - retrieval takes time |
| 500 errors | Ollama down | Expected - system uses mock LLM |
| Different results REST vs MCP | Caching or timing issues | Verify identical inputs |

---

## 🎓 What You're Testing

1. **Protocol Switching:** Can toggle between REST and MCP modes
2. **Agent Isolation:** Each agent works independently
3. **Request Routing:** Queries route to correct agents
4. **Response Format:** Responses match expected schema
5. **Performance:** Timing is reasonable
6. **Parity:** Same inputs produce same outputs in both modes

---

## 📚 Next Steps

1. Import `ThunderClient_Collection.json`
2. Read `HOW_TO_TEST_IN_THUNDERCLIENT.md`
3. Start services
4. Run REST mode tests
5. Switch config to MCP
6. Run MCP mode tests
7. Compare results
8. Celebrate! 🎉
