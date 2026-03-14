from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, UserGamificationStats, ProjectSubmission, UserBadge, SkillBadge
from typing import List, Dict, Any

router = APIRouter(prefix="/p", tags=["portfolio"])

@router.get("/{slug}")
def get_public_portfolio(slug: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.portfolio_slug == slug).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
        
    stats = db.query(UserGamificationStats).filter(UserGamificationStats.user_id == user.id).first()
    badges = db.query(UserBadge).filter(UserBadge.user_id == user.id).all()
    projects = db.query(ProjectSubmission).filter(
        ProjectSubmission.user_id == user.id,
        ProjectSubmission.status == "approved"
    ).all()
    
    return {
        "user": {
            "full_name": user.full_name,
            "email": user.email, # Optional: hide based on privacy settings
            "id": user.id
        },
        "stats": stats,
        "badges": [b.skill_badge for b in badges if b.skill_badge],
        "projects": projects
    }

from app.domains.identity.dependencies import get_current_user

@router.post("/claim-slug")
def claim_portfolio_slug(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if slug taken
    exists = db.query(User).filter(User.portfolio_slug == slug).first()
    if exists:
        raise HTTPException(status_code=400, detail="Slug already taken")
        
    current_user.portfolio_slug = slug
    db.commit()
    return {"message": "Portfolio slug updated", "slug": slug}
