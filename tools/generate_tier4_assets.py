#!/usr/bin/env python3
"""Generate the Tier 4 crypto material: certificates, private keys, keystores, SSH keys, JWKS,
and a Kubernetes TLS secret. Every artifact is real and parseable by standard tools.

Key bytes change on every run; the ground truth doesn't depend on them (it records algorithms,
sizes, curves and hashes, which are fixed here). Hand-written configs (nginx.conf, sshd_config,
etc.) are not generated and are not touched by this script.

Requires: cryptography; keytool (JDK) for the JKS truststore.
"""
import pyreq  # noqa: F401  (fails early on an unsupported Python)
import base64
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "tier4" / "assets"
PEM = serialization.Encoding.PEM
DER = serialization.Encoding.DER

warnings.filterwarnings("ignore")  # SHA-1 and 1024-bit keys are the point here


def name(cn: str, org: str = "CBOM Testbench") -> x509.Name:
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn),
                      x509.NameAttribute(NameOID.ORGANIZATION_NAME, org)])


def cert(subject_key, subject_cn, issuer_key=None, issuer_cn=None, hash_alg=hashes.SHA256(),
         ca=False, not_before=dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc), days=397):
    issuer_key = issuer_key or subject_key
    b = (x509.CertificateBuilder()
         .subject_name(name(subject_cn))
         .issuer_name(name(issuer_cn or subject_cn))
         .public_key(subject_key.public_key())
         .serial_number(x509.random_serial_number())
         .not_valid_before(not_before)
         .not_valid_after(not_before + dt.timedelta(days=days))
         .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True))
    if not ca:
        b = b.add_extension(x509.SubjectAlternativeName([x509.DNSName(subject_cn)]), critical=False)
    algo = None if isinstance(issuer_key, ed25519.Ed25519PrivateKey) else hash_alg
    return b.sign(issuer_key, algo)


def _der_len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


SHA256_RSA_OID = bytes.fromhex("06092a864886f70d01010b")  # 1.2.840.113549.1.1.11
SHA1_RSA_OID = bytes.fromhex("06092a864886f70d010105")    # 1.2.840.113549.1.1.5


def resign_sha1(c: x509.Certificate, issuer_key) -> x509.Certificate:
    """cryptography refuses SHA-1 certificate signatures (correctly). Real estates are full of them,
    so: swap the algorithm OID inside the TBSCertificate, sign that with SHA-1, reassemble the DER."""
    from cryptography.hazmat.primitives.asymmetric import padding
    tbs = c.tbs_certificate_bytes
    assert tbs.count(SHA256_RSA_OID) == 1, "expected exactly one sha256WithRSAEncryption OID in TBS"
    tbs = tbs.replace(SHA256_RSA_OID, SHA1_RSA_OID)
    sig = issuer_key.sign(tbs, padding.PKCS1v15(), hashes.SHA1())
    alg_id = b"\x30" + _der_len(len(SHA1_RSA_OID) + 2) + SHA1_RSA_OID + b"\x05\x00"
    bitstr = b"\x03" + _der_len(len(sig) + 1) + b"\x00" + sig
    body = tbs + alg_id + bitstr
    out = x509.load_der_x509_certificate(b"\x30" + _der_len(len(body)) + body)
    out.public_key().verify(out.signature, out.tbs_certificate_bytes, padding.PKCS1v15(), hashes.SHA1()) \
        if out.issuer == out.subject else None
    return out


def write(rel: str, data, mode="wb"):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        p.write_text(data, encoding="utf-8")
    else:
        p.write_bytes(data)
    print(f"  {p.relative_to(ROOT)}")


def b64u(n: int) -> str:
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def main() -> int:
    print("Generating Tier 4 assets:")

    # --- certs/ -------------------------------------------------------------
    k = rsa.generate_private_key(65537, 2048)
    write("certs/api_gateway.pem", cert(k, "api.example.internal").public_bytes(PEM))

    k = rsa.generate_private_key(65537, 1024)
    legacy = resign_sha1(cert(k, "payments-legacy.example.internal",
                              not_before=dt.datetime(2019, 3, 1, tzinfo=dt.timezone.utc), days=1825), k)
    write("certs/payments_legacy.crt", legacy.public_bytes(PEM))

    k = ec.generate_private_key(ec.SECP256R1())
    write("certs/telemetry_ecdsa.pem", cert(k, "telemetry.example.internal").public_bytes(PEM))

    k = ed25519.Ed25519PrivateKey.generate()
    write("certs/device_ed25519.pem", cert(k, "device-7731.example.internal").public_bytes(PEM))

    root_k = rsa.generate_private_key(65537, 4096)
    inter_k = rsa.generate_private_key(65537, 3072)
    leaf_k = ec.generate_private_key(ec.SECP384R1())
    inter = cert(inter_k, "CBOM Testbench Issuing CA 2", root_k, "CBOM Testbench Root CA",
                 hashes.SHA256(), ca=True, days=1825)
    leaf = cert(leaf_k, "portal.example.internal", inter_k, "CBOM Testbench Issuing CA 2", hashes.SHA384())
    write("certs/portal_fullchain.pem", leaf.public_bytes(PEM) + inter.public_bytes(PEM))

    k = rsa.generate_private_key(65537, 4096)
    write("certs/mainframe_gateway.der", cert(k, "mf-gw.example.internal", hash_alg=hashes.SHA512()).public_bytes(DER))

    # --- keys/ --------------------------------------------------------------
    k = rsa.generate_private_key(65537, 3072)
    write("keys/billing_service.pem", k.private_bytes(PEM, serialization.PrivateFormat.PKCS8,
                                                      serialization.NoEncryption()))

    k = ec.generate_private_key(ec.SECP256K1())
    write("keys/treasury_hot_wallet.key", k.private_bytes(PEM, serialization.PrivateFormat.TraditionalOpenSSL,
                                                          serialization.NoEncryption()))

    k = ec.generate_private_key(ec.SECP256R1())
    write("keys/backup_signing_encrypted.pem", k.private_bytes(
        PEM, serialization.PrivateFormat.PKCS8, serialization.BestAvailableEncryption(b"Sup3r-Secret-Backup")))

    rk = rsa.generate_private_key(65537, 2048).public_key().public_numbers()
    ek = ec.generate_private_key(ec.SECP256R1()).public_key().public_numbers()
    jwks = {"keys": [
        {"kty": "RSA", "use": "sig", "alg": "RS256", "kid": "auth-2026-01", "n": b64u(rk.n), "e": b64u(rk.e)},
        {"kty": "EC", "use": "sig", "alg": "ES256", "kid": "auth-2026-02", "crv": "P-256",
         "x": b64u(ek.x).rjust(43, "A"), "y": b64u(ek.y).rjust(43, "A")},
    ]}
    write("keys/jwks.json", json.dumps(jwks, indent=2) + "\n")

    # --- keystores/ ---------------------------------------------------------
    k = rsa.generate_private_key(65537, 2048)
    c = cert(k, "orders.example.internal")
    enc = (serialization.PrivateFormat.PKCS12.encryption_builder()
           .kdf_rounds(10000)
           .key_cert_algorithm(pkcs12.PBES.PBESv2SHA256AndAES256CBC)
           .hmac_hash(hashes.SHA256())
           .build(b"changeit"))
    write("keystores/orders_keystore.p12", pkcs12.serialize_key_and_certificates(b"orders", k, c, None, enc))

    if shutil.which("keytool"):
        ca_k = rsa.generate_private_key(65537, 1024)
        ca = resign_sha1(cert(ca_k, "Legacy Partner Root CA", ca=True,
                              not_before=dt.datetime(2014, 6, 1, tzinfo=dt.timezone.utc), days=7300), ca_k)
        with tempfile.TemporaryDirectory() as td:
            pem = Path(td) / "ca.pem"
            pem.write_bytes(ca.public_bytes(PEM))
            jks = OUT / "keystores" / "partner_truststore.jks"
            jks.unlink(missing_ok=True)
            r = subprocess.run(["keytool", "-importcert", "-noprompt", "-storetype", "JKS",
                                "-keystore", str(jks), "-storepass", "changeit",
                                "-alias", "legacy-partner-root", "-file", str(pem)],
                               capture_output=True, text=True)
            if r.returncode:
                print(r.stderr)
                return 1
        print(f"  {jks.relative_to(ROOT)}")
    else:
        print("  keytool not found: skipped keystores/partner_truststore.jks")

    # --- ssh/ ---------------------------------------------------------------
    k = rsa.generate_private_key(65537, 2048)
    pub = k.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
    write("ssh/ssh_host_rsa_key.pub", pub.decode() + " root@bastion-01\n")

    k = ed25519.Ed25519PrivateKey.generate()
    write("ssh/deploy_id_ed25519", k.private_bytes(PEM, serialization.PrivateFormat.OpenSSH,
                                                   serialization.NoEncryption()))

    # --- k8s/ ---------------------------------------------------------------
    k = ec.generate_private_key(ec.SECP384R1())
    c = cert(k, "ingress.example.internal", hash_alg=hashes.SHA384())
    crt_b64 = base64.b64encode(c.public_bytes(PEM)).decode()
    key_b64 = base64.b64encode(k.private_bytes(PEM, serialization.PrivateFormat.PKCS8,
                                               serialization.NoEncryption())).decode()
    write("k8s/ingress-tls-secret.yaml",
          "apiVersion: v1\nkind: Secret\nmetadata:\n  name: ingress-tls\n  namespace: edge\n"
          f"type: kubernetes.io/tls\ndata:\n  tls.crt: {crt_b64}\n  tls.key: {key_b64}\n")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
