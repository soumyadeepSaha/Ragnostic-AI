const client = require("prom-client");

const register = new client.Registry();

// 🔢 Total requests
const requestCounter = new client.Counter({
  name: "ragnostic_requests_total",
  help: "Total number of requests",
});

// 🧠 Agent decisions
const decisionCounter = new client.Counter({
  name: "ragnostic_decisions_total",
  help: "RAG vs REASON vs TOOL",
  labelNames: ["type"],
});

// 🔁 Retry count
const retryCounter = new client.Counter({
  name: "ragnostic_retries_total",
  help: "Number of retries triggered",
});

// ⏱️ Latency
const latencyHistogram = new client.Histogram({
  name: "ragnostic_latency_seconds",
  help: "Request latency",
  buckets: [0.1, 0.3, 0.5, 1, 2, 5],
});

const plannerLatency = new client.Histogram({
  name: "ragnostic_planner_latency_seconds",
  help: "Planner latency",
  buckets: [0.05, 0.1, 0.3, 0.5, 1],
});

const retrievalLatency = new client.Histogram({
  name: "ragnostic_retrieval_latency_seconds",
  help: "Retrieval latency",
  buckets: [0.1, 0.3, 0.5, 1, 2],
});

const reasoningLatency = new client.Histogram({
  name: "ragnostic_reasoning_latency_seconds",
  help: "Reasoning latency",
  buckets: [0.1, 0.5, 1, 2, 5],
});

const toolLatency = new client.Histogram({
  name: "ragnostic_tool_latency_seconds",
  help: "Tool latency",
  buckets: [0.05, 0.1, 0.3, 1],
});

const verifierLatency = new client.Histogram({
  name: "ragnostic_verifier_latency_seconds",
  help: "Verifier latency",
  buckets: [0.05, 0.1, 0.3, 1],
});

const confidenceGauge = new client.Gauge({
  name: "ragnostic_confidence_score",
  help: "Confidence score of responses",
});

// Register all
register.registerMetric(confidenceGauge);
register.registerMetric(requestCounter);
register.registerMetric(decisionCounter);
register.registerMetric(retryCounter);
register.registerMetric(latencyHistogram);
register.registerMetric(plannerLatency);
register.registerMetric(retrievalLatency);
register.registerMetric(reasoningLatency);
register.registerMetric(toolLatency);
register.registerMetric(verifierLatency);
module.exports = {
  register,
  requestCounter,
  decisionCounter,
  retryCounter,
  latencyHistogram,
   plannerLatency,
  retrievalLatency,
  reasoningLatency,
  toolLatency,
  verifierLatency,
<<<<<<< HEAD
  confidenceGauge,
=======
>>>>>>> main
};