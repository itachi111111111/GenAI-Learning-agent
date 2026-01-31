from memory.vector_store import VectorStore

store = VectorStore()

def store_interaction(text: str):
    store.add(text, metadata={"text": text})

def retrieve_context(query: str):
    results = store.search(query)
    return "\n".join([match.metadata.get("text", "") for match in results.matches])

