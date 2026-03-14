from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db.models import User, UserGamificationStats, InterviewSession, ProjectSubmission, Shortlist, Recruiter, Company
from typing import List, Dict, Any, Optional

class RecruiterService:
    @staticmethod
    def search_candidates(
        db: Session, 
        skills: Optional[List[str]] = None, 
        min_xp: Optional[int] = None, 
        min_interview_score: Optional[float] = None,
        graduation_year: Optional[int] = None
    ):
        query = db.query(User).filter(User.role == "student")
        
        # This is a simplified search. In production, we'd use a more robust search engine or complex joins.
        # Joining with GamificationStats for XP
        query = query.join(UserGamificationStats, isouter=True)
        
        if min_xp:
            query = query.filter(UserGamificationStats.total_xp >= min_xp)
            
        # Filter by interview scores (average of finalized sessions)
        if min_interview_score:
            # This would require an aggregation subquery
            pass
            
        return query.limit(50).all()

    @staticmethod
    def get_candidate_details(db: Session, student_id: int):
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            return None
            
        stats = db.query(UserGamificationStats).filter(UserGamificationStats.user_id == student_id).first()
        interviews = db.query(InterviewSession).filter(InterviewSession.user_id == student_id, InterviewSession.status == "completed").all()
        projects = db.query(ProjectSubmission).filter(ProjectSubmission.user_id == student_id, ProjectSubmission.status == "approved").all()
        
        return {
            "student": student,
            "stats": stats,
            "interview_count": len(interviews),
            "approved_projects": len(projects)
        }

    @staticmethod
    def shortlist_candidate(db: Session, recruiter_id: int, student_id: int):
        exists = db.query(Shortlist).filter(
            Shortlist.recruiter_id == recruiter_id, 
            Shortlist.student_id == student_id
        ).first()
        
        if not exists:
            shortlist = Shortlist(recruiter_id=recruiter_id, student_id=student_id)
            db.add(shortlist)
            db.commit()
            return shortlist
        return exists

    @staticmethod
    def request_interview(db: Session, recruiter_id: int, student_id: int):
        # Implementation for notifying TPO and student
        # Log event for now
        recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
        student = db.query(User).filter(User.id == student_id).first()
        
        # Placeholder for actual notification logic (e.g., Celery task)
        return {"status": "request_sent", "recruiter": recruiter.user.email, "student": student.email}
