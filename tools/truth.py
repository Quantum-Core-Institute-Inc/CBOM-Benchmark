"""Load the answer key: the shipped ground truth plus any bring-your-own-code (BYOC) case manifests.

Shipped findings live in expected/ground_truth.json. An organization's own cases live in
expected/custom/<case>.json, one manifest per case, with code under corpus/custom/<case>/.
Keeping them apart means a testbench upgrade never overwrites an organization's cases, and
their cases never leak into the published benchmark numbers (score with --exclude-custom).

Manifest format (paths are relative to the case directory):

{
  "case": "example_envelope",
  "description": "What pattern this reproduces from our estate",
  "owner": "team or person to ask",
  "lang": "python",                 # python | java | assets | mixed (informational)
  "use": "custom",                  # deadline category: firmware-signing|networking|web|os|niche|custom
  "run": ["python3", "main.py"],    # optional: proves the case executes (run from the case dir)
  "findings": [
    {"file": "envelope/kem_rsa.py", "family": "RSA", "params": {"key_size": 2048},
     "anchors": ["rsa.generate_private_key("], "alt_files": [{"file": "envelope/profiles.py", "anchors": [...]}],
     "note": "...", "confirmed": true}
  ],
  "also_ok": [{"file": "...", "families": ["SHA-256"]}],
  "materials": [{"id": "...", "kind": "certificate", "file": "...", "key": "<finding id>", "sig_alg": "..."}]
}

Only findings with "confirmed": true are scored. Drafts from `byoc.py draft` start unconfirmed.
"""
from __future__ import annotations

import pyreq  # noqa: F401  (fails early on an unsupported Python)
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHIPPED = ROOT / "expected" / "ground_truth.json"
CUSTOM_DIR = ROOT / "expected" / "custom"
CUSTOM_CORPUS = "corpus/custom"


def case_path(case: str, rel: str) -> str:
    rel = rel.replace("\\", "/")
    return rel if rel.startswith("corpus/") else f"{CUSTOM_CORPUS}/{case}/{rel}"


def load_manifest(path: Path) -> dict:
    m = json.loads(path.read_text(encoding="utf-8"))
    m.setdefault("case", path.stem)
    return m


def custom_manifests() -> list[tuple[Path, dict]]:
    if not CUSTOM_DIR.exists():
        return []
    return [(p, load_manifest(p)) for p in sorted(CUSTOM_DIR.glob("*.json"))]


def manifest_to_truth(m: dict, include_unconfirmed: bool = False) -> dict:
    """Convert one manifest into ground-truth entries (findings, also_ok, materials, decoys)."""
    case = m["case"]
    out = {"findings": [], "also_ok": [], "materials": [], "decoys": {}}
    n = 0
    for f in m.get("findings", []):
        if not f.get("confirmed") and not include_unconfirmed:
            continue
        n += 1
        g = {k: v for k, v in f.items() if k not in ("file", "alt_files", "confirmed")}
        g["id"] = f.get("id") or f"C-{case}-{n:02d}"
        g["tier"], g["lang"] = "custom", case
        g["file"] = case_path(case, f["file"])
        g.setdefault("params", {})
        g["use"] = f.get("use") or m.get("use") or "custom"
        if f.get("alt_files"):
            g["alt_files"] = [{**a, "file": case_path(case, a["file"])} for a in f["alt_files"]]
        g["confirmed"] = bool(f.get("confirmed"))
        out["findings"].append(g)
    for e in m.get("also_ok", []):
        out["also_ok"].append({"file": case_path(case, e["file"]), "families": e["families"]})
    for mat in m.get("materials", []):
        out["materials"].append({**mat, "file": case_path(case, mat["file"])})
    for rel, why in m.get("decoys", {}).items():
        out["decoys"][case_path(case, rel)] = why
    return out


def load_ground_truth(include_custom: bool = True) -> dict:
    gt = json.loads(SHIPPED.read_text(encoding="utf-8"))
    if include_custom:
        for _, m in custom_manifests():
            t = manifest_to_truth(m)
            gt["findings"] += t["findings"]
            gt.setdefault("also_ok", []).extend(t["also_ok"])
            gt.setdefault("materials", []).extend(t["materials"])
            gt.setdefault("decoys", {}).update(t["decoys"])
    return gt


def attach_facts(gt: dict) -> dict:
    """Read real facts (certificate subject, issuer, validity; key file format) into gt['materials']."""
    from assetfacts import certificate_facts, key_format
    by_id = {f["id"]: f for f in gt["findings"]}
    for m in gt.get("materials", []):
        k = by_id.get(m["key"])
        if k is None:
            continue
        path = ROOT / m["file"]
        if m["kind"] == "certificate":
            m["facts"] = certificate_facts(path, k["family"], k["params"])
        else:
            m["format"] = key_format(path)
    return gt


def library_for(f: dict) -> str | None:
    """Which library provides a code finding, for the reference CBOM's dependency graph.
    None for assets and for hand-rolled code (ground truth sets "library": null)."""
    if "library" in f and f["library"] is None:
        return None
    path = f["file"]
    if path.endswith(".java") or path.endswith(".jar"):
        return "lib-openjdk"
    if path.endswith(".pyc"):
        return "lib-cpython"
    if path.endswith(".go"):
        return "lib-go-stdlib"
    if path.endswith((".js", ".mjs", ".ts")):
        return "lib-node-crypto"
    if path.endswith(".c"):
        return "lib-openssl"
    if path.endswith(".py"):
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
        text = " ".join(lines[n - 1] for n in f.get("lines", [])[:1])
        return "lib-cpython" if ("hashlib" in text or "hmac." in text) else "lib-pyca-cryptography"
    return None


LIBRARIES = [
    {"type": "library", "bom-ref": "lib-pyca-cryptography", "name": "cryptography", "group": "pyca",
     "purl": "pkg:pypi/cryptography"},
    {"type": "library", "bom-ref": "lib-cpython", "name": "CPython standard library (hashlib, hmac)",
     "purl": "pkg:generic/cpython"},
    {"type": "library", "bom-ref": "lib-go-stdlib", "name": "Go standard library crypto", "group": "golang",
     "purl": "pkg:golang/std"},
    {"type": "library", "bom-ref": "lib-node-crypto", "name": "Node.js crypto (node:crypto, Web Crypto)",
     "purl": "pkg:generic/nodejs"},
    {"type": "library", "bom-ref": "lib-openssl", "name": "OpenSSL libcrypto / libssl", "group": "openssl",
     "purl": "pkg:generic/openssl"},
    {"type": "library", "bom-ref": "lib-openjdk", "name": "OpenJDK security providers (SUN, SunJCE, SunEC)",
     "purl": "pkg:generic/openjdk"},
]
