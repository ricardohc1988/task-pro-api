from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Intentar conectar con reintentos
engine = None
retries = 5
while retries > 0:
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        # Intentamos una conexión de prueba
        with engine.connect() as conn:
            print("¡Conexión a la DB exitosa!")
            break
    except Exception as e:
        print(f"Esperando a la DB... reintentos restantes: {retries}")
        retries -= 1
        time.sleep(3)

if not engine:
    raise Exception("No se pudo conectar a la base de datos después de varios intentos")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency Generator: Gestiona el ciclo de vida de la sesión de DB.
    Asegura que la conexión se cierre después de cada petición HTTP.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()