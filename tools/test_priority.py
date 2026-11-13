#!/usr/bin/env python3
"""Priority agreement: reading a scanner's urgency, and comparing its order with the deadlines.

Run: python tools/test_priority.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import priority  # noqa: E402
from adapters import sarif  # noqa: E402

BUCKETS = {"now": {"label": "Due now", "weight": 5}, "by-2030": {"label": "Due by end of 2030", "weight": 4},
           "2034-2035": {"label": "Due 2034 to 2035", "weight": 2}, "none": {"label": "No deadline", "weight": 0}}
FINDINGS = [("F1", "MD5", "now"), ("F2", "3DES", "now"), ("F3", "RSA", "by-2030"), ("F4", "EC", "2034-2035"), ("F5", "AES", "none")]
NAMES = {"MD5": "MD5", "3DES": "3DES", "RSA": "RSA-1024", "EC": "ECDSA-P256", "AES": "AES-256-GCM"}


def rep(detected=("F1", "F2", "F3", "F4", "F5")):
    return {"deadlines": {"buckets": BUCKETS},
            "results": [{"id": i, "tier": 1, "family": fam, "file": f"corpus/{i}.py", "due_bucket": b, "detected": i in detected,
                         "reported_files": [f"corpus/{i}.py"] if i in detected else []} for i, fam, b in FINDINGS]}


def bom(urgency: dict, prop="acme:severity", vulns=None):
    comps = []
    for i, fam, _ in FINDINGS:
        c = {"type": "cryptographic-asset", "name": NAMES[fam], "bom-ref": i,
             "cryptoProperties": {"assetType": "algorithm", "algorithmProperties": {}},
             "evidence": {"occurrences": [{"location": f"corpus/{i}.py", "line": 3}]}}
        if i in urgency:
            c["properties"] = [{"name": prop, "value": urgency[i]}]
        comps.append(c)
    return {"bomFormat": "CycloneDX", "specVersion": "1.6", "components": comps, **({"vulnerabilities": vulns} if vulns else {})}


def main() -> int:
    bad = []

    def check(name, ok):
        if not ok:
            bad.append(name)
        print(("ok   " if ok else "FAIL ") + name)

    ev = priority.evaluate(bom({"F1": "critical", "F2": "critical", "F3": "high", "F4": "low", "F5": "info"}), rep())
    check("the policy's own order scores 100%", (ev["verdict"], ev["agreement_pct"], ev["disagree"]) == ("measured", 100.0, 0))
    check("pairs are only between findings with different, dated deadlines (F1/F2 share one; F5 has none)", ev["pairs"] == 5)
    check("the source and coverage are reported", ev["source"] == "property acme:severity" and ev["coverage_pct"] == 100.0 and ev["with_urgency"] == 5)

    ev = priority.evaluate(bom({"F1": "low", "F2": "low", "F3": "medium", "F4": "critical", "F5": "info"}), rep())
    check("the reverse order scores 0%", ev["agreement_pct"] == 0.0 and ev["disagree"] == 5)
    check("the largest disagreement is named: something due now ranked below something due in 2035",
          ev["worst"][0]["due_sooner"]["bucket"] == "now" and ev["worst"][0]["ranked_above_it"]["id"] == "F4")

    ev = priority.evaluate(bom({i: "high" for i, _, _ in FINDINGS}), rep())
    check("one level for everything is no order: 'one level only', and 50%", ev["verdict"] == "one level only" and ev["agreement_pct"] == 50.0)

    ev = priority.evaluate(bom({}), rep())
    check("no priority field at all -> 'no priority given'", ev["verdict"] == "no priority given" and ev["source"] is None)

    ev = priority.evaluate(bom({"F1": "critical", "F2": "critical", "F3": "high", "F4": "low", "F5": "critical"}), rep())
    check("an undated finding ranked at the top costs nothing: the policy does not say how urgent it is", ev["agreement_pct"] == 100.0)
    check("... and is still shown in the table, marked as not compared",
          [b for b in ev["by_deadline"] if b["bucket"] == "none"][0]["compared"] is False)

    ev = priority.evaluate(bom({"F1": 90, "F2": "85", "F3": 60, "F4": 10}, prop="x:priority_score"), rep())
    check("numbers are read as written, higher more urgent; a finding without one is left out",
          (ev["agreement_pct"], ev["with_urgency"], ev["coverage_pct"]) == (100.0, 4, 80.0))
    ev = priority.evaluate(bom({"F1": "P1", "F2": "P1", "F3": "P2", "F4": "P4"}, prop="priority"), rep())
    check("P1 is more urgent than P4", ev["agreement_pct"] == 100.0)

    ev = priority.evaluate(bom({"F1": "critical", "F3": "high", "F4": "low"}), rep(detected=("F1", "F3")))
    check("only detected findings are compared", (ev["detected"], ev["with_urgency"], ev["pairs"]) == (2, 2, 1))

    mixed = bom({"F1": "critical", "F2": "critical", "F3": "high", "F4": "low"})
    mixed["components"][0]["properties"].append({"name": "acme:risk", "value": "low"})
    ev = priority.evaluate(mixed, rep())
    check("one property is used for the whole CBOM (the one most components carry); scales are not mixed",
          ev["source"] == "property acme:severity" and ev["agreement_pct"] == 100.0)

    vulns = [{"id": "W1", "ratings": [{"severity": "critical"}], "affects": [{"ref": "F1"}, {"ref": "F2"}]},
             {"id": "W2", "ratings": [{"severity": "medium"}, {"severity": "high"}], "affects": [{"ref": "F3"}]},
             {"id": "W3", "ratings": [{"severity": "low"}], "affects": [{"ref": "F4"}]}]
    ev = priority.evaluate(bom({"F1": "low"}, vulns=vulns), rep())
    check("vulnerability ratings are used when present, the highest per component",
          ev["source"] == "vulnerabilities[].ratings" and ev["agreement_pct"] == 100.0 and ev["with_urgency"] == 4)

    # SARIF tools: the adapter carries the tool's level or security-severity onto the component.
    doc = {"runs": [{"tool": {"driver": {"name": "T", "rules": [
        {"id": "crypto.use-of-md5", "properties": {"tags": ["CWE-327"], "security-severity": "7.5"}},
        {"id": "crypto.weak-rsa-key", "properties": {"tags": ["CWE-326"], "security-severity": "5.0"}}]}},
        "results": [{"ruleId": "crypto.use-of-md5", "message": {"text": "MD5"}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": "corpus/F1.py"}, "region": {"startLine": 3}}}]},
                    {"ruleId": "crypto.weak-rsa-key", "message": {"text": "RSA key of 1024 bits"}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": "corpus/F3.py"}, "region": {"startLine": 3}}}]}]}]}
    sbom, _, _ = sarif.translate(doc)
    props = {c["name"]: {p["name"]: p["value"] for p in c["properties"]} for c in sbom["components"]}
    check("the SARIF adapter carries security-severity onto each component",
          props["MD5"].get("sarif:security-severity") == "7.5" and props["RSA"].get("sarif:security-severity") == "5")
    ev = priority.evaluate(sbom, rep(detected=("F1", "F3")))
    check("... and it is read as the tool's urgency", ev["source"] == "property sarif:security-severity" and ev["agreement_pct"] == 100.0)
    doc["runs"][0]["tool"]["driver"]["rules"] = [{"id": "crypto.use-of-md5", "properties": {"tags": ["CWE-327"]}},
                                                 {"id": "crypto.weak-rsa-key", "properties": {"tags": ["CWE-326"]}}]
    doc["runs"][0]["results"][0]["level"] = "error"
    doc["runs"][0]["results"][1]["level"] = "note"
    sbom, _, _ = sarif.translate(doc)
    ev = priority.evaluate(sbom, rep(detected=("F1", "F3")))
    check("without a score, the SARIF level is used (error above note)", ev["source"] == "property sarif:level" and ev["agreement_pct"] == 100.0)

    check("the cell says it in words",
          priority.cell(None) == "not measured" and priority.cell(priority.evaluate(bom({}), rep())) == "no priority given"
          and priority.cell(ev) == "100.0% (100.0% of detections carry a priority)")
    md = priority.markdown(priority.evaluate(bom({"F1": "low", "F2": "low", "F3": "medium", "F4": "critical", "F5": "info"}), rep()), "X")
    check("the report names the property read and the worst disagreement", "property acme:severity" in md and "below F4 EC" in md)

    print("\nAll priority checks pass." if not bad else f"\n{len(bad)} FAILED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
