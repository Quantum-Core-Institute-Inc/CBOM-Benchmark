#!/usr/bin/env python3
"""Run the QCI PQC Readiness Scanner against the testbench and score it, in one command.

  # from a checkout of github.com/Quantum-Core-Institute-Inc/qci-pqc-scanner
  python tools/run_qci_pqc.py --scanner ../qci-pqc-scanner

  # or with qci-pqc already installed
  python tools/run_qci_pqc.py --qci-bin qci-pqc

Steps: install the scanner into its own virtualenv (.qci-venv/) unless --qci-bin is given; scan
corpus/ with --reproducible; translate its CBOM (tools/adapters/qci_pqc.py); score it against the
scanner's declared scope (integrations/qci-pqc/scope.json) and without it; measure risk-signal
coverage; with --holdout-seed (or CBOM_HOLDOUT_SEED), generate a private holdout set, scan it and
report the overfit gap (tools/holdout.py); write reports/qci-pqc/SUMMARY.md; check
integrations/qci-pqc/gates.json.

Exit codes, so CI can tell them apart:
  0  every gate evaluated and passed (or --report-only)
  1  a gate failed
  3  gates were NOT evaluated: no gates file, or a baseline stamped for a different testbench
     release, answer key, corpus, scorer, policy or adapter. Review the run, then --rebaseline.
--report-only (alias --no-gate) writes the reports, shows what the gates would say, and exits 0;
its summary is labelled REPORT ONLY so a green job can't be mistaken for an evaluated one.
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import tempfile
import json
import os
import subprocess
import sys
import venv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import qci_pqc  # noqa: E402
from score import load_scope, load_truth, score, to_markdown  # noqa: E402
import actionability as act  # noqa: E402
import holdout as ho  # noqa: E402
import release  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INTEGRATION = ROOT / "integrations" / "qci-pqc"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def install(scanner: Path, venv_dir: Path) -> Path:
    py = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "python"
    if not py.exists():
        print(f"Creating virtualenv {venv_dir.relative_to(ROOT) if venv_dir.is_relative_to(ROOT) else venv_dir}")
        venv.create(venv_dir, with_pip=True)
    print(f"Installing scanner from {scanner}")
    # Installing runs the scanner's build code, and needs the network, so it can't go in the sandbox.
    # It gets no secrets: the holdout seed and anything that looks like a credential are removed.
    # For third-party scanners, build in a separate job with no secrets at all (see the workflow).
    env = {k: v for k, v in os.environ.items()
           if k != "CBOM_HOLDOUT_SEED" and not any(t in k.upper() for t in ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "API_KEY"))}
    r = subprocess.run([str(py), "-m", "pip", "install", "-q", f"{scanner}[x509]"], capture_output=True, text=True, env=env)
    if r.returncode:
        raise SystemExit(f"pip install failed:\n{r.stderr[-2000:]}")
    exe = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "qci-pqc"
    return exe


def metric_rows(rep: dict) -> dict:
    a = rep["summary"]["all/all"]
    ac, d = rep["actionability"], rep["deadlines"]
    return {
        "recall": a["recall"], "primary_site_recall": a["usage_site_recall"], "params_accuracy": a["params_accuracy"],
        "precision": a["precision"], "false_positives": a["false_positives"],
        "negative_control_fps": rep["summary"]["negatives"]["false_positives"],
        "pqc_overclaims": rep["summary"]["pqc_overclaims"]["count"],
        "pqc_standard_name_pct": (rep["summary"].get("pqc_standard_names") or {}).get("accuracy"),
        "system_routable_pct": (rep.get("linkage") or {}).get("routable_pct"),
        "ticket_ready_pct": ac["ticket_ready_pct"], "actionable_recall": ac["actionable_recall"],
        "field_completeness": ac["completeness_pct"], "deadline_weighted_recall": d["weighted_recall"],
        "missed_due_by_2030": len(d["missed_due_by_2030"]),
        "library_recall": (rep.get("libraries") or {}).get("recall"),
        "parameter_recovery": ((rep.get("parameter_recovery") or {}).get("overall") or {}).get("pct"),
        "config_completeness": (rep.get("config_completeness") or {}).get("config_pct"),
        "library_pq_verdict_accuracy": (rep.get("libraries") or {}).get("pq_verdict_accuracy"),
    }


ADAPTER_FILES = ("tools/adapters/qci_pqc.py", "tools/adapters/common.py", "integrations/qci-pqc/scope.json")
EXIT_PASS, EXIT_FAIL, EXIT_NOT_EVALUATED = 0, 1, 3


def sandboxed_scan(exe: str, adapter: str, corpus: Path, raw: Path):
    """Scan in the secure lane: scrubbed environment (no holdout seed, no credentials), a private
    read-only copy of the corpus, no network where the host allows it. -> sandbox.Result"""
    import sandbox
    exe_path = Path(shutil.which(exe) or exe).resolve()
    res = sandbox.run([str(exe_path), "scan", "{corpus}", "--reproducible", "--adapter", adapter, "--out", "{out}", "--json"],
                      {"corpus": corpus}, extra_path=(str(exe_path.parent),),
                      hide=(str(ROOT), str(Path(corpus).parent)) if not Path(corpus).is_relative_to(ROOT) else (str(ROOT),))
    raw.mkdir(parents=True, exist_ok=True)
    for f in Path(res.out).iterdir():
        (shutil.copytree if f.is_dir() else shutil.copy2)(f, raw / f.name)
    (raw / "run.json").write_text(json.dumps(res.record(), indent=2) + "\n")
    sandbox.cleanup(res)
    return res


def gates_stamp(policy: str = "nist") -> dict:
    """The exact environment a baseline belongs to (tools/release.py)."""
    return release.stamp(policy, ADAPTER_FILES)


POLICY_LIMITS = {"overfit_gap_ci_low", "negative_fp_gap", "cbom_schema_valid"}


def rebaseline(gates: dict, m: dict, path: Path, policy: str = "nist") -> None:
    """Reset every gate to the current measurement (same keys, same direction) on this corpus."""
    for key, rule in gates.get("gates", {}).items():
        if m.get(key) is None:
            continue
        if key in POLICY_LIMITS:
            continue  # fixed limits, not ratchets: a rebaseline never moves them
        rule["min" if "min" in rule else "max"] = m[key]
    gates.pop("corpus", None)  # pre-1.17 stamp
    gates["stamp"] = gates_stamp(policy)
    gates["set_on"] = dt.date.today().isoformat()
    path.write_text(json.dumps(gates, indent=2) + "\n")


HOLDOUT_GATES = {"overfit_gap_ci_low", "negative_fp_gap"}


def evaluate_gates(gates: dict, m: dict, current_stamp: dict, report_only: bool = False,
                   without: dict | None = None) -> dict:
    """-> {status: pass|fail|not_evaluated, code, fails, missing, skipped, why}.

    Gates are evaluated only against the stamp they were set on; anything else is 'not evaluated',
    never a silent pass. Every gate is a required measurement: a gate whose metric is absent is
    listed in `missing` and the run is 'not evaluated' (exit 3), or 'fail' if another gate failed.
    Two ways a gate may be skipped, each recorded with its reason: the gate itself says
    {"when_missing": "skip", "reason": ...} (a measurement the scanner may legitimately not produce),
    or the caller passes `without` = {gate: reason} (e.g. a run explicitly made without a holdout)."""
    without = without or {}
    base = {"fails": [], "missing": [], "skipped": []}
    if not gates.get("gates"):
        res = {**base, "status": "not_evaluated", "why": "no gates configured"}
    elif "stamp" not in gates:
        res = {**base, "status": "not_evaluated",
               "why": "the gates file has no stamp for this testbench release" + (" (it carries a pre-1.17 corpus stamp)" if "corpus" in gates else "")}
    elif release.stamp_diff(gates["stamp"], current_stamp):
        res = {**base, "status": "not_evaluated",
               "why": "the baseline was set on a different " + "; ".join(release.stamp_diff(gates["stamp"], current_stamp))}
    else:
        fails, missing, skipped = [], [], []
        for key, rule in gates["gates"].items():
            v = m.get(key)
            if v is None:
                if key in without:
                    skipped.append({"gate": key, "reason": without[key]})
                elif rule.get("when_missing") == "skip":
                    skipped.append({"gate": key, "reason": rule.get("reason", "the gate allows this measurement to be absent")})
                else:
                    missing.append(key)
                continue
            if "min" in rule and v < rule["min"]:
                fails.append(f"{key} = {v} is below the gate minimum {rule['min']}")
            if "max" in rule and v > rule["max"]:
                fails.append(f"{key} = {v} is above the gate maximum {rule['max']}")
        status = "fail" if fails else "not_evaluated" if missing else "pass"
        why = ("required measurement(s) missing: " + ", ".join(missing)) if missing else ""
        res = {"status": status, "fails": fails, "missing": missing, "skipped": skipped, "why": why}
    res["code"] = EXIT_PASS if report_only else {"pass": EXIT_PASS, "fail": EXIT_FAIL, "not_evaluated": EXIT_NOT_EVALUATED}[res["status"]]
    return res


def gates_markdown(ev: dict, report_only: bool = False) -> list[str]:
    """One rendering of a gate verdict, used by SUMMARY.md and by evidence bundles."""
    lines = []
    if report_only:
        lines += ["**REPORT ONLY.** This run was not allowed to fail; what the gates say is shown for information.", ""]
    if ev["fails"]:
        lines += [f"**FAILED** ({len(ev['fails'])}):", ""] + [f"- {x}" for x in ev["fails"]] + [""]
    if ev["missing"]:
        lines += [f"**NOT EVALUATED** ({len(ev['missing'])} required measurement(s) missing):", ""] + \
                 [f"- {k}: not measured in this run" for k in ev["missing"]] + [""]
    elif ev["status"] == "not_evaluated":
        lines += [f"**NOT EVALUATED:** {ev['why']}. Review this run and reset the baseline with `--rebaseline`.", ""]
    if ev["status"] == "pass":
        lines += ["**All gates passed.**", ""]
    if ev["skipped"]:
        lines += ["Skipped:", ""] + [f"- {x['gate']}: {x['reason']}" for x in ev["skipped"]] + [""]
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--scanner", type=Path, help="path to a qci-pqc-scanner checkout (installed into a venv)")
    src.add_argument("--qci-bin", help="an existing qci-pqc executable")
    ap.add_argument("--venv", type=Path, default=ROOT / ".qci-venv")
    ap.add_argument("--adapter", default="internal", help="passed to qci-pqc --adapter (e.g. internal,semgrep)")
    ap.add_argument("--policy", default="nist")
    ap.add_argument("--out", type=Path, default=ROOT / "reports" / "qci-pqc")
    ap.add_argument("--gates", type=Path, default=INTEGRATION / "gates.json")
    ap.add_argument("--report-only", "--no-gate", dest="report_only", action="store_true",
                    help="write the reports and show what the gates say, but always exit 0 (summary is labelled REPORT ONLY)")
    ap.add_argument("--rebaseline", action="store_true",
                    help="reset gates.json to this run's numbers on the current corpus (after a corpus upgrade)")
    ap.add_argument("--holdout-seed", type=int, default=os.environ.get("CBOM_HOLDOUT_SEED") or None,
                    help="private seed for a holdout set (default: $CBOM_HOLDOUT_SEED; none = skip)")
    ap.add_argument("--without-holdout", action="store_true",
                    help="run with no holdout set on purpose: the two holdout gates are recorded as skipped. "
                         "Without this flag and without a seed they are missing measurements and the run exits 3.")
    ap.add_argument("--holdout-detail", type=Path,
                    help="keep the holdout files and per-finding scorecard here (default: discarded; "
                         "never put them anywhere the scanner team can read)")
    a = ap.parse_args()

    exe = str(install(a.scanner.resolve(), a.venv)) if a.scanner else a.qci_bin
    # Even --version is the scanner's code: it runs in the sandbox, without the seed or credentials.
    import sandbox
    exe_path = Path(shutil.which(str(exe)) or exe).resolve()
    vr = sandbox.run([str(exe_path), "--version"], extra_path=(str(exe_path.parent),), limits=sandbox.Limits(wall_s=60), keep=False,
                     hide=(str(ROOT),))
    version = vr.stdout.strip() or "unknown"
    print(f"Scanner: {version}")

    raw = a.out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    print(f"Scanning corpus/ with adapter(s) {a.adapter} ...")
    r = sandboxed_scan(exe, a.adapter, ROOT / "corpus", raw)
    print(f"  sandbox: {r.isolation['network']}, inputs {r.isolation['inputs_readonly']}; "
          f"exit {r.exit_code}, {r.wall_s}s, peak {r.peak_rss_mb} MB")
    if r.exit_code not in (0, 1) or r.tampered or not (raw / "cbom.json").exists():
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit("scan failed" + (f" (it modified its input: {r.tampered})" if r.tampered else ""))
    qci_bom = json.loads((raw / "cbom.json").read_text())

    schema = "not checked (pip install cyclonedx-python-lib[json-validation])"
    try:
        from cyclonedx.schema import SchemaVersion
        from cyclonedx.validation.json import JsonStrictValidator
        err = JsonStrictValidator(SchemaVersion.V1_6).validate_str((raw / "cbom.json").read_text())
        schema = "valid CycloneDX 1.6" if err is None else f"INVALID: {str(err)[:200]}"
    except ImportError:
        pass

    bom, signals, unmapped = qci_pqc.translate(qci_bom)
    adapted = a.out / "qci-pqc.cdx.json"
    adapted.write_text(json.dumps(bom, indent=2) + "\n")
    (a.out / "signals.json").write_text(json.dumps(signals, indent=2) + "\n")

    scope = load_scope(INTEGRATION / "scope.json")
    name = f"{version} (adapter {qci_pqc.ADAPTER_VERSION})"
    scoped = score(bom, policy=a.policy, custom="exclude", scope=scope)
    full = score(bom, policy=a.policy, custom="exclude")
    for rep in (scoped, full):
        rep["manifest"].update(scanner=version, adapter=f"qci_pqc {qci_pqc.ADAPTER_VERSION}",
                               adapter_sha=release.stamp(a.policy, ADAPTER_FILES)["adapter"])

    gt = load_truth(include_custom=False)[0]
    sc = qci_pqc.signal_coverage(scoped, gt, signals, act.material_index(gt))

    (a.out / "scorecard.md").write_text(to_markdown(f"{name}, declared scope", scoped)
                                        + "\n" + qci_pqc.signals_markdown(sc, unmapped))
    (a.out / "scorecard.json").write_text(json.dumps({**scoped, "signal_coverage": sc, "unmapped": unmapped},
                                                     indent=2, default=str) + "\n")
    (a.out / "scorecard-full.md").write_text(to_markdown(f"{name}, everything", full))
    sc_full = qci_pqc.signal_coverage(full, gt, signals, act.material_index(gt))
    (a.out / "scorecard-full.json").write_text(json.dumps({**full, "signal_coverage": sc_full}, indent=2, default=str) + "\n")

    ms, mf = metric_rows(scoped), metric_rows(full)
    if schema.startswith(("valid", "INVALID")):  # only when the validator is installed
        ms["cbom_schema_valid"] = mf["cbom_schema_valid"] = 1 if schema.startswith("valid") else 0
    gap, holdout_md = None, None
    if a.holdout_seed is not None:
        work = Path(tempfile.mkdtemp(prefix="cbom-holdout-"))
        try:
            print("Generating and scanning a holdout set ...")
            hdir = work / "set"
            ho.generate(int(a.holdout_seed), hdir)
            hraw = work / "scan"
            # This process holds the seed; the scanner runs in the sandbox and never sees it.
            hr = sandboxed_scan(exe, a.adapter, hdir / "corpus", hraw)
            if not (hraw / "cbom.json").exists():
                raise SystemExit(f"holdout scan failed: {hr.stderr[-1000:]}")
            hbom, _, _ = qci_pqc.translate(json.loads((hraw / "cbom.json").read_text()))
            hrep = ho.score_holdout(hbom, hdir, a.policy, scope)
            gap = ho.overfit_gap(scoped, hrep)
            neg = ho.negative_gap(scoped, hrep, hdir)
            lib = ho.library_gap(scoped.get("libraries"), hbom, hdir)
            holdout_md = ho.gap_markdown(gap, hrep) + ho.negative_markdown(neg) + ho.library_markdown(lib)
            broad = [r for r in hrep["results"] if r["tier"] == "holdout-broad"]
            ms.update({"negative_fp_gap": neg["gap_per_file"],
                       # reported, not gated: a few dozen manifests per seed is too few to fail a build on
                       "holdout_library_recall": lib["holdout"] if lib else None, "library_gap": lib["gap"] if lib else None})
            ms.update({"holdout_recall": gap["holdout"], "overfit_gap": gap["gap"], "overfit_gap_ci_low": gap["gap_ci95"][0],
                       "broad_recall": round(100 * sum(r["detected"] for r in broad) / len(broad), 1) if broad else None})
            if a.holdout_detail:
                if a.holdout_detail.exists():
                    shutil.rmtree(a.holdout_detail)
                shutil.copytree(hdir, a.holdout_detail)
                (a.holdout_detail / "holdout-score.md").write_text(to_markdown(f"{name}, holdout", hrep) + "\n" + holdout_md)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    gates = json.loads(a.gates.read_text()) if a.gates.exists() else {"gates": {}}
    cur_stamp = gates_stamp(a.policy)
    if a.rebaseline:
        rebaseline(gates, ms, a.gates, a.policy)
        print(f"Gates reset to this run, stamped {gates['stamp']}")
    without = {}
    if a.without_holdout and a.holdout_seed is None:
        without = {k: "run made without a holdout set (--without-holdout)" for k in HOLDOUT_GATES}
    ev = evaluate_gates(gates, ms, cur_stamp, a.report_only, without)
    fails = ev["fails"]
    # The one record of this run's verdict: SUMMARY.md is rendered from it, and the docs check
    # compares it with the evidence bundle's.
    (a.out / "gates-result.json").write_text(json.dumps(
        {"status": ev["status"], "fails": ev["fails"], "missing": ev["missing"], "skipped": ev["skipped"],
         "why": ev["why"], "report_only": a.report_only, "stamp": cur_stamp}, indent=2) + "\n")
    fmt = lambda v, pct=True: "n/a" if v is None else (f"{v}%" if pct else str(v))  # noqa: E731
    labels = [("recall", "Recall", True), ("primary_site_recall", "At primary site", True),
              ("params_accuracy", "Parameters correct", True), ("precision", "Precision", True),
              ("false_positives", "False positives", False), ("negative_control_fps", "  of which in negative controls", False),
              ("pqc_overclaims", "PQC over-claims", False), ("pqc_standard_name_pct", "PQC by standard name (of detected PQC)", True), ("system_routable_pct", "System fixture: routable (of detected)", True),
              ("ticket_ready_pct", "Ticket-ready (of detected)", True),
              ("actionable_recall", "Actionable recall", True), ("field_completeness", "Field completeness", True),
              ("deadline_weighted_recall", f"Deadline-weighted recall ({a.policy})", True),
              ("missed_due_by_2030", "Missed findings due by 2030", False),
              ("library_recall", "Crypto libraries, right manifest", True),
              ("library_pq_verdict_accuracy", "Library PQC verdicts right", True)]
    for key in ("holdout_recall", "broad_recall", "overfit_gap", "overfit_gap_ci_low", "negative_fp_gap",
                "holdout_library_recall", "library_gap"):
        mf.setdefault(key, None)
    if gap:
        labels += [("holdout_recall", "Matched holdout recall", True), ("broad_recall", "Broad holdout recall", True),
                   ("overfit_gap", "Overfit gap (points)", False), ("overfit_gap_ci_low", "  lower 95% bound", False),
                   ("negative_fp_gap", "Negative-control gap (FPs per file)", False),
                   ("holdout_library_recall", "Holdout crypto libraries, right manifest", True),
                   ("library_gap", "Library gap (points, not gated)", False)]
    s = scoped["summary"]
    lines = [f"# QCI PQC Scanner on the CBOM Testbench", "",
             f"- Scanner: **{version}**, adapter(s) `{a.adapter}`",
             f"- Scanner's own CBOM: {schema}; {len(qci_bom.get('components', []))} components",
             f"- Translation: `tools/adapters/qci_pqc.py` {qci_pqc.ADAPTER_VERSION}; scope: `integrations/qci-pqc/scope.json`",
             f"- Run: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", "",
             "| Metric | In declared scope | Everything |", "|---|---|---|"]
    for key, label, pct in labels:
        lines.append(f"| {label} | {fmt(ms[key], pct)} | {fmt(mf[key], pct)} |")
    lines += ["", f"Risk-signal coverage (in scope): strict {sc['strict_detected']}/{sc['expected']}, "
              f"plus {sc['signal_only']} covered only by a QCI category signal, "
              f"combined **{sc['combined_recall']}%**.", "",
              "| Bucket | Detected | Recall | At primary site | Params |", "|---|---|---|---|---|"]
    for k, v in s.items():
        if k in ("negatives", "pqc_overclaims", "pqc_standard_names", "all/all"):
            continue
        lines.append(f"| {k} | {v['detected']}/{v['expected']} | {fmt(v['recall'])} | {fmt(v['usage_site_recall'])} | "
                     f"{fmt(v['params_accuracy'])} |")
    ex = scoped["scope"]["excluded"]
    lines += ["", f"{len(ex)} expected findings are outside the declared scope and not counted; "
              f"{sum(1 for r in ex if r['detected'])} were detected anyway.", ""]
    if unmapped:
        lines += [f"**Unmapped QCI names:** {', '.join(unmapped)}. Add them to the adapter.", ""]
    if holdout_md:
        lines += [holdout_md.replace("## Holdout and overfit gap", "## Holdout (private seed)"), ""]
    else:
        lines += ["No holdout set this run. Set CBOM_HOLDOUT_SEED (a CI secret) to measure the overfit gap.", ""]
    lines += ["## Gates", "", f"Testbench {release.VERSION}; stamp `{json.dumps(cur_stamp)}`.", ""]
    lines += gates_markdown(ev, a.report_only)
    if ev["status"] == "not_evaluated" and not a.report_only:
        lines += ["The run exits 3.", ""]
    lines += ["", "Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), "
              "`raw/` (the scanner's own outputs)."]
    (a.out / "SUMMARY.md").write_text("\n".join(lines) + "\n")

    print("\n".join(lines[6:6 + len(labels) + 2]))
    if gap:
        print(f"\nOverfit gap {gap['gap']:+} points [{gap['gap_ci95'][0]:+}, {gap['gap_ci95'][1]:+}]")
    print(f"\nSignal coverage: combined {sc['combined_recall']}% ({sc['signal_only']} signal-only)")
    print(f"Summary: {a.out / 'SUMMARY.md'}")
    if fails:
        print("\nGATES FAILED:\n  " + "\n  ".join(fails) + (" (report only)" if a.report_only else ""))
    if ev["status"] == "not_evaluated" or ev["missing"]:
        print(f"\nGATES NOT EVALUATED: {ev['why']}" + (" (report only)" if a.report_only else "" if fails else " -> exit 3"))
    for x in ev["skipped"]:
        print(f"  skipped {x['gate']}: {x['reason']}")
    return ev["code"]


if __name__ == "__main__":
    sys.exit(main())
