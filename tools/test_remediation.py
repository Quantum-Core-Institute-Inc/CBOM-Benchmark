#!/usr/bin/env python3
"""Fix and rescan: the migrated files run, the after answer key resolves, a perfect scanner is
verified on every migration, and the ways of failing are each caught.

Run: python tools/test_remediation.py
"""
import copy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import remediate as rm  # noqa: E402
from cbomlib import load_json, make_component, same_file  # noqa: E402
from score import load_truth, score  # noqa: E402

ROOT = rm.ROOT
REF = load_json(ROOT / "expected" / "expected.cdx.json")


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return bool(cond)


def runs(path: Path, work: Path) -> tuple[bool, str]:
    """Execute one migrated file the way verify_corpus.py runs its original."""
    from verify_corpus import pq_java
    sfx = path.suffix
    try:
        if sfx == ".py":
            r = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=120)
        elif sfx == ".js":
            r = subprocess.run(["node", str(path)], capture_output=True, text=True, timeout=120)
        elif sfx == ".go":
            d = work / "gomod" / path.parent.name
            d.mkdir(parents=True)
            shutil.copy2(path, d / "main.go")
            (d / "go.mod").write_text("module example.com/mig\n\ngo 1.24\n")
            r = subprocess.run(["go", "run", "."], cwd=d, capture_output=True, text=True, timeout=300)
        elif sfx == ".c":
            exe = work / (path.stem + ".bin")
            r = subprocess.run(["cc", "-Wall", "-Werror", str(path), "-o", str(exe), "-lcrypto"], capture_output=True, text=True)
            if r.returncode == 0:
                r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=60)
        elif sfx == ".java":
            out = work / ("j_" + path.stem)
            r = subprocess.run(["javac", "-d", str(out), str(path)], capture_output=True, text=True, timeout=300)
            java = (pq_java() if "ML-DSA" in path.read_text() or "ML-KEM" in path.read_text() else None) or "java"
            if r.returncode == 0:
                r = subprocess.run([java, "-cp", str(out), path.stem], capture_output=True, text=True, timeout=120)
        else:
            return True, "config, not executed"
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, repr(e)
    text = (r.stdout if r.returncode == 0 else r.stderr or r.stdout).strip().splitlines()
    return r.returncode == 0, (text[-1][:60] if text else "")


def perfect_after(gt_after: dict) -> dict:
    """The reference CBOM with every migrated file re-described from the after answer key."""
    files = {m["file"] for m in rm.migrations()}
    bom = copy.deepcopy(REF)
    keep = []
    for c in bom["components"]:
        occ = (c.get("evidence") or {}).get("occurrences")
        if occ:
            occ[:] = [o for o in occ if not any(same_file(o.get("location", ""), f) for f in files)]
            if not occ:
                continue
        keep.append(c)
    bom["components"] = keep
    for f in gt_after["findings"]:
        if f["file"] in files:
            bom["components"].append(make_component(f"after-{f['id']}", f["family"], f["params"],
                                                    [{"location": f["file"], "line": (f["lines"] or [None])[0]}]))
    return bom


def main() -> int:
    ok = True
    work = Path(tempfile.mkdtemp(prefix="remed-test-"))
    for m in rm.migrations():
        good, detail = runs(rm.AFTER / m["file"], work)
        ok &= check(f"{m['id']} migrated file runs ({detail})", good)

    gt = load_truth(include_custom=False)[0]
    gt_after = rm.after_truth(gt)
    ok &= check("the after answer key resolves every anchor in the migrated files",
                all(f.get("lines") is not None for f in gt_after["findings"]))
    corpus = rm.build_after(work / "after")

    before = score(REF, custom="exclude")
    perfect = perfect_after(gt_after)
    after = score(perfect, custom="exclude", truth=copy.deepcopy(gt_after), corpus=corpus)
    ev = rm.evaluate(before, after)
    ok &= check(f"a perfect scanner: every migration eligible and verified ({ev['verified']}/{ev['total']})",
                ev["eligible"] == ev["total"] and ev["verified"] == ev["total"])
    ok &= check("a perfect scanner: nothing changes outside the migrated files",
                not ev["regressions_outside"]["lost"] and not ev["regressions_outside"]["gained"]
                and ev["regressions_outside"]["false_positives_before"] == ev["regressions_outside"]["false_positives_after"])

    # A scanner that keeps reporting what was removed (cached results, or it never re-read the file).
    stale = copy.deepcopy(perfect)
    stale["components"].append(make_component("stale-3des", "3DES", {"mode": "CBC"},
                                               [{"location": "corpus/tier1/c/t1_triple_des.c", "line": 12}]))
    stale["components"].append(make_component("stale-ecb", "AES", {"key_size": 128, "mode": "ECB"},
                                               [{"location": "corpus/tier1/python/t1_aes_ecb.py", "line": 7}]))
    ev2 = rm.evaluate(before, score(stale, custom="exclude", truth=copy.deepcopy(gt_after), corpus=corpus))
    v = {m["id"]: m for m in ev2["migrations"]}
    ok &= check("old algorithm still reported -> not verified (different family: 3DES left in the C file)",
                v["MIG-C-01"]["verdict"] == "not verified" and v["MIG-C-01"]["retired_still_reported"] == ["T1-C-07"])
    ok &= check("old parameters still reported -> not verified (same family: AES-128-ECB next to the new AES-GCM)",
                v["MIG-PY-02"]["verdict"] == "not verified")

    # A scanner that misses the new algorithm, or gets its parameters wrong.
    miss = copy.deepcopy(perfect)
    miss["components"] = [c for c in miss["components"] if c.get("bom-ref") != "after-MIG-PY-01-A1"]
    for c in miss["components"]:
        if c.get("bom-ref") == "after-MIG-GO-01-A1":
            c["cryptoProperties"]["algorithmProperties"]["parameterSetIdentifier"] = "128"
            c["name"] = "AES-128-GCM"
    ev3 = rm.evaluate(before, score(miss, custom="exclude", truth=copy.deepcopy(gt_after), corpus=corpus))
    v = {m["id"]: m for m in ev3["migrations"]}
    ok &= check("new algorithm not reported -> not verified", v["MIG-PY-01"]["verdict"] == "not verified")
    ok &= check("new algorithm with the wrong key size -> not verified", v["MIG-GO-01"]["verdict"] == "not verified")

    # A scanner that never found the old algorithm can't show it going away: not eligible, not a failure.
    blind = copy.deepcopy(REF)
    blind["components"] = [c for c in blind["components"]
                           if not any(same_file(o.get("location", ""), "corpus/tier1/javascript/t1_triple_des.js")
                                      for o in (c.get("evidence") or {}).get("occurrences") or [])]
    ev4 = rm.evaluate(score(blind, custom="exclude"), after)
    v = {m["id"]: m for m in ev4["migrations"]}
    ok &= check("old finding missed before the fix -> not eligible, and not counted against the rate",
                v["MIG-JS-01"]["verdict"] == "not eligible" and ev4["eligible"] == ev4["total"] - 1
                and ev4["verified"] == ev4["eligible"])

    shutil.rmtree(work, ignore_errors=True)
    print("\nAll remediation checks pass." if ok else "\nRemediation checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
