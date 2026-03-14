from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.domains.identity.dependencies import get_current_user
from app.db.models import User, Recruiter
from app.services.recruiter_service import RecruiterService
from .schemas import CandidateSearchFilters, ShortlistRequest, InterviewRequest
from typing import List, Optional

router = APIRouter(prefix="/recruiter", tags=["recruiter"])

@router.get("/search")
def search_candidates(
    skills: Optional[List[str]] = Query(None),
    min_xp: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    # Publicly accessible search
    candidates = RecruiterService.search_candidates(db, skills=skills, min_xp=min_xp)
    return candidates

@router.get("/candidates/{id}")
def get_candidate_details(id: int, db: Session = Depends(get_db)):
    # Publicly accessible profile
    details = RecruiterService.get_candidate_details(db, id)
    return details

@router.post("/shortlist")
def shortlist_candidate(
    data: ShortlistRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure current user is a recruiter
    recruiter = db.query(Recruiter).filter(Recruiter.user_id == current_user.id).first()
    if not recruiter:
        return {"error": "Unauthorized. Recruiter role required."}
        
    return RecruiterService.shortlist_candidate(db, recruiter.id, data.student_id)

@router.post("/request-interview")
def request_interview(
    data: InterviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recruiter = db.query(Recruiter).filter(Recruiter.user_id == current_user.id).first()
    if not recruiter:
        return {"error": "Unauthorized. Recruiter role required."}
        
    return RecruiterService.request_interview(db, recruiter.id, data.student_id)
