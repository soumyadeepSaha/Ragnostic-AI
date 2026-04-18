const express = require("express");
const queryRoute = require("./routes/query");
const app = express();
app.use(express.json());

const {
  register,
  requestCounter,
} = require("./metrics");

// 🔢 Track all requests
app.use((req, res, next) => {
  requestCounter.inc();
  next();
});

app.use("/query", queryRoute);

// 🔥 Prometheus metrics endpoint
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

app.listen(3000, () => {
  console.log("Gateway running on port 3000");
});

