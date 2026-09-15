import os
import shutil
import markdown
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from app.database import crear_db_y_tablas, obtener_session
from app.models import PerfilInstitucional, Planificacion, Usuario
from app.services.gemini_service import responder_consulta
from app.services.auth_service import (
    hashear_password, 
    verificar_password, 
    crear_token_sesion, 
    decodificar_token_sesion
)

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
# DEPENDENCIA DE AUTENTICACIÓN
# ==========================================
async def obtener_usuario_actual(
    session: Session = Depends(obtener_session),
    session_token: Optional[str] = Cookie(None)
) -> Optional[Usuario]:
    if not session_token:
        return None
    usuario_id = decodificar_token_sesion(session_token)
    if not usuario_id:
        return None
    return session.get(Usuario, usuario_id)

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

@app.get("/app", response_class=HTMLResponse)
async def workspace(
    request: Request,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    """Renderiza el espacio de trabajo protegido"""
    if not usuario:
        return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)

    perfil = session.exec(
        select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)
    ).first()
    
    planificaciones = session.exec(
        select(Planificacion)
        .where(Planificacion.usuario_id == usuario.id)
        .order_by(Planificacion.id.desc())
        .limit(15)
    ).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={
            "usuario": usuario,
            "perfil": perfil,
            "planificaciones": planificaciones
        }
    )

# ==========================================
# RUTAS DE REGISTRO Y LOGIN
# ==========================================

@app.post("/auth/registro")
async def registro(
    nombre_completo: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    rol: str = Form(default="Docente"),
    session: Session = Depends(obtener_session)
):
    correo_limpio = correo.strip().lower()
    existente = session.exec(select(Usuario).where(Usuario.correo == correo_limpio)).first()
    if existente:
        return HTMLResponse("<p class='text-red-500 text-xs font-bold text-center mt-2'>El correo ya está registrado.</p>", status_code=400)

    nuevo_usuario = Usuario(
        nombre_completo=nombre_completo.strip(),
        correo=correo_limpio,
        password_hash=hashear_password(password),
        rol=rol
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    # Crear perfil institucional por defecto asociado al usuario
    nuevo_perfil = PerfilInstitucional(
        usuario_id=nuevo_usuario.id,
        nombre_docente=nuevo_usuario.nombre_completo
    )
    session.add(nuevo_perfil)
    session.commit()

    token = crear_token_sesion(nuevo_usuario.id)
    response = RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_token", value=token, httponly=True, max_age=604800)
    return response

@app.post("/auth/login")
async def login(
    correo: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(obtener_session)
):
    correo_limpio = correo.strip().lower()
    usuario = session.exec(select(Usuario).where(Usuario.correo == correo_limpio)).first()
    
    if not usuario or not verificar_password(password, usuario.password_hash):
        return HTMLResponse("<p class='text-red-500 text-xs font-bold text-center mt-2'>Credenciales incorrectas.</p>", status_code=401)

    token = crear_token_sesion(usuario.id)
    response = RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_token", value=token, httponly=True, max_age=604800)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_token")
    return response

# ==========================================
# RUTAS DE ONBOARDING
# ==========================================

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding_view(
    request: Request,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
        
    perfil = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).first()
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
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)

    perfil = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).first()
    if not perfil:
        perfil = PerfilInstitucional(usuario_id=usuario.id)
        session.add(perfil)
        
    perfil.nombre_ie = nombre_ie.strip()
    perfil.ugel = ugel.strip()
    perfil.lema = lema.strip() if lema else None
    perfil.nombre_docente = nombre_docente.strip()
    
    if nivel_educativo:
        niveles_limpios = [n.strip() for n in nivel_educativo if n.strip()]
        perfil.nivel_educativo = ", ".join(niveles_limpios) if niveles_limpios else "No especificado"
    else:
        perfil.nivel_educativo = "No especificado"

    if area_curricular:
        areas_limpias = [a.strip() for a in area_curricular if a.strip()]
        perfil.area_curricular = ", ".join(areas_limpias) if areas_limpias else "Gestión Institucional"
    else:
        perfil.area_curricular = "Gestión Institucional"
    
    if grado_seccion and grado_seccion.strip():
        perfil.grado_seccion = grado_seccion.strip()
    else:
        perfil.grado_seccion = "Toda la Institución / General"

    perfil.enfoque_institucional = enfoque_institucional.strip() if enfoque_institucional else None

    session.add(perfil)
    session.commit()
    session.refresh(perfil)

    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

# ==========================================
# RUTAS DE CHAT Y GENERACIÓN IA
# ==========================================

@app.post("/enviar-mensaje", response_class=HTMLResponse)
async def enviar_mensaje(
    request: Request,
    prompt: str = Form(...),
    contexto_activo: str = Form(default="General"),
    grado_activo: str = Form(default="General"),
    seccion_activa: str = Form(default="Única"),
    foto: UploadFile = File(None),
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)

    ruta_guardada = None
    nombre_archivo = None
    
    if foto and foto.filename:
        nombre_archivo = foto.filename
        ruta_guardada = os.path.join(UPLOAD_DIR, nombre_archivo)
        with open(ruta_guardada, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    grado_completo = f"{grado_activo} - {seccion_activa}"

    perfil = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).first()
    contexto_institucional = ""

    if perfil:
        contexto_institucional = (
            f" [I.E.: {perfil.nombre_ie}, UGEL: {perfil.ugel}, Docente: {perfil.nombre_docente}, "
            f"Nivel Educativo: {perfil.nivel_educativo}, Curso Activo: {contexto_activo}, "
            f"Grados a cargo: {grado_completo}, Enfoque: {perfil.enfoque_institucional}, "
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
        usuario_id=usuario.id,
        titulo=titulo_doc,
        tipo_documento="Documento Pedagógico",
        area=contexto_activo,
        grado=grado_completo,
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
            "grado_contexto": grado_completo,
            "es_nuevo": True
        }
    )

@app.get("/historial/{planificacion_id}", response_class=HTMLResponse)
async def cargar_historial_detalle(
    request: Request,
    planificacion_id: int,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)

    plan = session.get(Planificacion, planificacion_id)
    if not plan or plan.usuario_id != usuario.id:
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
            "es_nuevo": False
        }
    )

# ==========================================
# RUTAS DE CONFIGURACIÓN INSTITUCIONAL
# ==========================================

@app.get("/modal-perfil", response_class=HTMLResponse)
async def obtener_modal_perfil(
    request: Request,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)

    perfil = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).first()
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
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)

    perfil = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).first()
    if not perfil:
        perfil = PerfilInstitucional(usuario_id=usuario.id)
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
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)

    plan = session.get(Planificacion, planificacion_id)
    if not plan or plan.usuario_id != usuario.id:
        return HTMLResponse("<p>Documento no encontrado o sin acceso.</p>", status_code=404)

    html_body = markdown.markdown(
        plan.contenido_markdown, 
        extensions=['tables', 'nl2br']
    )

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

    nombre_seguro = "".join([c for c in plan.titulo if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    nombre_archivo = f"{nombre_seguro.replace(' ', '_')}.doc"

    headers = {
        "Content-Disposition": f'attachment; filename="{nombre_archivo}"'
    }
    
    return Response(content=html_content, media_type="application/msword", headers=headers)

@app.get("/filtrar-historial", response_class=HTMLResponse)
async def filtrar_historial(
    request: Request,
    contexto_activo: Optional[str] = None,
    grado_activo: Optional[str] = None,
    seccion_activa: Optional[str] = None,
    ver_todos: bool = False,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)

    query = select(Planificacion).where(Planificacion.usuario_id == usuario.id).order_by(Planificacion.id.desc())
    
    if not ver_todos and contexto_activo and grado_activo:
        grado_filtro = f"{grado_activo} - {seccion_activa}" if seccion_activa else grado_activo
        query = query.where(
            Planificacion.area == contexto_activo,
            Planificacion.grado == grado_filtro
        )
        
    planificaciones = session.exec(query.limit(20)).all()
    
    if ver_todos:
        boton_toggle = """
        <div id="contenedor-toggle-filtro" hx-swap-oob="true">
            <button hx-get="/filtrar-historial" 
                    hx-include="#selector-contexto-dual" 
                    hx-target="#lista-historial" 
                    class="text-[11px] font-bold text-zen-700 bg-zen-50 border border-zen-200 px-3 py-1.5 rounded-xl transition whitespace-nowrap">
                Filtrar por aula activa
            </button>
        </div>
        """
    else:
        boton_toggle = """
        <div id="contenedor-toggle-filtro" hx-swap-oob="true">
            <button hx-get="/filtrar-historial?ver_todos=true" 
                    hx-target="#lista-historial" 
                    class="text-[11px] font-bold text-slate-600 hover:text-zen-700 bg-calm-50 border border-calm-200 px-3 py-1.5 rounded-xl transition whitespace-nowrap">
                Ver todo el historial
            </button>
        </div>
        """

    contenido_lista = templates.get_template("components/lista_historial.html").render(
        {"planificaciones": planificaciones}
    )
    
    return HTMLResponse(content=contenido_lista + boton_toggle)