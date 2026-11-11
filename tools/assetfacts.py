"""Read ground-truth facts out of the real certificates and keys in the corpus.

Actionability scoring checks that a scanner reported the *right* expiry date and subject, not just
that it filled the fields in. Those right answers come from here, read from the files themselves at
build time, so regenerating the keys and certificates never leaves the answer key stale.
"""
from __future__ import annotations

import base64
import re
import shutil
import subprocess
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed25519, rsa
from cryptography.hazmat.primitives.serialization import pkcs12

from cbomlib import _curve, normalize

KEYSTORE_PASSWORD = b"changeit"


def _load_certs(path: Path) -> list[x509.Certificate]:
    data = path.read_bytes()
    if path.suffix == ".der":
        return [x509.load_der_x509_certificate(data)]
    if path.suffix == ".p12":
        _, cert, extra = pkcs12.load_key_and_certificates(data, KEYSTORE_PASSWORD)
        return [c for c in [cert, *(extra or [])] if c is not None]
    if path.suffix == ".jks":
        if not shutil.which("keytool"):
            return []
        aliases = re.findall(r"^Alias name: (.+)$", subprocess.run(
            ["keytool", "-list", "-v", "-keystore", str(path), "-storepass", KEYSTORE_PASSWORD.decode()],
            capture_output=True, text=True).stdout, re.M)
        out = []
        for a in aliases:
            pem = subprocess.run(["keytool", "-exportcert", "-rfc", "-alias", a, "-keystore", str(path),
                                  "-storepass", KEYSTORE_PASSWORD.decode()], capture_output=True, text=True).stdout
            out += x509.load_pem_x509_certificates(pem.encode()) if "BEGIN CERTIFICATE" in pem else []
        return out
    if path.suffix in (".yaml", ".yml"):
        m = re.search(r"tls\.crt:\s*(\S+)", path.read_text())
        return x509.load_pem_x509_certificates(base64.b64decode(m.group(1))) if m else []
    return x509.load_pem_x509_certificates(data)


def _key_identity(cert: x509.Certificate) -> tuple[str, dict]:
    k = cert.public_key()
    if isinstance(k, rsa.RSAPublicKey):
        return "RSA", {"key_size": k.key_size}
    if isinstance(k, dsa.DSAPublicKey):
        return "DSA", {"key_size": k.key_size}
    if isinstance(k, ec.EllipticCurvePublicKey):
        return "EC", {"curve": _curve(k.curve.name)}
    if isinstance(k, ed25519.Ed25519PublicKey):
        return "Ed25519", {}
    return normalize(type(k).__name__.replace("PublicKey", ""))  # ML-DSA keys: "MLDSA65" -> ML-DSA 65


def _iso(d) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def certificate_facts(path: Path, key_family: str, key_params: dict) -> dict | None:
    """Facts for the certificate in `path` whose public key matches the given family and params."""
    for c in _load_certs(path):
        fam, params = _key_identity(c)
        if fam == key_family and all(params.get(k) == v for k, v in key_params.items()):
            cn = c.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
            return {"subject": c.subject.rfc4514_string(), "issuer": c.issuer.rfc4514_string(),
                    "subject_cn": cn[0].value if cn else None,
                    "not_before": _iso(c.not_valid_before_utc), "not_after": _iso(c.not_valid_after_utc),
                    "sig_oid": c.signature_algorithm_oid.dotted_string}
    return None


def key_format(path: Path) -> str | None:
    head = path.read_text(errors="ignore")[:120]
    for marker, fmt in (("BEGIN OPENSSH PRIVATE KEY", "OpenSSH"), ("BEGIN EC PRIVATE KEY", "SEC1 PEM"), ("BEGIN RSA PRIVATE KEY", "PKCS#1 PEM"),
                        ("BEGIN ENCRYPTED PRIVATE KEY", "PKCS#8 PEM (encrypted)"), ("BEGIN PRIVATE KEY", "PKCS#8 PEM"),
                        ("BEGIN PUBLIC KEY", "SPKI PEM"), ("ssh-", "OpenSSH public key"), ('"keys"', "JWK")):
        if marker in head:
            return fmt
    return None
