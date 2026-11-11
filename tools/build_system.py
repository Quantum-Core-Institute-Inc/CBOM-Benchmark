#!/usr/bin/env python3
"""Build the generated parts of the system fixture (corpus/system/payments-platform).

  * edge/nginx/tls/gateway.crt + gateway.key   RSA-2048, sha256WithRSAEncryption
  * deploy/k8s/gateway-ingress-tls.yaml          a kubernetes.io/tls Secret, EC P-384, ecdsa-with-SHA384
  * services/settlement-worker/partner_ca.py     a partner CA certificate embedded in source,
                                                 RSA-1024, sha1WithRSAEncryption
  * services/api-gateway/bin/api-gateway         the gateway, built for linux/amd64, stripped
  * services/ledger-service/build/libs/ledger-service.jar   ledger + cryptokit classes, no debug info

Key bytes change on every run; the answer key records algorithms, sizes, curves and hashes, which
are fixed here, and certificate facts are read back from the files at build time (assetfacts.py).
The binary and the jar are rebuilt from the source in the fixture; `--artifacts-only` skips the keys.

Requires: cryptography, Go 1.24+, a JDK (javac, jar).
"""
import pyreq  # noqa: F401
import argparse
import base64
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cryptography.hazmat.primitives import hashes, serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec, rsa  # noqa: E402

import generate_tier4_assets as g4  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "corpus" / "system" / "payments-platform"
PEM = serialization.Encoding.PEM


def keys() -> None:
    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    c = g4.cert(k, "api.payments.example", hash_alg=hashes.SHA256())
    (SYS / "edge/nginx/tls/gateway.crt").write_bytes(c.public_bytes(PEM))
    (SYS / "edge/nginx/tls/gateway.key").write_bytes(k.private_bytes(PEM, serialization.PrivateFormat.TraditionalOpenSSL,
                                                                      serialization.NoEncryption()))
    ek = ec.generate_private_key(ec.SECP384R1())
    ec_cert = g4.cert(ek, "api.payments.example", hash_alg=hashes.SHA384())
    crt = base64.b64encode(ec_cert.public_bytes(PEM)).decode()
    key = base64.b64encode(ek.private_bytes(PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())).decode()
    (SYS / "deploy/k8s/gateway-ingress-tls.yaml").write_text(
        "apiVersion: v1\nkind: Secret\nmetadata:\n  name: gateway-ingress-tls\n  namespace: payments\n"
        f"type: kubernetes.io/tls\ndata:\n  tls.crt: {crt}\n  tls.key: {key}\n")
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
    ca = g4.resign_sha1(g4.cert(ca_key, "Northwind Bank Partner CA", ca=True, days=3650), ca_key)
    (SYS / "services/settlement-worker/partner_ca.py").write_text(
        '"""The partner bank\'s private CA. Pinned here because their endpoint isn\'t in the public trust store."""\n\n'
        f'PARTNER_CA_PEM = """\\\n{ca.public_bytes(PEM).decode()}"""\n')
    print("  keys and certificates written")


def artifacts() -> None:
    env = {"CGO_ENABLED": "0", "GOOS": "linux", "GOARCH": "amd64", "GOFLAGS": "-trimpath", "GOTOOLCHAIN": "local"}
    out = SYS / "services/api-gateway/bin/api-gateway"
    r = subprocess.run(["go", "build", "-buildvcs=false", "-ldflags=-s -w -buildid=", "-o", str(out), "./services/api-gateway"],
                       cwd=SYS, capture_output=True, text=True, env={**__import__("os").environ, **env})
    if r.returncode:
        raise SystemExit(r.stderr)
    with tempfile.TemporaryDirectory() as tmp:
        srcs = [str(p) for p in (SYS / "libs/cryptokit/java").rglob("*.java")] + \
               [str(p) for p in (SYS / "services/ledger-service/src").rglob("*.java")]
        r = subprocess.run(["javac", "-g:none", "--release", "21", "-d", tmp, *srcs], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stderr)
        jar = SYS / "services/ledger-service/build/libs/ledger-service.jar"
        jar.unlink(missing_ok=True)
        r = subprocess.run(["jar", "--create", "--date=2026-01-01T00:00:00Z", "--file", str(jar),
                            "--main-class", "com.acme.ledger.LedgerService", "-C", tmp, "."], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stderr)
    print("  api-gateway binary and ledger-service.jar built")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artifacts-only", action="store_true")
    a = ap.parse_args()
    if not a.artifacts_only:
        keys()
    if not shutil.which("go") or not shutil.which("javac"):
        raise SystemExit("needs go and javac")
    artifacts()
    return 0


if __name__ == "__main__":
    sys.exit(main())
