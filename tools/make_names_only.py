#!/usr/bin/env python3
"""reports/reference-names-only.cdx.json: the answer key with everything but names, parameters and
locations stripped (OIDs, primitives, crypto functions, quantum levels, code context, certificate
subject/issuer/validity, library components and every dependency link). It finds everything, so it
shows how much of actionability and linkage is about the fields, not the detection.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP_ALG = {"parameterSetIdentifier", "curve", "mode"}
DROP_CERT = {"subjectName", "issuerName", "notValidBefore", "notValidAfter"}


def strip(bom: dict) -> dict:
    out = {k: v for k, v in bom.items() if k not in ("dependencies",)}
    comps = []
    for c in bom["components"]:
        if c.get("type") != "cryptographic-asset":
            continue
        c = json.loads(json.dumps(c))
        cp = c.get("cryptoProperties") or {}
        cp.pop("oid", None)
        if "algorithmProperties" in cp:
            cp["algorithmProperties"] = {k: v for k, v in cp["algorithmProperties"].items() if k in KEEP_ALG}
        if "certificateProperties" in cp:
            cp["certificateProperties"] = {k: v for k, v in cp["certificateProperties"].items() if k not in DROP_CERT}
        for o in (c.get("evidence") or {}).get("occurrences") or []:
            o.pop("additionalContext", None)
            o.pop("symbol", None)
        comps.append(c)
    out["components"] = comps
    out["metadata"] = {"tools": {"components": [{"type": "application", "name": "cbom-testbench reference, names only"}]}}
    return out


if __name__ == "__main__":
    bom = json.loads((ROOT / "expected" / "expected.cdx.json").read_text())
    (ROOT / "reports" / "reference-names-only.cdx.json").write_text(json.dumps(strip(bom), indent=2) + "\n")
    print("Wrote reports/reference-names-only.cdx.json")
    sys.exit(0)
