const axios = require("axios");

const PYTHON_BASE = "http://localhost:8000";

exports.handleQuery = async (query) => {
  // Step 1: Planner decides
  const plan = await axios.post(`${PYTHON_BASE}/planner`, { query });

  let response;

  if (plan.data.action === "RAG") {
    response = await axios.post(`${PYTHON_BASE}/retrieve`, { query });
  } else {
    response = await axios.post(`${PYTHON_BASE}/reason`, { query });
  }

  // Step 2: Verify
  const verified = await axios.post(`${PYTHON_BASE}/verify`, {
    query,
    answer: response.data.answer,
  });

  return verified.data.final_answer;
};