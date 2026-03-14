from fastapi import APIRouter

api_router = APIRouter()

# Placeholder for domain routers
# from app.domains.identity.router import router as identity_router
# api_router.include_router(identity_router, prefix="/identity", tags=["identity"])

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
