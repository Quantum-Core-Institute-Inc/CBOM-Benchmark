"""Tier 1: message authentication and password-based key derivation, literal parameters."""
import hashlib
import hmac
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

webhook_sig = hmac.new(b"shared-webhook-secret", b"{\"event\":\"paid\"}", hashlib.sha256).hexdigest()

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=os.urandom(16), iterations=600_000)
derived = kdf.derive(b"correct horse battery staple")

if __name__ == "__main__":
    print(webhook_sig, derived.hex())
