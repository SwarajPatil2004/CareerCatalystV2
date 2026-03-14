from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey, Text, Table, JSON
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
    analysis_results = Column(JSON, nullable=True)

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

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    career_type = Column(String) # e.g., full_stack, data_science
    is_active = Column(Integer, default=1) # Using int as bool for SQLite compatibility if needed, but project uses Postgres
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    phases = relationship("RoadmapPhase", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapPhase(Base):
    __tablename__ = "roadmap_phases"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    phase_index = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)

    roadmap = relationship("Roadmap", back_populates="phases")
    tasks = relationship("RoadmapTask", back_populates="phase", cascade="all, delete-orphan")

class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id = Column(Integer, primary_key=True, index=True)
    phase_id = Column(Integer, ForeignKey("roadmap_phases.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    resource_link = Column(String)
    xp = Column(Integer, default=10)

    phase = relationship("RoadmapPhase", back_populates="tasks")

class UserRoadmapProgress(Base):
    __tablename__ = "user_roadmap_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    completed_task_ids = Column(JSON, default=[]) # Storing as array of IDs
    total_xp = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String)  # e.g., "login", "task_complete", "resume_edit"
    metadata_json = Column(JSON, default={})
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

class StudentMetrics(Base):
    __tablename__ = "student_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    activity_score = Column(Integer, default=0)
    xp_gained = Column(Integer, default=0)
    completeness_score = Column(Float, default=0.0)

    user = relationship("User")
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class InstitutionBudget(Base):
    __tablename__ = "institution_budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), unique=True)
    monthly_cap = Column(Float, default=10.0) # $10 free tier
    current_spend = Column(Float, default=0.0)
    last_reset = Column(DateTime(timezone=True), server_default=func.now())

    institution = relationship("Institution")

class AICostLog(Base):
    __tablename__ = "ai_cost_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    institution_id = Column(Integer, ForeignKey("institutions.id"))
    model_name = Column(String) # e.g., "gemini-2.0-flash", "llama-3.3-70b"
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    cost = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    institution = relationship("Institution")

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    track = Column(String) # e.g., "full_stack", "data_science"
    status = Column(String, default="active") # active, completed, cancelled
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_score = Column(Float, default=0.0)
    xp_earned = Column(Integer, default=0)

    user = relationship("User")

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    text = Column(Text)
    type = Column(String) # technical, behavioral
    order = Column(Integer)

    session = relationship("InterviewSession")

class InterviewResponse(Base):
    __tablename__ = "interview_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("interview_questions.id"))
    transcript = Column(Text)
    audio_url = Column(String, nullable=True)
    evaluation_json = Column(JSON, default={})
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("InterviewQuestion")

class InterviewProctoringLog(Base):
    __tablename__ = "interview_proctoring_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    event_type = Column(String) # tab_switch, blur
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("InterviewSession")
