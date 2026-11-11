#!/usr/bin/env python3
"""Write corpus/calibration/: extra published Tier 1-2 cases that make the overfit gap measurable.

The overfit gap compares a scanner's published recall with its holdout recall cell by cell, a cell
being (tier, language, family). Most published Tier 1-2 cells hold one hand-written case, so the
published side of every comparison is 0 or 1 and the gap's interval is wide. This tops each cell up
to CELL_TARGET cases with generated ones, written by the same matched generator the holdout uses
(same API spellings, values and kinds of indirection as the hand-written case) from a fixed public
seed.

Calibration cases are scored, but kept apart: they don't enter recall, precision or any headline
number (the hand-written corpus stays the benchmark), and false positives in corpus/calibration/
aren't counted. score.py returns them as `calibration_results`, and the overfit gap uses them
together with the hand-written cases.

  python tools/build_calibration.py            # (re)write corpus/calibration and its ground truth entries
  python tools/build_calibration.py --check    # fail if corpus/calibration doesn't match the generator
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import holdout as ho  # noqa: E402
from holdout_common import Names  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "calibration"
GT = ROOT / "expected" / "ground_truth.json"
SEED = 20261111
CELL_TARGET = 4
ABBR = {"python": "PY", "java": "JV", "go": "GO", "javascript": "JS", "typescript": "TS", "c": "C"}


def hand_cells(gt: dict) -> Counter:
    return Counter((f["tier"], f["lang"], f["family"]) for f in gt["findings"]
                   if f["tier"] in (1, 2) and not f.get("calibration") and not f["family"].startswith(ho.UNCOVERED))


def one_case(lang: str, tier: int, family: str, rng: random.Random, names: Names, fid: str, k: int = 0):
    """One single-finding file in the style of the published Tier `tier` case. -> (text, lines, spec, style, cls) or None."""
    spec_lang = "javascript" if lang == "typescript" else lang
    if spec_lang in ("python", "java"):
        t1_fns, t2_fns, _ = ho.py_specs() if lang == "python" else ho.java_specs()
        fns = t2_fns if tier == 2 else t1_fns
    else:
        sets = ho._new_specs(spec_lang)
        fns = sets["t2" if tier == 2 else "t1"]
    for _ in range(40):
        sp = ho.draw(fns, family, rng, tier, tries=1000)
        if sp is None:
            return None
        if tier == 1:
            style, imports = "inline", "canonical"
            break
        if not sp["slot"]:
            continue
        if lang in ("python", "java"):
            if sp["carries_family"] or sp["family"] == "EC" or lang == "java":
                style = rng.choice([x for x in ho.STYLES[lang] if x != "alias"])
            else:
                style = "alias"
            imports = "alias" if style == "alias" else "canonical"
        else:
            imports = "canonical"
            builder_probe = ho._new_builder(lang, random.Random(0), Names(random.Random(0)), imports)
            style = rng.choice(builder_probe.styles_for(sp))
        break
    else:
        return None
    if lang in ("python", "java"):
        builder = ho.FileBuilder(lang, rng, names, imports)
    else:
        builder = ho._new_builder(lang, rng, names, imports)
    builder.add(sp, style, fid)
    for _ in range(rng.randint(1, 2)):
        builder.filler()
    cls = None
    if lang in ("python", "java"):
        cls = f"Cal{tier}{k:03d}{names.cap()}" if lang == "java" else None
        text, anchors = builder.render(cls)
    else:
        text, anchors = ho._lines_to_text(builder.render())
    return text, sorted(anchors[fid]), sp, style, cls


def build(root: Path, gt: dict):
    rng = random.Random(SEED)
    cells = hand_cells(gt)
    findings, also_ok, skipped = [], [], []
    counters = Counter()
    for (tier, lang, family), n in sorted(cells.items(), key=str):
        for _ in range(max(0, CELL_TARGET - n)):
            counters[(tier, lang)] += 1
            k = counters[(tier, lang)]
            fid = f"CAL-T{tier}-{ABBR[lang]}-{k:03d}"
            made = None
            for _attempt in range(10):
                made = one_case(lang, tier, family, rng, Names(rng), fid, k)
                if made is None:
                    break
                text, lines, sp, style, cls = made
                anchors = [text.splitlines()[n_ - 1].strip() for n_ in lines]
                if all(sum(1 for ln in text.splitlines() if a in ln) == 1 for a in anchors) and sp["family"] == family:
                    break
                made = None
            if made is None:
                skipped.append((tier, lang, family))
                break
            stem = f"cal_{family.lower().replace('-', '').replace('/', '')}_{k:03d}"
            if lang == "java":
                rel = f"corpus/calibration/tier{tier}/java/{cls}.java"
            elif lang == "go":
                # not main.go: the corpus has enough of those, and basename de-duplication in some
                # scanners would let these cost the hand-written Go cases findings
                rel = f"corpus/calibration/tier{tier}/go/{stem}/{stem}.go"
            else:
                ext = {"python": ".py", "javascript": ".js", "typescript": ".ts", "c": ".c"}[lang]
                rel = f"corpus/calibration/tier{tier}/{lang}/{stem}{ext}"
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            if lang == "go":
                mod = root / f"corpus/calibration/tier{tier}/go/go.mod"
                if not mod.exists():
                    mod.write_text(f"module example.com/calibration{tier}\n\ngo 1.24\n")
            findings.append({"id": fid, "tier": tier, "lang": lang, "file": rel, "family": family, "params": sp["params"],
                             "anchors": anchors, "calibration": True, "note": f"generated: {sp['api']}, {style}"})
            extra = [x for x in sp["also_ok"] if x != family]
            if extra:
                also_ok.append({"file": rel, "families": extra})
    return findings, also_ok, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    gt = json.loads(GT.read_text())
    if a.check:
        import filecmp
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            findings, _, _ = build(Path(tmp), gt)
            diff = []

            def walk(c, pre=""):
                diff.extend(pre + x for x in c.left_only + c.right_only + c.diff_files)
                for k, sub in c.subdirs.items():
                    walk(sub, f"{pre}{k}/")
            walk(filecmp.dircmp(Path(tmp) / "corpus" / "calibration", OUT))
            shipped = [f["id"] for f in gt["findings"] if f.get("calibration")]
            if diff or shipped != [f["id"] for f in findings]:
                print("corpus/calibration doesn't match the generator:", diff[:10] or "finding ids differ")
                return 1
        print(f"corpus/calibration matches the generator ({len(findings)} cases)")
        return 0
    if OUT.exists():
        shutil.rmtree(OUT)
    findings, also_ok, skipped = build(ROOT, gt)
    gt["findings"] = [f for f in gt["findings"] if not f.get("calibration")] + findings
    gt["also_ok"] = [e for e in gt.get("also_ok", []) if not e["file"].startswith("corpus/calibration/")] + also_ok
    GT.write_text(json.dumps(gt, indent=2) + "\n")
    print(f"Wrote {len(findings)} calibration cases to corpus/calibration/")
    for s in skipped:
        print(f"  not generated (the matched generator has no spelling for it): Tier {s[0]} {s[1]} {s[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
