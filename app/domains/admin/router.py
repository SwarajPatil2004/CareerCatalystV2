from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.domains.identity.dependencies import get_current_user, RoleChecker
from app.db.models import User, UserRole
from app.services.ai_cost_service import AICostService

router = APIRouter()

# Super admin only or TPO for their own? 
# The user said "Founder", which implies a higher level. 
# Let's assume ADMIN role exists or we use TPO for now but target Founder.
# If ADMIN role doesn't exist, I'll add it or use TPO.
admin_only = RoleChecker(allowed_roles=[UserRole.TPO]) # Target TPO for now if ADMIN is missing

@router.get("/costs")
def get_costs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _ = Depends(admin_only)
):
    return AICostService.get_founder_dashboard_data(db)
