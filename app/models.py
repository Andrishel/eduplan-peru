from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_completo: str
    correo: str = Field(unique=True, index=True)
    password_hash: str
    rol: str = Field(default="Docente")
    es_admin: bool = Field(default=False)
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    perfiles: List["PerfilInstitucional"] = Relationship(back_populates="usuario")
    planificaciones: List["Planificacion"] = Relationship(back_populates="usuario")
    colecciones: List["Coleccion"] = Relationship(back_populates="usuario")

class PerfilInstitucional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    
    nombre_ie: str = Field(default="I.E. Emblemática")
    ugel: str = Field(default="UGEL 01")
    lema: Optional[str] = Field(default="Disciplina, Estudio y Superación")
    logo_url: Optional[str] = Field(default=None)
    nombre_docente: str = Field(default="Docente Demo")
    nivel_educativo: str = Field(default="Secundaria")
    area_curricular: str = Field(default="Comunicación")
    grado_seccion: str = Field(default="2° Secundaria")
    enfoque_institucional: Optional[str] = Field(
        default="Enfoque por competencias según el CNEB con énfasis en trabajo colaborativo."
    )
    
    usuario: Optional[Usuario] = Relationship(back_populates="perfiles")
    cargas: List["CargaAcademica"] = Relationship(back_populates="institucion")
    planificaciones: List["Planificacion"] = Relationship(back_populates="institucion")

class CargaAcademica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    institucion_id: int = Field(foreign_key="perfilinstitucional.id")
    
    nivel: str = Field(default="Secundaria")
    area: str
    grado: str
    seccion: str = Field(default="Única")
    
    institucion: Optional[PerfilInstitucional] = Relationship(back_populates="cargas")

class Coleccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    nombre: str
    color_tag: str = Field(default="bg-zen-100 text-zen-800") 
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    usuario: Optional[Usuario] = Relationship(back_populates="colecciones")
    planificaciones: List["Planificacion"] = Relationship(back_populates="coleccion")

class Planificacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    # ondelete="SET NULL" para evitar violaciones de clave foránea en Postgres
    institucion_id: Optional[int] = Field(default=None, foreign_key="perfilinstitucional.id", ondelete="SET NULL")
    coleccion_id: Optional[int] = Field(default=None, foreign_key="coleccion.id", ondelete="SET NULL")
    
    titulo: str
    tipo_documento: str = Field(default="Documento Pedagógico")
    area: str
    grado: str
    contenido_markdown: str
    prompt_docente: str
    archivo_adjunto: Optional[str] = Field(default=None)
    modo_generacion: str = Field(default="CNEB")
    fijado: bool = Field(default=False)
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    usuario: Optional[Usuario] = Relationship(back_populates="planificaciones")
    institucion: Optional[PerfilInstitucional] = Relationship(back_populates="planificaciones")
    coleccion: Optional[Coleccion] = Relationship(back_populates="planificaciones")