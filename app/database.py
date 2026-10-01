import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# 1. Extraer la URL de conexión desde el archivo .env
database_url = os.getenv("DATABASE_URL")

# 2. SQLAlchemy requiere que el prefijo sea 'postgresql://' y no 'postgres://' (que es como lo da Supabase)
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# 3. Crear el motor de conexión hacia la nube (Supabase)
engine = create_engine(database_url, echo=False)

def crear_db_y_tablas():
    # Sincroniza y crea todas las tablas en Supabase automáticamente al iniciar
    SQLModel.metadata.create_all(engine)

def obtener_session():
    with Session(engine) as session:
        yield session