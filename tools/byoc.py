#!/usr/bin/env python3
"""Bring your own code: add your organization's crypto patterns to the testbench as scored cases.

  python tools/byoc.py new <case> --lang python|java|assets [--use web] [--owner "Team"] [--description "..."]
  python tools/byoc.py draft <case> [--write]       candidate findings from a naive scan, UNCONFIRMED
  python tools/byoc.py add <case> --file F --alg "RSA-2048" --anchor "generate_private_key(" [--confirm]
  python tools/byoc.py check [<case> ...] [--no-run] [--allow-drafts]
  python tools/byoc.py list

Code goes in corpus/custom/<case>/, the case's answer key in expected/custom/<case>.json.
See BYOC.md for the full walkthrough.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import FAMILIES, display_name, normalize  # noqa: E402
from truth import CUSTOM_DIR, ROOT, case_path, custom_manifests, load_manifest  # noqa: E402

CORPUS_CUSTOM = ROOT / "corpus" / "custom"
CASE_RE = re.compile(r"^[a-z][a-z0-9_]{1,48}$")
USES = ["custom", "web", "networking", "firmware-signing", "os", "niche"]
CODE_EXT = {".py", ".java", ".js", ".ts", ".go", ".cs", ".c", ".cpp", ".h", ".kt", ".rb", ".php", ".rs"}

# ---------------------------------------------------------------------------- templates
TEMPLATES = {
    "python": {
        "main.py": '"""Entry point for this case. Replace with a trimmed copy of the real pattern."""\n'
                   'from app import service\n\nif __name__ == "__main__":\n    print(service.run())\n',
        "app/__init__.py": '"""Application package."""\n',
        "app/service.py": '"""Replace with your code. Keep the crypto call pattern; drop the business logic."""\n\n\n'
                          'def run():\n    return "replace me"\n',
    },
    "java": {
        "src/com/acme/Main.java": "package com.acme;\n\n/** Entry point for this case. Replace with a trimmed copy of the real pattern. */\n"
                                  "public class Main {\n    public static void main(String[] args) throws Exception {\n"
                                  "        System.out.println(\"replace me\");\n    }\n}\n",
    },
    "assets": {
        "README.txt": "Put configuration files, certificates and key files for this case here.\n"
                      "Use freshly generated test keys only. Never copy production key material.\n",
    },
}
RUNNERS = {"python": {"run": ["python3", "main.py"]}, "java": {"java_main": "com.acme.Main"}, "assets": {}}

# ---------------------------------------------------------------------------- lint patterns
SECRET_PATTERNS = [
    (r"-----BEGIN (RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----", "private key block"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}\b", "GitHub token"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b", "Slack token"),
    (r"(?i)\b(password|passwd|secret|api[_-]?key|token)\b\s*[=:]\s*['\"][^'\"\s]{8,}['\"]", "hardcoded credential"),
]
SAFE_DOMAINS = re.compile(r"(^|\.)(example\.(com|org|net)|[a-z0-9-]+\.(example|test|invalid|local|localhost|internal))$")
DOMAIN_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:com|net|org|io|gov|mil|edu|co|us|uk|de|fr|ca|au|in|cloud|corp|biz|info)\b", re.I)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
IP_RE = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")
ALG_WORDS = re.compile(r"(?i)\b(RSA|AES|3?DES(ede)?|SHA-?\d+|SHA3|MD5|HMAC|PBKDF2|ECDSA|ECDH|Ed25519|X25519|ML-?KEM|ML-?DSA|"
                       r"Kyber|Dilithium|ChaCha20|P-?(256|384|521)|secp\d+[rk]1|\d{3,4}-bit|ECB|CBC|GCM)\b")


def _ip_is_public(m) -> bool:
    a, b = int(m.group(1)), int(m.group(2))
    if any(int(x) > 255 for x in m.groups()):
        return False
    private = a in (10, 127, 0) or (a == 172 and 16 <= b <= 31) or (a == 192 and b == 168) or (a == 169 and b == 254)
    documentation = (a, b) in ((192, 0), (198, 51), (203, 0)) or a >= 224
    return not (private or documentation)


def comment_lines(path: Path) -> list[tuple[int, str]]:
    """Approximate comment and docstring lines for Python and C-family files."""
    out, in_block, quote = [], False, None
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        t = line.strip()
        if path.suffix == ".py":
            if quote:
                out.append((n, line))
                if quote in t:
                    quote = None
                continue
            if t.startswith(('"""', "'''")):
                q = t[:3]
                out.append((n, line))
                if t.count(q) == 1:
                    quote = q
                continue
            if "#" in line:
                out.append((n, line[line.index("#"):]))
        else:
            if in_block:
                out.append((n, line))
                if "*/" in t:
                    in_block = False
                continue
            if t.startswith("/*"):
                out.append((n, line))
                in_block = "*/" not in t
                continue
            if "//" in line:
                out.append((n, line[line.index("//"):]))
    return out


# ---------------------------------------------------------------------------- helpers
def manifest_path(case: str) -> Path:
    return CUSTOM_DIR / f"{case}.json"


def case_dir(case: str) -> Path:
    return CORPUS_CUSTOM / case


def save(case: str, m: dict) -> None:
    CUSTOM_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path(case).write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")


def need_case(case: str) -> dict:
    if not manifest_path(case).exists():
        raise SystemExit(f"no case {case!r}: run `byoc.py new {case} --lang ...` first")
    return load_manifest(manifest_path(case))


def anchor_hits(file: Path, anchor: str) -> int:
    return sum(1 for line in file.read_text(encoding="utf-8", errors="ignore").splitlines() if anchor in line)


def run_case(case: str, m: dict) -> tuple[bool, str]:
    """Execute a case per its manifest, in the sandbox: a read-only copy of the case directory, a
    scrubbed environment (no credentials, no holdout seed), no network where the host allows it, and
    a 5-minute limit. Returns (ok, detail)."""
    import sandbox
    d = case_dir(case)
    lim = sandbox.Limits(wall_s=300)
    py_bin = (str(Path(sys.executable).parent),)
    env = {"PYTHONDONTWRITEBYTECODE": "1"}
    if m.get("run"):
        r = sandbox.run(list(m["run"]), {"case": d}, lim, extra_path=py_bin, cwd_input="case", set_env=env, keep=False, hide=(str(ROOT),))
    elif m.get("java_main"):
        if not shutil.which("javac"):
            return True, "skipped: javac not found"
        srcs = [str(p.relative_to(d)) for p in sorted(d.rglob("*.java"))]
        r = sandbox.run(["sh", "-c", 'out="$1"; main="$2"; shift 2; javac -d "$out/classes" "$@" && java -cp "$out/classes" "$main"',
                         "byoc", "{out}", m["java_main"], *srcs], {"case": d}, lim, cwd_input="case", keep=False, hide=(str(ROOT),))
    else:
        return True, "no run command (asset case)"
    if r.timed_out:
        return False, "timed out after 300s"
    if r.exit_code is None and r.signal is None:
        return False, r.stderr or "could not start"
    if r.tampered:
        return False, f"modified its own case files ({', '.join(r.tampered)})"
    tail = (r.stderr or r.stdout).strip().splitlines()[-1:] if r.exit_code else []
    return r.exit_code == 0, ("exit 0" if r.exit_code == 0 else f"exit {r.exit_code}: {' '.join(tail)}")


# ---------------------------------------------------------------------------- commands
def cmd_new(a) -> int:
    if not CASE_RE.match(a.case):
        raise SystemExit("case names are lowercase letters, digits and underscores, starting with a letter")
    if manifest_path(a.case).exists() or case_dir(a.case).exists():
        raise SystemExit(f"case {a.case!r} already exists")
    for rel, body in TEMPLATES[a.lang].items():
        p = case_dir(a.case) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    m = {"case": a.case, "description": a.description or "TODO: which pattern from our estate this reproduces",
         "owner": a.owner or "TODO", "lang": a.lang, "use": a.use, **RUNNERS[a.lang],
         "findings": [], "also_ok": [], "decoys": {}}
    save(a.case, m)
    print(f"Created corpus/custom/{a.case}/ and expected/custom/{a.case}.json")
    print("Next: replace the template with your trimmed code, then `byoc.py draft` or `byoc.py add`.")
    return 0


def cmd_draft(a) -> int:
    """Propose candidate findings from the naive grep scanner. They are wrong in predictable ways:
    no key sizes from constants, nothing hidden behind indirection, false hits in comments."""
    from baseline_grep import scan
    m = need_case(a.case)
    d = case_dir(a.case)
    bom = scan(d)
    have = {(f["file"], f["family"]) for f in m.get("findings", [])}
    drafts = []
    for c in bom["components"]:
        fam, params = normalize(c["name"], c["cryptoProperties"]["algorithmProperties"])
        occ = c["evidence"]["occurrences"]
        rel = str((ROOT / occ[0]["location"]).relative_to(d)).replace("\\", "/")
        if (rel, fam) in have or fam not in FAMILIES:
            continue
        lines = (d / rel).read_text(encoding="utf-8", errors="ignore").splitlines()
        anchors = []
        for o in occ:
            text = lines[o["line"] - 1].strip()
            if text and anchor_hits(d / rel, text) == 1 and text not in anchors:
                anchors.append(text)
        drafts.append({"file": rel, "family": fam, "params": params, "anchors": anchors[:2],
                       "note": "DRAFT from naive scan: verify family, parameters and location by reading the code",
                       "confirmed": False})
    if not drafts:
        print("No new candidates. A naive scan can't see indirection; add findings by hand with `byoc.py add`.")
        return 0
    print(json.dumps(drafts, indent=2))
    if a.write:
        m.setdefault("findings", []).extend(drafts)
        save(a.case, m)
        print(f"\nAppended {len(drafts)} UNCONFIRMED drafts to expected/custom/{a.case}.json.")
        print("Edit each one, delete the wrong ones, and set \"confirmed\": true. `check` fails until you do.")
    else:
        print("\n(Not written. Re-run with --write to append these as unconfirmed drafts.)")
    return 0


def cmd_add(a) -> int:
    m = need_case(a.case)
    d = case_dir(a.case)
    f = d / a.file
    if not f.exists():
        raise SystemExit(f"{a.file} not found in corpus/custom/{a.case}/")
    fam, params = normalize(a.alg)
    if fam not in FAMILIES:
        raise SystemExit(f"don't recognize {a.alg!r}. Try a standard name like RSA-2048, AES-256-GCM, SHA-1, "
                         f"HMAC-SHA256, ECDSA-P256, ML-KEM-768, X25519MLKEM768.")
    for kv in a.param or []:
        k, v = kv.split("=", 1)
        params[k] = int(v) if v.isdigit() and k == "key_size" else v
    for anc in a.anchor or []:
        n = anchor_hits(f, anc)
        if n != 1:
            raise SystemExit(f"anchor {anc!r} appears {n} times in {a.file}; it must appear exactly once")
    if any(x["file"] == a.file and x["family"] == fam for x in m.get("findings", [])):
        raise SystemExit(f"{a.file} already has a {fam} finding (one per file and family)")
    entry = {"file": a.file, "family": fam, "params": params, "anchors": a.anchor or []}
    if a.alt:
        entry["alt_files"] = []
        for alt in a.alt:
            af, _, anc = alt.partition(":")
            entry["alt_files"].append({"file": af, "anchors": [anc] if anc else []})
    if a.note:
        entry["note"] = a.note
    entry["confirmed"] = bool(a.confirm)
    m.setdefault("findings", []).append(entry)
    save(a.case, m)
    print(f"Added {display_name(fam, params)} ({fam} {params}) at {a.file}"
          f"{'' if a.confirm else '  [unconfirmed: set confirmed=true or re-add with --confirm]'}")
    return 0


def check_case(case: str, m: dict, run: bool, allow_drafts: bool):
    errors, warnings, info = [], [], []
    d = case_dir(case)
    if not CASE_RE.match(case):
        errors.append("case name must be lowercase letters, digits, underscores")
    if not d.exists():
        return [f"corpus/custom/{case}/ does not exist"], [], []
    for key in ("description", "owner"):
        if not m.get(key) or str(m[key]).startswith("TODO"):
            warnings.append(f"manifest '{key}' is not filled in")
    if m.get("use", "custom") not in USES:
        errors.append(f"use must be one of {', '.join(USES)}")

    seen = set()
    findings = m.get("findings", [])
    if not findings:
        errors.append("no findings: a case with no expected crypto belongs under decoys, or isn't a case yet")
    for i, f in enumerate(findings, 1):
        tag = f"finding {i} ({f.get('family')} in {f.get('file')})"
        p = d / f.get("file", "")
        if not p.is_file():
            errors.append(f"{tag}: file not found")
            continue
        if f.get("family") not in FAMILIES:
            errors.append(f"{tag}: unknown family; use byoc.py add to normalize names")
        key = (f["file"], f.get("family"))
        if key in seen:
            errors.append(f"{tag}: duplicate file+family; split the code or merge the findings")
        seen.add(key)
        if not f.get("confirmed"):
            (warnings if allow_drafts else errors).append(f"{tag}: not confirmed (drafts are not scored)")
        if p.suffix in CODE_EXT and not f.get("anchors"):
            warnings.append(f"{tag}: no anchors, so line accuracy can't be judged")
        for anc in f.get("anchors", []):
            n = anchor_hits(p, anc)
            if n != 1:
                errors.append(f"{tag}: anchor {anc!r} appears {n} times (needs exactly 1)")
        for alt in f.get("alt_files", []):
            ap = d / alt["file"]
            if not ap.is_file():
                errors.append(f"{tag}: alt file {alt['file']} not found")
                continue
            for anc in alt.get("anchors", []):
                if anchor_hits(ap, anc) != 1:
                    errors.append(f"{tag}: alt anchor {anc!r} not unique in {alt['file']}")
        for k in f.get("params", {}):
            if k not in ("key_size", "curve", "mode", "hash", "param_set"):
                warnings.append(f"{tag}: param '{k}' is not one the scorer checks")

    ids = {f.get("id") for f in findings}
    for mat in m.get("materials", []):
        if mat.get("key") not in ids:
            errors.append(f"material {mat.get('id')}: key must name a finding id (give that finding an 'id')")

    decoys = set(m.get("decoys", {}))
    files_with_findings = {f.get("file") for f in findings} | {a["file"] for f in findings for a in f.get("alt_files", [])}
    for p in sorted(x for x in d.rglob("*") if x.is_file()):
        rel = str(p.relative_to(d)).replace("\\", "/")
        if p.name.endswith((".class", ".pyc")) and "__pycache__" in p.parts:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        is_asset_dir = m.get("lang") == "assets"
        for pat, what in SECRET_PATTERNS:
            for mm in re.finditer(pat, text):
                line = text[:mm.start()].count("\n") + 1
                if what == "private key block":
                    msg = (f"{rel}:{line}: {what}. Confirm it was generated for this test, never copied from production"
                           + ("" if is_asset_dir else ". In a code case, prefer generating keys at runtime"))
                    warnings.append(msg)
                else:
                    errors.append(f"{rel}:{line}: looks like a {what}. Remove it; test cases must not carry real secrets")
        for mm in EMAIL_RE.finditer(text):
            if not SAFE_DOMAINS.search(mm.group(1).lower()):
                warnings.append(f"{rel}: email address {mm.group(0)!r}; replace with someone@example.com")
        for mm in DOMAIN_RE.finditer(text):
            host = mm.group(0).lower()
            if not SAFE_DOMAINS.search(host):
                warnings.append(f"{rel}: hostname {host!r}; real hostnames can reveal internal systems. Use *.example.internal")
        for mm in IP_RE.finditer(text):
            if _ip_is_public(mm):
                warnings.append(f"{rel}: public IP {mm.group(0)}; use 192.0.2.x (documentation range)")
        if p.suffix in (".py", ".java") and rel not in decoys:
            for n, line in comment_lines(p):
                hit = ALG_WORDS.search(line)
                if hit:
                    warnings.append(f"{rel}:{n}: comment mentions {hit.group(0)!r}. Comments that name the algorithm "
                                    "hand a scanner the answer; describe the pattern instead (or list the file under decoys)")
        if rel not in files_with_findings and rel not in decoys and p.suffix in CODE_EXT | {".conf", ".cnf", ".yml", ".yaml", ".json", ".pem", ".properties", ".ini"}:
            info.append(f"{rel}: no findings, so it acts as a negative control (anything reported there is a false positive)")

    if run:
        ok, detail = run_case(case, m)
        (info if ok else errors).append(f"run: {detail}")
    return errors, warnings, info


def cmd_check(a) -> int:
    cases = a.cases or [m["case"] for _, m in custom_manifests()]
    if not cases:
        print("No custom cases yet. Start with `byoc.py new <case> --lang python`.")
        return 0
    total_err = 0
    for case in cases:
        m = need_case(case)
        errs, warns, info = check_case(case, m, not a.no_run, a.allow_drafts)
        total_err += len(errs)
        n_conf = sum(1 for f in m.get("findings", []) if f.get("confirmed"))
        print(f"\n== {case}: {n_conf} confirmed finding(s), {len(errs)} error(s), {len(warns)} warning(s)")
        for e in errs:
            print(f"  ERROR  {e}")
        for w in warns:
            print(f"  warn   {w}")
        for i in info:
            print(f"  info   {i}")
    print("\nAll cases pass." if not total_err else f"\n{total_err} error(s). Fix them before scoring.")
    return 1 if total_err else 0


def cmd_list(_a) -> int:
    rows = custom_manifests()
    if not rows:
        print("No custom cases yet.")
    for _, m in rows:
        conf = sum(1 for f in m.get("findings", []) if f.get("confirmed"))
        print(f"{m['case']:<28} {m.get('lang', '?'):<8} {conf:>3} confirmed / {len(m.get('findings', [])):<3} "
              f"{m.get('description', '')[:60]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new")
    p.add_argument("case")
    p.add_argument("--lang", choices=sorted(TEMPLATES), required=True)
    p.add_argument("--use", choices=USES, default="custom")
    p.add_argument("--owner")
    p.add_argument("--description")
    p = sub.add_parser("draft")
    p.add_argument("case")
    p.add_argument("--write", action="store_true")
    p = sub.add_parser("add")
    p.add_argument("case")
    p.add_argument("--file", required=True, help="path relative to the case directory")
    p.add_argument("--alg", required=True, help="algorithm name, e.g. RSA-2048, AES-128-CBC, ML-KEM-768")
    p.add_argument("--param", action="append", help="override a parameter, e.g. key_size=2048")
    p.add_argument("--anchor", action="append", help="text that appears exactly once on the usage line")
    p.add_argument("--alt", action="append", help="alternate location FILE[:ANCHOR], e.g. the config naming the algorithm")
    p.add_argument("--note")
    p.add_argument("--confirm", action="store_true", help="mark as confirmed by a human who read the code")
    p = sub.add_parser("check")
    p.add_argument("cases", nargs="*")
    p.add_argument("--no-run", action="store_true")
    p.add_argument("--allow-drafts", action="store_true")
    sub.add_parser("list")
    a = ap.parse_args()
    return {"new": cmd_new, "draft": cmd_draft, "add": cmd_add, "check": cmd_check, "list": cmd_list}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
