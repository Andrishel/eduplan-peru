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
                # Subida de archivo con manejo seguro
                archivo_remoto = client.files.upload(file=ruta_archivo)
                contenidos.append(archivo_remoto)
        except Exception as err:
            print(f"Aviso: No se pudo adjuntar el documento a Gemini ({err}). Se procesará solo el texto.")

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