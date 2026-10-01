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