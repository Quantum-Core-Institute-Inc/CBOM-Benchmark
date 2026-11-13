#!/usr/bin/env python3
"""Change detection: the changed files run, the after answer key resolves, a perfect scanner sees
every change, and each way of missing one is caught. Also the identity comparison.

Run: python tools/test_drift.py
"""
import copy
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drift  # noqa: E402
from cbomlib import load_json, make_component, same_file  # noqa: E402
from score import load_truth, score  # noqa: E402
from test_remediation import runs  # noqa: E402

ROOT = drift.ROOT
REF = load_json(ROOT / "expected" / "expected.cdx.json")


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return bool(cond)


def perfect_after(gt_after: dict) -> dict:
    """The reference CBOM with every changed file re-described from the after answer key."""
    files = drift.changed_files()
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


def drop(bom: dict, ref: str) -> dict:
    out = copy.deepcopy(bom)
    out["components"] = [c for c in out["components"] if c.get("bom-ref") != ref]
    return out


def main() -> int:
    ok = True
    work = Path(tempfile.mkdtemp(prefix="drift-test-"))
    chs = drift.changes()
    kinds = [c["kind"] for c in chs]
    ok &= check("three changes of each kind", all(kinds.count(k) == 3 for k in drift.KINDS))
    ok &= check("no change touches a file fix-and-rescan migrates (the two kits stay independent)",
                not drift.changed_files() & {m["file"] for m in drift.rm.migrations()})
    for c in chs:
        if c.get("delete"):
            ok &= check(f"{c['id']} deletes a file the corpus has", (ROOT / c["file"]).is_file())
            continue
        good, detail = runs(drift.AFTER / c["file"], work)
        ok &= check(f"{c['id']} changed file runs ({detail})", good)
    ok &= check("an added file is one the shipped corpus does not have",
                not (ROOT / "corpus/tier1/python/t1_export_digest.py").exists())

    gt = load_truth(include_custom=False)[0]
    gt_after = drift.after_truth(gt)
    ok &= check("the after answer key resolves every anchor in the changed files",
                all(f.get("lines") is not None for f in gt_after["findings"]))
    ok &= check("the after answer key has 3 fewer shipped findings in changed files and 6 new ones",
                len(gt_after["findings"]) == len(gt["findings"]) - 6 + 6
                and sum(1 for f in gt_after["findings"] if f.get("remediation")) == 6)
    corpus = drift.build_after(work / "after")
    ok &= check("the changed corpus has the new file and not the deleted one",
                (corpus / "tier1/python/t1_export_digest.py").is_file() and not (corpus / "tier1/python/t1_dsa.py").exists())

    before = score(REF, custom="exclude")
    perfect = perfect_after(gt_after)

    def ev_of(bom, b=before):
        return drift.evaluate(b, score(bom, custom="exclude", truth=copy.deepcopy(gt_after), corpus=corpus), bom)

    ev = ev_of(perfect)
    ok &= check(f"a perfect scanner sees every change ({ev['seen']}/{ev['total']})",
                ev["eligible"] == ev["total"] == 9 and ev["seen"] == 9 and all(v == {"total": 3, "eligible": 3, "seen": 3} for v in ev["by_kind"].values()))
    ok &= check("a perfect scanner: no noise outside the changed files",
                not ev["noise_outside"]["lost"] and not ev["noise_outside"]["gained"]
                and ev["noise_outside"]["false_positives_before"] == ev["noise_outside"]["false_positives_after"])

    # A scanner that reports the shipped corpus again (cached results, or it scanned the wrong tree).
    v = {c["id"]: c for c in ev_of(REF)["changes"]}
    ok &= check("the unchanged report on the changed corpus: no addition, removal or downgrade is seen",
                all(c["verdict"] == "missed" for c in v.values()))
    ok &= check("... and the removed algorithm is named as still reported", v["DRIFT-REMOVE-02"]["removed_still_reported"] == ["T1-GO-09"])
    ok &= check("... including one still reported in a file that was deleted", v["DRIFT-REMOVE-03"]["removed_still_reported"] == ["T1-PY-07"])

    # An addition missed.
    v = {c["id"]: c for c in ev_of(drop(perfect, "after-DRIFT-ADD-02-A1"))["changes"]}
    ok &= check("a new algorithm not reported -> missed; the other changes are still seen",
                v["DRIFT-ADD-02"]["verdict"] == "missed" and sum(c["verdict"] == "seen" for c in v.values()) == 8)

    # A downgrade reported with the old strength.
    wrong = copy.deepcopy(perfect)
    for c in wrong["components"]:
        if c.get("bom-ref") == "after-DRIFT-DOWN-02-A1":
            c["cryptoProperties"]["algorithmProperties"]["parameterSetIdentifier"] = "3072"
            c["name"] = "RSA-3072"
    v = {c["id"]: c for c in ev_of(wrong)["changes"]}
    ok &= check("RSA-3072 to RSA-1024 reported as still 3072 -> missed", v["DRIFT-DOWN-02"]["verdict"] == "missed")

    # A downgrade where the new algorithm is found but the old one is still reported.
    both = copy.deepcopy(perfect)
    both["components"].append(make_component("stale-gcm", "AES", {"key_size": 256, "mode": "GCM"},
                                             [{"location": "corpus/tier1/javascript/t1_aes_gcm.js", "line": 5}]))
    v = {c["id"]: c for c in ev_of(both)["changes"]}
    ok &= check("old parameters still reported beside the new ones -> missed", v["DRIFT-DOWN-03"]["verdict"] == "missed")

    # A removal the scanner could never show: it had not found the original.
    blind = copy.deepcopy(REF)
    blind["components"] = [c for c in blind["components"]
                           if not any(same_file(o.get("location", ""), "corpus/tier1/python/t1_dsa.py")
                                      for o in (c.get("evidence") or {}).get("occurrences") or [])]
    e = ev_of(perfect, score(blind, custom="exclude"))
    v = {c["id"]: c for c in e["changes"]}
    ok &= check("original not found before -> not eligible, and not counted against the rate",
                v["DRIFT-REMOVE-03"]["verdict"] == "not eligible" and e["eligible"] == 8 and e["seen"] == 8
                and e["by_kind"]["remove"] == {"total": 3, "eligible": 2, "seen": 2})

    # An addition the scanner had already (falsely) reported before the change.
    noisy = copy.deepcopy(REF)
    noisy["components"].append(make_component("fp-3des", "3DES", {"mode": "CBC"},
                                              [{"location": "corpus/tier1/go/ed25519/main.go", "line": 5}]))
    v = {c["id"]: c for c in ev_of(perfect, score(noisy, custom="exclude"))["changes"]}
    ok &= check("an algorithm falsely reported before the change does not count as a seen addition",
                v["DRIFT-ADD-02"]["verdict"] == "missed" and v["DRIFT-ADD-02"]["already_reported_before"] == ["3DES"])

    # A change in the scanner's output where nothing changed.
    lost = drop(perfect, next(c["bom-ref"] for c in perfect["components"]
                              if any(same_file(o.get("location", ""), "corpus/tier1/python/t1_hashes.py")
                                     for o in (c.get("evidence") or {}).get("occurrences") or [])))
    ok &= check("a finding lost in an untouched file is reported as noise", len(ev_of(lost)["noise_outside"]["lost"]) >= 1)

    # ---- identity
    changed = {"corpus/a/changed.py"}

    def comp(ref, name, loc):
        return {"type": "cryptographic-asset", "name": name, **({"bom-ref": ref} if ref else {}),
                "evidence": {"occurrences": [{"location": loc, "line": 3}]}}

    b = {"components": [comp("x1", "AES", "corpus/a/one.py"), comp("x2", "RSA", "corpus/a/two.py"), comp("x3", "MD5", "corpus/a/changed.py")]}
    a_same = {"components": [comp("x2", "RSA", "corpus/a/two.py"), comp("x1", "AES", "corpus/a/one.py"), comp("x9", "SHA-1", "corpus/a/changed.py")]}
    i = drift.identity(b, a_same, changed)
    ok &= check("content-derived identifiers: unchanged assets keep them (order does not matter)",
                (i["verdict"], i["paired"], i["same"]) == ("stable", 2, 2))
    a_seq = {"components": [comp("x1", "SHA-1", "corpus/a/changed.py"), comp("x2", "AES", "corpus/a/one.py"), comp("x3", "RSA", "corpus/a/two.py")]}
    i = drift.identity(b, a_seq, changed)
    ok &= check("sequence-numbered identifiers shift when a file changes -> not stable",
                (i["verdict"], i["paired"], i["same"]) == ("not stable", 2, 0))
    none = {"components": [comp(None, "AES", "corpus/a/one.py"), comp(None, "RSA", "corpus/a/two.py")]}
    ok &= check("no bom-ref at all -> 'no identifiers'", drift.identity(none, none, changed)["verdict"] == "no identifiers")
    multi_b = {"components": [{"type": "cryptographic-asset", "name": "AES", "bom-ref": "aes",
                               "evidence": {"occurrences": [{"location": "corpus/a/one.py"}, {"location": "corpus/a/changed.py"}]}}]}
    multi_a = {"components": [{"type": "cryptographic-asset", "name": "AES", "bom-ref": "aes",
                               "evidence": {"occurrences": [{"location": "corpus/a/one.py"}]}}]}
    i = drift.identity(multi_b, multi_a, changed)
    ok &= check("a component that loses an occurrence in a changed file is still the same asset", (i["paired"], i["same"]) == (1, 1))
    dup = {"components": [comp("d1", "AES", "corpus/a/one.py"), comp("d2", "AES", "corpus/a/one.py")]}
    i = drift.identity(dup, dup, changed)
    ok &= check("assets with identical content are left out, not guessed at", i["paired"] == 0 and i["content_not_unique"] == 1 and i["verdict"] == "not measurable")

    def res(fp, uri):
        return {"ruleId": "weak-hash", "message": {"text": "MD5"}, **({"partialFingerprints": {"h": fp}} if fp else {}),
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}, "region": {"startLine": 2}}}]}
    s1 = {"runs": [{"results": [res("f1", "corpus/a/one.py"), res("f2", "corpus/a/changed.py")]}]}
    s2 = {"runs": [{"results": [res("f1", "corpus/a/one.py")]}]}
    i = drift.identity(s1, s2, changed)
    ok &= check("SARIF results are followed by their fingerprints", (i["identifier"], i["verdict"], i["same"]) == ("SARIF fingerprints", "stable", 1))
    ok &= check("output that is neither is 'not applicable'", drift.identity([], [], changed)["verdict"] == "not applicable")
    ok &= check("the cells say it in words",
                drift.seen_cell(ev) == "9/9 (100.0%)" and drift.seen_cell(None) == "not measured"
                and drift.identity_cell({"identity": drift.identity(b, a_seq, changed)}) == "0/2 unchanged assets keep their identifier")

    shutil.rmtree(work, ignore_errors=True)
    print("\nAll change-detection checks pass." if ok else "\nChange-detection checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
