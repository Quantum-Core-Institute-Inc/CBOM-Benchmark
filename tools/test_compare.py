#!/usr/bin/env python3
"""compare.py refuses scorecards that weren't measured on the same thing.

Run: python tools/test_compare.py
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import load_json  # noqa: E402
from compare import eligibility  # noqa: E402
from score import load_scope, score  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return cond


def main() -> int:
    ok = True
    ref = load_json(ROOT / "expected" / "expected.cdx.json")
    full = score(ref, custom="exclude")
    scoped = score(ref, custom="exclude", scope=load_scope(ROOT / "integrations" / "qci-pqc" / "scope.json"))

    ok &= check("two unscoped scorecards on the same release -> comparable", eligibility({"a": full, "b": copy.deepcopy(full)}) == [])
    probs = eligibility({"full": full, "scoped": scoped})
    n_scoped = sum(1 for r in scoped["results"] if r["tier"] != "custom")
    ok &= check(f"scoped vs full (the reviewer's case; here {n_scoped} vs {len(full['results'])}) -> refused, names the scope and the counts",
                any("declared scope" in p for p in probs) and any(f"scores {n_scoped} findings" in p for p in probs))
    ok &= check("same pair with --allow-scoped -> allowed (rendered with labelled denominators)",
                eligibility({"full": full, "scoped": scoped}, allow_scoped=True) == [])
    for key in ("release", "answer_key", "corpus", "scorer", "policy"):
        other = copy.deepcopy(full)
        other["manifest"][key] = "something-else"
        ok &= check(f"different {key} -> refused", any(key in p for p in eligibility({"a": full, "b": other})))
    legacy = copy.deepcopy(full)
    legacy.pop("manifest")
    ok &= check("scorecard without a manifest -> refused", any("no manifest" in p for p in eligibility({"a": full, "b": legacy})))
    fewer = copy.deepcopy(full)
    fewer["results"] = fewer["results"][:-5]
    ok &= check("same manifest but five findings dropped -> refused",
                any("only there" in p for p in eligibility({"a": full, "b": fewer})))
    print("\nAll comparison checks pass." if ok else "\nComparison checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
