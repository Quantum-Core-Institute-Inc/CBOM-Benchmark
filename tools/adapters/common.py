"""Pieces shared by scanner adapters: signal coverage for findings a scanner reports without naming
the algorithm (QCI's risk categories, cdxgen's crypto-file entries)."""
from __future__ import annotations

from cbomlib import same_file


def key_material(fam, f, mat_idx):
    """The finding is a key or certificate's key (Tier 4 / PQC assets)."""
    return mat_idx.get(f["id"], (None, None))[1] == "key"


def _near(sig_line, lines, tol=1):
    if not lines or not isinstance(sig_line, int):
        return True  # file-level asset, or a signal without a line
    return any(abs(sig_line - ln) <= tol for ln in lines)


def signal_coverage(report: dict, gt: dict, signals: list[dict], mat_idx: dict, predicates: dict,
                    informational: frozenset | set = frozenset()) -> dict:
    """Credit signals with ground-truth findings they plausibly describe: same file, same line (±1)
    when the signal has one, and predicates[category](family, finding, mat_idx) true.

    report: the strict scorer result (already scope-filtered); gt: ground truth with resolved lines."""
    by_id = {f["id"]: f for f in gt["findings"]}
    covered, by_category, used = {}, {}, set()
    for r in report["results"]:
        f = by_id[r["id"]]
        places = [(f["file"], f.get("lines", []))] + [(a["file"], a.get("lines", [])) for a in f.get("alt_files", [])]
        for i, s in enumerate(signals):
            pred = predicates[s["category"]]
            if not any(same_file(s["location"], p) and _near(s["line"], lines) for p, lines in places):
                continue
            if pred(f["family"], f, mat_idx):
                covered.setdefault(r["id"], []).append(s["category"])
                by_category.setdefault(s["category"], set()).add(r["id"])
                used.add(i)
    results = report["results"]
    strict = {r["id"] for r in results if r["detected"]}
    signal_only = [rid for rid in covered if rid not in strict]
    unused = [s for i, s in enumerate(signals) if i not in used and s["category"] not in informational]
    n = len(results)
    return {
        "expected": n,
        "strict_detected": len(strict),
        "signal_only": len(signal_only),
        "combined": len(strict | set(covered)),
        "strict_recall": round(100 * len(strict) / n, 1) if n else None,
        "combined_recall": round(100 * len(strict | set(covered)) / n, 1) if n else None,
        "signal_only_ids": sorted(signal_only),
        "by_category": {k: len(v) for k, v in sorted(by_category.items())},
        "signals_total": len(signals),
        "signals_matching_nothing": unused,
    }
