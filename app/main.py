"""Punto de Entrada de la API.

Este módulo define las rutas de FastAPI, la configuración global de la aplicación
y la integración de los manejadores de excepciones y dependencias.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database, crud, exceptions
from typing import Optional

# Inicializa la base de datos al arrancar la aplicación.
# Crea las tablas en PostgreSQL si aún no existen.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Task Pro API",
    description="""
    ## Task Pro API - Sistema de Gestión de Tareas
    
    Esta API proporciona una solución profesional para la gestión de tareas,
    optimizada para el rendimiento y la facilidad de integración.
    
    ### Funcionalidades Principales:
    * **Operaciones CRUD**: Control total sobre el ciclo de vida de las tareas.
    * **Búsqueda Avanzada**: Filtrado dual en títulos y descripciones.
    * **Métricas en Tiempo Real**: Estadísticas de productividad integradas.
    * **Resiliencia**: Arquitectura diseñada para entornos de contenedores.
    """,
    version="1.0.0",
    contact={
        "name": "Soporte Task Pro",
        "url": "https://github.com/tu-usuario/task-pro-api",
    },
)

# Registro de manejadores de excepciones personalizados
app.add_exception_handler(exceptions.TaskNotFoundException, exceptions.task_not_found_handler)
app.add_exception_handler(exceptions.TaskValidationException, exceptions.task_validation_handler)
app.add_exception_handler(exceptions.EmptyUpdateException, exceptions.empty_update_handler)

@app.get("/", tags=["General"])
def home():
    """Servicio de verificación de estado (Health Check).

    Returns:
        dict: Mensaje de bienvenida indicando que la API está operativa.
    """
    return {"message": "Bienvenido a Task Pro API conectada a PostgreSQL"}

@app.get("/tasks/stats", response_model=schemas.TaskStats, tags=["Analytics"])
def read_task_stats(db: Session = Depends(database.get_db)):
    """Obtiene métricas agregadas de las tareas.

    Calcula el total de tareas, el conteo por estado (completado/pendiente)
    y el porcentaje de progreso general.

    Returns:
        schemas.TaskStats: Objeto con KPIs de productividad.
    """
    return crud.get_task_stats(db)

@app.post("/tasks/", response_model=schemas.TaskResponse, tags=["Tasks"], status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    """Crea una nueva tarea en el sistema.

    Args:
        task (schemas.TaskCreate): Datos de la tarea (título y descripción).
        db (Session): Sesión de base de datos inyectada.

    Returns:
        schemas.TaskResponse: La tarea creada con sus datos de servidor (ID, fechas).
    """
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def read_tasks(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(database.get_db)
):
    """Lista tareas con capacidades de filtrado dinámico y paginación.

    Args:
        skip (int): Número de registros iniciales a omitir.
        limit (int): Cantidad máxima de registros a retornar.
        search (Optional[str]): Término de búsqueda para título o descripción.
        completed (Optional[bool]): Filtrar por tareas finalizadas o pendientes.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        list[schemas.TaskResponse]: Una lista de tareas que cumplen los criterios.
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, search=search, completed=completed)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    """Busca una tarea específica por su identificador único.

    Args:
        task_id (int): ID numérico de la tarea.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        schemas.TaskResponse: Los detalles de la tarea encontrada.

    Raises:
        TaskNotFoundException: Si el ID no existe en la base de datos.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise exceptions.TaskNotFoundException(task_id)
    return db_task

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def toggle_task_status(task_id: int, db: Session = Depends(database.get_db)):
    """Alterna el estado de completado de una tarea.

    Si la tarea estaba pendiente, pasa a completada y viceversa.

    Args:
        task_id (int): ID de la tarea a modificar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        schemas.TaskResponse: La tarea con su estado actualizado.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise exceptions.TaskNotFoundException(task_id)
    return crud.update_task_status(db=db, db_task=db_task)

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    """Actualiza el contenido informativo de una tarea (Título/Descripción).

    Args:
        task_id (int): ID de la tarea a actualizar.
        task (schemas.TaskUpdate): Nuevos datos opcionales.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        schemas.TaskResponse: La tarea modificada.

    Raises:
        EmptyUpdateException: Si no se proporcionan campos para actualizar.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise exceptions.TaskNotFoundException(task_id)
    if not task.model_dump(exclude_unset=True):
        raise exceptions.EmptyUpdateException()
    return crud.update_task(db=db, db_task=db_task, task_update=task)

@app.delete("/tasks/{task_id}", tags=["Tasks"], status_code=200)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    """Elimina permanentemente una tarea del sistema.

    Args:
        task_id (int): ID de la tarea a borrar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Confirmación de la eliminación exitosa.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise exceptions.TaskNotFoundException(task_id)
    crud.delete_task(db=db, db_task=db_task)
    return {"message": f"Tarea {task_id} eliminada con éxito"}


