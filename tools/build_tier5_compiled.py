#!/usr/bin/env python3
"""Build the Tier 5 compiled-only artifacts from tier5-sources/ into corpus/tier5/*/compiled/.

  tier5-sources/python/ledger_sync.py                -> corpus/tier5/python/compiled/ledger_sync.pyc
  tier5-sources/java/com/acme/billing/Settlement.java -> corpus/tier5/java/compiled/billing-core.jar

The sources stay outside corpus/ so a scanner sees only bytecode. A .pyc is tied to the Python
minor version that built it (its magic number), so rebuild if you run the corpus under another one.
"""
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tier5-sources"
OUT_PY = ROOT / "corpus" / "tier5" / "python" / "compiled"
OUT_JV = ROOT / "corpus" / "tier5" / "java" / "compiled"


def main() -> int:
    OUT_PY.mkdir(parents=True, exist_ok=True)
    OUT_JV.mkdir(parents=True, exist_ok=True)

    pyc = OUT_PY / "ledger_sync.pyc"
    py_compile.compile(str(SRC / "python" / "ledger_sync.py"), cfile=str(pyc), doraise=True,
                       invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
    print(f"  {pyc.relative_to(ROOT)}  (Python {sys.version_info.major}.{sys.version_info.minor} bytecode)")

    if not shutil.which("javac") or not shutil.which("jar"):
        print("  javac/jar not found: skipped billing-core.jar")
        return 0
    with tempfile.TemporaryDirectory() as td:
        sources = [str(p) for p in (SRC / "java").rglob("*.java")]
        subprocess.run(["javac", "--release", "17", "-g:none", "-d", td, *sources], check=True)
        jar = OUT_JV / "billing-core.jar"
        jar.unlink(missing_ok=True)
        subprocess.run(["jar", "--create", "--file", str(jar), "--main-class", "com.acme.billing.Settlement",
                        "-C", td, "."], check=True)
    print(f"  {jar.relative_to(ROOT)}  (Java 17 bytecode, no debug info)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
