"""Fix and rescan: does the scanner see a migration happen?

remediation/migrations.json lists reference migrations (RSA-2048 signing to ML-DSA-65, 3DES to
AES-256-GCM, TLS 1.0 to 1.3 with a hybrid group, ...). Each replaces one corpus file with
remediation/after/<same path>. The scanner rescans the migrated corpus, and each migration is
"verified remediation" when:

  * eligible: the scanner found everything the migration retires, before (otherwise it can't show
    the old finding going away, and the migration is reported as not eligible, not as a failure)
  * retired:  nothing it retires is still reported in that file (for a same-family migration such
    as AES-ECB to AES-GCM: no report in the file still carries the old parameters)
  * added:    every algorithm the new code uses is reported, with the right parameters
  * stable:   every other finding in that file is detected after exactly when it was before

Separately, any change outside the migrated files (a finding detected before and not after, or
new false positives) is a regression, which a scanner that's deterministic shouldn't have.
"""
from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "remediation" / "migrations.json"
AFTER = ROOT / "remediation" / "after"


def migrations() -> list[dict]:
    return json.loads(SPEC.read_text())["migrations"]


def build_after(dst: Path, migs: list[dict] | None = None, after_dir: Path = AFTER) -> Path:
    """Copy corpus/ to dst/corpus with every migration applied. -> dst/corpus

    The same machinery serves tools/drift.py, whose changes can also delete a file ("delete") or
    add one that the shipped corpus does not have."""
    out = Path(dst) / "corpus"
    shutil.copytree(ROOT / "corpus", out, symlinks=True)
    for m in migrations() if migs is None else migs:
        target = Path(dst) / m["file"]
        if m.get("delete"):
            target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(after_dir / m["file"], target)
    return out


def _resolve(text_lines: list[str], anchors: list[str], what: str) -> list[int]:
    out = []
    for a in anchors:
        hits = [i + 1 for i, ln in enumerate(text_lines) if a in ln]
        if len(hits) != 1:
            raise ValueError(f"{what}: anchor {a!r} found {len(hits)} times in the migrated file")
        out.append(hits[0])
    return out


def after_truth(gt: dict, migs: list[dict] | None = None, after_dir: Path = AFTER) -> dict:
    """The answer key for the migrated corpus, from the (resolved) shipped one."""
    gt = copy.deepcopy(gt)
    migs = migrations() if migs is None else migs
    retired = {i for m in migs for i in m["retires"]}
    by_file = {m["file"]: m for m in migs}
    keep = []
    for f in gt["findings"]:
        if f["id"] in retired:
            continue
        m = by_file.get(f["file"])
        if m:
            if m.get("delete"):
                raise ValueError(f"{m['id']} deletes {m['file']} but does not retire {f['id']}")
            lines = (after_dir / f["file"]).read_text().splitlines()
            anchors = m.get("reanchor", {}).get(f["id"], f.get("anchors", []))
            f = {**f, "anchors": anchors, "lines": _resolve(lines, anchors, f["id"]) if anchors else []}
        keep.append(f)
    for m in migs:
        if not m["adds"]:
            continue
        lines = (after_dir / m["file"]).read_text().splitlines()
        # tier and language come from a finding the change retires, else from another in the same
        # file, else from the change itself (a file the shipped corpus does not have)
        model = next((f for f in gt["findings"] if f["id"] in m["retires"]), None) \
            or next((f for f in gt["findings"] if f["file"] == m["file"]), None) or {"tier": m["tier"], "lang": m["lang"]}
        for k, add in enumerate(m["adds"], 1):
            fid = f"{m['id']}-A{k}"
            keep.append({"id": fid, "tier": model["tier"], "lang": model["lang"], "file": m["file"],
                         "family": add["family"], "params": add["params"], "anchors": add["anchors"],
                         "lines": _resolve(lines, add["anchors"], fid), "remediation": m["id"]})
    gt["findings"] = keep
    return gt


def _matches(params: dict, want: dict) -> bool:
    return bool(want) and all(params.get(k) == v for k, v in want.items())


def evaluate(before: dict, after: dict, migs: list[dict] | None = None) -> dict:
    """before: the scorecard on the shipped corpus; after: on the migrated one (unscoped, same policy)."""
    b = {r["id"]: r for r in before["results"]}
    a = {r["id"]: r for r in after["results"]}
    migs = migrations() if migs is None else migs
    files = {m["file"] for m in migs}
    out = []
    for m in migs:
        ret = [b[i] for i in m["retires"] if i in b]
        eligible = len(ret) == len(m["retires"]) and all(r["detected"] for r in ret)
        adds = [a.get(f"{m['id']}-A{k}") for k in range(1, len(m["adds"]) + 1)]
        added = all(x and x["detected"] and x["params_ok"] for x in adds)
        fp_here = [x for x in after["false_positives"] if x["file"] == m["file"]]
        lingering = []
        for r in ret:
            if any(x["family"] == r["family"] for x in fp_here):
                lingering.append(r["id"])
                continue
            # same family still in the file (AES-ECB -> AES-GCM): the old parameters must be gone
            same = [x for x in a.values() if x["file"] == m["file"] and x["family"] == r["family"]]
            if any(_matches(p, r["expected_params"]) for x in same for p in x.get("reported_params") or []):
                lingering.append(r["id"])
        kept = [i for i, r in b.items() if r["file"] == m["file"] and i not in m["retires"]]
        unstable = [i for i in kept if i in a and a[i]["detected"] != b[i]["detected"]]
        verdict = ("not eligible" if not eligible else
                   "verified" if not lingering and added and not unstable else "not verified")
        out.append({"id": m["id"], "title": m["title"], "file": m["file"], "eligible": eligible,
                    "retired_still_reported": lingering, "added_found": [bool(x and x["detected"]) for x in adds],
                    "added_params_ok": [bool(x and x["params_ok"]) for x in adds],
                    "unstable": unstable, "verdict": verdict})
    outside_lost = sorted(i for i, r in b.items() if r["file"] not in files and i in a and r["detected"] and not a[i]["detected"])
    outside_gained = sorted(i for i, r in b.items() if r["file"] not in files and i in a and not r["detected"] and a[i]["detected"])
    fp_before = sum(1 for x in before["false_positives"] if x["file"] not in files)
    fp_after = sum(1 for x in after["false_positives"] if x["file"] not in files)
    elig = [x for x in out if x["eligible"]]
    ver = [x for x in elig if x["verdict"] == "verified"]
    return {"migrations": out, "total": len(out), "eligible": len(elig), "verified": len(ver),
            "verified_pct": round(100 * len(ver) / len(elig), 1) if elig else None,
            "regressions_outside": {"lost": outside_lost, "gained": outside_gained,
                                    "false_positives_before": fp_before, "false_positives_after": fp_after}}


def markdown(ev: dict, name: str) -> str:
    out = [f"# Fix and rescan: {name}", "",
           f"**Verified remediation: {ev['verified']}/{ev['eligible']} eligible migrations"
           + (f" ({ev['verified_pct']}%)" if ev["verified_pct"] is not None else "") + f"**, of {ev['total']}. "
           "A migration is eligible when the scanner found everything it retires before the fix.", "",
           "| Migration | Verdict | Retired but still reported | New algorithm found / params right | Other findings changed |",
           "|---|---|---|---|---|"]
    for m in ev["migrations"]:
        found = ", ".join(f"{'yes' if f else 'no'}/{'yes' if p else 'no'}" for f, p in zip(m["added_found"], m["added_params_ok"]))
        out.append(f"| {m['title']} | {m['verdict']} | {', '.join(m['retired_still_reported']) or 'none'} | {found} | "
                   f"{', '.join(m['unstable']) or 'none'} |")
    r = ev["regressions_outside"]
    out += ["", f"Outside the migrated files: {len(r['lost'])} finding(s) lost, {len(r['gained'])} gained, false positives "
            f"{r['false_positives_before']} -> {r['false_positives_after']}. Any change here is the scanner being "
            "non-deterministic or reacting to files it shouldn't.", ""]
    return "\n".join(out)
