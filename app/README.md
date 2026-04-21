# 🚀 Task Pro API - Backend Profesional con FastAPI & Docker

Task Pro API es una solución robusta para la gestión de tareas (Task Management), diseñada bajo una arquitectura escalable, utilizando **FastAPI** para el backend y **PostgreSQL** como motor de base de datos, todo orquestado mediante **Docker**.

Este proyecto no es solo un CRUD; implementa filtros avanzados, búsqueda dual (título/descripción), estadísticas en tiempo real y una arquitectura resiliente con manejo de reconexión automática a la base de datos.

## 🛠️ Tecnologías Utilizadas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
* **Base de Datos:** [PostgreSQL 15](https://www.postgresql.org/)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Validación de Datos:** [Pydantic v2](https://docs.pydantic.dev/)
* **Contenedores:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## ✨ Características Destacadas

* **Arquitectura Refactorizada:** Separación clara entre rutas (main), esquemas (Pydantic), modelos y lógica de negocio (CRUD).
* **Búsqueda Inteligente:** Filtro dual que busca palabras clave simultáneamente en títulos y descripciones.
* **Dashboard de Estadísticas:** Endpoint especializado (`/tasks/stats`) que calcula métricas de productividad (porcentaje de completado, totales, etc.).
* **Validación Estricta:** Blindaje de datos mediante Pydantic para asegurar la integridad de la base de datos.
* **Resiliencia:** Script de conexión con reintentos automáticos para esperar la inicialización de PostgreSQL en contenedores.

## Instalación y Ejecución con Docker

Asegúrate de tener **Docker Desktop** instalado y sigue estos pasos:

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/task-pro-api.git](https://github.com/tu-usuario/task-pro-api.git)
    cd task-pro-api
    ```

2.  **Inicia la aplicación:**
    ```bash
    docker-compose up --build
    ```

3.  **Accede a la documentación interactiva:**
    Una vez que los logs indiquen que la base de datos está lista, ve a:
    👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## 📁 Estructura del Proyecto

```text
task-pro-api/
├── app/
│   ├── main.py          # Punto de entrada y rutas de la API
│   ├── models.py        # Definición de tablas PostgreSQL
│   ├── schemas.py       # Modelos de validación Pydantic
│   ├── crud.py          # Lógica de base de datos (Query builder)
│   └── database.py      # Configuración de SQLAlchemy y reconexión
├── docker-compose.yml   # Orquestación de servicios (Web + DB)
├── Dockerfile           # Configuración de la imagen de Python
└── requirements.txt     # Dependencias del proyecto