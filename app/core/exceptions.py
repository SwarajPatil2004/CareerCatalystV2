from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional

class AppException(Exception):
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details

APIException = AppException

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "details": exc.details,
                    "code": exc.status_code
                }
            }
        )
    
    # Fallback for unhandled exceptions
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "details": str(exc) if hasattr(exc, "message") else "Internal Server Error",
                "code": 500
            }
        }
    )
