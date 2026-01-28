from memory.vector_store import VectorStore

store = VectorStore()

def store_interaction(text: str):
    store.add(text, metadata={"text": text})

def retrieve_context(query: str):
    results = store.search(query)
    return "\n".join([r.get("text", "") for r in results])
