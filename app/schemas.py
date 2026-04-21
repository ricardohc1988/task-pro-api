"""Esquemas de Validación de Datos (Pydantic).

Define los contratos de entrada y salida para la API, asegurando la integridad
de los datos y la documentación automática en Swagger.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    """Esquema base con los campos comunes de una Tarea."""
    title: str = Field(min_length=3, max_length=50, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=250, description="Descripción de la tarea")

class TaskCreate(TaskBase):
    """Esquema para la creación de una nueva Tarea."""
    pass

class TaskResponse(TaskBase):
    """Esquema para las respuestas de la API, incluye campos generados por el servidor."""
    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskUpdate(TaskBase):
    """Esquema para actualizaciones parciales o totales de una Tarea."""
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=250)

class TaskStats(BaseModel):
    """Esquema para las estadísticas globales de productividad."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_percentage: float
