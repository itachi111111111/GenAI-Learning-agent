import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX")

        if not api_key:
            raise RuntimeError("PINECONE_API_KEY not set")
        if not index_name:
            raise RuntimeError("PINECONE_INDEX not set")

        # Correct for pinecone==3.2.2
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name)

        # 384-dim embeddings (matches index)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add(self, text: str, metadata: dict | None = None):
        vector = self.model.encode(text).tolist()

        self.index.upsert(
            vectors=[
                {
                    "id": str(hash(text)),
                    "values": vector,
                    "metadata": {
                        "text": text,
                        **(metadata or {}),
                    },
                }
            ]
        )

    def search(self, query: str, top_k: int = 3):
        vector = self.model.encode(query).tolist()
        return self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
        )

    def retrieve(self, query: str, top_k: int = 3) -> str:
        result = self.search(query, top_k)
        matches = result.get("matches", [])

        if not matches:
            return ""

        return "\n\n".join(
            m["metadata"]["text"]
            for m in matches
            if "metadata" in m and "text" in m["metadata"]
        )
