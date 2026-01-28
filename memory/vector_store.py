import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.dim = 384
        self.index_path = "memory/faiss.index"
        self.meta_path = "memory/meta.pkl"

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(self.dim)
        self.metadata = []

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)

    def add(self, text: str, meta: dict):
        emb = self.model.encode([text]).astype("float32")
        self.index.add(emb)
        self.metadata.append(meta)

        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query: str, k: int = 3):
        if self.index.ntotal == 0:
            return []

        emb = self.model.encode([query]).astype("float32")
        _, idxs = self.index.search(emb, k)

        return [self.metadata[i] for i in idxs[0] if i < len(self.metadata)]
