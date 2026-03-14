from fastapi import APIRouter

from app.domains.identity.router import router as identity_router

api_router = APIRouter()

api_router.include_router(identity_router, prefix="/auth", tags=["auth"])

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
