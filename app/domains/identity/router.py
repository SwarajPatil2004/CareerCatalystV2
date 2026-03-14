from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.db.models import User
from app.core.exceptions import AppException

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_in)

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise AppException(
            message="Incorrect email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    access_token = AuthService.create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
