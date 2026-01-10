from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from backend.pdf_reader import extract_text_from_pdf
from backend.jobs_data import job_descriptions
from backend.nlp_utils import preprocess_text, match_resume_to_jobs
from backend.models import Job  
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Resume Screening & Job Recommendation system")

# CORS (needed for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message":"resume screening api is running"}

@app.post("/analyze-resume")
async def analyze_resume(
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if not resume_text and not resume_file:
        raise HTTPException(
            status_code=400,
            detail="Please provide resume text or upload a PDF file."
        )

    extracted_text = ""

    # Case 1: Resume text provided
    if resume_text:
        extracted_text = resume_text

    # Case 2: PDF provided
    elif resume_file:
        if resume_file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        extracted_text = extract_text_from_pdf(resume_file.file)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    cleaned_text = preprocess_text(extracted_text)

    jobs = db.query(Job).all()

    job_data = [
        {
            "title":job.title,
            "description":job.description
        }
        for job in jobs
    ]

    job_matches = match_resume_to_jobs(
    resume_text=cleaned_text,
    jobs=job_data
    )

    return {
    "status": "success",
    "recommended_jobs": job_matches
    }