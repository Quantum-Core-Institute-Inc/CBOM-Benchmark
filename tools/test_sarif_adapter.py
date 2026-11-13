#!/usr/bin/env python3
"""SARIF adapter checks (no scanner needed). Run: python tools/test_sarif_adapter.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import sarif  # noqa: E402


def result(rule, message, uri="src/a.py", line=3):
    return {"ruleId": rule, "message": {"text": message},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}, "region": {"startLine": line}}}]}


def run(tool, rules, results):
    return {"tool": {"driver": {"name": tool, "semanticVersion": "1.0.0", "rules": rules}}, "results": results}


def rule(rid, tags=(), short=""):
    return {"id": rid, "shortDescription": {"text": short}, "properties": {"tags": list(tags)}}


def main() -> int:
    bad = []

    def check(name, ok):
        if not ok:
            bad.append(name)
        print(("ok   " if ok else "FAIL ") + name)

    md5 = "python.lang.security.insecure-hash-algorithms-md5.insecure-hash-algorithm-md5"
    doc = {"runs": [
        run("Semgrep OSS", [rule(md5, ["CWE-327: Use of a Broken or Risky Cryptographic Algorithm"]),
                            rule("java.lang.security.audit.crypto.des-is-deprecated.des-is-deprecated", ["CWE-326"]),
                            rule("java.lang.security.audit.crypto.ecb-cipher.ecb-cipher", ["CWE-327"]),
                            rule("python.lang.security.audit.eval-detected.eval-detected", ["CWE-95"])],
            [result(md5, "Detected MD5 hash algorithm which is considered insecure. Use SHA256 or SHA3 instead.", "t/a.py", 5),
             result("java.lang.security.audit.crypto.des-is-deprecated.des-is-deprecated", "DES is considered deprecated. AES is the recommended cipher.", "t/B.java", 9),
             result("java.lang.security.audit.crypto.ecb-cipher.ecb-cipher", "Cipher in ECB mode is detected.", "t/C.java", 4),
             result("python.lang.security.audit.eval-detected.eval-detected", "Detected eval of an md5 string.", "t/d.py", 1)]),
        run("CodeQL", [rule("java/weak-cryptographic-algorithm", ["security", "external/cwe/cwe-327"], "Use of a broken or risky cryptographic algorithm"),
                       rule("py/weak-crypto-key", ["external/cwe/cwe-326"], "Use of weak cryptographic key")],
            [result("java/weak-cryptographic-algorithm", "Cryptographic algorithm [DES/ECB/PKCS5Padding](1) is weak and should not be used.", "t/E.java", 7),
             result("py/weak-crypto-key", "Creation of an RSA key uses [1024](1) bits, which is below 2048 and considered breakable.", "t/f.py", 4)]),
    ]}
    bom, signals, notes = sarif.translate(doc)
    by = {(c["name"], tuple(sorted(c["cryptoProperties"]["algorithmProperties"].items()))): c for c in bom["components"]}

    check("a rule id that names an algorithm gives that algorithm", ("MD5", ()) in by)
    check("an algorithm a message only recommends is not reported",
          not any(n.startswith(("SHA-256", "SHA3", "AES")) for n, _ in by))
    check("the occurrence carries the result's file and line",
          by[("MD5", ())]["evidence"]["occurrences"] == [{"location": "t/a.py", "line": 5}])
    check("a CodeQL message names the algorithm and its mode", ("DES", (("mode", "ecb"),)) in by)
    check("a key size in the message is kept", ("RSA", (("parameterSetIdentifier", "1024"),)) in by)
    check("a crypto result that names no algorithm becomes no component, and is counted",
          notes["unnamed"] == 1 and "java.lang.security.audit.crypto.ecb-cipher.ecb-cipher" in notes["unnamed_rules"])
    check("a rule that is not about cryptography is dropped, whatever its message says",
          notes["results"] == 6 and notes["crypto_results"] == 5 and not any("eval" in r for r in notes["rules_used"]))
    check("both tools are recorded", notes["tools"] == ["Semgrep OSS 1.0.0", "CodeQL 1.0.0"])
    check("the output is a CycloneDX 1.6 BOM of cryptographic assets",
          bom["bomFormat"] == "CycloneDX" and bom["specVersion"] == "1.6"
          and all(c["type"] == "cryptographic-asset" for c in bom["components"]))
    check("names inside longer names are not double counted",
          sarif.algorithms_in("use of 3des and sha-512, never des-ede3") == ["3DES", "SHA-512"])
    check("an empty document gives an empty BOM", sarif.translate({})[0]["components"] == [])

    print("\nAll SARIF adapter checks pass." if not bad else f"\n{len(bad)} FAILED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
