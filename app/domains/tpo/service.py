from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from app.db.models import (
    TPOProfile, Institution, PlacementDrive, StudentProfile, 
    StudentDriveAssociation, User, StudentDriveStatus
)
from app.domains.tpo.schemas import (
    TPOProfileCreate, TPOProfileUpdate, 
    PlacementDriveCreate, PlacementDriveUpdate,
    DriveParticipationUpdate
)
from app.core.exceptions import AppException
from fastapi import status

class TPOService:
    @staticmethod
    def get_tpo_profile(db: Session, user_id: int) -> Optional[TPOProfile]:
        return db.query(TPOProfile).filter(TPOProfile.user_id == user_id).first()

    @staticmethod
    def create_tpo_profile(db: Session, user_id: int, data: TPOProfileCreate) -> TPOProfile:
        existing = TPOService.get_tpo_profile(db, user_id)
        if existing:
            raise AppException("TPO profile already exists", status.HTTP_400_BAD_REQUEST)
        
        db_tpo = TPOProfile(user_id=user_id, **data.model_dump())
        db.add(db_tpo)
        db.commit()
        db.refresh(db_tpo)
        return db_tpo

    @staticmethod
    def update_tpo_profile(db: Session, user_id: int, data: TPOProfileUpdate) -> TPOProfile:
        db_tpo = TPOService.get_tpo_profile(db, user_id)
        if not db_tpo:
            raise AppException("TPO profile not found", status.HTTP_404_NOT_FOUND)
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_tpo, key, value)
        
        db.commit()
        db.refresh(db_tpo)
        return db_tpo

    @staticmethod
    def create_placement_drive(db: Session, institution_id: int, data: PlacementDriveCreate) -> PlacementDrive:
        db_drive = PlacementDrive(institution_id=institution_id, **data.model_dump())
        db.add(db_drive)
        db.commit()
        db.refresh(db_drive)
        return db_drive

    @staticmethod
    def get_placement_drives(db: Session, institution_id: int) -> List[PlacementDrive]:
        return db.query(PlacementDrive).filter(PlacementDrive.institution_id == institution_id).all()

    @staticmethod
    def get_placement_drive(db: Session, drive_id: int, institution_id: int) -> PlacementDrive:
        drive = db.query(PlacementDrive).filter(
            PlacementDrive.id == drive_id, 
            PlacementDrive.institution_id == institution_id
        ).first()
        if not drive:
            raise AppException("Placement drive not found", status.HTTP_404_NOT_FOUND)
        return drive

    @staticmethod
    def update_placement_drive(db: Session, drive_id: int, institution_id: int, data: PlacementDriveUpdate) -> PlacementDrive:
        db_drive = TPOService.get_placement_drive(db, drive_id, institution_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_drive, key, value)
        db.commit()
        db.refresh(db_drive)
        return db_drive

    @staticmethod
    def delete_placement_drive(db: Session, drive_id: int, institution_id: int):
        db_drive = TPOService.get_placement_drive(db, drive_id, institution_id)
        db.delete(db_drive)
        db.commit()

    @staticmethod
    def list_institution_students(db: Session, institution_id: int, branch: Optional[str] = None):
        query = db.query(StudentProfile, User.full_name).join(User, StudentProfile.user_id == User.id).filter(
            StudentProfile.institution_id == institution_id
        )
        if branch:
            query = query.filter(StudentProfile.branch == branch)
        
        students = query.all()
        result = []
        for profile, full_name in students:
            # Simple completeness calculation
            fields = [profile.headline, profile.branch, profile.college_name, profile.location, 
                      profile.github_link, profile.linkedin_link]
            completeness = (len([f for f in fields if f]) / len(fields)) * 100
            
            result.append({
                "id": profile.id,
                "full_name": full_name,
                "headline": profile.headline,
                "current_year": profile.current_year,
                "branch": profile.branch,
                "last_active_date": profile.last_active_date,
                "profile_completeness": completeness
            })
        return result

    @staticmethod
    def associate_student_with_drive(db: Session, drive_id: int, institution_id: int, data: DriveParticipationUpdate):
        # Verify drive belongs to TPO institution
        TPOService.get_placement_drive(db, drive_id, institution_id)
        
        # Verify student belongs to same institution
        student = db.query(StudentProfile).filter(
            StudentProfile.id == data.student_profile_id,
            StudentProfile.institution_id == institution_id
        ).first()
        if not student:
            raise AppException("Student not found in your institution", status.HTTP_404_NOT_FOUND)
        
        assoc = db.query(StudentDriveAssociation).filter(
            StudentDriveAssociation.drive_id == drive_id,
            StudentDriveAssociation.student_profile_id == data.student_profile_id
        ).first()
        
        if assoc:
            assoc.status = data.status
        else:
            assoc = StudentDriveAssociation(
                drive_id=drive_id,
                student_profile_id=data.student_profile_id,
                status=data.status
            )
            db.add(assoc)
        
        db.commit()
        db.refresh(assoc)
        return assoc

    @staticmethod
    def get_drive_participants(db: Session, drive_id: int, institution_id: int):
        # Verify drive
        TPOService.get_placement_drive(db, drive_id, institution_id)
        
        return db.query(StudentDriveAssociation).filter(
            StudentDriveAssociation.drive_id == drive_id
        ).all()
