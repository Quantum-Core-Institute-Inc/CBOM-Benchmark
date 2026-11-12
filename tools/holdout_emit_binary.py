"""Emit one stripped-binary holdout cell per seed.

The generated file is a tiny ELF-shaped stub that carries algorithm evidence only in
places a source-level scanner misses: a dynsym-style symbol name and a .rodata-style
string. The finding record expects the scanner to recover the family from those
sources or to record a skip.
"""
from __future__ import annotations

from pathlib import Path


def emit_stripped_binary(rng, out_dir: Path) -> dict:
    """Write one stripped-binary stub and return the finding record."""
    family = rng.choice(["MD5", "3DES", "SHA-1", "HMAC-MD5", "AES-256-GCM"])
    symbol = {"MD5": "EVP_md5", "3DES": "EVP_des_ede3_cbc", "SHA-1": "EVP_sha1",
              "HMAC-MD5": "HMAC", "AES-256-GCM": "EVP_aes_256_gcm"}[family]
    # Minimal ELF-shaped stub: magic + symbol name in a data section.
    # Not a real executable; enough for a scanner that reads dynsym/.rodata.
    blob = b"\x7fELF" + b"\x00" * 12 + symbol.encode() + b"\x00" + family.encode() + b"\x00"
    path = out_dir / "holdout-hard" / "stripped.bin"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)
    return {
        "id": f"holdout-bin-{family.lower().replace('-', '')}",
        "file": str(path.relative_to(out_dir.parent) if out_dir.parent.name else path),
        "family": family,
        "tier": 5,
        "lang": "C / OpenSSL",
        "params": {},
        "lines": [],
        "site": False,
        "evidence": ["dynsym", ".rodata"],
    }
