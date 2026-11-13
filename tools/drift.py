"""Change detection: when the code changes, does the difference between two scans show it?

A scanner is run every week, not once. drift/changes.json lists injected changes of three kinds:

  * add        an algorithm appears: in a new file, or in a file that already had other crypto
  * remove     an algorithm goes away: the call is removed, or the whole file is deleted
  * downgrade  an algorithm is replaced by something weaker (AES-256-GCM to 3DES, RSA-3072 to 1024)

The scanner scans the shipped corpus and then the changed one. Nothing is asked of it beyond two
scans: the benchmark takes the difference between its two reports itself. A change is **seen** when

  * add:        the new algorithm is reported afterwards, with the right parameters, and was not
                already (falsely) reported in that file before
  * remove:     what was removed was reported before and is not reported in that file afterwards
  * downgrade:  both: the old one is gone and the new, weaker one is reported with its parameters

and, in each case, every other finding in the changed file is detected afterwards exactly when it
was before. A removal or a downgrade is **eligible** only when the scanner found the original
beforehand; otherwise it cannot show it going away, and the change is reported as not eligible
instead of counted as missed.

Two more things are read off the same pair of scans:

  * Noise. Anything that differs outside the changed files. Nothing there changed, so a difference
    is the scanner inventing one.
  * Identity. An asset that did not change should keep the same identifier, or nobody can follow
    it from one report to the next. Read from the scanner's own output before any adapter:
    `bom-ref` for a CycloneDX component, `fingerprints` for a SARIF result.

Shares the corpus-rewriting and answer-key code with fix-and-rescan (tools/remediate.py).
"""
from __future__ import annotations

import json
from pathlib import Path

import remediate as rm

ROOT = rm.ROOT
SPEC = ROOT / "drift" / "changes.json"
AFTER = ROOT / "drift" / "after"
KINDS = ("add", "remove", "downgrade")


def changes() -> list[dict]:
    return json.loads(SPEC.read_text())["changes"]


def changed_files() -> set[str]:
    return {c["file"] for c in changes()}


def build_after(dst: Path) -> Path:
    """Copy corpus/ to dst/corpus with every change applied. -> dst/corpus"""
    return rm.build_after(dst, changes(), AFTER)


def after_truth(gt: dict) -> dict:
    """The answer key for the changed corpus."""
    return rm.after_truth(gt, changes(), AFTER)


def evaluate(before: dict, after: dict, after_bom: dict) -> dict:
    """before: the scorecard on the shipped corpus; after: on the changed one (unscoped, same policy);
    after_bom: the CBOM the after scorecard was scored from."""
    from cbomlib import same_file
    chs = changes()
    base = rm.evaluate(before, after, chs)
    by_id = {m["id"]: m for m in base["migrations"]}
    out = []
    for c in chs:
        m = by_id[c["id"]]
        # The scorer does not count a report in a file the corpus no longer has, so a report that
        # still points at a deleted file is looked for in the CBOM itself.
        if c.get("delete") and any(same_file((o or {}).get("location", ""), c["file"])
                                   for comp in after_bom.get("components") or []
                                   for o in (comp.get("evidence") or {}).get("occurrences") or []):
            m = {**m, "retired_still_reported": list(c["retires"]), "verdict": "not verified" if m["eligible"] else m["verdict"]}
        # An addition the scanner already (falsely) reported in that file is no change in its output.
        already = [a["family"] for a in c["adds"]
                   if c["kind"] == "add" and any(x["file"] == c["file"] and x["family"] == a["family"] for x in before["false_positives"])]
        seen = m["verdict"] == "verified" and not already
        out.append({"id": c["id"], "kind": c["kind"], "title": c["title"], "file": c["file"], "eligible": m["eligible"],
                    "removed_still_reported": m["retired_still_reported"], "added_found": m["added_found"],
                    "added_params_ok": m["added_params_ok"], "already_reported_before": already, "unstable": m["unstable"],
                    "verdict": "not eligible" if not m["eligible"] else "seen" if seen else "missed"})
    by_kind = {}
    for k in KINDS:
        rows = [x for x in out if x["kind"] == k]
        elig = [x for x in rows if x["eligible"]]
        by_kind[k] = {"total": len(rows), "eligible": len(elig), "seen": sum(x["verdict"] == "seen" for x in elig)}
    elig = [x for x in out if x["eligible"]]
    seen = sum(x["verdict"] == "seen" for x in elig)
    return {"changes": out, "total": len(out), "eligible": len(elig), "seen": seen,
            "seen_pct": round(100 * seen / len(elig), 1) if elig else None, "by_kind": by_kind,
            "noise_outside": base["regressions_outside"]}


# -------------------------------------------------------------------------------------- identity
def _norm(path: str) -> str:
    return (path or "").replace("\\", "/")


def _in_changed(location: str, changed: set[str]) -> bool:
    loc = _norm(location).split(":")[0]
    return any(loc == f or loc.endswith("/" + f) or f.endswith("/" + loc) or loc.endswith(f.split("corpus/", 1)[-1]) for f in changed)


def _cdx_assets(doc: dict, changed: set[str]) -> list[tuple[str, str | None]]:
    """(content, identifier) for every component that does not sit only in changed files."""
    out = []
    for c in doc.get("components") or []:
        if not isinstance(c, dict):
            continue
        body = {k: v for k, v in c.items() if k != "bom-ref"}
        occ = (c.get("evidence") or {}).get("occurrences")
        if isinstance(occ, list):
            kept = [o for o in occ if not _in_changed((o or {}).get("location", ""), changed)]
            if occ and not kept:
                continue  # an asset of the changed files: not one that should stay the same
            body = {**body, "evidence": {**c["evidence"], "occurrences": sorted(kept, key=lambda o: json.dumps(o, sort_keys=True))}}
        out.append((json.dumps(body, sort_keys=True, ensure_ascii=False), c.get("bom-ref")))
    return out


def _sarif_assets(doc: dict, changed: set[str]) -> list[tuple[str, str | None]]:
    out = []
    for run in doc.get("runs") or []:
        for r in (run.get("results") or []) if isinstance(run, dict) else []:
            uris = [(((loc.get("physicalLocation") or {}).get("artifactLocation") or {}).get("uri") or "") for loc in r.get("locations") or []]
            if uris and all(_in_changed(u, changed) for u in uris):
                continue
            ident = r.get("fingerprints") or r.get("partialFingerprints")
            body = {k: v for k, v in r.items() if k not in ("fingerprints", "partialFingerprints")}
            out.append((json.dumps(body, sort_keys=True, ensure_ascii=False), json.dumps(ident, sort_keys=True) if ident else None))
    return out


def identity(raw_before, raw_after, changed: set[str] | None = None) -> dict:
    """Do assets outside the changed files carry the same identifier in both scans?

    Assets are paired by content (everything but the identifier). An asset whose content is not
    unique in a report, or that has no counterpart with the same content in the other, is left out
    and counted: only a pair that is certainly the same asset says anything about identity."""
    changed = changed_files() if changed is None else changed
    if isinstance(raw_before, dict) and isinstance(raw_after, dict) and "runs" in raw_before and "runs" in raw_after:
        kind, a, b = "SARIF fingerprints", _sarif_assets(raw_before, changed), _sarif_assets(raw_after, changed)
    elif isinstance(raw_before, dict) and isinstance(raw_after, dict) and "components" in raw_before:
        kind, a, b = "CycloneDX bom-ref", _cdx_assets(raw_before, changed), _cdx_assets(raw_after, changed)
    else:
        return {"verdict": "not applicable", "identifier": None, "paired": 0, "same": 0, "same_pct": None,
                "note": "the output is neither CycloneDX components nor SARIF results"}

    def unique(rows):
        seen, dup = {}, set()
        for content, ident in rows:
            if content in seen:
                dup.add(content)
            seen[content] = ident
        return {c: i for c, i in seen.items() if c not in dup}, len(dup)

    ua, dup_a = unique(a)
    ub, dup_b = unique(b)
    pairs = [(ua[c], ub[c]) for c in ua if c in ub]
    with_id = [(x, y) for x, y in pairs if x is not None and y is not None]
    same = sum(x == y for x, y in with_id)
    out = {"identifier": kind, "assets_before": len(a), "assets_after": len(b), "paired": len(pairs),
           "with_identifier": len(with_id), "same": same, "unpaired_before": len(ua) - len(pairs),
           "unpaired_after": len(ub) - len(pairs), "content_not_unique": max(dup_a, dup_b),
           "same_pct": round(100 * same / len(with_id), 1) if with_id else None}
    if not pairs:
        out["verdict"] = "not measurable"
        out["note"] = "no unchanged asset could be paired between the two scans by content"
    elif not with_id:
        out["verdict"] = "no identifiers"
        out["note"] = "the output gives its entries no identifier, so nothing can be followed between scans"
    else:
        out["verdict"] = "stable" if same == len(with_id) else "not stable"
    return out


# ---------------------------------------------------------------------------------------- report
def seen_cell(ev: dict | None) -> str:
    if not ev:
        return "not measured"
    if not ev["eligible"]:
        return "none eligible"
    return f"{ev['seen']}/{ev['eligible']}" + (f" ({ev['seen_pct']}%)" if ev.get("seen_pct") is not None else "")


def identity_cell(ev: dict | None) -> str:
    i = (ev or {}).get("identity")
    if not i:
        return "not measured"
    if i["verdict"] in ("stable", "not stable"):
        return f"{i['same']}/{i['with_identifier']} unchanged assets keep their identifier"
    return i["verdict"]


def markdown(ev: dict, name: str) -> str:
    out = [f"# Change detection: {name}", "",
           f"**Changes seen: {seen_cell(ev)}** of {ev['total']} injected. A removal or downgrade is eligible when the "
           "scanner found the original before the change. See METHODOLOGY.md 4e.", "",
           "| Kind | Injected | Eligible | Seen |", "|---|---|---|---|"]
    for k in KINDS:
        r = ev["by_kind"][k]
        out.append(f"| {k} | {r['total']} | {r['eligible']} | {r['seen']} |")
    out += ["", "| Change | Verdict | Removed but still reported | New algorithm found / params right | Other findings changed |",
            "|---|---|---|---|---|"]
    for c in ev["changes"]:
        found = ", ".join(f"{'yes' if f else 'no'}/{'yes' if p else 'no'}" for f, p in zip(c["added_found"], c["added_params_ok"])) or "n/a"
        if c["already_reported_before"]:
            found += " (already reported before the change)"
        out.append(f"| {c['title']} | {c['verdict']} | {', '.join(c['removed_still_reported']) or 'none'} | {found} | "
                   f"{', '.join(c['unstable']) or 'none'} |")
    n = ev["noise_outside"]
    out += ["", f"Outside the changed files: {len(n['lost'])} finding(s) lost, {len(n['gained'])} gained, false positives "
            f"{n['false_positives_before']} -> {n['false_positives_after']}. Nothing there changed, so any difference is noise."]
    i = ev.get("identity")
    if i:
        out += ["", f"Identity ({i.get('identifier') or 'none'}): {identity_cell(ev)}."
                + (f" {i['note']}." if i.get("note") else "")
                + (f" Paired by content: {i['paired']} of {i['assets_before']} before and {i['assets_after']} after"
                   f" ({i['content_not_unique']} left out because their content is not unique)." if "paired" in i and i.get("assets_before") is not None else "")]
    return "\n".join(out) + "\n"
