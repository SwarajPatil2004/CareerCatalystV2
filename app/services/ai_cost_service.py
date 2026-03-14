from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.models import AICostLog, InstitutionBudget, Institution
import logging

logger = logging.getLogger(__name__)

# Prices per 1M tokens (as per user request/market standard)
# Groq Llama-3.3-70b: $0.59/M
# Gemini 2.0 Flash: $0.15/M
PRICING = {
    "llama-3.3-70b": {"input": 0.59, "output": 0.59}, # Simplified for now
    "gemini-2.0-flash": {"input": 0.15, "output": 0.15}
}

class AICostService:
    @staticmethod
    def log_usage(db: Session, user_id: int, institution_id: int, model: str, tokens_in: int, tokens_out: int):
        price = PRICING.get(model, {"input": 0, "output": 0})
        cost = ((tokens_in * price["input"]) + (tokens_out * price["output"])) / 1_000_000
        
        log = AICostLog(
            user_id=user_id,
            institution_id=institution_id,
            model_name=model,
            input_tokens=tokens_in,
            output_tokens=tokens_out,
            cost=cost
        )
        db.add(log)
        
        # Update institution spend
        budget = db.query(InstitutionBudget).filter(InstitutionBudget.institution_id == institution_id).first()
        if not budget:
            budget = InstitutionBudget(institution_id=institution_id)
            db.add(budget)
        
        budget.current_spend += cost
        db.commit()
        return log

    @staticmethod
    def is_within_budget(db: Session, institution_id: int) -> bool:
        budget = db.query(InstitutionBudget).filter(InstitutionBudget.institution_id == institution_id).first()
        if not budget:
            return True # No budget set yet
        return budget.current_spend < budget.monthly_cap

    @staticmethod
    def get_founder_dashboard_data(db: Session):
        total_spend = db.query(func.sum(AICostLog.cost)).scalar() or 0
        today = datetime.utcnow().date()
        daily_spend = db.query(func.sum(AICostLog.cost)).filter(func.date(AICostLog.timestamp) == today).scalar() or 0
        
        institution_stats = db.query(
            Institution.name,
            InstitutionBudget.current_spend,
            InstitutionBudget.monthly_cap
        ).join(InstitutionBudget, Institution.id == InstitutionBudget.institution_id).all()
        
        return {
            "total_spend": total_spend,
            "daily_spend": daily_spend,
            "institutions": [dict(zip(["name", "spend", "cap"], i)) for i in institution_stats]
        }
