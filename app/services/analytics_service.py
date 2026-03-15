from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any

class AnalyticsService:
    @staticmethod
    def track_event(db: Session, user_id: int, event_type: str, metadata: Dict[str, Any] = None):
        from app.db.models import AnalyticsEvent
        event = AnalyticsEvent(
            user_id=user_id,
            event_type=event_type,
            metadata_json=metadata or {}
        )
        db.add(event)
        db.commit()
        return event

    @staticmethod
    def get_institution_health(db: Session, institution_id: int):
        from app.db.constants import StudentDriveStatus
        from app.db.models import AnalyticsEvent, StudentProfile, Skill, PlacementDriveModel, StudentDriveJoin
        # 1. Basic Stats
        total_students = db.query(StudentProfile).filter(StudentProfile.institution_id == institution_id).count()
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_students = db.query(func.count(func.distinct(AnalyticsEvent.user_id))).join(
            StudentProfile, AnalyticsEvent.user_id == StudentProfile.user_id
        ).filter(
            StudentProfile.institution_id == institution_id,
            AnalyticsEvent.timestamp >= thirty_days_ago
        ).scalar()

        # 2. Top Skills Distribution
        skills_dist = db.query(Skill.name, func.count(Skill.id)).join(
            StudentProfile, Skill.user_id == StudentProfile.user_id
        ).filter(
            StudentProfile.institution_id == institution_id
        ).group_by(Skill.name).order_by(desc(func.count(Skill.id))).limit(10).all()

        # 3. Placement Funnel
        total_eligible = db.query(StudentDriveJoin).join(
            PlacementDriveModel, StudentDriveJoin.drive_id == PlacementDriveModel.id
        ).filter(
            PlacementDriveModel.institution_id == institution_id
        ).count()
        shortlisted = db.query(StudentDriveJoin).join(
            PlacementDriveModel, StudentDriveJoin.drive_id == PlacementDriveModel.id
        ).filter(
            PlacementDriveModel.institution_id == institution_id,
            StudentDriveJoin.status == "shortlisted"
        ).count()
        placed = db.query(StudentDriveJoin).join(
            PlacementDriveModel, StudentDriveJoin.drive_id == PlacementDriveModel.id
        ).filter(
            PlacementDriveModel.institution_id == institution_id,
            StudentDriveJoin.status == "selected"
        ).count()
        
        funnel = {
            "eligible": total_eligible,
            "shortlisted": shortlisted,
            "placed": placed
        }

        # 4. Activity Trend (Last 7 days)
        trend = []
        for i in range(7):
            d = datetime.utcnow().date() - timedelta(days=i)
            count = db.query(AnalyticsEvent).join(
                StudentProfile, AnalyticsEvent.user_id == StudentProfile.user_id
            ).filter(
                StudentProfile.institution_id == institution_id,
                func.date(AnalyticsEvent.timestamp) == d
            ).count()
            trend.append({"date": d.isoformat(), "count": count})
        
        return {
            "stats": {
                "total_students": total_students,
                "active_students": active_students,
                "at_risk_students": total_students - (active_students or 0)
            },
            "skills_distribution": [dict(zip(["name", "count"], s)) for s in skills_dist],
            "placement_funnel": funnel,
            "activity_trend": trend[::-1] # Chronological order
        }

    @staticmethod
    def export_analytics_csv(db: Session, institution_id: int):
        import csv
        import io
        from app.db.models import AnalyticsEvent, StudentProfile
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["User ID", "Event Type", "Timestamp", "Metadata"])
        
        events = db.query(AnalyticsEvent).join(
            StudentProfile, AnalyticsEvent.user_id == StudentProfile.user_id
        ).filter(
            StudentProfile.institution_id == institution_id
        ).order_by(desc(AnalyticsEvent.timestamp)).all()
        
        for e in events:
            writer.writerow([e.user_id, e.event_type, e.timestamp, e.metadata_json])
        
        return output.getvalue()
