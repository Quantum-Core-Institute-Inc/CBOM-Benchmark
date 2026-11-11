#!/usr/bin/env python3
"""bench.py end to end, with the grep baseline as the scanner: a bundle reproduces, a doctored one
doesn't, and a scanner that misbehaves isn't scored.

Run: python tools/test_bench.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
GREP = str(ROOT / "tools" / "baseline_grep.py")


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return bool(cond)


def bench(*args, env=None):
    return subprocess.run([PY, "tools/bench.py", *args], cwd=ROOT, capture_output=True, text=True,
                          env={**os.environ, **(env or {})})


def main() -> int:
    ok = True
    tmp = Path(tempfile.mkdtemp(prefix="bench-test-"))
    b = tmp / "grep"
    sys.path.insert(0, str(ROOT / "tools"))
    import release
    gfile = tmp / "gates.json"  # a gate file stamped for this release and no adapter
    gfile.write_text(json.dumps({"gates": {"recall": {"min": 99.0}, "precision": {"min": 10.0}, "cbom_schema_valid": {"min": 1},
                                           "overfit_gap_ci_low": {"max": 0}, "negative_fp_gap": {"max": 0.5}},
                                 "stamp": release.stamp("nist", ())}))
    TOOLS = ["--allow-path", str(ROOT / "tools")]  # grep is a testbench script: it lives in the hidden tree
    r = bench("run", "--name", "grep baseline", "--scanner-cmd", f"{PY} {GREP} {{corpus}} -o {{out}}/cbom.json",
              "--scanner-version", "baseline", "--bundle", str(b), *TOOLS,
              "--gates", str(gfile), "--without-holdout")
    ok &= check("without --allow-path the same command can't even read its script (the tree is hidden)",
                bench("run", "--name", "g", "--scanner-cmd", f"{PY} {GREP} {{corpus}} -o {{out}}/cbom.json",
                      "--scanner-version", "x", "--bundle", str(tmp / "noallow")).returncode == 2
                or not __import__("sandbox").probe().get("confine"))
    ok &= check("grep through bench.py is scored; its gates are evaluated and fail (exit 1)", r.returncode == 1)
    m = json.loads((b / "manifest.json").read_text())
    ref = json.loads((ROOT / "reports" / "baseline_grep.json").read_text())["summary"]["all/all"]
    ok &= check(f"same recall and precision as the release scorecard ({m['headline']['recall']}%, {m['headline']['precision']}%)",
                m["headline"]["recall"] == ref["recall"] and m["headline"]["precision"] == ref["precision"])
    ok &= check("manifest records methodology, stamp, file hashes, sandbox run and isolation",
                m["methodology"] and m["stamp"]["release"] and "tools/score.py" in m["files"]
                and m["run"]["isolation"]["environment"] == "scrubbed" and m["run"]["peak_rss_mb"] > 0)
    ok &= check("manifest carries no host paths", str(tmp) not in json.dumps(m) and "/home/" not in json.dumps(m["run"]))
    r = bench("verify", str(b))
    ok &= check("an untouched bundle verifies, gate verdict included",
                r.returncode == 0 and "the gate verdict (fail) re-derives" in r.stdout)
    gm = m["gates"]
    ok &= check("the bundle records the holdout gates as skipped with a reason, and the scanner's schema verdict",
                {x["gate"] for x in gm["skipped"]} >= {"overfit_gap_ci_low", "negative_fp_gap"} and "cbom_schema" in m["scanner"])

    # Reviewer reproductions (v2.1 review): things removed or changed, with checksums recomputed.
    def tampered(name, fn):
        d2 = tmp / name
        shutil.copytree(b, d2)
        fn(d2)
        (d2 / "SHA256SUMS").write_text(bm.sums(d2))
        return bench("verify", str(d2))
    sys.path.insert(0, str(ROOT / "tools"))
    import bench as bm

    def edit(rel, fn):
        def go(d2):
            doc = json.loads((d2 / rel).read_text())
            fn(doc)
            (d2 / rel).write_text(json.dumps(doc, indent=2) + "\n")
        return go
    r = tampered("no-raw", lambda d2: (d2 / "raw" / "cbom.json").unlink())
    ok &= check("raw CBOM removed -> does not verify", r.returncode == 1 and "missing: raw/cbom.json" in r.stdout)
    r = tampered("lib", edit("scorecard.json", lambda doc: doc["libraries"].__setitem__("recall", 99.0)))
    ok &= check("library result changed -> does not verify (libraries named)", r.returncode == 1 and "libraries" in r.stdout)
    r = tampered("link", edit("scorecard.json", lambda doc: doc["linkage"].__setitem__("routable", 26)))
    ok &= check("linkage result changed -> does not verify (linkage named)", r.returncode == 1 and "linkage" in r.stdout)
    r = tampered("gate", edit("manifest.json", lambda doc: doc["gates"].update(status="pass", fails=[])))
    ok &= check("gate verdict changed to pass -> does not verify", r.returncode == 1 and "[FAIL] the gate verdict" in r.stdout)
    r = tampered("gatefile", edit("gates.json", lambda doc: [rule.update(min=0) for rule in doc["gates"].values() if "min" in rule]))
    ok &= check("gates file loosened -> the recorded verdict no longer re-derives", r.returncode == 1)

    d = tmp / "doctored"
    shutil.copytree(b, d)
    sc = json.loads((d / "scorecard.json").read_text())
    sc["summary"]["all/all"]["recall"] = 99.9
    (d / "scorecard.json").write_text(json.dumps(sc, indent=2) + "\n")
    r = bench("verify", str(d))
    ok &= check("a changed number without new checksums -> checksum failure", r.returncode == 1 and "SHA256SUMS" in r.stdout)
    (d / "SHA256SUMS").write_text(bm.sums(d))
    r = bench("verify", str(d))
    ok &= check("a changed number with recomputed checksums -> fails to re-derive from the raw CBOM",
                r.returncode == 1 and "[FAIL] scorecard: every section re-derives" in r.stdout)

    probe = tmp / "probe.py"
    probe.write_text(
        "import json, os, sys\n"
        "corpus, out = sys.argv[1], sys.argv[2]\n"
        "try:\n"
        "    open(os.path.join(corpus, 'tier1/python/t1_aes_ecb.py'), 'a').write('# was here\\n')\n"
        "except OSError:\n"
        "    pass\n"
        "seen = {k: v for k, v in os.environ.items() if 'SEED' in k or 'TOKEN' in k}\n"
        "json.dump({'bomFormat': 'CycloneDX', 'specVersion': '1.6', 'components': [], 'metadata': {'properties':"
        " [{'name': 'seen', 'value': json.dumps(seen)}]}}, open(os.path.join(out, 'cbom.json'), 'w'))\n")
    p = tmp / "probe"
    r = bench("run", "--name", "probe", "--scanner-cmd", f"{PY} {probe} {{corpus}} {{out}}", "--scanner-version", "0",
              "--bundle", str(p), "--allow-path", str(probe), env={"CBOM_HOLDOUT_SEED": "777", "GITHUB_TOKEN": "x"})
    pm = json.loads((p / "manifest.json").read_text())
    ok &= check("the shipped corpus is never modified by a scanner",
                "was here" not in (ROOT / "corpus/tier1/python/t1_aes_ecb.py").read_text())
    ok &= check("a scanner that writes to its corpus is blocked (read-only) or not scored (tampered)",
                (pm["run"]["isolation"]["inputs_readonly"] == "read-only bind mount" and not pm["run"]["tampered"])
                or (pm["verdict"] == "not scored" and r.returncode == 2))
    if (p / "raw" / "cbom.json").exists():
        seen = json.loads(json.loads((p / "raw" / "cbom.json").read_text())["metadata"]["properties"][0]["value"])
        ok &= check("the scanner saw no seed and no token", seen == {})
    r = bench("run", "--name", "probe", "--scanner-cmd", f"{PY} {probe} {{corpus}} {{out}}", "--scanner-version", "0",
              "--bundle", str(tmp / "probe-h"), "--holdout-seed", "31337", "--allow-path", str(probe))
    hm = json.loads((tmp / "probe-h" / "manifest.json").read_text())
    blob = "".join(f.read_text(errors="ignore") for f in (tmp / "probe-h").rglob("*") if f.is_file())
    ok &= check("a holdout run records a seed commitment, and the seed appears nowhere in the bundle",
                hm["holdout"]["seed_commitment"] == bm.seed_commitment(31337) and "31337" not in blob)
    r = bench("run", "--name", "grep", "--scanner-cmd", f"{PY} {GREP} {{corpus}} -o {{out}}/cbom.json", "--scanner-version", "0",
              "--bundle", str(tmp / "grep-h"), "--holdout-seed", "31337", "--keep-holdout-cbom", str(tmp / "kept" / "h.json"), *TOOLS)
    r1 = bench("verify", str(tmp / "grep-h"))
    r2 = bench("verify", str(tmp / "grep-h"), "--holdout-seed", "31337", "--holdout-cbom", str(tmp / "kept" / "h.json"))
    r3 = bench("verify", str(tmp / "grep-h"), "--holdout-seed", "31338")
    ok &= check("holdout gaps: flagged as not re-derived without the seed; re-derive with seed and kept CBOM; a wrong seed fails",
                r1.returncode == 0 and "not re-derived here: the holdout gaps" in r1.stdout
                and r2.returncode == 0 and "gaps re-derive from the seed" in r2.stdout and r3.returncode == 1)

    r = bench("run", "--name", "slow", "--scanner-cmd", f"{PY} -c 'import time; time.sleep(60)'",
              "--scanner-version", "0", "--timeout", "2", "--bundle", str(tmp / "slow"))
    sm = json.loads((tmp / "slow" / "manifest.json").read_text())
    ok &= check("a scanner past its time limit is not scored (exit 2) and the bundle says why",
                r.returncode == 2 and sm["verdict"] == "not scored" and any("timed out" in w for w in sm["why"]))
    r = bench("verify", str(tmp / "slow"))
    ok &= check("a not-scored bundle still verifies its checksums", r.returncode == 0)

    # The large-repository fixture: grep finishes the small tree, the result reproduces, and a scanner
    # that doesn't finish inside the budget is reported as such.
    r = bench("perf", "--name", "grep", "--scanner-cmd", f"{PY} {GREP} {{corpus}} -o {{out}}/cbom.json",
              "--size", "small", "--bundle", str(tmp / "perf"), *TOOLS)
    pm = json.loads((tmp / "perf" / "manifest.json").read_text())
    ok &= check(f"perf: grep finishes the small fixture inside the budget ({pm['result']['found']}/{pm['result']['planted']} planted found)",
                r.returncode == 0 and pm["within_budget"] and pm["result"]["found"] >= pm["result"]["planted"] * 0.7)
    r = bench("verify", str(tmp / "perf"))
    ok &= check("perf: the fixture regenerates and the result re-derives", r.returncode == 0)
    shutil.copytree(tmp / "perf", tmp / "perf-noraw")
    (tmp / "perf-noraw" / "raw" / "cbom.json").unlink()
    (tmp / "perf-noraw" / "SHA256SUMS").write_text(bm.sums(tmp / "perf-noraw"))
    r = bench("verify", str(tmp / "perf-noraw"))
    ok &= check("perf: a finished bundle without its raw CBOM does not verify (the reviewer's case)",
                r.returncode == 1 and "carries raw/cbom.json" in r.stdout)
    r = bench("perf", "--name", "slow", "--scanner-cmd", f"{PY} -c 'import time; time.sleep(60)'", "--size", "small",
              "--budget", "2", "--bundle", str(tmp / "perf-slow"))
    sm = json.loads((tmp / "perf-slow" / "manifest.json").read_text())
    ok &= check("perf: a scanner over budget -> 'timed out', exit 2", r.returncode == 2 and sm["status"] == "timed out")

    shutil.rmtree(tmp, ignore_errors=True)
    print("\nAll bench checks pass." if ok else "\nBench checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
