import hashlib
import os
import secrets
from itsdangerous import URLSafeTimedSerializer
from typing import Optional

SECRET_KEY = "eduplan_secret_key_super_segura_cambiar_en_produccion"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def hashear_password(password: str) -> str:
    """Genera un hash seguro usando PBKDF2-HMAC-SHA256 con Salt aleatorio"""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica si la contraseña coincide con el hash almacenado"""
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