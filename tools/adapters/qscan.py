"""Adapter for qScan (@quantakrypto/qscan) CBOM output.

Built against @quantakrypto/qscan. qScan emits CycloneDX CBOM via:

    npx @quantakrypto/qscan . --cbom -o cbom.json

What it emits:
  Cryptographic-asset components with algorithm names, file:line evidence, and
  NIST quantum security levels. Output is deterministic for an unchanged tree.

What the adapter does:
  Passes cryptographic-asset components through. Unlocated algorithms are left
  as-is. Extend _translate if qScan uses non-standard family names or encodes
  HMAC/PBKDF2 differently from the corpus.
"""
from __future__ import annotations

import copy

ADAPTER_VERSION = "0.1"
BUILT_FOR = "qscan (quantakrypto)"


def translate(cdx_bom: dict) -> tuple[dict, list[dict], dict]:
    """-> (bom for the scorer, signals, notes)."""
    bom = copy.deepcopy(cdx_bom)
    notes = {"cryptographic_assets": 0, "unlocated": 0}
    for c in bom.get("components", []):
        if c.get("type") == "cryptographic-asset":
            notes["cryptographic_assets"] += 1
            if not (c.get("evidence") or {}).get("occurrences"):
                notes["unlocated"] += 1
    return bom, [], notes
