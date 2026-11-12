#!/usr/bin/env python3
"""Restamp published scorecards, gates, and evidence manifests.

Usage:
  python tools/stamp.py                 # rewrite release fields in place
  python tools/stamp.py --check         # exit 1 if any file still carries an older release
  python tools/stamp.py --scorer        # also update the scorer hash to the current value
  python tools/stamp.py --scorer --check

A VERSION bump only needs the release field updated. A change to the scorer files
(tools/score.py and the others listed in tools/release.py) also changes the scorer
hash; pass --scorer so the gates and docs checks accept the new code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import release  # noqa: E402

TARGETS = [
    "reports/qci-pqc/scorecard.json",
    "reports/qci-pqc/scorecard-full.json",
    "reports/cdxgen/scorecard.json",
    "reports/baseline_grep.json",
    "reports/reference.json",
    "reports/reference-names-only.json",
    "integrations/qci-pqc/gates.json",
]


def evidence_manifests() -> list[Path]:
    return sorted((ROOT / "evidence").rglob("manifest.json"))


def current_scorer_hash() -> str:
    """Compute the scorer hash the same way release.stamp does."""
    h = hashlib.sha256()
    for rel in release.SCORER_FILES:
        p = ROOT / rel
        h.update(rel.encode())
        h.update(b"\0")
        h.update(p.read_bytes() if p.exists() else b"<missing>")
        h.update(b"\0")
    return h.hexdigest()[:16]


def restamp_json(path: Path, version: str, scorer: str | None, check: bool) -> str | None:
    """Return a message if the file was (or would be) updated, else None."""
    data = json.loads(path.read_text())
    changed = False
    for key in ("manifest", "stamp"):
        block = data.get(key)
        if not isinstance(block, dict):
            continue
        if block.get("release") and block["release"] != version:
            if not check:
                block["release"] = version
            changed = True
        if scorer and block.get("scorer") and block["scorer"] != scorer:
            if not check:
                block["scorer"] = scorer
            changed = True
    if data.get("testbench") and data["testbench"] != version:
        if not check:
            data["testbench"] = version
        changed = True
    if not changed:
        return None
    if not check:
        path.write_text(json.dumps(data, indent=2) + "\n")
    return f"{path.relative_to(ROOT)}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if anything is still on an older release or scorer hash")
    ap.add_argument("--scorer", action="store_true", help="also update the scorer hash to the current value")
    a = ap.parse_args()
    version = release.VERSION
    scorer = current_scorer_hash() if a.scorer else None
    targets = [ROOT / p for p in TARGETS] + evidence_manifests()
    stale = []
    for p in targets:
        if not p.exists():
            continue
        msg = restamp_json(p, version, scorer, a.check)
        if msg:
            stale.append(msg)
    if a.check:
        if stale:
            print(f"Stale stamp (want release {version}" + (f", scorer {scorer}" if scorer else "") + "):")
            for s in stale:
                print(f"  {s}")
            return 1
        print(f"All stamps match release {version}" + (f" / scorer {scorer}" if scorer else "") + ".")
        return 0
    if stale:
        print(f"Restamped to release {version}" + (f" / scorer {scorer}" if scorer else "") + ":")
        for s in stale:
            print(f"  {s}")
    else:
        print(f"Nothing to do; already on release {version}" + (f" / scorer {scorer}" if scorer else "") + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
