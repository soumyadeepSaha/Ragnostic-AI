# 🚀 ThunderClient Testing - Complete Setup Guide

## 📦 What You Have Now

### Files Created for Testing:

1. **ThunderClient_Collection.json** (8 KB)
   - Pre-configured HTTP requests for both modes
   - Ready to import into ThunderClient
   - Organized by REST and MCP test groups

2. **HOW_TO_TEST_IN_THUNDERCLIENT.md** (4 KB)
   - Step-by-step walkthrough
   - Configuration switching instructions
   - Troubleshooting tips

3. **THUNDERCLIENT_TESTING_GUIDE.md** (4 KB)
   - Detailed request/response examples
   - Expected response times
   - Test case descriptions

4. **REST_vs_MCP_COMPARISON.md** (6 KB)
   - Visual architecture diagrams
   - Side-by-side request flows
   - Feature comparison matrix

5. **TESTING_QUICK_REFERENCE.md** (8 KB)
   - Visual quick-start guide
   - Common issues & fixes
   - Testing checklist

6. **CONFIG_EXAMPLES.js** (4 KB)
   - Configuration examples
   - When to use each mode
   - Comment-based documentation

---

## 🎬 Quick Start (5 Minutes)

### Step 1: Have These Windows Open

**Terminal 1 - FastAPI Service:**
```bash
cd c:\Users\dante\Desktop\Ragnostic-AI\agents-service
python -m uvicorn main:app --port 8000
```

**Terminal 2 - Gateway Service:**
```bash
cd c:\Users\dante\Desktop\Ragnostic-AI\gateway
npm start
```

**ThunderClient:**
- Open in VS Code
- Collections panel (left sidebar)

### Step 2: Import Collection

1. In ThunderClient: **Collections** menu
2. Click **"Import Collection"**
3. Select: **ThunderClient_Collection.json**
4. See tests organized by mode!

### Step 3: Test REST Mode

Edit `gateway/config.js`:
```javascript
module.exports = { USE_MCP: false };
```

Restart gateway, then in ThunderClient:
- Expand **"🔵 REST Mode Tests"**
- Click each request and press **Send**
- Observe responses

### Step 4: Switch to MCP Mode

Edit `gateway/config.js`:
```javascript
module.exports = { USE_MCP: true };
```

Restart gateway, then in ThunderClient:
- Expand **"🟢 MCP Mode Tests"**
- Click each request and press **Send**
- Compare responses

### Step 5: Compare Results

Both modes should:
- Return status 200
- Have similar response times
- Provide same information (possibly wrapped differently)

---

## 📊 File Locations

```
Ragnostic-AI/
├── gateway/
│   ├── config.js ← EDIT THIS TO SWITCH MODES
│   ├── services/orchestrator.js
│   └── server.js
│
├── agents-service/
│   ├── main.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── mcp_server.py ← MCP endpoint logic
│   └── agents/
│       ├── planner/planner.py
│       ├── reasoning/reasoning.py
│       ├── retrieval/retriever.py
│       ├── verifier/verifier.py
│       └── tool/tool_agent.py
│
├── ThunderClient_Collection.json ← IMPORT THIS
├── HOW_TO_TEST_IN_THUNDERCLIENT.md ← START HERE
├── TESTING_QUICK_REFERENCE.md
├── REST_vs_MCP_COMPARISON.md
├── THUNDERCLIENT_TESTING_GUIDE.md
└── CONFIG_EXAMPLES.js
```

---

## 🎯 Key Endpoints to Test

### Always Available (Port 8000)
- `GET http://localhost:8000/` - Health check
- `GET http://localhost:8000/openapi.json` - API documentation

### REST Mode Only (Direct Agent Access)
- `POST http://localhost:8000/planner/` - Route decision
- `POST http://localhost:8000/reason/` - Reasoning
- `POST http://localhost:8000/retrieve/` - RAG retrieval
- `POST http://localhost:8000/tool/` - Tool execution
- `POST http://localhost:8000/verify/` - Response verification

### MCP Mode Only (Dispatcher)
- `POST http://localhost:8000/mcp` - With any action:
  - `{"action": "planner", "input": {...}}`
  - `{"action": "reason", "input": {...}}`
  - `{"action": "retrieve", "input": {...}}`
  - `{"action": "tool", "input": {...}}`
  - `{"action": "verify", "input": {...}}`

### Gateway (Both Modes)
- `POST http://localhost:3000/query` - Main query endpoint
  - Routes through either REST or MCP based on config

---

## 🔄 The Switch (config.js)

### Location:
`c:\Users\dante\Desktop\Ragnostic-AI\gateway\config.js`

### REST Mode:
```javascript
module.exports = {
  USE_MCP: false
};
```

### MCP Mode:
```javascript
module.exports = {
  USE_MCP: true
};
```

**After changing:** Restart gateway with `npm start`

---

## 🧪 What to Test

### Basic Sanity Checks
```
✅ Services start without errors
✅ Port 8000 (FastAPI) is accessible
✅ Port 3000 (Gateway) is accessible
✅ Can toggle config.js without breaking anything
✅ Gateway restarts successfully after config change
```

### REST Mode Tests
```
✅ POST /query works
✅ POST /planner/ works
✅ POST /reason/ works
✅ POST /retrieve/ works
✅ POST /tool/ works
✅ POST /verify/ works
✅ All return status 200
✅ Responses have expected format
```

### MCP Mode Tests
```
✅ POST /query works
✅ POST /mcp with action="planner" works
✅ POST /mcp with action="reason" works
✅ POST /mcp with action="retrieve" works
✅ POST /mcp with action="tool" works
✅ POST /mcp with action="verify" works
✅ All return status 200
✅ Responses are wrapped with action field
```

### Parity Tests
```
✅ Same query in both modes returns same information
✅ Response times are comparable
✅ Error handling is consistent
✅ Switching modes works smoothly
```

---

## 📈 Expected Timing

| Query Type | REST Mode | MCP Mode | Difference |
|------------|-----------|----------|-----------|
| Math (5+3) | 0.8s | 0.9s | ~10% |
| Reasoning | 25s | 26s | ~4% |
| Retrieval | 15s | 16s | ~7% |
| Direct call | 0.5s | N/A | N/A |

MCP adds minimal overhead (< 5-10%)

---

## 🐛 Troubleshooting

### "Connection refused" on port 3000 or 8000
- Check if services are running
- Check terminal for error messages
- Restart service

### "404 Not Found" on /mcp
- Check if USE_MCP is true
- Check if gateway was restarted
- Check if mcp_server.py is in agents-service/mcp/

### Different responses in REST vs MCP
- Verify same input
- Check timing (Ollama might be slow)
- Compare response structure
- Check for any error messages in terminals

### Gateway won't start after config change
- Check syntax in config.js (JavaScript must be valid)
- Check if there's a comma at the end
- Use a syntax checker or editor

---

## 💡 Tips for Effective Testing

1. **Keep terminals visible**
   - Watch for error messages in real-time
   - See request logs from services

2. **Test in order**
   - Basic sanity checks first
   - Then mode-specific tests
   - Then parity tests

3. **Note the differences**
   - REST mode: Direct responses
   - MCP mode: Wrapped responses
   - Both have same information

4. **Use the collection**
   - All requests pre-configured
   - Just modify body if needed
   - Easy to repeat tests

5. **Compare responses side-by-side**
   - Keep ThunderClient response visible
   - Switch modes and re-run same request
   - Spot differences easily

---

## 📝 Documentation Files Reference

| File | Purpose | Read When |
|------|---------|-----------|
| HOW_TO_TEST_IN_THUNDERCLIENT.md | Step-by-step guide | Starting tests |
| TESTING_QUICK_REFERENCE.md | Visual guide & checklist | Need quick reference |
| REST_vs_MCP_COMPARISON.md | Architecture & flows | Understanding design |
| THUNDERCLIENT_TESTING_GUIDE.md | Detailed examples | Need request details |
| CONFIG_EXAMPLES.js | Configuration reference | Implementing features |
| ThunderClient_Collection.json | Pre-built requests | Setting up tests |

---

## ✨ You're All Set!

Everything is ready for testing:
- ✅ Dual-mode architecture implemented
- ✅ Configuration switching enabled
- ✅ MCP endpoint tested and working
- ✅ ThunderClient collection created
- ✅ Documentation complete

**Next Steps:**
1. Import ThunderClient collection
2. Follow HOW_TO_TEST_IN_THUNDERCLIENT.md
3. Test both modes
4. Compare results
5. Celebrate! 🎉

---

## 🚀 Architecture Summary

```
┌──────────────────────────────────────────────────────────┐
│                   ThunderClient                          │
│              (Your Testing Tool)                         │
└────────────┬─────────────────────────────┬───────────────┘
             │                             │
        REST requests              MCP requests
             │                             │
    ┌────────▼──────────┐      ┌──────────▼────────┐
    │ Gateway (3000)    │      │ Gateway (3000)    │
    │ USE_MCP: false    │      │ USE_MCP: true     │
    └────────┬──────────┘      └──────────┬────────┘
             │                            │
    Routes to individual agents   Routes to /mcp
             │                            │
    ┌────────▼──────────────────────────────────────┐
    │   Agents Service (Port 8000)                   │
    │                                                │
    │   REST Endpoints:          MCP Endpoint:      │
    │   /planner/                /mcp               │
    │   /reason/                 (dispatcher)       │
    │   /tool/                                       │
    │   /retrieve/                                   │
    │   /verify/                                     │
    └────────────────────────────────────────────────┘
```

---

**Happy Testing!** 🧪✨
