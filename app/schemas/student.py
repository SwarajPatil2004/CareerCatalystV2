from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Any
from app.schemas.base import BaseSchema

# Profile Schemas
class StudentProfileBase(BaseSchema):
    headline: Optional[str] = None
    current_year: Optional[int] = None
    branch: Optional[str] = None
    college_name: Optional[str] = None
    location: Optional[str] = None
    github_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    portfolio_link: Optional[str] = None

class StudentProfileUpdate(StudentProfileBase):
    pass

class StudentProfileOut(StudentProfileBase):
    id: int
    user_id: int

# Skill Schemas
class SkillBase(BaseSchema):
    name: str
    level: str
    category: str

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    id: int

# Experience Schemas
class ExperienceBase(BaseSchema):
    title: str
    organization: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    link: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceOut(ExperienceBase):
    id: int
    analysis_results: Optional[Any] = None

# Certificate Schemas
class CertificateBase(BaseSchema):
    title: str
    organization: str
    description: Optional[str] = None
    received_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    link: Optional[str] = None

class CertificateCreate(CertificateBase):
    pass

class CertificateOut(CertificateBase):
    id: int

# Achievement Schemas
class AchievementBase(BaseSchema):
    title: str
    date: Optional[datetime] = None
    description: Optional[str] = None
    link: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class AchievementOut(AchievementBase):
    id: int

# Project Schemas
class ProjectBase(BaseSchema):
    title: str
    summary: Optional[str] = None
    tech_stack: Optional[str] = None
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    impact: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    analysis_results: Optional[Any] = None
