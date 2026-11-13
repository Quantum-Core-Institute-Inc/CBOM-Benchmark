#!/usr/bin/env python3
"""Report which published scorecards, gates and evidence bundles were measured on another release.

  python tools/stamp.py            # list what is stale; exit 1 if anything is
  python tools/stamp.py --check    # the same (kept for scripts that pass it)

This tool used to rewrite the release field and scorer hash in place. It no longer does. A stamp
says what a number was measured on: the release, corpus, answer key, scorer and policy. Editing it
makes a scorecard claim a measurement that didn't happen, and an edited evidence manifest stops
verifying (`bench.py verify` re-derives every number and checks every file hash). After any change
to VERSION, the corpus, the answer key, the scorer or a policy, measure again:

  tools/release_run.sh
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import release  # noqa: E402

TARGETS = ["reports/qci-pqc/scorecard.json", "reports/qci-pqc/scorecard-full.json", "reports/cdxgen/scorecard.json",
           "reports/baseline_grep.json", "reports/reference.json", "reports/reference-names-only.json",
           "integrations/qci-pqc/gates.json"]
FIELDS = ("release", "methodology", "findings", "answer_key", "corpus", "scorer")


def stale_fields(path: Path, cur: dict) -> list[str]:
    data = json.loads(path.read_text())
    block = data.get("manifest") if isinstance(data.get("manifest"), dict) else data.get("stamp")
    if not isinstance(block, dict):
        if "testbench" in data:   # a timing bundle: no scores, so it records the release and methodology only
            return [f"{k} {data.get(k)} (now {v})" for k, v in (("testbench", cur["release"]), ("methodology", cur["methodology"]))
                    if data.get(k) != v]
        return ["no stamp"]
    return [f"{k} {block.get(k)} (now {cur[k]})" for k in FIELDS if k in block and block.get(k) != cur[k]]


def main() -> int:
    cur = release.stamp("nist")
    stale = []
    for p in [ROOT / t for t in TARGETS] + sorted((ROOT / "evidence").rglob("manifest.json")):
        if p.exists():
            diff = stale_fields(p, cur)
            if diff:
                stale.append(f"  {p.relative_to(ROOT)}: {'; '.join(diff)}")
    if stale:
        print(f"Measured on something other than this tree (release {cur['release']}):")
        print("\n".join(stale))
        print("\nThese can't be restamped. Run tools/release_run.sh to measure them again.")
        return 1
    print(f"Every published scorecard, gate file and evidence bundle was measured on release {cur['release']}.")
    if release.REVISION:
        print(f"Published as {release.PUBLISHED}: results revision {release.REVISION} of {cur['release']}, nothing rescored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
