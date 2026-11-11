#!/usr/bin/env python3
"""Library (dependency) scoring checks. Run: python tools/test_libraries.py"""
import pyreq  # noqa: F401  (fails early on an unsupported Python)
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import libraries as libs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REF = json.loads((ROOT / "expected" / "expected.cdx.json").read_text())


def lib(name, loc=None, version=None, purl=None, group=None, typ="library", props=()):
    c = {"type": typ, "name": name, "bom-ref": f"x-{name}-{loc}"}
    if version:
        c["version"] = version
    if purl:
        c["purl"] = purl
    if group:
        c["group"] = group
    if loc:
        c["evidence"] = {"occurrences": [{"location": loc}]}
    if props:
        c["properties"] = [{"name": k, "value": v} for k, v in props]
    return c


def run(components):
    return libs.score_libraries({"components": components})


def main() -> int:
    bad = []

    def check(label, ok):
        print(("ok   " if ok else "FAIL ") + label)
        if not ok:
            bad.append(label)

    names = [(("cryptography", None, "pkg:pypi/cryptography@41.0.7"), "pyca-cryptography"),
             (("pycrypto", None, None), "pycrypto"), (("pycryptodome", None, None), "pycryptodome"),
             (("bcpkix-jdk15on", "org.bouncycastle", None), "bouncycastle"), (("BouncyCastle", None, None), "bouncycastle"),
             ((None, None, "pkg:npm/%40noble/curves@2.0.1"), "noble-curves"), (("Go-CIRCL", None, None), "circl"),
             ((None, None, "pkg:golang/github.com/golang-jwt/jwt/v5@v5.2.1"), "golang-jwt"),
             (("requests", None, None), None), (("bcryptjs", None, None), "bcryptjs"), (("bcrypt", None, None), "bcrypt")]
    check("library names normalize", all(libs.normalize_library(*a) == want for a, want in names))

    r = libs.score_libraries(REF)
    n_exp = len(json.loads((ROOT / "expected" / "libraries.json").read_text())["libraries"])
    check(f"reference: {n_exp}/{n_exp} in manifest, versions 100%, no false positives",
          r["found_in_manifest"] == r["expected"] == n_exp and r["version_accuracy"] == 100 and not r["false_positives"])

    req = "corpus/deps/python-billing/requirements.txt"
    r = run([lib("pycrypto", req, "2.6.1")])
    check("commented-out dependency reported -> decoy false positive", [x["kind"] for x in r["false_positives"]] == ["decoy"])
    r = run([lib("hashids", req, "1.3.1")])
    check("look-alike listed as a plain library -> no penalty", not r["false_positives"])
    r = run([lib("hashids", req, "1.3.1", typ="cryptographic-asset")])
    check("look-alike reported as cryptography -> false positive", [x["kind"] for x in r["false_positives"]] == ["look-alike"])
    r = run([lib("libsodium", req)])
    check("crypto library attributed to a manifest that doesn't declare it -> false positive",
          [x["kind"] for x in r["false_positives"]] == ["unexpected"])

    r = run([lib("cryptography", req)])
    row = next(x for x in r["results"] if x["id"] == "L-PY-01")
    check("found without a version -> 'not reported', counted as not correct",
          row["version_state"] == "not reported" and r["version_accuracy"] == 0)
    r = run([lib("cryptography", req, "42.0.0")])
    check("wrong version -> 'wrong'", next(x for x in r["results"] if x["id"] == "L-PY-01")["version_state"] == "wrong")
    r = run([lib("cryptography", None, "41.0.7")])
    row = next(x for x in r["results"] if x["id"] == "L-PY-01")
    check("no location -> found anywhere, not in manifest", row["found_anywhere"] and not row["found_in_manifest"])
    r = run([lib("jws", "corpus/deps/node-api/package-lock.json", "3.2.3")])
    check("transitive dependency credited from the lockfile", r["transitive_recall"] == 25.0)
    r = run([lib("jsonwebtoken", "corpus/deps/node-api/package-lock.json", "9.0.2")])
    check("direct npm dependency credited from its lockfile (alt file)",
          next(x for x in r["results"] if x["id"] == "L-JS-01")["found_in_manifest"])

    gradle = "corpus/deps/java-pq/build.gradle"
    r = run([lib("BouncyCastle", gradle, props=[(libs.PQ_PROPERTY, "false")])])
    check("wrong PQC verdict counted", r["pq_verdict_accuracy"] == 0 and len(r["pq_verdicts_wrong"]) == 1)
    r = run([lib("BouncyCastle", gradle, props=[(libs.PQ_PROPERTY, "true")])])
    check("right PQC verdict counted", r["pq_verdict_accuracy"] == 100)

    ref = copy.deepcopy(REF)
    ref["components"] = [c for c in ref["components"] if c.get("type") != "library" or not c["bom-ref"].startswith("L-")]
    r = libs.score_libraries(ref)
    check("no library components -> 0 in manifest", r["found_in_manifest"] == 0)

    print(f"\n{'All library checks pass.' if not bad else f'{len(bad)} library checks FAILED.'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
