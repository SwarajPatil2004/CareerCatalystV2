from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TPO = "tpo"

class InstitutionType(str, enum.Enum):
    ENGINEERING = "engineering"
    MANAGEMENT = "management"
    OTHER = "other"

class DriveStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class StudentDriveStatus(str, enum.Enum):
    INVITED = "invited"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    SELECTED = "selected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    tpo_profile = relationship("TPOProfile", back_populates="user", uselist=False)

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    type = Column(SQLEnum(InstitutionType), default=InstitutionType.OTHER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tpo_profiles = relationship("TPOProfile", back_populates="institution")
    student_profiles = relationship("StudentProfile", back_populates="institution")
    placement_drives = relationship("PlacementDrive", back_populates="institution")

class TPOProfile(Base):
    __tablename__ = "tpo_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    designation = Column(String)
    contact_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="tpo_profile")
    institution = relationship("Institution", back_populates="tpo_profiles")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    headline = Column(String)
    current_year = Column(Integer)
    branch = Column(String)
    college_name = Column(String)
    location = Column(String)
    github_link = Column(String)
    linkedin_link = Column(String)
    portfolio_link = Column(String)
    last_active_date = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="student_profile")
    institution = relationship("Institution", back_populates="student_profiles")
    drive_associations = relationship("StudentDriveAssociation", back_populates="student")

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

class PlacementDrive(Base):
    __tablename__ = "placement_drives"

    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    job_description = Column(Text)
    eligibility_criteria = Column(Text)
    application_deadline = Column(DateTime)
    status = Column(SQLEnum(DriveStatus), default=DriveStatus.UPCOMING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    institution = relationship("Institution", back_populates="placement_drives")
    student_associations = relationship("StudentDriveAssociation", back_populates="drive")

class StudentDriveAssociation(Base):
    __tablename__ = "student_drive_associations"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    drive_id = Column(Integer, ForeignKey("placement_drives.id"), nullable=False)
    status = Column(SQLEnum(StudentDriveStatus), default=StudentDriveStatus.INVITED)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    student = relationship("StudentProfile", back_populates="drive_associations")
    drive = relationship("PlacementDrive", back_populates="student_associations")
