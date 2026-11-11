"""Shared helpers: algorithm-name normalization, family metadata, CycloneDX 1.6 CBOM I/O.

Scanners name the same thing a dozen ways ("SHA1withRSA", "RSASSA-PKCS1-v1_5",
"RSA-2048", "rsa"). Scoring on raw strings would measure naming conventions, not
detection. Everything goes through normalize() first.
"""
from __future__ import annotations

import pyreq  # noqa: F401  (fails early on an unsupported Python)
import json
import re
from pathlib import Path, PurePosixPath

# ---------------------------------------------------------------------------
# Family metadata
#   primitive: CycloneDX 1.6 algorithmProperties.primitive default
#   shor:      broken by a cryptographically relevant quantum computer (Shor)
# ---------------------------------------------------------------------------
FAMILIES = {
    "MD5":               {"primitive": "hash",          "shor": False},
    "SHA-1":             {"primitive": "hash",          "shor": False},
    "SHA-224":           {"primitive": "hash",          "shor": False},
    "SHA-256":           {"primitive": "hash",          "shor": False},
    "SHA-384":           {"primitive": "hash",          "shor": False},
    "SHA-512":           {"primitive": "hash",          "shor": False},
    "SHA3-256":          {"primitive": "hash",          "shor": False},
    "SHA3-384":          {"primitive": "hash",          "shor": False},
    "SHA3-512":          {"primitive": "hash",          "shor": False},
    "HMAC":              {"primitive": "mac",           "shor": False},
    "PBKDF2":            {"primitive": "kdf",           "shor": False},
    "AES":               {"primitive": "block-cipher",  "shor": False},
    "DES":               {"primitive": "block-cipher",  "shor": False},
    "3DES":              {"primitive": "block-cipher",  "shor": False},
    "ChaCha20-Poly1305": {"primitive": "ae",            "shor": False},
    "RC4":               {"primitive": "stream-cipher", "shor": False},
    "TEA":               {"primitive": "block-cipher",  "shor": False},
    "RSA":               {"primitive": "pke",           "shor": True},
    "DSA":               {"primitive": "signature",     "shor": True},
    "EC":                {"primitive": "signature",     "shor": True},
    "DH":                {"primitive": "key-agree",     "shor": True},
    "Ed25519":           {"primitive": "signature",     "shor": True},
    "X25519":            {"primitive": "key-agree",     "shor": True},
    "ML-KEM":            {"primitive": "kem",           "shor": False, "pq": True},
    "ML-DSA":            {"primitive": "signature",     "shor": False, "pq": True},
    "SLH-DSA":           {"primitive": "signature",     "shor": False, "pq": True},
    "FN-DSA":            {"primitive": "signature",     "shor": False, "pq": True},
    # Hybrid key-establishment groups: a classical and a post-quantum exchange combined. Each is
    # its own family. Reporting only the classical half calls a migrated endpoint vulnerable;
    # reporting only the PQ half overstates what was deployed.
    "X25519MLKEM768":     {"primitive": "kem",          "shor": False, "pq": True, "hybrid": True},
    "SecP256r1MLKEM768":  {"primitive": "kem",          "shor": False, "pq": True, "hybrid": True},
    "SecP384r1MLKEM1024": {"primitive": "kem",          "shor": False, "pq": True, "hybrid": True},
    "sntrup761x25519":    {"primitive": "kem",          "shor": False, "pq": True, "hybrid": True},
}

PQ_PARAM_FAMILIES = {"ML-KEM", "ML-DSA", "SLH-DSA"}
PQ_LEVELS = {"ML-KEM": {"512": 1, "768": 3, "1024": 5}, "ML-DSA": {"44": 2, "65": 3, "87": 5}}
HYBRID_LEVELS = {"X25519MLKEM768": 3, "SecP256r1MLKEM768": 3, "SecP384r1MLKEM1024": 5}
PQ_OIDS = {
    "2.16.840.1.101.3.4.3.17": ("ML-DSA", "44"), "2.16.840.1.101.3.4.3.18": ("ML-DSA", "65"),
    "2.16.840.1.101.3.4.3.19": ("ML-DSA", "87"), "2.16.840.1.101.3.4.4.1": ("ML-KEM", "512"),
    "2.16.840.1.101.3.4.4.2": ("ML-KEM", "768"), "2.16.840.1.101.3.4.4.3": ("ML-KEM", "1024"),
}
HYBRID_PATTERNS = [
    (r"X25519[-_]?MLKEM[-_]?768|MLKEM[-_]?768[-_]?X25519", "X25519MLKEM768"),
    (r"X25519[-_]?KYBER[-_]?768", "X25519MLKEM768"),  # the pre-standard draft codepoint; flagged below
    (r"(SECP256R1|P-?256)[-_]?MLKEM[-_]?768", "SecP256r1MLKEM768"),
    (r"(SECP384R1|P-?384)[-_]?MLKEM[-_]?1024", "SecP384r1MLKEM1024"),
    (r"SNTRUP761[-_]?X25519", "sntrup761x25519"),
]
DILITHIUM_LEVELS = {"2": "44", "3": "65", "5": "87"}

# Protocol versions (Tier 4). Scored as families like any algorithm.
PROTOCOLS = ["SSL-2.0", "SSL-3.0", "TLS-1.0", "TLS-1.1", "TLS-1.2", "TLS-1.3"]
for _p in PROTOCOLS:
    FAMILIES[_p] = {"primitive": "other", "shor": False, "protocol": True}

# TLS cipher suites, canonical IANA name -> OpenSSL name. Key exchange via RSA or (EC)DHE
# is Shor-vulnerable; TLS 1.3 suites don't name a key exchange, so they aren't flagged.
CIPHER_SUITES = {
    "TLS_RSA_WITH_RC4_128_SHA": "RC4-SHA",
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA": "DES-CBC3-SHA",
    "TLS_RSA_WITH_AES_128_CBC_SHA": "AES128-SHA",
    "TLS_RSA_WITH_AES_256_CBC_SHA": "AES256-SHA",
    "TLS_RSA_WITH_AES_128_GCM_SHA256": "AES128-GCM-SHA256",
    "TLS_RSA_WITH_AES_256_GCM_SHA384": "AES256-GCM-SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256": "ECDHE-RSA-AES128-GCM-SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384": "ECDHE-RSA-AES256-GCM-SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256": "ECDHE-ECDSA-AES128-GCM-SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384": "ECDHE-ECDSA-AES256-GCM-SHA384",
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-RSA-CHACHA20-POLY1305",
    "TLS_AES_128_GCM_SHA256": "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384": "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256": "TLS_CHACHA20_POLY1305_SHA256",
}
OPENSSL_TO_IANA = {v.upper(): k for k, v in CIPHER_SUITES.items()}
for _s in CIPHER_SUITES:
    FAMILIES[_s] = {"primitive": "other", "shor": "_WITH_" in _s, "suite": True}

SSH_DH_GROUPS = {"1": 1024, "14": 2048, "15": 3072, "16": 4096, "18": 8192}

# NIST PQC security category (0 = no meaningful security against a quantum or
# classical attacker). Mirrors the convention used in CycloneDX CBOM examples.
CLASSICALLY_BROKEN = {"MD5", "SHA-1", "DES", "3DES", "RC4"}
HASH_LEVEL = {"SHA-224": 1, "SHA-256": 2, "SHA-384": 4, "SHA-512": 5,
              "SHA3-256": 2, "SHA3-384": 4, "SHA3-512": 5}
AES_LEVEL = {128: 1, 192: 3, 256: 5}


def expected_quantum_level(family: str, params: dict) -> int | None:
    if FAMILIES.get(family, {}).get("protocol"):
        return None
    if family in HYBRID_LEVELS:
        return HYBRID_LEVELS[family]
    if family in PQ_LEVELS:
        return PQ_LEVELS[family].get(params.get("param_set"))
    if FAMILIES.get(family, {}).get("pq"):
        return None
    if family in CLASSICALLY_BROKEN or FAMILIES.get(family, {}).get("shor"):
        return 0
    if family in HASH_LEVEL:
        return HASH_LEVEL[family]
    if family == "AES":
        return AES_LEVEL.get(params.get("key_size"))
    if family == "ChaCha20-Poly1305":
        return 5
    if family in ("HMAC", "PBKDF2"):
        h = params.get("hash")
        return 0 if h in CLASSICALLY_BROKEN else HASH_LEVEL.get(h)
    return None


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------
_HASH_PATTERNS = [
    (r"SHA3[-_]?512", "SHA3-512"), (r"SHA3[-_]?384", "SHA3-384"), (r"SHA3[-_]?256", "SHA3-256"),
    (r"SHA2[-_]512", "SHA-512"), (r"SHA2[-_]384", "SHA-384"), (r"SHA2[-_]256", "SHA-256"),  # SSH style
    (r"SHA[-_]?512", "SHA-512"), (r"SHA[-_]?384", "SHA-384"), (r"SHA[-_]?256", "SHA-256"),
    (r"SHA[-_]?224", "SHA-224"), (r"SHA[-_]?1\b|SHA[-_]?1(?=[^0-9])|^SHA$", "SHA-1"),
    (r"MD5", "MD5"),
]
_CURVES = {
    # secp256k1 first: "SECP256K1" contains "P256" and would otherwise be read as NIST P-256.
    "secp256k1": ["SECP256K1"],
    "P-256": ["P-256", "P256", "SECP256R1", "PRIME256V1", "NISTP256"],
    "P-384": ["P-384", "P384", "SECP384R1", "NISTP384"],
    "P-521": ["P-521", "P521", "SECP521R1", "NISTP521"],
}
_MODES = ["ECB", "CBC", "GCM", "CTR", "CFB", "OFB", "CCM", "XTS"]


def norm_hash(s: str | None) -> str | None:
    if not s:
        return None
    u = s.upper().replace(" ", "")
    for pat, name in _HASH_PATTERNS:
        if re.search(pat, u):
            return name
    return None


def _curve(s: str) -> str | None:
    u = s.upper().replace("_", "-")
    for canon, aliases in _CURVES.items():
        for a in aliases:
            if a in u or a.replace("-", "") in u.replace("-", ""):
                return canon
    return None


def _mode(s: str) -> str | None:
    tokens = re.split(r"[^A-Z0-9]", s.upper())
    for m in _MODES:
        if m in tokens:
            return m
    for m in _MODES:  # e.g. "AESGCM", "AES256GCM"
        if s.upper().endswith(m):
            return m
    return None


def _first_int(s: str, choices) -> int | None:
    for n in re.findall(r"(\d{3,5})", s):
        if int(n) in choices:
            return int(n)
    return None


MODP_BITS = {"1": 768, "2": 1024, "5": 1536, "14": 2048, "15": 3072, "16": 4096, "17": 6144, "18": 8192}


def normalize(name: str, props: dict | None = None) -> tuple[str, dict]:
    """Map a scanner's algorithm name (+ optional CycloneDX algorithmProperties) to (family, params)."""
    props = props or {}
    raw = (name or "").strip()
    u = raw.upper().replace(" ", "")
    u = re.sub(r"^(EVP_PKEY_|EVP_|NID_)", "", u)  # OpenSSL symbol names: EVP_des_ede3_cbc, EVP_PKEY_X25519
    params: dict = {}

    def finish(family):
        psi = str(props.get("parameterSetIdentifier") or "")
        if family in PQ_PARAM_FAMILIES:
            m = re.search(r"(\d+[A-Za-z]?)$", psi) if family != "SLH-DSA" else None
            if psi and "param_set" not in params:
                params["param_set"] = m.group(1) if m else psi
        elif psi.isdigit() and "key_size" not in params and family not in ("HMAC", "PBKDF2"):
            params["key_size"] = int(psi)
        if props.get("curve") and "curve" not in params:
            c = _curve(str(props["curve"]))
            if c:
                params["curve"] = c
        if props.get("mode") and "mode" not in params and str(props["mode"]).upper() in _MODES:
            params["mode"] = str(props["mode"]).upper()
        return family, params

    # TLS cipher suites: IANA names (also Java's SSL_ prefix) and OpenSSL names.
    suite = "TLS_" + u[4:] if u.startswith("SSL_") else u
    if suite in CIPHER_SUITES:
        return suite, params
    if u in OPENSSL_TO_IANA:
        return OPENSSL_TO_IANA[u], params

    # Protocol versions: TLSv1, TLSv1.2, TLS1.3, TLS-1.2, SSLv3.
    # Also Go's tls.VersionTLS12 and OpenSSL's TLS1_2_VERSION / SSL3_VERSION.
    u_proto = re.sub(r"^(TLS\.)?VERSION(?=TLS|SSL)|_VERSION$", "", u)
    proto = re.fullmatch(r"(SSL|TLS)[V-]?(\d)(?:[._]?(\d))?", u_proto)
    if proto:
        kind, major, minor = proto.groups()
        return f"{kind}-{major}.{minor or 0}", params

    # SSH algorithm names (RFC 4253 / 8268 / OpenSSH).
    ssh_dh = re.match(r"DIFFIE-HELLMAN-GROUP(\d+)-(SHA\S*)", u)
    if ssh_dh:
        if ssh_dh.group(1) in SSH_DH_GROUPS:
            params["key_size"] = SSH_DH_GROUPS[ssh_dh.group(1)]
        h = norm_hash(ssh_dh.group(2))
        if h:
            params["hash"] = h
        return finish("DH")
    if u == "SSH-RSA":  # RSA signatures with SHA-1
        params["hash"] = "SHA-1"
        return finish("RSA")

    # Certificate signature names written hash-last: ecdsa-with-SHA384, dsa_with_SHA256.
    sig = re.fullmatch(r"(EC)?DSA[-_]WITH[-_](.+)", u)
    if sig:
        h = norm_hash(sig.group(2))
        if h:
            params["hash"] = h
        return finish("EC" if sig.group(1) else "DSA")

    # JWS/JWA 'alg' names (RFC 7518): HS256, RS256, PS384, ES512, EdDSA.
    jws = re.fullmatch(r"(HS|RS|PS|ES)(256|384|512)", u)
    if jws:
        kind, bits = jws.groups()
        params["hash"] = f"SHA-{bits}"
        if kind == "HS":
            return finish("HMAC")
        if kind == "ES":
            params["curve"] = {"256": "P-256", "384": "P-384", "512": "P-521"}[bits]
            return finish("EC")
        return finish("RSA")
    if u == "EDDSA":
        return finish("Ed25519")

    # Pre-standard names (Kyber, Dilithium, SPHINCS+, Falcon, the X25519Kyber768 draft) earn
    # family-level discovery credit, but are flagged: they aren't the FIPS 203/204/205 algorithms
    # (different encodings and test vectors), so they fail the standardised-name check.
    if re.search(r"KYBER|DILITHIUM|SPHINCS|FALCON", u):
        params["prestandard"] = True
    # Post-quantum. Hybrids first (they contain both halves' names), then OIDs (what a scanner on
    # a pre-PQC crypto library sees), then ML-KEM / ML-DSA with parameter sets and their
    # pre-standard Kyber / Dilithium names. All before "DSA", so ML-DSA is never read as DSA.
    for pat, fam in HYBRID_PATTERNS:
        if re.search(pat, u):
            return finish(fam)
    if raw in PQ_OIDS:
        fam, ps = PQ_OIDS[raw]
        params["param_set"] = ps
        return finish(fam)
    m = re.search(r"ML[-_]?KEM[-_.]?(?:GENERATEKEY)?(512|768|1024)?|KYBER[-_]?(512|768|1024)?", u)
    if m:
        ps = m.group(1) or m.group(2)
        if ps:
            params["param_set"] = ps
        return finish("ML-KEM")
    m = re.search(r"ML[-_]?DSA[-_]?(44|65|87)?|DILITHIUM[-_]?([235])?", u)
    if m:
        ps = m.group(1) or DILITHIUM_LEVELS.get(m.group(2) or "")
        if ps:
            params["param_set"] = ps
        return finish("ML-DSA")
    if re.search(r"FN[-_]?DSA|FALCON", u):  # FIPS 206 draft; post-quantum, never classical DSA
        return finish("FN-DSA")
    m = re.search(r"SLH[-_]?DSA[-_]?(.*)|SPHINCS\+?[-_]?(.*)", u)
    if m:
        ps = (m.group(1) or m.group(2) or "").strip("-_")
        if ps:
            params["param_set"] = ps
        return finish("SLH-DSA")

    if "PBKDF2" in u:
        h = norm_hash(u.split("PBKDF2", 1)[1])
        if h:
            params["hash"] = h
        return finish("PBKDF2")

    if u.startswith("HMAC") or "HMAC-" in u:
        h = norm_hash(u.replace("HMAC", "", 1))
        if h:
            params["hash"] = h
        return finish("HMAC")

    if "WITH" in u:  # JCA signature names: SHA256withRSA, SHA256withECDSA, SHA1withDSA
        left, right = u.split("WITH", 1)
        h = norm_hash(left)
        fam, p = normalize(right, props)
        if h:
            p.setdefault("hash", h)
        return fam, p

    if "ED25519" in u:
        return finish("Ed25519")
    if "X25519" in u or "CURVE25519" in u:
        return finish("X25519")
    if "CHACHA20" in u:
        return finish("ChaCha20-Poly1305")
    if re.search(r"(^|[^A-Z])A?RC4|ARCFOUR", u):
        return finish("RC4")
    if re.fullmatch(r"X?TEA(-\d+)?", u):
        return finish("TEA")
    if re.search(r"DESEDE|TRIPLEDES|3DES|TDEA|DES[-_]EDE|DES3", u):
        m = _mode(u)
        if m:
            params["mode"] = m
        return finish("3DES")
    if re.match(r"^DES(\b|[/_-]|$)", u):
        m = _mode(u)
        if m:
            params["mode"] = m
        return finish("DES")
    if "AES" in u:
        ks = _first_int(u, (128, 192, 256))
        if ks:
            params["key_size"] = ks
        m = _mode(u.replace("AES", "", 1))
        if m:
            params["mode"] = m
        return finish("AES")
    if re.search(r"ECDSA|ECDH|^EC$|^ECC|^EC[-_]|EC(?=P\d)", u) or _curve(u) and "RSA" not in u:
        c = _curve(u)
        if c:
            params["curve"] = c
        return finish("EC")
    if "RSA" in u:
        ks = _first_int(u, range(512, 16385))
        if ks:
            params["key_size"] = ks
        return finish("RSA")
    if re.search(r"(^|[^A-Z])DSA", u):
        ks = _first_int(u, range(512, 16385))
        if ks:
            params["key_size"] = ks
        return finish("DSA")
    modp = re.fullmatch(r"MODP[-_]?(\d+)", u)  # RFC 3526 group numbers (Node's getDiffieHellman)
    if modp and modp.group(1) in MODP_BITS:
        params["key_size"] = MODP_BITS[modp.group(1)]
        return finish("DH")
    if re.search(r"^(FF)?DHE?($|[-_\d])|DIFFIE", u):
        ks = _first_int(u, range(512, 16385))
        if ks:
            params["key_size"] = ks
        return finish("DH")
    h = norm_hash(u)
    if h:
        return finish(h)
    return finish(raw or "UNKNOWN")


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
def norm_path(p: str) -> str:
    """Normalize a scanner location. Findings inside an archive ('app.jar!/com/x/Y.class',
    'jar:file:/srv/app.jar!/...') are attributed to the archive file itself."""
    p = p.replace("\\", "/")
    for prefix in ("jar:", "zip:", "file://", "file:"):
        if p.startswith(prefix):
            p = p[len(prefix):]
    if "!/" in p:
        p = p.split("!/", 1)[0]
    return str(PurePosixPath(p))


def same_file(scanner_path: str, truth_path: str) -> bool:
    """Suffix match so absolute paths and corpus-relative paths both work."""
    a, b = norm_path(scanner_path), norm_path(truth_path)
    if a == b:
        return True
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    return long_.endswith("/" + short) and short.count("/") >= 1


# ---------------------------------------------------------------------------
# CycloneDX 1.6 I/O
# ---------------------------------------------------------------------------
def display_name(family: str, params: dict) -> str:
    if family == "AES":
        parts = ["AES"] + ([str(params["key_size"])] if "key_size" in params else []) \
                + ([params["mode"]] if "mode" in params else [])
        return "-".join(parts)
    if family in ("DES", "3DES"):
        return family + (f"-{params['mode']}" if "mode" in params else "")
    if family in ("RSA", "DSA", "DH") and "key_size" in params:
        return f"{family}-{params['key_size']}"
    if family == "EC" and "curve" in params:
        return f"ECC-{params['curve']}"
    if family == "HMAC" and "hash" in params:
        return f"HMAC-{params['hash']}"
    if family == "PBKDF2" and "hash" in params:
        return f"PBKDF2-HMAC-{params['hash']}"
    if family in PQ_PARAM_FAMILIES and "param_set" in params:
        return f"{family}-{params['param_set']}"
    return family


# OIDs for the algorithm components a good CBOM should carry. Families with no standard OID
# (TEA, hybrid TLS groups, cipher suites, protocol versions) return None and aren't checked.
_AES_OID = {128: {"ECB": 1, "CBC": 2, "OFB": 3, "CFB": 4, "GCM": 6},
            192: {"ECB": 21, "CBC": 22, "OFB": 23, "CFB": 24, "GCM": 26},
            256: {"ECB": 41, "CBC": 42, "OFB": 43, "CFB": 44, "GCM": 46}}
_OID = {
    "MD5": "1.2.840.113549.2.5", "SHA-1": "1.3.14.3.2.26", "SHA-224": "2.16.840.1.101.3.4.2.4",
    "SHA-256": "2.16.840.1.101.3.4.2.1", "SHA-384": "2.16.840.1.101.3.4.2.2", "SHA-512": "2.16.840.1.101.3.4.2.3",
    "SHA3-256": "2.16.840.1.101.3.4.2.8", "SHA3-384": "2.16.840.1.101.3.4.2.9", "SHA3-512": "2.16.840.1.101.3.4.2.10",
    "PBKDF2": "1.2.840.113549.1.5.12", "DES": "1.3.14.3.2.7", "3DES": "1.2.840.113549.3.7", "RC4": "1.2.840.113549.3.4",
    "ChaCha20-Poly1305": "1.2.840.113549.1.9.16.3.18", "RSA": "1.2.840.113549.1.1.1", "DSA": "1.2.840.10040.4.1",
    "EC": "1.2.840.10045.2.1", "DH": "1.2.840.113549.1.3.1", "Ed25519": "1.3.101.112", "X25519": "1.3.101.110",
}
_HMAC_OID = {"SHA-1": "1.2.840.113549.2.7", "SHA-256": "1.2.840.113549.2.9", "SHA-384": "1.2.840.113549.2.10",
             "SHA-512": "1.2.840.113549.2.11", "MD5": "1.3.6.1.5.5.8.1.1"}


def oid_for(family: str, params: dict) -> str | None:
    if family == "AES":
        n = _AES_OID.get(params.get("key_size"), {}).get(params.get("mode"))
        return f"2.16.840.1.101.3.4.1.{n}" if n else None
    if family == "HMAC":
        return _HMAC_OID.get(params.get("hash"))
    if family in PQ_PARAM_FAMILIES:
        for oid, (fam, ps) in PQ_OIDS.items():
            if fam == family and ps == params.get("param_set"):
                return oid
        return None
    return _OID.get(family)


_FUNCTIONS = {"hash": ["digest"], "mac": ["tag"], "kdf": ["keyderive"], "block-cipher": ["encrypt", "decrypt"],
              "stream-cipher": ["encrypt", "decrypt"], "ae": ["encrypt", "decrypt"], "signature": ["keygen", "sign", "verify"],
              "pke": ["keygen", "encrypt", "decrypt"], "kem": ["keygen", "encapsulate", "decapsulate"],
              "key-agree": ["keygen", "keyderive"]}


def functions_for(primitive: str | None) -> list[str] | None:
    return _FUNCTIONS.get(primitive or "")


def make_component(ref: str, family: str, params: dict, occurrences: list[dict],
                   primitive: str | None = None, functions: list[str] | None = None, oid: str | None = None) -> dict:
    alg = {"primitive": primitive or FAMILIES.get(family, {}).get("primitive", "unknown")}
    if "key_size" in params:
        alg["parameterSetIdentifier"] = str(params["key_size"])
    if "param_set" in params:
        alg["parameterSetIdentifier"] = str(params["param_set"])
    if "curve" in params:
        alg["curve"] = params["curve"]
    if "mode" in params:
        alg["mode"] = params["mode"].lower()
    if functions:
        alg["cryptoFunctions"] = functions
    lvl = expected_quantum_level(family, params)
    if lvl is not None:
        alg["nistQuantumSecurityLevel"] = lvl
    cp = {"assetType": "algorithm", "algorithmProperties": alg}
    if oid:
        cp["oid"] = oid
    return {
        "type": "cryptographic-asset",
        "bom-ref": ref,
        "name": display_name(family, params),
        "cryptoProperties": cp,
        "evidence": {"occurrences": occurrences},
    }


def make_bom(components: list[dict], tool_name: str, dependencies: list[dict] | None = None) -> dict:
    bom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {"tools": {"components": [{"type": "application", "name": tool_name}]}},
        "components": components,
    }
    if dependencies:
        bom["dependencies"] = dependencies
    return bom


SIGNATURE_FAMILIES = {"RSA", "EC", "DSA"}


def _walk(comps):
    for c in comps or []:
        yield c
        yield from _walk(c.get("components"))


def iter_crypto_findings_ctx(bom: dict):
    """Yield (family, params, [(location, line)], nist_level, ctx) for every cryptographic asset in a BOM.

    Handles all four CycloneDX 1.6 asset types:
      algorithm               -> the algorithm itself
      certificate             -> follows subjectPublicKeyRef and signatureAlgorithmRef
      related-crypto-material -> follows algorithmRef; 'size' becomes key_size
      protocol                -> TLS version as a family, plus each cipherSuites[].name
    A compound signature name (SHA256withRSA, ecdsa-with-SHA384, RS256) also yields its hash,
    so a SHA-1-signed certificate surfaces SHA-1 as well as RSA.

    ctx keeps what actionability scoring needs: the top-level asset ('asset', its 'kind'), the
    algorithm component the item resolved through ('via'), the raw occurrence records, which
    dependencies 'provide' the asset, and 'role' (key / signature / suite / version / algorithm).
    """
    comps = [c for c in _walk(bom.get("components")) if c.get("type") == "cryptographic-asset"]
    by_ref = {c["bom-ref"]: c for c in comps if c.get("bom-ref")}
    providers = {}
    for d in bom.get("dependencies", []) or []:
        for r in d.get("provides", []) or []:
            providers.setdefault(r, []).append(d.get("ref"))

    referenced = set()
    for c in comps:
        cp = c.get("cryptoProperties") or {}
        cert = cp.get("certificateProperties") or {}
        rcm = cp.get("relatedCryptoMaterialProperties") or {}
        referenced.update(r for r in (cert.get("signatureAlgorithmRef"), cert.get("subjectPublicKeyRef"),
                                      rcm.get("algorithmRef")) if r)
        for cs in (cp.get("protocolProperties") or {}).get("cipherSuites", []) or []:
            referenced.update(cs.get("algorithms") or [])

    def resolve(c, depth=0, role="algorithm") -> list:
        """-> [(family, params, via_component, role)]"""
        if c is None or depth > 4:
            return []
        cp = c.get("cryptoProperties") or {}
        at = cp.get("assetType") or "algorithm"
        if at == "algorithm":
            fam, params = normalize(c.get("name", ""), cp.get("algorithmProperties") or {})
            if fam not in FAMILIES and cp.get("oid"):  # name unknown to us, OID may not be
                fam, params = normalize(str(cp["oid"]), cp.get("algorithmProperties") or {})
            return [(fam, params, c, role)]
        if at == "related-crypto-material":
            rcm = cp.get("relatedCryptoMaterialProperties") or {}
            ref = rcm.get("algorithmRef")
            items = (resolve(by_ref.get(ref), depth + 1, "key") if ref
                     else [(*normalize(c.get("name", ""), cp.get("algorithmProperties") or {}), c, "key")])
            size = rcm.get("size")
            if isinstance(size, int):
                for fam, p, _, _ in items:
                    if fam in ("RSA", "DSA", "DH"):
                        p.setdefault("key_size", size)
            return items
        if at == "certificate":
            cert = cp.get("certificateProperties") or {}
            out = []
            for key, r in (("subjectPublicKeyRef", "key"), ("signatureAlgorithmRef", "signature")):
                if cert.get(key):
                    out += resolve(by_ref.get(cert[key]), depth + 1, r)
            if not out:  # no refs: some scanners name the certificate by its key algorithm instead
                fam, params = normalize(c.get("name", ""), cp.get("algorithmProperties") or {})
                if fam in FAMILIES:
                    out.append((fam, params, c, "key"))
            return out
        if at == "protocol":
            pp = cp.get("protocolProperties") or {}
            out = []
            if pp.get("type") == "tls" and pp.get("version"):
                v = str(pp["version"]).upper().replace("TLS", "").replace("V", "").strip(" -")
                out.append((*normalize(f"TLS{v}" if not v.startswith("SSL") else v), c, "version"))
            for cs in pp.get("cipherSuites", []) or []:
                if cs.get("name"):
                    out.append((*normalize(cs["name"]), c, "suite"))
            return out or [(*normalize(c.get("name", "")), c, "algorithm")]
        return []

    for c in comps:
        raw = (c.get("evidence") or {}).get("occurrences", []) or []
        occ = [(o.get("location", ""), o.get("line")) for o in raw]
        if not occ and c.get("bom-ref") in referenced:
            continue  # reached through the certificate / key / protocol that references it
        cp = c.get("cryptoProperties") or {}
        kind = cp.get("assetType") or "algorithm"
        for family, params, via, role in resolve(c):
            via_ap = ((via or {}).get("cryptoProperties") or {}).get("algorithmProperties") or {}
            level = via_ap.get("nistQuantumSecurityLevel") if kind == "algorithm" or role == "key" else None
            prov = providers.get(c.get("bom-ref"), []) + providers.get((via or {}).get("bom-ref"), [])
            ctx = {"kind": kind, "asset": c, "via": via, "role": role, "occurrences": raw, "provided_by": prov}
            yield family, params, occ, level, ctx
            if family in SIGNATURE_FAMILIES and params.get("hash"):
                yield params["hash"], {}, occ, None, {**ctx, "role": "signature-hash"}


def iter_crypto_findings(bom: dict):
    """Yield (family, params, [(location, line)], nist_level) for every cryptographic asset in a BOM."""
    for family, params, occ, level, _ in iter_crypto_findings_ctx(bom):
        yield family, params, occ, level


def make_certificate(ref: str, file: str, key_family: str, key_params: dict, sig_alg: str,
                     facts: dict | None = None) -> list[dict]:
    """A certificate component plus the two algorithm components it references. 'facts' (subject,
    issuer, validity, signature OID) are read from the real certificate by build_expected.py."""
    facts = facts or {}
    key_prim = "signature"  # a certificate's subject key is a signing key (or, rarely, KEM; scored leniently)
    key = make_component(f"{ref}-key", key_family, key_params, [], primitive=key_prim,
                         functions=functions_for(key_prim), oid=oid_for(key_family, key_params))
    sig_fam, sig_params = normalize(sig_alg)
    sig = make_component(f"{ref}-sig", sig_fam, sig_params, [], primitive="signature",
                         functions=["sign", "verify"], oid=facts.get("sig_oid"))
    sig["name"] = sig_alg
    for c in (key, sig):
        del c["evidence"]
    props = {"subjectPublicKeyRef": key["bom-ref"], "signatureAlgorithmRef": sig["bom-ref"], "certificateFormat": "X.509"}
    for k_out, k_in in (("subjectName", "subject"), ("issuerName", "issuer"),
                        ("notValidBefore", "not_before"), ("notValidAfter", "not_after")):
        if facts.get(k_in):
            props[k_out] = facts[k_in]
    cert = {
        "type": "cryptographic-asset", "bom-ref": ref, "name": f"certificate {Path(file).name}",
        "cryptoProperties": {"assetType": "certificate", "certificateProperties": props},
        "evidence": {"occurrences": [{"location": file}]},
    }
    return [cert, key, sig]


def make_key_material(ref: str, file: str, kind: str, family: str, params: dict, fmt: str | None = None) -> list[dict]:
    """A related-crypto-material component (private-key / public-key) plus its algorithm component."""
    prim = FAMILIES.get(family, {}).get("primitive")
    alg = make_component(f"{ref}-alg", family, params, [], functions=functions_for(prim), oid=oid_for(family, params))
    del alg["evidence"]
    rcm = {"type": kind, "algorithmRef": alg["bom-ref"]}
    if "key_size" in params:
        rcm["size"] = params["key_size"]
    if fmt:
        rcm["format"] = fmt
    km = {"type": "cryptographic-asset", "bom-ref": ref, "name": f"{kind} {Path(file).name}",
          "cryptoProperties": {"assetType": "related-crypto-material", "relatedCryptoMaterialProperties": rcm},
          "evidence": {"occurrences": [{"location": file}]}}
    return [km, alg]


def make_protocols(ref: str, file: str, versions: list[str], suites: list[str], lines: dict) -> list[dict]:
    """One protocol component per TLS version, each listing the file's cipher suites."""
    out = []
    for v in versions or [None]:
        pp = {"type": "tls"}
        if v:
            pp["version"] = v.split("-", 1)[1]
        if suites:
            pp["cipherSuites"] = [{"name": s} for s in suites]
        occ_lines = sorted({ln for k, ln in lines.items() if k == v or k in suites})
        occs = [{"location": file, "line": ln} for ln in occ_lines] or [{"location": file}]
        out.append({"type": "cryptographic-asset", "bom-ref": f"{ref}-{v or 'suites'}",
                    "name": v or "TLS", "cryptoProperties": {"assetType": "protocol", "protocolProperties": pp},
                    "evidence": {"occurrences": occs}})
    return out


def load_json(path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
