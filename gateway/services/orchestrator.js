const axios = require("axios");
const { USE_MCP } = require("../config");

const PYTHON_BASE = "http://localhost:8000";
const MCP_URL = "http://localhost:8000/mcp";

const {
  decisionCounter,
  retryCounter,
  latencyHistogram,
   plannerLatency,
  retrievalLatency,
  reasoningLatency,
  toolLatency,
  verifierLatency,
  confidenceGauge,  
} = require("../metrics");

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
  // ⏱️ Start latency timer
  const end = latencyHistogram.startTimer();

  try {
    // Step 1: Planner
    const plannerTimer = plannerLatency.startTimer();
    const plan = await callService("planner", { query });
    plannerTimer();
    const action = plan.action;

    // 🧠 Track decision
    decisionCounter.inc({ type: action });

    // Step 2: Execute based on action
    const actionMap = {
      RAG: "retrieve",
      REASON: "reason",
      TOOL: "tool",
    };

    const selectedAction = actionMap[action] || "reason";

let response;

if (selectedAction === "retrieve") {
  const t = retrievalLatency.startTimer();
  response = await callService("retrieve", { query });
  t();
} else if (selectedAction === "reason") {
  const t = reasoningLatency.startTimer();
  response = await callService("reason", { query });
  t();
} else {
  const t = toolLatency.startTimer();
  response = await callService("tool", { query });
  t();
}

    // Step 3: Verify
  const verifyTimer = verifierLatency.startTimer();
const verify = await callService("verify", {
  query,
  answer: response.answer,
  context: response.context || "",
});

confidenceGauge.set(verify.confidence|| 0.5);

verifyTimer();

    // Step 4: Retry logic
 if (verify.status === "RETRY" || verify.confidence < 0.6) {
  console.log(
    `Low confidence (${verify.confidence}) → attempting self-correction`
  );

  retryCounter.inc();

  // 🔥 Step 1: Improve answer
  const improved = await callService("improve", {
    query,
    answer: response.answer,
    feedback: verify.reason,
  });

  // 🔥 Step 2: Re-verify improved answer
  const reverifyTimer = verifierLatency.startTimer();
  const reverify = await callService("verify", {
    query,
    answer: improved.answer,
  });
  reverifyTimer();

  // Track improved confidence
  confidenceGauge.set(reverify.confidence || 0.5);

  // 🔥 Step 3: Choose better answer
  if (reverify.confidence > verify.confidence) {
    console.log("Improved answer accepted");
    return improved.answer;
  } else {
    console.log("Improvement failed → fallback to RAG");

    const retry = await callService("retrieve", { query });
    return retry.answer;
  }
}
    return verify.final_answer;
  } catch (error) {
    console.error("Orchestrator Error:", error.message);
    throw new Error("Failed to process query");
  } finally {
    // ⏱️ Stop latency timer
    end();
  }
};