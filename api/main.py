from fastapi import FastAPI
from core.state import crew, vector_store

app = FastAPI(title="GenAI Learning Assistant API")

@app.on_event("startup")
def startup_event():
    from crew import create_learning_crew
    from memory.vector_store import VectorStore
    import core.state as state

    print("🔄 Initializing vector store...")
    state.vector_store = VectorStore()

    print("🔄 Initializing CrewAI...")
    state.crew = create_learning_crew()

    print("✅ Startup complete")
