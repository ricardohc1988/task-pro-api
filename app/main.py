from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, crud
from typing import Optional

# Inicializa la base de datos. Crea las tablas en PostgreSQL si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Task Pro API",
    description="""
    API para la gestión de tareas de alto rendimiento.
    
    ## Funcionalidades
    * **CRUD** completo de tareas.
    * **Búsqueda** avanzada por filtros.
    * **Estadísticas** de productividad.
    """
)

@app.get("/", tags=["General"])
def home():
    """Endpoint de bienvenida para verificar el estado de la API."""
    return {"message": "Bienvenido a Task Pro API conectada a PostgreSQL"}

@app.get("/tasks/stats", response_model=schemas.TaskStats, tags=["Analytics"])
def read_task_stats(db: Session = Depends(database.get_db)):
    """
    Obtener métricas generales de las tareas:
    - Total de tareas creadas.
    - Cantidad de completadas vs pendientes.
    - Porcentaje de progreso.
    """
    return crud.get_task_stats(db)

# Crear una tarea
@app.post("/tasks/", response_model=schemas.TaskResponse, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    """
    Crear una tarea
    - Valida que el título tenga al menos 3 caracteres.
    - Asigna automáticamente una fecha de creación.
    """
    return crud.create_task(db=db, task=task)

# Obtener todas las tareas
@app.get("/tasks/", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def read_tasks(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(database.get_db)):
    """
    Listar tareas con filtros opcionales:
    - **search**: Busca palabras en el título.
    - **completed**: Filtra por True o False.
    - **skip/limit**: Manejo de paginación
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, search=search, completed=completed)
    return tasks

# Obtener una tarea
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    """**Obtener una tarea específica por su ID.**"""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

# Actualizar una tarea (Marcar como completada)
@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def toggle_task_status(task_id: int, db: Session = Depends(database.get_db)):
    """**Alternar estado de la tarea.**"""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return crud.update_task_status(db=db, db_task=db_task)

# Editar título o descripción
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    """**Editar una tarea** """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return crud.update_task(db=db, db_task=db_task, task_update=task)

# Eliminar una tarea
@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    """**Eliminar tarea.** Borra el registro de la base de datos."""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    crud.delete_task(db=db, db_task=db_task)
    return {"message": f"Tarea {task_id} eliminada con éxito"}

