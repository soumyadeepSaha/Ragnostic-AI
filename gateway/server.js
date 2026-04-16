const express = require("express");
const queryRoute = require("./routes/query");
const client = require("prom-client");
const app = express();
app.use(express.json());

app.use("/query", queryRoute);

const requestCounter = new client.Counter({
  name: "requests_total",
  help: "Total requests",
});

app.use((req, res, next) => {
  requestCounter.inc();
  next();
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", client.register.contentType);
  res.end(await client.register.metrics());
});


app.listen(3000, () => {
  console.log("Gateway running on port 3000");
});

