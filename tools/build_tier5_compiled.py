#!/usr/bin/env python3
"""Build the Tier 5 compiled-only artifacts from tier5-sources/ into corpus/tier5/*/compiled/.

  tier5-sources/python/ledger_sync.py                -> corpus/tier5/python/compiled/ledger_sync.pyc
  tier5-sources/java/com/acme/billing/Settlement.java -> corpus/tier5/java/compiled/billing-core.jar
  tier5-sources/java-obfuscated/                      -> corpus/tier5/java/compiled/token-vault.jar  (ProGuard)
  tier5-sources/javascript/session_tokens.js          -> corpus/tier5/javascript/dist/session-tokens.min.js  (terser)
  tier5-sources/c/meterd.c                            -> corpus/tier5/c/bin/meterd  (stripped ELF, links libcrypto)

The sources stay outside corpus/ so a scanner sees only bytecode. A .pyc is tied to the Python
minor version that built it (its magic number), so rebuild if you run the corpus under another one.

The last three need tools that aren't part of the verify toolchain: ProGuard (`apt install
proguard-cli`), terser (`npm install terser@5.36.0`, on PATH or named in $TERSER) and a C compiler
with OpenSSL headers. Each is skipped with a message when its tool is missing; the built files are
committed, so only someone changing a source needs them. The binary is x86-64 Linux.
"""
import os
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

    build_minified_js()
    build_native()
    build_obfuscated_jar()
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


def build_obfuscated_jar():
    if not all(shutil.which(t) for t in ("javac", "jar", "proguard")):
        print("  javac/jar/proguard not found: skipped token-vault.jar")
        return
    src = SRC / "java-obfuscated"
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["javac", "--release", "11", "-g:none", "-d", f"{td}/cls", *[str(p) for p in src.rglob("*.java")]], check=True)
        subprocess.run(["jar", "--create", "--file", f"{td}/in.jar", "--main-class", "Main", "-C", f"{td}/cls", "."], check=True)
        jar = OUT_JV / "token-vault.jar"
        jar.unlink(missing_ok=True)
        subprocess.run(["proguard", f"@{src / 'proguard.pro'}", "-injars", f"{td}/in.jar", "-outjars", str(jar)],
                       check=True, stdout=subprocess.DEVNULL)
    print(f"  {jar.relative_to(ROOT)}  (ProGuard: names replaced, packages flattened)")


def build_minified_js():
    terser = os.environ.get("TERSER") or shutil.which("terser")
    if not terser:
        print("  terser not found (npm install terser@5.36.0, or set $TERSER): skipped session-tokens.min.js")
        return
    out = ROOT / "corpus" / "tier5" / "javascript" / "dist" / "session-tokens.min.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([terser, str(SRC / "javascript" / "session_tokens.js"), "--compress", "--mangle", "--toplevel", "-o", str(out)], check=True)
    print(f"  {out.relative_to(ROOT)}  (terser --compress --mangle --toplevel)")


def build_native():
    cc = shutil.which("cc") or shutil.which("gcc")
    if not cc or not shutil.which("strip"):
        print("  cc/strip not found: skipped meterd")
        return
    out = ROOT / "corpus" / "tier5" / "c" / "bin" / "meterd"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([cc, "-O2", "-o", str(out), str(SRC / "c" / "meterd.c"), "-lcrypto"], check=True)
    subprocess.run(["strip", str(out)], check=True)
    print(f"  {out.relative_to(ROOT)}  (stripped, dynamically linked to libcrypto)")


if __name__ == "__main__":
    sys.exit(main())
