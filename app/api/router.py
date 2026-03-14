from fastapi import APIRouter

from app.domains.identity.router import router as identity_router
from app.domains.student.router import router as student_router
from app.domains.tpo.router import router as tpo_router
from app.domains.roadmap.router import router as roadmap_router

api_router = APIRouter()
api_router.include_router(identity_router, prefix="/auth", tags=["auth"])
api_router.include_router(student_router, prefix="/students", tags=["students"])
api_router.include_router(tpo_router, prefix="/tpo", tags=["tpo"])
api_router.include_router(roadmap_router, prefix="/roadmaps", tags=["roadmaps"])

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
