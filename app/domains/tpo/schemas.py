from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.db.models import InstitutionType, DriveStatus, StudentDriveStatus

class InstitutionBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    type: InstitutionType = InstitutionType.OTHER

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    type: Optional[InstitutionType] = None

class InstitutionResponse(InstitutionBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TPOProfileBase(BaseModel):
    institution_id: int
    designation: Optional[str] = None
    contact_number: Optional[str] = None

class TPOProfileCreate(TPOProfileBase):
    pass

class TPOProfileUpdate(BaseModel):
    institution_id: Optional[int] = None
    designation: Optional[str] = None
    contact_number: Optional[str] = None

class TPOProfileResponse(TPOProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PlacementDriveBase(BaseModel):
    title: str
    company_name: str
    role: str
    job_description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    application_deadline: Optional[datetime] = None
    status: DriveStatus = DriveStatus.UPCOMING

class PlacementDriveCreate(PlacementDriveBase):
    pass

class PlacementDriveUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    job_description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    application_deadline: Optional[datetime] = None
    status: Optional[DriveStatus] = None

class PlacementDriveResponse(PlacementDriveBase):
    id: int
    institution_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StudentManagementInfo(BaseModel):
    id: int
    full_name: str
    headline: Optional[str] = None
    current_year: Optional[int] = None
    branch: Optional[str] = None
    last_active_date: datetime
    profile_completeness: float = 0.0 # Will be calculated

class DriveParticipationUpdate(BaseModel):
    student_profile_id: int
    status: StudentDriveStatus

class StudentDriveStatusResponse(BaseModel):
    student_profile_id: int
    drive_id: int
    status: StudentDriveStatus
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)
