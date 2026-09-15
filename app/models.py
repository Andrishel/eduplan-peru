from datetime import datetime, timezone
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
    rol: str = Field(default="Docente")  # Docente o Directivo
    es_admin: bool = Field(default=False)  # Para el panel de control
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Un usuario puede tener uno o varios perfiles/colegios
    perfiles: List["PerfilInstitucional"] = Relationship(back_populates="usuario")
    planificaciones: List["Planificacion"] = Relationship(back_populates="usuario")


# ==========================================
# 2. TABLA DE PERFIL INSTITUCIONAL / COLEGIO
# ==========================================
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
    
    # Relaciones
    usuario: Optional[Usuario] = Relationship(back_populates="perfiles")
    cargas: List["CargaAcademica"] = Relationship(back_populates="institucion")
    planificaciones: List["Planificacion"] = Relationship(back_populates="institucion")


# ==========================================
# 3. TABLA DE CARGA ACADÉMICA (Polidocencia)
# ==========================================
class CargaAcademica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    institucion_id: int = Field(foreign_key="perfilinstitucional.id")
    
    nivel: str = Field(default="Secundaria")  # Primaria o Secundaria
    area: str                                 # Comunicación, Matemática, etc.
    grado: str                                # 1°, 2°, etc.
    seccion: str = Field(default="Única")     # A, B, C, Única
    
    institucion: Optional[PerfilInstitucional] = Relationship(back_populates="cargas")


# ==========================================
# 4. TABLA DE HISTORIAL / PLANIFICACIONES
# ==========================================
class Planificacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    institucion_id: Optional[int] = Field(default=None, foreign_key="perfilinstitucional.id")
    
    titulo: str
    tipo_documento: str = Field(default="Documento Pedagógico")
    area: str
    grado: str
    contenido_markdown: str
    prompt_docente: str
    archivo_adjunto: Optional[str] = Field(default=None)
    fijado: bool = Field(default=False)
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relaciones bidireccionales
    usuario: Optional[Usuario] = Relationship(back_populates="planificaciones")
    institucion: Optional[PerfilInstitucional] = Relationship(back_populates="planificaciones")