from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from  parser import extract_text_from_pdf, clean_text
from pydantic import BaseModel
from scorer import score_resume

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
    result = score_resume(resume_text, job_description)
    return ScoreResponse(fit_score=result["fit_score"], message=result["reason"])