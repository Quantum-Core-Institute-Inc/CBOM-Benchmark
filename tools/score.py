#!/usr/bin/env python3
"""Score a scanner's CycloneDX 1.6 CBOM against the testbench ground truth.

Usage:
  python tools/score.py path/to/scanner-output.cdx.json [--name "Scanner X"] [--out reports/scanner-x]

Writes <out>.md (human scorecard) and <out>.json (machine-readable) and prints a summary.

Matching rules (also in README):
  * A finding is DETECTED when the scanner reports the same algorithm family in the
    expected file (or one of its alt_files). Names are normalized first.
  * PARAMS are correct when every expected parameter (key size, curve, mode, hash) matches.
  * LINE is accurate when a reported line is within +/-tolerance of any anchor line.
  * Mixed files (corpus/mixed/) hold several uses of one family in one file, so their findings are
    SITE findings: a reported occurrence counts for the site whose anchor line is nearest, if it is
    within SITE_WINDOW lines, and params are judged on that site's occurrences only. An occurrence
    with no line can't be placed, so it detects no site. Occurrences that match no site are false
    positives, one per cluster of nearby lines (plus one for any without a line).
  * Declared scopes: a file-level rule (glob) removes that file's findings and its false positives;
    a rule naming finding ids or a certificate role removes those findings only.
  * A reported (file, family) pair that matches no finding and isn't in also_ok is a
    FALSE POSITIVE. Names the normalizer can't classify (padding schemes, RNGs, etc.)
    are listed as UNRECOGNIZED for manual review and not scored.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_expected import resolve  # noqa: E402
from cbomlib import FAMILIES, display_name, expected_quantum_level, iter_crypto_findings_ctx, load_json, same_file  # noqa: E402
import actionability as act  # noqa: E402
import libraries as libs  # noqa: E402
import datetime as dt  # noqa: E402
from truth import attach_facts, load_ground_truth  # noqa: E402
from policy import BUCKETS, DEFAULT_AS_OF, LABEL, WEIGHT, bucket, due_date, evaluate, infer_use, load_policy  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
SITE_WINDOW = 3  # lines either side of a site's anchors that still count as that site


def load_truth(include_custom: bool = True, gt: dict | None = None):
    """The shipped answer key (plus BYOC cases), or `gt` as given. Findings that already carry
    resolved "lines" (generated holdout sets) keep them; anchors are resolved otherwise."""
    gt = attach_facts(load_ground_truth(include_custom)) if gt is None else gt
    for f in gt["findings"]:
        if "lines" not in f:
            f["lines"] = resolve(f["file"], f.get("anchors", []), f["id"])
        for alt in f.get("alt_files", []):
            if "lines" not in alt:
                alt["lines"] = resolve(alt["file"], alt.get("anchors", []), f["id"])
    also_ok = defaultdict(set)
    for e in gt.get("also_ok", []):
        also_ok[e["file"]].update(e["families"])
    return gt, also_ok


def corpus_files(corpus: Path = CORPUS):
    """Corpus files as "corpus/..." paths, wherever that corpus directory lives."""
    return sorted(str(p.relative_to(corpus.parent)).replace("\\", "/") for p in corpus.rglob("*") if p.is_file())


def bucket_of(path: str) -> tuple[str, str]:
    parts = path.split("/")
    return parts[1], parts[2]  # e.g. ("tier1", "python") or ("negatives", "java")


def collect(bom: dict, files: list[str]):
    """Group scanner output by (corpus file, family)."""
    groups = defaultdict(lambda: {"params": [], "lines": [], "levels": [], "entries": []})
    unrecognized, out_of_scope, unlocated = [], 0, 0
    for family, params, occ, level, ctx in iter_crypto_findings_ctx(bom):
        if not occ:
            unlocated += 1
            continue
        for loc, line in occ:
            match = next((f for f in files if same_file(loc, f)), None)
            if match is None:
                out_of_scope += 1
                continue
            if family not in FAMILIES:
                unrecognized.append({"file": match, "name": family, "line": line})
                continue
            g = groups[(match, family)]
            g["params"].append(params)
            g["entries"].append({"ctx": ctx, "params": params, "line": line, "path": match, "level": level})
            if isinstance(line, int):
                g["lines"].append(line)
            if level is not None:
                g["levels"].append(level)
    return groups, unrecognized, out_of_scope, unlocated


def _manifest(results: list, policy: str, scope: dict | None, holdout: bool, custom: str) -> dict:
    """What this scorecard was measured against; compare.py refuses to put mismatched ones side by side."""
    import release
    ids = [r["id"] for r in results if r["tier"] != "custom"]
    st = release.stamp(policy)
    if holdout:  # a generated holdout set: its own answer key and corpus
        st = {k: v for k, v in st.items() if k not in ("answer_key", "corpus", "findings")}
    return {**st, "holdout": holdout, "custom": custom,
            "scored_findings": len(ids), "finding_set": release.findings_sha(ids),
            "scope": (scope or {}).get("name") if scope else None}


def assign_sites(findings: list[dict], groups: dict, window: int = SITE_WINDOW, unplaced: dict | None = None) -> dict:
    """Site findings share a (file, family) group. Each reported occurrence goes to the site with the
    nearest anchor line, if within `window`. -> {finding id: group-shaped dict of its occurrences}
    unplaced: if given, filled with {(file, family): [lines that belong to no site]} (None = no line)."""
    by_key = defaultdict(list)
    site_lines = defaultdict(lambda: defaultdict(list))
    for f in findings:
        if f.get("site") and f["lines"]:
            by_key[(f["file"], f["family"])].append(f)
            site_lines[f["file"]][f["family"]].extend(f["lines"])
    out = {}
    for key, sites in by_key.items():
        g = groups.get(key)
        if not g:
            continue
        for e in g["entries"]:
            if not isinstance(e["line"], int):
                if unplaced is not None:
                    unplaced.setdefault(key, []).append(None)
                continue
            dist, best = min((min(abs(e["line"] - ln) for ln in f["lines"]), i) for i, f in enumerate(sites))
            if dist > window:
                if unplaced is not None and not neutral_occurrence(key[0], key[1], e["line"], site_lines):
                    unplaced.setdefault(key, []).append(e["line"])
                continue
            mine = out.setdefault(sites[best]["id"], {"params": [], "lines": [], "levels": [], "entries": []})
            mine["params"].append(e["params"])
            mine["lines"].append(e["line"])
            mine["entries"].append(e)
            if e.get("level") is not None:
                mine["levels"].append(e["level"])
    return out


_IMPORT = re.compile(r"""^\s*(?:from\s+\S+\s+import\b|import\b|\#\s*include\b|package\b)|\brequire\s*\(""")
_GO_IMPORT_SPEC = re.compile(r'^\s*(?:[\w.]+\s+)?"[^"]+"\s*$')
_lines_cache: dict = {}


def _source_lines(path: str) -> list[str]:
    if path not in _lines_cache:
        p = ROOT / path
        try:
            _lines_cache[path] = p.read_text(errors="replace").splitlines()
        except OSError:
            _lines_cache[path] = []
    return _lines_cache[path]


def is_import_line(path: str, line: int) -> bool:
    """An import/include/require line. It names a crypto module, not a use of it, so a report there
    is neither credit nor noise."""
    src = _source_lines(path)
    if not 1 <= line <= len(src):
        return False
    text = src[line - 1]
    if _IMPORT.search(text):
        return True
    if path.endswith(".go") and _GO_IMPORT_SPEC.match(text):  # inside an import ( ... ) block
        for prev in reversed(src[:line - 1]):
            if prev.strip().startswith(")"):
                return False
            if prev.strip().startswith("import"):
                return True
    return False


def neutral_occurrence(path: str, family: str, line: int, site_lines: dict) -> bool:
    """An unplaced occurrence that isn't a false positive either: on an import line, or a hash or MAC
    reported at another algorithm's site (HMAC inside pbkdf2_hmac, SHA-256 inside a signature),
    which is the per-site version of also_ok."""
    if is_import_line(path, line):
        return True
    if FAMILIES.get(family, {}).get("primitive") in ("hash", "mac"):
        return any(abs(line - ln) <= SITE_WINDOW for fam, lns in site_lines.get(path, {}).items()
                   if fam != family for ln in lns)
    return False


def unplaced_clusters(lines: list, window: int = SITE_WINDOW) -> list[list]:
    """Occurrences that match no site, grouped: lines within `window` of each other are one report;
    every occurrence without a line is one more."""
    nums = sorted({ln for ln in lines if isinstance(ln, int)})
    clusters = []
    for ln in nums:
        if clusters and ln - clusters[-1][-1] <= window:
            clusters[-1].append(ln)
        else:
            clusters.append([ln])
    if any(ln is None for ln in lines):
        clusters.append([])
    return clusters


def load_scope(path) -> dict | None:
    return load_json(path) if path else None


def scope_reason(f: dict, scope: dict | None, mat_idx: dict) -> str | None:
    """Why a finding is outside the scanner's declared scope, or None if it's in scope.

    A scope file lists rules: {"glob": "*.jar", "reason": ...} matches the finding's file (full path
    or basename); {"cert_role": "signature", "reason": ...} matches findings that come from a
    certificate's signature rather than its key; {"ids": [...], "reason": ...} names findings."""
    if not scope:
        return None
    from fnmatch import fnmatch
    for rule in scope.get("out_of_scope", []):
        if "glob" in rule and (fnmatch(f["file"], rule["glob"]) or fnmatch(Path(f["file"]).name, rule["glob"])):
            return rule["reason"]
        if "cert_role" in rule and mat_idx.get(f["id"], (None, None))[1] == rule["cert_role"]:
            return rule["reason"]
        if f["id"] in rule.get("ids", []):
            return rule["reason"]
    return None


def score(bom: dict, tolerance: int = 1, policy: str = "nist", as_of: dt.date = DEFAULT_AS_OF,
          custom: str = "include", scope: dict | None = None, truth: dict | None = None,
          corpus: Path | None = None) -> dict:
    """custom: 'include' (default), 'exclude' (the shipped benchmark only) or 'only' (your own cases only).
    scope: a declared-scope dict (see scope_reason); findings outside it are reported, not scored.
    truth / corpus: score against another answer key and corpus directory (a generated holdout set,
    see tools/holdout.py) instead of the shipped one."""
    gt, also_ok = load_truth(include_custom=custom != "exclude", gt=truth)
    if custom == "only":
        gt["findings"] = [f for f in gt["findings"] if f["tier"] == "custom"]
    cal_ids = {f["id"] for f in gt["findings"] if f.get("calibration")}
    pol = load_policy(policy)
    rubric = act.load_rubric()
    mat_idx = act.material_index(gt)
    files = corpus_files(corpus or CORPUS)
    groups, unrecognized, out_of_scope, unlocated = collect(bom, files)
    consumed = set()
    results = []
    unplaced = {}
    site_groups = assign_sites(gt["findings"], groups, unplaced=unplaced)

    for f in gt["findings"]:
        if f.get("site"):
            key = (f["file"], f["family"])
            if key in groups:
                consumed.add(key)  # judged per occurrence below: reports that match no site are false positives
            mine = site_groups.get(f["id"])
            hit_groups = [(f["file"], f["lines"], mine)] if mine else []
        else:
            places = [(f["file"], f["lines"])] + [(a["file"], a["lines"]) for a in f.get("alt_files", [])]
            hit_groups = [(path, lines, groups[(path, f["family"])]) for path, lines in places if (path, f["family"]) in groups]
        for path, _, _ in hit_groups:
            consumed.add((path, f["family"]))

        r = {"id": f["id"], "tier": f["tier"], "lang": f["lang"], "file": f["file"], "family": f["family"],
             "expected_params": f["params"], "expected_line": f["lines"][0] if f["lines"] else None,
             "detected": bool(hit_groups),
             "at_usage_site": bool(hit_groups) if f.get("site") else (f["file"], f["family"]) in groups,
             "params_ok": None, "line_ok": None, "quantum_ok": None,
             "reported_params": [], "reported_lines": [], "reported_files": sorted({p for p, _, _ in hit_groups})}
        # Which rule decided detection, so a disputed result can be traced (METHODOLOGY.md section 2).
        if not hit_groups:
            r["rule"] = "missed: no report of this family in the file" + (" or its alt files" if f.get("alt_files") else "") \
                        + (f" within {SITE_WINDOW} lines of the site" if f.get("site") else "")
        elif f.get("site"):
            r["rule"] = f"site-match/window={SITE_WINDOW}"
        elif (f["file"], f["family"]) in groups:
            r["rule"] = "file+family"
        else:
            r["rule"] = "alt-file+family"
        v = evaluate(pol, f["family"], f["params"], f.get("use") or infer_use(f["file"]), f.get("primitive"))
        r["due"], r["due_bucket"], r["due_note"] = due_date(v), bucket(v, as_of), v["note"]
        r["algorithm"] = display_name(f["family"], f["params"])
        if hit_groups:
            all_params = [p for _, _, g in hit_groups for p in g["params"]]
            r["reported_params"] = all_params
            r["params_ok"] = any(all(p.get(k) == v for k, v in f["params"].items()) for p in all_params)
            r["reported_lines"] = sorted({ln for _, _, g in hit_groups for ln in g["lines"]})
            judged = [(lines, g) for _, lines, g in hit_groups if lines and g["lines"]]
            if judged:  # file-level assets (PEM, DER, keystores) have no line to judge
                r["line_ok"] = any(abs(ln - want) <= tolerance
                                   for lines, g in judged for ln in g["lines"] for want in lines)
            levels = [lv for _, _, g in hit_groups for lv in g["levels"]]
            exp_level = expected_quantum_level(f["family"], f["params"])
            if levels and exp_level is not None:
                r["quantum_ok"] = (levels[0] == 0) == (exp_level == 0)
        r["actionability"] = act.assess(f, r, [e for _, _, g in hit_groups for e in g["entries"]],
                                        mat_idx.get(f["id"])) if hit_groups else {}
        results.append(r)

    oos = []
    if scope:
        keep = []
        for r in results:
            why = scope_reason(next(f for f in gt["findings"] if f["id"] == r["id"]), scope, mat_idx)
            (oos.append({**r, "scope_reason": why}) if why else keep.append(r))
        results = keep
    def file_out_of_scope(path):
        # Only file-level rules (globs) say the scanner doesn't read a file. Excluding a finding by
        # id or certificate role removes that finding, never the other reports in its file.
        return bool(scope) and scope_reason({"id": "", "file": path}, scope, {}) is not None
    # Calibration cases (corpus/calibration/, see build_calibration.py) feed the overfit gap only.
    calibration = [r for r in results if r["id"] in cal_ids]
    results = [r for r in results if r["id"] not in cal_ids]
    cal_fps = []

    false_positives = []
    for (path, family), g in sorted(groups.items()):
        if (path, family) in consumed or family in also_ok.get(path, set()):
            continue
        if file_out_of_scope(path):
            continue  # a file the scanner says it doesn't read: no false positives there either
        in_custom = path.startswith("corpus/custom/")
        if (custom == "only" and not in_custom) or (custom == "exclude" and in_custom):
            continue
        if path.startswith("corpus/calibration/"):
            cal_fps.append({"file": path, "family": family})
            continue
        false_positives.append({"file": path, "family": family, "lines": sorted(set(g["lines"])),
                                "negative_control": path.startswith("corpus/negatives/"),
                                "rule": "unmatched: no finding of this family in this file, not in also_ok"})
    # Site-level truth (mixed files): each report of a family the file uses, but nowhere near any of
    # its sites, is a false positive of its own.
    for (path, family), lines in sorted(unplaced.items()):
        if family in also_ok.get(path, set()) or file_out_of_scope(path):
            continue
        for cl in unplaced_clusters(lines):
            fp = {"file": path, "family": family, "lines": cl, "negative_control": False, "kind": "unplaced",
                  "rule": f"unplaced/window={SITE_WINDOW}: no site of this family within {SITE_WINDOW} lines"}
            (cal_fps if path.startswith("corpus/calibration/") else false_positives).append(fp)

    return {"results": results, "false_positives": false_positives, "unrecognized": unrecognized,
            "scope": {"name": scope.get("name"), "excluded": oos} if scope else None,
            "out_of_scope_occurrences": out_of_scope, "unlocated_components": unlocated,
            "summary": summarize(results, false_positives),
            "linkage": __import__("linkage").evaluate(results, gt, bom),
            "deadlines": summarize_deadlines(results, pol, as_of),
            "actionability": act.summarize(results, rubric),
            "libraries": libs.score_libraries(bom) if truth is None and custom != "only" else None,
            "calibration_results": calibration, "calibration_false_positives": cal_fps,
            "manifest": _manifest(results, policy, scope, truth is not None, custom)}


def summarize_deadlines(results, pol, as_of):
    """Recall by when the finding falls due, and recall weighted so misses that are due sooner cost more."""
    by = {}
    for key, label, weight in BUCKETS:
        sel = [r for r in results if r["due_bucket"] == key]
        det = sum(1 for r in sel if r["detected"])
        at_site = sum(1 for r in sel if r["at_usage_site"])
        by[key] = {"label": label, "weight": weight, "expected": len(sel), "detected": det,
                   "recall": pct(det, len(sel)), "primary_site_recall": pct(at_site, len(sel))}
    total_w = sum(WEIGHT[r["due_bucket"]] for r in results)
    got_w = sum(WEIGHT[r["due_bucket"]] for r in results if r["detected"])
    site_w = sum(WEIGHT[r["due_bucket"]] for r in results if r["at_usage_site"])
    missed = [r for r in results if not r["detected"] and r["due_bucket"] in ("now", "by-2030")]
    return {"policy": pol["id"], "title": pol["title"], "as_of": as_of.isoformat(), "buckets": by,
            "weighted_recall": pct(got_w, total_w), "weighted_primary_site_recall": pct(site_w, total_w),
            "missed_due_by_2030": [{"id": r["id"], "algorithm": r["algorithm"], "file": r["file"],
                                    "due": r["due"], "why": r["due_note"]} for r in missed]}


def pct(n, d):
    return None if d == 0 else round(100.0 * n / d, 1)


THIN = 10  # cells with fewer findings than this are flagged as thin evidence


def wilson(n, d, z=1.96):
    """95% Wilson score interval for n successes in d trials, in percent. None when d == 0."""
    if not d:
        return None
    p = n / d
    den = 1 + z * z / d
    mid = (p + z * z / (2 * d)) / den
    half = z * ((p * (1 - p) / d + z * z / (4 * d * d)) ** 0.5) / den
    return [round(100 * max(0.0, mid - half), 1), round(100 * min(1.0, mid + half), 1)]


def bucket_key(tier, lang) -> str:
    return f"{tier}/{lang}"


def bucket_dir(tier, lang) -> str:
    """Numbered tiers live in corpus/tierN/<lang>/; the PQC category in corpus/pqc/<lang>/."""
    return f"corpus/tier{tier}/{lang}/" if isinstance(tier, int) else f"corpus/{tier}/{lang}/"


def bucket_label(key: str) -> str:
    tier, lang = key.split("/")
    if tier.isdigit():
        return f"Tier {tier} {lang}"
    if tier == "custom":
        return f"Your case: {lang}"
    if tier == "system":
        return f"System fixture {lang}"
    return f"Mixed files {lang}" if tier == "mixed" else f"{tier.upper()} {lang}"


def system_lang(path: str) -> str:
    """Bucket of a file in the system fixture, for false positives (it has no per-language dirs)."""
    p = Path(path)
    if p.suffix == ".jar" or "/bin/" in path:
        return "artifacts"
    return {".go": "go", ".py": "python", ".java": "java"}.get(p.suffix, "assets")


def summarize(results, fps):
    rows = {}
    order = lambda t: (not isinstance(t[0], int), str(t[0]), t[1])  # noqa: E731  numbered tiers first
    keys = sorted({(r["tier"], r["lang"]) for r in results}, key=order) + [("all", "all")]
    for tier, lang in keys:
        sel = [r for r in results if tier == "all" or (r["tier"] == tier and r["lang"] == lang)]
        det = [r for r in sel if r["detected"]]
        bdir = None if tier == "all" else bucket_dir(tier, lang)
        if tier == "system":
            fp = [x for x in fps if x["file"].startswith("corpus/system/") and system_lang(x["file"]) == lang]
        else:
            fp = [x for x in fps if not x["negative_control"] and (bdir is None or x["file"].startswith(bdir))]
        line_judged = [r for r in det if r["line_ok"] is not None]
        q_judged = [r for r in det if r["quantum_ok"] is not None]
        rows[f"{tier}/{lang}"] = {
            "expected": len(sel), "detected": len(det), "recall": pct(len(det), len(sel)),
            "recall_ci95": wilson(len(det), len(sel)), "thin": len(sel) < THIN,
            "usage_site_recall": pct(sum(1 for r in sel if r["at_usage_site"]), len(sel)),
            "params_correct": sum(1 for r in det if r["params_ok"]),
            "params_accuracy": pct(sum(1 for r in det if r["params_ok"]), len(det)),
            "line_accuracy": pct(sum(1 for r in line_judged if r["line_ok"]), len(line_judged)),
            "quantum_flag_accuracy": pct(sum(1 for r in q_judged if r["quantum_ok"]), len(q_judged)),
            "false_positives": len(fp),
            "precision": pct(len(det), len(det) + len(fp)),
        }
    neg = [x for x in fps if x["negative_control"]]
    rows["negatives"] = {"false_positives": len(neg)}
    # PQC over-claims: post-quantum or hybrid algorithms reported where the code has none.
    # The costliest kind of false positive for a migration program: it marks work as done.
    over = [x for x in fps if FAMILIES.get(x["family"], {}).get("pq")]
    rows["pqc_overclaims"] = {"count": len(over), "files": sorted({x["file"] for x in over})}
    # Standardised names: a detected PQC finding still earns discovery credit when the scanner calls
    # it Kyber or Dilithium, but only counts here when at least one report uses the FIPS 203/204/205
    # name (or OID). Pre-standard algorithms are not the standards; an inventory that can't tell them
    # apart can't tell you whether a system will interoperate with a FIPS module.
    pq_det = [r for r in results if r["detected"] and FAMILIES.get(r["family"], {}).get("pq")]
    std = [r for r in pq_det if any(not p.get("prestandard") for p in r["reported_params"])]
    rows["pqc_standard_names"] = {"detected": len(pq_det), "standard": len(std),
                                  "accuracy": pct(len(std), len(pq_det)),
                                  "prestandard_only": sorted(r["id"] for r in pq_det if r not in std)}
    total_fp = len(fps)
    all_det = rows["all/all"]["detected"]
    rows["all/all"]["false_positives"] = total_fp
    rows["all/all"]["precision"] = pct(all_det, all_det + total_fp)
    return rows


def fmt(v, suffix="%"):
    return "n/a" if v is None else f"{v}{suffix}"


def to_markdown(name: str, rep: dict) -> str:
    s = rep["summary"]
    out = [f"# CBOM Testbench Scorecard: {name}", ""]
    a = s["all/all"]
    out += [f"**Overall:** {a['detected']}/{a['expected']} findings detected ({fmt(a['recall'])} recall), "
            f"{a['false_positives']} false positives ({fmt(a['precision'])} precision), "
            f"parameters correct on {fmt(a['params_accuracy'])} of detections.", ""]
    cal = rep.get("calibration_results") or []
    if cal:
        cd = sum(1 for r in cal if r["detected"])
        out += [f"Calibration cases (generated Tier 1-2 siblings of the hand-written cases; they feed the holdout's "
                f"overfit gap and are not counted anywhere else here): {cd}/{len(cal)} detected "
                f"({fmt(pct(cd, len(cal)))}), {len(rep.get('calibration_false_positives') or [])} false positives.", ""]
    out += ["| Bucket | Detected | Recall | 95% interval | At primary site | Params correct | Line accurate | Quantum flag | False pos. | Precision |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in s.items():
        if k in ("negatives", "pqc_overclaims", "pqc_standard_names"):
            continue
        label = "**Total**" if k == "all/all" else bucket_label(k)
        ci = v.get("recall_ci95")
        ci_s = f"{ci[0]}–{ci[1]}%" + (" (thin)" if v.get("thin") else "") if ci else "n/a"
        out.append(f"| {label} | {v['detected']}/{v['expected']} | {fmt(v['recall'])} | {ci_s} | {fmt(v['usage_site_recall'])} | "
                   f"{fmt(v['params_accuracy'])} | {fmt(v['line_accuracy'])} | {fmt(v['quantum_flag_accuracy'])} | "
                   f"{v['false_positives']} | {fmt(v['precision'])} |")
    out.append(f"| Negative controls | | | | | | | | {s['negatives']['false_positives']} | |")
    out.append("")
    thin = [k for k, v in s.items() if isinstance(v, dict) and v.get("thin")]
    if thin:
        out.append(f"Intervals are 95% Wilson intervals on recall. {len(thin)} bucket(s) have fewer than {THIN} findings "
                   "and are marked thin: read their rates as indications, not measurements.")
        out.append("")
    oc = s["pqc_overclaims"]
    out.append(f"**PQC over-claims: {oc['count']}.** Post-quantum or hybrid algorithms reported where the "
               "code or config has none. Each one makes migration look further along than it is. "
               "Any number above zero should be explained by the vendor before purchase.")
    out.append("")
    sn = s.get("pqc_standard_names")
    if sn and sn["detected"]:
        out.append(f"**PQC by standard name: {sn['standard']}/{sn['detected']} ({fmt(sn['accuracy'])}).** Detected "
                   "post-quantum findings reported under the FIPS 203/204/205 name or OID. Reports that only say "
                   "Kyber, Dilithium, SPHINCS+ or Falcon keep their recall credit and fail this check.")
        out.append("")
    lk = rep.get("linkage")
    if lk:
        import linkage
        out.append(linkage.markdown(lk))
    out.append("**Recall** counts a finding reported anywhere acceptable, including the config or constants file "
               "that names the algorithm. **At primary site** counts only findings reported in the file the "
               "ground truth anchors them to: the crypto call itself or, for a shared wrapper, the caller that "
               "binds the parameters. It's the stricter number, and the one that tells an engineer what to change.")
    out.append("")
    out.append("False positives in the bucket rows are those inside positive test files; negative-control "
               "false positives are counted separately and included in the total.")
    out.append("")

    misses = [r for r in rep["results"] if not r["detected"]]
    d = rep["deadlines"]
    out += [f"## Deadline view: {d['title']}", "",
            f"As of {d['as_of']}. Each expected finding is dated under this policy; misses that fall due "
            "sooner weigh more.", "",
            f"**Deadline-weighted recall: {fmt(d['weighted_recall'])}** (at primary site: "
            f"{fmt(d['weighted_primary_site_recall'])}). "
            f"**Findings due by end of 2030 that this scanner missed: {len(d['missed_due_by_2030'])}.**", "",
            "| When it's due | Weight | Detected | Recall | At primary site |", "|---|---|---|---|---|"]
    for key, b in d["buckets"].items():
        out.append(f"| {b['label']} | {b['weight']} | {b['detected']}/{b['expected']} | {fmt(b['recall'])} | "
                   f"{fmt(b['primary_site_recall'])} |")
    out.append("")
    if d["missed_due_by_2030"]:
        out += ["| Missed | Algorithm | Due | File |", "|---|---|---|---|"]
        for m in d["missed_due_by_2030"]:
            out.append(f"| {m['id']} | {m['algorithm']} | {'**now**' if m['due'] == 'now' else m['due']} | `{m['file']}` |")
        out.append("")

    ac = rep["actionability"]
    out += ["## Actionability: could an engineer open a ticket from this?", "",
            f"Rubric `{ac['rubric']}` ({ac['rubric_status']}; see `rubric/actionability.json`). Each detected finding is "
            "checked for the fields a migration ticket needs. Facts are checked against the real files.", "",
            f"**Ticket-ready: {ac['ticket_ready']}/{ac['detected']} detected findings ({fmt(ac['ticket_ready_pct'])})**, "
            f"meaning every must-have is present and correct. **Actionable recall: {fmt(ac['actionable_recall'])}** "
            f"of all {ac['expected']} expected findings were both found and ticket-ready. "
            f"Field completeness across all checks: {fmt(ac['completeness_pct'])}.", "",
            "| Check | Tier | Applies to | Passed | Rate |", "|---|---|---|---|---|"]
    for cid, c in ac["checks"].items():
        out.append(f"| {c['label']} | {c['tier']} | {c['applicable']} | {c['passed']} | {fmt(c['pct'])} |")
    out.append("")
    not_ready = [r for r in rep["results"] if r["detected"] and not r.get("ticket_ready")]
    if not_ready:
        out += [f"Detected but not ticket-ready ({len(not_ready)}), first 25:", "",
                "| ID | Algorithm | Missing must-haves |", "|---|---|---|"]
        labels = {cid: c["label"] for cid, c in ac["checks"].items()}
        for r in not_ready[:25]:
            out.append(f"| {r['id']} | {r['algorithm']} | {', '.join(labels[m] for m in r['missing_must'])} |")
        out.append("")

    if rep.get("scope"):
        ex = rep["scope"]["excluded"]
        out += [f"## Outside declared scope: {rep['scope']['name']}", "",
                f"{len(ex)} expected findings fall outside what this scanner says it covers. They are not counted "
                f"above. {sum(1 for r in ex if r['detected'])} were detected anyway.", "",
                "| ID | Algorithm | File | Detected anyway | Why out of scope |", "|---|---|---|---|---|"]
        for r in ex:
            out.append(f"| {r['id']} | {r['algorithm']} | `{r['file']}` | {'yes' if r['detected'] else 'no'} | {r['scope_reason']} |")
        out.append("")

    out += ["## Missed findings", ""]
    if misses:
        out += ["| ID | File | Expected | Line |", "|---|---|---|---|"]
        for r in misses:
            out.append(f"| {r['id']} | `{r['file']}` | {r['family']} {r['expected_params'] or ''} | {r['expected_line'] or 'file'} |")
    else:
        out.append("None.")
    out.append("")

    wrong = [r for r in rep["results"] if r["detected"] and not r["params_ok"]]
    out += ["## Detected with wrong or missing parameters", ""]
    if wrong:
        out += ["| ID | Family | Expected params | Reported params |", "|---|---|---|---|"]
        for r in wrong:
            rp = "; ".join(json.dumps(p) for p in r["reported_params"]) or "none"
            out.append(f"| {r['id']} | {r['family']} | `{json.dumps(r['expected_params'])}` | `{rp}` |")
    else:
        out.append("None.")
    out.append("")

    out += ["## False positives", ""]
    if rep["false_positives"]:
        out += ["| File | Reported family | Lines | Negative control? |", "|---|---|---|---|"]
        for x in rep["false_positives"]:
            out.append(f"| `{x['file']}` | {x['family']} | {', '.join(map(str, x['lines'])) or '?'} | "
                       f"{'yes' if x['negative_control'] else 'no'} |")
    else:
        out.append("None.")
    out.append("")

    if rep["unrecognized"]:
        out += ["## Unrecognized names (not scored, review manually)", ""]
        for u in rep["unrecognized"]:
            out.append(f"- `{u['file']}` line {u['line']}: {u['name']}")
        out.append("")

    if rep.get("libraries"):
        out += [libs.to_markdown(rep["libraries"])]

    out += ["## Per-finding detail", "",
            "| ID | Family | Detected | At primary site | Params | Line | Quantum flag |", "|---|---|---|---|---|---|---|"]
    mark = {True: "yes", False: "NO", None: "n/a"}
    for r in rep["results"]:
        out.append(f"| {r['id']} | {r['family']} | {mark[r['detected']]} | {mark[r['at_usage_site']]} | "
                   f"{mark[r['params_ok']]} | {mark[r['line_ok']]} | {mark[r['quantum_ok']]} |")
    if rep["out_of_scope_occurrences"] or rep["unlocated_components"]:
        out += ["", f"_Ignored: {rep['out_of_scope_occurrences']} occurrences outside the corpus, "
                    f"{rep['unlocated_components']} components with no location evidence._"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cbom", help="scanner output, CycloneDX 1.6 JSON")
    ap.add_argument("--name", default=None, help="scanner name for the report title")
    ap.add_argument("--out", default=None, help="output path prefix (default: reports/<cbom stem>)")
    ap.add_argument("--tolerance", type=int, default=1, help="line-number tolerance (default 1)")
    ap.add_argument("--policy", default="nist", help="deadline policy in policies/ (nist, eo14412-hva, cnsa2)")
    ap.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat(), help="date the deadlines are judged from")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--exclude-custom", action="store_true", help="score the shipped benchmark only (comparable across orgs)")
    g.add_argument("--only-custom", action="store_true", help="score your own BYOC cases only")
    ap.add_argument("--scope", help="declared-scope JSON: findings the scanner says it doesn't cover are listed, not scored")
    args = ap.parse_args()

    bom = load_json(args.cbom)
    name = args.name or Path(args.cbom).stem
    mode = "exclude" if args.exclude_custom else "only" if args.only_custom else "include"
    rep = score(bom, args.tolerance, args.policy, dt.date.fromisoformat(args.as_of), mode, load_scope(args.scope))

    out = Path(args.out) if args.out else ROOT / "reports" / Path(args.cbom).name.replace(".cdx.json", "").replace(".json", "")
    out.parent.mkdir(parents=True, exist_ok=True)
    rep["manifest"]["scanner"] = name
    Path(str(out) + ".json").write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
    Path(str(out) + ".md").write_text(to_markdown(name, rep), encoding="utf-8")

    print(f"{name}")
    print(f"{'bucket':<26}{'detected':>10}{'recall':>9}{'primary':>9}{'params':>9}{'lines':>8}{'FP':>5}{'prec':>8}")
    for k, v in rep["summary"].items():
        if k == "negatives":
            print(f"{'negatives':<26}{'':>10}{'':>9}{'':>9}{'':>9}{'':>8}{v['false_positives']:>5}")
            continue
        if k == "pqc_overclaims":
            print(f"{'PQC overclaim':<26}{'':>10}{'':>9}{'':>9}{'':>9}{'':>8}{v['count']:>5}")
            continue
        if k == "pqc_standard_names":
            continue
        print(f"{k:<26}{v['detected']:>4}/{v['expected']:<5}{fmt(v['recall']):>9}{fmt(v['usage_site_recall']):>9}"
              f"{fmt(v['params_accuracy']):>9}{fmt(v['line_accuracy']):>8}{v['false_positives']:>5}{fmt(v['precision']):>8}")
    ac = rep["actionability"]
    print(f"\nActionability: ticket-ready {ac['ticket_ready']}/{ac['detected']} detected ({fmt(ac['ticket_ready_pct'])}), "
          f"actionable recall {fmt(ac['actionable_recall'])}, field completeness {fmt(ac['completeness_pct'])}")
    d = rep["deadlines"]
    print(f"\nDeadlines ({d['policy']}, as of {d['as_of']}): weighted recall {fmt(d['weighted_recall'])}, "
          f"primary-site {fmt(d['weighted_primary_site_recall'])}; missed findings due by 2030: {len(d['missed_due_by_2030'])}")
    for key, b in d["buckets"].items():
        print(f"  {b['label']:<55} {b['detected']:>3}/{b['expected']:<3} {fmt(b['recall']):>7}")
    print(f"\nScorecard: {Path(str(out) + '.md').relative_to(ROOT) if str(out).startswith(str(ROOT)) else str(out) + '.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
