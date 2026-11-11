#!/usr/bin/env python3
"""Reset the ratchet floors in a gates file from scored runs, and stamp it for this release.

  python tools/rebaseline.py reports/qci-pqc-v2.2/scorecard.json reports/qci-pqc/scorecard.json

Each ratchet gate becomes the best value any of the given scorecards reached (highest for a
minimum, lowest for a maximum), so a floor never moves down because a later release regressed.
Policy limits (schema validity, the two holdout gates) are never touched. Scorecards must carry
this release's manifest. Rebaseline first, then run the scanners: a run made before the rebaseline
reports "not evaluated", and the docs check refuses reports and evidence that disagree.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release  # noqa: E402
import run_qci_pqc as r  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scorecards", nargs="+", type=Path)
    ap.add_argument("--gates", type=Path, default=r.INTEGRATION / "gates.json")
    ap.add_argument("--policy", default="nist")
    a = ap.parse_args()
    cur = release.stamp(a.policy)
    ms = {}
    for p in a.scorecards:
        rep = json.loads(p.read_text())
        diff = [k for k in ("release", "methodology", "answer_key", "corpus", "scorer", "policy") if rep.get("manifest", {}).get(k) != cur[k]]
        if diff:
            raise SystemExit(f"{p}: scored on a different {', '.join(diff)}; rescore it on this release first")
        ms[str(p)] = r.metric_rows(rep)
    g = json.loads(a.gates.read_text())
    for key, rule in g["gates"].items():
        if key in r.POLICY_LIMITS:
            continue
        vals = [m[key] for m in ms.values() if m.get(key) is not None]
        if not vals:
            print(f"{key:30} kept at {rule.get('min', rule.get('max'))} (no scorecard measures it)")
            continue
        d = "min" if "min" in rule else "max"
        new = max(vals) if d == "min" else min(vals)
        print(f"{key:30} {d} {rule[d]} -> {new}")
        rule[d] = new
    g.pop("corpus", None)
    g["stamp"] = r.gates_stamp(a.policy)
    g["set_on"] = dt.date.today().isoformat()
    g["set_from"] = [str(p) for p in a.scorecards]
    a.gates.write_text(json.dumps(g, indent=2) + "\n")
    print(f"Stamped {a.gates} for testbench {release.VERSION}. Now rerun the scanners so their reports are judged against it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
