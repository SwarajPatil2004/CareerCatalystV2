from sqlalchemy.orm import Session
from app.db.models import User, Institution, PlatformMetric
from datetime import datetime, timedelta

class MonitoringService:
    @staticmethod
    def check_churn_risk(db: Session):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        # TPOs with no activity in 30 days
        risk_tpos = db.query(User).filter(
        from app.db.constants import UserRole
        risk_tpos = db.query(User).filter(
            User.role == UserRole.TPO,
            User.last_login_at < thirty_days_ago
        ).all()
        
        # Institutions with no drives in 30 days
        # (This would require joining with placement_drives)
        
        return {
            "risk_users_count": len(risk_tpos),
            "alert": "High churn risk detected" if len(risk_tpos) > 5 else "Normal"
        }

    @staticmethod
    def log_daily_metrics(db: Session):
        # This would be called by a Celery beat task
        stats = {
            "dau": db.query(User).filter(User.last_login_at >= datetime.now() - timedelta(days=1)).count(),
            "new_signups": db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=1)).count()
        }
        
        for name, value in stats.items():
            metric = PlatformMetric(metric_name=name, value=float(value))
            db.add(metric)
        db.commit()
