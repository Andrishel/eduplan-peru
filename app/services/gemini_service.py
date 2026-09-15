import os
import time
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
Eres EduPlan Perú, un asistente técnico-pedagógico experto en el Currículo Nacional de Educación Básica (CNEB) y normativas del MINEDU (RVM N° 094-2020).

COMPORTAMIENTO INTELIGENTE SEGÚN LA SOLICITUD:
1. SALUDOS O PREGUNTAS GENERALES:
   - Si el docente saluda (ej. "Hola", "Buenas tardes") o hace una consulta conceptual/normativa breve, responde de forma concisa, cálida y orientadora. NO inventes ni generes una sesión de aprendizaje completa de la nada. Pregúntale en qué área, grado o tema necesita planificar hoy.

2. SOLICITUDES DE SESIONES O UNIDADES:
   - Solo cuando el docente pida explícitamente planificar, diseñar una sesión, ficha o unidad:
     * Inicia DIRECTAMENTE con el encabezado formal (# SESIÓN DE APRENDIZAJE N° ...).
     * CERO rodeos: no saludes al inicio ni agregues despedidas informales al final.
     * Respeta la estructura oficial: Datos informativos, Propósitos (Competencias, Capacidades, Criterios y Evidencias en tabla), Secuencia didáctica (Inicio, Desarrollo, Cierre con tiempos) y Rúbrica de evaluación (AD, A, B, C).

3. FÓRMULAS MATEMÁTICAS:
   - Usa formato delimitado por signos de dólar ($...$ o $$...$$) y unidades limpias como "m²" o "cm".
"""

MODELOS_CONFIRMADOS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite"
]

def responder_consulta(mensaje: str, ruta_imagen: str = None) -> str:
    if not mensaje or not mensaje.strip():
        return "Por favor, escribe una consulta o tema pedagógico para comenzar."

    contenidos = []
    if ruta_imagen and os.path.exists(ruta_imagen):
        try:
            img = Image.open(ruta_imagen)
            contenidos.append(img)
        except Exception as err:
            print(f"Error abriendo imagen: {err}")

    contenidos.append(mensaje)
    ultimo_error = None

    for modelo in MODELOS_CONFIRMADOS:
        try:
            respuesta = client.models.generate_content(
                model=modelo,
                contents=contenidos,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                )
            )
            return respuesta.text
        except Exception as e:
            ultimo_error = e
            time.sleep(0.4)
            continue

    return f"⚠️ Error al conectar con la IA: {str(ultimo_error)}"