import base64, hashlib, hmac, secrets
from cryptography.fernet import Fernet
from .config import settings

def cipher() -> Fernet:
    try: return Fernet(settings.token_encryption_key.encode())
    except Exception:
        return Fernet(base64.urlsafe_b64encode(hashlib.sha256(settings.token_encryption_key.encode()).digest()))

def encrypt(value: str) -> str: return cipher().encrypt(value.encode()).decode()
def decrypt(value: str) -> str: return cipher().decrypt(value.encode()).decode()
def new_state() -> str: return secrets.token_urlsafe(32)
def valid_signature(body: bytes, signature: str | None, secret: str) -> bool:
    if not signature or not signature.startswith("sha256="): return False
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
