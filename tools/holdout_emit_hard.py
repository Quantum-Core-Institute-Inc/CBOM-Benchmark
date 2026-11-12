"""Emit one hard holdout cell per seed: a minified-JS bundle with hoisted constants.

This is the first concrete emission for the cells documented in holdout_hard_cells.py.
The generator can import and call emit_minified_js(rng, out_dir) to drop a single
file into the holdout corpus. Full coverage of stripped binaries and LMS/XMSS OID
cells follows the same pattern.
"""
from __future__ import annotations

import json
from pathlib import Path


def emit_minified_js(rng, out_dir: Path) -> dict:
    """Write one minified JS file and return the finding record.

    The algorithm name is a hoisted one-letter constant two hops from the call,
    matching the shape of the published Tier 5 minified bundles.
    """
    family = rng.choice(["SHA-1", "HMAC-MD5", "AES-256-GCM"])
    const = rng.choice(list("abcdefghijklmnopqrstuvwxyz"))
    call = {"SHA-1": "createHash", "HMAC-MD5": "createHmac", "AES-256-GCM": "createCipheriv"}[family]
    arg = {"SHA-1": '"sha1"', "HMAC-MD5": '"md5"', "AES-256-GCM": '"aes-256-gcm"'}[family]
    body = f"var {const}={arg};function s(t){{return require('crypto').{call}({const},t)}}module.exports=s;"
    path = out_dir / "holdout-hard" / "minified.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return {
        "id": f"holdout-minjs-{family.lower().replace('-', '')}",
        "file": str(path.relative_to(out_dir.parent) if out_dir.parent.name else path),
        "family": family,
        "tier": 5,
        "lang": "JavaScript / TypeScript",
        "params": {},
        "lines": [1],
        "site": True,
    }
