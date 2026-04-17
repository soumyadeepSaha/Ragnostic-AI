const axios = require("axios");
const { USE_MCP } = require("../config");

const PYTHON_BASE = "http://localhost:8000";
const MCP_URL = "http://localhost:8000/mcp";

// 🔹 Generic call wrapper (REST / MCP switch)
async function callService(action, payload) {
  if (USE_MCP) {
    const res = await axios.post(MCP_URL, {
      action,
      input: payload,
    });

    return res.data.result;
  } else {
    const urlMap = {
      planner: "/planner/",
      retrieve: "/retrieve/",
      reason: "/reason/",
      verify: "/verify/",
      tool: "/tool/",
    };

    const res = await axios.post(
      `${PYTHON_BASE}${urlMap[action]}`,
      payload
    );

    return res.data;
  }
}
// 🔹 Main orchestrator
exports.handleQuery = async (query) => {
  try {
    // Step 1: Planner
    const plan = await callService("planner", { query });
    const action = plan.action;

    // Step 2: Execute based on action
    const actionMap = {
      RAG: "retrieve",
      REASON: "reason",
      TOOL: "tool",
    };

    const selectedAction = actionMap[action] || "reason";

    const response = await callService(selectedAction, { query });

    // Step 3: Verify
    const verify = await callService("verify", {
      query,
      answer: response.answer,
    });

    // Step 4: Retry logic
    if (verify.status === "RETRY") {
      console.log("Retry triggered → falling back to RAG");

      const retry = await callService("retrieve", { query });
      return retry.answer;
    }

    return verify.final_answer;
  } catch (error) {
    console.error("Orchestrator Error:", error.message);
    throw new Error("Failed to process query");
  }
};