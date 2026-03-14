from sqlalchemy.orm import Session
from app.services.ai_cost_service import AICostService
from app.core.exceptions import AppException
from fastapi import status
import random # Placeholder for real AI calls

class AIProviderService:
    @staticmethod
    def call_gemini(db: Session, user_id: int, institution_id: int, prompt: str):
        if not AICostService.is_within_budget(db, institution_id):
            raise AppException("Institution AI budget exceeded", status.HTTP_402_PAYMENT_REQUIRED)
        
        # Simulate API call and token counting
        tokens_in = len(prompt) // 4
        tokens_out = random.randint(50, 500)
        
        # Log cost
        AICostService.log_usage(db, user_id, institution_id, "gemini-2.0-flash", tokens_in, tokens_out)
        
        return f"Gemini response for: {prompt[:20]}..."

    @staticmethod
    def call_groq(db: Session, user_id: int, institution_id: int, prompt: str):
        if not AICostService.is_within_budget(db, institution_id):
            raise AppException("Institution AI budget exceeded", status.HTTP_402_PAYMENT_REQUIRED)
        
        tokens_in = len(prompt) // 4
        tokens_out = random.randint(50, 500)
        
        AICostService.log_usage(db, user_id, institution_id, "llama-3.3-70b", tokens_in, tokens_out)
        
        return f"Groq response for: {prompt[:20]}..."
