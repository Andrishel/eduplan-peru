This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: venv, venv/**, __pycache__, *.png, *.jpg, .env
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
app/
  services/
    __init__.py
    auth_service.py
    gemini_service.py
    storage_service.py
  static/
    uploads/
      .gitkeep
  templates/
    components/
      lista_historial.html
      mensaje_ia.html
      modal_perfil.html
      perfil_badge.html
    landing/
      components/
        beneficios.html
        faq.html
        planes.html
      footer.html
      header.html
    auth.html
    base.html
    index.html
    landing.html
    onboarding.html
    terminos.html
  __init__.py
  database.py
  main.py
  models.py
.gitignore
exportar.sh
requirements.txt
```

# Files

## File: exportar.sh
```bash
#!/bin/bash
npx repomix --style markdown --output context_completo.md --ignore "venv,venv/**,__pycache__,*.png,*.jpg,.env"
echo "✅ context_completo.md generado con éxito en la raíz del proyecto."
```

## File: app/services/__init__.py
```python

```

## File: app/services/storage_service.py
```python
import os
import uuid
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "colegios"

def subir_logo_supabase(archivo_bytes: bytes, nombre_original: str, usuario_id: int) -> Optional[str]:
    if not archivo_bytes or not nombre_original:
        return None

    ext = os.path.splitext(nombre_original)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
        return None

    nombre_remoto = f"usr_{usuario_id}/{uuid.uuid4().hex[:10]}{ext}"

    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=nombre_remoto,
            file=archivo_bytes,
            file_options={"content-type": f"image/{ext.replace('.', '')}"}
        )
        url_publica = supabase.storage.from_(BUCKET_NAME).get_public_url(nombre_remoto)
        return url_publica
    except Exception as e:
        print(f"Error subiendo imagen a Supabase Storage: {e}")
        return None
```

## File: app/static/uploads/.gitkeep
```

```

## File: app/templates/components/perfil_badge.html
```html
<div id="sidebar-perfil-container" class="p-3 border-t border-slate-200">
  <button 
    type="button" 
    hx-get="/modal-perfil" 
    hx-target="#modal-slot" 
    hx-swap="innerHTML"
    class="w-full text-left flex items-center gap-3 p-2 rounded-xl bg-slate-50 hover:bg-blue-50 border border-slate-100 transition group">
    <div class="h-9 w-9 rounded-full bg-blue-100 group-hover:bg-blue-200 flex items-center justify-center font-bold text-blue-800 text-sm shrink-0 transition">
      {% if perfil and perfil.nombre_ie %}
        {{ perfil.nombre_ie[:2]|upper }}
      {% else %}
        IE
      {% endif %}
    </div>
    <div class="truncate flex-1">
      <p class="text-xs font-bold text-slate-800 group-hover:text-blue-900 truncate">
        {{ perfil.nombre_ie if perfil else 'I.E. Emblemática' }}
      </p>
      <p class="text-[10px] text-slate-400 font-medium truncate">
        {{ perfil.nombre_docente if perfil else 'Docente Activo' }} • {{ perfil.ugel if perfil else 'UGEL 01' }}
      </p>
    </div>
    <span class="text-slate-400 group-hover:text-blue-700 text-xs">⚙️</span>
  </button>
</div>
```

## File: app/templates/landing/components/faq.html
```html
<section id="faq" class="py-20 bg-calm-50 border-t border-calm-200/60">
    <div class="max-w-4xl mx-auto px-6">
        
        <!-- Encabezado de la sección -->
        <div class="text-center mb-14">
            <span class="inline-block rounded-full bg-zen-50 border border-zen-200 px-3.5 py-1 text-xs font-bold text-zen-700 uppercase tracking-wider mb-3">
                Dudas Resueltas
            </span>
            <h2 class="text-3xl md:text-4xl font-extrabold text-calm-800 mb-3">Preguntas Frecuentes</h2>
            <p class="text-slate-500 text-sm md:text-base max-w-lg mx-auto font-medium">
                Todo lo que directores y docentes consultan antes de incorporar EduPlan Perú.
            </p>
        </div>

        <!-- Lista Acordeón -->
        <div class="space-y-4">
            
            <!-- Pregunta 1 -->
            <details class="group rounded-2xl bg-white border border-calm-200/80 p-5 shadow-sm transition hover:border-zen-300">
                <summary class="flex justify-between items-center text-sm md:text-base font-bold text-slate-800 cursor-pointer list-none select-none">
                    <span class="group-hover:text-zen-700 transition">¿Los documentos cumplen con las exigencias de monitoreo de la UGEL?</span>
                    <span class="h-7 w-7 rounded-full bg-calm-50 flex items-center justify-center text-xs text-slate-400 group-hover:bg-zen-50 group-hover:text-zen-700 group-open:rotate-180 transition shrink-0 ml-3">▾</span>
                </summary>
                <div class="mt-3 text-xs md:text-sm text-slate-600 leading-relaxed border-t border-calm-100 pt-3">
                    Sí. Toda la matriz curricular respeta el <strong>CNEB</strong>, los procesos pedagógicos (problematización, propósito, motivación, saberes previos) y los procesos didácticos propios de cada área (Matemática, Comunicación, Ciencia y Tecnología, etc.). Además, los criterios e instrumentos están alineados a la escala valorativa oficial (AD, A, B, C) según la <strong>RVM N° 094-2020-MINEDU</strong>.
                </div>
            </details>

            <!-- Pregunta 2 -->
            <details class="group rounded-2xl bg-white border border-calm-200/80 p-5 shadow-sm transition hover:border-zen-300">
                <summary class="flex justify-between items-center text-sm md:text-base font-bold text-slate-800 cursor-pointer list-none select-none">
                    <span class="group-hover:text-zen-700 transition">¿Puedo descargar en Word y llevar los archivos a un colegio sin internet?</span>
                    <span class="transition h-7 w-7 rounded-full bg-calm-50 flex items-center justify-center text-xs text-slate-400 group-hover:bg-zen-50 group-hover:text-zen-700 group-open:rotate-180 shrink-0 ml-3">▾</span>
                </summary>
                <div class="mt-3 text-xs md:text-sm text-slate-600 leading-relaxed border-t border-calm-100 pt-3">
                    Totalmente. Puedes generar tus sesiones o instrumentos en casa o con datos móviles, presionar <strong>"Word (.docx)"</strong> y guardar el archivo editable en una memoria USB. En el aula o institución podrás abrirlo, modificarlo o imprimirlo sin necesidad de conexión.
                </div>
            </details>

            <!-- Pregunta 3 -->
            <details class="group rounded-2xl bg-white border border-calm-200/80 p-5 shadow-sm transition hover:border-zen-300">
                <summary class="flex justify-between items-center text-sm md:text-base font-bold text-slate-800 cursor-pointer list-none select-none">
                    <span class="group-hover:text-zen-700 transition">¿Cómo ayuda a las directoras y directores en su labor de gestión?</span>
                    <span class="transition h-7 w-7 rounded-full bg-calm-50 flex items-center justify-center text-xs text-slate-400 group-hover:bg-zen-50 group-hover:text-zen-700 group-open:rotate-180 shrink-0 ml-3">▾</span>
                </summary>
                <div class="mt-3 text-xs md:text-sm text-slate-600 leading-relaxed border-t border-calm-100 pt-3">
                    El modo Directivo genera con un clic las <strong>Resoluciones Directorales (RD)</strong> para comités de gestión escolar (condiciones operativas, gestión pedagógica y bienestar), actas de asamblea de padres, oficios técnicos a la UGEL y fichas de monitoreo basadas en las 5 rúbricas de desempeño docente del MINEDU.
                </div>
            </details>

            <!-- Pregunta 4 -->
            <details class="group rounded-2xl bg-white border border-calm-200/80 p-5 shadow-sm transition hover:border-zen-300">
                <summary class="flex justify-between items-center text-sm md:text-base font-bold text-slate-800 cursor-pointer list-none select-none">
                    <span class="transition group-hover:text-zen-700">¿Cómo funciona el Plan Institucional para colegios?</span>
                    <span class="transition h-7 w-7 rounded-full bg-calm-50 flex items-center justify-center text-xs text-slate-400 group-hover:bg-zen-50 group-hover:text-zen-700 group-open:rotate-180 shrink-0 ml-3">▾</span>
                </summary>
                <div class="mt-3 text-xs md:text-sm text-slate-600 leading-relaxed border-t border-calm-100 pt-3">
                    Se configura una sola vez el membrete, logo, lema y el enfoque del Proyecto Educativo Institucional (PEI). Todos los docentes del colegio tienen su acceso y cuando la IA genera una sesión, adopta automáticamente la identidad de la institución educativa, estandarizando las entregas ante revisiones pedagógicas.
                </div>
            </details>

            <!-- Pregunta 5 -->
            <details class="group rounded-2xl bg-white border border-calm-200/80 p-5 shadow-sm transition hover:border-zen-300">
                <summary class="flex justify-between items-center text-sm md:text-base font-bold text-slate-800 cursor-pointer list-none select-none">
                    <span class="group-hover:text-zen-700 transition">¿La plataforma reemplaza la labor del profesor?</span>
                    <span class="transition h-7 w-7 rounded-full bg-calm-50 flex items-center justify-center text-xs text-slate-400 group-hover:bg-zen-50 group-hover:text-zen-700 group-open:rotate-180 shrink-0 ml-3">▾</span>
                </summary>
                <div class="mt-3 text-xs md:text-sm text-slate-600 leading-relaxed border-t border-calm-100 pt-3">
                    No. Es un asistente de apoyo que asume el 80% de la carga burocrática y de redacción técnica. El docente aporta el diagnóstico de sus estudiantes, revisa la propuesta y aplica la mediación didáctica en el aula.
                </div>
            </details>

        </div>
    </div>
</section>
```

## File: app/templates/terminos.html
```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones | EduPlan Perú</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Nunito', 'sans-serif'] },
                    colors: {
                        calm: { 50: '#fafaf9', 100: '#f5f5f4', 200: '#e7e5e4', 800: '#292524', 900: '#1c1917' },
                        zen: { 50: '#f0fdfa', 100: '#ccfbf1', 600: '#0d9488', 700: '#0f766e', 800: '#115e59', 900: '#134e4a' }
                    }
                }
            }
        }
    </script>
</head>

<body class="bg-calm-50 font-sans text-calm-800 antialiased selection:bg-zen-600 selection:text-white">

    <!-- Header Compacto -->
    <header class="bg-white border-b border-calm-200 sticky top-0 z-30">
        <div class="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center gap-2.5">
                <div class="flex h-8 w-8 items-center justify-center rounded-xl bg-zen-700 text-sm font-black text-white">EP</div>
                <span class="text-base font-black tracking-tight text-calm-800">EduPlan Perú</span>
            </a>
            <a href="/" class="text-xs font-bold text-zen-700 hover:text-zen-800 flex items-center gap-1">
                ← Volver al inicio
            </a>
        </div>
    </header>

    <!-- Contenido Legal -->
    <main class="max-w-4xl mx-auto px-6 py-12 md:py-16">
        <div class="bg-white border border-calm-200 rounded-3xl p-8 md:p-12 shadow-sm space-y-8">
            
            <div class="border-b border-calm-200 pb-6">
                <span class="inline-block bg-zen-50 border border-zen-200 px-3 py-1 rounded-full text-[11px] font-extrabold text-zen-800 uppercase tracking-wider mb-2">
                    Marco Legal Vigente &bull; República del Perú
                </span>
                <h1 class="text-3xl font-black text-calm-900">Términos y Condiciones de Uso</h1>
                <p class="text-xs text-slate-500 mt-2">Última actualización: Septiembre de 2026</p>
            </div>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">1. Aceptación de los Términos</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    Al registrarse, acceder o utilizar la plataforma web <strong>EduPlan Perú</strong>, el usuario declara haber leído, comprendido y aceptado en su totalidad los presentes Términos y Condiciones. Si no está de acuerdo con alguna disposición, deberá abstenerse de utilizar el servicio.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">2. Naturaleza y Alcance del Servicio</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    EduPlan Perú es un software como servicio (SaaS) que proporciona asistencia pedagógica basada en inteligencia artificial, diseñada para optimizar la formulación de programaciones curriculares, unidades de aprendizaje, sesiones de clase, rúbricas de evaluación e instrumentos de gestión directiva conforme al Currículo Nacional de la Educación Básica (CNEB) y las normativas emitidas por el Ministerio de Educación del Perú (MINEDU), en particular la Resolución Viceministerial N° 094-2020-MINEDU.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">3. Responsabilidad Pedagógica y Criterio Profesional</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    Los contenidos, borradores y estructuras generadas por la plataforma constituyen herramientas de apoyo técnico. El docente o directivo es el único responsable de revisar, adaptar, validar y contextualizar los documentos a la realidad sociocultural, diagnóstica e inclusiva de sus estudiantes antes de su aplicación en el aula o presentación formal ante especialistas de UGEL o DRE.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">4. Registro de Cuentas y Seguridad</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    El usuario es responsable de mantener la confidencialidad de sus credenciales de acceso. Cada cuenta es de uso personal e intransferible, salvo en los planes institucionales donde se otorguen accesos colegiados gestionados por la dirección escolar.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">5. Protección de Datos Personales (Ley N° 29733)</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    En cumplimiento de la <strong>Ley N° 29733 (Ley de Protección de Datos Personales del Perú)</strong> y su reglamento, los datos institucionales (nombres de instituciones, logos, cargas horarias y nombres de docentes) son tratados con estricta confidencialidad para fines exclusivos de la personalización de las plantillas y el funcionamiento de la cuenta. EduPlan Perú no comercializa ni comparte información con terceros.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">6. Propiedad Intelectual</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    Los diseños de interfaz, código fuente, logotipos y algoritmos de procesamiento pertenecen exclusivamente a EduPlan Perú. Por su parte, los documentos finales exportados en formatos editables (.docx, .pdf) son de libre disposición y propiedad del docente o institución que los genera.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">7. Planes, Pagos y Cancelación</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    El acceso a los planes de pago se otorga mediante suscripción mensual en moneda nacional (PEN). El usuario puede cancelar la continuidad de su servicio en cualquier momento sin penalidad alguna, conservando el acceso a sus documentos hasta el término del periodo facturado.
                </p>
            </section>

            <section class="space-y-3">
                <h2 class="text-base font-black text-slate-800">8. Jurisdicción y Ley Aplicable</h2>
                <p class="text-xs md:text-sm text-slate-600 leading-relaxed">
                    Estos términos se rigen por las leyes de la República del Perú. Cualquier controversia será sometida a la competencia de los juzgados y tribunales de la jurisdicción correspondiente.
                </p>
            </section>

            <div class="pt-6 border-t border-calm-200 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
                <span>Canal de atención legal y soporte: soporte@eduplanperu.pe</span>
                <a href="/auth" class="px-5 py-2.5 rounded-xl bg-zen-700 text-white font-bold hover:bg-zen-800 transition">
                    Iniciar Sesión
                </a>
            </div>

        </div>
    </main>

</body>

</html>
```

## File: app/__init__.py
```python

```

## File: app/services/auth_service.py
```python
import hashlib
import os
import secrets
from itsdangerous import URLSafeTimedSerializer
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or "cambiar_en_produccion" in SECRET_KEY:
    SECRET_KEY = secrets.token_hex(32)

serializer = URLSafeTimedSerializer(SECRET_KEY)

def hashear_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verificar_password(password_plano: str, password_hash: str) -> bool:
    try:
        salt, key_hex = password_hash.split('$')
        key_verificar = hashlib.pbkdf2_hmac(
            'sha256',
            password_plano.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(key_verificar.hex(), key_hex)
    except Exception:
        return False

def crear_token_sesion(usuario_id: int) -> str:
    return serializer.dumps(usuario_id, salt="auth-cookie")

def decodificar_token_sesion(token: str, max_age: int = 604800) -> Optional[int]:
    try:
        return serializer.loads(token, salt="auth-cookie", max_age=max_age)
    except Exception:
        return None
```

## File: app/services/gemini_service.py
```python
import os
import time
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_CNEB = """
Eres EduPlan Perú, un asistente técnico-pedagógico experto en el Currículo Nacional de Educación Básica (CNEB) y normativas del MINEDU (RVM N° 094-2020).
1. Si el docente saluda, responde de forma cálida y pregúntale en qué área o tema necesita planificar.
2. Si pide una sesión, ficha o unidad, NO saludes, inicia DIRECTAMENTE con el encabezado formal (# SESIÓN DE APRENDIZAJE N° ...).
3. Usa la estructura oficial: Datos informativos, Propósitos (Competencias, Capacidades, Criterios y Evidencias en tabla), Secuencia didáctica (Inicio, Desarrollo, Cierre con tiempos) y Rúbrica (AD, A, B, C).
4. Fórmulas matemáticas: usa formato delimitado por signos de dólar ($...$ o $$...$$).
"""

PROMPT_LIBRE = """
Eres EduPlan Perú, un consultor pedagógico experto.
Estás en MODO LIBRE. Compórtate de forma directa, conversacional y experta.
Resuelve dudas curriculares, lluvia de ideas o redacción sin forzar formatos rígidos de tabla escolar.
"""

MODELOS_CONFIRMADOS = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest"
]

def responder_consulta(mensaje: str, ruta_archivo: str = None, modo: str = "CNEB") -> str:
    if not mensaje or not mensaje.strip():
        return "Por favor, escribe una consulta o tema pedagógico para comenzar."

    contenidos = []
    if ruta_archivo and os.path.exists(ruta_archivo):
        ext = os.path.splitext(ruta_archivo)[1].lower()
        try:
            if ext in [".png", ".jpg", ".jpeg", ".webp"]:
                contenidos.append(Image.open(ruta_archivo))
            elif ext == ".pdf":
                archivo_remoto = client.files.upload(file=ruta_archivo)
                contenidos.append(archivo_remoto)
        except Exception as err:
            print(f"Error procesando adjunto para Gemini: {err}")

    contenidos.append(mensaje)
    ultimo_error = None
    instruccion_activa = PROMPT_CNEB if modo == "CNEB" else PROMPT_LIBRE

    for modelo in MODELOS_CONFIRMADOS:
        try:
            respuesta = client.models.generate_content(
                model=modelo,
                contents=contenidos,
                config=types.GenerateContentConfig(
                    system_instruction=instruccion_activa,
                    temperature=0.2 if modo == "CNEB" else 0.5,
                )
            )
            return respuesta.text
        except Exception as e:
            ultimo_error = e
            time.sleep(0.4)
            continue

    return f"⚠️ Error al conectar con la IA: {str(ultimo_error)}"
```

## File: app/templates/components/lista_historial.html
```html
{% if planificaciones %}
    {% for plan in planificaciones %}
    <button hx-get="/historial/{{ plan.id }}" hx-target="#area-documento" class="w-full text-left px-3 py-2.5 rounded-lg hover:bg-calm-50 dark:hover:bg-calm-800 transition group flex flex-col gap-0.5 border-l-2 border-transparent hover:border-zen-600 dark:hover:border-zen-400">
        <span class="text-xs font-bold text-slate-700 dark:text-calm-200 truncate group-hover:text-zen-700 dark:group-hover:text-zen-400 transition">{{ plan.titulo }}</span>
        
        {% if plan.modo_generacion == 'LIBRE' %}
            <span class="text-[10px] text-slate-400 dark:text-stone-500 font-bold tracking-wide">💭 Asistente Libre</span>
        {% else %}
            <span class="text-[10px] text-slate-400 dark:text-stone-400 truncate font-medium">{{ plan.area }} • {{ plan.grado }}</span>
        {% endif %}
    </button>
    {% endfor %}
{% else %}
    <div class="px-3 py-4 text-xs text-slate-400 dark:text-stone-500 italic text-center">
        No hay planificaciones recientes.
    </div>
{% endif %}
```

## File: app/templates/landing/components/beneficios.html
```html
<section id="beneficios" class="py-24 bg-white relative">
    <div class="max-w-6xl mx-auto px-6 relative z-10">
        
        <div class="text-center mb-16">
            <span class="inline-block rounded-full bg-zen-50 border border-zen-200 px-3 py-1 text-[10px] font-extrabold text-zen-700 uppercase tracking-wider mb-3">
                Propuesta de Valor
            </span>
            <h2 class="text-3xl md:text-4xl font-extrabold text-calm-800 mb-4">Diseñado para la realidad educativa peruana</h2>
            <p class="text-slate-500 max-w-2xl mx-auto text-sm md:text-base">Respuestas técnicas ajustadas a la estructura formal exigida por especialistas de UGEL y DRE.</p>
        </div>

        <div class="grid md:grid-cols-3 gap-6 md:gap-8">
            
            <!-- Card 1 -->
            <a href="https://www.minedu.gob.pe/curriculo/pdf/rvm-094-2020-minedu.pdf" target="_blank" class="group block bg-white border border-calm-200 rounded-3xl p-8 hover:-translate-y-1.5 hover:shadow-xl hover:border-zen-200 transition-all duration-300">
                <div class="flex items-center justify-between mb-6">
                    <div class="h-10 w-10 rounded-xl bg-zen-700 text-white flex items-center justify-center font-black text-lg shadow-sm">01</div>
                    <span class="text-[10px] font-extrabold text-zen-700 uppercase tracking-wider">Currículo CNEB</span>
                </div>
                <h3 class="text-xl font-extrabold text-calm-800 mb-3">Alineación Curricular Estricta</h3>
                <p class="text-sm text-slate-500 leading-relaxed mb-6">
                    Formulación precisa de competencias, capacidades, desempeños precisados y enfoques transversales contextualizados a la realidad del aula sin mezclar terminologías extranjeras.
                </p>
                <div class="mt-auto flex items-center text-xs font-bold text-zen-700">
                    Cumplimiento RVM N° 094-2020 <span class="ml-2 transition-transform duration-300 group-hover:translate-x-2">→</span>
                </div>
            </a>

            <!-- Card 2 -->
            <a href="/auth" class="group block bg-white border border-calm-200 rounded-3xl p-8 hover:-translate-y-1.5 hover:shadow-xl hover:border-blue-200 transition-all duration-300">
                <div class="flex items-center justify-between mb-6">
                    <div class="h-10 w-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-black text-lg shadow-sm">02</div>
                    <span class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Editorial Limpia</span>
                </div>
                <h3 class="text-xl font-extrabold text-calm-800 mb-3">Exportación a Word y PDF</h3>
                <p class="text-sm text-slate-500 leading-relaxed mb-6">
                    Descarga inmediata con márgenes oficiales, encabezados estandarizados y matrices tabuladas. Diseñado para imprimir directamente o archivar en tu carpeta pedagógica.
                </p>
                <div class="mt-auto flex items-center text-xs font-bold text-blue-600">
                    Listo para presentación técnica <span class="ml-2 transition-transform duration-300 group-hover:translate-x-2">→</span>
                </div>
            </a>

            <!-- Card 3 -->
            <a href="/auth" class="group block bg-white border border-calm-200 rounded-3xl p-8 hover:-translate-y-1.5 hover:shadow-xl hover:border-amber-200 transition-all duration-300">
                <div class="flex items-center justify-between mb-6">
                    <div class="h-10 w-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-black text-lg shadow-sm">03</div>
                    <span class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Liderazgo Escolar</span>
                </div>
                <h3 class="text-xl font-extrabold text-calm-800 mb-3">Gestión Directiva Ágil</h3>
                <p class="text-sm text-slate-500 leading-relaxed mb-6">
                    Generación estructurada de Resoluciones Directorales (RD), oficios formales y fichas de monitoreo basadas en las 5 rúbricas de desempeño docente del MINEDU.
                </p>
                <div class="mt-auto flex items-center text-xs font-bold text-amber-600">
                    Comités de Gestión 2026 <span class="ml-2 transition-transform duration-300 group-hover:translate-x-2">→</span>
                </div>
            </a>

        </div>
    </div>
</section>
```

## File: app/templates/landing/footer.html
```html
<footer class="bg-zen-900 text-white pt-16 pb-12 border-t border-zen-800">
    <div class="max-w-6xl mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-zen-800/80">
            
            <!-- Columna 1: Identidad -->
            <div class="space-y-4">
                <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-white text-zen-900 text-lg font-black shadow-sm">
                        EP
                    </div>
                    <div>
                        <span class="text-lg font-black tracking-tight text-white block leading-tight">EduPlan Perú</span>
                        <span class="text-[10px] font-bold text-zen-400 tracking-wider uppercase block">Gestión Curricular</span>
                    </div>
                </div>
                <p class="text-xs text-zen-200/80 leading-relaxed">
                    Asistencia técnica, curricular y directiva para instituciones educativas públicas y privadas del Perú.
                </p>
                <div class="inline-flex items-center gap-2 bg-zen-950/60 border border-zen-800 px-3 py-1.5 rounded-xl text-[11px] font-bold text-zen-400">
                    <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    Plataforma Activa &bull; Ciclo Escolar 2026
                </div>
            </div>

            <!-- Columna 2: Niveles Educativos (Texto estático sin hover engañoso) -->
            <div>
                <h4 class="text-xs font-black uppercase tracking-wider text-zen-300 mb-4">Niveles Educativos</h4>
                <ul class="space-y-2.5 text-xs text-zen-200/90 select-none">
                    <li>
                        <span class="font-bold text-white block">Inicial</span>
                        <span class="text-[11px] text-zen-400">Aulas de 3, 4 y 5 años </span>
                    </li>
                    <li>
                        <span class="font-bold text-white block">Primaria Regular</span>
                        <span class="text-[11px] text-zen-400">De 1° a 6° grado </span>
                    </li>
                    <li>
                        <span class="font-bold text-white block">Secundaria</span>
                        <span class="text-[11px] text-zen-400">De 1° a 5° año </span>
                    </li>
                </ul>
            </div>

            <!-- Columna 3: Base Normativa MINEDU -->
            <div>
                <h4 class="text-xs font-black uppercase tracking-wider text-zen-300 mb-4">Base Normativa MINEDU</h4>
                <ul class="space-y-2.5 text-xs text-zen-200/80">
                    <li>
                        <a href="https://www.minedu.gob.pe/curriculo/" target="_blank" rel="noopener noreferrer" class="hover:text-white transition flex items-center gap-1.5">
                            <span>Currículo Nacional (CNEB)</span>
                            <span class="text-[10px] text-zen-400">↗</span>
                        </a>
                    </li>
                    <li>
                        <a href="https://www.minedu.gob.pe/curriculo/pdf/rvm-094-2020-minedu.pdf" target="_blank" rel="noopener noreferrer" class="hover:text-white transition flex items-center gap-1.5">
                            <span>RVM N° 094-2020-MINEDU</span>
                            <span class="text-[10px] text-zen-400">↗</span>
                        </a>
                    </li>
                    <li>
                        <span class="text-zen-200/70 block">Comités de Gestión Escolar 2026</span>
                    </li>
                    <li>
                        <span class="text-zen-200/70 block">Marco de Buen Desempeño Docente</span>
                    </li>
                </ul>
            </div>

            <!-- Columna 4: Contacto y Convenios -->
            <div>
                <h4 class="text-xs font-black uppercase tracking-wider text-zen-300 mb-4">Contacto y Convenios</h4>
                <p class="text-xs text-zen-200/80 mb-4 leading-relaxed">
                    Coordinación directa para colegios, directivos y soporte pedagógico:
                </p>
                <a href="https://wa.me/51922498580?text=Hola,%20solicito%20información%20sobre%20EduPlan%20Perú" target="_blank" rel="noopener noreferrer"
                    class="inline-flex items-center justify-center gap-2 w-full rounded-xl bg-teal-500 hover:bg-teal-400 px-4 py-2.5 text-xs font-extrabold text-zen-950 transition shadow-lg shadow-teal-500/20">
                    <span>💬 WhatsApp Oficial</span>
                </a>
                <span class="block text-[11px] text-zen-400 mt-4">
                    Desarrollado y administrado por Andrishel Alvarez M.
                </span>
            </div>

        </div>

        <!-- Barra Inferior Legal -->
        <div class="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-zen-400">
            <p>&copy; 2026 EduPlan Perú. Todos los derechos reservados.</p>
            <div class="flex items-center gap-6">
                <a href="/terminos" class="hover:text-white transition underline underline-offset-4 font-semibold">
                    Términos y Condiciones del Servicio
                </a>
                <span class="hidden md:inline text-zen-600">&bull;</span>
                <span class="hidden md:inline text-zen-400">Comprometidos con la educación peruana.</span>
            </div>
        </div>
    </div>
</footer>
```

## File: app/templates/landing/header.html
```html
<header class="bg-white/90 backdrop-blur-md sticky top-0 z-50 border-b border-calm-100">
    <div class="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">

        <!-- Logo e Identidad -->
        <a href="/" class="flex items-center gap-3 group">
            <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-zen-700 text-xl font-black text-white shadow-sm group-hover:scale-105 transition-transform">
                EP
            </div>
            <div>
                <span class="text-xl font-black tracking-tight text-calm-800 block leading-tight">EduPlan Perú</span>
                <span class="text-[10px] font-bold text-zen-700 tracking-wider uppercase block">Gestión Curricular</span>
            </div>
        </a>

        <!-- Enlaces Centrales con efecto Píldora (Hover Background) -->
        <nav class="hidden md:flex items-center gap-2 text-xs font-extrabold text-slate-600">
            <a href="#beneficios" class="px-4 py-2.5 rounded-xl hover:bg-calm-100 hover:text-zen-700 transition-all">Beneficios</a>
            <a href="#planes" class="px-4 py-2.5 rounded-xl hover:bg-calm-100 hover:text-zen-700 transition-all">Planes y Precios</a>
            <a href="#faq" class="px-4 py-2.5 rounded-xl hover:bg-calm-100 hover:text-zen-700 transition-all">Preguntas Frecuentes</a>
        </nav>

        <!-- Acciones -->
        <div class="flex items-center gap-2">
            <!-- Soporte también con efecto píldora -->
            <a href="https://wa.me/51922498580?text=Hola,%20tengo%20consultas%20sobre%20EduPlan%20Perú" target="_blank"
                class="hidden sm:inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:bg-calm-100 hover:text-zen-700 transition-all">
                <span>💬 Soporte</span>
            </a>
            
            <!-- Botón Principal -->
            <a href="/auth"
                class="ml-2 rounded-full bg-zen-700 px-6 py-2.5 text-xs font-extrabold text-white shadow hover:bg-zen-800 hover:shadow-md hover:-translate-y-0.5 transition-all">
                Iniciar Sesión
            </a>
        </div>

    </div>
</header>
```

## File: app/templates/auth.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso al Sistema | EduPlan Perú</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Nunito', 'sans-serif'] },
                    colors: {
                        calm: {
                            50: '#fafaf9',
                            100: '#f5f5f4',
                            200: '#e7e5e4',
                            800: '#292524',
                        },
                        zen: {
                            50: '#f0fdfa',
                            100: '#ccfbf1',
                            600: '#0d9488',
                            700: '#0f766e',
                            800: '#115e59',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #fafaf9; color: #292524; }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-zen-600 selection:text-white">

    <!-- Barra de Navegación Simple -->
    <header class="w-full max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2.5 group">
            <div class="flex h-9 w-9 items-center justify-center rounded-2xl bg-zen-700 text-lg font-black text-white shadow-sm group-hover:scale-105 transition">
                EP
            </div>
            <div>
                <span class="text-lg font-black tracking-tight text-calm-800 block leading-tight">EduPlan Perú</span>
                <span class="text-[9px] font-bold text-zen-700 tracking-wider uppercase block">Gestión Curricular</span>
            </div>
        </a>

        <a href="/" class="text-xs font-bold text-slate-500 hover:text-zen-700 transition flex items-center gap-1">
            <span>← Volver a la portada</span>
        </a>
    </header>

    <!-- Contenedor Principal Centrado -->
    <main class="flex-1 flex items-center justify-center px-4 py-8">
        <div class="w-full max-w-md bg-white rounded-3xl border border-calm-200 shadow-xl shadow-slate-200/50 p-7 sm:p-9 transition-all">
            
            <!-- Selector de Modo (Tabs) -->
            <div class="flex rounded-2xl bg-calm-100 p-1 mb-7 text-xs font-bold">
                <button id="tab-login" onclick="cambiarTab('login')" type="button" class="flex-1 py-2.5 rounded-xl bg-white text-calm-800 shadow-sm transition">
                    Iniciar Sesión
                </button>
                <button id="tab-registro" onclick="cambiarTab('registro')" type="button" class="flex-1 py-2.5 rounded-xl text-slate-500 hover:text-calm-800 transition">
                    Crear Cuenta
                </button>
            </div>

            <!-- Botón Principal: Acceso con Google -->
            <a href="/onboarding" class="w-full flex items-center justify-center gap-3 rounded-2xl border border-calm-200 bg-white py-3 text-xs sm:text-sm font-bold text-slate-700 hover:bg-calm-50 hover:border-slate-300 transition shadow-sm mb-6 group">
                <svg class="h-4 w-4 shrink-0" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17Z"/>
                    <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.26v3.15C3.25 21.36 7.33 24 12 24Z"/>
                    <path fill="#FBBC05" d="M5.28 14.27a7.195 7.195 0 0 1 0-4.54V6.58H1.26a11.988 11.988 0 0 0 0 10.84l4.02-3.15Z"/>
                    <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.25 2.64 1.26 6.58l4.02 3.15c.95-2.83 3.6-4.98 6.72-4.98Z"/>
                </svg>
                <span id="google-btn-text">Continuar con Google</span>
            </a>

            <!-- Separador -->
            <div class="relative flex items-center justify-center mb-6">
                <div class="border-t border-calm-200 w-full"></div>
                <span class="bg-white px-3 text-[11px] font-bold text-slate-400 uppercase tracking-wider">o con tu correo</span>
            </div>

            <!-- Formulario de Iniciar Sesión -->
            <form id="form-login" action="/auth/login" method="POST" class="space-y-4 text-xs">
                <div>
                    <label class="block font-bold text-slate-700 mb-1">Correo Electrónico</label>
                    <input type="email" name="correo" placeholder="ejemplo@ie.edu.pe o personal" required class="w-full rounded-xl border border-calm-200 p-3 text-slate-900 focus:border-zen-700 focus:outline-none transition">
                </div>
                <div>
                    <div class="flex items-center justify-between mb-1">
                        <label class="font-bold text-slate-700">Contraseña</label>
                        <a href="#" class="text-[11px] font-semibold text-zen-700 hover:underline">¿La olvidaste?</a>
                    </div>
                    <input type="password" name="password" placeholder="Tu contraseña" required class="w-full rounded-xl border border-calm-200 p-3 text-slate-900 focus:border-zen-700 focus:outline-none transition">
                </div>
                <button type="submit" class="w-full rounded-2xl bg-zen-700 py-3.5 font-extrabold text-white text-xs sm:text-sm hover:bg-zen-800 transition shadow-md shadow-zen-700/20 mt-2 cursor-pointer">
                    Entrar al Espacio de Trabajo
                </button>
            </form>

            <!-- Formulario de Registro (Oculto por defecto) -->
            <form id="form-registro" action="/auth/registro" method="POST" class="space-y-4 text-xs hidden">
                <div>
                    <label class="block font-bold text-slate-700 mb-1">Nombre Completo</label>
                    <input type="text" name="nombre_completo" placeholder="Prof. o Directora Nombres y Apellidos" required class="w-full rounded-xl border border-calm-200 p-3 text-slate-900 focus:border-zen-700 focus:outline-none transition">
                </div>
                <div>
                    <label class="block font-bold text-slate-700 mb-1">Correo Electrónico</label>
                    <input type="email" name="correo" placeholder="ejemplo@ie.edu.pe o gmail" required class="w-full rounded-xl border border-calm-200 p-3 text-slate-900 focus:border-zen-700 focus:outline-none transition">
                </div>
                <div>
                    <label class="block font-bold text-slate-700 mb-1">Rol en la Institución</label>
                    <select name="rol" class="w-full rounded-xl border border-calm-200 p-3 text-slate-900 focus:border-zen-700 focus:outline-none transition bg-white font-medium">
                        <option value="Docente">Docente de Aula / Especialidad</option>
                        <option value="Directivo">Directivo / Coordinador Pedagógico</option>
                    </select>
                </div>
                <div>
                    <label class="block font-bold text-slate-700 mb-1">Contraseña Nueva</label>
                    <input type="password" name="password" placeholder="Mínimo 6 caracteres" minlength="6" required class="w-full rounded-xl border border-calm-200 p-3 text-slate-900 focus:border-zen-700 focus:outline-none transition">
                </div>
                <div class="text-[11px] text-slate-500 leading-tight">
                    Al registrarte, inicias tu período de <strong>7 días de prueba gratuita completa</strong> sin cobros automáticos.
                </div>
                <button type="submit" class="w-full rounded-2xl bg-zen-700 py-3.5 font-extrabold text-white text-xs sm:text-sm hover:bg-zen-800 transition shadow-md shadow-zen-700/20 mt-2 cursor-pointer">
                    Crear Cuenta e Iniciar Prueba
                </button>
            </form>

            <!-- Nota de Confianza -->
            <div class="mt-6 pt-4 border-t border-calm-100 flex items-center justify-center gap-2 text-[11px] text-slate-400 font-medium">
                <span>🔒 Tus datos están aislados y protegidos</span>
            </div>

        </div>
    </main>

    <!-- Pie Mínimo -->
    <footer class="py-6 text-center text-xs text-slate-400 font-medium">
        © 2026 EduPlan Perú &bull; Soporte al docente y directivo peruano
    </footer>

    <!-- Script de Cambio de Pestañas -->
    <script>
        function cambiarTab(modo) {
            const tabLogin = document.getElementById('tab-login');
            const tabRegistro = document.getElementById('tab-registro');
            const formLogin = document.getElementById('form-login');
            const formRegistro = document.getElementById('form-registro');
            const googleText = document.getElementById('google-btn-text');

            if (modo === 'login') {
                tabLogin.className = "flex-1 py-2.5 rounded-xl bg-white text-calm-800 shadow-sm transition";
                tabRegistro.className = "flex-1 py-2.5 rounded-xl text-slate-500 hover:text-calm-800 transition";
                formLogin.classList.remove('hidden');
                formRegistro.classList.add('hidden');
                googleText.innerText = "Continuar con Google";
            } else {
                tabRegistro.className = "flex-1 py-2.5 rounded-xl bg-white text-calm-800 shadow-sm transition";
                tabLogin.className = "flex-1 py-2.5 rounded-xl text-slate-500 hover:text-calm-800 transition";
                formRegistro.classList.remove('hidden');
                formLogin.classList.add('hidden');
                googleText.innerText = "Registrarme con Google";
            }
        }
    </script>

</body>
</html>
```

## File: app/templates/base.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EduPlan Perú - Sistema Pedagógico</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
  
  <!-- HTMX -->
  <script src="https://unpkg.com/htmx.org@1.9.11"></script>
  
  <!-- Markdown Parser -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  
  <!-- KaTeX (Renderizado Matemático Profesional) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  
  <!-- Exportadores de Word y PDF -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/html-docx-js/dist/html-docx.js"></script>

  <style>
    /* Estilos globales y HTMX Indicator */
    body { background-color: #fafaf9; color: #292524; }
    .htmx-indicator { display: none; }
    .htmx-request .htmx-indicator { display: flex; }
    .htmx-request.htmx-indicator { display: flex; }
    
    /* Evitar saltos de layout durante requests HTMX */
    [hx-swap-oob="true"] { display: none !important; }
  </style>
</head>
<body class="bg-slate-100 font-sans text-slate-900 antialiased overflow-hidden">
  {% block content %}{% endblock %}
</body>
</html>
```

## File: app/templates/landing.html
```html
<!DOCTYPE html>
<html lang="es" class="scroll-smooth">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduPlan Perú | Asistente Pedagógico y Directivo CNEB</title>
    <meta name="description"
        content="Plataforma de inteligencia artificial para docentes y directivos del Perú. Genera sesiones de aprendizaje, rúbricas e instrumentos de gestión escolar bajo la normativa MINEDU.">
    <meta name="keywords"
        content="sesiones de aprendizaje, CNEB, RVM 094-2020, MINEDU, planificaciones escolares, rubricas de evaluacion, gestion directiva">
    <link rel="canonical" href="https://eduplanperu.pe/">

    <meta property="og:title" content="EduPlan Perú | Planificación Escolar y Gestión Directiva">
    <meta property="og:description"
        content="Ahorra horas de trabajo administrativo y genera documentos pedagógicos oficiales en segundos.">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="es_PE">

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap"
        rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Nunito', 'sans-serif'] },
                    colors: {
                        calm: {
                            50: '#fafaf9',
                            100: '#f5f5f4',
                            200: '#e7e5e4',
                            800: '#292524',
                            900: '#1c1917',
                        },
                        zen: {
                            50: '#f0fdfa',
                            100: '#ccfbf1',
                            200: '#99f6e4',
                            600: '#0d9488',
                            700: '#0f766e',
                            800: '#115e59',
                            900: '#134e4a',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #fafaf9;
            color: #292524;
        }
    </style>
</head>

<body class="antialiased flex flex-col min-h-screen selection:bg-zen-600 selection:text-white">

    <!-- HEADER -->
    {% include "landing/header.html" %}

    <!-- HERO SECTION LIMPIO, MODERNO Y SIN DUPLICIDAD -->
    <section
        class="relative pt-16 pb-20 overflow-hidden bg-gradient-to-b from-teal-50/40 via-white to-calm-50 border-b border-calm-200">

        <!-- Glow radial de fondo -->
        <div
            class="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[480px] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-teal-200/35 via-zen-100/15 to-transparent pointer-events-none -z-10">
        </div>
        <div
            class="absolute inset-0 bg-[linear-gradient(to_right,#e7e5e4_1px,transparent_1px),linear-gradient(to_bottom,#e7e5e4_1px,transparent_1px)] bg-[size:3.5rem_3.5rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-30 pointer-events-none -z-10">
        </div>

        <div class="max-w-5xl mx-auto px-6 relative z-10 text-center">

            <!-- Badge Normativo Oficial -->
            <div
                class="inline-flex items-center gap-2 rounded-full bg-white border border-zen-200 px-4 py-1.5 text-xs font-extrabold text-zen-800 shadow-sm mb-6">
                <span class="flex h-2 w-2 rounded-full bg-zen-600 animate-pulse"></span>
                Normativa Oficial CNEB 2026 &bull; RVM N° 094-2020
            </div>

            <!-- Título Principal -->
            <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight text-calm-900 leading-[1.1] mb-6">
                Menos carga administrativa.<br>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-zen-700 via-teal-600 to-zen-800">Más
                    tiempo para educar.</span>
            </h1>

            <!-- Bajada -->
            <p class="text-base sm:text-lg text-slate-600 mb-8 max-w-2xl mx-auto font-medium leading-relaxed">
                Genera sesiones de aprendizaje completas, rúbricas formativas y documentos oficiales de UGEL en
                segundos. Diseñado para la estructura curricular peruana.
            </p>

            <!-- Botones de Acción -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
                <a href="/auth"
                    class="w-full sm:w-auto rounded-2xl bg-zen-700 px-8 py-4 text-sm font-extrabold text-white shadow-xl shadow-zen-700/25 hover:bg-zen-800 hover:-translate-y-0.5 transition-all">
                    Probar Asistente Gratis
                </a>
                <a href="#planes"
                    class="w-full sm:w-auto rounded-2xl bg-white border border-calm-200 px-8 py-4 text-sm font-bold text-calm-800 shadow-sm hover:border-zen-600 hover:text-zen-700 transition">
                    Ver Planes y Tarifas
                </a>
            </div>

            <!-- Previsualización Real del Espacio de Trabajo (Un solo elemento visual protagónico) -->
            <div
                class="relative mx-auto max-w-3xl rounded-3xl border border-calm-200 bg-white p-2.5 shadow-2xl shadow-zen-900/10 text-left">
                <div class="rounded-2xl border border-calm-100 bg-calm-50 overflow-hidden">

                    <!-- Barra de la ventana simulada -->
                    <div class="flex items-center justify-between px-4 py-3 bg-white border-b border-calm-200 text-xs">
                        <div class="flex items-center gap-2">
                            <span class="h-3 w-3 rounded-full bg-rose-400"></span>
                            <span class="h-3 w-3 rounded-full bg-amber-400"></span>
                            <span class="h-3 w-3 rounded-full bg-emerald-400"></span>
                            <span class="text-slate-400 font-bold ml-2 text-[11px] hidden sm:inline">EduPlan Workspace
                                &bull; Vista Previa</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span
                                class="text-[10px] font-bold text-slate-500 bg-calm-100 border border-calm-200 px-2 py-0.5 rounded-md">Contexto:
                                Comunicación 1° Sec.</span>
                            <span
                                class="text-[10px] font-extrabold text-zen-700 bg-zen-50 border border-zen-200 px-2.5 py-0.5 rounded-md">.DOCX</span>
                        </div>
                    </div>

                    <!-- Mensaje simulado IA -->
                    <div class="p-5 sm:p-6 bg-white space-y-3">
                        <div class="flex items-start gap-3">
                            <div
                                class="h-7 w-7 rounded-lg bg-zen-700 text-white flex items-center justify-center font-bold text-xs shrink-0">
                                EP</div>
                            <div class="space-y-2 flex-1">
                                <p class="text-xs font-bold text-slate-800">Sesión Generada: "Elaboramos un texto
                                    argumentativo sobre el cuidado del agua en nuestra comunidad"</p>

                                <div
                                    class="grid grid-cols-1 sm:grid-cols-3 gap-2 bg-calm-50 border border-calm-200 p-2.5 rounded-xl text-[11px]">
                                    <div>
                                        <span class="font-extrabold text-slate-700 block">Competencia:</span>
                                        <span class="text-slate-500">Escribe diversos tipos de textos en su lengua
                                            materna.</span>
                                    </div>
                                    <div>
                                        <span class="font-extrabold text-slate-700 block">Instrumento:</span>
                                        <span class="text-slate-500">Rúbrica analítica (Escala AD, A, B, C).</span>
                                    </div>
                                    <div>
                                        <span class="font-extrabold text-slate-700 block">Enfoque:</span>
                                        <span class="text-slate-500">Ambiental y DUA (múltiples formas de
                                            acción).</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- Cinta sutil de compatibilidad normativa (una sola línea limpia) -->
            <div
                class="mt-8 flex flex-wrap items-center justify-center gap-6 text-xs font-bold text-slate-400 uppercase tracking-wider">
                <span>✓ RVM N° 094-2020</span>
                <span>•</span>
                <span>✓ Formato Tabular UGEL</span>
                <span>•</span>
                <span>✓ Diseño Universal DUA</span>
                <span>•</span>
                <span>✓ Rúbricas de Desempeño</span>
            </div>

        </div>
    </section>

    <!-- CARDS DE BENEFICIOS -->
    {% include "landing/components/beneficios.html" %}

    <!-- TABLA DE PLANES -->
    {% include "landing/components/planes.html" %}

    <!-- PREGUNTAS FRECUENTES -->
    {% include "landing/components/faq.html" %}

    <!-- FOOTER -->
    {% include "landing/footer.html" %}

</body>

</html>
```

## File: app/templates/landing/components/planes.html
```html
<section id="planes" class="py-20 bg-calm-50 border-t border-calm-200">
    <div class="max-w-6xl mx-auto px-6">
        <div class="text-center mb-14">
            <span class="inline-block rounded-full bg-zen-50 border border-zen-200 px-3.5 py-1 text-xs font-bold text-zen-700 uppercase tracking-wider mb-3">
                Tarifas Accesibles 2026
            </span>
            <h2 class="text-3xl md:text-4xl font-extrabold text-calm-800 mb-3">Planes Adaptados a tu Labor Oficial</h2>
            <p class="text-slate-500 text-base max-w-2xl mx-auto font-medium">Alineado al Currículo Nacional (CNEB) y a los requerimientos de supervisión de UGEL y DRE.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
            
            <!-- PLAN 1: DOCENTE -->
            <div class="flex flex-col justify-between rounded-3xl border border-calm-200 bg-white p-6 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div>
                    <div class="h-11 w-11 rounded-2xl bg-blue-50 text-blue-700 flex items-center justify-center text-xl mb-4">📚</div>
                    <h3 class="text-xl font-bold text-calm-800">Docente de Aula</h3>
                    <p class="text-slate-500 text-xs mt-1 mb-4 h-8 leading-relaxed">Planificación curricular y evaluación formativa diaria.</p>
                    <div class="mb-5">
                        <span class="text-3xl font-extrabold text-calm-800">S/ 25</span>
                        <span class="text-slate-400 text-xs font-medium">/mes</span>
                    </div>

                    <ul class="space-y-2.5 text-xs font-medium text-slate-600 mb-6">
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Sesiones según CNEB y RVM 094</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Rúbricas formativas (AD, A, B, C)</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Situaciones significativas reales</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Descarga inmediata en Word y PDF</li>
                    </ul>
                </div>

                <div class="pt-4 border-t border-calm-100 flex flex-col gap-3">
                    <button type="button" onclick="abrirModalPlan('modal-docente')" class="text-xs font-bold text-zen-700 hover:text-zen-800 flex items-center justify-center gap-1.5 py-1">
                        <span>Ver cobertura pedagógica</span>
                        <span class="text-[11px]">→</span>
                    </button>
                    <a href="/auth" class="block w-full text-center rounded-xl bg-calm-100 hover:bg-calm-200 border border-calm-200 py-2.5 text-xs font-bold text-calm-800 hover:text-zen-700 transition">
                        Elegir este plan
                    </a>
                </div>
            </div>

            <!-- PLAN 2: DIRECTIVO -->
            <div class="flex flex-col justify-between rounded-3xl border border-calm-200 bg-white p-6 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div>
                    <div class="h-11 w-11 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center text-xl mb-4">🏢</div>
                    <h3 class="text-xl font-bold text-calm-800">Directivo / Jerárquico</h3>
                    <p class="text-slate-500 text-xs mt-1 mb-4 h-8 leading-relaxed">Gestión escolar, supervisión pedagógica y UGEL.</p>
                    <div class="mb-5">
                        <span class="text-3xl font-extrabold text-calm-800">S/ 30</span>
                        <span class="text-slate-400 text-xs font-medium">/mes</span>
                    </div>

                    <ul class="space-y-2.5 text-xs font-medium text-slate-600 mb-6">
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Fichas de Monitoreo MINEDU</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Resoluciones Directorales (RD)</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Oficios formales, informes y actas</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Asistencia en PEI, PAT, PCI y RI</li>
                    </ul>
                </div>

                <div class="pt-4 border-t border-calm-100 flex flex-col gap-3">
                    <button type="button" onclick="abrirModalPlan('modal-directivo')" class="text-xs font-bold text-zen-700 hover:text-zen-800 flex items-center justify-center gap-1.5 py-1">
                        <span>Ver cobertura de gestión</span>
                        <span class="text-[11px]">→</span>
                    </button>
                    <a href="/auth" class="block w-full text-center rounded-xl bg-calm-100 hover:bg-calm-200 border border-calm-200 py-2.5 text-xs font-bold text-calm-800 hover:text-zen-700 transition">
                        Elegir este plan
                    </a>
                </div>
            </div>

            <!-- PLAN 3: DOBLE ROL -->
            <div class="flex flex-col justify-between rounded-3xl border-2 border-zen-700 bg-white p-6 shadow-xl relative hover:-translate-y-1 transition-all duration-300">
                <div class="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-zen-700 text-white px-3.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider shadow">
                    Recomendado
                </div>
                <div>
                    <div class="h-11 w-11 rounded-2xl bg-zen-100 text-zen-800 flex items-center justify-center text-xl mb-4">⭐</div>
                    <h3 class="text-xl font-bold text-calm-800">Doble Rol</h3>
                    <p class="text-slate-500 text-xs mt-1 mb-4 h-8 leading-relaxed">Coordinadores pedagógicos o directivos con aula.</p>
                    <div class="mb-5">
                        <span class="text-3xl font-extrabold text-zen-800">S/ 35</span>
                        <span class="text-slate-400 text-xs font-medium">/mes</span>
                    </div>

                    <ul class="space-y-2.5 text-xs font-medium text-slate-600 mb-6">
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Suite Docente + Directiva completa</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Alternancia de rol en 1 clic</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Carteles de alcance y secuencias</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Historial dual segmentado por rol</li>
                    </ul>
                </div>

                <div class="pt-4 border-t border-zen-100 flex flex-col gap-3">
                    <button type="button" onclick="abrirModalPlan('modal-doble')" class="text-xs font-bold text-zen-700 hover:text-zen-800 flex items-center justify-center gap-1.5 py-1">
                        <span>Ver alcance integral</span>
                        <span class="text-[11px]">→</span>
                    </button>
                    <a href="/auth" class="block w-full text-center rounded-xl bg-zen-700 hover:bg-zen-800 py-2.5 text-xs font-bold text-white transition shadow-md shadow-zen-700/20">
                        Elegir este plan
                    </a>
                </div>
            </div>

            <!-- PLAN 4: INSTITUCIONAL -->
            <div class="flex flex-col justify-between rounded-3xl border border-calm-200 bg-white p-6 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div>
                    <div class="h-11 w-11 rounded-2xl bg-amber-50 text-amber-700 flex items-center justify-center text-xl mb-4">🤝</div>
                    <h3 class="text-xl font-bold text-calm-800">Institucional</h3>
                    <p class="text-slate-500 text-xs mt-1 mb-4 h-8 leading-relaxed">Colegios por convenio o privadas completas.</p>
                    <div class="mb-5">
                        <span class="text-2xl font-extrabold text-calm-800">A medida</span>
                        <span class="text-slate-400 text-xs block font-medium">Por plana docente</span>
                    </div>

                    <ul class="space-y-2.5 text-xs font-medium text-slate-600 mb-6">
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Cuentas independientes para toda la I.E.</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Panel de supervisión y avance</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Membrete, escudo y PEI unificado</li>
                        <li class="flex items-center gap-2"><span class="text-zen-700 font-bold">✓</span> Taller de capacitación oficial</li>
                    </ul>
                </div>

                <div class="pt-4 border-t border-calm-100 flex flex-col gap-3">
                    <button type="button" onclick="abrirModalPlan('modal-institucional')" class="text-xs font-bold text-zen-700 hover:text-zen-800 flex items-center justify-center gap-1.5 py-1">
                        <span>Ver beneficios institucionales</span>
                        <span class="text-[11px]">→</span>
                    </button>
                    <a href="https://wa.me/51922498580?text=Hola,%20solicito%20cotización%20del%20Plan%20Institucional%20para%20mi%20colegio" target="_blank" class="block w-full text-center rounded-xl bg-calm-100 hover:bg-calm-200 border border-calm-200 py-2.5 text-xs font-bold text-calm-800 hover:text-zen-700 transition">
                        Coordinar por WhatsApp
                    </a>
                </div>
            </div>

        </div>
    </div>
</section>

<!-- ========================================== -->
<!-- MODALES DETALLADOS CON INFORMACIÓN AMPLIA -->
<!-- ========================================== -->

<!-- Modal 1: Docente de Aula -->
<div id="modal-docente" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white border border-calm-200 w-full max-w-2xl rounded-3xl shadow-2xl p-6 sm:p-8 overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between pb-4 border-b border-calm-100 mb-6">
            <div class="flex items-center gap-3">
                <span class="text-2xl p-2 bg-blue-50 text-blue-700 rounded-2xl">📚</span>
                <div>
                    <h3 class="text-xl font-black text-calm-800">Plan Docente de Aula</h3>
                    <p class="text-xs text-slate-500">Diseñado para simplificar el 100% de la carga pedagógica de clase</p>
                </div>
            </div>
            <button onclick="cerrarModalPlan('modal-docente')" class="text-slate-400 hover:text-slate-600 text-lg p-2">✕</button>
        </div>

        <div class="space-y-4 text-xs text-slate-600 leading-relaxed">
            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>🎯</span> Secuencias Didácticas Completas (90 y 135 min)
                </h4>
                <p>Genera sesiones articuladas con los procesos pedagógicos obligatorios (problematización, propósito, motivación, saberes previos, gestión y acompañamiento, y evaluación) junto a los procesos didácticos propios de cada especialidad.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>📊</span> Matriz de Evaluación Formativa y RVM N° 094-2020
                </h4>
                <p>Formulación coherente y no mecánica de competencias, capacidades, estándares de aprendizaje y desempeños precisados. Incluye criterios de evaluación redactados con el mismo verbo rector y descriptores en escala cualitativa (AD, A, B y C).</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>♿</span> Adaptaciones Curriculares y DUA
                </h4>
                <p>Articulación explícita con el Diseño Universal para el Aprendizaje: múltiples formas de motivación, representación de la información y expresión para aulas diversas y atención a Necesidades Educativas Especiales (NEE).</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>📄</span> Exportación Directa a Word (.docx)
                </h4>
                <p>Olvídate del copiar y pegar desordenado. Descarga tus sesiones listas con tablas cuadradas oficiales, membrete institucional configurado y márgenes listos para archivar en tu carpeta pedagógica.</p>
            </div>
        </div>

        <div class="mt-8 pt-4 border-t border-calm-100 flex justify-end gap-3">
            <button onclick="cerrarModalPlan('modal-docente')" class="px-5 py-2.5 rounded-xl border border-calm-200 text-xs font-bold text-slate-600 hover:bg-calm-100">Cerrar</button>
            <a href="/auth" class="px-6 py-2.5 rounded-xl bg-zen-700 text-xs font-bold text-white hover:bg-zen-800 shadow">Elegir este plan</a>
        </div>
    </div>
</div>

<!-- Modal 2: Directivo / Jerárquico -->
<div id="modal-directivo" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white border border-calm-200 w-full max-w-2xl rounded-3xl shadow-2xl p-6 sm:p-8 overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between pb-4 border-b border-calm-100 mb-6">
            <div class="flex items-center gap-3">
                <span class="text-2xl p-2 bg-emerald-50 text-emerald-700 rounded-2xl">🏢</span>
                <div>
                    <h3 class="text-xl font-black text-calm-800">Plan Directivo y Jerárquico</h3>
                    <p class="text-xs text-slate-500">Liderazgo pedagógico, normativo y supervisión escolar</p>
                </div>
            </div>
            <button onclick="cerrarModalPlan('modal-directivo')" class="text-slate-400 hover:text-slate-600 text-lg p-2">✕</button>
        </div>

        <div class="space-y-4 text-xs text-slate-600 leading-relaxed">
            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>📋</span> Fichas de Monitoreo con Rúbricas MINEDU
                </h4>
                <p>Instrumentos estandarizados basados en las 5 rúbricas de desempeño docente (Involucramiento activo, Razonamiento y creatividad, Evaluación formativa y retroalimentación, Clima de respeto y Regulación de conducta).</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>⚖️</span> Resoluciones Directorales (RD) Normativas
                </h4>
                <p>Redacción jurídica y administrativa precisa para conformación de Comités de Gestión Escolar 2026 (Condiciones Operativas, Pedagógicas y Bienestar), comisiones de inventario, plan de lector institucional y planes de contingencia.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>📁</span> Instrumentos de Gestión Escolar (PEI, PAT, PCI, RI)
                </h4>
                <p>Estructuración y revisión de diagnósticos situacionales, metas de aprendizaje y formulación de actividades de gestión para cumplimiento de compromisos directivos ante la UGEL.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>✉️</span> Oficios Formales, Descargos e Informes Técnicos
                </h4>
                <p>Respuestas técnicas para especialistas de UGEL y DRE con terminología formal del aparato estatal educativo peruano.</p>
            </div>
        </div>

        <div class="mt-8 pt-4 border-t border-calm-100 flex justify-end gap-3">
            <button onclick="cerrarModalPlan('modal-directivo')" class="px-5 py-2.5 rounded-xl border border-calm-200 text-xs font-bold text-slate-600 hover:bg-calm-100">Cerrar</button>
            <a href="/auth" class="px-6 py-2.5 rounded-xl bg-zen-700 text-xs font-bold text-white hover:bg-zen-800 shadow">Elegir este plan</a>
        </div>
    </div>
</div>

<!-- Modal 3: Doble Rol -->
<div id="modal-doble" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white border border-calm-200 w-full max-w-2xl rounded-3xl shadow-2xl p-6 sm:p-8 overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between pb-4 border-b border-calm-100 mb-6">
            <div class="flex items-center gap-3">
                <span class="text-2xl p-2 bg-zen-50 text-zen-800 rounded-2xl">⭐</span>
                <div>
                    <h3 class="text-xl font-black text-calm-800">Plan Doble Rol (Docente + Directivo)</h3>
                    <p class="text-xs text-slate-500">La solución híbrida para coordinadores pedagógicos y directores con horas de aula</p>
                </div>
            </div>
            <button onclick="cerrarModalPlan('modal-doble')" class="text-slate-400 hover:text-slate-600 text-lg p-2">✕</button>
        </div>

        <div class="space-y-4 text-xs text-slate-600 leading-relaxed">
            <div class="p-4 bg-zen-50/50 rounded-2xl border border-zen-100">
                <h4 class="font-extrabold text-zen-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>🔄</span> Conmutador de Rol en 1 Clic
                </h4>
                <p>Cambia instantáneamente en tu barra de trabajo entre planificar tus clases de aula o generar oficios y monitoreos de coordinación sin tener que salir ni abrir cuentas separadas.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>📈</span> Carteles de Alcance y Secuencia Curricular
                </h4>
                <p>Diseña la progresión de competencias por ciclo escolar para coordinar con los profesores de tu área y asegurar la coherencia en las evaluaciones diagnósticas y planes de refuerzo escolar.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>🗂️</span> Historial Dual Inteligente
                </h4>
                <p>Tu biblioteca de documentos mantiene organizadas tus sesiones de clase por grado y sección separadas de los informes de gestión y actas de coordinación.</p>
            </div>
        </div>

        <div class="mt-8 pt-4 border-t border-calm-100 flex justify-end gap-3">
            <button onclick="cerrarModalPlan('modal-doble')" class="px-5 py-2.5 rounded-xl border border-calm-200 text-xs font-bold text-slate-600 hover:bg-calm-100">Cerrar</button>
            <a href="/auth" class="px-6 py-2.5 rounded-xl bg-zen-700 text-xs font-bold text-white hover:bg-zen-800 shadow">Elegir este plan</a>
        </div>
    </div>
</div>

<!-- Modal 4: Institucional -->
<div id="modal-institucional" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white border border-calm-200 w-full max-w-2xl rounded-3xl shadow-2xl p-6 sm:p-8 overflow-y-auto max-h-[90vh]">
        <div class="flex items-center justify-between pb-4 border-b border-calm-100 mb-6">
            <div class="flex items-center gap-3">
                <span class="text-2xl p-2 bg-amber-50 text-amber-800 rounded-2xl">🤝</span>
                <div>
                    <h3 class="text-xl font-black text-calm-800">Plan Institucional para Colegios</h3>
                    <p class="text-xs text-slate-500">Estandarización pedagógica e identidad institucional para toda la plana docente</p>
                </div>
            </div>
            <button onclick="cerrarModalPlan('modal-institucional')" class="text-slate-400 hover:text-slate-600 text-lg p-2">✕</button>
        </div>

        <div class="space-y-4 text-xs text-slate-600 leading-relaxed">
            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>🏛️</span> Personalización con el Sello de tu Institución Educativa
                </h4>
                <p>Entrenamos el contexto institucional con tu PEI (Misión, Visión, Valores institucionales, Lema y Enfoques transversales priorizados). Toda la plana docente generará documentos alineados a la misma identidad.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>📊</span> Panel de Supervisión y Auditoría Directiva
                </h4>
                <p>La dirección escolar puede monitorear el avance de las programaciones curriculares por nivel, grado y área en tiempo real, garantizando la entrega oportuna para supervisiones de UGEL.</p>
            </div>

            <div class="p-4 bg-calm-50 rounded-2xl border border-calm-200">
                <h4 class="font-extrabold text-slate-800 text-sm mb-1.5 flex items-center gap-2">
                    <span>🎓</span> Taller de Inducción Docente y Acompañamiento
                </h4>
                <p>Sesión sincrónica de capacitación pedagógica para todo el cuerpo docente y directivo, garantizando un aprovechamiento óptimo desde el primer día de clase.</p>
            </div>
        </div>

        <div class="mt-8 pt-4 border-t border-calm-100 flex justify-end gap-3">
            <button onclick="cerrarModalPlan('modal-institucional')" class="px-5 py-2.5 rounded-xl border border-calm-200 text-xs font-bold text-slate-600 hover:bg-calm-100">Cerrar</button>
            <a href="https://wa.me/51922498580?text=Hola,%20solicito%20cotización%20del%20Plan%20Institucional%20para%20mi%20colegio" target="_blank" class="px-6 py-2.5 rounded-xl bg-zen-700 text-xs font-bold text-white hover:bg-zen-800 shadow">Coordinar por WhatsApp</a>
        </div>
    </div>
</div>

<script>
    function abrirModalPlan(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            document.body.style.overflow = 'hidden';
        }
    }

    function cerrarModalPlan(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            document.body.style.overflow = 'auto';
        }
    }

    // Cerrar al hacer clic fuera del contenido
    window.addEventListener('click', function(e) {
        const modales = ['modal-docente', 'modal-directivo', 'modal-doble', 'modal-institucional'];
        modales.forEach(id => {
            const m = document.getElementById(id);
            if (m && e.target === m) {
                cerrarModalPlan(id);
            }
        });
    });
</script>
```

## File: app/templates/onboarding.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuración Curricular | EduPlan Perú</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Nunito', 'sans-serif'] },
                    colors: {
                        calm: { 50: '#fafaf9', 100: '#f5f5f4', 200: '#e7e5e4', 800: '#292524' },
                        zen: { 50: '#f0fdfa', 100: '#ccfbf1', 600: '#0d9488', 700: '#0f766e', 800: '#115e59' }
                    }
                }
            }
        }
    </script>
</head>
<body class="min-h-screen bg-calm-50 text-calm-800 flex items-center justify-center p-4 sm:p-8">

    <div class="max-w-4xl w-full bg-white border border-calm-200 rounded-3xl shadow-xl p-6 sm:p-10">
        
        <div class="flex items-center justify-between mb-8 pb-4 border-b border-calm-200 text-xs font-bold" id="progress-bar">
            <div id="badge-1" class="flex items-center gap-2 text-zen-700">
                <span class="h-6 w-6 rounded-full bg-zen-700 text-white flex items-center justify-center text-[11px]">1</span>
                <span>Perfil de Trabajo</span>
            </div>
            <div class="h-0.5 flex-1 mx-4 bg-calm-200"></div>
            <div id="badge-2" class="flex items-center gap-2 text-slate-400">
                <span class="h-6 w-6 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center text-[11px]">2</span>
                <span>Instituciones y Carga Académica</span>
            </div>
        </div>

        <form action="/completar-onboarding" method="POST" enctype="multipart/form-data" id="onboarding-form">
            
            <!-- PASO 1 -->
            <div id="paso-1" class="space-y-6">
                <div>
                    <h2 class="text-xl font-black text-slate-800">¡Bienvenido a tu espacio docente!</h2>
                    <p class="text-sm text-slate-500 mt-1">Configura tu carga de trabajo para personalizar los membretes y formatos de tus sesiones.</p>
                </div>

                <div class="bg-calm-50 p-5 rounded-2xl border border-calm-200">
                    <label class="block text-sm font-bold text-slate-700 mb-3">¿En cuántas instituciones educativas trabajas este año?</label>
                    <select id="num-colegios" name="num_colegios" class="w-full sm:w-1/2 text-sm rounded-xl border border-calm-200 p-3 bg-white outline-none focus:border-zen-700 transition">
                        <option value="1">1 Institución</option>
                        <option value="2">2 Instituciones</option>
                        <option value="3">3 Instituciones</option>
                    </select>
                </div>

                <div class="flex items-center gap-3 p-4 border border-calm-200 rounded-2xl cursor-pointer hover:bg-calm-50 transition" onclick="document.getElementById('check-independiente').click()">
                    <input type="checkbox" id="check-independiente" name="es_independiente" class="w-5 h-5 text-zen-600 rounded cursor-pointer">
                    <div>
                        <span class="block text-sm font-bold text-slate-700">Habilitar "Espacio Personal / Tutorías"</span>
                        <span class="block text-xs text-slate-500">Permite planificar sin estar atado a una institución formal específica.</span>
                    </div>
                </div>

                <div class="flex justify-end pt-4">
                    <button type="button" onclick="generarColegiosYAvanzar()" class="px-6 py-3 rounded-2xl bg-zen-700 text-white font-bold text-sm hover:bg-zen-800 transition shadow-md shadow-zen-700/20">
                        Siguiente Paso →
                    </button>
                </div>
            </div>

            <!-- PASO 2 -->
            <div id="paso-2" class="space-y-6 hidden">
                <div>
                    <h2 class="text-xl font-black text-slate-800">Configura tus Instituciones y Aulas</h2>
                    <p class="text-sm text-slate-500 mt-1">Selecciona los grados y las secciones que tienes a cargo en cada colegio.</p>
                </div>

                <div id="contenedor-colegios" class="space-y-8"></div>

                <div class="flex justify-between pt-4 border-t border-calm-200">
                    <button type="button" onclick="volverPaso1()" class="px-6 py-3 rounded-2xl border border-calm-200 text-slate-600 font-bold text-sm hover:bg-calm-100 transition">
                        ← Atrás
                    </button>
                    <button type="submit" class="px-6 py-3 rounded-2xl bg-zen-700 text-white font-bold text-sm hover:bg-zen-800 transition shadow-md shadow-zen-700/20">
                        Finalizar e Ingresar →
                    </button>
                </div>
            </div>

        </form>
    </div>

    <script>
        let contadorBloques = 0; 
        const areasCNEB = [
            "Matemática", "Comunicación", "Ciencia y Tecnología", "Personal Social / CC.SS.", 
            "DPCC", "Educación Física", "Arte y Cultura", "Inglés", "Educación Religiosa", 
            "Educación para el Trabajo (EPT)", "Tutoría", "Computación / Informática"
        ];
        const seccionesLetras = ["A", "B", "C", "D", "E", "F", "G"];

        function generarColegiosYAvanzar() {
            const num = parseInt(document.getElementById('num-colegios').value);
            const contenedor = document.getElementById('contenedor-colegios');
            contenedor.innerHTML = ''; 
            contadorBloques = 0;

            for (let i = 1; i <= num; i++) {
                contenedor.innerHTML += `
                <div class="bg-calm-50 p-5 sm:p-6 rounded-2xl border border-calm-200 shadow-sm relative">
                    <div class="absolute -top-3 left-6 bg-zen-700 text-white text-[10px] font-black uppercase px-3 py-1 rounded-full">
                        Institución ${i}
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-2">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Nombre de la I.E.</label>
                            <input type="text" name="colegio_${i}_nombre" required placeholder="Ej: I.E. San Miguel" class="w-full text-sm rounded-xl border border-calm-200 p-2.5 outline-none focus:border-zen-700 bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">UGEL</label>
                            <input type="text" name="colegio_${i}_ugel" required placeholder="Ej: UGEL Piura" class="w-full text-sm rounded-xl border border-calm-200 p-2.5 outline-none focus:border-zen-700 bg-white">
                        </div>
                        <div class="sm:col-span-2">
                            <label class="block text-xs font-bold text-slate-700 mb-1">Logo del Colegio (Opcional)</label>
                            <input type="file" name="colegio_${i}_logo" accept="image/png, image/jpeg, image/webp" class="w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-zen-100 file:text-zen-700 hover:file:bg-zen-200 transition">
                        </div>
                    </div>

                    <div class="mt-6 border-t border-calm-200 pt-4">
                        <label class="block text-sm font-bold text-slate-700 mb-3">Carga Académica</label>
                        <div id="cargas_colegio_${i}" class="space-y-4"></div>
                        <button type="button" onclick="agregarBloqueAsignacion(${i})" class="w-full mt-3 py-3 border-2 border-dashed border-calm-200 rounded-xl text-xs font-bold text-slate-500 hover:border-zen-400 hover:text-zen-700 hover:bg-zen-50 transition">
                            + Añadir un Curso a esta Institución
                        </button>
                    </div>
                </div>
                `;
                agregarBloqueAsignacion(i);
            }

            document.getElementById('paso-1').classList.add('hidden');
            document.getElementById('paso-2').classList.remove('hidden');
            document.getElementById('badge-1').className = "flex items-center gap-2 text-slate-400";
            document.getElementById('badge-1').children[0].className = "h-6 w-6 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center text-[11px]";
            document.getElementById('badge-2').className = "flex items-center gap-2 text-zen-700";
            document.getElementById('badge-2').children[0].className = "h-6 w-6 rounded-full bg-zen-700 text-white flex items-center justify-center text-[11px]";
        }

        function agregarBloqueAsignacion(idColegio) {
            contadorBloques++;
            const bId = contadorBloques;
            const contenedor = document.getElementById(`cargas_colegio_${idColegio}`);
            
            let optionsHTML = areasCNEB.map(area => `<option value="${area}">${area}</option>`).join('');
            optionsHTML += `<option value="Otro">Otro (Especificar)</option>`;

            const div = document.createElement('div');
            div.className = "bg-white p-4 rounded-xl border border-calm-200 shadow-sm relative";
            div.innerHTML = `
                <button type="button" onclick="this.parentElement.remove()" class="absolute top-3 right-3 text-slate-400 hover:text-red-500 transition" title="Quitar curso">✕</button>
                <input type="hidden" name="colegio_${idColegio}_bloques[]" value="${bId}">

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                    <div>
                        <label class="text-[11px] font-bold text-slate-500 block mb-1">Nivel Educativo</label>
                        <select name="col_${idColegio}_b${bId}_nivel" onchange="actualizarGrados(this, ${bId})" class="w-full text-xs rounded-lg border border-calm-200 p-2.5 outline-none bg-calm-50 focus:border-zen-600">
                            <option value="Secundaria" selected>Secundaria</option>
                            <option value="Primaria">Primaria</option>
                            <option value="Inicial">Inicial</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-[11px] font-bold text-slate-500 block mb-1">Área / Curso</label>
                        <div class="flex flex-col gap-2">
                            <select name="col_${idColegio}_b${bId}_area" onchange="verificarOtro(this, ${idColegio}, ${bId})" class="w-full text-xs rounded-lg border border-calm-200 p-2.5 outline-none bg-calm-50 focus:border-zen-600">
                                ${optionsHTML}
                            </select>
                            <input type="text" id="otro_${idColegio}_${bId}" name="col_${idColegio}_b${bId}_area_otro" placeholder="Escribe el nombre del curso..." class="hidden w-full text-xs rounded-lg border border-calm-200 p-2.5 outline-none focus:border-zen-600">
                        </div>
                    </div>
                </div>

                <div>
                    <label class="text-[11px] font-bold text-slate-500 block mb-2">Selecciona los grados y secciones a cargo:</label>
                    <div id="grados_b${bId}" class="flex flex-col gap-2.5"></div>
                </div>
            `;
            contenedor.appendChild(div);
            
            const selectNivel = div.querySelector(`select[name="col_${idColegio}_b${bId}_nivel"]`);
            actualizarGrados(selectNivel, bId);
        }

        function verificarOtro(selectElement, idColegio, bId) {
            const inputOtro = document.getElementById(`otro_${idColegio}_${bId}`);
            if (selectElement.value === "Otro") {
                inputOtro.classList.remove("hidden");
                inputOtro.required = true;
            } else {
                inputOtro.classList.add("hidden");
                inputOtro.required = false;
                inputOtro.value = "";
            }
        }

        function actualizarGrados(selectElement, bId) {
            const nivel = selectElement.value;
            const contenedorGrados = document.getElementById(`grados_b${bId}`);
            const colId = selectElement.name.split('_')[1]; 

            let grados = [];
            if (nivel === 'Inicial') grados = ["3 Años", "4 Años", "5 Años"];
            else if (nivel === 'Primaria') grados = ["1°", "2°", "3°", "4°", "5°", "6°"];
            else grados = ["1°", "2°", "3°", "4°", "5°"];

            contenedorGrados.innerHTML = grados.map((g, index) => `
                <div class="border border-calm-200 rounded-xl overflow-hidden bg-calm-50">
                    <label class="flex items-center gap-2 p-2.5 bg-white cursor-pointer hover:bg-calm-50 transition border-b border-calm-100">
                        <input type="checkbox" name="col_${colId}_b${bId}_grados[]" value="${g}" onchange="toggleSecciones(this, 'secc_${colId}_${bId}_${index}')" class="accent-zen-600 w-4 h-4 rounded"> 
                        <span class="text-xs font-black text-slate-700">${g}</span>
                    </label>
                    <div id="secc_${colId}_${bId}_${index}" class="hidden p-3 bg-calm-50/80">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Secciones:</span>
                            <div class="flex gap-2">
                                <button type="button" onclick="marcarTodasSecciones('${colId}', '${bId}', '${g}', true)" class="text-[10px] font-bold text-zen-700 hover:underline">Marcar A-G</button>
                                <span class="text-slate-300">|</span>
                                <button type="button" onclick="marcarTodasSecciones('${colId}', '${bId}', '${g}', false)" class="text-[10px] font-bold text-slate-400 hover:underline">Limpiar</button>
                            </div>
                        </div>

                        <div class="flex flex-wrap items-center gap-2">
                            <!-- Opción Única -->
                            <label id="lbl_unica_${colId}_${bId}_${g}" class="flex items-center gap-1.5 px-3 py-1.5 bg-zen-50 border border-zen-300 rounded-lg text-xs font-extrabold text-zen-800 cursor-pointer hover:bg-zen-100 transition">
                                <input type="checkbox" name="col_${colId}_b${bId}_g_${g}_secciones[]" value="Única" onchange="gestionarSeccionUnica(this, '${colId}', '${bId}', '${g}')" class="accent-zen-600"> 
                                Única
                            </label>

                            <div class="h-5 w-px bg-calm-200 mx-1"></div>

                            <!-- Opciones A-G -->
                            ${seccionesLetras.map(s => `
                                <label id="lbl_sec_${colId}_${bId}_${g}_${s}" class="flex items-center gap-1 px-2.5 py-1.5 bg-white border border-calm-200 rounded-lg text-xs font-bold text-slate-700 cursor-pointer hover:border-zen-400 transition">
                                    <input type="checkbox" name="col_${colId}_b${bId}_g_${g}_secciones[]" value="${s}" onchange="gestionarSeccionLetra(this, '${colId}', '${bId}', '${g}')" class="accent-zen-600 sec-letra-${colId}-${bId}-${g}"> 
                                    ${s}
                                </label>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function toggleSecciones(checkbox, targetId) {
            const divSecciones = document.getElementById(targetId);
            if (checkbox.checked) {
                divSecciones.classList.remove("hidden");
            } else {
                divSecciones.classList.add("hidden");
                const subChecks = divSecciones.querySelectorAll('input[type="checkbox"]');
                subChecks.forEach(c => c.checked = false);
            }
        }

        // LÓGICA DE SECCIÓN ÚNICA vs LETRAS
        function gestionarSeccionUnica(checkUnica, colId, bId, g) {
            const letras = document.querySelectorAll(`.sec-letra-${colId}-${bId}-${g}`);
            letras.forEach(chk => {
                const label = chk.parentElement;
                if (checkUnica.checked) {
                    chk.checked = false;
                    chk.disabled = true;
                    label.classList.add('opacity-35', 'pointer-events-none', 'bg-slate-100');
                    label.classList.remove('hover:border-zen-400');
                } else {
                    chk.disabled = false;
                    label.classList.remove('opacity-35', 'pointer-events-none', 'bg-slate-100');
                }
            });
        }

        function gestionarSeccionLetra(checkLetra, colId, bId, g) {
            if (checkLetra.checked) {
                const checkUnica = document.querySelector(`input[name="col_${colId}_b${bId}_g_${g}_secciones[]"][value="Única"]`);
                if (checkUnica && checkUnica.checked) {
                    checkUnica.checked = false;
                }
            }
        }

        function marcarTodasSecciones(colId, bId, g, marcar) {
            const checkUnica = document.querySelector(`input[name="col_${colId}_b${bId}_g_${g}_secciones[]"][value="Única"]`);
            if (checkUnica) {
                checkUnica.checked = false;
                gestionarSeccionUnica(checkUnica, colId, bId, g);
            }
            const letras = document.querySelectorAll(`.sec-letra-${colId}-${bId}-${g}`);
            letras.forEach(chk => {
                chk.disabled = false;
                chk.checked = marcar;
                chk.parentElement.classList.remove('opacity-35', 'pointer-events-none', 'bg-slate-100');
            });
        }

        function volverPaso1() {
            document.getElementById('paso-2').classList.add('hidden');
            document.getElementById('paso-1').classList.remove('hidden');
            document.getElementById('badge-2').className = "flex items-center gap-2 text-slate-400";
            document.getElementById('badge-2').children[0].className = "h-6 w-6 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center text-[11px]";
            document.getElementById('badge-1').className = "flex items-center gap-2 text-zen-700";
            document.getElementById('badge-1').children[0].className = "h-6 w-6 rounded-full bg-zen-700 text-white flex items-center justify-center text-[11px]";
        }
    </script>
</body>
</html>
```

## File: app/database.py
```python
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
```

## File: .gitignore
```
.env
__pycache__/
*.pyc
app/static/uploads/*
!app/static/uploads/.gitkeep
venv/
database.db
```

## File: app/templates/components/mensaje_ia.html
```html
<div class="w-full max-w-4xl mx-auto mb-10 animate-fade-in-up print:m-0 print:max-w-none">

  <!-- Mensaje del Usuario (Oculto al imprimir) -->
  <div class="flex justify-end mb-6 print:hidden">
    <div
      class="bg-zen-100 text-zen-900 px-5 py-3.5 rounded-3xl rounded-tr-sm max-w-2xl shadow-sm text-sm border border-zen-200">
      <div class="flex items-center gap-2 mb-1.5">
        <span class="font-extrabold text-[10px] uppercase tracking-wider text-zen-700">Tú (Docente)</span>
        {% if archivo_nombre %}
        <span class="bg-white/60 text-zen-800 text-[9px] font-bold px-2 py-0.5 rounded-full border border-zen-200">📎
          Adjunto</span>
        {% endif %}
      </div>
      <p class="leading-relaxed">{{ prompt_usuario }}</p>
    </div>
  </div>

  <!-- Respuesta de la IA / Documento Generado -->
  <div
    class="bg-white border border-calm-200 rounded-3xl shadow-sm overflow-hidden print:border-none print:shadow-none print:rounded-none">

    <!-- Cabecera de herramientas (Oculta al imprimir) -->
    <div
      class="bg-calm-50 border-b border-calm-200 px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 print:hidden">
      <div class="flex items-center gap-2">
        <span
          class="bg-emerald-100 border border-emerald-200 text-emerald-800 text-[10px] font-extrabold px-2.5 py-1 rounded-full uppercase tracking-wider">Normativa
          CNEB</span>
        <span class="text-xs font-bold text-slate-500">Planificación Generada</span>
      </div>

      <div class="flex gap-2">
        <!-- Botón de Word con seguro de pestaña nueva -->
        <a href="/descargar/word/{{ planificacion_id }}" target="_blank" download
          class="px-4 py-2 bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer">
          Word (.doc)
        </a>
        <button onclick="generarPDF('{{ planificacion_id }}');"
          class="px-4 py-2 bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 rounded-xl text-xs font-bold transition flex items-center gap-1.5">
          PDF
        </button>
        <button onclick="window.print()"
          class="px-4 py-2 bg-white border border-calm-200 text-slate-700 hover:bg-calm-50 hover:text-zen-700 rounded-xl text-xs font-extrabold transition shadow-sm flex items-center gap-1.5">
          🖨️ Imprimir
        </button>
      </div>
    </div>

    <!-- Contenido Formateado -->
    <div id="documento-imprimible-{{ planificacion_id }}" class="p-6 md:p-10 bg-white">

      {% if perfil and perfil.logo_url and modo_generacion != 'LIBRE' %}
      <div class="flex items-center gap-4 border-b border-calm-200 pb-4 mb-6">
        <img src="{{ perfil.logo_url if perfil.logo_url.startswith('http') else '/static/uploads/' ~ perfil.logo_url }}"
          alt="Logo I.E." class="h-14 w-auto object-contain">
        <div>
          <h2 class="text-base font-black text-slate-800 uppercase tracking-tight">{{ perfil.nombre_ie }}</h2>
          <p class="text-xs text-slate-500 font-semibold">{{ perfil.ugel }} • Planificación Curricular</p>
        </div>
      </div>
      {% endif %}
      <!-- La clase "prose" de Tailwind da estilo automático a tablas, listas y negritas -->
      <!-- El filtro | safe evita que Jinja2 escape el HTML -->
      <div class="prose prose-sm md:prose-base prose-slate max-w-none 
                        prose-headings:text-zen-800 prose-headings:font-extrabold 
                        prose-a:text-zen-600 
                        prose-table:w-full prose-table:border-collapse prose-table:text-sm
                        prose-th:bg-calm-50 prose-th:p-3 prose-th:border prose-th:border-calm-200 prose-th:text-calm-800
                        prose-td:p-3 prose-td:border prose-td:border-calm-200 prose-td:text-slate-600
                        prose-strong:text-calm-800">
        {{ respuesta_html | safe }}
      </div>
    </div>

  </div>
</div>

<!-- SOLO se ejecuta si es un mensaje recién creado -->
{% if es_nuevo %}
<!-- OOB directo al ID del index -->
<button hx-swap-oob="afterbegin:#lista-historial" hx-get="/historial/{{ planificacion_id }}" hx-target="#area-documento"
  class="w-full text-left px-3 py-2.5 rounded-lg hover:bg-calm-50 dark:hover:bg-calm-800 transition group flex flex-col gap-0.5 border-l-2 border-zen-600 bg-zen-50/40 dark:bg-zen-900/20 mb-1">

  <span
    class="text-xs font-extrabold text-slate-800 dark:text-calm-200 truncate group-hover:text-zen-700 dark:group-hover:text-zen-400 transition">
    {{ prompt_usuario[:45] | capitalize }}{% if prompt_usuario|length > 45 %}...{% endif %}
  </span>

  {% if modo_generacion == 'LIBRE' %}
  <span class="text-[10px] text-slate-500 font-bold tracking-wide">💭 Asistente Libre</span>
  {% else %}
  <span class="text-[10px] text-slate-500 truncate font-semibold">
    {{ area_contexto }} • {{ grado_contexto }}
  </span>
  {% endif %}
</button>
{% endif %}

<!-- Estilo CSS específico para que al imprimir no salga la barra lateral ni el menú -->
<style>
  @media print {
    body {
      background-color: white;
      overflow: visible !important;
    }

    aside,
    header,
    form,
    #pildoras-atajos {
      display: none !important;
    }

    main {
      display: block !important;
      padding: 0 !important;
      overflow: visible !important;
    }

    #area-documento {
      display: block !important;
      padding: 0 !important;
      overflow: visible !important;
      height: auto !important;
    }

    .prose {
      max-width: 100% !important;
      font-size: 12pt !important;
    }

    /* Reglas MÁGICAS para evitar que las tablas se rompan en PDF */
    table {
      page-break-inside: auto;
      width: 100%;
    }

    tr {
      page-break-inside: avoid;
      page-break-after: auto;
    }

    thead {
      display: table-header-group;
    }

    tfoot {
      display: table-footer-group;
    }
  }
</style>

<script>
  function generarPDF(id) {
    const elemento = document.getElementById('documento-imprimible-' + id);

    // Ocultar temporalmente bordes o sombras si lo deseas para el PDF
    const opciones = {
      margin: [10, 10, 15, 10], // Márgenes: Arriba, Derecha, Abajo, Izquierda
      filename: 'Sesion_EduPlan_' + id + '.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['css', 'legacy'] } // <-http://127.0.0.1:8000/docs-- ¡Añadir esta línea!
    };

    html2pdf().set(opciones).from(elemento).save();
  }
</script>
```

## File: app/templates/components/modal_perfil.html
```html
<div id="modal-backdrop"
    class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div
        class="bg-white dark:bg-calm-800 border border-calm-200 dark:border-slate-700 w-full max-w-xl rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] transition-all">

        <!-- Cabecera del Modal -->
        <div class="px-6 py-4 border-b border-calm-100 dark:border-slate-700 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <span class="text-base">⚙️</span>
                <h3 class="text-sm font-extrabold text-slate-800 dark:text-slate-100">Configuración del Sistema</h3>
            </div>
            <button onclick="document.getElementById('modal-backdrop').remove()"
                class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition">✕</button>
        </div>

        <!-- Pestañas -->
        <div class="flex border-b border-calm-100 dark:border-slate-700 px-6 pt-3 text-xs font-bold gap-4">
            <button id="tab-btn-sedes" onclick="cambiarTabConfig('sedes')"
                class="pb-2.5 border-b-2 border-zen-700 text-zen-700 dark:text-zen-400">
                🏫 Instituciones y Aulas
            </button>
            <button id="tab-btn-ajustes" onclick="cambiarTabConfig('ajustes')"
                class="pb-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-600 dark:hover:text-slate-300">
                🎨 Apariencia y Perfil
            </button>
        </div>

        <!-- Contenido Scrollable -->
        <div class="p-6 overflow-y-auto flex-1 space-y-5">

            <!-- PANEL 1: SEDES Y AULAS -->
            <div id="tab-content-sedes" class="space-y-4">
                {% for item in datos_sedes %}
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        {% if item.institucion.logo_url %}
                        <img src="{{ item.institucion.logo_url if item.institucion.logo_url.startswith('http') else '/static/uploads/' ~ item.institucion.logo_url }}"
                            alt="Logo {{ item.institucion.nombre_ie }}"
                            class="w-9 h-9 object-contain rounded-lg border border-calm-200 dark:border-slate-700 bg-white p-0.5 shadow-sm">
                        {% endif %}
                        <div>
                            <span class="text-xs font-black text-slate-800 dark:text-slate-100 block">{{
                                item.institucion.nombre_ie }}</span>
                            <span class="text-[10px] text-slate-400">{{ item.institucion.ugel }}</span>
                        </div>
                    </div>
                </div>

                <!-- Lista de Aulas / Cargas -->
                <div class="space-y-1.5">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Cargas
                        Asignadas:</span>
                    <div class="flex flex-wrap gap-1.5">
                        {% for c in item.cargas %}
                        <div id="badge-carga-{{ c.id }}"
                            class="inline-flex items-center gap-1.5 bg-white dark:bg-slate-800 border border-calm-200 dark:border-slate-700 px-2.5 py-1 rounded-lg text-xs font-bold text-slate-700 dark:text-slate-200">
                            <span>{{ c.area }} ({{ c.grado }} "{{ c.seccion }}")</span>
                            <button hx-delete="/api/eliminar-carga/{{ c.id }}" hx-target="#badge-carga-{{ c.id }}"
                                hx-swap="outerHTML"
                                class="text-slate-300 hover:text-red-500 transition text-[10px] font-black"
                                title="Eliminar esta aula">✕</button>
                        </div>
                        {% else %}
                        <span class="text-xs text-slate-400 italic">Sin aulas registradas en esta sede.</span>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endfor %}

            <div class="pt-2 text-center">
                <a href="/onboarding"
                    class="inline-flex items-center gap-2 text-xs font-bold text-zen-700 dark:text-zen-400 hover:underline">
                    <span>🔄 Reconfigurar todos los colegios (Asistente Completo)</span>
                </a>
            </div>
        </div>

        <!-- PANEL 2: APARIENCIA Y GENERAL -->
        <div id="tab-content-ajustes" class="space-y-4 hidden">
            <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Nombre Completo</label>
                <input type="text" value="{{ usuario.nombre_completo }}" disabled
                    class="w-full text-xs rounded-xl border border-calm-200 dark:border-slate-700 p-2.5 bg-calm-50 dark:bg-slate-900 text-slate-500">
            </div>

            <!-- Switch Modo Oscuro -->
            <div
                class="flex items-center justify-between p-4 rounded-2xl bg-calm-50 dark:bg-slate-900/50 border border-calm-200 dark:border-slate-700">
                <div>
                    <span class="block text-xs font-bold text-slate-700 dark:text-slate-200">Modo Oscuro</span>
                    <span class="block text-[11px] text-slate-400">Reduce el brillo para trabajo nocturno</span>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" id="dark-mode-toggle" class="sr-only peer"
                        onchange="alternarModoOscuro(this)">
                    <div
                        class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-zen-600">
                    </div>
                </label>
            </div>

            <div class="pt-2 border-t border-calm-100 dark:border-slate-700">
                <a href="/logout"
                    class="block w-full py-2.5 text-center text-xs font-bold text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-xl transition">
                    Cerrar Sesión
                </a>
            </div>
        </div>

    </div>

</div>
</div>

<script>
    // Sincronizar estado inicial del toggle
    if (document.documentElement.classList.contains('dark')) {
        document.getElementById('dark-mode-toggle').checked = true;
    }

    function alternarModoOscuro(checkbox) {
        if (checkbox.checked) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }
    }

    function cambiarTabConfig(tab) {
        const btnSedes = document.getElementById('tab-btn-sedes');
        const btnAjustes = document.getElementById('tab-btn-ajustes');
        const contentSedes = document.getElementById('tab-content-sedes');
        const contentAjustes = document.getElementById('tab-content-ajustes');

        if (tab === 'sedes') {
            btnSedes.className = "pb-2.5 border-b-2 border-zen-700 text-zen-700 dark:text-zen-400";
            btnAjustes.className = "pb-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-600 dark:hover:text-slate-300";
            contentSedes.classList.remove('hidden');
            contentAjustes.classList.add('hidden');
        } else {
            btnAjustes.className = "pb-2.5 border-b-2 border-zen-700 text-zen-700 dark:text-zen-400";
            btnSedes.className = "pb-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-600 dark:hover:text-slate-300";
            contentAjustes.classList.remove('hidden');
            contentSedes.classList.add('hidden');
        }
    }
</script>
```

## File: app/models.py
```python
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
```

## File: requirements.txt
```
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.0
asarPy==1.0.1
bcrypt==5.0.0
certifi==2026.7.22
cffi==2.1.1
charset-normalizer==3.5.1
click==8.5.0
cryptography==50.0.1
deprecation==2.1.0
distro==1.9.0
fastapi==0.141.1
google-auth==2.57.0
google-genai==2.22.0
greenlet==3.5.5
h11==0.16.0
h2==4.4.1
hpack==4.2.0
httpcore==1.0.9
httptools==0.8.0
httpx==0.28.1
hyperframe==6.1.0
idna==3.19
itsdangerous==2.2.0
Jinja2==3.1.6
Markdown==3.10.3
MarkupSafe==3.0.3
multidict==7.0.0
nh3==0.3.7
packaging==26.3
passlib==1.7.4
pillow==12.3.0
postgrest==2.31.0
propcache==0.5.4
psycopg2-binary==2.9.13
pyasn1==0.6.4
pyasn1_modules==0.4.2
pycparser==3.0
pydantic==2.13.5
pydantic_core==2.46.5
PyJWT==2.15.1
python-dotenv==1.2.3
python-multipart==0.0.32
PyYAML==6.0.3
realtime==2.31.0
requests==2.34.2
sniffio==1.3.1
SQLAlchemy==2.0.52
sqlmodel==0.0.42
starlette==1.6.0
storage3==2.31.0
StrEnum==0.4.15
supabase==2.31.0
supabase-auth==2.31.0
supabase-functions==2.31.0
tenacity==9.1.4
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.7.0
uvicorn==0.52.4
uvloop==0.22.1
watchfiles==1.2.0
websockets==15.0.1
yarl==1.25.1
```

## File: app/templates/index.html
```html
{% extends "base.html" %}

{% block content %}
<script>
    tailwind.config = {
        darkMode: 'class',
        theme: {
            extend: {
                fontFamily: { sans: ['Nunito', 'sans-serif'] },
                colors: {
                    calm: { 50: '#fafaf9', 100: '#f5f5f4', 200: '#e7e5e4', 700: '#44403c', 800: '#292524', 900: '#1c1917', 950: '#0c0a09' },
                    zen: { 50: '#f0fdfa', 100: '#ccfbf1', 200: '#99f6e4', 400: '#2dd4bf', 600: '#0d9488', 700: '#0f766e', 800: '#115e59', 900: '#134e4a' }
                }
            }
        }
    }
</script>
<script>
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
</script>
<style>
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #e7e5e4;
        border-radius: 10px;
    }

    .dark ::-webkit-scrollbar-thumb {
        background: #44403c;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #d6d3d1;
    }

    .dark ::-webkit-scrollbar-thumb:hover {
        background: #57534e;
    }
</style>

<div
    class="flex h-screen bg-calm-50 dark:bg-calm-950 font-sans text-calm-800 dark:text-calm-100 antialiased selection:bg-zen-600 selection:text-white overflow-hidden transition-colors duration-200">

    <!-- ========================================== -->
    <!-- BARRA LATERAL (Historial y Colecciones)    -->
    <!-- ========================================== -->
    <aside
        class="w-72 bg-white dark:bg-calm-900 border-r border-calm-200 dark:border-calm-700 flex flex-col h-full shadow-sm z-10 hidden md:flex transition-colors duration-200">

        <!-- Logo superior -->
        <div class="h-16 flex items-center px-6 border-b border-calm-100 dark:border-calm-700/60 shrink-0">
            <div class="flex items-center gap-2.5">
                <div
                    class="flex h-8 w-8 items-center justify-center rounded-xl bg-zen-700 text-sm font-black text-white shadow-sm">
                    EP</div>
                <span class="text-base font-black tracking-tight text-calm-800 dark:text-white">EduPlan Perú</span>
            </div>
        </div>

        <!-- Botón Nuevo Documento -->
        <div class="p-4 shrink-0">
            <button onclick="window.location.reload()"
                class="w-full flex items-center justify-center gap-2 rounded-xl bg-white dark:bg-calm-800 border border-calm-200 dark:border-calm-700 py-2.5 text-sm font-bold text-slate-600 dark:text-calm-100 hover:border-zen-600 dark:hover:border-zen-400 hover:text-zen-700 dark:hover:text-zen-400 transition shadow-sm group">
                <span class="text-lg group-hover:rotate-90 transition-transform duration-300">+</span> Nueva
                planificación
            </button>
        </div>

        <!-- Colecciones / Carpetas -->
        <div class="px-4 pb-3 border-b border-calm-100 dark:border-calm-700/60 mb-2 shrink-0">
            <div class="flex items-center justify-between mb-2 px-2">
                <h3 class="text-[10px] font-extrabold text-slate-400 dark:text-stone-400 uppercase tracking-wider">Tus
                    Carpetas</h3>
                <button onclick="document.getElementById('modal-coleccion').classList.remove('hidden')"
                    class="text-slate-400 hover:text-zen-700 dark:hover:text-zen-400 transition font-bold"
                    title="Nueva Carpeta">➕</button>
            </div>
            <div class="space-y-1 max-h-32 overflow-y-auto">
                {% for col in colecciones %}
                <button
                    class="w-full text-left px-3 py-2 rounded-lg hover:bg-calm-50 dark:hover:bg-calm-800 transition flex items-center gap-2 group">
                    <span class="text-[10px]">📁</span>
                    <span
                        class="text-xs font-bold text-slate-700 dark:text-calm-200 truncate group-hover:text-zen-700 dark:group-hover:text-zen-400">{{
                        col.nombre }}</span>
                </button>
                {% else %}
                <div class="px-3 py-2 text-[10px] text-slate-400 italic text-center">No hay carpetas creadas.</div>
                {% endfor %}
            </div>
        </div>

        <!-- Lista de Historial -->
        <div class="flex-1 overflow-y-auto px-4 pb-4 mt-2">
            <div class="flex items-center justify-between mb-3 px-2">
                <h3 class="text-[10px] font-extrabold text-slate-400 dark:text-stone-400 uppercase tracking-wider">
                    Historial Reciente</h3>
            </div>
            <div id="lista-historial" class="space-y-1">
                {% include "components/lista_historial.html" %}
            </div>
        </div>

        <!-- Badge de Perfil (Bottom) -->
        <div class="p-4 border-t border-calm-100 dark:border-calm-700/60 shrink-0 bg-calm-50/50 dark:bg-calm-900/60">
            <div class="flex items-center gap-3">
                <div
                    class="h-9 w-9 rounded-full bg-zen-100 dark:bg-zen-900/60 flex items-center justify-center text-zen-700 dark:text-zen-400 font-bold border border-zen-200 dark:border-zen-700 shrink-0 overflow-hidden">
                    {% if perfil and perfil.logo_url %}
                    <img src="/static/uploads/{{ perfil.logo_url }}" alt="Logo" class="h-full w-full object-cover">
                    {% else %}
                    {{ perfil.nombre_docente[0:1] if perfil and perfil.nombre_docente else (usuario.nombre_completo[0:1]
                    if usuario else 'U') }}
                    {% endif %}
                </div>
                <div class="flex flex-col overflow-hidden">
                    <span class="text-xs font-extrabold text-slate-700 dark:text-calm-100 truncate">
                        {{ perfil.nombre_docente if perfil and perfil.nombre_docente else (usuario.nombre_completo if
                        usuario else 'Docente') }}
                    </span>
                    <span class="text-[10px] text-slate-500 dark:text-stone-400 truncate">
                        {{ perfil.nombre_ie if perfil else 'Sin Institución' }}
                    </span>
                </div>
                <button hx-get="/modal-perfil" hx-target="body" hx-swap="beforeend"
                    class="p-2 ml-auto text-slate-400 dark:text-stone-400 hover:text-zen-700 dark:hover:text-zen-400 transition"
                    title="Configurar instituciones y apariencia">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z">
                        </path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                </button>
            </div>
        </div>
    </aside>

    <!-- ========================================== -->
    <!-- ÁREA PRINCIPAL (Header, Chat, Formulario)  -->
    <!-- ========================================== -->
    <main class="flex-1 flex flex-col h-full relative bg-calm-50 dark:bg-calm-950 transition-colors duration-200">

        <!-- HEADER CONGELADO -->
        <header
            class="bg-white dark:bg-calm-900 border-b border-calm-200 dark:border-calm-700 h-16 flex items-center px-6 shrink-0 print:hidden z-10 transition-colors duration-200">
            <div class="flex justify-between items-center w-full max-w-6xl">

                <div class="flex items-center gap-4">
                    <!-- Toggle de Modo (CNEB / Libre) SIEMPRE VISIBLE -->
                    <div
                        class="flex bg-calm-100 dark:bg-calm-800 rounded-lg p-0.5 border border-calm-200 dark:border-calm-700 shrink-0">
                        <button type="button" id="btn-modo-cneb" onclick="alternarModo('CNEB')"
                            class="px-3 py-1.5 text-[11px] font-extrabold rounded-md bg-white dark:bg-calm-700 text-calm-800 dark:text-white shadow-sm transition"
                            title="Modo Oficial CNEB">CNEB</button>
                        <button type="button" id="btn-modo-libre" onclick="alternarModo('LIBRE')"
                            class="px-3 py-1.5 text-[11px] font-extrabold rounded-md text-slate-500 hover:text-calm-800 dark:hover:text-white transition"
                            title="Asistente Libre sin Formato">Libre</button>
                    </div>

                    <!-- CONTENEDOR DE CONTEXTO (Se oculta en Modo Libre) -->
                    <div id="panel-contexto-dual"
                        class="flex items-center gap-3 transition-all duration-300 overflow-hidden">

                        <div class="w-px h-6 bg-calm-200 dark:bg-calm-700 mx-1 hidden sm:block"></div>

                        <!-- Selector Colegio -->
                        <div
                            class="flex items-center gap-1.5 bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 rounded-xl px-2.5 py-1.5 shrink-0">
                            <span class="text-xs">🏫</span>
                            <select onchange="window.location.href='/app?institucion_id=' + this.value"
                                class="bg-transparent text-slate-700 dark:text-calm-100 text-xs font-bold outline-none cursor-pointer truncate max-w-[120px]">
                                {% for inst in instituciones %}
                                <option value="{{ inst.id }}"
                                    class="bg-white dark:bg-calm-900 text-slate-700 dark:text-calm-100" {% if perfil and
                                    inst.id==perfil.id %}selected{% endif %}>
                                    {{ inst.nombre_ie }}
                                </option>
                                {% endfor %}
                            </select>
                        </div>

                        <!-- Selector Área -->
                        <select name="contexto_activo" form="form-chat"
                            hx-get="/api/selector-grados?institucion_id={{ perfil.id }}"
                            hx-target="#contenedor-grado-seccion" hx-trigger="change"
                            class="bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 text-zen-800 dark:text-zen-400 text-xs font-bold rounded-xl px-2.5 py-1.5 outline-none transition cursor-pointer hidden md:block">
                            {% for a in areas %}
                            <option value="{{ a }}" class="bg-white dark:bg-calm-900 text-slate-700 dark:text-calm-100">
                                {{ a }}</option>
                            {% endfor %}
                        </select>

                        <!-- Grado y Sección -->
                        <div id="contenedor-grado-seccion" class="hidden lg:flex gap-2 items-center">
                            <select name="grado_activo" form="form-chat"
                                hx-get="/api/selector-secciones?institucion_id={{ perfil.id }}&contexto_activo={{ areas[0] if areas else 'General' }}"
                                hx-target="next select" hx-trigger="change"
                                class="bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 text-zen-800 dark:text-zen-400 text-xs font-bold rounded-xl px-2.5 py-1.5 outline-none transition cursor-pointer min-w-[70px]">
                                {% for g in grados %}
                                <option value="{{ g }}"
                                    class="bg-white dark:bg-calm-900 text-slate-700 dark:text-calm-100">{{ g }}</option>
                                {% endfor %}
                            </select>
                            <select name="seccion_activa" form="form-chat"
                                class="bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 text-zen-800 dark:text-zen-400 text-xs font-bold rounded-xl px-2.5 py-1.5 outline-none transition cursor-pointer min-w-[80px]">
                                {% for s in secciones %}
                                <option value="{{ s }}"
                                    class="bg-white dark:bg-calm-900 text-slate-700 dark:text-calm-100">Secc. {{ s }}
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Columna Derecha: Filtro de Historial -->
                <div id="contenedor-toggle-filtro" class="shrink-0">
                    <button hx-get="/filtrar-historial?ver_todos=true" hx-target="#lista-historial" hx-swap="innerHTML"
                        class="text-[11px] font-bold text-slate-600 dark:text-stone-300 hover:text-zen-700 dark:hover:text-zen-400 bg-calm-50 dark:bg-calm-800 border border-calm-200 dark:border-calm-700 px-3 py-1.5 rounded-xl transition whitespace-nowrap shadow-sm">
                        Ver todo el historial
                    </button>
                </div>

            </div>
        </header>

        <!-- AREA CENTRAL DE DOCUMENTO (Scrolleable) -->
        <div id="area-documento" class="flex-1 overflow-y-auto p-6 md:p-10 flex flex-col items-center">

            <!-- Estado Inicial Vacío -->
            <div class="w-full max-w-3xl mt-10 md:mt-20 text-center animate-fade-in">
                <div
                    class="h-16 w-16 mx-auto bg-calm-100 dark:bg-calm-900 rounded-3xl flex items-center justify-center text-3xl mb-6 shadow-inner text-zen-700 dark:text-zen-400 border border-transparent dark:border-calm-700/60">
                    ✨
                </div>
                <h2 class="text-2xl font-extrabold text-calm-800 dark:text-white mb-2">¿Qué planificaremos hoy?</h2>
                <p class="text-sm text-slate-500 dark:text-stone-400 max-w-md mx-auto leading-relaxed"
                    id="texto-bienvenida">
                    Tus documentos estarán alineados automáticamente al área seleccionada arriba y a los datos de tu
                    institución.
                </p>
            </div>

            <!-- Indicador de Carga HTMX -->
            <div id="indicador-carga"
                class="htmx-indicator w-full max-w-3xl mt-12 flex flex-col items-center justify-center gap-4 text-slate-500 dark:text-slate-400">
                <div class="flex gap-2">
                    <div class="w-2.5 h-2.5 bg-zen-600 rounded-full animate-bounce" style="animation-delay: -0.3s">
                    </div>
                    <div class="w-2.5 h-2.5 bg-zen-600 rounded-full animate-bounce" style="animation-delay: -0.15s">
                    </div>
                    <div class="w-2.5 h-2.5 bg-zen-600 rounded-full animate-bounce"></div>
                </div>
                <span class="text-sm font-bold text-zen-700 dark:text-zen-400">Procesando solicitud...</span>
            </div>

        </div>

        <!-- FORMULARIO INFERIOR FIJO -->
        <div
            class="w-full bg-white dark:bg-calm-900 border-t border-calm-200 dark:border-calm-700 shrink-0 print:hidden transition-colors duration-200 z-10 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
            <div class="w-full max-w-4xl mx-auto p-4 sm:p-6">

                <!-- Atajos Rápidos -->
                <div class="flex gap-2 overflow-x-auto pb-3 mb-1 snap-x scrollbar-hide" id="pildoras-atajos">
                    <button
                        onclick="insertarPrompt('Crea una sesión de aprendizaje de 90 minutos usando los procesos pedagógicos.')"
                        class="snap-start shrink-0 rounded-full border border-calm-200 dark:border-calm-700 bg-calm-50 dark:bg-calm-800 px-4 py-1.5 text-xs font-bold text-slate-600 dark:text-stone-300 hover:border-zen-600 dark:hover:border-zen-400 hover:text-zen-700 dark:hover:text-zen-400 transition">
                        📝 Sesión 90 min
                    </button>
                    <button
                        onclick="insertarPrompt('Elabora una rúbrica de evaluación formativa con escala AD, A, B, C.')"
                        class="snap-start shrink-0 rounded-full border border-calm-200 dark:border-calm-700 bg-calm-50 dark:bg-calm-800 px-4 py-1.5 text-xs font-bold text-slate-600 dark:text-stone-300 hover:border-zen-600 dark:hover:border-zen-400 hover:text-zen-700 dark:hover:text-zen-400 transition">
                        📊 Rúbrica CNEB
                    </button>
                    <button onclick="insertarPrompt('Redacta un oficio formal dirigido a la UGEL justificando...')"
                        class="snap-start shrink-0 rounded-full border border-calm-200 dark:border-calm-700 bg-calm-50 dark:bg-calm-800 px-4 py-1.5 text-xs font-bold text-slate-600 dark:text-stone-300 hover:border-zen-600 dark:hover:border-zen-400 hover:text-zen-700 dark:hover:text-zen-400 transition">
                        🏢 Oficio UGEL
                    </button>
                    <button onclick="insertarPrompt('Genera una dinámica de integración para mis estudiantes sobre...')"
                        class="snap-start shrink-0 rounded-full border border-calm-200 dark:border-calm-700 bg-calm-50 dark:bg-calm-800 px-4 py-1.5 text-xs font-bold text-slate-600 dark:text-stone-300 hover:border-zen-600 dark:hover:border-zen-400 hover:text-zen-700 dark:hover:text-zen-400 transition">
                        🌍 Dinámica
                    </button>
                </div>

                <!-- Formulario Principal de Chat -->
                <form id="form-chat" hx-post="/enviar-mensaje" hx-target="#area-documento"
                    hx-indicator="#indicador-carga"
                    hx-on="htmx:beforeRequest: document.getElementById('area-documento').innerHTML = '';"
                    hx-on::after-request="if(event.detail.successful) { this.reset(); document.getElementById('prompt-input').style.height = 'auto'; }"
                    enctype="multipart/form-data"
                    class="relative flex items-end gap-3 bg-white dark:bg-calm-800 rounded-2xl border border-calm-200 dark:border-calm-700 p-2 shadow-sm focus-within:border-zen-600 dark:focus-within:border-zen-400 focus-within:ring-4 focus-within:ring-zen-50 dark:focus-within:ring-zen-900/30 transition-all">

                    <!-- INPUT OCULTO PARA EL MODO DE GENERACIÓN -->
                    <input type="hidden" name="modo_generacion" id="input-modo-generacion" value="CNEB">

                    <!-- Adjuntar -->
                    <label
                        class="cursor-pointer p-3 text-slate-400 dark:text-stone-400 hover:text-zen-700 dark:hover:text-zen-400 hover:bg-zen-50 dark:hover:bg-calm-700 rounded-xl transition shrink-0">
                        <input type="file" name="foto" class="hidden" accept="image/*, .pdf">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13">
                            </path>
                        </svg>
                    </label>

                    <!-- Textarea -->
                    <textarea id="prompt-input" name="prompt" rows="1"
                        placeholder="Describe lo que necesitas pedagógicamente..." required
                        class="w-full max-h-40 resize-none border-none bg-transparent py-3 text-sm text-slate-800 dark:text-calm-100 placeholder-slate-400 dark:placeholder-stone-400 focus:outline-none focus:ring-0"></textarea>

                    <!-- Botón Enviar -->
                    <button id="btn-enviar-prompt" type="submit"
                        class="p-3 text-white bg-zen-700 hover:bg-zen-800 dark:bg-zen-600 dark:hover:bg-zen-700 rounded-xl transition shadow-md shrink-0 mb-0.5 mr-0.5 cursor-pointer">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                        </svg>
                    </button>
                </form>

            </div>
        </div>

    </main>

    <!-- ========================================== -->
    <!-- MODAL NUEVA CARPETA / COLECCIÓN            -->
    <!-- ========================================== -->
    <div id="modal-coleccion"
        class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
        <div
            class="bg-white dark:bg-calm-800 border border-calm-200 dark:border-slate-700 w-full max-w-sm rounded-3xl shadow-2xl p-6 transition-all">
            <div class="flex justify-between items-center mb-4 pb-3 border-b border-calm-100 dark:border-calm-700">
                <h3 class="font-extrabold text-calm-800 dark:text-white flex items-center gap-2">
                    <span>📁</span> Crear Colección
                </h3>
                <button onclick="document.getElementById('modal-coleccion').classList.add('hidden')"
                    class="text-slate-400 hover:text-slate-600 dark:hover:text-white transition">✕</button>
            </div>

            <form hx-post="/api/colecciones" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5">Nombre de la
                        Carpeta</label>
                    <input type="text" name="nombre" placeholder="Ej. Unidad 1, Tutoría, Exámenes..." required
                        class="w-full text-sm rounded-xl border border-calm-200 dark:border-slate-700 p-2.5 bg-calm-50 dark:bg-slate-900 text-slate-800 dark:text-calm-100 outline-none focus:border-zen-700 dark:focus:border-zen-400 transition">
                </div>
                <div class="pt-2">
                    <button type="submit"
                        class="w-full bg-zen-700 dark:bg-zen-600 text-white font-extrabold text-xs py-3 rounded-xl hover:bg-zen-800 dark:hover:bg-zen-700 transition shadow-md shadow-zen-700/20">
                        Guardar Carpeta
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Script de Interacción -->
    <script>
        const textarea = document.getElementById('prompt-input');
        textarea.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight < 160 ? this.scrollHeight : 160) + 'px';
        });

        function insertarPrompt(texto) {
            textarea.value = texto;
            textarea.focus();
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        }

        // Lógica para alternar Modos (CNEB vs Libre)
        function alternarModo(modo) {
            const btnCneb = document.getElementById('btn-modo-cneb');
            const btnLibre = document.getElementById('btn-modo-libre');
            const panelContexto = document.getElementById('panel-contexto-dual');
            const inputHidden = document.getElementById('input-modo-generacion');
            const textoBienvenida = document.getElementById('texto-bienvenida');

            inputHidden.value = modo;

            if (modo === 'CNEB') {
                btnCneb.className = "px-3 py-1.5 text-[11px] font-extrabold rounded-md bg-white dark:bg-calm-700 text-calm-800 dark:text-white shadow-sm transition";
                btnLibre.className = "px-3 py-1.5 text-[11px] font-extrabold rounded-md text-slate-500 hover:text-calm-800 dark:hover:text-white transition";

                // Mostrar contexto (colegio, curso, grado)
                panelContexto.classList.remove('hidden');

                if (textoBienvenida) textoBienvenida.innerHTML = "Tus documentos estarán alineados automáticamente al área seleccionada arriba y a los datos de tu institución.";
            } else {
                btnLibre.className = "px-3 py-1.5 text-[11px] font-extrabold rounded-md bg-white dark:bg-calm-700 text-calm-800 dark:text-white shadow-sm transition";
                btnCneb.className = "px-3 py-1.5 text-[11px] font-extrabold rounded-md text-slate-500 hover:text-calm-800 dark:hover:text-white transition";

                // Ocultar contexto completamente
                panelContexto.classList.add('hidden');

                if (textoBienvenida) textoBienvenida.innerHTML = "<strong>Modo Libre activado.</strong><br>Consultas pedagógicas generales sin formato estricto de aula.";
            }
        }

        // Auto-scroll del documento generado
        document.body.addEventListener('htmx:afterSwap', function (evt) {
            if (evt.detail.target.id === 'area-documento') {
                const area = document.getElementById('area-documento');
                area.scrollTop = 0;
            }
        });
    </script>

    <!-- Renderizado Matemático Automático con KaTeX -->
    <script>
        document.body.addEventListener('htmx:afterSwap', function (evt) {
            if (window.renderMathInElement) {
                renderMathInElement(evt.detail.target, {
                    delimiters: [
                        { left: '$$', right: '$$', display: true },
                        { left: '$', right: '$', display: false }
                    ],
                    throwOnError: false
                });
            }
        });
    </script>
</div>
{% endblock %}
```

## File: app/main.py
```python
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
from app.services.storage_service import subir_logo_supabase
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
        logo_url = None
        
        if logo_file and getattr(logo_file, "filename", ""):
            contenido_bytes = await logo_file.read()
            if contenido_bytes:
                logo_url = subir_logo_supabase(contenido_bytes, logo_file.filename, usuario.id)

        nuevo_colegio = PerfilInstitucional(
            usuario_id=usuario.id,
            nombre_ie=nombre_ie.strip(),
            ugel=ugel.strip(),
            nombre_docente=usuario.nombre_completo,
            logo_url=logo_url
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
            "perfil": perfil,
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

    # Resolver el perfil institucional asociado a la planificación
    perfil = None
    if plan.institucion_id:
        perfil = session.get(PerfilInstitucional, plan.institucion_id)

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
            "perfil": perfil,
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
```
