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

// Register all
register.registerMetric(requestCounter);
register.registerMetric(decisionCounter);
register.registerMetric(retryCounter);
register.registerMetric(latencyHistogram);

module.exports = {
  register,
  requestCounter,
  decisionCounter,
  retryCounter,
  latencyHistogram,
};