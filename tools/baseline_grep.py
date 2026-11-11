#!/usr/bin/env python3
"""A deliberately naive regex "scanner" that emits a CycloneDX 1.6 CBOM.

It exists to calibrate the testbench: any real CBOM product should beat it on
precision and on parameter extraction. If one doesn't, it is a grep with a logo.

Usage: python tools/baseline_grep.py [scan_dir] [-o out.cdx.json]
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import make_bom, make_component  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".py", ".java", ".js", ".mjs", ".ts", ".c", ".h", ".mod", ".json", ".properties", ".yaml", ".yml", ".xml", ".conf", ".cfg", ".ini", ".go", ".cs",
            ".pem", ".crt", ".key", ".pub", ".cnf", ".md", ""}  # "" = extensionless (sshd_config, id_ed25519)

PATTERNS = [
    ("MD5", r"md5"),
    ("SHA-1", r"sha-?1(?![0-9])"),
    ("SHA-256", r"sha-?256"),
    ("SHA-384", r"sha-?384"),
    ("SHA3-256", r"sha3[-_]?256"),
    ("RSA", r"(?<![a-z])rsa"),
    ("DSA", r"(?<![a-z])dsa"),
    ("EC", r"ecdsa|secp\d+r1|\bec\.generate|getinstance\(\"ec\"\)"),
    ("AES", r"aes"),
    ("3DES", r"desede|tripledes|3des"),
    ("DES", r"(?<![a-z0-9])des(?![a-z])"),
    ("HMAC", r"hmac"),
    ("PBKDF2", r"pbkdf2"),
    ("ChaCha20-Poly1305", r"chacha20"),
    ("Ed25519", r"ed25519"),
    ("X25519", r"x25519|curve25519"),
    ("DH", r"(?<![a-z])dh\.|getinstance\(\"dh\"\)|diffie-hellman"),
    ("ML-KEM", r"ml-?kem"),
    ("ML-DSA", r"ml-?dsa"),
]
COMPILED = [(fam, re.compile(p, re.IGNORECASE)) for fam, p in PATTERNS]
PROTO_RX = re.compile(r"\b(ssl|tls)v(\d)(?:\.(\d))?\b", re.IGNORECASE)


def line_params(family: str, line: str) -> dict:
    p = {}
    nums = [int(n) for n in re.findall(r"\b(\d{3,4})\b", line)]
    if family == "AES":
        ks = next((n for n in nums if n in (128, 192, 256)), None)
        if ks:
            p["key_size"] = ks
    if family in ("RSA", "DSA", "DH"):
        ks = next((n for n in nums if n in (1024, 2048, 3072, 4096)), None)
        if ks:
            p["key_size"] = ks
    if family in ("AES", "DES", "3DES"):
        m = re.search(r"\b(ECB|CBC|GCM|CTR)\b", line.upper())
        if m:
            p["mode"] = m.group(1)
    if family == "EC":
        m = re.search(r"secp(256|384|521)r1", line, re.IGNORECASE)
        if m:
            p["curve"] = f"P-{m.group(1)}"
    return p


def scan(scan_dir: Path) -> dict:
    hits = defaultdict(lambda: {"occ": [], "params": {}})
    for path in sorted(scan_dir.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_EXT:
            continue
        base = ROOT if path.resolve().is_relative_to(ROOT) else scan_dir.parent  # holdout sets live elsewhere
        rel = str(path.resolve().relative_to(base)).replace("\\", "/")
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            hits_here = [fam for fam, rx in COMPILED if rx.search(line)]
            for m in PROTO_RX.finditer(line):
                hits_here.append(f"{m.group(1).upper()}-{m.group(2)}.{m.group(3) or 0}")
            for fam in hits_here:
                h = hits[(rel, fam)]
                h["occ"].append({"location": rel, "line": n})
                for k, v in line_params(fam, line).items():
                    h["params"].setdefault(k, v)
    comps = [make_component(f"grep-{i}", fam, h["params"], h["occ"])
             for i, ((rel, fam), h) in enumerate(sorted(hits.items()))]
    return make_bom(comps, "baseline_grep")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scan_dir", nargs="?", default=str(ROOT / "corpus"))
    ap.add_argument("-o", "--out", default=str(ROOT / "reports" / "baseline_grep.cdx.json"))
    a = ap.parse_args()
    bom = scan(Path(a.scan_dir).resolve())
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(bom, indent=2) + "\n", encoding="utf-8")
    print(f"baseline_grep: {len(bom['components'])} components -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
