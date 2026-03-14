from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TPO = "tpo"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, Column("user_id", Integer, index=True), nullable=False)
    headline = Column(String)
    current_year = Column(Integer)
    branch = Column(String)
    college_name = Column(String)
    location = Column(String)
    github_link = Column(String)
    linkedin_link = Column(String)
    portfolio_link = Column(String)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    level = Column(String)  # beginner, intermediate, advanced
    category = Column(String) # language, framework, tool

class Experience(Base):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String)
    link = Column(String)

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    description = Column(String)
    received_date = Column(DateTime)
    expiry_date = Column(DateTime)
    link = Column(String)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(DateTime)
    description = Column(String)
    link = Column(String)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String)
    tech_stack = Column(String)
    github_link = Column(String)
    demo_link = Column(String)
    impact = Column(String)
