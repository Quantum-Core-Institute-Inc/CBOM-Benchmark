#!/usr/bin/env python3
"""Prove every corpus case is real, working code.

Exit codes: 0 every case ran and passed (or some were skipped, without --strict: the summary says
so), 1 a case failed, 4 a case was skipped under --strict. Release verification uses --strict.

Single-file tiers (1, 2, mixed, negatives): run each Python file; compile and run each Java file.
Multi-file tiers (3+): each directory under corpus/tierN/<lang>/ is one case.
  Python: runs main.py from the case directory.
  Java:   compiles everything under src/ and runs the class in src/com/acme/Main.java.

A test corpus with code that doesn't execute invites the reply "your test is wrong, not our scanner".
"""
import pyreq  # noqa: F401  (fails early on an unsupported Python)
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
MULTI_FILE_TIERS = {"tier3", "system"}


# Every [ok ] / [FAIL] / [skip] line is counted, by language, so a partial run can't read as complete.
import builtins  # noqa: E402
from collections import Counter  # noqa: E402

TALLY = {"ok": Counter(), "fail": Counter(), "skip": Counter()}
SKIP_REASONS = []


def _category(text: str) -> str:
    m = re.search(r"corpus/\S+", text)
    path = m.group(0) if m else text
    if path.startswith("corpus/system/"):
        return "System fixture"
    if "(go run)" in text or path.endswith(".go"):
        return "Go"
    if "(dotnet)" in text or path.split(" ")[0].endswith(".cs"):
        return "C#"
    if "/tier5/c/bin/" in path:
        return "C"
    for ext, cat in ((".py", "Python"), (".pyc", "Python"), (".java", "Java"), (".jar", "Java"), (".js", "JavaScript/TypeScript"),
                     (".mjs", "JavaScript/TypeScript"), (".ts", "JavaScript/TypeScript"), (".c", "C")):
        if path.split(" ")[0].endswith(ext):
            return cat
    if "/tier3/python/" in path or "/custom/" in path and "main.py" in text:
        return "Python"
    if "/tier3/java/" in path:
        return "Java"
    if "/deps/" in path:
        return "Dependency manifests"
    return "Assets and other"


def print(*args, **kw):  # noqa: A001  (counts result lines, then prints them)
    msg = " ".join(str(a) for a in args)
    for tag, key in (("[ok ]", "ok"), ("[FAIL]", "fail"), ("[skip]", "skip")):
        if msg.startswith(tag):
            TALLY[key][_category(msg)] += 1
            if key == "skip":
                SKIP_REASONS.append(msg[len(tag):].strip())
    builtins.print(*args, **kw)


def skip_many(category: str, n: int, reason: str):
    TALLY["skip"][category] += n
    SKIP_REASONS.append(f"{n} {category} case(s): {reason}")
    builtins.print(f"[skip] {n} {category} case(s): {reason}")


def run(cmd, cwd):
    # No __pycache__ in the corpus: compiled files are scannable input, and only Tier 5 ships one on purpose.
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180, env=env)


def is_multi_file(path: Path) -> bool:
    return path.relative_to(CORPUS).parts[0] in MULTI_FILE_TIERS | {"custom"}


def verify_system(failures):
    """The system fixture: each service runs from source with the shared wrapper and config, the
    built artifacts run, and every certificate and key parses."""
    sysroot = CORPUS / "system" / "payments-platform"
    if not sysroot.exists():
        return
    rel = lambda p: str(p.relative_to(ROOT))  # noqa: E731
    env_cfg = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "CRYPTO_PROFILES": str(sysroot / "config/crypto-profiles.json")}
    worker = sysroot / "services/settlement-worker/worker.py"
    report(f"{rel(worker)} (settlement-worker, with cryptokit)", run([sys.executable, worker.name], cwd=worker.parent), failures)
    if shutil.which("go"):
        r = subprocess.run(["go", "run", "./services/api-gateway"], cwd=sysroot, capture_output=True, text=True, timeout=300, env=env_cfg)
        report(f"{rel(sysroot / 'services/api-gateway')}/ (api-gateway from source, go run)", r, failures)
    else:
        skip_many("System fixture", 1, "go not found")
    binary = sysroot / "services/api-gateway/bin/api-gateway"
    import platform
    if platform.system() == "Linux" and platform.machine() in ("x86_64", "AMD64"):
        r = subprocess.run([str(binary)], cwd=sysroot, capture_output=True, text=True, timeout=60, env=env_cfg)
        report(f"{rel(binary)} (built binary)", r, failures)
    else:
        skip_many("System fixture", 1, "the gateway binary is linux/amd64")
    if shutil.which("javac"):
        srcs = [str(p) for p in (sysroot / "libs/cryptokit/java").rglob("*.java")] + \
               [str(p) for p in (sysroot / "services/ledger-service/src").rglob("*.java")]
        with tempfile.TemporaryDirectory() as out:
            c = run(["javac", "-d", out, *srcs], cwd=sysroot)
            if c.returncode == 0:
                c = run(["java", "-cp", out, "com.acme.ledger.LedgerService"], cwd=sysroot)
            report(f"{rel(sysroot / 'services/ledger-service')}/ (ledger-service from source, with cryptokit)", c, failures)
        jar = sysroot / "services/ledger-service/build/libs/ledger-service.jar"
        report(f"{rel(jar)} (built jar)", run(["java", "-cp", str(jar), "com.acme.ledger.LedgerService"], cwd=sysroot), failures)
    else:
        skip_many("System fixture", 2, "javac not found")
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization as ser
    import base64
    for label, load in (
            ("edge/nginx/tls/gateway.crt", lambda: x509.load_pem_x509_certificate((sysroot / "edge/nginx/tls/gateway.crt").read_bytes())),
            ("edge/nginx/tls/gateway.key", lambda: ser.load_pem_private_key((sysroot / "edge/nginx/tls/gateway.key").read_bytes(), None)),
            ("deploy/k8s/gateway-ingress-tls.yaml", lambda: x509.load_pem_x509_certificate(base64.b64decode(
                re.search(r"tls\.crt:\s*(\S+)", (sysroot / "deploy/k8s/gateway-ingress-tls.yaml").read_text()).group(1)))),
            ("services/settlement-worker/partner_ca.py", lambda: x509.load_pem_x509_certificates(
                (sysroot / "services/settlement-worker/partner_ca.py").read_bytes())[0])):
        try:
            load()
            print(f"[ok ] corpus/system/payments-platform/{label} (parses)")
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] corpus/system/payments-platform/{label}: {e}")
            failures.append((label, [str(e)]))


def verify_custom(failures):
    """Bring-your-own-code cases run through their manifest's run command (see BYOC.md)."""
    from byoc import run_case
    from truth import custom_manifests
    for _, m in custom_manifests():
        ok, detail = run_case(m["case"], m)
        label = f"corpus/custom/{m['case']}/ ({detail})"
        print(f"[{'ok ' if ok else 'FAIL'}] {label}")
        if not ok:
            failures.append((label, [detail]))


def report(label, proc, failures, tail=1):
    ok = proc.returncode == 0
    print(f"[{'ok ' if ok else 'FAIL'}] {label}")
    if not ok:
        failures.append((label, proc.stderr.strip().splitlines()[-tail:]))


def verify_tier4(failures):
    """Tier 4 has no code to run, so instead prove each asset parses with standard tooling."""
    import base64
    import re

    from cryptography import x509
    from cryptography.hazmat.primitives import serialization as ser
    from cryptography.hazmat.primitives.serialization import pkcs12

    a = CORPUS / "tier4" / "assets"
    if not a.exists():
        return

    def chk(label, fn):
        try:
            detail = fn()
            print(f"[ok ] {label}{': ' + detail if detail else ''}")
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {label}")
            failures.append((label, [repr(e)]))

    def certs(data):
        return ", ".join(c.signature_algorithm_oid._name for c in x509.load_pem_x509_certificates(data))

    for p in sorted((a / "certs").glob("*")):
        rel = p.relative_to(ROOT)
        if p.suffix == ".der":
            chk(rel, lambda p=p: x509.load_der_x509_certificate(p.read_bytes()).signature_algorithm_oid._name)
        else:
            chk(rel, lambda p=p: certs(p.read_bytes()))
    for name in ("billing_service.pem", "treasury_hot_wallet.key"):
        chk(f"corpus/tier4/assets/keys/{name}",
            lambda n=name: type(ser.load_pem_private_key((a / "keys" / n).read_bytes(), None)).__name__)
    chk("corpus/tier4/assets/keys/backup_signing_encrypted.pem",
        lambda: type(ser.load_pem_private_key((a / "keys" / "backup_signing_encrypted.pem").read_bytes(),
                                              b"Sup3r-Secret-Backup")).__name__ + " (password from generator)")
    chk("corpus/tier4/assets/keys/jwks.json",
        lambda: f"{len(__import__('json').loads((a / 'keys' / 'jwks.json').read_text())['keys'])} keys")
    chk("corpus/tier4/assets/keystores/orders_keystore.p12",
        lambda: type(pkcs12.load_pkcs12((a / "keystores" / "orders_keystore.p12").read_bytes(), b"changeit").key).__name__)
    jks = a / "keystores" / "partner_truststore.jks"
    if jks.exists() and shutil.which("keytool"):
        chk(jks.relative_to(ROOT), lambda: (
            "trustedCertEntry" if "trustedCertEntry" in run(
                ["keytool", "-list", "-keystore", str(jks), "-storepass", "changeit"], cwd=ROOT).stdout
            else (_ for _ in ()).throw(ValueError("no trusted cert entry"))))
    chk("corpus/tier4/assets/ssh/ssh_host_rsa_key.pub",
        lambda: f"RSA {ser.load_ssh_public_key((a / 'ssh' / 'ssh_host_rsa_key.pub').read_bytes()).key_size}")
    chk("corpus/tier4/assets/ssh/deploy_id_ed25519",
        lambda: type(ser.load_ssh_private_key((a / "ssh" / "deploy_id_ed25519").read_bytes(), None)).__name__)
    chk("corpus/tier4/assets/k8s/ingress-tls-secret.yaml", lambda: certs(base64.b64decode(
        re.search(r"tls.crt: (\S+)", (a / "k8s" / "ingress-tls-secret.yaml").read_text()).group(1))))
    fake = CORPUS / "negatives" / "assets" / "upload_validator_fake.pem"
    if fake.exists():
        def must_fail():
            try:
                x509.load_pem_x509_certificate(fake.read_bytes())
            except ValueError:
                return "correctly unparseable"
            raise ValueError("fake PEM parsed as a certificate")
        chk(fake.relative_to(ROOT), must_fail)


def verify_tier5(failures, has_java):
    """Run the compiled-only artifacts, and prove each hand-rolled algorithm is the real thing by
    checking it against a reference implementation. Without that, 'your scanner missed RC4' invites
    'that isn't RC4'."""
    import hashlib
    import importlib.util

    t5 = CORPUS / "tier5"
    if not t5.exists():
        return

    def load(name):
        spec = importlib.util.spec_from_file_location(name, t5 / "python" / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def chk(label, fn):
        try:
            detail = fn()
            print(f"[ok ] {label}{': ' + detail if detail else ''}")
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {label}")
            failures.append((label, [repr(e)]))

    def digest_matches():
        d = load("t5_handrolled_digest")
        for m in (b"", b"abc", b"x" * 55, b"x" * 56, b"x" * 64, b"y" * 1000):
            assert d.digest(m) == hashlib.sha256(m).digest(), m[:8]
        return "matches hashlib.sha256 incl. padding edge cases"

    def keystream_matches():
        from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4
        from cryptography.hazmat.primitives.ciphers import Cipher
        k = load("t5_handrolled_keystream")
        key, pt = b"partner-feed-key", b"ACCT=4471;AMT=120.00" * 7
        assert k.transform(key, pt) == Cipher(ARC4(key), mode=None).encryptor().update(pt)
        return "matches cryptography's ARC4"

    def pubkey_bits():
        n = load("t5_handrolled_pubkey").N
        assert n.bit_length() == 1024 and n % 2 == 1
        return "1024-bit odd modulus"

    chk("corpus/tier5/python/t5_handrolled_digest.py", digest_matches)
    chk("corpus/tier5/python/t5_handrolled_keystream.py", keystream_matches)
    chk("corpus/tier5/python/t5_handrolled_pubkey.py", pubkey_bits)

    pyc = t5 / "python" / "compiled" / "ledger_sync.pyc"
    if pyc.exists():
        r = run([sys.executable, str(pyc)], cwd=ROOT)
        if r.returncode and "bad magic number" in r.stderr:
            print(f"[skip] {pyc.relative_to(ROOT)}: built for another Python; run tools/build_tier5_compiled.py")
        else:
            report(f"{pyc.relative_to(ROOT)} (runs as bytecode)", r, failures)

    native = t5 / "c" / "bin" / "meterd"
    if native.exists():
        import platform
        if platform.system() == "Linux" and platform.machine() == "x86_64":
            native.chmod(0o755)
            report(f"{native.relative_to(ROOT)} (stripped binary, self-test)", run([str(native)], cwd=ROOT), failures)
        else:
            print(f"[skip] {native.relative_to(ROOT)}: an x86-64 Linux binary, and this host isn't")
    if has_java and (t5 / "java" / "compiled" / "token-vault.jar").exists():
        vault = t5 / "java" / "compiled" / "token-vault.jar"
        report(f"{vault.relative_to(ROOT)} (obfuscated, java -jar)", run(["java", "-jar", str(vault)], cwd=ROOT), failures, tail=3)
    if has_java:
        jar = t5 / "java" / "compiled" / "billing-core.jar"
        if jar.exists():
            report(f"{jar.relative_to(ROOT)} (java -jar)", run(["java", "-jar", str(jar)], cwd=ROOT), failures, tail=3)
        with tempfile.TemporaryDirectory() as out:
            c = run(["javac", "-d", out, "T5BlockTransform.java", "T5HandrolledPubkey.java"], cwd=t5 / "java")
            if c.returncode == 0:
                c = run(["java", "-cp", out, "T5BlockTransform"], cwd=t5 / "java")
            ok = c.returncode == 0 and c.stdout.strip() == "41ea3a0a 94baa940"
            print(f"[{'ok ' if ok else 'FAIL'}] corpus/tier5/java/T5BlockTransform.java: "
                  f"{'matches the published zero-key test vector' if ok else c.stdout.strip()}")
            if not ok:
                failures.append(("T5BlockTransform test vector", [c.stdout.strip(), c.stderr.strip()[-200:]]))
            c = run(["java", "-cp", out, "T5HandrolledPubkey"], cwd=t5 / "java")
            report("corpus/tier5/java/T5HandrolledPubkey.java (2048-bit modulus)", c, failures)


def bcprov_jar() -> str | None:
    """Bouncy Castle's provider jar, for the LMS and XMSS cases (the JDK has neither)."""
    for cand in (os.environ.get("BCPROV_JAR"), "/usr/share/java/bcprov.jar"):
        if cand and Path(cand).is_file():
            return cand
    return None


def verify_csharp(failures):
    """One project per case. Built with an empty package source list, so nothing is fetched: the
    cases use only the base class library."""
    projects = sorted(CORPUS.rglob("*.csproj"))
    if not projects:
        return
    if not shutil.which("dotnet"):
        skip_many("C#", len(projects), "dotnet not found")
        return
    env = dict(os.environ, DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1")
    with tempfile.TemporaryDirectory() as td:
        cfg = Path(td) / "nuget.config"
        cfg.write_text('<?xml version="1.0"?>\n<configuration><packageSources><clear/></packageSources></configuration>\n')
        for proj in projects:
            name = proj.stem
            c = subprocess.run(["dotnet", "build", str(proj.parent), "--configfile", str(cfg), "--artifacts-path", f"{td}/{name}",
                                "-p:UseAppHost=false", "-v", "q"], capture_output=True, text=True, env=env)
            if c.returncode == 0:
                c = subprocess.run(["dotnet", f"{td}/{name}/bin/{name}/debug/{name}.dll"], capture_output=True, text=True, env=env, cwd=proj.parent)
            report(f"{proj.parent.relative_to(ROOT)}/Program.cs (dotnet)", c, failures, tail=3)


def pq_java() -> str | None:
    """A Java runtime with ML-KEM / ML-DSA in the standard JCA (JDK 24+): the system 'java' if new
    enough, else the jdk4py runtime from PyPI (pip install jdk4py)."""
    r = run(["java", "-version"], cwd=ROOT) if shutil.which("java") else None
    if r is not None:
        import re
        m = re.search(r'version "(\d+)', r.stderr)
        if m and int(m.group(1)) >= 24:
            return "java"
    try:
        import jdk4py
        if jdk4py.JAVA_VERSION[0] >= 24:
            return str(jdk4py.JAVA)
    except ImportError:
        pass
    return None


def verify_pqc_assets(failures):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization as ser

    a = CORPUS / "pqc" / "assets"
    if not a.exists():
        return
    for p in sorted((a / "certs").glob("*.pem")):
        try:
            c = x509.load_pem_x509_certificate(p.read_bytes())
            print(f"[ok ] {p.relative_to(ROOT)}: key {type(c.public_key()).__name__.replace('PublicKey', '')}, "
                  f"signed {c.signature_algorithm_oid._name}")
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {p.relative_to(ROOT)}")
            failures.append((str(p), [repr(e)]))
    # Stateful hash-based keys: no Python library here parses them, so check the algorithm OID in the SPKI.
    import base64
    for name, oid_der, what in (("bootloader_lms_pub.pem", bytes.fromhex("060b2a864886f70d0109100311"), "HSS/LMS (1.2.840.113549.1.9.16.3.17)"),
                                ("update_xmss_pub.pem", bytes.fromhex("060904007f000f01010d00"), "XMSS (0.4.0.127.0.15.1.1.13.0)")):
        p = a / "keys" / name
        der = base64.b64decode("".join(ln for ln in p.read_text().splitlines() if not ln.startswith("-----")))
        ok = der[0] == 0x30 and der[2] == 0x30 and der[4:4 + len(oid_der)] == oid_der
        print(f"[{'ok ' if ok else 'FAIL'}] {p.relative_to(ROOT)}: SPKI algorithm {what}")
        if not ok:
            failures.append((str(p), ["SPKI algorithm identifier is not the expected OID"]))
    for p, loader in ((a / "keys" / "kem_recipient_pub.pem", lambda b: ser.load_pem_public_key(b)),
                      (a / "keys" / "attestation_signer.pem", lambda b: ser.load_pem_private_key(b, None))):
        try:
            print(f"[ok ] {p.relative_to(ROOT)}: {type(loader(p.read_bytes())).__name__}")
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {p.relative_to(ROOT)}")
            failures.append((str(p), [repr(e)]))


def verify_go_node_c(failures):
    """Go cases are one directory per program under a go.mod; Node runs .js/.mjs and, from 22.18,
    .ts directly (type stripping); C links against the system OpenSSL 3 (libssl, libcrypto)."""
    if shutil.which("go"):
        for mod in sorted(m for m in CORPUS.rglob("go.mod") if "system" not in m.relative_to(CORPUS).parts[:1]):
            for case in sorted(p for p in mod.parent.iterdir() if p.is_dir()):
                report(f"{case.relative_to(ROOT)}/ (go run)", run(["go", "run", f"./{case.name}"], cwd=mod.parent), failures)
    else:
        skip_many("Go", sum(1 for m in CORPUS.rglob("go.mod") if "system" not in m.relative_to(CORPUS).parts[:1]
                            for p in m.parent.iterdir() if p.is_dir()), "go not found")
    if shutil.which("node"):
        for js in sorted(p for ext in ("*.js", "*.mjs", "*.ts") for p in CORPUS.rglob(ext)):
            report(js.relative_to(ROOT), run(["node", js.name], cwd=js.parent), failures)
    else:
        skip_many("JavaScript/TypeScript", sum(1 for e in ("*.js", "*.mjs", "*.ts") for _ in CORPUS.rglob(e)), "node not found")
    cc = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if cc:
        for c_src in sorted(CORPUS.rglob("*.c")):
            with tempfile.TemporaryDirectory() as out:
                exe = str(Path(out) / "case")
                c = run([cc, "-Wall", "-Werror", c_src.name, "-o", exe, "-lssl", "-lcrypto"], cwd=c_src.parent)
                if c.returncode == 0:
                    c = run([exe], cwd=c_src.parent)
                report(f"{c_src.relative_to(ROOT)} (cc + OpenSSL 3)", c, failures, tail=3)
    else:
        skip_many("C", sum(1 for _ in CORPUS.rglob("*.c")), "no C compiler found")


def verify_manifests(failures):
    """corpus/deps/: every manifest parses with its ecosystem's own rules, and lists what the answer
    key (expected/libraries.json) says it lists."""
    import json as _json
    import re
    import tomllib
    import xml.etree.ElementTree as ET
    deps = CORPUS / "deps"
    if not deps.exists():
        return

    def check(label, fn):
        try:
            fn()
            print(f"[ok ] {label}")
        except Exception as e:  # noqa: BLE001
            failures.append((label, [str(e)[:300]]))
            print(f"[FAIL] {label}: {e}")

    def requirements(p):
        from packaging.requirements import Requirement
        for line in p.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                Requirement(line)

    def pyproject(p):
        from packaging.requirements import Requirement
        for r in tomllib.loads(p.read_text())["project"]["dependencies"]:
            Requirement(r)

    def pom(p):
        ns = {"m": "http://maven.apache.org/POM/4.0.0"}
        root = ET.parse(p).getroot()
        props = {c.tag.split("}")[1]: c.text for c in root.find("m:properties", ns) or []}
        for d in root.iterfind("m:dependencies/m:dependency", ns):
            v = d.findtext("m:version", namespaces=ns) or ""
            for ref in re.findall(r"\$\{([^}]+)\}", v):
                if ref not in props:
                    raise ValueError(f"undefined property {ref}")

    def gradle(p):
        coords = re.findall(r"(?:implementation|api|testImplementation)\s+'([^':]+:[^':]+:[^']+)'", p.read_text())
        if not coords:
            raise ValueError("no dependency coordinates")

    def npm(p):
        pkg = _json.loads(p.read_text())
        lock = _json.loads((p.parent / "package-lock.json").read_text())
        missing = [d for d in pkg.get("dependencies", {}) if f"node_modules/{d}" not in lock["packages"]]
        if missing:
            raise ValueError(f"lockfile lacks {missing}")

    def gomod(p):
        r = run(["go", "mod", "edit", "-json", p.name], cwd=p.parent)
        if r.returncode:
            raise ValueError(r.stderr.strip()[-200:])
        _json.loads(r.stdout)

    def conan(p):
        sections = re.findall(r"^\[(\w+)\]", p.read_text(), re.M)
        if "requires" not in sections:
            raise ValueError("no [requires] section")

    handlers = {"requirements.txt": requirements, "pyproject.toml": pyproject, "pom.xml": pom, "build.gradle": gradle,
                "package.json": npm, "go.mod": gomod, "conanfile.txt": conan}
    for p in sorted(deps.rglob("*")):
        if p.name == "go.mod" and p.name in handlers and not shutil.which("go"):
            print(f"[skip] {p.relative_to(ROOT)}: go not found")
            continue
        if p.name in handlers:
            check(f"{p.relative_to(ROOT)} (parses)", lambda p=p: handlers[p.name](p))
    exp = ROOT / "expected" / "libraries.json"
    if exp.exists():
        def listed():
            bad = []
            for e in _json.loads(exp.read_text())["libraries"]:
                text = (ROOT / e["file"]).read_text().lower()
                for pkg in (x.strip().split(":")[-1] for x in e["package"].split(",")):
                    if pkg.lower() not in text:
                        bad.append(f"{e['id']}: {pkg} not in {e['file']}")
            if bad:
                raise ValueError("; ".join(bad))
        check("expected/libraries.json matches the manifests", listed)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--summary-json", help="also write the pass/fail/skip counts per area to this file")
    ap.add_argument("--strict", action="store_true",
                    help="a skipped case is a failure (release verification: every case must run)")
    args = ap.parse_args()
    failures = []
    has_java = shutil.which("javac") is not None
    if not has_java:
        skip_many("Java", sum(1 for j in CORPUS.rglob("*.java") if not is_multi_file(j))
                  + sum(1 for t in MULTI_FILE_TIERS for _ in (CORPUS / t / "java").glob("*/")), "javac not found")
    java25 = pq_java() if has_java else None

    for py in sorted(CORPUS.rglob("*.py")):
        if is_multi_file(py):
            continue
        report(py.relative_to(ROOT), run([sys.executable, py.name], cwd=py.parent), failures)

    if has_java:
        for java in sorted(CORPUS.rglob("*.java")):
            if is_multi_file(java):
                continue
            if "org.bouncycastle" in java.read_text():
                bc = bcprov_jar()
                if bc is None:
                    print(f"[skip] {java.relative_to(ROOT)}: needs Bouncy Castle (apt install libbcprov-java, or set BCPROV_JAR)")
                    continue
                with tempfile.TemporaryDirectory() as out:
                    c = run(["javac", "-cp", bc, "-d", out, java.name], cwd=java.parent)
                    if c.returncode == 0:
                        c = run(["java", "-cp", f"{out}{os.pathsep}{bc}", java.stem], cwd=java.parent)
                    report(f"{java.relative_to(ROOT)} (Bouncy Castle)", c, failures, tail=3)
                continue
            needs_pq = java.relative_to(CORPUS).parts[0] == "pqc" or (
                java.relative_to(CORPUS).parts[0] == "mixed" and re.search(r'"ML-(KEM|DSA)', java.read_text()))
            if needs_pq and java25 is None:
                print(f"[skip] {java.relative_to(ROOT)}: needs a JDK 24+ runtime (pip install jdk4py)")
                continue
            with tempfile.TemporaryDirectory() as out:
                c = run(["javac", "-d", out, java.name], cwd=java.parent)
                if c.returncode == 0:
                    c = run([java25 if needs_pq else "java", "-cp", out, java.stem], cwd=java.parent)
                label = f"{java.relative_to(ROOT)}{' (Java 24+ runtime)' if needs_pq else ''}"
                report(label, c, failures, tail=3)

    for tier in sorted(MULTI_FILE_TIERS):
        for case in sorted((CORPUS / tier / "python").glob("*/")):
            report(f"{case.relative_to(ROOT)}/ (main.py)",
                   run([sys.executable, "main.py"], cwd=case), failures, tail=3)
        if has_java:
            for case in sorted((CORPUS / tier / "java").glob("*/")):
                sources = [str(p.relative_to(case)) for p in sorted((case / "src").rglob("*.java"))]
                with tempfile.TemporaryDirectory() as out:
                    c = run(["javac", "-d", out, *sources], cwd=case)
                    if c.returncode == 0:
                        c = run(["java", "-cp", out, "com.acme.Main"], cwd=case)
                    report(f"{case.relative_to(ROOT)}/ ({len(sources)} classes)", c, failures, tail=3)

    verify_go_node_c(failures)
    verify_manifests(failures)
    verify_tier4(failures)
    verify_csharp(failures)
    verify_tier5(failures, has_java)
    verify_pqc_assets(failures)
    verify_custom(failures)
    verify_system(failures)

    for d in CORPUS.rglob("__pycache__"):  # nothing compiled may be left behind in the corpus
        shutil.rmtree(d, ignore_errors=True)
    cats = sorted(set(TALLY["ok"]) | set(TALLY["fail"]) | set(TALLY["skip"]))
    builtins.print("\n| Area | Passed | Failed | Skipped |\n|---|---|---|---|")
    for c in cats:
        builtins.print(f"| {c} | {TALLY['ok'][c]} | {TALLY['fail'][c]} | {TALLY['skip'][c]} |")
    n_ok, n_fail, n_skip = (sum(TALLY[k].values()) for k in ("ok", "fail", "skip"))
    builtins.print(f"| **Total** | {n_ok} | {n_fail} | {n_skip} |")
    if args.summary_json:
        import json
        Path(args.summary_json).write_text(json.dumps({
            "areas": {c: {"passed": TALLY["ok"][c], "failed": TALLY["fail"][c], "skipped": TALLY["skip"][c]} for c in cats},
            "total": {"passed": n_ok, "failed": n_fail, "skipped": n_skip},
            "failures": [lbl for lbl, _ in failures], "skip_reasons": list(SKIP_REASONS)}, indent=2) + "\n")
    if failures:
        builtins.print(f"\n{len(failures)} case(s) failed:")
        for label, err in failures:
            builtins.print(f"  {label}: {' | '.join(err)}")
    if n_skip:
        builtins.print(f"\n{n_skip} case(s) skipped, so this is NOT a complete verification:")
        for r in SKIP_REASONS:
            builtins.print(f"  {r}")
    if failures:
        return 1
    if n_skip:
        return 4 if args.strict else 0
    builtins.print(f"\nAll {n_ok} corpus cases execute (0 failed, 0 skipped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
