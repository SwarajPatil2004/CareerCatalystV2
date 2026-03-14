from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.db.models import AnalyticsEvent, StudentMetrics, User, StudentProfile, Skill, PlacementDrive, StudentDriveAssociation, StudentDriveStatus
import csv
import io

class AnalyticsService:
    @staticmethod
    def track_event(db: Session, user_id: int, event_type: str, metadata: Dict[str, Any] = None):
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
        # Shortlisted -> Selected
        funnel = {
            "shortlisted": db.query(StudentDriveAssociation).join(
                PlacementDrive, StudentDriveAssociation.drive_id == PlacementDrive.id
            ).filter(
                PlacementDrive.institution_id == institution_id,
                StudentDriveAssociation.status == "shortlisted"
            ).count(),
            "selected": db.query(StudentDriveAssociation).join(
                PlacementDrive, StudentDriveAssociation.drive_id == PlacementDrive.id
            ).filter(
                PlacementDrive.institution_id == institution_id,
                StudentDriveAssociation.status == "selected"
            ).count()
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
