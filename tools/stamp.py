#!/usr/bin/env python3
"""Restamp published scorecards, gates, and evidence manifests to the current VERSION.

Usage:
  python tools/stamp.py              # rewrite release fields in place
  python tools/stamp.py --check      # exit 1 if any file still carries an older release

Only the release field is updated. Corpus, answer-key, scorer, and policy hashes are left
alone; a real rescan is required when those change. This tool exists so a patch-level
VERSION bump does not leave CI red because published artifacts still say the previous release.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import release  # noqa: E402

TARGETS = [
    # published scorecards
    "reports/qci-pqc/scorecard.json",
    "reports/qci-pqc/scorecard-full.json",
    "reports/cdxgen/scorecard.json",
    "reports/baseline_grep.json",
    "reports/reference.json",
    "reports/reference-names-only.json",
    # gates
    "integrations/qci-pqc/gates.json",
]


def evidence_manifests() -> list[Path]:
    return sorted((ROOT / "evidence").rglob("manifest.json"))


def restamp_json(path: Path, version: str, check: bool) -> str | None:
    """Return a message if the file was (or would be) updated, else None."""
    data = json.loads(path.read_text())
    changed = False
    # scorecards carry a manifest; gates and evidence manifests carry a stamp
    for key in ("manifest", "stamp"):
        block = data.get(key)
        if isinstance(block, dict) and block.get("release") and block["release"] != version:
            if not check:
                block["release"] = version
            changed = True
    # some manifests use a top-level testbench field
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
    ap.add_argument("--check", action="store_true", help="exit 1 if anything is still on an older release")
    a = ap.parse_args()
    version = release.VERSION
    targets = [ROOT / p for p in TARGETS] + evidence_manifests()
    stale = []
    for p in targets:
        if not p.exists():
            continue
        msg = restamp_json(p, version, a.check)
        if msg:
            stale.append(msg)
    if a.check:
        if stale:
            print(f"Stale release stamp (want {version}):")
            for s in stale:
                print(f"  {s}")
            return 1
        print(f"All stamps match {version}.")
        return 0
    if stale:
        print(f"Restamped to {version}:")
        for s in stale:
            print(f"  {s}")
    else:
        print(f"Nothing to do; already on {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
