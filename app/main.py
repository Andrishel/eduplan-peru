import os
import shutil
import markdown
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from app.database import crear_db_y_tablas, obtener_session
from app.models import PerfilInstitucional, Planificacion
from app.services.gemini_service import responder_consulta

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield

app = FastAPI(title="EduPlan Perú", lifespan=lifespan)

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ==========================================
# RUTAS DE NAVEGACIÓN PRINCIPAL
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Renderiza la portada comercial (Landing Page)"""
    return templates.TemplateResponse(
        request=request, 
        name="landing.html"
    )

@app.get("/auth", response_class=HTMLResponse)
async def pagina_auth(request: Request):
    """Renderiza la pantalla de Registro / Inicio de sesión"""
    return templates.TemplateResponse(
        request=request, 
        name="auth.html"
    )

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding_view(
    request: Request,
    session: Session = Depends(obtener_session)
):
    """Muestra el asistente paso a paso para configurar el perfil docente/directivo"""
    perfil = session.exec(select(PerfilInstitucional)).first()
    return templates.TemplateResponse(
        request=request, 
        name="onboarding.html",
        context={"perfil": perfil}
    )

@app.post("/completar-onboarding")
async def completar_onboarding(
    nombre_ie: str = Form(...),
    ugel: str = Form(...),
    lema: Optional[str] = Form(None),
    nombre_docente: str = Form(...),
    nivel_educativo: Optional[List[str]] = Form(None),
    area_curricular: Optional[List[str]] = Form(None),
    grado_seccion: Optional[str] = Form(None),
    enfoque_institucional: Optional[str] = Form(None),
    session: Session = Depends(obtener_session)
):
    """Guarda la configuración del onboarding en SQLite y redirige a /app"""
    perfil = session.exec(select(PerfilInstitucional)).first()
    if not perfil:
        perfil = PerfilInstitucional()
        session.add(perfil)
        
    perfil.nombre_ie = nombre_ie.strip()
    perfil.ugel = ugel.strip()
    perfil.lema = lema.strip() if lema else None
    perfil.nombre_docente = nombre_docente.strip()
    
    # Procesar niveles educativos seleccionados
    if nivel_educativo:
        niveles_limpios = [n.strip() for n in nivel_educativo if n.strip()]
        perfil.nivel_educativo = ", ".join(niveles_limpios) if niveles_limpios else "No especificado"
    else:
        perfil.nivel_educativo = "No especificado"

    # Procesar áreas curriculares (si es directivo, asigna Gestión Institucional)
    if area_curricular:
        areas_limpias = [a.strip() for a in area_curricular if a.strip()]
        perfil.area_curricular = ", ".join(areas_limpias) if areas_limpias else "Gestión Institucional"
    else:
        perfil.area_curricular = "Gestión Institucional"
    
    # Procesar grado o sección
    if grado_seccion and grado_seccion.strip():
        perfil.grado_seccion = grado_seccion.strip()
    else:
        perfil.grado_seccion = "Toda la Institución / General"

    perfil.enfoque_institucional = enfoque_institucional.strip() if enfoque_institucional else None

    session.add(perfil)
    session.commit()
    session.refresh(perfil)

    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/app", response_class=HTMLResponse)
async def workspace(
    request: Request,
    session: Session = Depends(obtener_session)
):
    """Renderiza el espacio de trabajo (Chat y herramientas)"""
    perfil = session.exec(select(PerfilInstitucional)).first()
    planificaciones = session.exec(
        select(Planificacion).order_by(Planificacion.id.desc()).limit(15)
    ).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={
            "perfil": perfil,
            "planificaciones": planificaciones
        }
    )

# ==========================================
# RUTAS DE CHAT Y GENERACIÓN IA
# ==========================================

@app.post("/enviar-mensaje", response_class=HTMLResponse)
async def enviar_mensaje(
    request: Request,
    prompt: str = Form(...),
    contexto_activo: str = Form(default="General"),
    grado_activo: str = Form(default="General"), # ¡Recibimos el grado dinámico!
    foto: UploadFile = File(None),
    session: Session = Depends(obtener_session)
):
    ruta_guardada = None
    nombre_archivo = None
    
    if foto and foto.filename:
        nombre_archivo = foto.filename
        ruta_guardada = os.path.join(UPLOAD_DIR, nombre_archivo)
        with open(ruta_guardada, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

    # Obtenemos la fecha actual
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    perfil = session.exec(select(PerfilInstitucional)).first()
    contexto_institucional = ""

    if perfil:
        # Inyectamos el área y grado seleccionados en la cabecera directamente a la IA
        contexto_institucional = (
            f" [I.E.: {perfil.nombre_ie}, UGEL: {perfil.ugel}, Docente: {perfil.nombre_docente}, "
            f"Nivel Educativo: {perfil.nivel_educativo}, Curso Activo: {contexto_activo}, "
            f"Grados a cargo: {grado_activo}, Enfoque: {perfil.enfoque_institucional}, "
            f"Fecha de hoy: {fecha_actual}]"
        )

    reglas_cneb = """
    REGLAS ESTRICTAS DE FORMATO (Basado en requerimientos directivos UGEL):
    Si el usuario pide una sesión de aprendizaje, DEBES estructurarla así:
    1. Título de la sesión.
    2. Datos informativos (Usa los datos de contexto provistos y la 'Fecha de hoy').
    3. Una tabla inicial con las columnas: Área, Competencia, Capacidades, Desempeño, Criterios a evaluar, y Recursos/Materiales.
    4. Una segunda tabla llamada 'Desarrollo de la Actividad' que incluya los procesos pedagógicos (Inicio, Desarrollo, Cierre) y los procesos didácticos del área.
    5. Articular explícitamente la sesión con el DUA (Diseño Universal para el Aprendizaje).
    Asegúrate de que los criterios tengan el mismo verbo del desempeño pero más específicos.
    """

    prompt_enriquecido = f"{prompt}\n\nDatos de contexto del docente:{contexto_institucional}\n\n{reglas_cneb}"

    respuesta_ia = responder_consulta(prompt_enriquecido, ruta_guardada)

    respuesta_html = markdown.markdown(
        respuesta_ia, 
        extensions=['tables', 'nl2br', 'fenced_code']
    )

    titulo_limpio = prompt.strip()
    titulo_doc = (titulo_limpio[:45] + "...") if len(titulo_limpio) > 45 else titulo_limpio
    titulo_doc = titulo_doc.capitalize()

    nueva_planificacion = Planificacion(
        titulo=titulo_doc,
        tipo_documento="Documento Pedagógico",
        area=contexto_activo,
        grado=grado_activo, # Guardamos el grado dinámico en la BD
        contenido_markdown=respuesta_ia,
        prompt_docente=prompt,
        archivo_adjunto=nombre_archivo
    )
    session.add(nueva_planificacion)
    session.commit()
    session.refresh(nueva_planificacion)

    return templates.TemplateResponse(
        request=request,
        name="components/mensaje_ia.html",
        context={
            "prompt_usuario": prompt,
            "archivo_nombre": nombre_archivo,
            "respuesta_html": respuesta_html,
            "planificacion_id": nueva_planificacion.id,
            "area_contexto": contexto_activo,
            "grado_contexto": grado_activo, # Lo enviamos al historial
            "es_nuevo": True
        }
    )

@app.get("/historial/{planificacion_id}", response_class=HTMLResponse)
async def cargar_historial_detalle(
    request: Request,
    planificacion_id: int,
    session: Session = Depends(obtener_session)
):
    plan = session.get(Planificacion, planificacion_id)
    if not plan:
        return HTMLResponse("<p class='text-red-500 text-sm'>No se encontró la planificación.</p>")

    respuesta_html = markdown.markdown(
        plan.contenido_markdown, 
        extensions=['tables', 'nl2br', 'fenced_code']
    )

    return templates.TemplateResponse(
        request=request,
        name="components/mensaje_ia.html",
        context={
            "prompt_usuario": plan.prompt_docente,
            "archivo_nombre": plan.archivo_adjunto,
            "respuesta_html": respuesta_html,
            "planificacion_id": plan.id,
            "es_nuevo": False # Al cargar historial, NO inyectamos el botón OOB
        }
    )

# ==========================================
# RUTAS DE CONFIGURACIÓN INSTITUCIONAL
# ==========================================

@app.get("/modal-perfil", response_class=HTMLResponse)
async def obtener_modal_perfil(
    request: Request,
    session: Session = Depends(obtener_session)
):
    perfil = session.exec(select(PerfilInstitucional)).first()
    return templates.TemplateResponse(
        request=request,
        name="components/modal_perfil.html",
        context={"perfil": perfil}
    )

@app.post("/guardar-perfil", response_class=HTMLResponse)
async def guardar_perfil(
    request: Request,
    nombre_ie: str = Form(...),
    ugel: str = Form(...),
    lema: Optional[str] = Form(None),
    nombre_docente: str = Form(...),
    area_curricular: str = Form(...),
    grado_seccion: str = Form(...),
    enfoque_institucional: Optional[str] = Form(None),
    session: Session = Depends(obtener_session)
):
    perfil = session.exec(select(PerfilInstitucional)).first()
    if not perfil:
        perfil = PerfilInstitucional()
        session.add(perfil)
        
    perfil.nombre_ie = nombre_ie.strip()
    perfil.ugel = ugel.strip()
    perfil.lema = lema.strip() if lema else None
    perfil.nombre_docente = nombre_docente.strip()
    perfil.area_curricular = area_curricular.strip()
    perfil.grado_seccion = grado_seccion.strip()
    perfil.enfoque_institucional = enfoque_institucional.strip() if enfoque_institucional else None

    session.commit()
    session.refresh(perfil)

    return templates.TemplateResponse(
        request=request,
        name="components/perfil_badge.html",
        context={"perfil": perfil}
    )

@app.get("/descargar/word/{planificacion_id}")
async def descargar_word(
    planificacion_id: int,
    session: Session = Depends(obtener_session)
):
    """Genera un archivo Word (.doc) a partir del Markdown de la planificación"""
    plan = session.get(Planificacion, planificacion_id)
    if not plan:
        return HTMLResponse("<p>Documento no encontrado.</p>", status_code=404)

    # Convertimos el markdown a HTML
    html_body = markdown.markdown(
        plan.contenido_markdown, 
        extensions=['tables', 'nl2br']
    )

    # Plantilla HTML con sintaxis XML de Microsoft Office
    # Esto asegura que Word respete las tildes (utf-8) y dibuje las tablas correctamente
    html_content = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
        <meta charset="utf-8">
        <title>{plan.titulo}</title>
        <style>
            body {{ font-family: 'Calibri', 'Arial', sans-serif; font-size: 11pt; }}
            h1, h2, h3 {{ color: #292524; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #000000; padding: 8px; text-align: left; vertical-align: top; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # Limpiamos el título para que sea un nombre de archivo válido
    nombre_seguro = "".join([c for c in plan.titulo if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    nombre_archivo = f"{nombre_seguro.replace(' ', '_')}.doc"

    # Forzamos la descarga del archivo estableciendo los Headers HTTP
    headers = {
        "Content-Disposition": f'attachment; filename="{nombre_archivo}"'
    }
    
    return Response(content=html_content, media_type="application/msword", headers=headers)