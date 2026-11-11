"""Token fingerprints. The digest name is defined in config.settings, not here."""
import hashlib

from config import settings


def fingerprint(token: bytes) -> str:
    h = hashlib.new(settings.TOKEN_DIGEST)
    h.update(token)
    return h.hexdigest()
