from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import random
from app.db.models import ProjectSubmission, ProjectReview, ReviewQueue, User
from typing import List, Dict, Any
from app.core.exceptions import APIException
from fastapi import status

class P2PService:
    @staticmethod
    def submit_project(db: Session, user_id: int, project_id: int, title: str, code_url: str):
        submission = ProjectSubmission(
            user_id=user_id,
            project_id=project_id,
            title=title,
            code_url=code_url
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        # Add to Review Queue
        queue_item = ReviewQueue(submission_id=submission.id, weight=0)
        db.add(queue_item)
        db.commit()
        
        return submission

    @staticmethod
    def get_review_queue(db: Session, user_id: int) -> List[ProjectSubmission]:
        # Check if user is eligible to review (must have 1 approved review of their own)
        my_approved = db.query(ProjectSubmission).filter(
            ProjectSubmission.user_id == user_id,
            ProjectSubmission.status == "approved"
        ).count()
        
        if my_approved < 1:
            raise APIException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have at least 1 approved project submission to review others."
            )

        # Get submissions excluding own
        submissions = db.query(ProjectSubmission).join(ReviewQueue).filter(
            ProjectSubmission.user_id != user_id,
            ProjectSubmission.status == "submitted"
        ).order_by(ReviewQueue.weight.desc(), ProjectSubmission.timestamp.asc()).limit(5).all()
        
        return submissions

    @staticmethod
    def submit_review(db: Session, reviewer_id: int, submission_id: int, rubric_scores: Dict[str, int], feedback: str):
        # 1. Record the review
        review = ProjectReview(
            submission_id=submission_id,
            reviewer_id=reviewer_id,
            rubric_scores=rubric_scores,
            feedback=feedback,
            is_approved=True # Simplified for now
        )
        db.add(review)
        
        # 2. Update submission status
        submission = db.query(ProjectSubmission).filter(ProjectSubmission.id == submission_id).first()
        if submission:
            submission.status = "under_review"
            
            # Check if it has enough reviews (e.g., 2) to be fully approved
            review_count = db.query(ProjectReview).filter(ProjectReview.submission_id == submission_id).count()
            if review_count >= 2:
                submission.status = "approved"
                # Remove from queue
                db.query(ReviewQueue).filter(ReviewQueue.submission_id == submission_id).delete()
        
        db.commit()
        return review

    @staticmethod
    def detect_plagiarism(db: Session, submission_id: int):
        # Placeholder for AI/Code similarity check
        import random
        similarity = random.uniform(0.01, 0.15)
        is_flagged = similarity > 0.8
        return {"similarity_score": similarity, "is_flagged": is_flagged}

    @staticmethod
    def seed_game_data(db: Session, institution_id: int):
        from app.db.models import Season, Squad, Badge
        from datetime import datetime, timedelta
        
        # 1. Season
        season = db.query(Season).filter(Season.is_active == True).first()
        if not season:
            season = Season(
                name="Season 4: Spring Sprint",
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=28)
            )
            db.add(season)
            
        # 2. Squads
        squad_names = ["Senior Fullstack Squad", "Cloud Navigators", "Data Deities", "AI Architects"]
        for name in squad_names:
            exists = db.query(Squad).filter(Squad.name == name, Squad.institution_id == institution_id).first()
            if not exists:
                squad = Squad(name=name, institution_id=institution_id, goal_xp=5000, current_xp=random.randint(1000, 4500))
                db.add(squad)
                
        # 3. Badges
        badges = [
            ("Week Warrior", "Maintain a 7-day streak", "🔥"),
            ("Review Master", "Complete 10 peer reviews", "🧐"),
            ("Season Champ", "Finish in the top 100", "🏆")
        ]
        for name, desc, icon in badges:
            exists = db.query(Badge).filter(Badge.name == name).first()
            if not exists:
                badge = Badge(name=name, description=desc, icon_url=icon)
                db.add(badge)
                
        db.commit()
