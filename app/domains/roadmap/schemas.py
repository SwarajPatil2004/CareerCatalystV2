from typing import List, Optional
from pydantic import BaseModel
from app.schemas.base import BaseSchema

class RoadmapTaskBase(BaseSchema):
    title: str
    description: Optional[str] = None
    resource_link: Optional[str] = None
    xp: int = 10

class RoadmapTaskOut(RoadmapTaskBase):
    id: int
    phase_id: int

class RoadmapPhaseBase(BaseSchema):
    phase_index: int
    title: str
    description: Optional[str] = None

class RoadmapPhaseOut(RoadmapPhaseBase):
    id: int
    roadmap_id: int
    tasks: List[RoadmapTaskOut] = []

class RoadmapBase(BaseSchema):
    name: str
    slug: str
    description: Optional[str] = None
    career_type: str
    is_active: bool = True

class RoadmapOut(RoadmapBase):
    id: int
    phases: List[RoadmapPhaseOut] = []

class RoadmapSimpleOut(RoadmapBase):
    id: int

class UserRoadmapProgressOut(BaseSchema):
    roadmap_id: int
    completed_task_ids: List[int]
    total_xp: int

class RoadmapTaskComplete(BaseModel):
    task_id: int
