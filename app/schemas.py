from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=50, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=250, description="Descripción de la tarea")

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_percentage: float