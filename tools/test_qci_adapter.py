#!/usr/bin/env python3
"""QCI adapter regression tests (no scanner needed). Run: python tools/test_qci_adapter.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import FAMILIES, iter_crypto_findings, normalize  # noqa: E402
from adapters import qci_pqc  # noqa: E402


def comp(name, line=3, loc="tier1/python/x.py"):
    return {"type": "cryptographic-asset", "name": name, "bom-ref": f"r-{name}",
            "cryptoProperties": {"assetType": "algorithm",
                                 "algorithmProperties": {"primitive": "key-agree", "parameterSetIdentifier": name}},
            "evidence": {"occurrences": [{"location": loc, "line": line}]}}


def main() -> int:
    bad = []
    cats = sorted(set(qci_pqc.SIGNALS) | qci_pqc.NOT_MODELED)
    bom, signals, unmapped = qci_pqc.translate({"components": [comp(n) for n in cats + ["Brand-New-Thing"]]})
    found = [f for f in iter_crypto_findings(bom) if f[0] in FAMILIES]
    if found:
        bad.append(f"categories leaked into the strict score: {[f[0] for f in found]}")
    if unmapped != ["Brand-New-Thing"]:
        bad.append(f"unmapped should list only the unknown name, got {unmapped}")
    if len(signals) != len(qci_pqc.SIGNALS):
        bad.append(f"expected one signal per category, got {len(signals)}")
    kept = {p["value"] for c in bom["components"] for p in c.get("properties", []) if p["name"] == "qci:category"}
    if kept != set(cats + ["Brand-New-Thing"]):
        bad.append("original category names not preserved as qci:category properties")
    for q, tb in qci_pqc.EXACT.items():
        if normalize(tb, {})[0] not in FAMILIES:
            bad.append(f"EXACT {q} -> {tb} is not a known testbench family")
    exact_bom, _, _ = qci_pqc.translate({"components": [comp("ML-KEM-768"), comp("Kyber-prestandard", 4)]})
    fams = sorted(f[0] for f in iter_crypto_findings(exact_bom))
    if fams != ["ML-KEM", "ML-KEM"]:
        bad.append(f"exact names should score as ML-KEM, got {fams}")
    for b in bad:
        print("FAIL", b)
    print(f"{5 - len(bad)}/5 adapter checks pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
