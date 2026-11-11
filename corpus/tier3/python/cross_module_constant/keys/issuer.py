"""Issues partner signing keys. Key size lives in config.settings."""
from cryptography.hazmat.primitives.asymmetric import rsa

from config import settings


def issue_partner_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=settings.SIGNING_KEY_BITS)
