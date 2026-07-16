# AI Resume Screener

An end-to-end AI-powered tool that scores a candidate's resume against a job description using Google Gemini. Built as a portfolio project to demonstrate full-stack ML application development.

---

## What It Does

1. User uploads a resume (PDF) and pastes a job description
2. The backend parses the PDF and extracts clean text
3. The text is sent to Google Gemini via LangChain for semantic evaluation
4. Gemini returns a fit score (0–100) and a one-sentence reason
5. The result is displayed in a clean Streamlit UI

---

## Architecture

```
User (Browser)
     │
     ▼
Streamlit Frontend (Port 8501)
     │  HTTP POST /score
     ▼
FastAPI Backend (Port 8000)
     │
     ├── pdfplumber → extracts resume text
     │
     └── LangChain + Gemini API → scores resume against JD
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| PDF Parsing | pdfplumber |
| LLM Orchestration | LangChain |
| LLM | Google Gemini 2.5 Flash |
| Containerisation | Docker + Docker Compose |

---

## How to Run Locally

### Without Docker

**1. Clone the repo**
```bash
git clone https://github.com/ashwin1999nairn/job-screener
cd job-screener
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Gemini API key**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

**5. Run FastAPI**
```bash
uvicorn main:app --reload
```

**6. Run Streamlit (new terminal)**
```bash
streamlit run app.py
```

Visit `http://localhost:8501`

---

### With Docker

**1. Add your Gemini API key to `.env` (same as above)**

**2. Build and run**
```bash
docker-compose up --build
```

Visit `http://localhost:8501`

---

## Example Output

| Input | Output |
|---|---|
| Resume: MSc AI student with Python, NLP, LLM experience | Fit Score: 72/100 |
| JD: Senior AI Engineer, Dublin | Reason: Strong technical skills but limited senior-level experience |

---

## Project Structure

```
job-screener/
├── main.py               # FastAPI app — /health and /score endpoints
├── parser.py             # PDF parsing with pdfplumber
├── scorer.py             # LangChain + Gemini scoring logic
├── app.py                # Streamlit frontend
├── Dockerfile.api        # FastAPI container
├── Dockerfile.streamlit  # Streamlit container
├── docker-compose.yml    # Runs both containers together
├── requirements.txt      # Python dependencies
└── .env                  # API keys (not committed to Git)
```

---

## Future Improvements

- AWS deployment (EC2 or ECS)
- Resume improvement suggestions alongside the score
- Support for scanned PDFs via OCR
- Job description URL input instead of manual paste
- Score history and comparison across multiple JDs
