const express = require("express");
const router = express.Router();
const orchestrator = require("../services/orchestrator");

router.post("/", async (req, res) => {
  const { query } = req.body;

  try {
    const result = await orchestrator.handleQuery(query);
    res.json({ result });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;