#!/usr/bin/env python3
"""Turn any CycloneDX 1.6 CBOM into a deadline report: what's due, when, under which policy.

Usage:
  python tools/policy_report.py scan.cdx.json [--policy nist --policy cnsa2] [--as-of 2026-11-10]
                                [--use-map uses.json] [--out reports/scan-deadlines]

Works on any CBOM, not just this testbench's corpus: point it at your own scanner output.
Writes <out>.md (readable), <out>.csv (one row per file x algorithm x policy) and <out>.json.

--use-map is a JSON list of [glob, use] pairs, first match wins, e.g.
  [["*/firmware/*", "firmware-signing"], ["infra/vpn/*", "networking"], ["*", "custom"]]
Uses: firmware-signing, networking, web, os, niche, custom. Only CNSA 2.0 dates depend on it.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import FAMILIES, display_name, iter_crypto_findings, load_json, norm_path  # noqa: E402
from policy import BUCKETS, DEFAULT_AS_OF, LABEL, bucket, due_date, evaluate, infer_use, load_policy  # noqa: E402


def inventory(bom: dict) -> list[dict]:
    """Collapse a CBOM to one row per (file, algorithm family), merging what the scanner said."""
    rows = {}
    for family, params, occ, _ in iter_crypto_findings(bom):
        if family not in FAMILIES:
            continue
        for loc, line in occ or [("(no location)", None)]:
            key = (norm_path(loc), family)
            r = rows.setdefault(key, {"file": key[0], "family": family, "params": {}, "lines": set()})
            for k, v in params.items():
                r["params"].setdefault(k, v)
            if isinstance(line, int):
                r["lines"].add(line)
    return sorted(rows.values(), key=lambda r: (r["file"], r["family"]))


def assess(rows, policies, as_of, use_map):
    out = []
    for r in rows:
        use = infer_use(r["file"], use_map)
        for pol in policies:
            v = evaluate(pol, r["family"], r["params"], use)
            out.append({**r, "lines": sorted(r["lines"]), "algorithm": display_name(r["family"], r["params"]),
                        "use": use, "policy": pol["id"], "status": v["status"], "due": due_date(v),
                        "bucket": bucket(v, as_of), "rule": v["rule"], "note": v["note"], "source": v["source"],
                        "quantum_vulnerable": bool(FAMILIES[r["family"]].get("shor"))})
    return out


def to_markdown(name, assessed, policies, as_of) -> str:
    out = [f"# Cryptographic deadline report: {name}", "",
           f"As of **{as_of.isoformat()}**. One row per file and algorithm family found in the CBOM.", ""]
    for pol in policies:
        rows = [a for a in assessed if a["policy"] == pol["id"]]
        out += [f"## {pol['title']}", "", f"_{pol['scope']}_", ""]
        out += ["| When | Findings | Quantum-vulnerable | Files |", "|---|---|---|---|"]
        for key, label, _ in BUCKETS:
            sel = [a for a in rows if a["bucket"] == key]
            out.append(f"| {label} | {len(sel)} | {sum(a['quantum_vulnerable'] for a in sel)} | "
                       f"{len({a['file'] for a in sel})} |")
        out.append("")
        urgent = [a for a in rows if a["bucket"] in ("now", "by-2030")]
        if urgent:
            out += [f"### Due now or by end of 2030 ({len(urgent)})", "",
                    "| Due | Algorithm | File | Why |", "|---|---|---|---|"]
            for a in sorted(urgent, key=lambda a: (a["due"] != "now", a["due"] or "", a["file"])):
                due = "**now**" if a["bucket"] == "now" else a["due"]
                out.append(f"| {due} | {a['algorithm']} | `{a['file']}` | {a['note']} |")
            out.append("")
        review = [a for a in rows if a["status"] in ("review", "unknown")]
        if review:
            out += [f"### Needs a human decision ({len(review)})", ""]
            for a in review:
                out.append(f"- `{a['file']}`: {a['algorithm']}: {a['status']}. {a['note']}")
            out.append("")
    srcs = {s["id"]: s for p in policies for s in p.get("sources", []) + p.get("_parent", {}).get("sources", [])}
    out += ["## Sources", ""]
    for s in srcs.values():
        link = f" ({s['url']})" if s.get("url") else ""
        out.append(f"- **{s['id']}**: {s['name']}. {s['status'].capitalize()}.{link}")
    out += ["", "_Policy rules live in `policies/*.json`. When a standard changes, edit the rule there; "
            "nothing else needs to change._"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cbom")
    ap.add_argument("--policy", action="append", help="policy id in policies/ (repeatable; default nist)")
    ap.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat())
    ap.add_argument("--use-map", help="JSON list of [glob, use] pairs")
    ap.add_argument("--name")
    ap.add_argument("--out")
    a = ap.parse_args()

    policies = [load_policy(p) for p in (a.policy or ["nist"])]
    as_of = dt.date.fromisoformat(a.as_of)
    use_map = json.loads(Path(a.use_map).read_text()) if a.use_map else None
    assessed = assess(inventory(load_json(a.cbom)), policies, as_of, use_map)
    name = a.name or Path(a.cbom).name
    out = Path(a.out) if a.out else Path("reports") / (Path(a.cbom).name.split(".")[0] + "-deadlines")
    out.parent.mkdir(parents=True, exist_ok=True)

    Path(f"{out}.md").write_text(to_markdown(name, assessed, policies, as_of), encoding="utf-8")
    Path(f"{out}.json").write_text(json.dumps(assessed, indent=2) + "\n", encoding="utf-8")
    with open(f"{out}.csv", "w", newline="", encoding="utf-8") as f:
        cols = ["policy", "bucket", "due", "status", "algorithm", "family", "file", "lines", "use",
                "quantum_vulnerable", "rule", "source", "note"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for row in assessed:
            w.writerow({**row, "lines": " ".join(map(str, row["lines"]))})

    for pol in policies:
        counts = defaultdict(int)
        for x in assessed:
            if x["policy"] == pol["id"]:
                counts[x["bucket"]] += 1
        print(f"{pol['id']:<14}" + "  ".join(f"{k}={counts[k]}" for k, _, _ in BUCKETS))
    print(f"Report: {out}.md (+ .csv, .json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
