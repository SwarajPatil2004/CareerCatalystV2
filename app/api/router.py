from fastapi import APIRouter

from app.domains.identity.router import router as identity_router
from app.domains.student.router import router as student_router
from app.domains.tpo.router import router as tpo_router
from app.domains.roadmap.router import router as roadmap_router
from app.domains.admin.router import router as admin_router
from app.domains.interview.router import router as interview_router
from app.domains.student.p2p_router import router as p2p_router
from app.domains.recruiter.router import router as recruiter_router
from app.domains.portfolio.router import router as portfolio_router

api_router = APIRouter()
api_router.include_router(identity_router, prefix="/auth", tags=["auth"])
api_router.include_router(student_router, prefix="/students", tags=["student"])
api_router.include_router(tpo_router, prefix="/tpo", tags=["tpo"])
api_router.include_router(roadmap_router, prefix="/roadmaps", tags=["roadmap"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(interview_router, prefix="/interviews", tags=["interview"])
api_router.include_router(p2p_router, prefix="/p2p", tags=["p2p"])
api_router.include_router(recruiter_router, prefix="/recruiter", tags=["recruiter"])
api_router.include_router(portfolio_router, tags=["portfolio"])

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
