import streamlit as st
import requests

import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Job Application Scoring Tool")
st.subheader("Upload your resume and paste the job description to get a fit score.")

uploaded_file = st.file_uploader("Choose a resume file (PDF Only)", type=["pdf"])
job_description = st.text_area("Paste the job description here:", height=200)

if st.button("Score Resume"):
    if not uploaded_file:
        st.error("Please upload a PDF resume file.")
    elif not job_description.strip():
        st.error("Please paste the job description.")
    else:
        with st.spinner("Scoring your resume..."):
            try:
                response = requests.post(f"{API_URL}/score", files={"file": (uploaded_file.name, uploaded_file.getvalue(),
                 "application/pdf")}, data={"job_description": job_description})
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Scoring complete!")
                    st.metric(label="Fit Score", value=f"{result['fit_score']}/100")
                    st.write(f"**Reason: {result['message']}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error occurred.')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend, make sure FastAPI server is running on http://localhost:8000")