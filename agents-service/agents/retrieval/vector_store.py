# agents/retrieval/vector_store.py

import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
from config.settings import settings

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.index = None
        self.documents = []

        if os.path.exists(settings.VECTOR_DB_PATH):
            self.load()

    def create_index(self, docs):
        embeddings = self.model.encode(docs)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.documents = docs
        self.save()

    def search(self, query):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, settings.TOP_K)

        results = []
        for i in indices[0]:
            results.append(self.documents[i])

        return results

    def save(self):
        os.makedirs("data", exist_ok=True)
        faiss.write_index(self.index, settings.VECTOR_DB_PATH)

        with open("data/docs.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load(self):
        self.index = faiss.read_index(settings.VECTOR_DB_PATH)

        with open("data/docs.pkl", "rb") as f:
            self.documents = pickle.load(f)


# Singleton instance
vector_store = VectorStore()