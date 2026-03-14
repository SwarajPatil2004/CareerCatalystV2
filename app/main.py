from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.router import api_router
from app.core.exceptions import global_exception_handler, AppException

# Initialize logging
setup_logging()

app = FastAPI(
    title="CareerCatalyst API",
    description="Production-grade web platform for career development.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handling
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(AppException, global_exception_handler)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to CareerCatalyst API"}
