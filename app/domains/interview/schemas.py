from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any

class InterviewStart(BaseModel):
    track: str = Field(..., description="Role track e.g. full_stack")

class InterviewQuestionResponse(BaseModel):
    id: int
    text: str
    type: str
    order: int

class InterviewSessionResponse(BaseModel):
    id: int
    track: str
    status: str
    start_time: datetime
    questions: List[InterviewQuestionResponse]

    class Config:
        from_attributes = True

class InterviewResponseSubmit(BaseModel):
    question_id: int
    transcript: str

class ProctoringEvent(BaseModel):
    event_type: str # tab_switch, blur

class InterviewEvaluationResponse(BaseModel):
    communication_score: float
    technical_score: float
    behavioral_score: float
    feedback: str
    suggestions: List[str]

class InterviewReport(BaseModel):
    session_id: int
    track: str
    score: float
    results: List[Dict[str, Any]]
