from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.runner import run_learning_assistant  # ✅ Make sure this path is correct

app = FastAPI()

# Optional: Add CORS if calling from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    user_input: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: AskRequest):
    output = run_learning_assistant(request.user_input)
    return {"response": output}
