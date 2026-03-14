from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import AppException
from fastapi import status
from app.tasks.email import send_email_verification
from app.services.analytics_service import AnalyticsService

class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def register_user(db: Session, user_in: UserCreate):
        if AuthService.get_user_by_email(db, user_in.email):
            raise AppException(
                message="User with this email already exists",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Trigger background verification email
        send_email_verification.delay(db_user.id, db_user.email)
        
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = AuthService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        # Track login event
        AnalyticsService.track_event(db, user.id, "login", {"email": email})
        
        return user

    @staticmethod
    def create_user_token(user: User):
        return create_access_token(subject=user.email)
