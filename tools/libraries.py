"""Dependency-level crypto: which crypto libraries each manifest pulls in, at which version.

Answer key: expected/libraries.json. A scanner's CBOM is read for library components (type
"library" or "framework", by purl, group/name or name) and for cryptographic-asset components named
after a library (QCI reports dependencies that way, after its adapter). Location comes from
evidence.occurrences or a SrcFile property.

Scored per expected (manifest, library):
  found in manifest   a matching library is reported in that manifest (or an alt file: package.json
                      and its lockfile describe the same dependency)
  found anywhere      ...or reported with no location at all (an inventory that can't say which app)
  version             the reported version equals what the manifest declares
False positives: a library reported from a commented-out line (decoys); a non-crypto look-alike
reported *as cryptography*; a crypto library attributed to a manifest that doesn't declare it.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from cbomlib import same_file

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = ROOT / "expected" / "libraries.json"

# key -> (is cryptography, display name)
LIBS = {
    "pyca-cryptography": (True, "pyca/cryptography"), "pycryptodome": (True, "PyCryptodome"),
    "pycrypto": (True, "PyCrypto"), "pyopenssl": (True, "pyOpenSSL"), "pyjwt": (True, "PyJWT"),
    "paramiko": (True, "Paramiko"), "bcrypt": (True, "bcrypt"), "liboqs": (True, "liboqs"),
    "bouncycastle": (True, "Bouncy Castle"), "nimbus-jose-jwt": (True, "Nimbus JOSE+JWT"), "jjwt": (True, "JJWT"),
    "jasypt": (True, "Jasypt"), "jsonwebtoken": (True, "jsonwebtoken"), "jws": (True, "jws"), "jwa": (True, "jwa"),
    "crypto-js": (True, "crypto-js"), "node-forge": (True, "node-forge"), "bcryptjs": (True, "bcryptjs"),
    "noble-post-quantum": (True, "@noble/post-quantum"), "noble-curves": (True, "@noble/curves"),
    "noble-hashes": (True, "@noble/hashes"), "ecdsa-sig-formatter": (True, "ecdsa-sig-formatter"),
    "buffer-equal-constant-time": (True, "buffer-equal-constant-time"), "golang-x-crypto": (True, "golang.org/x/crypto"),
    "circl": (True, "Cloudflare CIRCL"), "golang-jwt": (True, "golang-jwt"), "openssl": (True, "OpenSSL"),
    "libsodium": (True, "libsodium"), "nodejs-runtime": (True, "Node.js runtime"),
    "hashids": (False, "hashids"), "golang-x-sys": (False, "golang.org/x/sys"),
}

_EXACT = {  # lowercased package name (npm / pypi / conan / generic) or group:artifact or Go path -> key
    "cryptography": "pyca-cryptography", "python-cryptography": "pyca-cryptography", "pycryptodome": "pycryptodome",
    "pycryptodomex": "pycryptodome", "pycrypto": "pycrypto", "pyopenssl": "pyopenssl", "pyjwt": "pyjwt",
    "paramiko": "paramiko", "bcrypt": "bcrypt", "liboqs-python": "liboqs", "oqs": "liboqs", "liboqs": "liboqs",
    "com.nimbusds:nimbus-jose-jwt": "nimbus-jose-jwt", "nimbus-jose-jwt": "nimbus-jose-jwt",
    "org.jasypt:jasypt": "jasypt", "jasypt": "jasypt", "jsonwebtoken": "jsonwebtoken", "jws": "jws", "jwa": "jwa",
    "crypto-js": "crypto-js", "node-forge": "node-forge", "bcryptjs": "bcryptjs",
    "@noble/post-quantum": "noble-post-quantum", "@noble/curves": "noble-curves", "@noble/hashes": "noble-hashes",
    "ecdsa-sig-formatter": "ecdsa-sig-formatter", "buffer-equal-constant-time": "buffer-equal-constant-time",
    "golang.org/x/crypto": "golang-x-crypto", "golang.org/x/sys": "golang-x-sys",
    "github.com/cloudflare/circl": "circl", "go-circl": "circl", "circl": "circl",
    "openssl": "openssl", "libssl": "openssl", "libssl-dev": "openssl", "libcrypto": "openssl",
    "libsodium": "libsodium", "node.js": "nodejs-runtime", "nodejs": "nodejs-runtime", "hashids": "hashids",
}


def normalize_library(name: str | None, group: str | None = None, purl: str | None = None) -> str | None:
    """Map a reported library to a canonical key, or None if it isn't one the testbench tracks."""
    cands = []
    if purl:
        m = re.match(r"pkg:([^/]+)/(.+?)(?:@[^?#]*)?(?:[?#].*)?$", purl)
        if m:
            kind, path = m.group(1).lower(), m.group(2).replace("%40", "@").lower()
            if kind == "maven" and "/" in path:
                g, a = path.rsplit("/", 1)
                cands += [f"{g}:{a}", g + ":*"]
            cands.append(path)
    if group:
        cands += [f"{group}:{name}".lower(), f"{group}:*".lower(), f"{group}/{name}".lower()]
    if name:
        cands.append(name.lower())
    for c in cands:
        if c.startswith("org.bouncycastle") or re.fullmatch(r"(bc(prov|pkix|tls|util|pg|mail|jmail)-jdk\d+on)|bouncycastle", c):
            return "bouncycastle"
        if c.startswith("io.jsonwebtoken") or re.fullmatch(r"jjwt(-api|-impl|-jackson)?", c):
            return "jjwt"
        if re.fullmatch(r"github\.com/golang-jwt/jwt(/v\d+)?", c):
            return "golang-jwt"
        if re.fullmatch(r"(lib)?openssl(\d[\w.]*)?|libssl[\d.]*(-dev)?", c):
            return "openssl"
        if c in _EXACT:
            return _EXACT[c]
    return None


# Adapters that translate a scanner's own "this library does / doesn't do PQC" verdict set this property.
PQ_PROPERTY = "cbom-testbench:pq_capable"


def _locations(c: dict) -> list[str]:
    locs = [o["location"] for o in (c.get("evidence") or {}).get("occurrences") or [] if o.get("location")]
    paths = [p["value"] for p in c.get("properties") or [] if p.get("name") == "SrcFile" and p.get("value")]
    # evidence.identity methods carry the manifest path for some tools (cdxgen: CMakeLists.txt)
    for ident in (c.get("evidence") or {}).get("identity") or []:
        paths += [m["value"] for m in ident.get("methods") or [] if "/corpus/" in str(m.get("value", ""))]
    for v in paths:
        v = v.replace("\\", "/").split()[-1]
        locs.append("corpus/" + v.split("/corpus/", 1)[1] if "/corpus/" in v else v)
    return sorted(set(locs))


def _walk(components):
    for c in components or []:
        yield c
        yield from _walk(c.get("components"))


def reported_libraries(bom: dict) -> list[dict]:
    out = []
    for c in _walk(bom.get("components")):
        is_lib = c.get("type") in ("library", "framework")
        key = normalize_library(c.get("name"), c.get("group"), c.get("purl"))
        if key is None or not (is_lib or c.get("type") == "cryptographic-asset"):
            continue
        claim = c.get("type") == "cryptographic-asset" or bool(c.get("cryptoProperties")) or any(
            "crypto" in (p.get("name") or "").lower() for p in c.get("properties") or [])
        pq = next((p.get("value") for p in c.get("properties") or [] if p.get("name") == PQ_PROPERTY), None)
        out.append({"key": key, "name": c.get("name"), "version": c.get("version"), "locations": _locations(c),
                    "crypto_claim": claim, "pq_claim": {"true": True, "false": False}.get(str(pq).lower())})
    return out


def _ver(v: str | None) -> str | None:
    if not v:
        return None
    return re.sub(r"^(v|==|=|\^|~|>=)\s*", "", str(v).strip()).lower()


def load_expected() -> dict | None:
    return json.loads(EXPECTED.read_text()) if EXPECTED.exists() else None


def score_libraries(bom: dict, expected: dict | None = None) -> dict | None:
    exp = expected or load_expected()
    if not exp:
        return None
    rep = reported_libraries(bom)
    results, claimed = [], set()
    for e in exp["libraries"]:
        files = [e["file"]] + e.get("alt_files", [])
        cands = [r for r in rep if r["key"] == e["library"]]
        located = [r for r in cands if any(same_file(loc, f) for loc in r["locations"] for f in files)]
        loose = [r for r in cands if not r["locations"]]
        for r in located:
            claimed.add(id(r))
        pool = located + loose  # versions: any report of this library (one tool may split location and version)
        want = _ver(e.get("version"))
        got = {_ver(r["version"]) for r in pool if r["version"]}
        state = ("n/a" if want is None or not pool else "ok" if want in got else "wrong" if got else "not reported")
        results.append({**e, "found_in_manifest": bool(located), "found_anywhere": bool(located or loose),
                        "version_state": state,
                        # a found library with no version counts against accuracy: the CBOM can't answer "which version?"
                        "version_ok": None if state == "n/a" else state == "ok",
                        "reported_versions": sorted({str(r["version"]) for r in pool if r["version"]}),
                        "pq_ok": None if e["pq_capable"] is None or not [r for r in pool if r["pq_claim"] is not None]
                        else any(r["pq_claim"] == e["pq_capable"] for r in pool if r["pq_claim"] is not None)})
    fps = []
    for d in exp.get("decoys", []):
        for r in rep:
            if r["key"] == d["library"] and any(same_file(loc, d["file"]) for loc in r["locations"]):
                fps.append({"kind": "decoy", "file": d["file"], "library": d["library"], "why": d["why"]})
    for d in exp.get("lookalikes", []):
        for r in rep:
            if r["key"] == d["library"] and r["crypto_claim"] and any(same_file(loc, d["file"]) for loc in r["locations"]):
                fps.append({"kind": "look-alike", "file": d["file"], "library": d["library"], "why": d["why"]})
    ok = {(a["file"], lib) for a in exp.get("also_ok", []) for lib in a["libraries"]}
    known = {(f, e["library"]) for e in exp["libraries"] for f in [e["file"]] + e.get("alt_files", [])}
    decoy_keys = {(d["file"], d["library"]) for d in exp.get("decoys", []) + exp.get("lookalikes", [])}
    for r in rep:
        if id(r) in claimed or not LIBS.get(r["key"], (False,))[0]:
            continue
        for loc in r["locations"]:
            path = next((f for f in {x[0] for x in known | ok | decoy_keys} if same_file(loc, f)), None)
            if path and (path, r["key"]) not in known | ok | decoy_keys:
                fps.append({"kind": "unexpected", "file": path, "library": r["key"],
                            "why": "manifest doesn't declare it"})
    n = len(results)
    direct = [r for r in results if r["scope"] == "direct"]
    trans = [r for r in results if r["scope"] == "transitive"]
    judged = [r for r in results if r["version_ok"] is not None]
    pq_judged = [r for r in results if r["pq_ok"] is not None]
    pct = lambda a, b: round(100 * a / b, 1) if b else None  # noqa: E731
    return {
        "expected": n,
        "found_in_manifest": sum(r["found_in_manifest"] for r in results),
        "found_anywhere": sum(r["found_anywhere"] for r in results),
        "recall": pct(sum(r["found_in_manifest"] for r in results), n),
        "recall_anywhere": pct(sum(r["found_anywhere"] for r in results), n),
        "direct_recall": pct(sum(r["found_in_manifest"] for r in direct), len(direct)),
        "transitive_recall": pct(sum(r["found_in_manifest"] for r in trans), len(trans)),
        "version_accuracy": pct(sum(r["version_ok"] for r in judged), len(judged)),
        "pq_verdicts_judged": len(pq_judged),
        "pq_verdict_accuracy": pct(sum(r["pq_ok"] for r in pq_judged), len(pq_judged)),
        "pq_verdicts_wrong": [f"{r['package']} {r['version'] or '(range)'} in {r['file'].replace('corpus/deps/', '')}: "
                              f"reported {'not ' if r['pq_capable'] else ''}PQC-capable" for r in pq_judged if not r["pq_ok"]],
        "false_positives": fps,
        "missed_not_pq_capable": [f"{r['package']} {r['version'] or ''} ({r['file'].split('/')[-2]})".replace(" (", " (", 1)
                                  for r in results if not r["found_anywhere"] and r["pq_capable"] is False],
        "missed_with_status": [f"{r['package']} {r['version']}: {r['status']}" for r in results
                               if not r["found_anywhere"] and r.get("status")],
        "results": results,
    }


def to_markdown(lib: dict | None) -> str:
    if not lib:
        return ""
    f = lambda v: "n/a" if v is None else f"{v}%"  # noqa: E731
    out = ["## Crypto libraries (dependency manifests)", "",
           f"- Found in the right manifest: **{lib['found_in_manifest']}/{lib['expected']}** ({f(lib['recall'])}); "
           f"found anywhere, including with no location: {lib['found_anywhere']}/{lib['expected']}",
           f"- Direct dependencies: {f(lib['direct_recall'])}; transitive (lockfile): {f(lib['transitive_recall'])}",
           f"- Versions correct, of found libraries the manifest pins (none reported counts as not correct): "
           f"{f(lib['version_accuracy'])}",
           f"- PQC-capability verdicts (where the scanner gives one): "
           + (f"{lib['pq_verdict_accuracy']}% right of {lib['pq_verdicts_judged']}" if lib["pq_verdicts_judged"] else "none given"),
           f"- False positives: {len(lib['false_positives'])}", ""]
    if lib["pq_verdicts_wrong"]:
        out += ["Wrong PQC verdicts: " + "; ".join(lib["pq_verdicts_wrong"]), ""]
    if lib["missed_not_pq_capable"]:
        out += ["Missed, and the declared version has no ML-KEM/ML-DSA: "
                + "; ".join(lib["missed_not_pq_capable"]), ""]
    if lib["missed_with_status"]:
        out += ["Missed, with a support problem: " + "; ".join(lib["missed_with_status"]), ""]
    out += ["| Manifest | Library | Declared | Scope | Found | Version |", "|---|---|---|---|---|---|"]
    for r in lib["results"]:
        found = "yes" if r["found_in_manifest"] else ("no location" if r["found_anywhere"] else "no")
        ver = {"ok": "ok", "wrong": "wrong: " + ", ".join(r["reported_versions"]), "not reported": "not reported",
               "n/a": "n/a"}[r["version_state"]]
        out.append(f"| `{r['file'].replace('corpus/deps/', '')}` | {r['package']} | {r['version'] or 'range'} | {r['scope']} | "
                   f"{found} | {ver} |")
    for x in lib["false_positives"]:
        out.append(f"\n- False positive ({x['kind']}): {x['library']} in `{x['file']}`: {x['why']}")
    return "\n".join(out) + "\n"
