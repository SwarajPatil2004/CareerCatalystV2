from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import User, UserRole
from app.services.admin_service import AdminService
from typing import List, Dict, Any

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin level permissions required."
        )
    return current_user

@router.get("/stats", dependencies=[Depends(require_admin)])
def get_stats(db: Session = Depends(get_db)):
    return AdminService.get_platform_stats(db)

@router.patch("/institutions/{id}/approve", dependencies=[Depends(require_admin)])
def approve_institution(id: int, db: Session = Depends(get_db)):
    return AdminService.approve_institution(db, id)

@router.post("/users/{id}/suspend", dependencies=[Depends(require_admin)])
def suspend_user(id: int, db: Session = Depends(get_db)):
    return AdminService.suspend_user(db, id)
