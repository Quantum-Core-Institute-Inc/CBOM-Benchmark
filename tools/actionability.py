"""Actionability: could an engineer open a migration ticket from what the scanner reported?

Detection says a scanner found something. This module checks the fields it reported for each
detected finding against rubric/actionability.json: must-haves (no ticket without them) and
should-haves (the ticket bounces back without them). Facts are checked for correctness where the
corpus knows the answer: a certificate's expiry and subject are compared with the real file.
"""
from __future__ import annotations

import json
from pathlib import Path

from cbomlib import FAMILIES, expected_quantum_level, normalize, oid_for

ROOT = Path(__file__).resolve().parent.parent
RUBRIC = ROOT / "rubric" / "actionability.json"
CODE_SUFFIXES = (".py", ".java")
COMPILED_SUFFIXES = (".pyc", ".jar")

# Primitives a scanner may reasonably report for each family.
COMPATIBLE = {
    "AES": {"block-cipher", "ae"}, "DES": {"block-cipher"}, "3DES": {"block-cipher"}, "TEA": {"block-cipher"},
    "RC4": {"stream-cipher"}, "ChaCha20-Poly1305": {"ae", "stream-cipher"},
    "RSA": {"pke", "signature", "kem"}, "DSA": {"signature"}, "EC": {"signature", "key-agree"},
    "DH": {"key-agree"}, "Ed25519": {"signature"}, "X25519": {"key-agree"},
    "HMAC": {"mac"}, "PBKDF2": {"kdf"}, "ML-KEM": {"kem"}, "ML-DSA": {"signature"}, "SLH-DSA": {"signature"},
}


AMBIGUOUS_PRIMITIVE = {"RSA", "EC"}


def load_rubric() -> dict:
    r = json.loads(RUBRIC.read_text(encoding="utf-8"))
    r["checks"] = [c for c in r["checks"] if c.get("enabled", True)]
    return r


def _compatible(family: str) -> set:
    if family in COMPATIBLE:
        return COMPATIBLE[family]
    meta = FAMILIES.get(family, {})
    if meta.get("hybrid"):
        return {"kem", "key-agree"}
    return {meta.get("primitive")} if meta.get("primitive") else set()


def _ap(ctx) -> dict:
    return (((ctx.get("via") or {}).get("cryptoProperties") or {}).get("algorithmProperties")) or {}


def _cp(component) -> dict:
    return (component or {}).get("cryptoProperties") or {}


def material_index(gt: dict) -> dict:
    """finding id -> (material, role) for findings that come from a certificate or key file."""
    by_id = {f["id"]: f for f in gt["findings"]}
    idx = {}
    for m in gt.get("materials", []):
        k = by_id.get(m["key"])
        if k is None:
            continue
        idx[k["id"]] = (m, "key")
    for m in gt.get("materials", []):
        if m["kind"] != "certificate":
            continue
        sig_fam, sig_params = normalize(m["sig_alg"])
        derived = {sig_fam, sig_params.get("hash")} - {None}
        for f in gt["findings"]:
            if f["file"] == m["file"] and f["id"] not in idx and f["family"] in derived:
                idx[f["id"]] = (m, "signature")
    return idx


def _cn(dn: str | None) -> str | None:
    """Common name out of an RFC 4514 string ('O=Acme,CN=Issuing CA' -> 'Issuing CA')."""
    for part in (dn or "").split(","):
        if part.strip().upper().startswith("CN="):
            return part.strip()[3:]
    return None


def _fmt(v) -> str:
    """Key formats compared loosely on spelling: 'PKCS#8 PEM' == 'pkcs8-pem' == 'PKCS8 (PEM)'."""
    import re
    return re.sub(r"[^a-z0-9]", "", str(v or "").lower())


def assess(f: dict, r: dict, entries: list[dict], mat: tuple | None) -> dict:
    """Return {check_id: True | False | None (not applicable)} for one detected finding.

    f: ground-truth finding; r: its scoring result (line_ok, params_ok, ...);
    entries: the scanner items matched to it, each {"ctx", "params", "lines", "path"}."""
    fam = f["family"]
    meta = FAMILIES.get(fam, {})
    is_proto, is_suite = bool(meta.get("protocol")), bool(meta.get("suite"))
    material, role = mat if mat else (None, None)
    cert = material if material and material["kind"] == "certificate" else None
    keymat = material if material and material["kind"] != "certificate" and role == "key" else None
    # A certificate or key embedded in a source file is still an asset, judged on asset fields.
    code = f["file"].endswith(CODE_SUFFIXES) and not mat
    algorithmic = not (is_proto or is_suite) and role != "signature"
    ctxs = [e["ctx"] for e in entries]
    out = {}

    out["location"] = bool(r["line_ok"]) if (code and f.get("lines")) else bool(r["at_usage_site"])
    out["parameters"] = bool(r["params_ok"]) if f["params"] else None
    # Only where the family alone doesn't say what it's for: an RSA key may be key transport (replace
    # with ML-KEM) or signing (replace with ML-DSA); EC may be ECDH or ECDSA. For AES or SHA-256 the
    # name already answers it, so requiring the field there would be pedantry.
    out["primitive"] = (any(_ap(c).get("primitive") in _compatible(fam) for c in ctxs)
                        if algorithmic and fam in AMBIGUOUS_PRIMITIVE else None)

    if cert:
        facts = cert.get("facts") or {}
        cps = [_cp(c["asset"]).get("certificateProperties") or {} for c in ctxs if c["kind"] == "certificate"]

        def expiry_ok(cp):
            got = str(cp.get("notValidAfter") or "")
            return bool(got) and (not facts.get("not_after") or got[:10] == facts["not_after"][:10])

        def subject_ok(cp):
            got = str(cp.get("subjectName") or "")
            return bool(got) and (not facts.get("subject_cn") or facts["subject_cn"] in got)

        out["cert_expiry"] = any(expiry_ok(cp) for cp in cps)
        out["cert_subject"] = any(subject_ok(cp) for cp in cps)
        # Values, not presence: the issuer must name the real issuer, the start date must be the real one.
        def issuer_ok(cp):
            got = str(cp.get("issuerName") or "")
            want = _cn(facts.get("issuer"))
            return bool(got) and (not want or want in got)

        def start_ok(cp):
            got = str(cp.get("notValidBefore") or "")
            return bool(got) and (not facts.get("not_before") or got[:10] == facts["not_before"][:10])

        out["cert_issuer"] = any(issuer_ok(cp) for cp in cps)
        out["cert_validity_start"] = any(start_ok(cp) for cp in cps)
        out["cert_refs"] = any(cp.get("subjectPublicKeyRef") and cp.get("signatureAlgorithmRef") for cp in cps)
    else:
        for k in ("cert_expiry", "cert_subject", "cert_issuer", "cert_validity_start", "cert_refs"):
            out[k] = None

    if keymat:
        rcms = [_cp(c["asset"]).get("relatedCryptoMaterialProperties") or {} for c in ctxs
                if c["kind"] == "related-crypto-material"]
        out["key_type"] = any(x.get("type") == keymat["kind"] for x in rcms)
        want_fmt = _fmt(keymat.get("format"))
        out["key_format"] = any(x.get("format") and (not want_fmt or _fmt(x["format"]) == want_fmt) for x in rcms)
    else:
        out["key_type"] = out["key_format"] = None

    out["protocol_version"] = any(c["kind"] == "protocol" and c["role"] == "version" for c in ctxs) if is_proto else None
    out["suite_listed"] = any(c["kind"] == "protocol" and c["role"] == "suite" for c in ctxs) if is_suite else None

    if algorithmic and oid_for(fam, f["params"]):
        def oid_ok(c):
            got = _cp(c.get("via")).get("oid")
            return bool(got) and (got == oid_for(fam, f["params"]) or normalize(str(got))[0] == fam)
        out["oid"] = any(oid_ok(c) for c in ctxs)
    else:
        out["oid"] = None
    out["functions"] = any(_ap(c).get("cryptoFunctions") for c in ctxs) if algorithmic else None
    out["quantum_level"] = bool(r["quantum_ok"]) if (algorithmic and expected_quantum_level(fam, f["params"]) is not None) else None

    if code:
        out["code_context"] = any(o.get("symbol") or o.get("additionalContext") for c in ctxs for o in c["occurrences"])
    else:
        out["code_context"] = None
    if (code or f["file"].endswith(COMPILED_SUFFIXES)) and not ("library" in f and f["library"] is None):
        out["provenance"] = any(c["provided_by"] for c in ctxs)
    else:
        out["provenance"] = None
    return out


def summarize(results: list[dict], rubric: dict) -> dict:
    tiers = {c["id"]: c["tier"] for c in rubric["checks"]}
    det = [r for r in results if r["detected"]]
    per_check = {}
    for c in rubric["checks"]:
        vals = [r["actionability"][c["id"]] for r in det if r["actionability"].get(c["id"]) is not None]
        per_check[c["id"]] = {"label": c["label"], "tier": c["tier"], "applicable": len(vals),
                              "passed": sum(vals), "pct": round(100 * sum(vals) / len(vals), 1) if vals else None}
    ready, total_checks, passed_checks = [], 0, 0
    for r in det:
        a = {k: v for k, v in r["actionability"].items() if k in tiers and v is not None}
        total_checks += len(a)
        passed_checks += sum(a.values())
        missing_must = [k for k, v in a.items() if tiers[k] == "must" and not v]
        r["missing_must"] = missing_must
        r["ticket_ready"] = not missing_must
        if not missing_must:
            ready.append(r)
    pct = lambda n, d: round(100 * n / d, 1) if d else None  # noqa: E731
    return {"rubric": rubric["id"], "rubric_status": rubric["status"], "detected": len(det),
            "ticket_ready": len(ready), "ticket_ready_pct": pct(len(ready), len(det)),
            "actionable_recall": pct(len(ready), len(results)), "expected": len(results),
            "completeness_pct": pct(passed_checks, total_checks), "checks": per_check}
