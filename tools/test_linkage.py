#!/usr/bin/env python3
"""System fixture: CODEOWNERS routing and asset links.

Run: python tools/test_linkage.py
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import linkage  # noqa: E402
from cbomlib import load_json, make_component, same_file  # noqa: E402
from score import score  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REF = load_json(ROOT / "expected" / "expected.cdx.json")
P = "corpus/system/payments-platform/"


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return bool(cond)


def drop_located(bom, file):
    for c in bom["components"]:
        occ = (c.get("evidence") or {}).get("occurrences")
        if occ:
            occ[:] = [o for o in occ if not same_file(o.get("location", ""), file)]
    bom["components"] = [c for c in bom["components"] if (c.get("evidence") or {}).get("occurrences") != []]


def main() -> int:
    ok = True
    rules = linkage.parse_codeowners(ROOT / P / "CODEOWNERS")
    for rel, want in (("services/api-gateway/main.go", "@acme/edge-team"),
                      ("services/api-gateway/bin/api-gateway", "@acme/edge-team"),
                      ("libs/cryptokit/go/cryptokit.go", "@acme/platform-security"),
                      ("config/crypto-profiles.json", "@acme/platform-security"),
                      ("infra/terraform/kms.tf", "@acme/sre"),
                      ("README.md", "@acme/platform-architecture")):
        ok &= check(f"CODEOWNERS: {rel} -> {want}", linkage.owner_of(rel, rules) == want)

    lk = score(REF, custom="exclude")["linkage"]
    ok &= check("reference: every system finding routable, both asset links found",
                lk["routable"] == lk["detected"] == lk["system_findings"] and lk["links_found"] == lk["links_expected"] == 2)

    # Only the wrapper reports the gateway's RSA: detected (alt file), routed to the wrong team.
    bom = copy.deepcopy(REF)
    drop_located(bom, P + "services/api-gateway/main.go")
    bom["components"].append(make_component("wrap-rsa", "RSA", {"key_size": 2048},
                                            [{"location": P + "libs/cryptokit/go/cryptokit.go", "line": 47}]))
    rep = score(bom, custom="exclude")
    r = next(x for x in rep["results"] if x["id"] == "SYS-GO-01")
    mis = {m["id"]: m for m in rep["linkage"]["misrouted"]}
    ok &= check("wrapper-only report: detected, not at the call site, routed to platform-security",
                r["detected"] and not r["at_usage_site"] and mis.get("SYS-GO-01", {}).get("routed_to") == ["@acme/platform-security"])

    # The config line is shared by two services: one report there routes neither.
    bom = copy.deepcopy(REF)
    drop_located(bom, P + "services/api-gateway/main.go")
    drop_located(bom, P + "services/settlement-worker/worker.py")
    cfg = P + "config/crypto-profiles.json"
    line = next(i for i, t in enumerate((ROOT / cfg).read_text().splitlines(), 1) if '"webhook-signature"' in t)
    bom["components"].append(make_component("cfg-hmac", "HMAC", {"hash": "SHA-1"}, [{"location": cfg, "line": line}]))
    rep = score(bom, custom="exclude")
    mis = {m["id"] for m in rep["linkage"]["misrouted"]}
    ok &= check("one report on the shared config line: both HMAC findings detected, neither routable",
                {"SYS-GO-02", "SYS-PY-02"} <= mis)

    bom = copy.deepcopy(REF)
    bom["dependencies"] = [d for d in bom.get("dependencies", []) if "dependsOn" not in d]
    ok &= check("no dependency links -> 0/2 asset links", score(bom, custom="exclude")["linkage"]["links_found"] == 0)
    bom = copy.deepcopy(REF)
    bom["dependencies"] = [d for d in bom.get("dependencies", []) if "dependsOn" not in d]
    for c in bom["components"]:
        if c.get("cryptoProperties", {}).get("assetType") == "protocol" and any(
                same_file(o.get("location", ""), P + "edge/nginx/gateway.conf") for o in c["evidence"]["occurrences"]):
            cert = next(x["bom-ref"] for x in bom["components"] if x.get("cryptoProperties", {}).get("assetType") == "certificate"
                        and any(same_file(o.get("location", ""), P + "edge/nginx/tls/gateway.crt") for o in x["evidence"]["occurrences"]))
            c["cryptoProperties"]["protocolProperties"]["cryptoRefArray"] = [cert]
    ok &= check("protocol names its certificate in cryptoRefArray -> that link found",
                score(bom, custom="exclude")["linkage"]["links_found"] == 1)

    print("\nAll linkage checks pass." if ok else "\nLinkage checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
