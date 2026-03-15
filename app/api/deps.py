from typing import List
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.db.constants import UserRole
from app.core.config import settings
from app.schemas.auth import TokenData
from app.core.exceptions import AppException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise AppException(
                message="Could not validate credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        token_data = TokenData(email=email)
    except JWTError:
        raise AppException(
            message="Could not validate credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise AppException(
            message="User not found",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise AppException(
                message="You do not have enough permissions",
                status_code=status.HTTP_403_FORBIDDEN
            )
        return user
