"""Signs JWTs. The algorithm comes from config/app.ini via the DIGESTS table."""
import base64
import configparser
import hmac
import json
from pathlib import Path

from jwtlib.algorithms import DIGESTS

_CFG = configparser.ConfigParser()
_CFG.read(Path(__file__).resolve().parent.parent / "config" / "app.ini")
ALG = _CFG["jwt"]["algorithm"]


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def sign(claims: dict, secret: bytes) -> str:
    header = _b64(json.dumps({"alg": ALG, "typ": "JWT"}).encode())
    body = _b64(json.dumps(claims).encode())
    signing_input = f"{header}.{body}".encode()
    tag = hmac.new(secret, signing_input, DIGESTS[ALG]).digest()
    return f"{header}.{body}.{_b64(tag)}"
