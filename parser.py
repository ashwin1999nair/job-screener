import pdfplumber
import io
from fastapi import HTTPException, UploadFile

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Accepts raw PDF bytes and returns extracted plain text.
    
    Why bytes and not a file path?
    - FastAPI's UploadFile gives us bytes in memory
    - We never want to write uploaded files to disk (security + statelessness)
    - io.BytesIO wraps bytes so pdfplumber can read them like a file
    """
    text_pages = []
    try:
        # Wrap bytes in a file-like object — pdfplumber expects a file handle   
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf: 
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
    except Exception as e: 
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")
    
    if not text_pages: 
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF.")
    
    # Join pages with double newline to preserve section boundaries
    full_text = "\n\n".join(text_pages)
    return full_text

def clean_text(raw_text: str) -> str:
    """
    Light cleaning pass after extraction.
    
    Resumes often have:
    - Multiple consecutive blank lines (from layout artifacts)
    - Leading/trailing whitespace per line
    
    We normalise these without destroying structure.
    """
    lines=raw_text.splitlines()
    # Strip each line, remove lines that are purely whitespace
    cleaned_lines = [line.strip() for line in lines]
    # Collapse runs of empty lines into a single blank line
    result = []
    previous_line_empty = False
    for line in cleaned_lines:
        if line == "":
            if not previous_line_empty:
                result.append("")  # Keep one blank line
            previous_line_empty = True
        else:
            result.append(line)
            previous_line_empty = False

    return "\n".join(result).strip()
