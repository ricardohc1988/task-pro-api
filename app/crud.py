from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import models, schemas

def get_task(db: Session, task_id: int):
    """Busca un registro único por su clave primaria."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, 
    completed: Optional[bool] = None
):
    """
    Construye una consulta dinámica basada en los filtros proporcionados.
    Implementa búsqueda 'case-insensitive' en múltiples columnas.
    """
    query = db.query(models.Task)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                models.Task.title.ilike(search_filter),
                models.Task.description.ilike(search_filter)
            )
        )
    
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
        
    return query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    """Mapea el esquema de Pydantic al modelo de SQLAlchemy y persiste el dato."""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, db_task: models.Task):
    """Lógica simple de 'toggle' para el estado de completado."""
    db_task.completed = not db_task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: models.Task):
    """Elimina el registro de la sesión y confirma la transacción."""
    db.delete(db_task)
    db.commit()
    return True

def get_task_stats(db: Session):
    """Realiza cálculos agregados directamente en el motor de base de datos."""
    total = db.query(models.Task).count()
    
    completed = db.query(models.Task).filter(models.Task.completed).count()
    
    pending = total - completed
    
    percentage = (completed / total * 100) if total > 0 else 0
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": round(percentage, 2)
    }