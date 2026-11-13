#!/usr/bin/env python3
"""Checks for tools/integrity.py: the signature verdict and the second-scan comparison."""
from __future__ import annotations

import base64
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrity  # noqa: E402

from cryptography.hazmat.primitives import hashes  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa, utils  # noqa: E402


def b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def num(n: int, size: int | None = None) -> str:
    return b64u(n.to_bytes(size or (n.bit_length() + 7) // 8, "big"))


BOM = {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1, "serialNumber": "urn:uuid:1",
       "metadata": {"timestamp": "2026-11-13T00:00:00Z"},
       "components": [{"type": "cryptographic-asset", "name": "AES-256-GCM", "bom-ref": "a"},
                      {"type": "cryptographic-asset", "name": "RSA-2048", "bom-ref": "b"}]}


def sign(doc: dict, alg: str) -> dict:
    """Sign as JSF says: over the canonical document carrying the signature object without `value`."""
    doc = copy.deepcopy(doc)
    if alg == "Ed25519":
        key = ed25519.Ed25519PrivateKey.generate()
        jwk = {"kty": "OKP", "crv": "Ed25519", "x": b64u(key.public_key().public_bytes_raw())}
    elif alg == "ES256":
        key = ec.generate_private_key(ec.SECP256R1())
        n = key.public_key().public_numbers()
        jwk = {"kty": "EC", "crv": "P-256", "x": num(n.x, 32), "y": num(n.y, 32)}
    else:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        n = key.public_key().public_numbers()
        jwk = {"kty": "RSA", "n": num(n.n), "e": num(n.e)}
    doc["signature"] = {"algorithm": alg, "publicKey": jwk}
    data = integrity.canonical(doc)
    if alg == "Ed25519":
        sig = key.sign(data)
    elif alg == "ES256":
        r, s = utils.decode_dss_signature(key.sign(data, ec.ECDSA(hashes.SHA256())))
        sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    elif alg == "PS256":
        sig = key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32), hashes.SHA256())
    else:
        sig = key.sign(data, padding.PKCS1v15(), hashes.SHA256())
    doc["signature"]["value"] = b64u(sig)
    return doc


def main() -> int:
    bad = []

    def check(name, ok):
        if not ok:
            bad.append(name)
        print(("ok   " if ok else "FAIL ") + name)

    # ---- signature
    f = integrity.signature_facts(BOM)
    check("an unsigned CBOM is reported as not signed", f["signed"] == "no" and f["verifies"] == "n/a")
    for alg in ("Ed25519", "ES256", "RS256", "PS256"):
        signed = sign(BOM, alg)
        f = integrity.signature_facts(signed)
        check(f"a {alg} JSF signature verifies", (f["signed"], f["algorithm"], f["verifies"]) == ("embedded", alg, "yes"))
        tampered = copy.deepcopy(signed)
        tampered["components"][0]["name"] = "AES-128-GCM"
        check(f"one changed value fails the {alg} signature", integrity.signature_facts(tampered)["verifies"] == "no")
    signed = sign(BOM, "Ed25519")
    reordered = json.loads(json.dumps({k: signed[k] for k in reversed(list(signed))}, indent=4))
    check("key order and whitespace do not affect the verdict", integrity.signature_facts(reordered)["verifies"] == "yes")
    other = sign(BOM, "Ed25519")
    swapped = copy.deepcopy(signed)
    swapped["signature"]["publicKey"] = other["signature"]["publicKey"]
    check("another key does not verify the signature", integrity.signature_facts(swapped)["verifies"] == "no")
    unknown = copy.deepcopy(signed)
    unknown["signature"]["algorithm"] = "ML-DSA-65"
    f = integrity.signature_facts(unknown)
    check("an algorithm outside the list is 'not checked', never 'no'", f["signed"] == "embedded" and f["verifies"] == "not checked")
    nokey = copy.deepcopy(signed)
    del nokey["signature"]["publicKey"]
    check("a signature without its public key is 'not checked'", integrity.signature_facts(nokey)["verifies"] == "not checked")
    multi = {**BOM, "signature": {"signers": [signed["signature"]]}}
    check("a multi-signer signature is 'not checked'", integrity.signature_facts(multi)["verifies"] == "not checked")
    withfloat = sign({**BOM, "score": 7.5}, "Ed25519")
    check("a document with non-integer numbers is 'not checked'", integrity.signature_facts(withfloat)["verifies"] == "not checked")
    excl = copy.deepcopy(BOM)
    excl["signature"] = {"algorithm": "Ed25519", "excludes": ["metadata"]}
    key = ed25519.Ed25519PrivateKey.generate()
    excl["signature"]["publicKey"] = {"kty": "OKP", "crv": "Ed25519", "x": b64u(key.public_key().public_bytes_raw())}
    body = {k: v for k, v in excl.items() if k != "metadata"}
    excl["signature"]["value"] = b64u(key.sign(integrity.canonical(body)))
    excl["metadata"]["timestamp"] = "2027-01-01T00:00:00Z"
    check("a property the signature excludes can change", integrity.signature_facts(excl)["verifies"] == "yes")

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "cbom.json").write_text(json.dumps(BOM))
        (d / "cbom.json.sig").write_text("x")
        f = integrity.signature_facts(BOM, d, "cbom.json")
        check("a signature file beside the CBOM is reported, not verified",
              f["signed"] == "detached" and f["verifies"] == "not checked" and f["detached_files"] == ["cbom.json.sig"])

        # ---- repeatability
        def rep(a, b, text=False):
            (d / "a.json").write_text(a if text else json.dumps(a, indent=2))
            (d / "b.json").write_text(b if text else json.dumps(b, indent=2))
            return integrity.repeatability(d / "a.json", d / "b.json")

        check("two identical files are byte-identical", rep(BOM, BOM)["verdict"] == "byte-identical")
        later = {**copy.deepcopy(BOM), "serialNumber": "urn:uuid:2", "metadata": {"timestamp": "2026-11-14T00:00:00Z"}}
        r = rep(BOM, later)
        check("a new serial number and timestamp are the expected difference",
              r["verdict"] == "identical apart from serial number and timestamp"
              and r["ignored"] == ["metadata.timestamp", "serialNumber"])
        shuffled = copy.deepcopy(later)
        shuffled["components"].reverse()
        check("the same components in another order are reported as such", rep(BOM, shuffled)["verdict"] == "same content, different order")
        changed = copy.deepcopy(later)
        changed["components"][1]["name"] = "RSA-4096"
        changed["components"].append({"type": "cryptographic-asset", "name": "MD5", "bom-ref": "c"})
        r = rep(BOM, changed)
        check("a different component is a difference, and is counted",
              (r["verdict"], r["only_in_first"], r["only_in_second"]) == ("different", 1, 2))
        renumbered = copy.deepcopy(BOM)
        renumbered["components"][0]["bom-ref"] = "z"
        check("a changed bom-ref is a difference: identity is content", rep(BOM, renumbered)["verdict"] == "different")
        other_meta = copy.deepcopy(BOM)
        other_meta["metadata"]["tools"] = ["x"]
        check("no other metadata difference is forgiven", rep(BOM, other_meta)["verdict"] == "different")
        sarif = {"runs": [{"invocations": [{"startTimeUtc": "a", "endTimeUtc": "b"}], "results": [{"ruleId": "r"}]}]}
        sarif2 = {"runs": [{"invocations": [{"startTimeUtc": "c", "endTimeUtc": "d"}], "results": [{"ruleId": "r"}]}]}
        check("SARIF run times are the expected difference", rep(sarif, sarif2)["verdict"].startswith("identical apart"))
        check("outputs that are not JSON are compared as bytes", rep("x", "y", text=True)["verdict"] == "different")

        (d / "raw").mkdir(); (d / "again").mkdir()
        (d / "raw" / "cbom.json").write_text(json.dumps(sign(BOM, "Ed25519")))
        f = integrity.facts(d / "raw", "cbom.json")
        check("with no second scan, repeatability is 'not run'", f["repeat"]["verdict"] == "not run" and f["signature"]["verifies"] == "yes")
        (d / "again" / "cbom.json").write_text((d / "raw" / "cbom.json").read_text())
        f = integrity.facts(d / "raw", "cbom.json", d / "again")
        check("facts() reads both from the bundle's directories", f["repeat"]["verdict"] == "byte-identical")
        check("the table cells say it in words",
              integrity.signed_cell(f) == "yes (Ed25519), verifies" and integrity.repeat_cell(f) == "byte-identical"
              and integrity.signed_cell(None) == "not measured" and integrity.repeat_cell({"repeat": {"verdict": "not run"}}) == "not measured")

    print("\nAll integrity checks pass." if not bad else f"\n{len(bad)} FAILED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
