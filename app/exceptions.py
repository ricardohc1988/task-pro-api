from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(status_code=404, detail=f"Tarea con id {task_id} no encontrada")

class TaskValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)

class EmptyUpdateException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Debes enviar al menos un campo para actualizar")

async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Not Found", "detail": exc.detail}
    )

async def task_validation_handler(request: Request, exc: TaskValidationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Validation Error", "detail": exc.detail}
    )

async def empty_update_handler(request: Request, exc: EmptyUpdateException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Bad Request", "detail": exc.detail}
    )
