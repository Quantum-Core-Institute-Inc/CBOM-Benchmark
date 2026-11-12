"""Emit one LMS or XMSS OID-only holdout cell per seed.

The generated file is a PEM-shaped public key that contains only the OID. No algorithm
name appears in the file. A scanner must recognise the OID to report the family.
"""
from __future__ import annotations

from pathlib import Path

OIDS = {
    "LMS": "1.2.840.113549.1.9.16.3.17",          # id-alg-hss-lms-hashsig (RFC 8708)
    "XMSS": "1.3.6.1.5.5.7.6.34",                 # id-alg-xmss (RFC 9802)
}


def emit_oid_only(rng, out_dir: Path) -> dict:
    """Write one OID-only public key and return the finding record."""
    family = rng.choice(list(OIDS))
    oid = OIDS[family]
    body = f"-----BEGIN PUBLIC KEY-----\n{oid}\n-----END PUBLIC KEY-----\n"
    path = out_dir / "holdout-hard" / f"{family.lower()}_oid.pem"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return {
        "id": f"holdout-oid-{family.lower()}",
        "file": str(path.relative_to(out_dir.parent) if out_dir.parent.name else path),
        "family": family,
        "tier": "pqc",
        "lang": "assets",
        "params": {},
        "lines": [],
        "site": False,
        "evidence": [f"OID {oid}"],
    }
