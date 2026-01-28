from memory.vector_store import VectorStore

vector_store = VectorStore()

def store_interaction(user_input: str, assistant_output: str):
    combined = f"User: {user_input}\nAssistant: {assistant_output}"
    vector_store.add(combined, {"query": user_input})

def retrieve_context(user_input: str):
    return vector_store.search(user_input)
