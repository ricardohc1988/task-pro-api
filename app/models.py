"""Modelos de Datos para SQLAlchemy.

Define la estructura de las tablas en la base de datos PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Task(Base):
    """Modelo de base de datos para una Tarea.

    Atributos:
        id (int): Identificador único (Clave Primaria).
        title (str): Título corto de la tarea.
        description (str): Detalle extendido de la tarea.
        completed (bool): Estado de finalización.
        created_at (datetime): Marca de tiempo de creación automática.
        updated_at (datetime): Marca de tiempo de la última actualización.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)