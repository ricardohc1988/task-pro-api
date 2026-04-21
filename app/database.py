"""Configuración de la Base de Datos.

Este módulo gestiona la conexión con PostgreSQL utilizando SQLAlchemy, incluyendo
un mecanismo de resiliencia para esperar a que el servicio de base de datos esté
listo (útil en entornos Docker Compose).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

# URL de conexión obtenida de las variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Gestión de conexión con lógica de reintentos
# Esto previene fallos si la API inicia antes que el contenedor de PostgreSQL
engine = None
retries = 5
while retries > 0:
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        # Intento de conexión de prueba para validar que el motor está listo
        with engine.connect() as conn:
            print("¡Conexión a la DB exitosa!")
            break
    except Exception as e:
        print(f"Esperando a la DB... reintentos restantes: {retries}")
        retries -= 1
        time.sleep(3)

if not engine:
    raise Exception("Error crítico: No se pudo conectar a la base de datos después de varios intentos.")

# Fábrica de sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán todos los modelos de SQLAlchemy
Base = declarative_base()

def get_db():
    """Generador de sesiones de base de datos (Dependencia de FastAPI).

    Gestiona el ciclo de vida de la sesión (abrir, usar, cerrar) asegurando
    que los recursos se liberen después de cada petición HTTP.

    Yields:
        Session: Una sesión activa de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
