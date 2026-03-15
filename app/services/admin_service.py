from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import User, Institution, PlatformMetric, InterviewSession, ProjectSubmission
from app.services.compliance_service import ComplianceService
from datetime import datetime, timedelta
from typing import Dict, Any

class AdminService:
    @staticmethod
    def get_platform_stats(db: Session) -> Dict[str, Any]:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        total_users = db.query(User).count()
        active_users_30d = db.query(User).filter(User.last_login_at >= thirty_days_ago).count()
        pending_institutions = db.query(Institution).filter(Institution.status == "pending").count()
        total_interviews = db.query(InterviewSession).count()
        approved_projects = db.query(ProjectSubmission).filter(ProjectSubmission.status == "approved").count()
        
        return {
            "total_users": total_users,
            "dau": active_users_30d, # Simplified DAU for MVP
            "pending_institutions": pending_institutions,
            "total_interviews": total_interviews,
            "approved_projects": approved_projects,
            "system_health": "stable"
        }

    @staticmethod
    def approve_institution(db: Session, institution_id: int):
        inst = db.query(Institution).filter(Institution.id == institution_id).first()
        if inst:
            inst.status = "approved"
            ComplianceService.log_audit_event(db, 0, "approve_institution", f"institution:{institution_id}")
            db.commit()
            return inst
        return None

    @staticmethod
    def suspend_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = False
            ComplianceService.log_audit_event(db, 0, "suspend_user", f"user:{user_id}")
            db.commit()
            return user
        return None
