from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ScoreRequest(BaseModel):
    resume_text: str
    jd_text: str

class ScoreResponse(BaseModel):
    fit_score: float
    message: str

@app.get("/health")
def health_check():
    return {"status": "running"}

@app.post("/score", response_model=ScoreResponse)
def score_application(request: ScoreRequest):
    # Placeholder for now — real logic comes later
    return ScoreResponse(fit_score=50, message="Placeholder score")