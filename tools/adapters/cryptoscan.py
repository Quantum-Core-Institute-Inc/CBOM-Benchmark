"""Adapter for cryptoscan (csnp/cryptoscan) CBOM output.

Built against cryptoscan v1.5.0. cryptoscan emits CycloneDX 1.6 CBOM via:

    cryptoscan scan . --format cbom --output cbom.json

What it emits:
  Cryptographic-asset components with algorithm names and, when available, file
  locations. Parameter recovery varies; many findings are names-only.

What the adapter does:
  Passes cryptographic-asset components through. Unlocated algorithms are left
  as-is (the scorer treats them as unlocated). No renaming is applied yet;
  extend _translate if cryptoscan uses non-standard family names.
"""
from __future__ import annotations

import copy

ADAPTER_VERSION = "0.1"
BUILT_FOR = "cryptoscan 1.5.0"


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
