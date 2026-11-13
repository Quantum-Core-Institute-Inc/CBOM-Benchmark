#!/usr/bin/env python3
"""The one command: run a scanner in the sandbox, score it, and write an evidence bundle.

  # score any scanner; {corpus} and {out} are filled in by the sandbox
  python tools/bench.py run --name "QCI v2.3.4.3" --adapter qci-pqc \\
      --scanner-cmd "qci-pqc scan {corpus} --reproducible --out {out} --json" --cbom cbom.json \\
      --version-cmd "qci-pqc --version" --scope integrations/qci-pqc/scope.json \\
      --bundle bundles/qci-v2.3.4.3

  # the testbench's required checks (CI runs this on a tag; a bundle can carry the result)
  python tools/bench.py checks --out bundles/checks.json

  # an evaluator re-derives every number in a bundle from its raw CBOM, on this tree
  python tools/bench.py verify bundles/qci-v2.3.4.3

Set CBOM_HOLDOUT_SEED (or --holdout-seed) to add a private holdout run: this process generates the
set, the scanner scans it in the sandbox without the seed, and the bundle records a commitment to the
seed, never the seed. In the container image the network guard is `docker run --network none`.

Exit codes for `run`: 0 scored; 2 not scored (scanner failed, timed out, modified its input, or
isolation was required and missing); 1 gates failed (with --gates); 3 gates not evaluated.
`verify`: 0 every number reproduces, 1 something doesn't.
`checks`: 0 every required check passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release  # noqa: E402
import sandbox  # noqa: E402
from score import load_scope, load_truth, score, to_markdown  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

ADAPTERS = {
    "none": {"files": (), "module": None},
    "qci-pqc": {"files": ("tools/adapters/qci_pqc.py", "tools/adapters/common.py"), "module": "adapters.qci_pqc"},
    "cdxgen": {"files": ("tools/adapters/cdxgen.py", "tools/adapters/common.py"), "module": "adapters.cdxgen"},
    "qscan": {"files": ("tools/adapters/qscan.py",), "module": "adapters.qscan"},
    "sarif": {"files": ("tools/adapters/sarif.py",), "module": "adapters.sarif"},
}


def fs(a, *extra_hidden) -> dict:
    """Filesystem boundary for a scanner run: the testbench tree (answer key, evidence, reports) and
    any evaluator-side directory are hidden; --allow-path puts named paths back."""
    return {"hide": (str(ROOT), *map(str, extra_hidden)), "allow": tuple(str(Path(p).resolve()) for p in a.allow_path),
            "require_confine": a.require_isolation, "image": getattr(a, "scanner_image", None)}


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def seed_commitment(seed) -> str:
    return hashlib.sha256(f"cbom-holdout:{seed}".encode()).hexdigest()


def translate(adapter: str, raw_bom: dict):
    """-> (CycloneDX bom for the scorer, signals, notes)"""
    if adapter == "none":
        return raw_bom, [], None
    import importlib
    mod = importlib.import_module(ADAPTERS[adapter]["module"])
    return mod.translate(raw_bom)


def adapter_version(adapter: str) -> str | None:
    if adapter == "none":
        return None
    import importlib
    return importlib.import_module(ADAPTERS[adapter]["module"]).ADAPTER_VERSION


def score_all(adapter: str, raw_bom: dict, policy: str, scope: dict | None, name: str, version: str) -> dict:
    """Everything a bundle's numbers are derived from. Deterministic for a given tree and raw CBOM."""
    bom, signals, notes = translate(adapter, raw_bom)
    out = {"cbom": bom}
    for key, sc in (("scorecard", scope), ("scorecard-full", None)) if scope else (("scorecard", None),):
        rep = score(bom, policy=policy, custom="exclude", scope=sc)
        rep["manifest"].update(scanner=name, scanner_version=version,
                               adapter=f"{adapter} {adapter_version(adapter)}" if adapter != "none" else None)
        if signals and adapter != "none":
            import importlib
            import actionability as act
            gt = load_truth(include_custom=False)[0]
            mod = importlib.import_module(ADAPTERS[adapter]["module"])
            rep["signal_coverage"] = mod.signal_coverage(rep, gt, signals, act.material_index(gt))
        out[key] = rep
    return out


def headline(rep: dict) -> dict:
    a, ac = rep["summary"]["all/all"], rep["actionability"]
    lib = rep.get("libraries") or {}
    return {"scored_findings": a["expected"], "recall": a["recall"], "primary_site_recall": a["usage_site_recall"],
            "params_accuracy": a["params_accuracy"], "precision": a["precision"],
            "false_positives": a["false_positives"], "pqc_overclaims": rep["summary"]["pqc_overclaims"]["count"],
            "pqc_standard_name_pct": (rep["summary"].get("pqc_standard_names") or {}).get("accuracy"),
            "ticket_ready_pct": ac["ticket_ready_pct"], "actionable_recall": ac["actionable_recall"],
            "deadline_weighted_recall": rep["deadlines"]["weighted_recall"], "library_recall": lib.get("recall")}


def validate_cyclonedx(path: Path) -> str:
    try:
        from cyclonedx.schema import SchemaVersion
        from cyclonedx.validation.json import JsonStrictValidator
    except ImportError:
        return "not checked (cyclonedx-python-lib not installed)"
    err = JsonStrictValidator(SchemaVersion.V1_6).validate_str(path.read_text())
    return "valid CycloneDX 1.6" if err is None else f"invalid: {str(err).splitlines()[0][:200]}"


def write_bundle_files(bundle: Path, parts: dict, name: str) -> None:
    for key in ("scorecard", "scorecard-full"):
        if key in parts:
            (bundle / f"{key}.json").write_text(json.dumps(parts[key], indent=2, default=str) + "\n")
            label = f"{name}, declared scope" if key == "scorecard" and "scorecard-full" in parts else name
            (bundle / f"{key}.md").write_text(to_markdown(label, parts[key]))
    (bundle / "cbom.cdx.json").write_text(json.dumps(parts["cbom"], indent=2) + "\n")


def host_info() -> dict:
    h = {"python": platform.python_version(), "platform": platform.platform(), "machine": platform.machine()}
    tc = ROOT / "TOOLCHAINS.json"  # written when the container image is built
    if tc.exists():
        h["toolchains"] = json.loads(tc.read_text())
    return h


def sums(bundle: Path) -> str:
    lines = [f"{sha256(p)}  {p.relative_to(bundle)}" for p in sorted(bundle.rglob("*"))
             if p.is_file() and p.name != "SHA256SUMS"]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------------- run
def cmd_run(a) -> int:
    adapter_files = ADAPTERS[a.adapter]["files"] + ((a.scope,) if a.scope else ())
    bundle = Path(a.bundle)
    if bundle.exists():
        if not a.force:
            raise SystemExit(f"{bundle} exists; pass --force to replace it")
        shutil.rmtree(bundle)
    (bundle / "raw").mkdir(parents=True)

    cmd = shlex.split(a.scanner_cmd)
    exe = cmd[0] if a.scanner_image else (shutil.which(cmd[0]) or cmd[0])  # with an image, the command is the image's
    extra_path = () if a.scanner_image else (str(Path(exe).resolve().parent),) if os.path.isabs(exe) or shutil.which(cmd[0]) else ()
    version = a.scanner_version
    if not version and a.version_cmd:
        vr = sandbox.run(shlex.split(a.version_cmd), extra_path=extra_path, limits=sandbox.Limits(wall_s=60), keep=False, **fs(a))
        version = (vr.stdout.strip() or vr.stderr.strip()).splitlines()[0] if (vr.stdout or vr.stderr).strip() else None
    lim = sandbox.Limits(wall_s=a.timeout, mem_mb=a.mem_mb or None, cpu_s=a.cpu_s, network=a.allow_network)

    print(f"Scanning corpus/ in the sandbox: {a.scanner_cmd}")
    res = sandbox.run(cmd, {"corpus": ROOT / "corpus"}, lim, pass_env=tuple(a.pass_env), extra_path=extra_path,
                      require=a.require_isolation, **fs(a))
    for f in Path(res.out).iterdir():
        (shutil.copytree if f.is_dir() else shutil.copy2)(f, bundle / "raw" / f.name)
    (bundle / "run.log").write_text("\n".join((res.stdout + "\n--- stderr ---\n" + res.stderr).splitlines()[-400:]) + "\n")
    sandbox.cleanup(res)
    print(f"  {res.isolation['network']}; corpus {res.isolation['inputs_readonly']}; exit {res.exit_code}, "
          f"{res.wall_s}s wall, {res.cpu_user_s + res.cpu_sys_s:.1f}s CPU, peak {res.peak_rss_mb} MB")

    problems = []
    cbom_path = bundle / "raw" / a.cbom
    if res.timed_out:
        problems.append(f"timed out after {a.timeout}s")
    if res.tampered:
        problems.append(f"modified its input ({', '.join(res.tampered)})")
    if res.exit_code not in tuple(a.ok_exit):
        problems.append(f"exit {res.exit_code}" + (f" (signal {res.signal})" if res.signal else ""))
    if not cbom_path.exists():
        problems.append(f"no CBOM at {a.cbom} in the output directory")

    manifest = {
        "bundle_format": 1,
        "testbench": release.VERSION, "methodology": release.METHODOLOGY,
        "created": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stamp": release.stamp(a.policy, adapter_files), "files": release.file_inventory(adapter_files),
        "scanner": {"name": a.name, "version": version, "cmd": [Path(c).name if os.path.isabs(c) else c for c in cmd],
                    "executable_sha256": sha256(exe) if not a.scanner_image and Path(exe).is_file() else None,
                    "image": a.scanner_image, "image_id": res.isolation.get("container_image"),
                    "allowed_paths": [str(Path(p).resolve().relative_to(ROOT)) if Path(p).resolve().is_relative_to(ROOT)
                                      else Path(p).name for p in a.allow_path],
                    "cbom": a.cbom, "adapter": a.adapter, "adapter_version": adapter_version(a.adapter),
                    "scope": a.scope, "policy": a.policy},
        "image": {"digest": os.environ.get("CBOM_IMAGE_DIGEST"), "containerized": bool(os.environ.get("CBOM_IMAGE_DIGEST"))},
        "host": host_info(),
        "run": res.record(),
    }
    if problems:
        manifest.update(verdict="not scored", why=problems)
        finish(bundle, manifest, a)
        print("NOT SCORED: " + "; ".join(problems))
        return 2

    raw_bom = json.loads(cbom_path.read_text())
    manifest["scanner"]["cbom_schema"] = validate_cyclonedx(cbom_path)
    scope = load_scope(a.scope) if a.scope else None
    parts = score_all(a.adapter, raw_bom, a.policy, scope, a.name, version)
    write_bundle_files(bundle, parts, a.name)
    manifest["headline"] = headline(parts["scorecard"])
    if "scorecard-full" in parts:
        manifest["headline_full"] = headline(parts["scorecard-full"])

    seed = a.holdout_seed if a.holdout_seed is not None else os.environ.get("CBOM_HOLDOUT_SEED")
    if seed is not None:
        manifest["holdout"] = run_holdout(int(seed), cmd, a, lim, extra_path, parts["scorecard"], scope, bundle)

    if a.remediation:
        manifest["remediation"] = run_remediation(cmd, a, lim, extra_path, parts, version, bundle)

    gate_code = None
    if a.gates:
        gate_code = gates(a, manifest, parts["scorecard"], bundle)
    if a.checks:
        chk = json.loads(Path(a.checks).read_text())
        shutil.copy2(a.checks, bundle / "checks.json")
        stale = release.stamp_diff({k: v for k, v in chk["stamp"].items() if k != "adapter"},
                                   {k: v for k, v in manifest["stamp"].items() if k != "adapter"})
        manifest["checks"] = {"status": chk["status"] if not stale else "stale (run on a different tree)",
                              "counts": chk["counts"], "stale": stale or None}
    else:
        manifest["checks"] = {"status": "not run", "note": "run `bench.py checks` and pass --checks for a release bundle"}
    manifest["verdict"] = "scored"
    finish(bundle, manifest, a)
    h = manifest["headline"]
    print(f"Scored {h['scored_findings']} findings: recall {h['recall']}%, precision {h['precision']}%, "
          f"params {h['params_accuracy']}%, ticket-ready {h['ticket_ready_pct']}%")
    print(f"Bundle: {bundle}  (check it with: python tools/bench.py verify {bundle})")
    return gate_code if gate_code is not None else 0


def run_holdout(seed: int, cmd, a, lim, extra_path, published: dict, scope, bundle: Path) -> dict:
    import holdout as ho
    work = Path(tempfile.mkdtemp(prefix="cbom-holdout-"))
    try:
        print("Generating a holdout set (this process holds the seed) ...")
        hdir = work / "set"
        ho.generate(seed, hdir)
        print("Scanning it in the sandbox (the scanner never sees the seed) ...")
        hres = sandbox.run(cmd, {"corpus": hdir / "corpus"}, lim, pass_env=tuple(a.pass_env), extra_path=extra_path,
                           require=a.require_isolation, **fs(a, work))  # the set and its answer key are hidden
        out = {"seed_commitment": seed_commitment(seed), "run": hres.record()}
        hcbom = Path(hres.out) / a.cbom
        if hres.timed_out or hres.tampered or not hcbom.exists():
            out["verdict"] = "not scored"
            sandbox.cleanup(hres)
            return out
        out["raw_cbom_sha256"] = sha256(hcbom)
        if a.keep_holdout_cbom:  # evaluator-side copy, for verify --holdout-cbom after the seed is revealed
            Path(a.keep_holdout_cbom).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hcbom, a.keep_holdout_cbom)
        hbom, _, _ = translate(a.adapter, json.loads(hcbom.read_text()))
        sandbox.cleanup(hres)
        hrep = ho.score_holdout(hbom, hdir, a.policy, scope)
        gap = ho.overfit_gap(published, hrep)
        neg = ho.negative_gap(published, hrep, hdir)
        lib = ho.library_gap(published.get("libraries"), hbom, hdir)
        out.update(verdict="scored", overfit_gap=gap, negative_gap=neg, library_gap=lib)
        (bundle / "holdout.md").write_text(ho.gap_markdown(gap, hrep) + ho.negative_markdown(neg) + ho.library_markdown(lib))
        print(f"  overfit gap {gap.get('gap')} {gap.get('gap_ci95')}, negative gap {neg['gap_per_file']}")
        return out
    finally:
        shutil.rmtree(work, ignore_errors=True)


def remediation_score(adapter: str, raw_after: dict, policy: str, before: dict, after_corpus: Path) -> dict:
    import remediate as rm
    bom, _, _ = translate(adapter, raw_after)
    gt_after = rm.after_truth(load_truth(include_custom=False)[0])
    after = score(bom, policy=policy, custom="exclude", truth=gt_after, corpus=after_corpus)
    return rm.evaluate(before, after)


def run_remediation(cmd, a, lim, extra_path, parts: dict, version, bundle: Path) -> dict:
    import remediate as rm
    work = Path(tempfile.mkdtemp(prefix="cbom-remed-"))
    try:
        print("Fix and rescan: applying the reference migrations and rescanning ...")
        corpus = rm.build_after(work)
        res = sandbox.run(cmd, {"corpus": corpus}, lim, pass_env=tuple(a.pass_env), extra_path=extra_path,
                          require=a.require_isolation, **fs(a, work))
        (bundle / "raw-after").mkdir()
        cb = Path(res.out) / a.cbom
        if cb.exists():
            shutil.copy2(cb, bundle / "raw-after" / a.cbom)
        sandbox.cleanup(res)
        if res.timed_out or res.tampered or not (bundle / "raw-after" / a.cbom).exists():
            return {"verdict": "not scored", "run": res.record()}
        before = parts.get("scorecard-full") or parts["scorecard"]
        ev = remediation_score(a.adapter, json.loads((bundle / "raw-after" / a.cbom).read_text()), a.policy,
                               json.loads(json.dumps(before, default=str)), corpus)
        (bundle / "remediation.json").write_text(json.dumps(ev, indent=2) + "\n")
        (bundle / "remediation.md").write_text(rm.markdown(ev, a.name))
        print(f"  verified remediation {ev['verified']}/{ev['eligible']} eligible (of {ev['total']}); "
              f"outside the migrated files: {len(ev['regressions_outside']['lost'])} lost")
        return {"verdict": "scored", "run": res.record(), "total": ev["total"], "eligible": ev["eligible"],
                "verified": ev["verified"], "verified_pct": ev["verified_pct"],
                "regressions_outside": len(ev["regressions_outside"]["lost"]) + len(ev["regressions_outside"]["gained"])}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def gates(a, manifest: dict, rep: dict, bundle: Path) -> int:
    import run_qci_pqc as r
    g = json.loads(Path(a.gates).read_text())
    m = r.metric_rows(rep)
    schema = manifest["scanner"].get("cbom_schema", "")
    if schema.startswith(("valid", "invalid")):
        m["cbom_schema_valid"] = 1 if schema.startswith("valid") else 0
    ho = manifest.get("holdout") or {}
    if ho.get("verdict") == "scored":
        m["overfit_gap_ci_low"] = ho["overfit_gap"]["gap_ci95"][0] if ho["overfit_gap"].get("gap_ci95") else None
        m["negative_fp_gap"] = ho["negative_gap"]["gap_per_file"]
    without = {}
    if a.without_holdout and "holdout" not in manifest:
        without = {k: "run made without a holdout set (--without-holdout)" for k in r.HOLDOUT_GATES}
    ev = r.evaluate_gates(g, m, release.stamp(a.policy, ADAPTERS[a.adapter]["files"] + ((a.scope,) if a.scope else ())),
                          without=without)
    # The gates file and the metrics it was applied to go in the bundle, so verify can re-derive the verdict.
    shutil.copy2(a.gates, bundle / "gates.json")
    (bundle / "gates.md").write_text("\n".join(["# Gates", ""] + r.gates_markdown(ev)) + "\n")
    manifest["gates"] = {"file": "gates.json", "status": ev["status"], "fails": ev["fails"], "missing": ev["missing"],
                         "skipped": ev["skipped"], "why": ev["why"], "metrics": m, "without": without}
    print(f"Gates: {ev['status'].upper()}" + (f": {ev['why']}" if ev["why"] else "")
          + "".join(f"\n  {f}" for f in ev["fails"]) + "".join(f"\n  skipped {x['gate']}: {x['reason']}" for x in ev["skipped"]))
    return ev["code"]


def finish(bundle: Path, manifest: dict, a) -> None:
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str) + "\n")
    (bundle / "SHA256SUMS").write_text(sums(bundle))


# -------------------------------------------------------------------------------------------- perf
def cmd_perf(a) -> int:
    """Scan the generated large-repository fixture inside a time budget."""
    import perf
    bundle = Path(a.bundle)
    if bundle.exists():
        if not a.force:
            raise SystemExit(f"{bundle} exists; pass --force to replace it")
        shutil.rmtree(bundle)
    (bundle / "raw").mkdir(parents=True)
    work = Path(tempfile.mkdtemp(prefix="cbom-perf-"))
    try:
        meta = perf.generate(a.seed, work, a.size)
        print(f"Fixture: {meta['code_files']} code files, {meta['planted']} planted uses, "
              f"{meta['bytes'] / 1e6:.1f} MB (seed {a.seed}, {a.size})")
        cmd = shlex.split(a.scanner_cmd)
        exe = cmd[0] if a.scanner_image else (shutil.which(cmd[0]) or cmd[0])
        extra_path = () if a.scanner_image else (str(Path(exe).resolve().parent),) if os.path.isabs(exe) or shutil.which(cmd[0]) else ()
        lim = sandbox.Limits(wall_s=a.budget, mem_mb=a.mem_mb or None)
        res = sandbox.run(cmd, {"corpus": work / "corpus"}, lim, extra_path=extra_path, require=a.require_isolation, **fs(a, work))
        cbom = Path(res.out) / a.cbom
        if cbom.exists():
            shutil.copy2(cbom, bundle / "raw" / a.cbom)
        sandbox.cleanup(res)
        got = (bundle / "raw" / a.cbom).exists()
        status = ("timed out" if res.timed_out else "tampered" if res.tampered else
                  "no CBOM" if not got else f"exit {res.exit_code}" if res.exit_code not in (0, 1) else "finished")
        result = None
        if (bundle / "raw" / a.cbom).exists():
            bom, _, _ = translate(a.adapter, json.loads((bundle / "raw" / a.cbom).read_text()))
            result = perf.score_perf(bom, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    secs = max(res.wall_s, 0.01)
    manifest = {"bundle_format": 1, "kind": "perf", "testbench": release.VERSION, "methodology": release.METHODOLOGY,
                "created": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fixture": meta, "budget_s": a.budget, "scanner": {"name": a.name, "cmd": [Path(c).name if os.path.isabs(c) else c for c in cmd],
                "cbom": a.cbom, "adapter": a.adapter}, "image": {"digest": os.environ.get("CBOM_IMAGE_DIGEST")},
                "host": host_info(), "run": res.record(), "status": status,
                "within_budget": status == "finished",
                "throughput": {"files_per_s": round(meta["code_files"] / secs, 1), "mb_per_s": round(meta["bytes"] / 1e6 / secs, 2)},
                "result": result}
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str) + "\n")
    (bundle / "SHA256SUMS").write_text(sums(bundle))
    r = result or {}
    print(f"{status}: {res.wall_s}s of {a.budget}s budget, peak {res.peak_rss_mb} MB, "
          f"{manifest['throughput']['files_per_s']} files/s; planted found {r.get('found', 0)}/{meta['planted']}"
          f" by quartile {r.get('recall_by_quartile')}" + ("; COVERAGE FALLS OFF" if r.get("coverage_falloff") else ""))
    return 0 if status == "finished" else 2


def verify_perf(bundle: Path, m: dict, say) -> None:
    import perf
    work = Path(tempfile.mkdtemp(prefix="cbom-perf-v-"))
    try:
        meta = perf.generate(m["fixture"]["seed"], work, m["fixture"]["size"])
        say(meta == m["fixture"], "the fixture regenerates identically from its seed")
        raw = bundle / "raw" / m["scanner"]["cbom"]
        # What a verdict claims decides what must be in the bundle. A result needs its raw CBOM.
        claims_result = m.get("result") is not None or m.get("status") == "finished" or m.get("within_budget")
        if claims_result:
            say(raw.exists(), f"a bundle that reports a result carries raw/{m['scanner']['cbom']}")
            say(m.get("result") is not None, "a finished run records its result")
        else:
            say(not raw.exists() or m.get("status") != "no CBOM", "status 'no CBOM' and a raw CBOM don't both hold")
        if raw.exists() and m.get("result") is not None:
            bom, _, _ = translate(m["scanner"]["adapter"], json.loads(raw.read_text()))
            say(perf.score_perf(bom, work) == m["result"], "the result re-derives from the raw CBOM")
        secs = max(m["run"]["wall_s"], 0.01)
        say(m["throughput"] == {"files_per_s": round(meta["code_files"] / secs, 1), "mb_per_s": round(meta["bytes"] / 1e6 / secs, 2)}
            and m["within_budget"] == (m["status"] == "finished") and (m["status"] != "finished" or m["run"]["wall_s"] <= m["budget_s"]),
            "throughput and the budget verdict follow from the recorded run")
    finally:
        shutil.rmtree(work, ignore_errors=True)


# ------------------------------------------------------------------------------------------ verify
def cmd_verify(a) -> int:
    bundle = Path(a.bundle)
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"[{'ok ' if cond else 'FAIL'}] {msg}")

    listed = {}
    for line in (bundle / "SHA256SUMS").read_text().splitlines():
        h, rel = line.split("  ", 1)
        listed[rel] = h
    present = {str(p.relative_to(bundle)) for p in bundle.rglob("*") if p.is_file() and p.name != "SHA256SUMS"}
    bad = [rel for rel, h in listed.items() if not (bundle / rel).exists() or sha256(bundle / rel) != h]
    say(not bad and present == set(listed), "every file matches SHA256SUMS, nothing added or missing"
        + (f" (changed: {bad[:5]})" if bad else "") + (f" (unlisted: {sorted(present - set(listed))[:5]})" if present - set(listed) else ""))
    m = json.loads((bundle / "manifest.json").read_text())
    if m.get("kind") == "perf":
        verify_perf(bundle, m, say)
        print("Bundle verifies." if ok else "Bundle does NOT verify.")
        return 0 if ok else 1
    sc = m["scanner"]
    adapter_files = ADAPTERS[sc["adapter"]]["files"] + ((sc["scope"],) if sc.get("scope") else ())
    here = release.stamp(sc["policy"], adapter_files)
    diff = release.stamp_diff(m["stamp"], here)
    say(not diff, "this tree is the release the bundle was scored on" + (f" (differs: {'; '.join(diff)})" if diff else ""))
    if diff:
        files = release.file_inventory(adapter_files)
        changed = [f for f in sorted(set(files) | set(m["files"])) if files.get(f) != m["files"].get(f)]
        print("       files that differ: " + (", ".join(changed) if changed else "(corpus only)"))
    if m.get("verdict") != "scored":
        print(f"Bundle verdict: {m.get('verdict')}: {m.get('why')}")
        return 0 if ok else 1
    # What the manifest claims decides what must be in the bundle.
    need = [f"raw/{sc['cbom']}", "cbom.cdx.json", "scorecard.json", "scorecard.md"]
    need += ["scorecard-full.json"] if sc.get("scope") else []
    rem_scored = (m.get("remediation") or {}).get("verdict") == "scored"
    need += [f"raw-after/{sc['cbom']}", "remediation.json"] if rem_scored else []
    need += ["gates.json"] if m.get("gates") else []
    need += ["checks.json"] if (m.get("checks") or {}).get("status") not in (None, "not run") else []
    absent = [f for f in need if not (bundle / f).exists()]
    say(not absent, "every artifact the manifest's claims rest on is present" + (f" (missing: {', '.join(absent)})" if absent else ""))
    if absent:
        print("Bundle does NOT verify.")
        return 1
    raw = json.loads((bundle / "raw" / sc["cbom"]).read_text())
    parts = score_all(sc["adapter"], raw, sc["policy"], load_scope(sc["scope"]) if sc.get("scope") else None,
                      sc["name"], sc["version"])
    for key in ("scorecard", "scorecard-full"):
        p = bundle / f"{key}.json"
        if key in parts or p.exists():
            want = json.loads(p.read_text()) if p.exists() else None
            got = json.loads(json.dumps(parts.get(key), default=str))
            # every section: results, false positives, summary, actionability, deadlines, libraries,
            # linkage, scope, signal coverage, calibration, manifest
            differ = sorted(k for k in set(want or {}) | set(got or {}) if (want or {}).get(k) != (got or {}).get(k))
            say(want is not None and not differ, f"{key}: every section re-derives from raw/{sc['cbom']}"
                + (f" (differs: {', '.join(differ)})" if differ else ""))
    say(json.loads((bundle / "cbom.cdx.json").read_text()) == parts["cbom"], "the adapted CBOM re-derives from the raw one")
    say(headline(parts["scorecard"]) == m["headline"], "the manifest's headline matches")
    if "headline_full" in m:
        say(headline(parts["scorecard-full"]) == m["headline_full"], "the manifest's unscoped headline matches")
    now = validate_cyclonedx(bundle / "raw" / sc["cbom"])
    if now.startswith("not checked") or str(sc.get("cbom_schema", "")).startswith("not checked"):
        print("[note] not re-derived here: the raw CBOM's schema verdict (the validator isn't installed on one side)")
    else:
        say(now == sc["cbom_schema"], "the raw CBOM's schema verdict re-derives")
    rem_ev = None
    if rem_scored:
        import remediate as rm
        work = Path(tempfile.mkdtemp(prefix="cbom-remed-v-"))
        try:
            corpus = rm.build_after(work)
            before = parts.get("scorecard-full") or parts["scorecard"]
            rem_ev = remediation_score(sc["adapter"], json.loads((bundle / "raw-after" / sc["cbom"]).read_text()), sc["policy"],
                                       json.loads(json.dumps(before, default=str)), corpus)
            mr = m["remediation"]
            say(rem_ev == json.loads((bundle / "remediation.json").read_text())
                and (mr["total"], mr["eligible"], mr["verified"]) == (rem_ev["total"], rem_ev["eligible"], rem_ev["verified"]),
                "fix-and-rescan re-derives from raw-after/, and the manifest's counts match")
        finally:
            shutil.rmtree(work, ignore_errors=True)
    ho_m = m.get("holdout") or {}
    ho_checked = False
    if ho_m.get("verdict") == "scored" and a.holdout_seed is not None:
        say(seed_commitment(a.holdout_seed) == ho_m["seed_commitment"], "the revealed seed matches the bundle's commitment")
        if a.holdout_cbom:
            import holdout as ho
            say(sha256(a.holdout_cbom) == ho_m.get("raw_cbom_sha256"), "the holdout CBOM supplied is the one the bundle committed to")
            work = Path(tempfile.mkdtemp(prefix="cbom-holdout-v-"))
            try:
                ho.generate(int(a.holdout_seed), work / "set")
                hbom, _, _ = translate(sc["adapter"], json.loads(Path(a.holdout_cbom).read_text()))
                scope = load_scope(sc["scope"]) if sc.get("scope") else None
                hrep = ho.score_holdout(hbom, work / "set", sc["policy"], scope)
                pub = json.loads(json.dumps(parts["scorecard"], default=str))
                say(ho.overfit_gap(pub, hrep) == ho_m["overfit_gap"] and ho.negative_gap(pub, hrep, work / "set") == ho_m["negative_gap"],
                    "the overfit and negative-control gaps re-derive from the seed and the holdout CBOM")
                ho_checked = True
            finally:
                shutil.rmtree(work, ignore_errors=True)
    if m.get("gates"):
        import run_qci_pqc as r
        g = json.loads((bundle / "gates.json").read_text())
        gm = r.metric_rows(json.loads(json.dumps(parts["scorecard"], default=str)))
        recorded = m["gates"].get("metrics") or {}
        say(all(recorded.get(k) == v for k, v in gm.items()), "the gate metrics are the scorecard's")
        ev = r.evaluate_gates(g, recorded, here, without=m["gates"].get("without"))
        say((ev["status"], ev["fails"], ev["missing"], ev["skipped"]) ==
            (m["gates"]["status"], m["gates"]["fails"], m["gates"].get("missing", []), m["gates"].get("skipped", [])),
            f"the gate verdict ({m['gates']['status']}) re-derives from gates.json and the recorded metrics")
    if (m.get("checks") or {}).get("status") not in (None, "not run"):
        chk = json.loads((bundle / "checks.json").read_text())
        stale = release.stamp_diff({k: v for k, v in chk["stamp"].items() if k != "adapter"}, {k: v for k, v in m["stamp"].items() if k != "adapter"})
        say(not stale and chk["status"] == m["checks"]["status"] and all(c["status"] == "pass" for c in chk["checks"]) == (chk["status"] == "pass"),
            "checks.json is for this release and says what the manifest says")
    not_rederived = []
    if ho_m.get("verdict") == "scored" and not ho_checked:
        not_rederived.append("the holdout gaps (private: pass --holdout-seed and --holdout-cbom once the seed is revealed)")
    if not_rederived:
        print("[note] not re-derived here: " + "; ".join(not_rederived))
    print(f"\nRun: {m['run']['isolation']['network']}, corpus {m['run']['isolation']['inputs_readonly']}, "
          f"exit {m['run']['exit_code']}, {m['run']['wall_s']}s, peak {m['run']['peak_rss_mb']} MB. "
          f"Image: {m['image']['digest'] or 'not containerized'}. Required checks: {m['checks']['status']}.")
    print("Bundle verifies." if ok else "Bundle does NOT verify.")
    return 0 if ok else 1


# ------------------------------------------------------------------------------------------ checks
CHECKS = [
    ("corpus executes (strict)", [PY, "tools/verify_corpus.py", "--strict", "--summary-json", "{tmp}/verify.json"]),
    ("answer key reproducible", None),
    ("mixed files reproducible", [PY, "tools/build_mixed.py", "--check"]),
    ("calibration cases reproducible", [PY, "tools/build_calibration.py", "--check"]),
    ("reference replays to 100%", None),
    ("docs match scorecards", [PY, "tools/render_docs.py", "--check"]),
]


def cmd_checks(a) -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cbom-checks-"))
    results = []
    tests = sorted(ROOT.glob("tools/test_*.py"))
    plan = list(CHECKS) + [(f"tests: {t.stem}", [PY, str(t.relative_to(ROOT))] + (["--strict"] if t.stem == "test_sandbox" else []))
                           for t in tests]
    for name, cmd in plan:
        t0 = time.monotonic()
        if name == "answer key reproducible":
            before = {p: sha256(p) for p in (ROOT / "expected").glob("*.json")}
            r = subprocess.run([PY, "tools/build_expected.py"], cwd=ROOT, capture_output=True, text=True)
            after = {p: sha256(p) for p in (ROOT / "expected").glob("*.json")}
            changed = [p.name for p in after if before.get(p) != after[p]]
            st, detail = ("pass", "byte-identical") if r.returncode == 0 and not changed else \
                         ("fail", f"exit {r.returncode}; changed: {changed}")
        elif name == "reference replays to 100%":
            rep = score(json.loads((ROOT / "expected" / "expected.cdx.json").read_text()), custom="exclude")
            al = rep["summary"]["all/all"]
            good = al["recall"] == 100 and al["params_accuracy"] == 100 and al["false_positives"] == 0
            st, detail = ("pass" if good else "fail"), f"recall {al['recall']}, params {al['params_accuracy']}, FP {al['false_positives']}"
        else:
            r = subprocess.run([c.format(tmp=tmp) for c in cmd], cwd=ROOT, capture_output=True, text=True)
            tail = (r.stdout.strip().splitlines() or [""])[-1][:200]
            st = {0: "pass", 4: "skip"}.get(r.returncode, "fail")
            detail = tail
        results.append({"name": name, "status": st, "detail": detail, "seconds": round(time.monotonic() - t0, 1)})
        print(f"[{ {'pass': 'ok ', 'skip': 'skip', 'fail': 'FAIL'}[st] }] {name}: {detail}")
    verify = json.loads((tmp / "verify.json").read_text()) if (tmp / "verify.json").exists() else None
    shutil.rmtree(tmp, ignore_errors=True)
    status = "pass" if all(r["status"] == "pass" for r in results) else "fail"
    out = {"testbench": release.VERSION, "methodology": release.METHODOLOGY, "stamp": release.stamp("nist"),
           "created": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "image": os.environ.get("CBOM_IMAGE_DIGEST"), "host": host_info(), "status": status,
           "counts": {"checks": len(results), "passed": sum(r["status"] == "pass" for r in results),
                      "corpus": (verify or {}).get("total")},
           "checks": results, "corpus_verification": verify}
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nRequired checks: {status.upper()} ({out['counts']['passed']}/{len(results)})")
    return 0 if status == "pass" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="scan, score and bundle")
    r.add_argument("--name", required=True, help="scanner name for reports")
    r.add_argument("--scanner-cmd", required=True, help="command line; {corpus} and {out} are filled in")
    r.add_argument("--cbom", default="cbom.json", help="the CBOM's path inside {out}")
    r.add_argument("--adapter", choices=sorted(ADAPTERS), default="none")
    g = r.add_mutually_exclusive_group()
    g.add_argument("--scanner-version")
    g.add_argument("--version-cmd", help="command that prints the version (run in the sandbox)")
    r.add_argument("--scope", help="declared-scope JSON")
    r.add_argument("--policy", default="nist")
    r.add_argument("--holdout-seed", type=int, default=None, help="default: $CBOM_HOLDOUT_SEED")
    r.add_argument("--keep-holdout-cbom", help="write the scanner's raw holdout CBOM here (outside the bundle; keep it private)")
    r.add_argument("--gates", help="gates JSON to evaluate (exit 1 fail, 3 not evaluated)")
    r.add_argument("--without-holdout", action="store_true",
                   help="no holdout on purpose: the holdout gates are recorded as skipped instead of missing")
    r.add_argument("--checks", help="checks.json from `bench.py checks` to include")
    r.add_argument("--remediation", action="store_true",
                   help="also apply the reference migrations, rescan, and score verified remediation")
    r.add_argument("--bundle", required=True)
    r.add_argument("--force", action="store_true", help="replace an existing bundle directory")
    r.add_argument("--timeout", type=int, default=1800, help="wall-clock seconds (default 1800)")
    r.add_argument("--cpu-s", type=int, default=None)
    r.add_argument("--mem-mb", type=int, default=32768, help="address-space cap in MB (0 = none)")
    r.add_argument("--ok-exit", type=int, nargs="*", default=[0, 1], help="scanner exit codes that mean it ran (default 0 1)")
    r.add_argument("--pass-env", action="append", default=[], help="environment variable the scanner may see")
    r.add_argument("--allow-network", action="store_true", help="don't isolate the network (recorded in the bundle)")
    r.add_argument("--require-isolation", action="store_true",
                   help="refuse to run without network isolation and a filesystem boundary")
    r.add_argument("--scanner-image", help="run the scanner in its own container from this local image: it sees only "
                                           "the corpus (read-only) and the output directory. --scanner-cmd is then the "
                                           "command inside the image. The strongest lane; use it for scanners you don't trust.")
    r.add_argument("--allow-path", action="append", default=[],
                   help="a path the scanner may read although it is inside a hidden location (recorded in the bundle)")
    v = sub.add_parser("verify", help="re-derive every number in a bundle")
    v.add_argument("bundle")
    v.add_argument("--holdout-seed", type=int, default=None, help="the revealed seed: checks the bundle's commitment")
    v.add_argument("--holdout-cbom", help="the scanner's raw CBOM on the holdout set (kept by the evaluator): "
                                          "with the seed, re-derives the holdout gaps")
    pf = sub.add_parser("perf", help="scan the large-repository fixture inside a time budget")
    pf.add_argument("--name", required=True)
    pf.add_argument("--scanner-cmd", required=True)
    pf.add_argument("--cbom", default="cbom.json")
    pf.add_argument("--adapter", choices=sorted(ADAPTERS), default="none")
    pf.add_argument("--size", choices=["small", "medium", "large"], default="medium")
    pf.add_argument("--seed", type=int, default=2026, help="public; the fixture isn't secret")
    pf.add_argument("--budget", type=int, default=600, help="wall-clock seconds the scanner gets (default 600)")
    pf.add_argument("--mem-mb", type=int, default=32768)
    pf.add_argument("--require-isolation", action="store_true")
    pf.add_argument("--allow-path", action="append", default=[])
    pf.add_argument("--scanner-image")
    pf.add_argument("--bundle", required=True)
    pf.add_argument("--force", action="store_true")
    c = sub.add_parser("checks", help="run the testbench's required checks")
    c.add_argument("--out")
    a = ap.parse_args()
    return {"run": cmd_run, "verify": cmd_verify, "checks": cmd_checks, "perf": cmd_perf}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
