"""Dead code: crypto that ships in the package and never runs."""
import hashlib

from cryptography.hazmat.primitives.asymmetric import rsa

LEGACY_EXPORT = False


def _old_fingerprint(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def export_key():
    if LEGACY_EXPORT:
        return rsa.generate_private_key(public_exponent=65537, key_size=1024)
    return None


if __name__ == "__main__":
    print(export_key())
