#!/usr/bin/env python3
"""Compare scanners side by side on the shipped corpus.

  python tools/compare.py \\
      --scanner "QCI v2.3.4.1=reports/qci-pqc/scorecard-full.json" \\
      --scanner "cdxgen 12.9.1=reports/cdxgen/scorecard.json" \\
      --baseline "grep baseline=reports/baseline_grep.json" \\
      --out reports/comparison

Every number is recomputed from the per-finding results, over the shipped corpus only (BYOC cases
are left out). Before anything is rendered the scorecards must be comparable: each carries a
manifest (testbench >= 1.17), and they must share the scored finding set, corpus, answer key,
scorer and policy, and have no declared scope. Otherwise the comparison is refused and the
differences are listed. --allow-scoped renders scoped scorecards anyway, with each column's own
denominator labelled and no "same denominator" claim. Baselines get a column but are left out of
the overlap analysis.

Use the run_* scripts' scorecard-full.json (or score.py --exclude-custom) for unscoped scorecards.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import FAMILIES  # noqa: E402

LANGS = [("Python", {"python"}), ("Java", {"java"}), ("Go", {"go"}), ("JavaScript / TypeScript", {"javascript", "typescript"}),
         ("C / OpenSSL", {"c"}), ("C# / .NET", {"csharp"}), ("Certificates, keys, configs", {"assets"}), ("Built artifacts (system fixture)", {"artifacts"})]
TIERS = [("1. Direct", {1}), ("2. Indirection", {2}), ("3. Cross-file", {3}), ("4. Non-code assets", {4}),
         ("5. Adversarial", {5}), ("Post-quantum", {"pqc"}),
         ("Mixed files", {"mixed"}), ("System fixture", {"system"}), ("Dead code", {"deadcode"})]


MUST_MATCH = ("release", "methodology", "answer_key", "corpus", "scorer", "policy")


def eligibility(cols: dict[str, dict], allow_scoped: bool = False) -> list[str]:
    """-> reasons the scorecards can't share a table; empty when they can."""
    problems = []
    for name, rep in cols.items():
        if "manifest" not in rep:
            problems.append(f"{name}: no manifest (scored before testbench 1.17); rescore it")
        elif rep["manifest"].get("holdout"):
            problems.append(f"{name}: scored on a holdout set, not the shipped corpus")
    if problems:
        return problems
    first, ref = next(iter(cols.items()))
    ref_ids = {r["id"] for r in ref["results"] if r["tier"] != "custom"}
    for name, rep in cols.items():
        m = rep["manifest"]
        if m.get("scope") and not allow_scoped:
            problems.append(f"{name}: scored in a declared scope ({m['scope']}); use the unscoped scorecard "
                            "(scorecard-full.json) or pass --allow-scoped")
        for k in MUST_MATCH:
            if m.get(k) != ref["manifest"].get(k):
                problems.append(f"{name}: {k} {m.get(k)} differs from {first}'s {ref['manifest'].get(k)}")
        ids = {r["id"] for r in rep["results"] if r["tier"] != "custom"}
        scoped_pair = bool(m.get("scope") or ref["manifest"].get("scope"))
        if ids != ref_ids and not (allow_scoped and scoped_pair):
            problems.append(f"{name}: scores {len(ids)} findings, {first} scores {len(ref_ids)} "
                            f"({len(ids - ref_ids)} only here, {len(ref_ids - ids)} only there)")
    return problems


def pct(n, d):
    return round(100 * n / d, 1) if d else None


def _std_names(det):
    pq = [r for r in det if FAMILIES.get(r["family"], {}).get("pq")]
    return pct(sum(1 for r in pq if any(not p.get("prestandard") for p in r.get("reported_params") or [])), len(pq))


def metrics(rep: dict) -> dict:
    res = [r for r in rep["results"] if r["tier"] != "custom"]
    fps = [x for x in rep["false_positives"] if not x["file"].startswith("corpus/custom/")]
    det = [r for r in res if r["detected"]]
    n = len(res)
    sc = rep.get("signal_coverage")
    out = {
        "Findings": n,
        "Recall": pct(len(det), n),
        "Recall incl. signals": sc["combined_recall"] if sc else None,
        "At primary site": pct(sum(r["at_usage_site"] for r in res), n),
        "Parameters correct (of detected)": pct(sum(1 for r in det if r["params_ok"]), len(det)),
        "False positives": len(fps),
        "  in negative controls": sum(1 for x in fps if x["negative_control"]),
        "Precision": pct(len(det), len(det) + len(fps)),
        "PQC over-claims": sum(1 for x in fps if FAMILIES.get(x["family"], {}).get("pq")),
        "PQC by standard name (of detected PQC)": _std_names(det),
        "System fixture: routable (of detected)": (rep.get("linkage") or {}).get("routable_pct"),
        "System fixture: asset links": ((rep["linkage"]["links_found"], rep["linkage"]["links_expected"])
                                        if rep.get("linkage") else None),
        "Ticket-ready (of detected)": pct(sum(1 for r in det if r.get("ticket_ready")), len(det)),
        "Actionable recall": pct(sum(1 for r in det if r.get("ticket_ready")), n),
        "Detected, due by 2030 (NIST)": f"{sum(1 for r in det if (r.get('due') or '9999') <= '2030-12-31')}"
                                        f"/{sum(1 for r in res if (r.get('due') or '9999') <= '2030-12-31')}",
    }
    lib = rep.get("libraries")
    if lib:
        out.update({
            "lib:Crypto libraries, in the right manifest": (lib["found_in_manifest"], lib["expected"]),
            "lib:Found anywhere (incl. no location)": (lib["found_anywhere"], lib["expected"]),
            "lib:Transitive (lockfile)": lib["transitive_recall"],
            "lib:Versions correct (of found)": lib["version_accuracy"],
            "lib:PQC verdicts right": (f"{lib['pq_verdict_accuracy']}% of {lib['pq_verdicts_judged']}"
                                       if lib["pq_verdicts_judged"] else "none given"),
            "lib:False positives": len(lib["false_positives"]),
        })
    for label, langs in LANGS:
        sel = [r for r in res if r["lang"] in langs]
        out[f"lang:{label}"] = (sum(r["detected"] for r in sel), len(sel))
    for label, tiers in TIERS:
        sel = [r for r in res if r["tier"] in tiers]
        out[f"tier:{label}"] = (sum(r["detected"] for r in sel), len(sel))
    return out


THIN = 10


def fmt(v, is_pct=True):
    if v is None:
        return "n/a"
    if isinstance(v, tuple):
        d, n = v
        return (f"{pct(d, n)}% ({d}/{n})" + (" †" if n < THIN else "")) if n else "n/a"
    return f"{v}%" if is_pct and isinstance(v, (int, float)) else str(v)


def overlap(reps: dict[str, dict]) -> dict:
    """Which findings each real scanner catches alone, together, or nobody does."""
    names = list(reps)
    by_id = {}
    for name, rep in reps.items():
        for r in rep["results"]:
            if r["tier"] != "custom":
                by_id.setdefault(r["id"], {"lang": r["lang"], "family": r["family"], "hits": set()})
                if r["detected"]:
                    by_id[r["id"]]["hits"].add(name)
    out = {"nobody": [i for i, v in by_id.items() if not v["hits"]], "all": [i for i, v in by_id.items()
                                                                          if v["hits"] == set(names)]}
    for n in names:
        out[f"only {n}"] = [i for i, v in by_id.items() if v["hits"] == {n}]
    out["_meta"] = by_id
    return out


def to_json(ms: dict) -> str:
    return json.dumps({k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()}
                       for k, v in ms.items()}, indent=2) + "\n"


def render(scanners: dict, baselines: dict, allow_scoped: bool = False) -> tuple[str, dict]:
    """-> (markdown, metrics per column). Call eligibility() first."""
    cols = {**scanners, **baselines}
    ms = {k: metrics(v) for k, v in cols.items()}
    scoped = [c for c in cols if cols[c]["manifest"].get("scope")]

    head = "| | " + " | ".join(cols) + " |"
    sep = "|---|" + "---|" * len(cols)
    m0 = next(iter(cols.values()))["manifest"]
    intro = ("Shipped corpus only, every scanner on the same denominator, no declared scopes. " if not scoped else
             "**Denominators differ.** " + ", ".join(f"{c} is scored in its declared scope ({ms[c]['Findings']} findings)"
                                                     for c in scoped) + "; compare rates, not counts, and read a gap "
             "as possibly a scope difference. ")
    md = ["# Scanner comparison", "", intro +
          "Baselines (" + (", ".join(baselines) or "none") + ") are calibration points, not products.", "",
          f"Testbench {m0['release']}, policy {m0['policy']}, answer key {m0['answer_key']}, scorer {m0['scorer']}. "
          "Scanners: " + "; ".join(f"{c} = {cols[c]['manifest'].get('scanner', '?')}"
                                   + (f" via {cols[c]['manifest']['adapter']}" if cols[c]['manifest'].get('adapter') else "")
                                   for c in cols) + ".", "",
          "## Overall", "", head, sep]
    for key in ["Findings", "Recall", "Recall incl. signals", "At primary site", "Parameters correct (of detected)",
                "Precision", "False positives", "  in negative controls", "PQC over-claims", "PQC by standard name (of detected PQC)", "System fixture: routable (of detected)",
                "System fixture: asset links",
                "Ticket-ready (of detected)", "Actionable recall", "Detected, due by 2030 (NIST)"]:
        is_pct = key not in ("Findings", "False positives", "  in negative controls", "PQC over-claims",
                             "Detected, due by 2030 (NIST)")
        md.append(f"| {key} | " + " | ".join(fmt(ms[c][key], is_pct) for c in cols) + " |")
    lib_keys = [k for k in ms[next(iter(cols))] if k.startswith("lib:")]
    if lib_keys:
        md += ["", "## Crypto libraries (dependency manifests)", "", head, sep]
        for k in lib_keys:
            md.append(f"| {k[4:]} | " + " | ".join(fmt(ms[c].get(k), k not in ("lib:False positives", "lib:PQC verdicts right"))
                                                 for c in cols) + " |")
    for title, prefix, groups in (("By language", "lang:", LANGS), ("By tier", "tier:", TIERS)):
        md += ["", f"## {title} (recall)", "", head, sep]
        for label, _ in groups:
            md.append(f"| {label} | " + " | ".join(fmt(ms[c][prefix + label]) for c in cols) + " |")

    if len(scanners) > 1:
        ov = overlap(scanners)
        meta = ov.pop("_meta")
        md += ["", "## Who finds what", "", "Findings detected by exactly one scanner, by both, or by neither "
               "(baselines excluded).", "", "| | Findings | By language |", "|---|---|---|"]
        for k, ids in ov.items():
            langs = {}
            for i in ids:
                lg = next(lbl for lbl, s in LANGS if meta[i]["lang"] in s)
                langs[lg] = langs.get(lg, 0) + 1
            md.append(f"| {k} | {len(ids)} | " + ", ".join(f"{lg} {n}" for lg, n in sorted(langs.items(), key=lambda x: -x[1])) + " |")
        md += ["", "Families nobody detects, by count: " + ", ".join(
            f"{f} {n}" for f, n in sorted({m["family"]: sum(1 for j in ov["nobody"] if meta[j]["family"] == m["family"])
                                           for m in (meta[i] for i in ov["nobody"])}.items(), key=lambda x: -x[1])[:15])]
    md += ["", f"† fewer than {THIN} findings in the cell: thin evidence, read the rate as an indication."]
    sig = [c for c in cols if cols[c].get("signal_coverage")]
    if sig:
        md += ["", "\"Recall incl. signals\" also credits findings a scanner reported without naming the algorithm: "
               "QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter."]
    return "\n".join(md) + "\n", ms


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scanner", action="append", default=[], help='"Name=path/to/scorecard.json"')
    ap.add_argument("--baseline", action="append", default=[], help='"Name=path" (shown, not in the overlap)')
    ap.add_argument("--out", type=Path, default=Path("reports/comparison"))
    ap.add_argument("--allow-scoped", action="store_true",
                    help="render scorecards with declared scopes; each column's denominator is labelled")
    a = ap.parse_args()
    if not a.scanner:
        ap.error("at least one --scanner")
    load = lambda spec: (spec.split("=", 1)[0], json.loads(Path(spec.split("=", 1)[1]).read_text()))  # noqa: E731
    scanners = dict(load(s) for s in a.scanner)
    baselines = dict(load(s) for s in a.baseline)
    cols = {**scanners, **baselines}
    problems = eligibility(cols, a.allow_scoped)
    if problems:
        print("Refusing to compare: these scorecards weren't measured on the same thing.", file=sys.stderr)
        print("  " + "\n  ".join(problems), file=sys.stderr)
        return 2
    md, ms = render(scanners, baselines, a.allow_scoped)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    Path(f"{a.out}.md").write_text(md)
    Path(f"{a.out}.json").write_text(to_json(ms))
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
