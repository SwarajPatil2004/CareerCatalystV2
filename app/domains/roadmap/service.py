from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Roadmap, RoadmapPhase, RoadmapTask, UserRoadmapProgress
from app.core.exceptions import AppException
from fastapi import status

class RoadmapService:
    @staticmethod
    def get_active_roadmaps(db: Session) -> List[Roadmap]:
        return db.query(Roadmap).filter(Roadmap.is_active == 1).all()

    @staticmethod
    def get_roadmap_by_slug(db: Session, slug: str) -> Optional[Roadmap]:
        roadmap = db.query(Roadmap).filter(Roadmap.slug == slug).first()
        if not roadmap:
            raise AppException("Roadmap not found", status.HTTP_404_NOT_FOUND)
        return roadmap

    @staticmethod
    def get_user_progress(db: Session, user_id: int, roadmap_id: int) -> UserRoadmapProgress:
        progress = db.query(UserRoadmapProgress).filter(
            UserRoadmapProgress.user_id == user_id,
            UserRoadmapProgress.roadmap_id == roadmap_id
        ).first()

        if not progress:
            progress = UserRoadmapProgress(user_id=user_id, roadmap_id=roadmap_id, completed_task_ids=[], total_xp=0)
            db.add(progress)
            db.commit()
            db.refresh(progress)
        return progress

    @staticmethod
    def complete_task(db: Session, user_id: int, task_id: int) -> UserRoadmapProgress:
        task = db.query(RoadmapTask).filter(RoadmapTask.id == task_id).first()
        if not task:
            raise AppException("Task not found", status.HTTP_404_NOT_FOUND)

        phase = db.query(RoadmapPhase).filter(RoadmapPhase.id == task.phase_id).first()
        roadmap_id = phase.roadmap_id

        progress = RoadmapService.get_user_progress(db, user_id, roadmap_id)
        
        # Avoid duplicate completion
        if task_id in progress.completed_task_ids:
            return progress

        # Update progress
        # Since completed_task_ids is a JSON/List, we need to handle it carefully
        completed_tasks = list(progress.completed_task_ids)
        completed_tasks.append(task_id)
        progress.completed_task_ids = completed_tasks
        progress.total_xp += task.xp

        db.commit()
        db.refresh(progress)
        return progress
