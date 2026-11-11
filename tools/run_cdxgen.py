#!/usr/bin/env python3
"""Score cdxgen's CBOM mode against the testbench, in one command.

  python tools/run_cdxgen.py                        # uses `cbom` on PATH
  python tools/run_cdxgen.py --install              # npm-installs @cyclonedx/cdxgen@12.9.1 into .cdxgen/
  python tools/run_cdxgen.py --cbom-bin path/to/cbom

Scans a copy of corpus/ (cdxgen writes analysis files next to what it scans) with
`cbom --spec-version 1.6 --no-install-deps --evidence`, translates the result
(tools/adapters/cdxgen.py), scores it, and writes reports/cdxgen/. No gates: this is a comparison
point, not a CI target.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import cdxgen  # noqa: E402
from score import load_truth, score, to_markdown  # noqa: E402
import actionability as act  # noqa: E402
from run_qci_pqc import metric_rows  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
VERSION = "12.9.1"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--cbom-bin", help="cdxgen's `cbom` executable (default: on PATH)")
    g.add_argument("--install", action="store_true", help=f"npm install @cyclonedx/cdxgen@{VERSION} into .cdxgen/")
    ap.add_argument("--policy", default="nist")
    ap.add_argument("--out", type=Path, default=ROOT / "reports" / "cdxgen")
    a = ap.parse_args()

    exe = a.cbom_bin or shutil.which("cbom")
    if a.install:
        d = ROOT / ".cdxgen"
        d.mkdir(exist_ok=True)
        r = subprocess.run(["npm", "install", "--no-audit", "--no-fund", "--prefix", str(d), f"@cyclonedx/cdxgen@{VERSION}"],
                           capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"npm install failed:\n{r.stderr[-1500:]}")
        exe = str(d / "node_modules" / ".bin" / "cbom")
    if not exe:
        raise SystemExit("cdxgen's `cbom` not found: pass --cbom-bin or --install")
    import re
    out = subprocess.run([exe, "--version"], capture_output=True, text=True).stdout
    version = (re.sub(r"\x1b\[[0-9;]*m", "", out).strip().splitlines() or ["?"])[0]
    print(f"Scanner: {version}")

    raw = a.out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cdxgen-scan-") as tmp:
        target = Path(tmp) / "corpus"  # keep the name: locations then read corpus/tier1/...
        shutil.copytree(ROOT / "corpus", target)
        print("Scanning a copy of corpus/ ...")
        r = subprocess.run([exe, "--spec-version", "1.6", "--no-install-deps", "--evidence", "-o", str(raw / "cbom.json"),
                            str(target)], capture_output=True, text=True, cwd=tmp)
        (raw / "log.txt").write_text(r.stdout + r.stderr)
    if not (raw / "cbom.json").exists():
        raise SystemExit("cdxgen produced no CBOM; see raw/log.txt")
    cbom = json.loads((raw / "cbom.json").read_text())

    bom, signals, notes = cdxgen.translate(cbom)
    (a.out / "cdxgen.cdx.json").write_text(json.dumps(bom, indent=2) + "\n")
    rep = score(bom, policy=a.policy, custom="exclude")
    rep["manifest"].update(scanner=version, adapter=f"cdxgen {cdxgen.ADAPTER_VERSION}")
    gt = load_truth(include_custom=False)[0]
    sc = cdxgen.signal_coverage(rep, gt, signals, act.material_index(gt))
    name = f"{version} (adapter {cdxgen.ADAPTER_VERSION})"
    (a.out / "scorecard.md").write_text(to_markdown(name, rep))
    (a.out / "scorecard.json").write_text(json.dumps({**rep, "signal_coverage": sc, "adapter_notes": notes},
                                                     indent=2, default=str) + "\n")
    m = metric_rows(rep)
    summary = [f"# cdxgen on the CBOM Testbench", "", f"- Scanner: **{version}**, `cbom --spec-version 1.6 --no-install-deps --evidence`",
               f"- Translation: `tools/adapters/cdxgen.py` {cdxgen.ADAPTER_VERSION}: {notes['renamed_hmac_kdf']} HMAC/PBKDF2 renames, "
               f"{notes['crypto_files']} crypto-file entries scored as signals, {notes['unlocated_algorithms']} algorithms with no location",
               "", "| Metric | Value |", "|---|---|"]
    for k, v in m.items():
        summary.append(f"| {k.replace('_', ' ')} | {v} |")
    summary += ["", f"Signal coverage: crypto-file entries cover {sc['signal_only']} more expected findings "
                f"(combined {sc['combined']}/{sc['expected']}, {sc['combined_recall']}%).", ""]
    (a.out / "SUMMARY.md").write_text("\n".join(summary) + "\n")
    print("\n".join(summary[6:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
