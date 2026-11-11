#!/usr/bin/env python3
"""Gate enforcement: a baseline is enforced only on the stamp it was set on, and a run that
evaluated nothing never exits 0 unless it was asked to be report-only.

Run: python tools/test_gates.py
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_qci_pqc as r  # noqa: E402


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return cond


def main() -> int:
    ok = True
    stamp = r.gates_stamp("nist")
    m = {"recall": 70.0, "precision": 95.0}
    gates = {"gates": {"recall": {"min": 60.0}, "precision": {"min": 90.0}}, "stamp": copy.deepcopy(stamp)}

    ev = r.evaluate_gates(gates, m, stamp)
    ok &= check("matching stamp, numbers above the floors -> pass, exit 0", ev["status"] == "pass" and ev["code"] == 0)

    ev = r.evaluate_gates(gates, {**m, "recall": 50.0}, stamp)
    ok &= check("matching stamp, a floor missed -> fail, exit 1", ev["status"] == "fail" and ev["code"] == 1)

    stale = copy.deepcopy(gates)
    stale["stamp"]["release"] = "1.16.2"
    ev = r.evaluate_gates(stale, {**m, "recall": 50.0}, stamp)
    ok &= check("baseline from another release -> not evaluated, exit 3 (even though a floor is missed)",
                ev["status"] == "not_evaluated" and ev["code"] == 3 and "release" in ev["why"])

    for key in ("methodology", "answer_key", "corpus", "scorer", "policy", "adapter"):
        s2 = copy.deepcopy(gates)
        s2["stamp"][key] = "0" * 16
        ev = r.evaluate_gates(s2, m, stamp)
        ok &= check(f"{key} changed since the baseline -> exit 3", ev["code"] == 3 and key in ev["why"])

    legacy = {"gates": gates["gates"], "corpus": {"findings": 304, "sha256": "dd40e72c3d35a960"}}
    ev = r.evaluate_gates(legacy, m, stamp)
    ok &= check("pre-1.17 corpus stamp -> exit 3, says so", ev["code"] == 3 and "pre-1.17" in ev["why"])

    ev = r.evaluate_gates({"gates": gates["gates"]}, m, stamp)
    ok &= check("unstamped gates -> exit 3", ev["code"] == 3)

    ev = r.evaluate_gates({"gates": {}}, m, stamp)
    ok &= check("no gates configured -> exit 3", ev["code"] == 3)

    ev = r.evaluate_gates(stale, m, stamp, report_only=True)
    ok &= check("report-only -> exit 0 but still says not evaluated", ev["code"] == 0 and ev["status"] == "not_evaluated")
    ev = r.evaluate_gates(gates, {**m, "recall": 50.0}, stamp, report_only=True)
    ok &= check("report-only with a failing gate -> exit 0, failure still listed", ev["code"] == 0 and bool(ev["fails"]))

    # --- Missing measurements (v2.1 review): a current baseline with nothing measured must not pass.
    shipped = r.json.loads((r.INTEGRATION / "gates.json").read_text())
    ok &= check("the shipped gates.json is stamped for this exact release", not r.release.stamp_diff(shipped["stamp"], stamp))
    ev = r.evaluate_gates(shipped, {}, stamp)
    ok &= check("shipped baseline, no metrics at all -> not evaluated, exit 3, every required gate listed as missing",
                ev["status"] == "not_evaluated" and ev["code"] == 3 and "recall" in ev["missing"] and "cbom_schema_valid" in ev["missing"])
    full = {k: (rule.get("min", rule.get("max"))) for k, rule in shipped["gates"].items()}
    ev = r.evaluate_gates(shipped, full, stamp)
    ok &= check("every measurement present and on its floor -> pass, exit 0", ev["status"] == "pass" and ev["code"] == 0 and not ev["missing"])
    for gone in ("cbom_schema_valid", "overfit_gap_ci_low", "negative_fp_gap", "precision"):
        ev = r.evaluate_gates(shipped, {k: v for k, v in full.items() if k != gone}, stamp)
        ok &= check(f"{gone} not measured -> not evaluated, exit 3", ev["code"] == 3 and ev["missing"] == [gone])
    ev = r.evaluate_gates(shipped, {k: v for k, v in full.items() if k not in r.HOLDOUT_GATES}, stamp,
                          without={k: "run made without a holdout set (--without-holdout)" for k in r.HOLDOUT_GATES})
    ok &= check("holdout gates explicitly waived -> pass, both listed as skipped with the reason",
                ev["status"] == "pass" and {x["gate"] for x in ev["skipped"]} == r.HOLDOUT_GATES and all(x["reason"] for x in ev["skipped"]))
    ev = r.evaluate_gates(shipped, {k: v for k, v in full.items() if k != "library_pq_verdict_accuracy"}, stamp)
    ok &= check("a gate marked when_missing: skip -> skipped with its reason, not missing",
                ev["status"] == "pass" and [x["gate"] for x in ev["skipped"]] == ["library_pq_verdict_accuracy"])
    ev = r.evaluate_gates(shipped, {**{k: v for k, v in full.items() if k != "precision"}, "recall": 0}, stamp)
    ok &= check("one gate failed and another missing -> fail (exit 1), and the missing one is still reported",
                ev["status"] == "fail" and ev["code"] == 1 and ev["missing"] == ["precision"])
    md = "\n".join(r.gates_markdown(ev))
    ok &= check("the rendered verdict names failures, missing and skipped", "FAILED" in md and "NOT EVALUATED" in md and "precision" in md)

    print("\nAll gate checks pass." if ok else "\nGate checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
