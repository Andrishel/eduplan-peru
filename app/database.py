from sqlmodel import SQLModel, create_engine, Session, select
from app.models import PerfilInstitucional

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        perfil = session.exec(select(PerfilInstitucional)).first()
        if not perfil:
            perfil_default = PerfilInstitucional()
            session.add(perfil_default)
            session.commit()

def obtener_session():
    with Session(engine) as session:
        yield session