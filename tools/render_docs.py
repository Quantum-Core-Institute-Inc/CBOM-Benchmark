#!/usr/bin/env python3
"""Fill the generated tables in the docs from the release scorecards, so a number can't drift.

  python tools/render_docs.py           # rewrite reports/comparison.* and every generated block
  python tools/render_docs.py --check   # CI: exit 1 if any of them is out of date

A generated block looks like

    <!-- generated:NAME (tools/render_docs.py; edit the scorecards, not this table) -->
    ...
    <!-- /generated:NAME -->

and everything between the markers is replaced. Every scorecard used must carry a manifest from
this exact release (answer key, corpus, scorer, policy); a stale one stops the render and names the
file to rescore. Every table states its denominator. Prose around the tables shouldn't repeat their
numbers: point at the table instead.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402
import release  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# The release scorecards. Paths are relative to the repo root.
CALIBRATION = [
    ("`expected/expected.cdx.json` (the answer key)", "reports/reference.json"),
    ("`reports/reference-names-only.cdx.json` (answer key, names and locations only)", "reports/reference-names-only.json"),
    ("`tools/baseline_grep.py` (naive regex)", "reports/baseline_grep.json"),
]
GREP = "reports/baseline_grep.json"
COMPARISON = {
    "scanners": [("QCI v2.3.4.5", "reports/qci-pqc/scorecard-full.json"),
                 ("cdxgen 12.9.1", "reports/cdxgen/scorecard.json"),
                 # Third-party scanners: scored in .github/workflows/third-party-scanners.yml, bundle
                 # read and committed by a person (integrations/third-party/README.md).
                 ],
    "baselines": [("grep baseline", "reports/baseline_grep.json")],
}
DOCS = ["README.md"]
# Each published scorecard has an evidence bundle; their headline numbers must agree.
EVIDENCE = {"reports/qci-pqc/scorecard.json": "evidence/qci-v2.3.4.5",
            "reports/cdxgen/scorecard.json": "evidence/cdxgen-12.9.1",
            "reports/baseline_grep.json": "evidence/grep-baseline",
            "reports/reference.json": "evidence/answer-key"}


# Fix-and-rescan and the large-repository run, per scanner: (column, run bundle, perf bundle)
OPS = [("QCI v2.3.4.5", "evidence/qci-v2.3.4.5", "evidence/perf-qci-v2.3.4.5"),
       ("cdxgen 12.9.1", "evidence/cdxgen-12.9.1", "evidence/perf-cdxgen-12.9.1"),
       ("grep baseline", "evidence/grep-baseline", "evidence/perf-grep-baseline")]


def operations_block() -> str:
    import integrity
    rows = {"Verified remediation (of eligible migrations)": [], "Migrations eligible (of 10)": [],
            "CBOM signed": [], "Second scan of the same input": [],
            "Large repo: finished inside the budget": [], "Large repo: wall time": [], "Large repo: peak memory": [],
            "Large repo: planted uses found": [], "Large repo: found, first vs last quarter of the tree": []}
    sizes = set()
    for name, run_b, perf_b in OPS:
        for b in (run_b, perf_b):  # a bundle that is missing or half-written is a stale doc, not a crash
            if not (ROOT / b / "manifest.json").is_file():
                raise Stale(f"{b} has no manifest.json: rebuild the bundle (bench.py run / perf --bundle {b})")
        m = json.loads((ROOT / run_b / "manifest.json").read_text())
        rem = m.get("remediation") or {}
        if rem.get("verdict") == "scored":
            rows["Verified remediation (of eligible migrations)"].append(
                "none eligible" if not rem["eligible"] else
                f"{rem['verified']}/{rem['eligible']}" + (f" ({rem['verified_pct']}%)" if rem.get("verified_pct") is not None else ""))
            rows["Migrations eligible (of 10)"].append(str(rem["eligible"]))
        else:
            rows["Verified remediation (of eligible migrations)"].append("not run")
            rows["Migrations eligible (of 10)"].append("n/a")
        ip = ROOT / run_b / "integrity.json"
        facts = json.loads(ip.read_text()) if ip.is_file() else None
        rows["CBOM signed"].append(integrity.signed_cell(facts))
        rows["Second scan of the same input"].append(integrity.repeat_cell(facts))
        pm = json.loads((ROOT / perf_b / "manifest.json").read_text())
        res = pm.get("result") or {}
        sizes.add((pm["fixture"]["code_files"], pm["fixture"]["planted"], round(pm["fixture"]["bytes"] / 1e6), pm["budget_s"]))
        q = res.get("recall_by_quartile") or [None] * 4
        rows["Large repo: finished inside the budget"].append("yes" if pm["within_budget"] else pm["status"])
        rows["Large repo: wall time"].append(f"{pm['run']['wall_s']:.0f} s")
        rows["Large repo: peak memory"].append(f"{pm['run']['peak_rss_mb']:.0f} MB")
        rows["Large repo: planted uses found"].append(f"{res.get('found', 0)}/{pm['fixture']['planted']}")
        rows["Large repo: found, first vs last quarter of the tree"].append(f"{q[0]}% / {q[-1]}%")
    out = ["| | " + " | ".join(n for n, _, _ in OPS) + " |", "|---|" + "---|" * len(OPS)]
    out += [f"| {k} | " + " | ".join(v) + " |" for k, v in rows.items()]
    (files, planted, mb, budget), = sizes
    return ("\n".join(out) + f"\n\nFix and rescan: the 10 reference migrations in `remediation/`, scored as in METHODOLOGY.md 4b. "
            "Signed and second scan: reported, not scored (METHODOLOGY.md 4d). "
            f"Large repo: `bench.py perf --size medium` ({files:,} code files, {mb} MB, {planted} planted Tier 1 uses, "
            f"seed 2026), {budget} s budget, same host for every scanner.\n")


def evidence_problems() -> list[str]:
    import bench
    out = []
    for rep_path, b in EVIDENCE.items():
        mf = ROOT / b / "manifest.json"
        if not mf.exists():
            out.append(f"{b}: no evidence bundle for {rep_path}")
            continue
        m = json.loads(mf.read_text())
        if m.get("verdict") != "scored":
            out.append(f"{b}: not scored")
            continue
        want = bench.headline(load(rep_path))
        if m["headline"] != want:
            diff = [k for k in want if want[k] != m["headline"].get(k)]
            out.append(f"{b}: headline differs from {rep_path} on {', '.join(diff)}")
        if m["stamp"]["release"] != release.VERSION or m["methodology"] != release.METHODOLOGY:
            out.append(f"{b}: scored on {m['stamp']['release']} / methodology {m['methodology']}")
        # A report directory and its bundle must give the same gate verdict (the v2.1 review found a
        # SUMMARY.md written before a rebaseline next to a manifest evaluated after it).
        gr = ROOT / Path(rep_path).parent / "gates-result.json"
        if gr.exists() and m.get("gates"):
            g = json.loads(gr.read_text())
            if g.get("report_only"):
                out.append(f"{gr.relative_to(ROOT)}: a report-only run; rerun it gated")
            same = all(g.get(k) == m["gates"].get(k) for k in ("status", "fails", "missing", "skipped"))
            if not same:
                out.append(f"{gr.relative_to(ROOT)} says {g.get('status')} ({len(g.get('fails', []))} failed), "
                           f"{b} says {m['gates']['status']} ({len(m['gates']['fails'])} failed)")
            summary = (gr.parent / "SUMMARY.md").read_text()
            if any(f not in summary for f in g.get("fails", [])) or ("NOT EVALUATED" in summary) != (g["status"] == "not_evaluated" or bool(g.get("missing"))):
                out.append(f"{gr.parent.relative_to(ROOT)}/SUMMARY.md doesn't say what gates-result.json says")
        elif m.get("gates") and (ROOT / Path(rep_path).parent / "SUMMARY.md").exists():
            out.append(f"{Path(rep_path).parent}: no gates-result.json beside SUMMARY.md; rerun the scanner")
    return out

# Grep by tier: README groups buckets and shows the range across them.
GREP_GROUPS = [
    ("1. Direct, Python and Java", ["1/python", "1/java"]),
    ("1. Direct, Go / JavaScript / C", ["1/go", "1/javascript", "1/c"]),
    ("1. Direct, C#", ["1/csharp"]),
    ("2. Indirection, Python and Java", ["2/python", "2/java"]),
    ("2. Indirection, Go / TypeScript / C", ["2/go", "2/typescript", "2/c"]),
    ("2. Indirection, C#", ["2/csharp"]),
    ("3. Cross-file", ["3/python", "3/java"]),
    ("4. Non-code assets", ["4/assets"]),
    ("5. Adversarial, source and bytecode", ["5/python", "5/java"]),
    ("5. Adversarial, minified JS and native binary", ["5/javascript", "5/c"]),
    ("PQC, code", ["pqc/python", "pqc/java", "pqc/go"]),
    ("PQC, assets", ["pqc/assets"]),
    ("Mixed files", ["mixed/python", "mixed/java", "mixed/go", "mixed/javascript", "mixed/typescript", "mixed/c"]),
    ("System fixture", ["system/go", "system/python", "system/java", "system/artifacts", "system/assets"]),
    ("Dead code", ["deadcode/python", "deadcode/java", "deadcode/go", "deadcode/javascript", "deadcode/c"]),
]

BLOCK = re.compile(r"(<!-- generated:(?P<name>[\w-]+)[^>]*-->\n)(?P<body>.*?)(<!-- /generated:(?P=name) -->)", re.S)


class Stale(Exception):
    pass


def load(rel: str) -> dict:
    p = ROOT / rel
    if not p.exists():
        raise Stale(f"{rel}: missing")
    rep = json.loads(p.read_text())
    m = rep.get("manifest")
    if not m:
        raise Stale(f"{rel}: no manifest (scored before 1.17); rescore it")
    cur = release.stamp(m.get("policy", "nist:").split(":")[0])
    diff = [k for k in ("release", "methodology", "answer_key", "corpus", "scorer", "policy") if m.get(k) != cur.get(k)]
    if diff:
        raise Stale(f"{rel}: scored on a different {', '.join(diff)} than this release; rescore it")
    return rep


def pct_range(vals) -> str:
    vals = [v for v in vals if v is not None]
    if not vals:
        return "n/a"
    lo, hi = min(vals), max(vals)
    f = lambda v: f"{v:g}" if v != round(v) else f"{int(round(v))}"  # noqa: E731
    return f"{f(lo)}%" if lo == hi else f"{f(lo)}–{f(hi)}%"


def calibration_block() -> str:
    rows = ["| Run | Findings | Recall | At primary site | Params correct | False positives | Precision | "
            "PQC over-claims | Ticket-ready | Actionable recall |", "|---|---|---|---|---|---|---|---|---|---|"]
    for label, rel in CALIBRATION:
        m = compare.metrics(load(rel))
        f = compare.fmt
        rows.append(f"| {label} | {m['Findings']} | {f(m['Recall'])} | {f(m['At primary site'])} | "
                    f"{f(m['Parameters correct (of detected)'])} | {m['False positives']} | {f(m['Precision'])} | "
                    f"{m['PQC over-claims']} | {f(m['Ticket-ready (of detected)'])} | {f(m['Actionable recall'])} |")
    return "\n".join(rows) + "\n\nShipped corpus only (BYOC example cases excluded), so every row has the same denominator.\n"


def grep_tier_block() -> str:
    rep = load(GREP)
    s = rep["summary"]
    rows = ["| Tier | Findings | Recall | At primary site | Params correct |", "|---|---|---|---|---|"]
    for label, keys in GREP_GROUPS:
        b = [s[k] for k in keys if k in s]
        n = sum(x["expected"] for x in b)
        rows.append(f"| {label} | {n} | {pct_range(x['recall'] for x in b)} | "
                    f"{pct_range(x['usage_site_recall'] for x in b)} | {pct_range(x['params_accuracy'] for x in b)} |")
    return "\n".join(rows) + "\n\nRanges run across the languages in each row.\n"


def comparison() -> tuple[str, dict]:
    sc = {n: load(p) for n, p in COMPARISON["scanners"]}
    bl = {n: load(p) for n, p in COMPARISON["baselines"]}
    problems = compare.eligibility({**sc, **bl})
    if problems:
        raise Stale("comparison: " + "; ".join(problems))
    return compare.render(sc, bl)


def comparison_block(ms: dict) -> str:
    cols = list(ms)
    f = compare.fmt
    n = {ms[c]["Findings"] for c in cols}
    rows = ["| | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for key, label, is_pct in [
            ("Recall", "Recall", True),
            ("Recall incl. signals", "incl. findings reported without an algorithm name", True),
            ("Parameters correct (of detected)", "Parameters correct (of detected)", True),
            ("Precision", "Precision", True),
            ("False positives", "False positives", False),
            ("PQC over-claims", "PQC over-claims", False),
            ("PQC by standard name (of detected PQC)", "PQC by standard name (of detected PQC)", True),
            ("tier:Dead code", "Dead code: recall", True),
            ("tier:System fixture", "System fixture: recall", True),
            ("System fixture: routable (of detected)", "System fixture: routable to the owning team", True),
            ("System fixture: asset links", "System fixture: asset links", True),
            ("Ticket-ready (of detected)", "Ticket-ready (of detected)", True),
            ("tier:Mixed files", "Mixed files: recall", True),
            ("lib:Crypto libraries, in the right manifest", "Crypto libraries, right manifest", True),
            ("lib:Versions correct (of found)", "Library versions correct (of found)", True)]:
        rows.append(f"| {label} | " + " | ".join(f(ms[c].get(key), is_pct) for c in cols) + " |")
    return ("\n".join(rows) + f"\n\nShipped corpus, {'/'.join(str(x) for x in sorted(n))} findings for every column, "
            "no declared scopes. Full tables, by language and tier, in `reports/comparison.md`.\n")


def render_all() -> dict[str, str]:
    """-> {repo-relative path: full new text}"""
    md, ms = comparison()
    blocks = {"calibration-points": calibration_block(), "grep-by-tier": grep_tier_block(),
              "comparison": comparison_block(ms), "operations": operations_block()}
    out = {"reports/comparison.md": md, "reports/comparison.json": compare.to_json(ms)}
    for doc in DOCS:
        text = (ROOT / doc).read_text()
        seen = set()

        def sub(m):
            name = m.group("name")
            if name not in blocks:
                raise Stale(f"{doc}: unknown generated block '{name}'")
            seen.add(name)
            return m.group(1) + blocks[name] + m.group(4)
        out[doc] = BLOCK.sub(sub, text)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if anything is out of date; write nothing")
    a = ap.parse_args()
    try:
        out = render_all()
        ev = evidence_problems()
        if ev:
            raise Stale("evidence bundles out of step with the release scorecards: " + "; ".join(ev))
    except Stale as e:
        print(f"render_docs: {e}", file=sys.stderr)
        return 1
    stale = []
    for rel, new in out.items():
        p = ROOT / rel
        old = p.read_text() if p.exists() else ""
        if old == new:
            continue
        stale.append(rel)
        if a.check:
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), rel, rel + " (regenerated)"))
        else:
            p.write_text(new)
    if a.check:
        print("Docs match the release scorecards." if not stale else
              f"\nOut of date: {', '.join(stale)}. Run python tools/render_docs.py and commit.")
        return 1 if stale else 0
    print("Updated: " + (", ".join(stale) if stale else "nothing (already current)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
