from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class PerfilInstitucional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_ie: str = Field(default="I.E. Emblemática")
    ugel: str = Field(default="UGEL 01")
    lema: Optional[str] = Field(default="Disciplina, Estudio y Superación")
    logo_url: Optional[str] = Field(default=None)
    nombre_docente: str = Field(default="Docente Demo")
    nivel_educativo: str = Field(default="Secundaria") # NUEVO CAMPO
    area_curricular: str = Field(default="Comunicación")
    grado_seccion: str = Field(default="2° Secundaria")
    enfoque_institucional: Optional[str] = Field(
        default="Enfoque por competencias según el CNEB con énfasis en trabajo colaborativo."
    )

class Planificacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    tipo_documento: str = Field(default="Sesión de Aprendizaje")
    area: str
    grado: str
    contenido_markdown: str
    prompt_docente: str
    archivo_adjunto: Optional[str] = Field(default=None)
    fijado: bool = Field(default=False)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)