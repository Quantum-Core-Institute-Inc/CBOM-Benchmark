#!/usr/bin/env python3
"""Policy regression tests. Each case pins a verdict to the document it comes from, so editing a
policy file can't silently move a deadline. Run: python tools/test_policy.py"""
import copy
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import load_json  # noqa: E402
from policy import bucket, evaluate, load_policy  # noqa: E402

NIST, EO, CNSA = (load_policy(p) for p in ("nist", "eo14412-hva", "cnsa2"))

# (policy, family, params, use, primitive, expected status, expected disallowed_after, why)
CASES = [
    # NIST IR 8547 final: all quantum-vulnerable public key, any size: deprecated after 2030, disallowed after 2035
    (NIST, "RSA", {"key_size": 2048}, "custom", None, "deprecated", "2035-12-31", "IR 8547 final"),
    (NIST, "RSA", {"key_size": 4096}, "custom", None, "deprecated", "2035-12-31", "IR 8547 final: no size exemption"),
    (NIST, "EC", {"curve": "P-384"}, "custom", None, "deprecated", "2035-12-31", "IR 8547 final"),
    (NIST, "Ed25519", {}, "custom", None, "deprecated", "2035-12-31", "IR 8547 final: EdDSA included"),
    (NIST, "X25519", {}, "custom", None, "deprecated", "2035-12-31", "IR 8547 final: ECDH"),
    (NIST, "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256", {}, "web", None, "deprecated", "2035-12-31", "classical key exchange"),
    # SP 800-131A Rev. 2, FIPS 186-5, SHA-1 2030
    (NIST, "RSA", {"key_size": 1024}, "custom", None, "disallowed", "2013-12-31", "below 112-bit"),
    (NIST, "DSA", {"key_size": 2048}, "custom", None, "disallowed", "2023-02-03", "FIPS 186-5"),
    (NIST, "3DES", {}, "custom", None, "disallowed", "2023-12-31", "TDEA encryption"),
    (NIST, "SHA-1", {}, "custom", None, "deprecated", "2030-12-31", "NIST Dec 2022"),
    (NIST, "HMAC", {"hash": "SHA-1"}, "custom", None, "deprecated", "2030-12-31", "all SHA-1 uses"),
    (NIST, "MD5", {}, "custom", None, "not-approved", None, "never approved"),
    (NIST, "EC", {"curve": "secp256k1"}, "custom", None, "review", None, "SP 800-186: blockchain-related use only"),
    (NIST, "TLS-1.1", {}, "web", None, "review", None, "SP 800-52 Rev. 2 Sec. 3.1: interoperability only"),
    (NIST, "SSL-3.0", {}, "web", None, "not-approved", None, "SP 800-52 Rev. 2 Sec. 3.1: shall not be used"),
    (NIST, "ChaCha20-Poly1305", {}, "custom", None, "not-approved", None, "not FIPS-approved"),
    (NIST, "AES", {"key_size": 128, "mode": "ECB"}, "custom", None, "approved", None, "131A Rev. 3 is still a draft"),
    (NIST, "ML-KEM", {"param_set": "512"}, "custom", None, "approved", None, "FIPS 203, all sets"),
    (NIST, "X25519MLKEM768", {}, "web", None, "approved", None, "SP 800-56C hybrid"),
    # EO 14412: HVAs, key establishment 2030, signatures 2031; stricter of overlay and NIST wins
    (EO, "X25519", {}, "web", None, "deprecated", "2030-12-31", "Sec. 4(b)(ii)"),
    (EO, "RSA", {"key_size": 3072}, "custom", "pke", "deprecated", "2030-12-31", "key establishment"),
    (EO, "RSA", {"key_size": 3072}, "custom", "signature", "deprecated", "2031-12-31", "Sec. 4(b)(iii)"),
    (EO, "Ed25519", {}, "custom", None, "deprecated", "2031-12-31", "signature-only family"),
    (EO, "DSA", {"key_size": 2048}, "custom", None, "disallowed", "2023-02-03", "inherited NIST date is stricter"),
    (EO, "RSA", {"key_size": 1024}, "custom", None, "disallowed", "2013-12-31", "inherited NIST date is stricter"),
    (EO, "MD5", {}, "custom", None, "not-approved", None, "falls through to NIST"),
    # CNSA 2.0: only AES-256, ML-KEM-1024, ML-DSA-87, SHA-384/512; CNSA 1.0 until the use's exclusive date
    (CNSA, "ML-KEM", {"param_set": "1024"}, "web", None, "approved", None, "CNSA 2.0 list"),
    (CNSA, "ML-KEM", {"param_set": "768"}, "web", None, "not-approved", None, "wrong level"),
    (CNSA, "ML-DSA", {"param_set": "65"}, "web", None, "not-approved", None, "wrong level"),
    (CNSA, "AES", {"key_size": 128}, "custom", None, "not-approved", None, "AES-256 only"),
    (CNSA, "RSA", {"key_size": 3072}, "web", None, "deprecated", "2033-12-31", "web/cloud exclusive 2033"),
    (CNSA, "RSA", {"key_size": 3072}, "firmware-signing", None, "deprecated", "2030-12-31", "signing exclusive 2030"),
    (CNSA, "EC", {"curve": "P-384"}, "networking", None, "deprecated", "2030-12-31", "networking exclusive 2030"),
    (CNSA, "EC", {"curve": "P-256"}, "web", None, "not-approved", None, "never CNSA 1.0"),
    (CNSA, "SHA-256", {}, "custom", None, "not-approved", None, "SHA-384/512 only"),
    (CNSA, "SecP384r1MLKEM1024", {}, "web", None, "review", None, "program-office call"),
    (CNSA, "TLS-1.3", {}, "web", None, "out-of-scope", None, "algorithms, not protocols"),
]


PRIMARY_HOSTS = ("csrc.nist.gov", "nvlpubs.nist.gov", "media.defense.gov", "www.nsa.gov", "www.whitehouse.gov")


def provenance_problems() -> list[str]:
    """Every rule cites a final, primary source by id, with the section that supports it."""
    import json
    from urllib.parse import urlparse
    out = []
    for p in sorted((Path(__file__).resolve().parent.parent / "policies").glob("*.json")):
        pol = json.loads(p.read_text())
        srcs = {s["id"]: s for s in pol["sources"]}
        for s in pol["sources"]:
            for k in ("name", "revision", "status", "published", "url"):
                if not s.get(k):
                    out.append(f"{p.name}: source {s['id']} has no {k}")
            if s.get("url") and urlparse(s["url"]).hostname not in PRIMARY_HOSTS:
                out.append(f"{p.name}: source {s['id']} links to {urlparse(s['url']).hostname}, not a primary publisher")
        for r in pol["rules"]:
            cites = [(r.get("source"), r.get("section"), True)] + [(a.get("source"), a.get("section"), False) for a in r.get("also", [])]
            for sid, sec, main_cite in cites:
                if sid not in srcs:
                    out.append(f"{p.name}: rule {r['id']} cites unknown source {sid}")
                    continue
                if not sec:
                    out.append(f"{p.name}: rule {r['id']} cites {sid} without a section")
                if main_cite and srcs[sid]["status"] != "final":
                    out.append(f"{p.name}: rule {r['id']} rests on {sid}, which is a {srcs[sid]['status']}")
    return out


def main() -> int:
    bad = 0
    for problem in provenance_problems():
        bad += 1
        print(f"FAIL provenance: {problem}")
    for pol, fam, prm, use, prim, status, date, why in CASES:
        v = evaluate(pol, fam, prm, use, prim)
        if v["status"] != status or v.get("disallowed_after") != date:
            bad += 1
            print(f"FAIL {pol['id']} {fam} {prm} use={use}: got {v['status']} {v.get('disallowed_after')}, "
                  f"want {status} {date} ({why})")

    # Buckets around the boundaries.
    v = evaluate(NIST, "SHA-1", {})
    for as_of, want in ((dt.date(2026, 11, 10), "by-2030"), (dt.date(2031, 1, 1), "now")):
        if bucket(v, as_of) != want:
            bad += 1
            print(f"FAIL bucket SHA-1 as of {as_of}: {bucket(v, as_of)} != {want}")

    # Deadline weighting: missing an overdue finding must cost more than missing an approved one.
    from score import score
    ref = load_json(Path(__file__).resolve().parent.parent / "expected" / "expected.cdx.json")
    a, b = copy.deepcopy(ref), copy.deepcopy(ref)
    a["components"] = [c for c in a["components"] if c["bom-ref"] != "T1-PY-01"]  # MD5: due now
    b["components"] = [c for c in b["components"] if c["bom-ref"] != "T1-PY-03"]  # SHA-256: approved
    wa, wb = score(a)["deadlines"]["weighted_recall"], score(b)["deadlines"]["weighted_recall"]
    if not wa < wb:
        bad += 1
        print(f"FAIL weighting: missing MD5 ({wa}) should cost more than missing SHA-256 ({wb})")
    if score(a)["deadlines"]["missed_due_by_2030"][0]["id"] != "T1-PY-01":
        bad += 1
        print("FAIL: missed MD5 not listed among findings due by 2030")

    total = len(CASES) + 4
    print(f"{total - bad}/{total} policy checks pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
