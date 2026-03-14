from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.domains.identity.dependencies import get_current_user, RoleChecker
from app.db.models import User, UserRole
from app.domains.tpo.service import TPOService
from app.domains.tpo.schemas import (
    TPOProfileCreate, TPOProfileUpdate, TPOProfileResponse,
    PlacementDriveCreate, PlacementDriveUpdate, PlacementDriveResponse,
    StudentManagementInfo, DriveParticipationUpdate, StudentDriveStatusResponse
)
from app.core.exceptions import AppException

router = APIRouter()

# TPO role check for all routes in this router
tpo_only = RoleChecker(allowed_roles=[UserRole.TPO])

@router.get("/me", response_model=TPOProfileResponse)
def get_my_tpo_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    if not profile:
        raise AppException("TPO profile not found", status.HTTP_404_NOT_FOUND)
    return profile

@router.post("/me", response_model=TPOProfileResponse, status_code=status.HTTP_201_CREATED)
def create_my_tpo_profile(
    data: TPOProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    return TPOService.create_tpo_profile(db, current_user.id, data)

@router.put("/me", response_model=TPOProfileResponse)
def update_my_tpo_profile(
    data: TPOProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    return TPOService.update_tpo_profile(db, current_user.id, data)

# Placement Drives
@router.post("/drives", response_model=PlacementDriveResponse, status_code=status.HTTP_201_CREATED)
def create_drive(
    data: PlacementDriveCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    if not profile:
        raise AppException("Complete your TPO profile first", status.HTTP_400_BAD_REQUEST)
    return TPOService.create_placement_drive(db, profile.institution_id, data)

@router.get("/drives", response_model=List[PlacementDriveResponse])
def get_drives(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    if not profile:
        return []
    return TPOService.get_placement_drives(db, profile.institution_id)

@router.get("/drives/{drive_id}", response_model=PlacementDriveResponse)
def get_drive(
    drive_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    if not profile:
        raise AppException("TPO profile not found", status.HTTP_404_NOT_FOUND)
    return TPOService.get_placement_drive(db, drive_id, profile.institution_id)

@router.put("/drives/{drive_id}", response_model=PlacementDriveResponse)
def update_drive(
    drive_id: int,
    data: PlacementDriveUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    return TPOService.update_placement_drive(db, drive_id, profile.institution_id, data)

@router.delete("/drives/{drive_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drive(
    drive_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    TPOService.delete_placement_drive(db, drive_id, profile.institution_id)

# Student Management
@router.get("/students", response_model=List[StudentManagementInfo])
def list_students(
    branch: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    if not profile:
        return []
    return TPOService.list_institution_students(db, profile.institution_id, branch)

@router.post("/drives/{drive_id}/students", response_model=StudentDriveStatusResponse)
def update_student_drive_status(
    drive_id: int,
    data: DriveParticipationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    return TPOService.associate_student_with_drive(db, drive_id, profile.institution_id, data)

@router.get("/drives/{drive_id}/students", response_model=List[StudentDriveStatusResponse])
def get_drive_students(
    drive_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(tpo_only)
):
    profile = TPOService.get_tpo_profile(db, current_user.id)
    return TPOService.get_drive_participants(db, drive_id, profile.institution_id)
