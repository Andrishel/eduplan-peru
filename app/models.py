from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ==========================================
# 1. TABLA DE USUARIOS
# ==========================================
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_completo: str
    correo: str = Field(unique=True, index=True)
    password_hash: str
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    
    perfil: Optional["PerfilInstitucional"] = Relationship(back_populates="usuario")
    planificaciones: List["Planificacion"] = Relationship(back_populates="usuario")


# ==========================================
# 2. TABLA DE PERFIL INSTITUCIONAL
# ==========================================
class PerfilInstitucional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Permitir None por defecto para no romper semillas automáticas
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
    
    usuario: Optional[Usuario] = Relationship(back_populates="perfil")


# ==========================================
# 3. TABLA DE HISTORIAL / PLANIFICACIONES
# ==========================================
class Planificacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Permitir None por defecto para compatibilidad
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    
    titulo: str
    tipo_documento: str = Field(default="Documento Pedagógico")
    area: str
    grado: str
    contenido_markdown: str
    prompt_docente: str
    archivo_adjunto: Optional[str] = Field(default=None)
    fijado: bool = Field(default=False)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    
    usuario: Optional[Usuario] = Relationship(back_populates="planificaciones")