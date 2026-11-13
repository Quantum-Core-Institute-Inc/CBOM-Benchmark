"""Artifact integrity: what can be said about a scanner's output file as a record.

Two facts, reported per scanner and not part of any score (METHODOLOGY.md 4d):

  * Signature. Is the CBOM signed, and does the signature verify? CycloneDX carries a signature as
    a top-level `signature` object in JSON Signature Format (JSF). A simple JSF signature with an
    embedded public key is verified here. Verifying with the key the file itself carries shows the
    file was not altered after signing. It does not show who signed it: that needs a key the reader
    already trusts, which a benchmark does not have. A detached signature file beside the CBOM is
    reported as present and not verified, for the same reason.

  * Repeatability. Does a second scan of the same input give the same output? The answer is one of
    four: byte-identical; identical apart from the serial number and timestamp; the same content in
    a different order; or different. A CBOM that changes between two scans of unchanged code cannot
    be compared week to week without separating real change from noise.

The JSF check follows the specification (https://cyberphone.github.io/doc/security/jsf.html) and
RFC 8785 canonicalization. It has been tested against signatures made here, not against another
signer's output, and it does not claim a verdict where it cannot be sure: multi-signer and chained
signatures, algorithms outside the list below, and documents with non-integer numbers (whose
canonical form depends on number formatting this code does not reproduce in every case) are all
"not checked", with the reason.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path

DETACHED_SUFFIXES = (".sig", ".asc", ".p7s", ".sigstore", ".sigstore.json", ".bundle", ".dsse", ".intoto.jsonl", ".minisig")
_HASH = {"256": "SHA256", "384": "SHA384", "512": "SHA512"}


# ------------------------------------------------------------------------------------- signature
def _b64u(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def _has_float(v) -> bool:
    if isinstance(v, float):
        return True
    if isinstance(v, dict):
        return any(_has_float(x) for x in v.values())
    if isinstance(v, list):
        return any(_has_float(x) for x in v)
    return False


def canonical(v) -> bytes:
    """RFC 8785 (JCS) for documents without non-integer numbers: sorted keys, no whitespace, UTF-8."""
    def enc(x) -> str:
        if isinstance(x, dict):
            # JCS sorts property names by UTF-16 code units
            items = sorted(x.items(), key=lambda kv: kv[0].encode("utf-16-be"))
            return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + enc(val) for k, val in items) + "}"
        if isinstance(x, list):
            return "[" + ",".join(enc(i) for i in x) + "]"
        return json.dumps(x, ensure_ascii=False)
    return enc(v).encode("utf-8")


def _public_key(jwk: dict):
    from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa
    kty = jwk.get("kty")
    if kty == "RSA":
        return rsa.RSAPublicNumbers(int.from_bytes(_b64u(jwk["e"]), "big"), int.from_bytes(_b64u(jwk["n"]), "big")).public_key()
    if kty == "EC":
        curve = {"P-256": ec.SECP256R1(), "P-384": ec.SECP384R1(), "P-521": ec.SECP521R1()}[jwk["crv"]]
        return ec.EllipticCurvePublicNumbers(int.from_bytes(_b64u(jwk["x"]), "big"), int.from_bytes(_b64u(jwk["y"]), "big"), curve).public_key()
    if kty == "OKP" and jwk.get("crv") == "Ed25519":
        return ed25519.Ed25519PublicKey.from_public_bytes(_b64u(jwk["x"]))
    raise ValueError(f"key type {kty} {jwk.get('crv', '')}".strip())


def _verify(alg: str, key, sig: bytes, data: bytes) -> None:
    """Raises on a bad signature or an algorithm this code does not handle."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, padding, utils
    if alg == "Ed25519":
        key.verify(sig, data)
        return
    h = getattr(hashes, _HASH[alg[2:]])()
    if alg.startswith("RS"):
        key.verify(sig, data, padding.PKCS1v15(), h)
    elif alg.startswith("PS"):
        key.verify(sig, data, padding.PSS(mgf=padding.MGF1(h), salt_length=h.digest_size), h)
    elif alg.startswith("ES"):
        half = len(sig) // 2  # JSF carries r || s; the library wants DER
        key.verify(utils.encode_dss_signature(int.from_bytes(sig[:half], "big"), int.from_bytes(sig[half:], "big")), data, ec.ECDSA(h))
    else:
        raise ValueError(f"algorithm {alg}")


SUPPORTED = ("RS256", "RS384", "RS512", "PS256", "PS384", "PS512", "ES256", "ES384", "ES512", "Ed25519")


def signature_facts(doc, raw_dir: Path | None = None, cbom_name: str | None = None) -> dict:
    """-> {"signed": "embedded" | "detached" | "no", "algorithm", "verifies": "yes" | "no" | "not checked", "note"}"""
    detached = []
    if raw_dir is not None and Path(raw_dir).is_dir():
        detached = sorted(p.name for p in Path(raw_dir).iterdir()
                          if p.is_file() and p.name != cbom_name and p.name.lower().endswith(DETACHED_SUFFIXES))
    sig = doc.get("signature") if isinstance(doc, dict) else None
    if not isinstance(sig, dict):
        if detached:
            return {"signed": "detached", "algorithm": None, "verifies": "not checked", "detached_files": detached,
                    "note": "a signature file sits beside the CBOM; verifying it needs the signer's key or identity"}
        return {"signed": "no", "algorithm": None, "verifies": "n/a", "note": "no signature in the file and none beside it"}
    out = {"signed": "embedded", "algorithm": sig.get("algorithm"), "verifies": "not checked",
           **({"detached_files": detached} if detached else {})}
    if "signers" in sig or "chain" in sig:
        return {**out, "algorithm": None, "note": "multi-signer or chained JSF signature: not verified here"}
    alg, value, jwk = sig.get("algorithm"), sig.get("value"), sig.get("publicKey")
    if alg not in SUPPORTED:
        return {**out, "note": f"algorithm {alg!r} is not one this check verifies ({', '.join(SUPPORTED)})"}
    if not isinstance(jwk, dict) or not value:
        return {**out, "note": "no public key in the file: verifying needs the signer's key"}
    body = copy.deepcopy(doc)
    for name in sig.get("excludes") or []:
        body.pop(name, None)
    body["signature"] = {k: v for k, v in sig.items() if k != "value"}
    if _has_float(body):
        return {**out, "note": "the document has non-integer numbers; their canonical form is not reproduced here"}
    try:
        key = _public_key(jwk)
    except Exception as e:  # noqa: BLE001  (any malformed key is the same answer)
        return {**out, "note": f"the embedded public key could not be read ({e})"}
    try:
        _verify(alg, key, _b64u(value), canonical(body))
    except Exception:  # noqa: BLE001  (InvalidSignature, or a signature of the wrong shape)
        return {**out, "verifies": "no", "note": "the signature does not match the file's content under the key the file carries"}
    return {**out, "verifies": "yes",
            "note": "verifies under the key the file carries: the content is unaltered since signing; who signed is not established"}


# --------------------------------------------------------------------------------- repeatability
# Fields a scanner is expected to change on every run. Named, so that nothing else is forgiven.
def _strip_volatile(doc):
    doc = copy.deepcopy(doc)
    dropped = []
    if isinstance(doc, dict):
        if "serialNumber" in doc:
            doc.pop("serialNumber"); dropped.append("serialNumber")
        if isinstance(doc.get("metadata"), dict) and "timestamp" in doc["metadata"]:
            doc["metadata"].pop("timestamp"); dropped.append("metadata.timestamp")
        if "signature" in doc:  # a signature over a timestamped document differs with it
            doc.pop("signature"); dropped.append("signature")
        for run in doc.get("runs") or []:  # SARIF
            for inv in (run.get("invocations") or []) if isinstance(run, dict) else []:
                for k in ("startTimeUtc", "endTimeUtc"):
                    if isinstance(inv, dict) and k in inv:
                        inv.pop(k); dropped.append(f"runs.invocations.{k}")
    return doc, sorted(set(dropped))


def _unordered(v):
    """The same value with every list sorted, so that only content is compared."""
    if isinstance(v, dict):
        return {k: _unordered(x) for k, x in v.items()}
    if isinstance(v, list):
        return sorted((_unordered(x) for x in v), key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
    return v


def _items(doc) -> list[str]:
    """One string per component (CycloneDX) or result (SARIF), order-free, for counting what differs."""
    rows = []
    if isinstance(doc, dict):
        rows += doc.get("components") or []
        for run in doc.get("runs") or []:
            rows += (run.get("results") or []) if isinstance(run, dict) else []
    return [json.dumps(_unordered(r), sort_keys=True, ensure_ascii=False) for r in rows]


def repeatability(first: Path, second: Path) -> dict:
    """Compare the outputs of two scans of the same input."""
    a_bytes, b_bytes = Path(first).read_bytes(), Path(second).read_bytes()
    out = {"first_sha256": hashlib.sha256(a_bytes).hexdigest(), "second_sha256": hashlib.sha256(b_bytes).hexdigest()}
    if a_bytes == b_bytes:
        return {**out, "verdict": "byte-identical", "ignored": [], "only_in_first": 0, "only_in_second": 0}
    try:
        a, b = json.loads(a_bytes), json.loads(b_bytes)
    except ValueError:
        return {**out, "verdict": "different", "ignored": [], "only_in_first": None, "only_in_second": None,
                "note": "the outputs differ and are not both JSON, so the difference is not broken down"}
    sa, da = _strip_volatile(a)
    sb, db = _strip_volatile(b)
    ignored = sorted(set(da) | set(db))
    if sa == sb:
        return {**out, "verdict": "identical apart from serial number and timestamp", "ignored": ignored,
                "only_in_first": 0, "only_in_second": 0}
    if _unordered(sa) == _unordered(sb):
        return {**out, "verdict": "same content, different order", "ignored": ignored, "only_in_first": 0, "only_in_second": 0}
    ia, ib = _items(sa), _items(sb)
    rest_b = list(ib)
    only_a = 0
    for row in ia:
        if row in rest_b:
            rest_b.remove(row)
        else:
            only_a += 1
    return {**out, "verdict": "different", "ignored": ignored, "only_in_first": only_a, "only_in_second": len(rest_b)}


# ---------------------------------------------------------------------------------------- report
def facts(raw_dir: Path, cbom_name: str, repeat_dir: Path | None = None) -> dict:
    """Everything this module reports for one bundle, from the files in it."""
    raw = Path(raw_dir) / cbom_name
    try:
        doc = json.loads(raw.read_text())
    except ValueError:
        doc = None
    out = {"signature": signature_facts(doc, raw_dir, cbom_name) if doc is not None else
           {"signed": "no", "algorithm": None, "verifies": "n/a", "note": "the output is not JSON"}}
    second = Path(repeat_dir) / cbom_name if repeat_dir else None
    out["repeat"] = repeatability(raw, second) if second and second.exists() else {"verdict": "not run"}
    return out


def signed_cell(f: dict | None) -> str:
    """One table cell: is it signed, and does the signature verify."""
    s = (f or {}).get("signature")
    if not s:
        return "not measured"
    if s["signed"] == "no":
        return "no"
    if s["signed"] == "detached":
        return "detached file, not verified"
    return {"yes": f"yes ({s['algorithm']}), verifies", "no": f"yes ({s['algorithm']}), does NOT verify",
            }.get(s["verifies"], f"yes ({s.get('algorithm') or 'JSF'}), not verified")


def repeat_cell(f: dict | None) -> str:
    r = (f or {}).get("repeat")
    if not r or r["verdict"] == "not run":
        return "not measured"
    if r["verdict"] == "different":
        a, b = r.get("only_in_first"), r.get("only_in_second")
        return "different" + (f" ({a} entries only in the first run, {b} only in the second)" if a is not None else "")
    return r["verdict"]


def markdown(f: dict, name: str) -> str:
    s, r = f["signature"], f["repeat"]
    out = [f"# Artifact integrity: {name}", "",
           "Reported, not scored. See METHODOLOGY.md 4d.", "",
           f"- **Signed:** {signed_cell(f)}. {s.get('note', '')}".rstrip(),
           f"- **Second scan of the same input:** {repeat_cell(f)}."]
    if r.get("ignored"):
        out.append(f"  Fields that differed and are expected to: {', '.join(r['ignored'])}.")
    if s.get("detached_files"):
        out.append(f"- Signature files beside the CBOM: {', '.join(s['detached_files'])}.")
    return "\n".join(out) + "\n"
