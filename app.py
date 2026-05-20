from fastapi import FastAPI
from pydantic import BaseModel

from main import process_claim

app = FastAPI(
    title="Sentinels of Truth API"
)


class ClaimRequest(BaseModel):
    claim: str


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/verify")
def verify_claim(request: ClaimRequest):
    state = process_claim(request.claim)

    return state.model_dump()