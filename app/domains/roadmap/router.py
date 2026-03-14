from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import User
from app.domains.roadmap.schemas import (
    RoadmapSimpleOut, RoadmapOut, UserRoadmapProgressOut, RoadmapTaskComplete
)
from app.domains.roadmap.service import RoadmapService

router = APIRouter()

@router.get("/", response_model=List[RoadmapSimpleOut])
def list_roadmaps(db: Session = Depends(get_db)):
    return RoadmapService.get_active_roadmaps(db)

@router.get("/{slug}", response_model=RoadmapOut)
def get_roadmap(slug: str, db: Session = Depends(get_db)):
    return RoadmapService.get_roadmap_by_slug(db, slug)

@router.get("/{roadmap_id}/progress", response_model=UserRoadmapProgressOut)
def get_progress(roadmap_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return RoadmapService.get_user_progress(db, current_user.id, roadmap_id)

@router.post("/tasks/complete", response_model=UserRoadmapProgressOut)
def complete_task(data: RoadmapTaskComplete, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return RoadmapService.complete_task(db, current_user.id, data.task_id)
