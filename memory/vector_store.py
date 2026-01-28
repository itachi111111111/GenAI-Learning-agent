import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index(os.getenv("PINECONE_INDEX"))
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add(self, text: str, metadata: dict = None):
        vector = self.model.encode(text).tolist()
        self.index.upsert([
            {
                "id": str(hash(text)),
                "values": vector,
                "metadata": metadata or {}
            }
        ])

    def search(self, query: str, top_k: int = 3):
        vector = self.model.encode(query).tolist()
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return [m["metadata"] for m in results["matches"]]
