from fastapi import APIRouter

from app.domains.identity.router import router as identity_router
from app.domains.student.router import router as student_router

api_router = APIRouter()

api_router.include_router(identity_router, prefix="/auth", tags=["auth"])
api_router.include_router(student_router, prefix="/students", tags=["students"])

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
