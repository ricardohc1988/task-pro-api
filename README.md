# Task Pro API
### Backend Profesional con FastAPI, PostgreSQL & Docker

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**Task Pro API** es una solución robusta para la gestión de tareas, diseñada bajo una arquitectura escalable. No es solo un CRUD básico, implementa patrones avanzados de filtrado, búsqueda inteligente y estadísticas de productividad en tiempo real.

---

## Características

*   ** Alto Rendimiento:** Construido sobre FastAPI y Pydantic v2 para una ejecución y validación ultra rápida.
*   ** Búsqueda Dual Inteligente:** Algoritmo que filtra palabras clave simultáneamente en títulos y descripciones.
*   ** Dashboard de Estadísticas:** Endpoint especializado (`/tasks/stats`) que calcula métricas clave de productividad.
*   ** Arquitectura Limpia:** Separación estricta de responsabilidades (Modelos, Esquemas, Lógica CRUD y Rutas).
*   ** Manejo de Errores Profesional:** Excepciones personalizadas con respuestas JSON estandarizadas.
*   ** Resiliencia de Base de Datos:** Script de conexión con auto-reintentos para asegurar estabilidad en entornos Docker.

---

## Tecnologías

*   **Backend:** Python 3.11+ con FastAPI.
*   **ORM:** SQLAlchemy para una gestión eficiente de la DB.
*   **Base de Datos:** PostgreSQL 15.
*   **Despliegue:** Docker & Docker Compose.

---

## Inicio Rápido (Docker)

Asegurarse de tener instalados **Docker** y **Docker Compose**.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/task-pro-api.git
    cd task-pro-api
    ```

2.  **Lanzar el entorno:**
    ```bash
    docker-compose up --build
    ```

3.  **Explorar la API:**
    La documentación interactiva estará disponible en:
    *   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Principales Endpoints

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/tasks/` | Lista tareas con filtros (`search`, `completed`) y paginación. |
| `POST` | `/tasks/` | Crea una nueva tarea (Validación de longitud mínima). |
| `GET` | `/tasks/{id}` | Obtiene detalles de una tarea específica. |
| `PATCH` | `/tasks/{id}` | Alterna el estado (completado/pendiente). |
| `GET` | `/tasks/stats` | Retorna métricas globales de productividad. |

---

## Estructura del Proyecto

```text
task-pro-api/
├── app/
│   ├── main.py          # Punto de entrada y definición de rutas
│   ├── models.py        # Modelos de tablas PostgreSQL (SQLAlchemy)
│   ├── schemas.py       # Validación de datos y contratos (Pydantic)
│   ├── crud.py          # Lógica de persistencia y consultas SQL
│   ├── database.py      # Configuración de conexión y sesión
│   └── exceptions.py    # Gestión de errores personalizados
├── docker-compose.yml   # Orquestación de contenedores
├── Dockerfile           # Definición de la imagen de la aplicación
└── requirements.txt     # Dependencias del sistema
```