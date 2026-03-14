from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.router import api_router
from fastapi.responses import RedirectResponse
from app.core.exceptions import global_exception_handler, AppException

# Initialize logging
setup_logging()

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT_DEFAULT])

app = FastAPI(
    title="CareerCatalyst API",
    description="Production-grade web platform for career development.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handling
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AppException, global_exception_handler)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

@app.get("/ready")
async def readiness_check():
    # In a real app, verify DB connection here
    return {"status": "ready"}

@app.get("/flower")
async def flower_redirect():
    # This assumes Flower is running and accessible on port 5555
    # In a production setup with a reverse proxy, this might change
    return RedirectResponse(url="http://localhost:5555")

@app.get("/")
async def root():
    return {"message": "Welcome to CareerCatalyst API"}
