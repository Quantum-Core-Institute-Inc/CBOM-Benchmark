#!/usr/bin/env python3
"""Generate the PQC certificates and key files under corpus/pqc/assets/.

  certs/release_root_mldsa.pem    self-signed, ML-DSA-65 key and signature
  certs/firmware_signing.pem      self-signed, ML-DSA-87 key and signature
  certs/migrated_leaf.pem         ML-DSA-65 key, but signed by a classical RSA-3072 CA (not in file)
  keys/kem_recipient_pub.pem      ML-KEM-768 public key (SubjectPublicKeyInfo)
  keys/attestation_signer.pem     ML-DSA-44 private key (PKCS#8)

The hand-written configs in tls/ and ssh/ are not touched. Requires cryptography >= 47.
"""
import datetime as dt
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import mldsa, mlkem, rsa
from cryptography.x509.oid import NameOID

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "pqc" / "assets"
PEM = serialization.Encoding.PEM
START = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)


def name(cn):
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn),
                      x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CBOM Testbench")])


def cert(subject_pub, subject_cn, issuer_key, issuer_cn, hash_alg=None, ca=False, days=397):
    return (x509.CertificateBuilder()
            .subject_name(name(subject_cn)).issuer_name(name(issuer_cn))
            .public_key(subject_pub).serial_number(x509.random_serial_number())
            .not_valid_before(START).not_valid_after(START + dt.timedelta(days=days))
            .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True)
            .sign(issuer_key, hash_alg))


def write(rel, data: bytes):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    print(f"  {p.relative_to(ROOT)}")


def main() -> int:
    print("Generating PQC assets:")
    k = mldsa.MLDSA65PrivateKey.generate()
    write("certs/release_root_mldsa.pem",
          cert(k.public_key(), "CBOM Testbench Release Root", k, "CBOM Testbench Release Root", ca=True, days=3650).public_bytes(PEM))

    k = mldsa.MLDSA87PrivateKey.generate()
    write("certs/firmware_signing.pem",
          cert(k.public_key(), "Firmware Signing 2026", k, "Firmware Signing 2026", days=1825).public_bytes(PEM))

    classical_ca = rsa.generate_private_key(65537, 3072)
    leaf = mldsa.MLDSA65PrivateKey.generate()
    write("certs/migrated_leaf.pem",
          cert(leaf.public_key(), "api-pq.example.internal", classical_ca, "CBOM Testbench Issuing CA 2",
               hashes.SHA256()).public_bytes(PEM))

    k = mlkem.MLKEM768PrivateKey.generate()
    write("keys/kem_recipient_pub.pem",
          k.public_key().public_bytes(PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

    k = mldsa.MLDSA44PrivateKey.generate()
    write("keys/attestation_signer.pem",
          k.private_bytes(PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
