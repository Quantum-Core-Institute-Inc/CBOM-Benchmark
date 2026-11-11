"""cryptokit: the platform's crypto wrapper. Callers name a profile; the profile names the algorithm."""
import hashlib
import hmac
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_PROFILES = Path(__file__).resolve().parents[3] / "config" / "crypto-profiles.json"
_MODES = {"CBC": modes.CBC, "CTR": modes.CTR}
_DIGESTS = {"HmacSHA1": hashlib.sha1, "HmacSHA256": hashlib.sha256, "HmacSHA512": hashlib.sha512}


def _profile(name: str) -> dict:
    return json.loads(_PROFILES.read_text())["profiles"][name]


def seal(profile: str, data: bytes, key: bytes | None = None) -> bytes:
    family, bits, mode = _profile(profile)["cipher"].split("-")
    key = key or os.urandom(int(bits) // 8)
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    body = padder.update(data) + padder.finalize()
    enc = Cipher(algorithms.AES(key), _MODES[mode](iv)).encryptor()
    return iv + enc.update(body) + enc.finalize()


def mac(profile: str, data: bytes, key: bytes = b"platform-webhook-key") -> str:
    digest = _DIGESTS[_profile(profile)["mac"]]
    return hmac.new(key, data, digest).hexdigest()
