from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.student import (
    StudentProfileOut, StudentProfileUpdate,
    SkillOut, SkillCreate,
    ExperienceOut, ExperienceCreate,
    CertificateOut, CertificateCreate,
    AchievementOut, AchievementCreate,
    ProjectOut, ProjectCreate
)
from app.services.student_service import StudentService

router = APIRouter()

# --- Profile ---
@router.get("/me/profile", response_model=StudentProfileOut)
def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.get_profile(db, current_user.id)

@router.put("/me/profile", response_model=StudentProfileOut)
def update_my_profile(profile_in: StudentProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.update_profile(db, current_user.id, profile_in)

# --- Skills ---
@router.get("/me/skills", response_model=List[SkillOut])
def get_my_skills(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.get_skills(db, current_user.id)

@router.post("/me/skills", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def add_skill(skill_in: SkillCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.create_skill(db, current_user.id, skill_in)

@router.delete("/me/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_skill(skill_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    StudentService.delete_skill(db, current_user.id, skill_id)

# --- Experiences ---
@router.get("/me/experiences", response_model=List[ExperienceOut])
def get_my_experiences(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.get_experiences(db, current_user.id)

@router.post("/me/experiences", response_model=ExperienceOut, status_code=status.HTTP_201_CREATED)
def add_experience(exp_in: ExperienceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.create_experience(db, current_user.id, exp_in)

@router.delete("/me/experiences/{exp_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_experience(exp_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    StudentService.delete_experience(db, current_user.id, exp_id)

# --- Certificates ---
@router.get("/me/certificates", response_model=List[CertificateOut])
def get_my_certificates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.get_certificates(db, current_user.id)

@router.post("/me/certificates", response_model=CertificateOut, status_code=status.HTTP_201_CREATED)
def add_certificate(cert_in: CertificateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.create_certificate(db, current_user.id, cert_in)

@router.delete("/me/certificates/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_certificate(cert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    StudentService.delete_certificate(db, current_user.id, cert_id)

# --- Achievements ---
@router.get("/me/achivements", response_model=List[AchievementOut])
def get_my_achievements(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.get_achievements(db, current_user.id)

@router.post("/me/achivements", response_model=AchievementOut, status_code=status.HTTP_201_CREATED)
def add_achievement(ach_in: AchievementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.create_achievement(db, current_user.id, ach_in)

@router.delete("/me/achivements/{ach_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_achievement(ach_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    StudentService.delete_achievement(db, current_user.id, ach_id)

# --- Projects ---
@router.get("/me/projects", response_model=List[ProjectOut])
def get_my_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.get_projects(db, current_user.id)

@router.post("/me/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def add_project(proj_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StudentService.create_project(db, current_user.id, proj_in)

@router.delete("/me/projects/{proj_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project(proj_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    StudentService.delete_project(db, current_user.id, proj_id)
