from cryptography.fernet import Fernet
from app.core.config import settings
import base64

# Use a static key for dev, should be loaded from secure env/vault in prod
ENCRYPTION_KEY = settings.PII_ENCRYPTION_KEY or Fernet.generate_key().decode()
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_pii(data: str) -> str:
    if not data:
        return data
    return fernet.encrypt(data.encode()).decode()

def decrypt_pii(token: str) -> str:
    if not token:
        return token
    try:
        return fernet.decrypt(token.encode()).decode()
    except Exception:
        return "[ENCRYPTED_DATA_UNAVAILABLE]"
