"""Holdout generators for what the code generators can't reach: certificates, keys and keystores
with random algorithms and containers, TLS and SSH configs with random protocol and suite lists,
and compiled artifacts (.pyc, .jar) with no source alongside.

Every file is real: certificates and keys are made with `cryptography`, configs use the same
spellings the published Tier 4 does, and the artifacts are compiled from generated programs that
are run once before the source is thrown away. File names say nothing about the algorithm.

Truth conventions match the published corpus: one finding per (file, family); certificates yield
the key's family and the signature's hash; config tokens are expected exactly as the normalizer
reads them (cbomlib.normalize), so a config here means what the same line means in Tier 4.
Post-quantum families go to the holdout-pqc tier (lang "assets"), everything else to holdout-t4;
artifacts go to holdout-t5 (lang python / java).
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, mldsa, rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID

from cbomlib import FAMILIES, normalize

PEM, DER = serialization.Encoding.PEM, serialization.Encoding.DER
# also_ok, as in the published Tier 4 and PQC configs: the parts inside a suite or a key-exchange name
SUITE_PARTS = ["RSA", "EC", "DH", "AES", "3DES", "ChaCha20-Poly1305", "SHA-1", "SHA-256", "SHA-384", "HMAC"]
SSH_PARTS = ["SHA-1", "SHA-256", "SHA-512"]
CURVES = {"P-256": ec.SECP256R1, "P-384": ec.SECP384R1, "P-521": ec.SECP521R1}
HASHES = {"SHA-256": hashes.SHA256, "SHA-384": hashes.SHA384, "SHA-512": hashes.SHA512}
WORDS = ("orders billing portal ledger partner device telemetry edge gateway vault archive relay "
         "payroll claims audit treasury signer ingest search").split()


def _cn(rng):
    return f"{rng.choice(WORDS)}-{rng.choice(WORDS)}.example.internal"


def _key(rng, allow=("RSA", "EC", "Ed25519")):
    fam = rng.choice(allow)
    if fam == "RSA":
        bits = rng.choice([1024, 2048, 2048, 3072, 4096])
        return rsa.generate_private_key(public_exponent=65537, key_size=bits), "RSA", {"key_size": bits}
    if fam == "EC":
        c = rng.choice(list(CURVES))
        return ec.generate_private_key(CURVES[c]()), "EC", {"curve": c}
    return ed25519.Ed25519PrivateKey.generate(), "Ed25519", {}


def _cert(rng, subject_key, issuer_key=None, sha1=False, ca=False):
    """-> (certificate, signature hash family or None)"""
    import generate_tier4_assets as g4
    issuer_key = issuer_key or subject_key
    h = rng.choice(list(HASHES))
    cn = _cn(rng)
    nb = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(days=rng.randint(0, 300))
    b = (x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)]))
         .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn if issuer_key is subject_key else "Issuing CA")]))
         .public_key(subject_key.public_key()).serial_number(x509.random_serial_number())
         .not_valid_before(nb).not_valid_after(nb + dt.timedelta(days=rng.choice([90, 397, 825, 3650])))
         .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True))
    if isinstance(issuer_key, (ed25519.Ed25519PrivateKey, mldsa.MLDSA65PrivateKey, mldsa.MLDSA44PrivateKey,
                               mldsa.MLDSA87PrivateKey)):
        return b.sign(issuer_key, None), None
    c = b.sign(issuer_key, HASHES[h]() if not sha1 else hashes.SHA256())
    if sha1 and isinstance(issuer_key, rsa.RSAPrivateKey):
        return g4.resign_sha1(c, issuer_key), "SHA-1"
    return c, h if not sha1 else "SHA-256"


def _config_findings(lines: list[str], tokens: list[tuple[str, int]]) -> list[tuple[str, dict, int]]:
    """tokens: (spelling, line) -> [(family, params, line)], first spelling of a family wins."""
    out, seen = [], set()
    for tok, ln in tokens:
        fam, params = normalize(tok)
        # same convention as Tier 4: a hash rides along only where it's the parameter that matters
        params = {k: v for k, v in params.items() if k != "hash" or fam in ("HMAC", "PBKDF2")}
        if fam in FAMILIES and fam not in seen:
            seen.add(fam)
            out.append((fam, params, ln))
    return out


class AssetSet:
    """Collects files and findings for one holdout set."""

    def __init__(self, out: Path, rng, tag, fid_for, published: dict | None = None):
        self.out, self.rng, self.tag, self.fid_for = Path(out), rng, tag, fid_for
        self.pub = published or {}
        self.findings, self.also_ok, self.n = [], [], 0

    def _write(self, rel, data):
        p = self.out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        (p.write_bytes if isinstance(data, bytes) else p.write_text)(data)

    def _rel(self, sub, ext):
        self.n += 1
        return f"corpus/holdout-t4/assets/{sub}/{self.rng.choice(WORDS)}_{self.tag(30_000 + self.n)}{ext}"

    def add(self, rel, family, params, lines=(), lang="assets", tier=None):
        if any(f["file"] == rel and f["family"] == family for f in self.findings):
            return
        # A finding feeds the overfit gap only where the published corpus has the same (tier, language,
        # family) cell; anything else the generator explores is scored as holdout-broad.
        if tier is None:
            if family in self.pub.get((4, "assets"), ()):
                tier = "holdout-t4"
            elif family in self.pub.get(("pqc", "assets"), ()):
                tier = "holdout-pqc"
            else:
                tier = "holdout-broad"
        elif tier == "holdout-t5" and family not in self.pub.get((5, lang), ()):
            tier = "holdout-broad"
        self.findings.append({"id": self.fid_for("assets"), "tier": tier, "lang": lang, "file": rel,
                              "family": family, "params": params, "lines": sorted(set(lines))})

    # -- certificates and keys -------------------------------------------------------------------
    def certificate(self):
        rng = self.rng
        k, fam, params = _key(rng)
        kind = rng.choice(["pem", "pem", "der", "chain", "k8s", "p12"])
        sha1 = isinstance(k, rsa.RSAPrivateKey) and rng.random() < 0.25
        if kind == "chain":
            ca_key, ca_fam, ca_params = _key(rng, allow=[x for x in ("RSA", "EC") if x != fam] or ["RSA"])
            leaf, h = _cert(rng, k, issuer_key=ca_key)
            ca, ca_h = _cert(rng, ca_key, ca=True)
            rel = self._rel("certs", rng.choice([".pem", ".crt"]))
            self._write(rel, leaf.public_bytes(PEM) + ca.public_bytes(PEM))
            for f_, p_ in ((fam, params), (ca_fam, ca_params)):
                self.add(rel, f_, p_)
            for hh in {h, ca_h} - {None}:
                self.add(rel, hh, {})
            return
        c, h = _cert(rng, k, sha1=sha1)
        if kind == "pem":
            rel = self._rel("certs", rng.choice([".pem", ".crt", ".cer"]))
            self._write(rel, c.public_bytes(PEM))
        elif kind == "der":
            rel = self._rel("certs", ".der")
            self._write(rel, c.public_bytes(DER))
        elif kind == "k8s":
            rel = self._rel("k8s", ".yaml")
            crt = base64.b64encode(c.public_bytes(PEM)).decode()
            self._write(rel, f"apiVersion: v1\nkind: Secret\nmetadata:\n  name: {rng.choice(WORDS)}-tls\n"
                             f"type: kubernetes.io/tls\ndata:\n  tls.crt: {crt}\n  tls.key: \"\"\n")
        else:  # PKCS#12 with the key: AES-256-CBC and PBKDF2-SHA256 protect it
            if isinstance(k, ed25519.Ed25519PrivateKey):
                k, fam, params = rsa.generate_private_key(public_exponent=65537, key_size=2048), "RSA", {"key_size": 2048}
                c, h = _cert(rng, k)
            rel = self._rel("keystores", ".p12")
            enc = (serialization.PrivateFormat.PKCS12.encryption_builder().kdf_rounds(rng.choice([2048, 10000, 50000]))
                   .key_cert_algorithm(pkcs12.PBES.PBESv2SHA256AndAES256CBC).hmac_hash(hashes.SHA256()).build(b"changeit"))
            self._write(rel, pkcs12.serialize_key_and_certificates(b"alias", k, c, None, enc))
            self.add(rel, "AES", {"key_size": 256, "mode": "CBC"})
            self.add(rel, "PBKDF2", {"hash": "SHA-256"})
        self.add(rel, fam, params)
        if h:
            self.add(rel, h, {})

    def pq_certificate(self):
        rng = self.rng
        ps = rng.choice(["44", "65", "87"])
        k = {"44": mldsa.MLDSA44PrivateKey, "65": mldsa.MLDSA65PrivateKey, "87": mldsa.MLDSA87PrivateKey}[ps].generate()
        c, _ = _cert(rng, k)
        rel = self._rel("certs", ".pem")
        self._write(rel, c.public_bytes(PEM))
        self.add(rel, "ML-DSA", {"param_set": ps})

    def key_file(self):
        rng = self.rng
        k, fam, params = _key(rng)
        kind = rng.choice(["traditional", "pkcs8", "encrypted", "public", "openssh", "openssh-pub", "jwks"])
        if kind == "traditional" and isinstance(k, ed25519.Ed25519PrivateKey):
            kind = "pkcs8"
        if kind == "jwks":
            return self.jwks()
        if kind == "openssh-pub":
            rel = self._rel("ssh", ".pub")
            self._write(rel, k.public_key().public_bytes(serialization.Encoding.OpenSSH,
                                                         serialization.PublicFormat.OpenSSH).decode() + f" deploy@{rng.choice(WORDS)}\n")
        elif kind == "openssh":
            rel = self._rel("ssh", "")
            self._write(rel, k.private_bytes(PEM, serialization.PrivateFormat.OpenSSH, serialization.NoEncryption()))
        elif kind == "public":
            rel = self._rel("keys", ".pem")
            self._write(rel, k.public_key().public_bytes(PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
        else:
            rel = self._rel("keys", rng.choice([".pem", ".key"]))
            fmt = serialization.PrivateFormat.TraditionalOpenSSL if kind == "traditional" else serialization.PrivateFormat.PKCS8
            enc = serialization.BestAvailableEncryption(b"changeit") if kind == "encrypted" else serialization.NoEncryption()
            self._write(rel, k.private_bytes(PEM, fmt, enc))
            if kind == "encrypted":
                self.add(rel, "AES", {"key_size": 256, "mode": "CBC"})
                self.add(rel, "PBKDF2", {"hash": "SHA-256"})
        self.add(rel, fam, params)

    def jwks(self):
        rng = self.rng
        keys, lines, entries = [], [], []
        for fam in rng.sample(["RSA", "EC"], 2):
            kid = f"{rng.choice(WORDS)}-{self.tag(40_000 + self.n + len(keys))}"
            if fam == "RSA":
                bits = rng.choice([2048, 3072, 4096])
                n = rsa.generate_private_key(public_exponent=65537, key_size=bits).public_key().public_numbers().n
                keys.append({"kty": "RSA", "kid": kid, "use": "sig", "alg": f"RS{rng.choice([256, 384, 512])}",
                             "n": base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big")).rstrip(b"=").decode(),
                             "e": "AQAB"})
                entries.append(("RSA", {"key_size": bits}, kid))
            else:
                crv = rng.choice(["P-256", "P-384"])
                pub = ec.generate_private_key(CURVES[crv]()).public_key().public_numbers()
                size = 32 if crv == "P-256" else 48
                b64 = lambda v: base64.urlsafe_b64encode(v.to_bytes(size, "big")).rstrip(b"=").decode()  # noqa: E731
                keys.append({"kty": "EC", "kid": kid, "use": "sig", "crv": crv, "x": b64(pub.x), "y": b64(pub.y)})
                entries.append(("EC", {"curve": crv}, kid))
        rel = self._rel("keys", ".json")
        text = json.dumps({"keys": keys}, indent=2) + "\n"
        self._write(rel, text)
        tl = text.splitlines()
        for fam, params, kid in entries:
            self.add(rel, fam, params, [next(i for i, t in enumerate(tl, 1) if f'"kid": "{kid}"' in t)])

    # -- configs -----------------------------------------------------------------------------------
    def nginx(self, pq=False):
        rng = self.rng
        protos = sorted(rng.sample(["TLSv1", "TLSv1.1", "TLSv1.2", "TLSv1.3"], rng.randint(1, 3)), key=lambda p: p)
        from cbomlib import CIPHER_SUITES
        pool = [s for s in CIPHER_SUITES if not s.startswith("TLS_AES") and not s.startswith("TLS_CHACHA")]
        suites = rng.sample(pool, rng.randint(1, 3))
        groups = (["X25519MLKEM768", "X25519"] if pq else rng.sample(["X25519", "secp384r1", "prime256v1"], rng.randint(0, 2)))
        lines = ["server {", "    listen 443 ssl;", f"    server_name {_cn(rng)};",
                 f"    ssl_certificate /etc/nginx/tls/{rng.choice(WORDS)}.crt;",
                 f"    ssl_certificate_key /etc/nginx/tls/{rng.choice(WORDS)}.key;"]
        if rng.random() < 0.5:
            lines += ["    # previous policy, kept for the audit trail:", "    # ssl_protocols SSLv3 TLSv1;"]
        p_ln = len(lines) + 1
        lines.append(f"    ssl_protocols {' '.join(protos)};")
        s_ln = len(lines) + 1
        lines.append(f"    ssl_ciphers {':'.join(CIPHER_SUITES[s] for s in suites)};")
        g_ln = None
        if groups:
            g_ln = len(lines) + 1
            lines.append(f"    ssl_ecdh_curve {':'.join(groups)};")
        lines += ["    location / {", f"        proxy_pass http://{rng.choice(WORDS)}_upstream;", "    }", "}"]
        rel = self._rel("tls", ".conf")
        self._write(rel, "\n".join(lines) + "\n")
        self.also_ok.append({"file": rel, "families": SUITE_PARTS + (["ML-KEM"] if pq else [])})
        toks = [(p, p_ln) for p in protos] + [(CIPHER_SUITES[s], s_ln) for s in suites] + [(g, g_ln) for g in groups]
        for fam, params, ln in _config_findings(lines, toks):
            self.add(rel, fam, params, [ln])

    def openssl_cnf(self):
        rng = self.rng
        minp = rng.choice(["TLSv1", "TLSv1.1", "TLSv1.2", "TLSv1.3"])
        bits = rng.choice([1024, 2048, 3072, 4096])
        md = rng.choice(["sha1", "sha256", "sha384", "sha512"])
        lines = ["# Build-image OpenSSL configuration", "", "openssl_conf = openssl_init", "", "[openssl_init]",
                 "ssl_conf = ssl_sect", "", "[ssl_sect]", "system_default = system_default_sect", "",
                 "[system_default_sect]", f"MinProtocol = {minp}", "CipherString = DEFAULT@SECLEVEL=1", "",
                 "[ req ]", f"default_bits       = {bits}", f"default_md         = {md}",
                 "distinguished_name = req_distinguished_name", "prompt             = no", "",
                 "[ req_distinguished_name ]", f"CN = {_cn(rng)}"]
        rel = self._rel("tls", ".cnf")
        self._write(rel, "\n".join(lines) + "\n")
        self.also_ok.append({"file": rel, "families": ["TLS-1.1", "TLS-1.2", "TLS-1.3"]})
        self.add(rel, normalize(minp)[0], {}, [12])
        self.add(rel, "RSA", {"key_size": bits}, [16])
        self.add(rel, normalize(md)[0], {}, [17])

    def spring(self):
        rng = self.rng
        from cbomlib import CIPHER_SUITES
        protos = sorted(rng.sample(["TLSv1", "TLSv1.1", "TLSv1.2", "TLSv1.3"], rng.randint(1, 2)))
        suites = rng.sample(list(CIPHER_SUITES), rng.randint(1, 3))
        lines = ["spring:", "  application:", f"    name: {rng.choice(WORDS)}-service", "", "server:", "  port: 8443",
                 "  ssl:", "    enabled: true", f"    key-store: classpath:{rng.choice(WORDS)}.p12",
                 f"    enabled-protocols: {','.join(protos)}", "    ciphers:"] + [f"      - {s}" for s in suites]
        rel = self._rel("tls", ".yml")
        self._write(rel, "\n".join(lines) + "\n")
        self.also_ok.append({"file": rel, "families": SUITE_PARTS})
        toks = [(p, 10) for p in protos] + [(s, 12 + i) for i, s in enumerate(suites)]
        for fam, params, ln in _config_findings(lines, toks):
            self.add(rel, fam, params, [ln])

    def sshd(self, pq=False):
        rng = self.rng
        hostkeys = rng.sample(["ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp256"], rng.randint(1, 2))
        kex = rng.sample(["diffie-hellman-group14-sha1", "curve25519-sha256"], rng.randint(1, 2))
        if pq:
            kex = [rng.choice(["mlkem768x25519-sha256", "sntrup761x25519-sha512@openssh.com"])] + kex
        ciphers = [rng.choice(["aes128-cbc", "aes256-ctr", "aes256-gcm@openssh.com", "3des-cbc"])]
        ciphers += rng.sample(["chacha20-poly1305@openssh.com"], rng.randint(0, 1))
        macs = [rng.choice(["hmac-sha1", "hmac-sha2-256", "hmac-sha2-512-etm@openssh.com"])]
        lines = [f"# {rng.choice(WORDS)} bastion", "", "Port 22", f"HostKeyAlgorithms {','.join(hostkeys)}",
                 f"KexAlgorithms {','.join(kex)}", f"Ciphers {','.join(ciphers)}", f"MACs {','.join(macs)}", "",
                 "PermitRootLogin no", "PasswordAuthentication no"]
        rel = self._rel("ssh", "_sshd_config")
        self._write(rel, "\n".join(lines) + "\n")
        self.also_ok.append({"file": rel, "families": SSH_PARTS + (["ML-KEM", "X25519"] if pq else [])})
        toks = [(h, 4) for h in hostkeys] + [(k, 5) for k in kex] + [(c, 6) for c in ciphers] + [(m, 7) for m in macs]
        for fam, params, ln in _config_findings(lines, toks):
            self.add(rel, fam, params, [ln])


# -- compiled artifacts -------------------------------------------------------------------------
PY_ART = {  # family -> (params, statement)
    "SHA-1": ({}, "digest = hashlib.sha1(payload).hexdigest()"),
    "MD5": ({}, "digest = hashlib.md5(payload).hexdigest()"),
    "SHA-256": ({}, "digest = hashlib.sha256(payload).hexdigest()"),
    "HMAC": ({"hash": "MD5"}, "tag = hmac.new(b'k' * 16, payload, hashlib.md5).hexdigest()"),
}
JAVA_ART = {
    "AES": ({"key_size": 128, "mode": "CBC"},
            ['KeyGenerator kg = KeyGenerator.getInstance("AES");', "kg.init(128);",
             'Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");',
             "c.init(Cipher.ENCRYPT_MODE, kg.generateKey(), new IvParameterSpec(new byte[16]));",
             "System.out.println(c.doFinal(payload).length);"]),
    "RSA": ({"key_size": 1024},
            ['KeyPairGenerator g = KeyPairGenerator.getInstance("RSA");', "g.initialize(1024);",
             "System.out.println(g.generateKeyPair().getPublic().getEncoded().length);"]),
    "SHA-1": ({}, ['System.out.println(MessageDigest.getInstance("SHA-1").digest(payload).length);']),
    "DES": ({"mode": "CBC"},
            ['SecretKey k = KeyGenerator.getInstance("DES").generateKey();',
             'Cipher d = Cipher.getInstance("DES/CBC/PKCS5Padding");',
             "d.init(Cipher.ENCRYPT_MODE, k, new IvParameterSpec(new byte[8]));",
             "System.out.println(d.doFinal(payload).length);"]),
}


def artifacts(aset: AssetSet, n_py: int, n_java: int) -> list[str]:
    """Compile generated programs into .pyc / .jar under corpus/holdout-t5/. -> problems"""
    rng, problems = aset.rng, []
    work = Path(tempfile.mkdtemp(prefix="cbom-art-"))
    try:
        for j in range(n_py):
            fams = rng.sample(list(PY_ART), rng.randint(1, 2))
            mod = f"{rng.choice(WORDS)}_{aset.tag(50_000 + j)}"
            body = ["import hashlib", "import hmac", "", "payload = b'" + rng.choice(WORDS) + "-batch'"]
            body += [PY_ART[f][1] for f in fams] + ["print('ok')"]
            src = work / f"{mod}.py"
            src.write_text("\n".join(body) + "\n")
            rel = f"corpus/holdout-t5/python/compiled/{mod}.pyc"
            dst = aset.out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            py_compile.compile(str(src), cfile=str(dst), doraise=True)
            for f in fams:
                aset.add(rel, f, PY_ART[f][0], lang="python", tier="holdout-t5")
        if shutil.which("javac") and shutil.which("jar"):
            for j in range(n_java):
                fams = rng.sample(list(JAVA_ART), rng.randint(1, 3))
                cls = f"{rng.choice(WORDS).title()}{aset.tag(60_000 + j).upper()}"
                src_dir = work / f"j{j}" / "com" / "acme" / "jobs"
                src_dir.mkdir(parents=True)
                body = ["package com.acme.jobs;", "", "import java.security.*;", "import javax.crypto.*;",
                        "import javax.crypto.spec.IvParameterSpec;", "", f"public class {cls} {{",
                        "    public static void main(String[] args) throws Exception {",
                        f'        byte[] payload = "{rng.choice(WORDS)}-batch".getBytes();']
                for f in fams:
                    body += ["        " + s for s in JAVA_ART[f][1]]
                body += ["    }", "}"]
                (src_dir / f"{cls}.java").write_text("\n".join(body) + "\n")
                classes = work / f"j{j}" / "classes"
                r = subprocess.run(["javac", "-g:none", "-d", str(classes), str(src_dir / f"{cls}.java")], capture_output=True, text=True)
                if r.returncode:
                    problems.append(f"javac {cls}: {r.stderr[-200:]}")
                    continue
                rel = f"corpus/holdout-t5/java/compiled/{rng.choice(WORDS)}-{aset.tag(61_000 + j)}.jar"
                dst = aset.out / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                r = subprocess.run(["jar", "--create", "--date=2026-01-01T00:00:00Z", "--file", str(dst),
                                    "--main-class", f"com.acme.jobs.{cls}", "-C", str(classes), "."], capture_output=True, text=True)
                if r.returncode:
                    problems.append(f"jar {cls}: {r.stderr[-200:]}")
                    continue
                for f in fams:
                    aset.add(rel, f, JAVA_ART[f][0], lang="java", tier="holdout-t5")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return problems


def generate(out: Path, rng, tag, fid_for, n_certs=10, n_keys=8, n_configs=8, n_pq=4, n_py=3, n_java=3,
             published: dict | None = None) -> dict:
    aset = AssetSet(out, rng, tag, fid_for, published)
    for _ in range(n_certs):
        aset.certificate()
    for _ in range(n_keys):
        aset.key_file()
    makers = [aset.nginx, aset.openssl_cnf, aset.spring, aset.sshd]
    for j in range(n_configs):
        makers[j % len(makers)]()
    for j in range(n_pq):
        [aset.pq_certificate, lambda: aset.nginx(pq=True), lambda: aset.sshd(pq=True)][j % 3]()
    problems = artifacts(aset, n_py, n_java)
    return {"findings": aset.findings, "also_ok": aset.also_ok, "problems": problems}


def verify(out: Path, findings: list[dict]) -> list[str]:
    """Every certificate, key and keystore parses; every artifact runs."""
    import assetfacts as af  # noqa: F401  (same loaders the answer key uses)
    fails = []
    files = sorted({f["file"] for f in findings if f["file"].startswith(("corpus/holdout-t4/", "corpus/holdout-t5/"))})
    for rel in files:
        p = Path(out) / rel
        try:
            data = p.read_bytes()
            if p.suffix == ".pyc":
                r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, timeout=60)
                if r.returncode:
                    fails.append(f"{rel}: {r.stderr.strip()[-160:]}")
            elif p.suffix == ".jar":
                r = subprocess.run(["java", "-jar", str(p)], capture_output=True, text=True, timeout=120)
                if r.returncode:
                    fails.append(f"{rel}: {r.stderr.strip()[-160:]}")
            elif p.suffix == ".der":
                x509.load_der_x509_certificate(data)
            elif p.suffix == ".p12":
                pkcs12.load_key_and_certificates(data, b"changeit")
            elif p.suffix in (".yaml",):
                import re
                x509.load_pem_x509_certificates(base64.b64decode(re.search(rb"tls\.crt:\s*(\S+)", data).group(1)))
            elif b"BEGIN CERTIFICATE" in data:
                x509.load_pem_x509_certificates(data)
            elif b"OPENSSH PRIVATE KEY" in data:
                serialization.load_ssh_private_key(data, None)
            elif p.suffix == ".pub":
                serialization.load_ssh_public_key(data.split(b" deploy@")[0])
            elif b"PUBLIC KEY" in data:
                serialization.load_pem_public_key(data)
            elif b"PRIVATE KEY" in data:
                serialization.load_pem_private_key(data, b"changeit" if b"ENCRYPTED" in data else None)
            elif p.suffix == ".json":
                json.loads(data)
        except Exception as e:  # noqa: BLE001
            fails.append(f"{rel}: {type(e).__name__}: {e}")
    return fails
