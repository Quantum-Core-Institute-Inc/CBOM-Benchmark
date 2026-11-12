"""Adapter for qScan (@quantakrypto/qscan) CBOM output.

Checked against qScan 0.12.0 run by .github/workflows/third-party-scanners.yml:

    qscan <dir> --cbom -o cbom.json

What it emits:
  One CycloneDX 1.6 cryptographic-asset component per algorithm, with every place it was seen
  listed under evidence.occurrences. The component name carries the primitive in parentheses:
  "DH (key-agree)", "DSA (signature)", "ECDH (key-agree)".

What the adapter does, and nothing else:
  Removes that parenthesised primitive from the name ("DH (key-agree)" -> "DH"), because the
  scorer's normalizer reads names and has no family called "DH (key-agree)". The primitive is
  already in cryptoProperties.algorithmProperties.primitive, so nothing is lost. Without this the
  scanner scores zero recall on a corpus where it reports real findings.
"""
from __future__ import annotations

import copy
import re

ADAPTER_VERSION = "0.2"
BUILT_FOR = "qscan 0.12.0"
_SUFFIX = re.compile(r"\s*\((?:[a-z][a-z0-9-]*)\)\s*$")


def translate(cdx_bom: dict) -> tuple[dict, list[dict], dict]:
    """-> (bom for the scorer, signals, notes)."""
    bom = copy.deepcopy(cdx_bom)
    notes = {"cryptographic_assets": 0, "unlocated": 0, "renamed": {}}
    for c in bom.get("components", []):
        if c.get("type") != "cryptographic-asset":
            continue
        notes["cryptographic_assets"] += 1
        if not (c.get("evidence") or {}).get("occurrences"):
            notes["unlocated"] += 1
        name = c.get("name") or ""
        short = _SUFFIX.sub("", name)
        if short and short != name:
            notes["renamed"][name] = short
            c["name"] = short
    return bom, [], notes
