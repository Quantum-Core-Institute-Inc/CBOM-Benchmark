"""Priority agreement: does the scanner's own urgency order agree with the policy's deadlines?

A team with three hundred findings fixes them in the order its scanner suggests. The policy says
when each algorithm stops being acceptable (METHODOLOGY.md 4, deadlines). This compares the two for
the findings the scanner detected. Reported per scanner; not part of any score or gate.

The scanner's urgency for a finding is read from its (adapted) CBOM, from the first of these that
is present:

  1. a CycloneDX vulnerability that affects the component: its highest rating, by severity word or
     numeric score;
  2. a component property whose name, after any `vendor:` prefix, is one of PROPERTY_NAMES.

One source is used per scanner: the property most components carry. Scales are never mixed.
A severity word maps to critical 4, high 3, medium 2, low 1, info or none 0. A number is taken as
written, higher meaning more urgent. `P1` to `P5` is read the other way round, as that convention
intends. The property read is named in the result, so that an assumption about direction can be
checked against the scanner's documentation.

Agreement is over pairs of detected findings whose deadlines differ. A pair agrees when the
scanner gives the finding that is due sooner the higher urgency, disagrees when it gives it the
lower, and counts half when it gives both the same. 50% is what any order unrelated to the
deadlines scores, including giving everything the same urgency; 100% is the policy's own order.

Only findings the policy gives a date are compared. The policy's undated bucket holds approved
algorithms together with ones it marks for review or leaves out of scope (TLS 1.0 under the NIST
policy, for one), so it says nothing about how urgent its members are, and a scanner is not
marked down for where it puts them. They are shown in the table and left out of the pairs.
"""
from __future__ import annotations

import re

from cbomlib import iter_crypto_findings_ctx, same_file

PROPERTY_NAMES = ("priority_score", "priority", "risk_score", "severity", "security-severity", "risk", "risk_level",
                  "urgency", "criticality", "level")
WORDS = {"critical": 4, "immediate": 4, "urgent": 4, "error": 3, "high": 3, "medium": 2, "moderate": 2, "warning": 2,
         "low": 1, "note": 1, "minor": 1, "info": 0, "informational": 0, "none": 0}
_PN = re.compile(r"^p([1-5])$", re.I)


def _value(v) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().lower()
    if not s:
        return None
    if s in WORDS:
        return float(WORDS[s])
    m = _PN.match(s)
    if m:
        return float(5 - int(m.group(1)))
    try:
        return float(s)
    except ValueError:
        return None


def _short(name: str) -> str:
    return str(name or "").rsplit(":", 1)[-1].strip().lower()


def _vuln_urgency(bom: dict) -> dict[str, float]:
    """bom-ref -> highest rating of any vulnerability that affects it."""
    out: dict[str, float] = {}
    for v in bom.get("vulnerabilities") or []:
        vals = [x for r in v.get("ratings") or [] for x in (_value(r.get("severity")), _value(r.get("score"))) if x is not None]
        sev = [x for r in v.get("ratings") or [] if (x := _value(r.get("severity"))) is not None]
        best = max(sev) if sev else max(vals) if vals else None
        if best is None:
            continue
        for a in v.get("affects") or []:
            ref = a.get("ref")
            if ref:
                out[ref] = max(out.get(ref, best), best)
    return out


def source_of(bom: dict) -> tuple[str | None, dict]:
    """Which field carries this scanner's urgency, and the urgency of each component by id().

    -> (source name or None, {id(component): urgency})"""
    comps = []

    def walk(cs):
        for c in cs or []:
            comps.append(c)
            walk(c.get("components"))
    walk(bom.get("components"))
    crypto = [c for c in comps if c.get("type") == "cryptographic-asset"]
    vu = _vuln_urgency(bom)
    by_vuln = {id(c): vu[c["bom-ref"]] for c in crypto if c.get("bom-ref") in vu}
    if by_vuln:
        return "vulnerabilities[].ratings", by_vuln
    counts: dict[str, int] = {}
    for c in crypto:
        for name in {_short(p.get("name")) for p in c.get("properties") or [] if _value(p.get("value")) is not None}:
            if name in PROPERTY_NAMES:
                counts[name] = counts.get(name, 0) + 1
    if not counts:
        return None, {}
    # the property most components carry; ties go to the order of PROPERTY_NAMES
    chosen = max(counts, key=lambda n: (counts[n], -PROPERTY_NAMES.index(n)))
    full = None
    out = {}
    for c in crypto:
        vals = []
        for p in c.get("properties") or []:
            if _short(p.get("name")) == chosen and (v := _value(p.get("value"))) is not None:
                vals.append(v)
                full = full or p.get("name")
        if vals:
            out[id(c)] = max(vals)
    return f"property {full}", out


def evaluate(bom: dict, rep: dict) -> dict:
    """bom: the adapted CBOM; rep: the scorecard scored from it (its results carry due_bucket)."""
    weights = {k: v["weight"] for k, v in rep["deadlines"]["buckets"].items() if k != "none"}
    source, urg = source_of(bom)
    detected = [r for r in rep["results"] if r["detected"] and r.get("tier") != "custom"]
    base = {"source": source, "detected": len(detected), "with_urgency": 0, "coverage_pct": 0.0, "levels": 0,
            "pairs": 0, "agree": 0, "tied": 0, "disagree": 0, "agreement_pct": None, "by_deadline": [], "worst": []}
    if source is None:
        return {**base, "verdict": "no priority given",
                "note": "no vulnerability rating and no priority, severity or risk property on the scanner's components"}
    # every (family, file) the CBOM reports, with the urgency of the asset it came from
    seen: list[tuple[str, str, float]] = []
    for family, _params, occ, _level, ctx in iter_crypto_findings_ctx(bom):
        u = urg.get(id(ctx["asset"]))
        if u is None and ctx.get("via") is not None:
            u = urg.get(id(ctx["via"]))
        if u is None:
            continue
        seen += [(family, loc, u) for loc, _line in occ]
    rows = []
    for r in detected:
        us = [u for fam, loc, u in seen if fam == r["family"] and any(same_file(loc, f) for f in r["reported_files"])]
        if us:
            rows.append({"id": r["id"], "family": r["family"], "file": r["file"], "bucket": r["due_bucket"],
                         "weight": weights.get(r["due_bucket"]), "urgency": max(us)})
    out = {**base, "with_urgency": len(rows), "coverage_pct": round(100 * len(rows) / len(detected), 1) if detected else 0.0,
           "levels": len({x["urgency"] for x in rows})}
    for b in sorted({x["bucket"] for x in rows}, key=lambda b: -weights.get(b, -1)):
        us = [x["urgency"] for x in rows if x["bucket"] == b]
        out["by_deadline"].append({"bucket": b, "label": (rep["deadlines"]["buckets"].get(b) or {}).get("label", "No deadline"),
                                   "compared": b in weights, "findings": len(us), "mean_urgency": round(sum(us) / len(us), 2),
                                   "min_urgency": min(us), "max_urgency": max(us)})
    agree = tied = disagree = 0
    worst = []
    dated = [x for x in rows if x["weight"] is not None]
    for i, a in enumerate(dated):
        for b in dated[i + 1:]:
            if a["weight"] == b["weight"]:
                continue
            sooner, later = (a, b) if a["weight"] > b["weight"] else (b, a)
            if sooner["urgency"] > later["urgency"]:
                agree += 1
            elif sooner["urgency"] == later["urgency"]:
                tied += 1
            else:
                disagree += 1
                worst.append((sooner["weight"] - later["weight"], later["urgency"] - sooner["urgency"], sooner, later))
    pairs = agree + tied + disagree
    out.update(pairs=pairs, agree=agree, tied=tied, disagree=disagree,
               agreement_pct=round(100 * (agree + 0.5 * tied) / pairs, 1) if pairs else None)
    worst.sort(key=lambda w: (-w[0], -w[1], w[2]["id"], w[3]["id"]))
    out["worst"] = [{"due_sooner": {k: s[k] for k in ("id", "family", "bucket", "urgency")},
                     "ranked_above_it": {k: lt[k] for k in ("id", "family", "bucket", "urgency")}} for _, _, s, lt in worst[:5]]
    if not pairs:
        out["verdict"] = "not measurable"
        out["note"] = "no two detected findings with an urgency have different deadlines"
    elif out["levels"] < 2:
        out["verdict"] = "one level only"
        out["note"] = "every finding carries the same urgency, so the scanner gives no order"
    else:
        out["verdict"] = "measured"
    return out


def cell(ev: dict | None) -> str:
    if not ev:
        return "not measured"
    if ev["verdict"] == "measured":
        return f"{ev['agreement_pct']}% ({ev['coverage_pct']}% of detections carry a priority)"
    return ev["verdict"]


def markdown(ev: dict, name: str) -> str:
    out = [f"# Priority agreement: {name}", "", "Reported, not scored. See METHODOLOGY.md 4f.", "",
           f"**Agreement with the policy's deadlines: {cell(ev)}.** 50% is what an order unrelated to the deadlines scores."]
    if ev.get("note"):
        out += ["", ev["note"].capitalize() + "."]
    if ev["source"]:
        out += ["", f"Urgency read from: {ev['source']} (higher taken as more urgent). {ev['with_urgency']} of {ev['detected']} "
                f"detected findings carry one, on {ev['levels']} distinct level(s). Pairs with different deadlines: {ev['pairs']} "
                f"({ev['agree']} agree, {ev['tied']} tied, {ev['disagree']} disagree)."]
    if ev["by_deadline"]:
        out += ["", "| Deadline | Findings | Mean urgency | Lowest | Highest |", "|---|---|---|---|---|"]
        out += [f"| {b['label']}{'' if b['compared'] else ' (not compared)'} | {b['findings']} | {b['mean_urgency']} | {b['min_urgency']:g} | {b['max_urgency']:g} |" for b in ev["by_deadline"]]
    if ev["worst"]:
        out += ["", "Largest disagreements (the first is due sooner, the scanner ranks the second above it):", ""]
        out += [f"- {w['due_sooner']['id']} {w['due_sooner']['family']} (due {w['due_sooner']['bucket']}, urgency {w['due_sooner']['urgency']:g}) "
                f"below {w['ranked_above_it']['id']} {w['ranked_above_it']['family']} (due {w['ranked_above_it']['bucket']}, "
                f"urgency {w['ranked_above_it']['urgency']:g})" for w in ev["worst"]]
    return "\n".join(out) + "\n"
