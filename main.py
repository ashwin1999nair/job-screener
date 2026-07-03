from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from  parser import extract_text_from_pdf, clean_text
from pydantic import BaseModel

app = FastAPI()

class ScoreResponse(BaseModel):
    fit_score: float
    message: str

@app.get("/health")
def health_check():
    return {"status": "running"}

@app.post("/score", response_model=ScoreResponse) 
async def score_application( 
    file: UploadFile = File(..., description="PDF file of the resume"), 
    job_description: str = Form(..., description="Job description text")  
):
    if file.content_type != "application/pdf":  
        raise HTTPException(status_code=415, detail="Uploaded file must be a PDF.") 
    
    file_bytes = await file.read() 
    raw_text = extract_text_from_pdf(file_bytes) 
    resume_text = clean_text(raw_text)

    # Placeholder — Phase 3 replaces this with Gemini scoring
    return ScoreResponse(fit_score=50, message=resume_text[:200])