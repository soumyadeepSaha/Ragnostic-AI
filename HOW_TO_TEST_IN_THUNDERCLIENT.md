# 🧪 How to Test MCP vs REST Mode in ThunderClient

## 📥 Import the Collection

1. **Open ThunderClient** in VS Code
2. **Click** Collections → "Import Collection"
3. **Select:** `ThunderClient_Collection.json`
4. **Done!** You'll see all test requests organized by mode

---

## 🔄 Complete Testing Workflow

### **Phase 1: Setup Services** (Do Once)

```bash
# Terminal 1 - Start FastAPI
cd agents-service
python -m uvicorn main:app --port 8000

# Terminal 2 - Start Gateway (when ready)
cd gateway
npm start
```

---

### **Phase 2: Test REST Mode**

**Step 1:** Edit `gateway/config.js`:
```javascript
module.exports = {
  USE_MCP: false  // ← REST mode
};
```

**Step 2:** Restart gateway (Ctrl+C and `npm start`)

**Step 3:** In ThunderClient, run requests under **"🔵 REST Mode Tests"**:
- Click "1. Query (REST Mode)" → Send
- Click "2. Direct Planner (REST)" → Send
- Click "3. Direct Reason (REST)" → Send
- Click "4. Direct Retrieve (REST)" → Send

**Expected:** Each request hits individual endpoints

---

### **Phase 3: Test MCP Mode**

**Step 1:** Edit `gateway/config.js`:
```javascript
module.exports = {
  USE_MCP: true  // ← MCP mode
};
```

**Step 2:** Restart gateway (Ctrl+C and `npm start`)

**Step 3:** In ThunderClient, run requests under **"🟢 MCP Mode Tests"**:
- Click "1. Query (MCP Mode)" → Send
- Click "2. MCP Planner" → Send
- Click "3. MCP Reason" → Send
- Click "4. MCP Retrieve" → Send
- Click "5. MCP Verify" → Send
- Click "6. MCP Tool" → Send

**Expected:** All requests go through `/mcp` endpoint

---

### **Phase 4: Compare Results**

| Test | REST Response | MCP Response | Difference |
|------|--------------|--------------|-----------|
| Query (same request) | Flows through individual agents | Flows through /mcp dispatcher | Should be identical |
| Planner | `{"action": "TOOL"}` | `{"action": "planner", "result": {"action": "TOOL"}}` | MCP wraps response |
| Direct Access | ✅ Can call `/reason/` directly | ❌ Must use `/mcp` with action | Architecture difference |

---

## 📝 Manual Requests (Without Collection)

### **Quick Test: REST Mode**

In ThunderClient, create new request:

```
POST http://localhost:3000/query
Content-Type: application/json

{
  "query": "Calculate 2 + 2"
}
```

**Expected Response:**
```json
{
  "result": "Response from mock LLM"
}
```

---

### **Quick Test: MCP Mode**

Create new request:

```
POST http://localhost:8000/mcp
Content-Type: application/json

{
  "action": "planner",
  "input": {
    "query": "Calculate 2 + 2"
  }
}
```

**Expected Response:**
```json
{
  "action": "planner",
  "result": {
    "action": "TOOL"
  }
}
```

---

## ⚡ Quick Switches in config.js

### REST Mode:
```javascript
module.exports = { USE_MCP: false };
```

### MCP Mode:
```javascript
module.exports = { USE_MCP: true };
```

**Remember:** Restart gateway after changing config!

---

## 🎯 What to Look For

### REST Mode Indicators:
- Multiple calls in orchestrator flow
- Individual endpoint responses
- Can access `/planner/`, `/reason/` directly
- Log shows: `POST /planner/`, `POST /reason/`, etc.

### MCP Mode Indicators:
- Single `/mcp` endpoint call
- Action dispatcher processes request
- Wrapped response format: `{ "action": "...", "result": {...} }`
- Log shows: `POST /mcp`

---

## 🐛 Troubleshooting

**Request times out:**
- Check FastAPI is running on 8000
- Check Gateway is running on 3000
- Ollama might be returning 500 errors (expected - uses mock LLM)

**404 Not Found:**
- Wrong port number
- Endpoint path incorrect
- Service not started

**Connection refused:**
- Services not running
- Check terminals for any error messages

---

## 📊 Expected Performance

| Query | Time | Mode | Notes |
|-------|------|------|-------|
| Math query | 3-5s | Both | Routed to TOOL |
| Reason query | 20-30s | Both | Calls LLM (Ollama) |
| Direct agent | 1-2s | REST only | Direct endpoint call |
| MCP action | 4-30s | MCP only | Through dispatcher |
