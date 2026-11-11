"""Tier 2: digest picked from an environment variable with a hardcoded default."""
import os

from cryptography.hazmat.primitives import hashes

DIGEST_NAME = os.environ.get("APP_DIGEST", "SHA1")


def audit_digest(record: bytes) -> bytes:
    h = hashes.Hash(getattr(hashes, DIGEST_NAME)())
    h.update(record)
    return h.finalize()


if __name__ == "__main__":
    print(audit_digest(b"audit-row-1182").hex())
