#!/usr/bin/env python3
"""Five-seed calibration of the overfit gap and the negative-control gap.

  python tools/recalibrate.py --qci-bin /path/to/venv/bin/qci-pqc [--seeds 1234 4242 55 777 90210]

For each seed: generate a holdout set, check every generated file runs, then score the answer key,
the grep baseline and the QCI scanner on it against their published scorecards. Prints one line per
scanner and seed and a summary. The answer key must read 0 on every seed; a control whose interval
excludes zero means the generator, not the scanner, needs fixing (HOLDOUT.md, "Calibration").

The seeds here are public, so these sets are for calibrating the metric, not for judging a scanner.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import holdout as ho  # noqa: E402
from adapters import qci_pqc  # noqa: E402
from score import load_scope  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--qci-bin", help="qci-pqc executable; omit to calibrate the controls only")
    ap.add_argument("--seeds", nargs="+", type=int, default=[1234, 4242, 55, 777, 90210])
    ap.add_argument("--out", type=Path, help="write the rows as JSON")
    a = ap.parse_args()
    pub = {"answer key": json.loads((ROOT / "reports/reference.json").read_text()),
           "grep": json.loads((ROOT / "reports/baseline_grep.json").read_text())}
    scope = None
    if a.qci_bin:
        pub["QCI"] = json.loads((ROOT / "reports/qci-pqc/scorecard.json").read_text())
        scope = load_scope(str(ROOT / "integrations/qci-pqc/scope.json"))
    rows, work = [], Path(tempfile.mkdtemp(prefix="recalibrate-"))
    try:
        for seed in a.seeds:
            d = work / str(seed)
            ho.generate(seed, d)
            unrunnable = ho.verify(d)
            if unrunnable:
                print(f"seed {seed}: {len(unrunnable)} generated files don't run, e.g. {unrunnable[0]}")
                return 1
            for name in pub:
                sc = None
                if name == "answer key":
                    bom = json.loads((d / "expected.cdx.json").read_text())
                elif name == "grep":
                    subprocess.run([sys.executable, str(ROOT / "tools/baseline_grep.py"), str(d / "corpus"), "-o", str(work / "grep.cdx.json")],
                                   capture_output=True, check=True)
                    bom = json.loads((work / "grep.cdx.json").read_text())
                else:
                    out = work / "scan"
                    shutil.rmtree(out, ignore_errors=True)
                    subprocess.run([a.qci_bin, "scan", str(d / "corpus"), "--reproducible", "--adapter", "internal", "--out", str(out), "--json"],
                                   capture_output=True, check=True)
                    bom, _, _ = qci_pqc.translate(json.loads((out / "cbom.json").read_text()))
                    sc = scope
                h = ho.score_holdout(bom, d, "nist", sc)
                g, n = ho.overfit_gap(pub[name], h), ho.negative_gap(pub[name], h, d)
                rows.append({"seed": seed, "scanner": name, "gap": g["gap"], "ci95": g["gap_ci95"], "significant": g["significant"],
                             "cells": g["cells"], "negative_gap": n["gap_per_file"], "findings": len(h["results"])})
                r = rows[-1]
                print(f"seed {seed:>6}  {name:<10} gap {r['gap']:+5.1f}  interval {r['ci95'][0]:+5.1f} to {r['ci95'][1]:+5.1f}"
                      f"{'  SIGNIFICANT' if r['significant'] else ''}  negatives {r['negative_gap']:+.2f}  ({r['cells']} cells)", flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print()
    bad = 0
    for name in pub:
        rs = [r for r in rows if r["scanner"] == name]
        widths = [r["ci95"][1] - r["ci95"][0] for r in rs]
        print(f"{name:<10} gap {min(r['gap'] for r in rs):+.1f} to {max(r['gap'] for r in rs):+.1f}, {sum(r['significant'] for r in rs)} significant; "
              f"interval width {min(widths):.1f} to {max(widths):.1f}; negatives {min(r['negative_gap'] for r in rs):+.2f} to {max(r['negative_gap'] for r in rs):+.2f}")
        if name == "answer key" and any(r["gap"] != 0 for r in rs):
            bad = 1
    if a.out:
        a.out.write_text(json.dumps(rows, indent=1) + "\n")
    if bad:
        print("\nThe answer key does not read 0 on every seed: the generator or the matching is wrong.")
    return bad


if __name__ == "__main__":
    sys.exit(main())
