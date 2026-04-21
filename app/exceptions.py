"""Manejo Personalizado de Excepciones.

Define excepciones específicas del dominio y sus correspondientes manejadores
para retornar respuestas JSON estandarizadas en caso de error.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class TaskNotFoundException(HTTPException):
    """Excepción lanzada cuando una tarea no existe en la base de datos."""
    def __init__(self, task_id: int):
        super().__init__(status_code=404, detail=f"Tarea con id {task_id} no encontrada")

class TaskValidationException(HTTPException):
    """Excepción lanzada por errores de validación de lógica de negocio."""
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)

class EmptyUpdateException(HTTPException):
    """Excepción lanzada cuando se intenta actualizar una tarea sin proporcionar campos."""
    def __init__(self):
        super().__init__(status_code=400, detail="Debes enviar al menos un campo para actualizar")

async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
    """Handler para TaskNotFoundException. Retorna error 404."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Not Found", "detail": exc.detail}
    )

async def task_validation_handler(request: Request, exc: TaskValidationException):
    """Handler para TaskValidationException. Retorna error 422."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Validation Error", "detail": exc.detail}
    )

async def empty_update_handler(request: Request, exc: EmptyUpdateException):
    """Handler para EmptyUpdateException. Retorna error 400."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Bad Request", "detail": exc.detail}
    )

