import requests
import json

def generate(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # Increased to 2 minutes for inference
        )
        res.raise_for_status()  # Raise exception for bad HTTP status
        data = res.json()
        if "response" in data:
            return data["response"]
        else:
            print(f"DEBUG: Unexpected Ollama response format: {list(data.keys())}")
            return "Response from mock LLM"
    except Exception as e:
        print(f"DEBUG: Ollama error: {type(e).__name__}: {str(e)[:100]}")
        # Mock responses for testing when Ollama is unavailable
        prompt_lower = prompt.lower()
        if "decide" in prompt_lower and "tool" in prompt_lower.lower():
            return "TOOL"
        elif "decide" in prompt_lower and "rag" in prompt_lower.lower():
            return "RAG"
        elif "check if" in prompt_lower or "valid" in prompt_lower:
            return "VALID"
        else:
            return "Response from mock LLM"