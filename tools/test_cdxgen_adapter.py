#!/usr/bin/env python3
"""cdxgen adapter checks (no scanner needed). Run: python tools/test_cdxgen_adapter.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import FAMILIES, iter_crypto_findings  # noqa: E402
from adapters import cdxgen  # noqa: E402


def alg(name, occ):
    return {"type": "cryptographic-asset", "name": name, "bom-ref": name,
            "cryptoProperties": {"assetType": "algorithm", "oid": "1.2.3"}, "evidence": {"occurrences": occ}}


def main() -> int:
    bad = []
    src = {"components": [
        alg("md5", [{"location": "tier1/javascript/a.js", "line": 3, "additionalContext": "hash", "symbol": "node:crypto.createHash"},
                    {"location": "tier2/typescript/b.ts", "line": 7, "additionalContext": "hmac", "symbol": "node:crypto.createHmac"}]),
        alg("sha-512", [{"location": "tier1/javascript/c.js", "line": 5, "additionalContext": "kdf", "symbol": "node:crypto.pbkdf2Sync"}]),
        alg("aes", []),
        {"type": "cryptographic-asset", "name": "telemetry_ecdsa.pem", "bom-ref": "f1",
         "cryptoProperties": {"assetType": "certificate", "algorithmProperties": {}},
         "properties": [{"name": "SrcFile", "value": "/tmp/x/corpus/tier4/assets/keys/telemetry_ecdsa.pem"}]},
    ]}
    bom, signals, notes = cdxgen.translate(src)
    found = sorted((f, tuple(sorted(p.items()))) for f, p, occ, *_ in iter_crypto_findings(bom) if f in FAMILIES and occ)
    want = sorted([("MD5", ()), ("HMAC", (("hash", "MD5"),)), ("PBKDF2", (("hash", "SHA-512"),))])
    if found != want:
        bad.append(f"translated findings {found}, want {want}")
    if any(f == "EC" for f, *_ in iter_crypto_findings(bom)):
        bad.append("a filename was read as an algorithm")
    if signals != [{"category": "crypto-file", "location": "corpus/tier4/assets/keys/telemetry_ecdsa.pem", "line": None, "ref": "f1"}]:
        bad.append(f"crypto-file signal wrong: {signals}")
    if notes != {"renamed_hmac_kdf": 2, "unlocated_algorithms": 1, "crypto_files": 1}:
        bad.append(f"notes {notes}")
    renamed = [c for c in bom["components"] if c["name"].startswith(("HMAC-", "PBKDF2-"))]
    if any("oid" in c["cryptoProperties"] for c in renamed):
        bad.append("the hash's OID stayed on a renamed HMAC/PBKDF2 component")
    for b in bad:
        print("FAIL", b)
    print(f"cdxgen adapter checks: {'all pass' if not bad else f'{len(bad)} failures'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
