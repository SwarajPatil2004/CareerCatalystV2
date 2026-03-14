from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import StudentProfile, Skill, Experience, Certificate, Achievement, Project
from app.schemas.student import (
    StudentProfileUpdate, SkillCreate, ExperienceCreate, 
    CertificateCreate, AchievementCreate, ProjectCreate
)
from app.services.skill_intelligence import SkillIntelligenceService
from app.core.exceptions import AppException
from fastapi import status
from app.tasks.ai import analyze_resume_with_ai

class StudentService:
    # --- Profile ---
    @staticmethod
    def get_profile(db: Session, user_id: int):
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        if not profile:
            # Auto-create profile if it doesn't exist
            profile = StudentProfile(user_id=user_id)
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile

    @staticmethod
    def update_profile(db: Session, user_id: int, profile_in: StudentProfileUpdate):
        profile = StudentService.get_profile(db, user_id)
        for field, value in profile_in.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
        db.commit()
        db.refresh(profile)
        
        # Trigger background profile analysis
        analyze_resume_with_ai.delay(user_id, profile_in.model_dump())
        
        return profile

    # --- Skills ---
    @staticmethod
    def get_skills(db: Session, user_id: int):
        return db.query(Skill).filter(Skill.user_id == user_id).all()

    @staticmethod
    def create_skill(db: Session, user_id: int, skill_in: SkillCreate):
        db_skill = Skill(**skill_in.model_dump(), user_id=user_id)
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
        return db_skill

    @staticmethod
    def delete_skill(db: Session, user_id: int, skill_id: int):
        skill = db.query(Skill).filter(Skill.id == skill_id, Skill.user_id == user_id).first()
        if not skill:
            raise AppException("Skill not found", status.HTTP_404_NOT_FOUND)
        db.delete(skill)
        db.commit()

    # --- Experiences ---
    @staticmethod
    def get_experiences(db: Session, user_id: int):
        return db.query(Experience).filter(Experience.user_id == user_id).all()

    @staticmethod
    def create_experience(db: Session, user_id: int, exp_in: ExperienceCreate):
        analysis = None
        if exp_in.description:
            analysis = SkillIntelligenceService.analyze_bullet_point(exp_in.description).model_dump()
            
        db_exp = Experience(**exp_in.model_dump(), user_id=user_id, analysis_results=analysis)
        db.add(db_exp)
        db.commit()
        db.refresh(db_exp)
        
        # Trigger background analysis
        analyze_resume_with_ai.delay(user_id, exp_in.model_dump())
        
        return db_exp

    @staticmethod
    def delete_experience(db: Session, user_id: int, exp_id: int):
        exp = db.query(Experience).filter(Experience.id == exp_id, Experience.user_id == user_id).first()
        if not exp:
            raise AppException("Experience not found", status.HTTP_404_NOT_FOUND)
        db.delete(exp)
        db.commit()

    # --- Certificates ---
    @staticmethod
    def get_certificates(db: Session, user_id: int):
        return db.query(Certificate).filter(Certificate.user_id == user_id).all()

    @staticmethod
    def create_certificate(db: Session, user_id: int, cert_in: CertificateCreate):
        db_cert = Certificate(**cert_in.model_dump(), user_id=user_id)
        db.add(db_cert)
        db.commit()
        db.refresh(db_cert)
        return db_cert

    @staticmethod
    def delete_certificate(db: Session, user_id: int, cert_id: int):
        cert = db.query(Certificate).filter(Certificate.id == cert_id, Certificate.user_id == user_id).first()
        if not cert:
            raise AppException("Certificate not found", status.HTTP_404_NOT_FOUND)
        db.delete(cert)
        db.commit()

    # --- Achievements ---
    @staticmethod
    def get_achievements(db: Session, user_id: int):
        return db.query(Achievement).filter(Achievement.user_id == user_id).all()

    @staticmethod
    def create_achievement(db: Session, user_id: int, ach_in: AchievementCreate):
        db_ach = Achievement(**ach_in.model_dump(), user_id=user_id)
        db.add(db_ach)
        db.commit()
        db.refresh(db_ach)
        return db_ach

    @staticmethod
    def delete_achievement(db: Session, user_id: int, ach_id: int):
        ach = db.query(Achievement).filter(Achievement.id == ach_id, Achievement.user_id == user_id).first()
        if not ach:
            raise AppException("Achievement not found", status.HTTP_404_NOT_FOUND)
        db.delete(ach)
        db.commit()

    # --- Projects ---
    @staticmethod
    def get_projects(db: Session, user_id: int):
        return db.query(Project).filter(Project.user_id == user_id).all()

    @staticmethod
    def create_project(db: Session, user_id: int, proj_in: ProjectCreate):
        analysis = None
        if proj_in.summary:
            analysis = SkillIntelligenceService.analyze_bullet_point(proj_in.summary).model_dump()
            
        db_proj = Project(**proj_in.model_dump(), user_id=user_id, analysis_results=analysis)
        db.add(db_proj)
        db.commit()
        db.refresh(db_proj)
        
        # Trigger background analysis
        analyze_resume_with_ai.delay(user_id, proj_in.model_dump())
        
        return db_proj

    @staticmethod
    def delete_project(db: Session, user_id: int, proj_id: int):
        proj = db.query(Project).filter(Project.id == proj_id, Project.user_id == user_id).first()
        if not proj:
            raise AppException("Project not found", status.HTTP_404_NOT_FOUND)
        db.delete(proj)
        db.commit()
