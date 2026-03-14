from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import UserGamificationStats, Season, Squad, UserBadge, Badge, AnalyticsEvent
from datetime import datetime, timedelta
from typing import List, Dict, Any

class GamificationService:
    @staticmethod
    def update_stats(db: Session, user_id: int, xp_gain: int):
        stats = db.query(UserGamificationStats).filter(UserGamificationStats.user_id == user_id).first()
        if not stats:
            stats = UserGamificationStats(user_id=user_id, total_xp=0, streak_days=0, streak_buffer=0)
            db.add(stats)
        
        stats.total_xp += xp_gain
        
        # Streak Logic
        now = datetime.utcnow()
        if stats.last_active:
            diff = now - stats.last_active
            if diff.days == 1:
                stats.streak_days += 1
            elif diff.days > 1:
                if stats.streak_buffer > 0:
                    stats.streak_buffer -= 1
                    # Streak maintained via buffer
                else:
                    stats.streak_days = 1
        else:
            stats.streak_days = 1
            
        stats.last_active = now
        
        # Squad progress
        if stats.squad_id:
            squad = db.query(Squad).filter(Squad.id == stats.squad_id).first()
            if squad:
                squad.current_xp += xp_gain
        
        db.commit()
        db.refresh(stats)
        return stats

    @staticmethod
    def get_leaderboard(db: Session, type: str, scope_id: int = None):
        if type == "individual":
            return db.query(UserGamificationStats).order_by(desc(UserGamificationStats.total_xp)).limit(10).all()
        elif type == "squad":
            return db.query(Squad).order_by(desc(Squad.current_xp)).limit(10).all()
        elif type == "institution":
            # Aggregated by institution via squads
            return db.query(Squad.institution_id, func.sum(Squad.current_xp).label("total_xp")).group_by(
                Squad.institution_id
            ).order_by(desc("total_xp")).limit(10).all()
        return []

    @staticmethod
    def check_badges(db: Session, user_id: int):
        stats = db.query(UserGamificationStats).filter(UserGamificationStats.user_id == user_id).first()
        if not stats: return []
        
        new_badges = []
        # Example: 7-day streak badge
        if stats.streak_days >= 7:
            badge = db.query(Badge).filter(Badge.name == "Week Warrior").first()
            if badge:
                exists = db.query(UserBadge).filter(
                    UserBadge.user_id == user_id, 
                    UserBadge.badge_id == badge.id
                ).first()
                if not exists:
                    ub = UserBadge(user_id=user_id, badge_id=badge.id)
                    db.add(ub)
                    new_badges.append(badge)
        
        db.commit()
        return new_badges
