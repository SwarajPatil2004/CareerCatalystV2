from sqlalchemy.orm import Session
from app.db.models import UserBadge, SkillBadge, User, InterviewSession, ProjectSubmission
from typing import List

class BadgeEngine:
    @staticmethod
    def evaluate_triggers(db: Session, user_id: int, event_type: str):
        """
        Trigger events: 'interview_complete', 'project_approved', 'roadmap_phase_complete'
        """
        if event_type == 'interview_complete':
            BadgeEngine._check_interview_badges(db, user_id)
        elif event_type == 'project_approved':
            BadgeEngine._check_project_badges(db, user_id)
            
    @staticmethod
    def _check_interview_badges(db: Session, user_id: int):
        last_interview = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id,
            InterviewSession.status == "completed"
        ).order_by(InterviewSession.timestamp.desc()).first()
        
        if last_interview and last_interview.score >= 80:
            # Issue "Communication Pro" badge (Gold)
            BadgeEngine.issue_skill_badge(db, user_id, "Communication", "Gold")

    @staticmethod
    def _check_project_badges(db: Session, user_id: int):
        approved_count = db.query(ProjectSubmission).filter(
            ProjectSubmission.user_id == user_id,
            ProjectSubmission.status == "approved"
        ).count()
        
        if approved_count >= 1:
            BadgeEngine.issue_skill_badge(db, user_id, "Project Builder", "Bronze")
        if approved_count >= 5:
            BadgeEngine.issue_skill_badge(db, user_id, "Open Source Contributor", "Silver")

    @staticmethod
    def issue_skill_badge(db: Session, user_id: int, skill_name: str, level: str):
        badge = db.query(SkillBadge).filter(
            SkillBadge.skill_name == skill_name,
            SkillBadge.level == level
        ).first()
        
        if not badge:
            badge = SkillBadge(skill_name=skill_name, level=level, verification_method="automated")
            db.add(badge)
            db.commit()
            db.refresh(badge)
            
        exists = db.query(UserBadge).filter(
            UserBadge.user_id == user_id,
            UserBadge.skill_badge_id == badge.id
        ).first()
        
        if not exists:
            user_badge = UserBadge(user_id=user_id, skill_badge_id=badge.id)
            db.add(user_badge)
            db.commit()
            return user_badge
        return exists
