const axios = require("axios");

const PYTHON_BASE = "http://localhost:8000";

exports.handleQuery = async (query) => {
  const plan = await axios.post(`${PYTHON_BASE}/planner/`, { query });

  let response;

  if (plan.data.action === "RAG") {
    response = await axios.post(`${PYTHON_BASE}/retrieve/`, { query });
  } else if (plan.data.action === "TOOL") {
    response = await axios.post(`${PYTHON_BASE}/tool/`, { query });
  } else {
    response = await axios.post(`${PYTHON_BASE}/reason/`, { query });
  }

  const verify = await axios.post(`${PYTHON_BASE}/verify/`, {
    query,
    answer: response.data.answer,
  });

  if (verify.data.status === "RETRY") {
    const retry = await axios.post(`${PYTHON_BASE}/retrieve/`, { query });
    return retry.data.answer;
  }

  return verify.data.final_answer;
};