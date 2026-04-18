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
      improve: "/improve/",
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
  const end = latencyHistogram.startTimer();

  try {
    // 🧠 STEP 1: Planner
    const plannerTimer = plannerLatency.startTimer();
    const plan = await callService("planner", { query });
    plannerTimer();

    const steps = plan.steps || [];

    let finalAnswer = "";
    let context = "";

    // 🧠 STEP 2: Execute steps
    for (const step of steps) {
      const action = step.action;
      decisionCounter.inc({ type: action });

      if (action === "retrieve") {
        const t = retrievalLatency.startTimer();
        const res = await callService("retrieve", { query });
        t();

        context = res.context || "";
        finalAnswer = res.answer;

      } else if (action === "reason") {
        const t = reasoningLatency.startTimer();
        const res = await callService("reason", {
          query: finalAnswer || query,
        });
        t();

        finalAnswer = res.answer;

      } else if (action === "tool") {
        const t = toolLatency.startTimer();
        const res = await callService("tool", { query });
        t();

        finalAnswer = res.answer;
      }
    }

    // 🧠 STEP 3: Verify (FIXED)
    const verifyTimer = verifierLatency.startTimer();
    const verify = await callService("verify", {
      query,
      answer: finalAnswer,        // ✅ FIXED
      context: context || "",     // ✅ FIXED
    });
    verifyTimer();

    confidenceGauge.set(verify.confidence || 0.5);

    // 🧠 STEP 4: Self-correction
    if (verify.status === "RETRY" || verify.confidence < 0.6) {
      console.log(
        `Low confidence (${verify.confidence}) → attempting self-correction`
      );

      retryCounter.inc();

      // 🔥 Improve
      const improved = await callService("improve", {
        query,
        answer: finalAnswer,       // ✅ FIXED
        feedback: verify.reason,
      });

      // 🔥 Re-verify
      const reverifyTimer = verifierLatency.startTimer();
      const reverify = await callService("verify", {
        query,
        answer: improved.answer,
        context: context || "",   // ✅ IMPORTANT
      });
      reverifyTimer();

      confidenceGauge.set(reverify.confidence || 0.5);

      // 🔥 Choose best
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
    end();
  }
};