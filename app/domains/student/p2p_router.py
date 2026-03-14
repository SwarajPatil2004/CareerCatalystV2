from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.domains.identity.dependencies import get_current_user
from app.db.models import User, ProjectSubmission
from app.services.p2p_service import P2PService
from app.services.gamification_service import GamificationService
from .p2p_schemas import ProjectSubmissionCreate, ProjectReviewSubmit, GamificationStatsResponse

router = APIRouter(prefix="/p2p", tags=["p2p"])

@router.post("/submit")
def submit_project(
    data: ProjectSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    submission = P2PService.submit_project(
        db, current_user.id, data.project_id, data.title, data.code_url
    )
    # Grant XP for submission
    GamificationService.update_stats(db, current_user.id, 50)
    return submission

@router.get("/queue")
def get_review_queue(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return P2PService.get_review_queue(db, current_user.id)

@router.post("/review")
def submit_review(
    data: ProjectReviewSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    review = P2PService.submit_review(
        db, current_user.id, data.submission_id, data.rubric_scores, data.feedback
    )
    # Grant XP for review
    GamificationService.update_stats(db, current_user.id, 100)
    return review

@router.get("/stats", response_model=GamificationStatsResponse)
def get_gamification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # This would ideally be in a GamificationRouter, but combining for now
    from app.db.models import UserGamificationStats, Squad
    stats = db.query(UserGamificationStats).filter(
        UserGamificationStats.user_id == current_user.id
    ).first()
    
    if not stats:
        return {
            "total_xp": 0, "streak_days": 0, "streak_buffer": 0,
            "last_active": None, "squad_name": None
        }
        
    squad_name = None
    if stats.squad_id:
        squad = db.query(Squad).filter(Squad.id == stats.squad_id).first()
        if squad: squad_name = squad.name
        
    return {
        "total_xp": stats.total_xp,
        "streak_days": stats.streak_days,
        "streak_buffer": stats.streak_buffer,
        "last_active": stats.last_active,
        "squad_name": squad_name
    }

@router.get("/seed")
def seed_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # In a real app, check for institution_id properly
    P2PService.seed_game_data(db, 1)
    return {"message": "Demo game data seeded successfully."}
