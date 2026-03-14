from typing import Optional
from pydantic import EmailStr, ConfigDict
from app.schemas.base import BaseSchema
from app.db.models import UserRole

class UserBase(BaseSchema):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserOut(UserBase):
    id: int
