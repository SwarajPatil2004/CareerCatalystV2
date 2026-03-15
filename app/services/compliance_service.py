from sqlalchemy.orm import Session
from app.db.models import AuditLog, UserConsent, InterviewSession
from datetime import datetime, timedelta

class ComplianceService:
    @staticmethod
    def log_audit_event(db: Session, user_id: int, action: str, resource: str, ip: str = None):
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip
        )
        db.add(log)
        db.commit()

    @staticmethod
    def record_consent(db: Session, user_id: int, consent_type: str, granted: bool):
        consent = UserConsent(
            user_id=user_id,
            consent_type=consent_type,
            is_granted=granted,
            version="1.0"
        )
        db.add(consent)
        db.commit()

    @staticmethod
    def enforce_data_retention(db: Session):
        """Delete interview recordings older than 30 days (FERPA/GDPR compliance)"""
        thirty_days_ago = datetime.now() - timedelta(days=30)
        sessions_to_wipe = db.query(InterviewSession).filter(
            InterviewSession.start_time < thirty_days_ago
        ).all()
        
        for session in sessions_to_wipe:
            # In a real app, delete from S3/Storage here
            session.recording_url = None # Wipe the pointer
            
        db.commit()
        return len(sessions_to_wipe)
