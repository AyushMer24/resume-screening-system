from pydantic import BaseModel
from typing import Optional

class ResumeTextRequest(BaseModel):
    resume_text: Optional[str] = None

class JobMatchResponse(BaseModel):
    job_title: str
    similarity_score: float