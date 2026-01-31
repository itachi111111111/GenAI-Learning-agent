from memory.vector_store import VectorStore

store = VectorStore()

def store_interaction(query: str, response: str = None):
    """
    Store an interaction in the vector store.
    If response is None, treats query as the full text.
    """
    if response:
        text = f"User: {query}\nAssistant: {response}"
        metadata = {
            "query": query,
            "response": response,
            "text": text,
            "type": "qa_pair"
        }
    else:
        text = query
        metadata = {"text": text, "type": "text"}
    
    store.add(text, metadata=metadata)

def retrieve_context(query: str):
    results = store.search(query)
    # Return full interaction text for context
    return "\n".join([match.metadata.get("text", "") for match in results.matches])