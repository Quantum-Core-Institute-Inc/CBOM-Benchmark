"""Hard holdout cells: minified JS, stripped binaries, LMS/XMSS pure-Python and OID-only.

These cells are planned for generator 1.3. They are not yet emitted by tools/holdout.py.
This module documents the expected shape so the generator can grow them without changing
the published answer key.

Cells
-----
minified_js
    One-line JavaScript bundles with hoisted one-letter constants and destructured crypto
    calls. Algorithm names never appear as string literals at the call site.

stripped_binary
    ELF / Go binaries where evidence is dynsym symbols, .rodata strings, or immediate
    operands. No source in the generated corpus.

lms_pure_python
    RFC 8554-style LMS signing/verification on hashlib alone. No API call names the scheme.

lms_oid_only / xmss_oid_only
    Public keys recognisable only by OID. No algorithm name in the file.
"""
from __future__ import annotations

HARD_CELLS = {
    "minified_js": {
        "description": "One-line JS with hoisted constants and destructured crypto calls",
        "evidence": ["hoisted one-letter constants", "destructured createCipheriv / createHash"],
        "families": ["SHA-1", "HMAC-MD5", "3DES-CBC", "AES-256-GCM", "P-256", "Ed25519"],
    },
    "stripped_binary": {
        "description": "Stripped ELF / Go; evidence in dynsym, .rodata, or immediate operands",
        "evidence": ["dynsym symbols", ".rodata strings", "immediate operands"],
        "families": ["MD5", "3DES", "SHA-1", "HMAC-MD5", "AES-256-GCM", "RSA", "P-256"],
    },
    "lms_pure_python": {
        "description": "RFC 8554 LMS on hashlib alone; no API call names the scheme",
        "evidence": ["parameter-set constants", "code shape"],
        "families": ["LMS"],
    },
    "lms_oid_only": {
        "description": "HSS/LMS public key recognisable only by OID",
        "evidence": ["OID 1.2.840.113549.1.9.16.3.17"],
        "families": ["LMS"],
    },
    "xmss_oid_only": {
        "description": "XMSS public key recognisable only by OID",
        "evidence": ["OID 0.4.0.127.0.15.1.1.13.0"],
        "families": ["XMSS"],
    },
}


def cell_names() -> list[str]:
    return list(HARD_CELLS)
