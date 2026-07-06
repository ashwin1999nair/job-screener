import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from fastapi import HTTPException
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0.2)

prompt_template = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template="""
You are a recruiter evaluating a candidate's resume against a job description.

Resume:
{resume_text}

Job Description:
{job_description}

Score how well the resume matches the job description from 0 to 100.
Return ONLY a JSON object with exactly these two keys:
- fit_score: a number between 0 and 100
- reason: one sentence explaining the score

Return nothing else. No markdown, no explanation, just the JSON.
""")

def score_resume(resume_text: str, job_description: str) -> dict:
    try:
        prompt=prompt_template.format(resume_text=resume_text, job_description=job_description)
        response=llm.invoke(prompt)
        content=response.content.strip()
        if content.startswith("```"):
            content=content.split("```")[1]
            if content.startswith("json"):
                content=content[4:]

        result=json.loads(content.strip())
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON from scoring response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring resume: {str(e)}")
    
