from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class ProjectSubmissionCreate(BaseModel):
    project_id: int
    title: str
    code_url: str

class ProjectReviewSubmit(BaseModel):
    submission_id: int
    rubric_scores: Dict[str, int]
    feedback: str

class GamificationStatsResponse(BaseModel):
    total_xp: int
    streak_days: int
    streak_buffer: int
    last_active: Optional[datetime]
    squad_name: Optional[str]

class LeaderboardEntry(BaseModel):
    name: str
    xp: int
    rank: int
