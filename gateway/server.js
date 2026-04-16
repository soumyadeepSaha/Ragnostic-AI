const express = require("express");
const queryRoute = require("./routes/query");

const app = express();
app.use(express.json());

app.use("/query", queryRoute);

app.listen(3000, () => {
  console.log("Gateway running on port 3000");
});