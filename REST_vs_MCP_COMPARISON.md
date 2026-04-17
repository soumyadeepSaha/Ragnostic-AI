# 🎯 Complete MCP vs REST Mode Comparison

## 📊 Visual Architecture

### REST MODE (Direct Agent Access)
```
┌────────────────────────────────────────────────────────┐
│             ThunderClient                              │
│        POST /query or direct /planner                  │
└─────────────┬──────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────────────┐
│   Gateway (port 3000)                                  │
│   USE_MCP: false ← Current Setting                     │
└─────────────┬──────────────────────────────────────────┘
              │
              ▼ Routes to individual endpoints
┌──────────────────────────────────────────────────────────┐
│   Agents Service (port 8000)                             │
│                                                          │
│   ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │
│   │ /planner/   │  │ /reason/     │  │ /tool/      │  │
│   │ (route)     │→ │ (reasoning)  │→ │ (execute)   │  │
│   └─────────────┘  └──────────────┘  └─────────────┘  │
│                                                          │
│   ┌──────────────┐  ┌─────────────────────────────┐    │
│   │ /retrieve/   │  │ /verify/                    │    │
│   │ (RAG)        │  │ (hallucination detection)   │    │
│   └──────────────┘  └─────────────────────────────┘    │
│                                                          │
│   REST endpoints - Direct access to agents              │
└──────────────────────────────────────────────────────────┘
```

### MCP MODE (Standardized Protocol)
```
┌────────────────────────────────────────────────────────┐
│             ThunderClient                              │
│        POST /query or /mcp with action                 │
└─────────────┬──────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────────────┐
│   Gateway (port 3000)                                  │
│   USE_MCP: true ← Current Setting                      │
└─────────────┬──────────────────────────────────────────┘
              │
              ▼ Routes to /mcp endpoint
┌────────────────────────────────────────────────────────┐
│   Agents Service (port 8000)                           │
│                                                        │
│   ┌──────────────────────────────────────────────┐    │
│   │              /mcp Endpoint                   │    │
│   │   (MCP Router / Dispatcher)                  │    │
│   └────────────┬─────────────────────────────────┘    │
│                │                                      │
│    ┌───────────┼───────────┬──────────┬──────────┐   │
│    │           │           │          │          │   │
│    ▼           ▼           ▼          ▼          ▼   │
│  /planner/  /reason/    /tool/   /retrieve/  /verify│
│                                                        │
│   MCP dispatcher routes action to correct agent       │
└────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow Comparison

### REST Mode Flow
```
User Request: "What is 5 + 3?"
       │
       ▼
   Gateway /query
       │
       ├─→ Check config: USE_MCP = false
       │
       ├─→ Call callService('planner', {...})
       │   └─→ Direct: POST /planner/
       │       Response: {"action": "TOOL"}
       │
       ├─→ Call callService('tool', {...})
       │   └─→ Direct: POST /tool/
       │       Response: {"result": "8"}
       │
       ├─→ Call callService('verify', {...})
       │   └─→ Direct: POST /verify/
       │       Response: {"verified": true}
       │
       ▼
   Return Response to User
```

### MCP Mode Flow
```
User Request: "What is 5 + 3?"
       │
       ▼
   Gateway /query
       │
       ├─→ Check config: USE_MCP = true
       │
       ├─→ Call callService('planner', {...})
       │   └─→ MCP: POST /mcp
       │       Body: {"action": "planner", "input": {...}}
       │       Response: {"action": "planner", "result": {"action": "TOOL"}}
       │
       ├─→ Call callService('tool', {...})
       │   └─→ MCP: POST /mcp
       │       Body: {"action": "tool", "input": {...}}
       │       Response: {"action": "tool", "result": {"result": "8"}}
       │
       ├─→ Call callService('verify', {...})
       │   └─→ MCP: POST /mcp
       │       Body: {"action": "verify", "input": {...}}
       │       Response: {"action": "verify", "result": {...}}
       │
       ▼
   Return Response to User (same format!)
```

---

## 📋 ThunderClient Test Requests

### Test Set 1: REST Mode Direct Agent Calls

```http
# Test 1.1: Direct Planner
POST http://localhost:8000/planner/
Content-Type: application/json

{
  "query": "What is 5 + 3?"
}

# Response:
{
  "action": "TOOL"
}
```

```http
# Test 1.2: Direct Reason
POST http://localhost:8000/reason/
Content-Type: application/json

{
  "query": "Explain photosynthesis"
}

# Response:
{
  "answer": "Response from mock LLM"
}
```

### Test Set 2: MCP Mode Action-Based Calls

```http
# Test 2.1: MCP Planner
POST http://localhost:8000/mcp
Content-Type: application/json

{
  "action": "planner",
  "input": {
    "query": "What is 5 + 3?"
  }
}

# Response:
{
  "action": "planner",
  "result": {
    "action": "TOOL"
  }
}
```

```http
# Test 2.2: MCP Reason
POST http://localhost:8000/mcp
Content-Type: application/json

{
  "action": "reason",
  "input": {
    "query": "Explain photosynthesis"
  }
}

# Response:
{
  "action": "reason",
  "result": {
    "answer": "Response from mock LLM"
  }
}
```

### Test Set 3: Gateway Query (Works Both Modes)

```http
# Same request works in both REST and MCP modes!
POST http://localhost:3000/query
Content-Type: application/json

{
  "query": "What is machine learning?"
}

# Response (identical in both modes):
{
  "result": "ML is a subset of AI..."
}
```

---

## 🔀 Configuration Toggle

### Current Value in gateway/config.js:
```javascript
module.exports = {
  USE_MCP: true  // ← ACTIVE MODE
};
```

### To Switch to REST:
```javascript
module.exports = {
  USE_MCP: false
};
// Then: npm start (restart gateway)
```

### To Switch to MCP:
```javascript
module.exports = {
  USE_MCP: true
};
// Then: npm start (restart gateway)
```

---

## 📊 Feature Comparison Matrix

| Feature | REST Mode | MCP Mode |
|---------|-----------|----------|
| **Direct Agent Access** | ✅ Yes | ❌ No (through dispatcher) |
| **Query Endpoint** | ✅ Works | ✅ Works |
| **Individual Routes** | ✅ /planner/, /reason/, etc. | ✅ All available in code |
| **MCP Endpoint** | ❌ Not used | ✅ Used for all requests |
| **Response Wrapping** | ❌ Direct | ✅ Wrapped with action |
| **Protocol** | HTTP REST | HTTP with MCP pattern |
| **Configuration** | USE_MCP: false | USE_MCP: true |
| **Latency** | Slightly lower | Slightly higher (negligible) |
| **Standardization** | ❌ Custom routing | ✅ Standardized protocol |

---

## 🎯 Testing Strategy

### Phase 1: Baseline (REST Mode)
1. Set `USE_MCP: false`
2. Test all endpoints work
3. Note response times

### Phase 2: Protocol Switch (MCP Mode)
1. Set `USE_MCP: true`
2. Test same queries
3. Compare response times
4. Verify identical responses

### Phase 3: Validation
1. Test both modes independently
2. Test query routing in both
3. Test error handling in both
4. Verify configuration switching

---

## 📈 Expected Results

### Timing Comparison
```
Query: "Calculate 10 + 20"

REST Mode:
  Gateway (0.1s) → Planner (0.3s) → Tool (0.1s) → Verify (0.1s)
  Total: ~0.6s

MCP Mode:
  Gateway (0.1s) → MCP /planner (0.3s) → MCP /tool (0.1s) → MCP /verify (0.1s)
  Total: ~0.6s

Difference: Negligible (MCP overhead < 5%)
```

### Response Format
```
REST: Direct from agent
{"action": "TOOL"}

MCP: Wrapped response
{"action": "planner", "result": {"action": "TOOL"}}
```

---

## ✅ Success Criteria

- [x] Both modes can be toggled via config.js
- [x] REST mode: Can call agents directly
- [x] MCP mode: All requests go through /mcp
- [x] Query endpoint works in both modes
- [x] Same inputs produce same outputs
- [x] Gateway restarts apply configuration changes
- [x] No service restarts needed (just gateway)
- [x] Response times are comparable
