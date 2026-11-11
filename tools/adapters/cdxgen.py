"""Adapter for cdxgen's CBOM mode (`cbom`, from @cyclonedx/cdxgen), built against 12.9.1.

What cdxgen emits, and what the adapter does with it:

  Algorithms with occurrences (JavaScript/TypeScript, from its AST analysis). Scored as reported,
  with one translation: cdxgen names the *hash* when it finds an HMAC or PBKDF2 call, and says so in
  the occurrence ("additionalContext": "hmac" / "kdf", "symbol": "node:crypto.createHmac"). That is
  an explicit statement, so "md5" in an hmac context becomes "HMAC-MD5", and in a pbkdf2 call
  "PBKDF2-SHA512". The hash's OID is dropped from the renamed component, since it describes the hash.

  Algorithms with no location at all (what it reports for Java and Python here). Left as they are:
  the scorer can't place them in a file, so they count as unlocated, neither credited nor penalized.

  Crypto files ("certificate" entries for every PEM, key, keystore and SSH key file, identified by
  filename, with no algorithm). The filename is not a claim about the algorithm: credited as a
  "crypto-file" signal, like QCI's categories, and renamed so "telemetry_ecdsa.pem" isn't read as EC.
"""
from __future__ import annotations

import copy

from . import common

ADAPTER_VERSION = "1.0"
BUILT_FOR = "cdxgen 12.9.1"


def _crypto_file(fam, f, mat_idx):
    """A file-level detection covers the key and signature findings carried by that file."""
    return mat_idx.get(f["id"], (None, None))[1] in ("key", "signature")


SIGNALS = {"crypto-file": _crypto_file}


def _location_of(c: dict) -> str | None:
    for p in c.get("properties", []):
        if p.get("name") == "SrcFile":
            v = p["value"].replace("\\", "/")
            return "corpus/" + v.split("/corpus/", 1)[1] if "/corpus/" in v else v
    return None


def translate(cdx_bom: dict) -> tuple[dict, list[dict], dict]:
    """-> (bom for the scorer, crypto-file signals, notes: counts of what was translated)."""
    bom = copy.deepcopy(cdx_bom)
    out, signals = [], []
    notes = {"renamed_hmac_kdf": 0, "unlocated_algorithms": 0, "crypto_files": 0}
    for c in bom.get("components", []):
        if c.get("type") != "cryptographic-asset":
            out.append(c)
            continue
        cp = c.get("cryptoProperties") or {}
        occ = (c.get("evidence") or {}).get("occurrences") or []
        if cp.get("assetType") == "certificate" and not cp.get("certificateProperties"):
            loc = _location_of(c)
            notes["crypto_files"] += 1
            if loc:
                signals.append({"category": "crypto-file", "location": loc, "line": None, "ref": c.get("bom-ref")})
            c = {**c, "name": f"cdxgen-file-{notes['crypto_files']}", "evidence": {}}
            out.append(c)
            continue
        if cp.get("assetType") == "algorithm" and not occ:
            notes["unlocated_algorithms"] += 1
            out.append(c)
            continue
        groups = {}
        for o in occ:
            ctx, sym = (o.get("additionalContext") or "").lower(), (o.get("symbol") or "").lower()
            name = c["name"]
            if ctx == "hmac" or "createhmac" in sym:
                name = f"HMAC-{c['name']}"
            elif ctx == "kdf" and "pbkdf2" in sym:
                name = f"PBKDF2-{c['name']}"
            groups.setdefault(name, []).append(o)
        for name, occs in groups.items():
            n = copy.deepcopy(c)
            n["name"] = name
            n["evidence"] = {**(c.get("evidence") or {}), "occurrences": occs}
            if name != c["name"]:
                notes["renamed_hmac_kdf"] += 1
                n["bom-ref"] = f"{c.get('bom-ref', name)}#{name}"
                n.get("cryptoProperties", {}).pop("oid", None)
            out.append(n)
    bom["components"] = out
    md = bom.setdefault("metadata", {}).setdefault("properties", [])
    md.append({"name": "cbom-testbench:adapter", "value": f"cdxgen {ADAPTER_VERSION} (built for {BUILT_FOR})"})
    return bom, signals, notes


def signal_coverage(report: dict, gt: dict, signals: list[dict], mat_idx: dict) -> dict:
    return common.signal_coverage(report, gt, signals, mat_idx, SIGNALS)
