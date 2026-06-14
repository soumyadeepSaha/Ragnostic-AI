# Ragnostic AI - Protocol Mode Testing Guide

## Quick Mode Switching

### ✅ REST Mode
1. Edit `gateway/config.js`:
```javascript
module.exports = {
  USE_MCP: false
};
```

### ✅ MCP Mode
1. Edit `gateway/config.js`:
```javascript
module.exports = {
  USE_MCP: true
};
```

2. Restart the gateway: `npm start` in `gateway/` directory

---

## 🧪 ThunderClient Testing Requests

### BASE URLs
- **Gateway (Query):** `http://localhost:3000`
- **Agents Service (Direct):** `http://localhost:8000`

---

## 📌 Test Case 1: Query Through Gateway (Both Modes)

**Endpoint:** `POST http://localhost:3000/query`

**Request Body:**
```json
{
  "query": "What is 5 + 3?"
}
```

**Expected Responses:**
- REST Mode: Routes to individual endpoints (/planner → /tool → /verify)
- MCP Mode: Routes through /mcp endpoint with action dispatcher

---

## 📌 Test Case 2: Direct MCP Endpoint

**Endpoint:** `POST http://localhost:8000/mcp`

**Request Body:**
```json
{
  "action": "planner",
  "input": {
    "query": "What is machine learning?"
  }
}
```

**Expected Response:**
```json
{
  "action": "planner",
  "result": {
    "action": "RAG"
  }
}
```

---

## 📌 Test Case 3: Direct REST Endpoints

### Test Planner
**Endpoint:** `POST http://localhost:8000/planner/`

**Request Body:**
```json
{
  "query": "Calculate 15 + 25"
}
```

**Expected Response:**
```json
{
  "action": "TOOL"
}
```

### Test Reasoning
**Endpoint:** `POST http://localhost:8000/reason/`

**Request Body:**
```json
{
  "query": "Explain photosynthesis"
}
```

**Expected Response:**
```json
{
  "answer": "Response from mock LLM"
}
```

### Test Retrieval
**Endpoint:** `POST http://localhost:8000/retrieve/`

**Request Body:**
```json
{
  "query": "machine learning basics"
}
```

### Test Verification
**Endpoint:** `POST http://localhost:8000/verify/`

**Request Body:**
```json
{
  "query": "Is this response accurate?",
  "response": "2+2=4"
}
```

### Test Tool Execution
**Endpoint:** `POST http://localhost:8000/tool/`

**Request Body:**
```json
{
  "query": "Calculate 100 / 5"
}
```

---

## 🔀 Comparison: REST vs MCP Mode

| Aspect | REST Mode | MCP Mode |
|--------|-----------|----------|
| **Query Endpoint** | `POST /query` → routes to individual agents | `POST /query` → routes through `/mcp` |
| **Direct Agent Access** | `POST /planner/`, `/reason/`, etc. | `POST /mcp` with action selector |
| **Protocol** | HTTP with individual endpoints | MCP with action dispatcher |
| **Use Case** | Direct agent integration | Standardized protocol interface |

---

## ⚡ Quick Test Sequence

1. **Start FastAPI (agents-service):**
   ```bash
   cd agents-service
   python -m uvicorn main:app --port 8000
   ```

2. **Start Gateway (separate terminal):**
   ```bash
   cd gateway
   npm start
   ```

3. **Test REST Mode:**
   - Set `USE_MCP: false` in config.js
   - Restart gateway
   - POST `http://localhost:3000/query` with test query

4. **Test MCP Mode:**
   - Set `USE_MCP: true` in config.js
   - Restart gateway
   - POST `http://localhost:3000/query` with same test query

5. **Compare Results** in ThunderClient

---

## 📊 Expected Response Times

- **Math Query:** 3-5 seconds (routed to TOOL)
- **Reasoning Query:** 20-30 seconds (calls Ollama)
- **Retrieval Query:** 10-15 seconds (FAISS + LLM)

---

## ✨ Key Differences You'll Notice

**REST Mode:**
- Separate endpoints for each agent
- Can call agents directly without planner
- Lower latency for direct calls

**MCP Mode:**
- Single `/mcp` endpoint for all actions
- Always goes through action dispatcher
- Standardized request/response format
- Better for protocol standardization

-better writes
