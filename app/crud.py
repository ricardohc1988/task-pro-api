"""Operaciones CRUD y Lógica de Negocio.

Este módulo encapsula todas las interacciones con la base de datos a través
de SQLAlchemy, separando la lógica de persistencia de las rutas de la API.
"""

from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import models, schemas

def get_task(db: Session, task_id: int):
    """Busca un registro único por su clave primaria.

    Args:
        db (Session): Sesión activa de base de datos.
        task_id (int): ID de la tarea a buscar.

    Returns:
        models.Task: El objeto de la tarea si se encuentra, de lo contrario None.
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, 
    completed: Optional[bool] = None
):
    """Obtiene una lista de tareas con opciones de filtrado y paginación.

    Implementa búsqueda 'case-insensitive' en título y descripción simultáneamente.

    Args:
        db (Session): Sesión activa de base de datos.
        skip (int): Número de registros a saltar (paginación).
        limit (int): Máximo de registros a retornar.
        search (Optional[str]): Palabra clave para filtrar título/descripción.
        completed (Optional[bool]): Filtrar por estado de finalización.

    Returns:
        list[models.Task]: Lista de tareas que coinciden con los criterios.
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
    """Crea una nueva tarea en la base de datos.

    Args:
        db (Session): Sesión activa de base de datos.
        task (schemas.TaskCreate): Datos de la tarea a crear.

    Returns:
        models.Task: El registro recién creado con su ID asignado.
    """
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: models.Task, task_update: schemas.TaskUpdate):
    """Actualiza una tarea existente de forma parcial.

    Solo modifica los campos que fueron enviados en la petición.

    Args:
        db (Session): Sesión activa de base de datos.
        db_task (models.Task): Objeto de tarea original.
        task_update (schemas.TaskUpdate): Nuevos datos a aplicar.

    Returns:
        models.Task: La tarea actualizada.
    """
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, db_task: models.Task):
    """Alterna el estado 'completed' de una tarea.

    Args:
        db (Session): Sesión activa de base de datos.
        db_task (models.Task): La tarea cuyo estado se desea cambiar.

    Returns:
        models.Task: La tarea con el estado invertido.
    """
    db_task.completed = not db_task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: models.Task):
    """Elimina físicamente una tarea de la base de datos.

    Args:
        db (Session): Sesión activa de base de datos.
        db_task (models.Task): La tarea a borrar.

    Returns:
        bool: True si la operación fue exitosa.
    """
    db.delete(db_task)
    db.commit()
    return True

def get_task_stats(db: Session):
    """Calcula estadísticas agregadas sobre las tareas.

    Realiza los cálculos directamente en el motor de base de datos para eficiencia.

    Args:
        db (Session): Sesión activa de base de datos.

    Returns:
        dict: Diccionario con total, completadas, pendientes y porcentaje.
    """
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