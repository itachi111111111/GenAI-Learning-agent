from fastapi import FastAPI
import core.state as state

app = FastAPI(title="GenAI Learning Assistant API")

@app.on_event("startup")
def startup_event():
    print("🔄 Startup: loading heavy components")

    from crew import create_learning_crew
    from memory.vector_store import VectorStore

    state.vector_store = VectorStore()
    state.crew = create_learning_crew()

    print("✅ Startup complete")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(query: dict):
    from core.runner import run_learning_assistant
    return {"response": run_learning_assistant(query["user_input"])}
