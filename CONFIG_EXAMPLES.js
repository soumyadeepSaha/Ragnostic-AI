// ⚙️ Ragnostic AI - Configuration Examples

// ========================================
// 🔵 REST MODE (Default)
// ========================================
// All requests go directly to individual agent endpoints
// Perfect for: Direct agent integration, custom routing, agent testing

// gateway/config.js - REST MODE
module.exports = {
  USE_MCP: false  // ← Switch to REST mode
};

// Example request flow in REST mode:
// POST /query
//   ↓ (orchestrator.js)
// POST /planner/  (route decision)
//   ↓
// POST /reason/   (get response)
//   ↓
// POST /verify/   (verify accuracy)
//   ↓
// Response returned to client

// ========================================
// 🟢 MCP MODE (New)
// ========================================
// All requests go through /mcp endpoint
// Perfect for: Standardized protocol, API integration, contract-based design

// gateway/config.js - MCP MODE
module.exports = {
  USE_MCP: true   // ← Switch to MCP mode
};

// Example request flow in MCP mode:
// POST /query
//   ↓ (orchestrator.js)
// POST /mcp { action: "planner", input: {...} }
//   ↓ (mcp_server.py - dispatcher)
// POST /planner/ (internal agent call)
//   ↓
// POST /mcp { action: "reason", input: {...} }
//   ↓ (dispatcher)
// POST /reason/ (internal agent call)
//   ↓
// POST /mcp { action: "verify", input: {...} }
//   ↓ (dispatcher)
// POST /verify/ (internal agent call)
//   ↓
// Response returned to client

// ========================================
// 🔀 How to Switch
// ========================================

// 1. Edit gateway/config.js
// 2. Change USE_MCP value (true or false)
// 3. Restart gateway: npm start
// 4. Done!

// ========================================
// 📊 Side-by-Side Comparison
// ========================================

// REST MODE REQUEST
// POST http://localhost:3000/query
// {
//   "query": "What is AI?"
// }
//
// Response (direct path through agents):
// {
//   "result": "AI is artificial intelligence..."
// }

// MCP MODE REQUEST (same input to gateway)
// POST http://localhost:3000/query
// {
//   "query": "What is AI?"
// }
//
// Internally (gateway calls):
// POST http://localhost:8000/mcp
// {
//   "action": "planner",
//   "input": { "query": "What is AI?" }
// }
//
// Response (same format):
// {
//   "result": "AI is artificial intelligence..."
// }

// ========================================
// 🎯 When to Use Each Mode
// ========================================

// Use REST Mode When:
// ✅ Direct agent access is needed
// ✅ Custom routing logic
// ✅ Agent-specific optimizations
// ✅ Testing individual agents
// ✅ Performance-critical direct calls

// Use MCP Mode When:
// ✅ Standardized API contract required
// ✅ External service integration
// ✅ Protocol standardization needed
// ✅ Multi-protocol support needed
// ✅ Abstract away agent details

// ========================================
// 🔧 Advanced: Environment Variable Option
// ========================================

// Future enhancement - could use environment variables:
// module.exports = {
//   USE_MCP: process.env.USE_MCP === 'true' ? true : false
// };
//
// Then: USE_MCP=true npm start

// ========================================
// 📝 Current Setting
// ========================================

// Check which mode is active:
// 1. Open gateway/config.js
// 2. Look at USE_MCP value
// 3. true = MCP mode (standardized protocol)
// 4. false = REST mode (direct endpoints)

// Current Active: Check the actual config.js file!
