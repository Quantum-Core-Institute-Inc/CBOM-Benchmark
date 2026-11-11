#!/usr/bin/env python3
"""Write corpus/mixed/ and its findings in expected/ground_truth.json.

Mixed files are realistic-size modules (220-520 lines) with three to five crypto sites each, usually
one family used twice with different parameters, among ordinary code and log text that names
algorithms the file doesn't use. See tools/mixed.py for why.

The files come from the same generator as the private holdout's mixed tier, with a fixed public
seed, so they are reproducible: rerunning this rewrites identical files. Anchors are the exact text
of each site's lines, checked to be unique in the file.

  python tools/build_mixed.py            # (re)write corpus/mixed and the ground truth entries
  python tools/build_mixed.py --check    # fail if corpus/mixed doesn't match the generator
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import holdout as ho  # noqa: E402
from holdout_common import WORDS, Names  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "mixed"
GT = ROOT / "expected" / "ground_truth.json"
SEED = 20261110
PLAN = [("python", 3), ("java", 3), ("go", 3), ("javascript", 2), ("typescript", 1), ("c", 3)]
EXT = {"python": ".py", "javascript": ".js", "typescript": ".ts", "c": ".c"}
KINDS = {"python": ["service", "jobs", "client", "handlers"], "go": ["sync", "worker", "gateway", "agent"],
         "javascript": ["api", "routes", "client", "session"], "typescript": ["service", "handlers"],
         "c": ["agent", "tool", "daemon", "link"]}
ABBR = {"python": "PY", "java": "JV", "go": "GO", "javascript": "JS", "typescript": "TS", "c": "C"}


def anchors_ok(text: str, sites) -> list[list[str]] | None:
    """Exact line text per site, each found once in the file; None if any isn't unique."""
    lines = text.splitlines()
    out = []
    for _, _, _, nums in sites:
        anchors = []
        for n in nums:
            a = lines[n - 1].strip()
            if sum(1 for ln in lines if a in ln) != 1:
                return None
            anchors.append(a)
        out.append(anchors)
    return out


def build(dest: Path) -> tuple[list[dict], list[dict]]:
    rng = random.Random(SEED)
    findings, also_ok, used_names = [], [], set()
    for lang, count in PLAN:
        for i in range(count):
            for _attempt in range(20):
                names = Names(rng)
                seq = iter(range(1, 100))
                text, sites, cls = ho.build_mixed_file(lang, rng, names, lambda: f"S{next(seq)}")
                anchors = anchors_ok(text, sites)
                if anchors:
                    break
            else:
                raise SystemExit(f"{lang} #{i}: no file with unique anchors in 20 tries")
            if lang == "java":
                rel = f"corpus/mixed/java/{cls}.java"
            else:
                for _ in range(50):
                    stem = f"{rng.choice(WORDS)}_{rng.choice(KINDS[lang])}"
                    if stem not in used_names:
                        break
                used_names.add(stem)
                rel = f"corpus/mixed/go/{stem}/main.go" if lang == "go" else f"corpus/mixed/{lang}/{stem}{EXT[lang]}"
            p = dest.parent.parent / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            extra = set()
            for n, ((_, sp, style, _), anc) in enumerate(zip(sites, anchors), 1):
                findings.append({"id": f"MX-{ABBR[lang]}-{i + 1}{chr(96 + n)}", "tier": "mixed", "lang": lang, "file": rel,
                                 "family": sp["family"], "params": sp["params"], "anchors": anc, "site": True,
                                 "note": f"{sp['api']}, {style}"})
                extra |= {x for x in sp["also_ok"] if x != sp["family"]}
            fams = {sp["family"] for _, sp, _, _ in sites}
            extra -= fams
            if extra:
                also_ok.append({"file": rel, "families": sorted(extra)})
    if (dest / "go").exists():
        (dest / "go" / "go.mod").write_text("module example.com/mixed\n\ngo 1.24\n")
    return findings, also_ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        import filecmp
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "corpus" / "mixed"
            findings, _ = build(dest)
            cmp = filecmp.dircmp(dest, OUT)
            diff = []

            def walk(c, pre=""):
                diff.extend(pre + x for x in c.left_only + c.right_only + c.diff_files)
                for k, sub in c.subdirs.items():
                    walk(sub, f"{pre}{k}/")
            walk(cmp)
            gt = json.loads(GT.read_text())
            shipped = [f for f in gt["findings"] if f["tier"] == "mixed"]
            if diff or [f["id"] for f in shipped] != [f["id"] for f in findings]:
                print("corpus/mixed doesn't match the generator:", diff[:10] or "finding ids differ")
                return 1
        print(f"corpus/mixed matches the generator ({len(findings)} sites)")
        return 0
    if OUT.exists():
        shutil.rmtree(OUT)
    findings, also_ok = build(OUT)
    gt = json.loads(GT.read_text())
    gt["findings"] = [f for f in gt["findings"] if f["tier"] != "mixed"] + findings
    gt["also_ok"] = [e for e in gt.get("also_ok", []) if not e["file"].startswith("corpus/mixed/")] + also_ok
    GT.write_text(json.dumps(gt, indent=2) + "\n")
    files = sorted({f["file"] for f in findings})
    print(f"Wrote {len(files)} files and {len(findings)} site findings to corpus/mixed/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
