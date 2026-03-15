from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import User
from app.services.interview_service import InterviewService
from app.domains.interview.schemas import (
    InterviewStart, InterviewSessionResponse, 
    InterviewResponseSubmit, ProctoringEvent, InterviewReport
)

router = APIRouter()

@router.post("/start", response_model=InterviewSessionResponse)
def start_interview(
    data: InterviewStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = InterviewService.start_session(db, current_user.id, data.track)
    # Map to schema manually to include questions
    return {
        "id": session.id,
        "track": session.track,
        "status": session.status,
        "start_time": session.start_time,
        "questions": [
            {"id": q.id, "text": q.text, "type": q.type, "order": q.order}
            for q in session.questions
        ]
    }

@router.post("/{session_id}/respond")
def submit_response(
    session_id: int,
    data: InterviewResponseSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.submit_response(db, session_id, data.question_id, data.transcript)

@router.post("/{session_id}/finalize")
def finalize_interview(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.finalize_interview(db, session_id)

@router.post("/{session_id}/proctor")
def log_proctoring(
    session_id: int,
    data: ProctoringEvent,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.log_proctoring_event(db, session_id, data.event_type)

@router.get("/{session_id}/report", response_model=InterviewReport)
def get_report(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.get_session_report(db, session_id)
