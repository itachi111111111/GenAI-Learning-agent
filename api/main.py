from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
import time
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from core.runner import run_learning_assistant
from security.auth import verify_api_key
from analytics.logger import log_event

# -------------------------------------------------
# App MUST be created first
# -------------------------------------------------
app = FastAPI(title="GenAI Learning Assistant API")

# -------------------------------------------------
# Rate Limiter
# -------------------------------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# -------------------------------------------------
# Request Model
# -------------------------------------------------
class Query(BaseModel):
    user_input: str

# -------------------------------------------------
# ROUTE (FIXED)
# -------------------------------------------------
@app.post("/ask")
@limiter.limit("5/minute")
def ask(
    request: Request,
    query: Query,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # manual verify
    token = credentials.credentials
    verify_api_key(f"Bearer {token}")

    start = time.time()
    response = run_learning_assistant(query.user_input)
    latency = time.time() - start

    log_event({
        "input": query.user_input,
        "latency": latency
    })

    return {"response": response}
@app.get("/")
def health():
    return {"status": "ok"}
