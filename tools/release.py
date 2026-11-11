"""What a score was measured against: testbench release, answer key, corpus, scorer, policy, adapter.

Two consumers:
  * gates (run_qci_pqc.py): a baseline is only enforced against the exact stamp it was set on.
  * scorecards (score.py manifest -> compare.py): two scorecards are only compared when they were
    produced on the same finding set, corpus, scorer and policy.
"""
from __future__ import annotations

import pyreq  # noqa: F401  (fails early on an unsupported Python)
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = (ROOT / "VERSION").read_text().strip()


def _methodology() -> str:
    import re
    m = re.search(r"Methodology version: \*\*([\d.]+)\*\*", (ROOT / "METHODOLOGY.md").read_text())
    if not m:
        raise SystemExit("METHODOLOGY.md has no 'Methodology version: **X.Y**' line")
    return m.group(1)


METHODOLOGY = _methodology()

# Everything that decides how a CBOM turns into numbers.
SCORER_FILES = ["tools/score.py", "tools/cbomlib.py", "tools/actionability.py", "tools/libraries.py",
                "tools/truth.py", "tools/assetfacts.py", "tools/policy.py", "rubric/actionability.json"]
ANSWER_KEY_FILES = ["expected/ground_truth.json", "expected/libraries.json"]


def _sha(paths, short=16) -> str:
    h = hashlib.sha256()
    for rel in paths:
        p = ROOT / rel
        h.update(rel.encode())
        h.update(b"\0")
        h.update(p.read_bytes() if p.exists() else b"<missing>")
        h.update(b"\0")
    return h.hexdigest()[:short]


def corpus_sha() -> str:
    files = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "corpus").rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and not p.relative_to(ROOT / "corpus").parts[0] == "custom")
    return _sha(files)


def shipped_finding_ids() -> list[str]:
    gt = json.loads((ROOT / "expected" / "ground_truth.json").read_text())
    return sorted(f["id"] for f in gt["findings"] if not f.get("calibration"))


def findings_sha(ids) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()[:16]


def stamp(policy: str = "nist", adapter_files: tuple[str, ...] = ()) -> dict:
    """The full identity of a measurement environment."""
    ids = shipped_finding_ids()
    return {
        "release": VERSION,
        "methodology": METHODOLOGY,
        "findings": len(ids),
        "answer_key": _sha(ANSWER_KEY_FILES),
        "corpus": corpus_sha(),
        "scorer": _sha(SCORER_FILES),
        "policy": f"{policy}:{_sha([f'policies/{policy}.json'])}",
        **({"adapter": _sha(list(adapter_files))} if adapter_files else {}),
    }


def file_inventory(adapter_files=()) -> dict:
    """Full sha256 of every file that decides a score, for an evidence bundle."""
    files = sorted({*SCORER_FILES, *ANSWER_KEY_FILES, *adapter_files, "METHODOLOGY.md", "VERSION",
                    *(str(p.relative_to(ROOT)) for p in (ROOT / "policies").glob("*.json"))})
    return {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files if (ROOT / f).exists()}


def stamp_diff(old: dict | None, new: dict) -> list[str]:
    """Human-readable differences; empty when the stamps match."""
    if not old:
        return ["no stamp"]
    return [f"{k}: {old.get(k)} -> {new.get(k)}" for k in sorted(set(old) | set(new)) if old.get(k) != new.get(k)]
