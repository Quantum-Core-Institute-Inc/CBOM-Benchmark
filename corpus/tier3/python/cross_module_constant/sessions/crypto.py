"""Session cookie sealing. Key length comes from config.settings."""
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from config import settings


def seal_cookie(value: bytes) -> bytes:
    aead = AESGCM(os.urandom(settings.SESSION_KEY_BYTES))
    nonce = os.urandom(12)
    return nonce + aead.encrypt(nonce, value, None)
