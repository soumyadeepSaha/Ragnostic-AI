# config/settings.py

import os

class Settings:
    # LLM
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "llama3"

    # Vector DB
    VECTOR_DB_PATH = "data/faiss_index"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # Retrieval
    TOP_K = 3

settings = Settings()