import os
import shutil
import uuid
import nh3
import markdown
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, update

from app.database import crear_db_y_tablas, obtener_session
from app.models import PerfilInstitucional, Planificacion, Usuario, CargaAcademica, Coleccion
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

IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production"

HTML_TAGS_PERMITIDAS = {
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr', 'strong', 'em', 'b', 'i',
    'table', 'thead', 'tbody', 'tr', 'th', 'td', 'ul', 'ol', 'li', 'blockquote',
    'pre', 'code', 'span', 'div'
}

def sanitizar_contenido(html_crudo: str) -> str:
    return nh3.clean(html_crudo, tags=HTML_TAGS_PERMITIDAS)

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
    return templates.TemplateResponse(request=request, name="landing.html")

@app.get("/auth", response_class=HTMLResponse)
async def pagina_auth(
    request: Request,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if usuario:
        instituciones = session.exec(
            select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)
        ).all()
        destino = "/app" if instituciones else "/onboarding"
        return RedirectResponse(url=destino, status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request=request, name="auth.html")

@app.get("/app", response_class=HTMLResponse)
async def workspace(
    request: Request,
    institucion_id: Optional[int] = None,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)

    instituciones = session.exec(
        select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)
    ).all()

    if not instituciones:
        return RedirectResponse(url="/onboarding", status_code=status.HTTP_303_SEE_OTHER)

    perfil_activo = None
    if institucion_id:
        perfil_activo = session.exec(
            select(PerfilInstitucional).where(
                PerfilInstitucional.id == institucion_id,
                PerfilInstitucional.usuario_id == usuario.id
            )
        ).first()
    
    if not perfil_activo:
        colegio_real = next((i for i in instituciones if i.nombre_ie != "Espacio Personal / Tutorías"), None)
        perfil_activo = colegio_real if colegio_real else instituciones[0]

    cargas = session.exec(
        select(CargaAcademica).where(CargaAcademica.institucion_id == perfil_activo.id)
    ).all()

    if cargas:
        areas_disponibles = sorted(list(set(c.area for c in cargas)))
        primera_area = areas_disponibles[0]
        cargas_area = [c for c in cargas if c.area == primera_area]
        grados_disponibles = sorted(list(set(c.grado for c in cargas_area)))
        primer_grado = grados_disponibles[0]
        secciones_disponibles = sorted(list(set(c.seccion for c in cargas_area if c.grado == primer_grado)))
    else:
        areas_disponibles = ["General"]
        grados_disponibles = ["Único"]
        secciones_disponibles = ["Única"]

    planificaciones = session.exec(
        select(Planificacion)
        .where(Planificacion.usuario_id == usuario.id)
        .order_by(Planificacion.id.desc())
        .limit(20)
    ).all()

    colecciones = session.exec(
        select(Coleccion)
        .where(Coleccion.usuario_id == usuario.id)
        .order_by(Coleccion.id.desc())
    ).all()

    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={
            "usuario": usuario,
            "instituciones": instituciones,
            "perfil": perfil_activo,
            "areas": areas_disponibles,
            "grados": grados_disponibles,
            "secciones": secciones_disponibles,
            "planificaciones": planificaciones,
            "colecciones": colecciones
        }
    )

# ==========================================
# SELECTORES DINÁMICOS (HTMX)
# ==========================================
@app.get("/api/selector-grados", response_class=HTMLResponse)
async def selector_grados(
    institucion_id: int,
    contexto_activo: str,
    session: Session = Depends(obtener_session)
):
    cargas = session.exec(
        select(CargaAcademica).where(
            CargaAcademica.institucion_id == institucion_id,
            CargaAcademica.area == contexto_activo
        )
    ).all()
    
    grados = sorted(list(set(c.grado for c in cargas))) if cargas else ["Único"]
    primer_grado = grados[0]
    secciones = sorted(list(set(c.seccion for c in cargas if c.grado == primer_grado))) if cargas else ["Única"]

    options_grados = "".join([f'<option value="{g}">{g}</option>' for g in grados])
    options_secciones = "".join([f'<option value="{s}">Secc. {s}</option>' for s in secciones])

    return HTMLResponse(f"""
        <select name="grado_activo" form="form-chat"
                hx-get="/api/selector-secciones?institucion_id={institucion_id}&contexto_activo={contexto_activo}" 
                hx-target="next select" 
                hx-trigger="change"
                class="bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 text-zen-800 dark:text-zen-400 text-xs font-bold rounded-xl px-2.5 py-1.5 outline-none transition cursor-pointer min-w-[70px]">
            {options_grados}
        </select>
        <select name="seccion_activa" form="form-chat"
                class="bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 text-zen-800 dark:text-zen-400 text-xs font-bold rounded-xl px-2.5 py-1.5 outline-none transition cursor-pointer min-w-[80px]">
            {options_secciones}
        </select>
    """)

@app.get("/api/selector-secciones", response_class=HTMLResponse)
async def selector_secciones(
    institucion_id: int,
    contexto_activo: str,
    grado_activo: str,
    session: Session = Depends(obtener_session)
):
    cargas = session.exec(
        select(CargaAcademica).where(
            CargaAcademica.institucion_id == institucion_id,
            CargaAcademica.area == contexto_activo,
            CargaAcademica.grado == grado_activo
        )
    ).all()
    
    secciones = sorted(list(set(c.seccion for c in cargas))) if cargas else ["Única"]
    options = "".join([f'<option value="{s}">Secc. {s}</option>' for s in secciones])
    
    return HTMLResponse(f"""
        <select name="seccion_activa" form="form-chat" class="bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 text-zen-800 dark:text-zen-400 text-xs font-bold rounded-xl px-2.5 py-1.5 outline-none transition cursor-pointer min-w-[80px]">
            {options}
        </select>
    """)

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
        return HTMLResponse("<div class='p-3 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs font-bold text-center mb-3'>Este correo ya está registrado.</div>", status_code=400)

    nuevo_usuario = Usuario(
        nombre_completo=nombre_completo.strip(),
        correo=correo_limpio,
        password_hash=hashear_password(password),
        rol=rol
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    token = crear_token_sesion(nuevo_usuario.id)
    response = RedirectResponse(url="/onboarding", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["HX-Redirect"] = "/onboarding"
    response.set_cookie(key="session_token", value=token, httponly=True, secure=IS_PRODUCTION, max_age=604800, samesite="lax")
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
        return HTMLResponse("<div class='p-3 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs font-bold text-center mb-3'>Correo o contraseña incorrectos.</div>", status_code=401)

    instituciones = session.exec(
        select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)
    ).all()
    destino = "/app" if instituciones else "/onboarding"

    token = crear_token_sesion(usuario.id)
    response = RedirectResponse(url=destino, status_code=status.HTTP_303_SEE_OTHER)
    response.headers["HX-Redirect"] = destino
    response.set_cookie(key="session_token", value=token, httponly=True, secure=IS_PRODUCTION, max_age=604800, samesite="lax")
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
    return templates.TemplateResponse(request=request, name="onboarding.html")

@app.post("/completar-onboarding")
async def completar_onboarding(
    request: Request,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)

    form_data = await request.form()
    colegios_previos = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).all()
    
    for col in colegios_previos:
        session.exec(update(Planificacion).where(Planificacion.institucion_id == col.id).values(institucion_id=None))
        cargas = session.exec(select(CargaAcademica).where(CargaAcademica.institucion_id == col.id)).all()
        for c in cargas:
            session.delete(c)
        session.delete(col)
    session.commit()

    if form_data.get("es_independiente") == "on":
        espacio_libre = PerfilInstitucional(
            usuario_id=usuario.id,
            nombre_ie="Espacio Personal / Tutorías",
            ugel="Sin formato oficial",
            nombre_docente=usuario.nombre_completo,
            nivel_educativo="General",
            area_curricular="General",
            grado_seccion="General"
        )
        session.add(espacio_libre)

    try:
        num_colegios = int(form_data.get("num_colegios", "0"))
    except ValueError:
        num_colegios = 0

    for i in range(1, num_colegios + 1):
        nombre_ie = form_data.get(f"colegio_{i}_nombre")
        if not nombre_ie:
            continue

        ugel = form_data.get(f"colegio_{i}_ugel", "")
        logo_file = form_data.get(f"colegio_{i}_logo")
        nombre_logo = None
        
        if logo_file and getattr(logo_file, "filename", ""):
            ext = os.path.splitext(logo_file.filename)[1].lower()
            if ext in [".png", ".jpg", ".jpeg", ".webp"]:
                nombre_logo = f"logo_{usuario.id}_{uuid.uuid4().hex[:8]}{ext}"
                ruta = os.path.join(UPLOAD_DIR, nombre_logo)
                with open(ruta, "wb") as buffer:
                    shutil.copyfileobj(logo_file.file, buffer)

        nuevo_colegio = PerfilInstitucional(
            usuario_id=usuario.id,
            nombre_ie=nombre_ie.strip(),
            ugel=ugel.strip(),
            nombre_docente=usuario.nombre_completo,
            logo_url=nombre_logo
        )
        session.add(nuevo_colegio)
        session.commit()
        session.refresh(nuevo_colegio)

        bloques = form_data.getlist(f"colegio_{i}_bloques[]")
        for bId in bloques:
            nivel = form_data.get(f"col_{i}_b{bId}_nivel", "Secundaria")
            area = form_data.get(f"col_{i}_b{bId}_area", "")
            if area == "Otro":
                area = form_data.get(f"col_{i}_b{bId}_area_otro", "Otro Curso").strip()
            
            grados = form_data.getlist(f"col_{i}_b{bId}_grados[]")
            for g in grados:
                secciones = form_data.getlist(f"col_{i}_b{bId}_g_{g}_secciones[]")
                if not secciones:
                    secciones = ["Única"]
                for s in secciones:
                    carga = CargaAcademica(
                        institucion_id=nuevo_colegio.id,
                        nivel=nivel,
                        area=area,
                        grado=g.strip(),
                        seccion=s.strip().upper()
                    )
                    session.add(carga)
            
    session.commit()
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

# ==========================================
# RUTAS DE CHAT Y GENERACIÓN IA
# ==========================================
@app.post("/enviar-mensaje", response_class=HTMLResponse)
async def enviar_mensaje(
    request: Request,
    prompt: str = Form(...),
    institucion_id: Optional[int] = Form(None),
    contexto_activo: str = Form(default="General"),
    grado_activo: str = Form(default="General"),
    seccion_activa: str = Form(default="Única"),
    modo_generacion: str = Form(default="CNEB"),
    foto: UploadFile = File(None),
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)

    ruta_guardada = None
    nombre_archivo_seguro = None
    
    if foto and foto.filename:
        ext = os.path.splitext(foto.filename)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".webp", ".pdf"]:
            nombre_archivo_seguro = f"{usuario.id}_{uuid.uuid4().hex[:12]}{ext}"
            ruta_guardada = os.path.join(UPLOAD_DIR, nombre_archivo_seguro)
            with open(ruta_guardada, "wb") as buffer:
                shutil.copyfileobj(foto.file, buffer)

    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    grado_completo = f"{grado_activo} - {seccion_activa}"

    if modo_generacion == "CNEB":
        perfil = None
        if institucion_id:
            perfil = session.exec(select(PerfilInstitucional).where(
                PerfilInstitucional.id == institucion_id,
                PerfilInstitucional.usuario_id == usuario.id
            )).first()
        if not perfil:
            perfil = session.exec(select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)).first()

        contexto_institucional = ""
        if perfil:
            contexto_institucional = (
                f"\n\n[DATOS INSTITUCIONALES PARA MEMBRETE]\n"
                f"- I.E.: {perfil.nombre_ie} (UGEL {perfil.ugel})\n"
                f"- Docente: {perfil.nombre_docente}\n"
                f"- Curso: {contexto_activo} | Aula: {grado_completo}\n"
                f"- Fecha de hoy: {fecha_actual}\n"
            )
        reglas_cneb = "\nREGLAS: Estructura la sesión con matrices pedagógicas según el CNEB (Inicio, Desarrollo, Cierre y Rúbrica)."
        prompt_final = f"{prompt}{contexto_institucional}{reglas_cneb}"
    else:
        prompt_final = prompt
        contexto_activo = "Modo Libre"
        grado_completo = "Sin aula específica"

    respuesta_ia = responder_consulta(prompt_final, ruta_guardada, modo_generacion)

    html_crudo = markdown.markdown(respuesta_ia, extensions=['tables', 'nl2br', 'fenced_code'])
    respuesta_html = sanitizar_contenido(html_crudo)

    titulo_limpio = prompt.strip()
    titulo_doc = (titulo_limpio[:45] + "...") if len(titulo_limpio) > 45 else titulo_limpio

    nueva_planificacion = Planificacion(
        usuario_id=usuario.id,
        institucion_id=institucion_id if modo_generacion == "CNEB" else None,
        titulo=titulo_doc.capitalize(),
        tipo_documento="Documento Pedagógico",
        area=contexto_activo,
        grado=grado_completo,
        contenido_markdown=respuesta_ia,
        prompt_docente=prompt,
        archivo_adjunto=nombre_archivo_seguro,
        modo_generacion=modo_generacion
    )
    session.add(nueva_planificacion)
    session.commit()
    session.refresh(nueva_planificacion)

    return templates.TemplateResponse(
        request=request,
        name="components/mensaje_ia.html",
        context={
            "prompt_usuario": prompt,
            "archivo_nombre": nombre_archivo_seguro,
            "respuesta_html": respuesta_html,
            "planificacion_id": nueva_planificacion.id,
            "area_contexto": contexto_activo,
            "grado_contexto": grado_completo,
            "es_nuevo": True,
            "modo_generacion": modo_generacion
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

    html_crudo = markdown.markdown(plan.contenido_markdown, extensions=['tables', 'nl2br', 'fenced_code'])
    respuesta_html = sanitizar_contenido(html_crudo)

    return templates.TemplateResponse(
        request=request,
        name="components/mensaje_ia.html",
        context={
            "prompt_usuario": plan.prompt_docente,
            "archivo_nombre": plan.archivo_adjunto,
            "respuesta_html": respuesta_html,
            "planificacion_id": plan.id,
            "es_nuevo": False,
            "modo_generacion": plan.modo_generacion
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

    instituciones = session.exec(
        select(PerfilInstitucional).where(PerfilInstitucional.usuario_id == usuario.id)
    ).all()

    datos_sedes = []
    for inst in instituciones:
        cargas = session.exec(
            select(CargaAcademica).where(CargaAcademica.institucion_id == inst.id)
        ).all()
        datos_sedes.append({"institucion": inst, "cargas": cargas})

    return templates.TemplateResponse(
        request=request,
        name="components/modal_perfil.html",
        context={"usuario": usuario, "datos_sedes": datos_sedes}
    )

@app.delete("/api/eliminar-carga/{carga_id}")
async def eliminar_carga(
    carga_id: int,
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse(status_code=401)

    carga = session.get(CargaAcademica, carga_id)
    if carga:
        inst = session.get(PerfilInstitucional, carga.institucion_id)
        if inst and inst.usuario_id == usuario.id:
            session.delete(carga)
            session.commit()
            return HTMLResponse("")
    return HTMLResponse(status_code=400)

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

    html_body = sanitizar_contenido(markdown.markdown(plan.contenido_markdown, extensions=['tables', 'nl2br']))

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

    nombre_seguro = "".join([c for c in plan.titulo if c.isalnum() or c == ' ']).rstrip().replace(' ', '_')
    headers = {
        "Content-Disposition": f'attachment; filename="{nombre_seguro}.doc"'
    }
    return Response(content=html_content, media_type="application/msword", headers=headers)

@app.get("/filtrar-historial", response_class=HTMLResponse)
async def filtrar_historial(
    request: Request,
    institucion_id: Optional[int] = None,
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
    
    boton_label = "Filtrar por aula activa" if ver_todos else "Ver todo el historial"
    toggle_flag = "" if ver_todos else "?ver_todos=true"
    
    boton_toggle = f"""
    <div id="contenedor-toggle-filtro" hx-swap-oob="true">
        <button hx-get="/filtrar-historial{toggle_flag}" 
                hx-include="#panel-contexto-dual" 
                hx-target="#lista-historial" 
                class="text-[11px] font-bold text-slate-600 dark:text-stone-300 hover:text-zen-700 bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 px-3 py-1.5 rounded-xl transition whitespace-nowrap">
            {boton_label}
        </button>
    </div>
    """

    contenido_lista = templates.get_template("components/lista_historial.html").render(
        {"planificaciones": planificaciones}
    )
    return HTMLResponse(content=contenido_lista + boton_toggle)

@app.get("/terminos", response_class=HTMLResponse)
async def terminos_condiciones(request: Request):
    return templates.TemplateResponse(request=request, name="terminos.html")

# ==========================================
# RUTAS DE GESTIÓN DE COLECCIONES (HTMX OOB)
# ==========================================
@app.post("/api/colecciones", response_class=HTMLResponse)
async def crear_coleccion(
    nombre: str = Form(...),
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse("<p>No autorizado</p>", status_code=401)
        
    nueva = Coleccion(
        usuario_id=usuario.id,
        nombre=nombre.strip(),
        color_tag="bg-zen-100 text-zen-800"
    )
    session.add(nueva)
    session.commit()
    session.refresh(nueva)

    html_boton = f"""
    <button hx-swap-oob="beforeend:#lista-colecciones-items" 
            class="w-full text-left px-3 py-2 rounded-lg hover:bg-calm-50 dark:hover:bg-calm-800 transition flex items-center gap-2 group">
        <span class="text-[10px]">📁</span>
        <span class="text-xs font-bold text-slate-700 dark:text-calm-200 truncate group-hover:text-zen-700 dark:group-hover:text-zen-400">{nueva.nombre}</span>
    </button>
    <script>document.getElementById('modal-coleccion').classList.add('hidden');</script>
    """
    return HTMLResponse(content=html_boton)

@app.post("/api/planificaciones/{plan_id}/mover", response_class=HTMLResponse)
async def mover_a_coleccion(
    plan_id: int,
    coleccion_id: Optional[int] = Form(default=None),
    usuario: Optional[Usuario] = Depends(obtener_usuario_actual),
    session: Session = Depends(obtener_session)
):
    if not usuario:
        return HTMLResponse(status_code=401)
        
    plan = session.get(Planificacion, plan_id)
    if plan and plan.usuario_id == usuario.id:
        plan.coleccion_id = coleccion_id if coleccion_id != 0 else None
        session.commit()
        return HTMLResponse("<span class='text-[10px] text-emerald-600 font-bold'>✓ Guardado</span>")
    
    return HTMLResponse(status_code=400)