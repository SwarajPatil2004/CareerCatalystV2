from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict

class CandidateSearchFilters(BaseModel):
    skills: Optional[List[str]] = None
    min_xp: Optional[int] = None
    min_score: Optional[float] = None
    graduation_year: Optional[int] = None

class ShortlistRequest(BaseModel):
    student_id: int

class InterviewRequest(BaseModel):
    student_id: int
    message: Optional[str] = None

class CandidateBasicInfo(BaseModel):
    id: int
    full_name: str
    email: str
    xp: int
    approved_projects: int
    interview_score: float
