"""Adapter for static-analysis tools that report findings as SARIF 2.1.0: Semgrep, Opengrep, CodeQL.

These tools are not CBOM scanners. They flag code a rule considers a problem; they do not list the
cryptography a codebase uses. A buyer who already runs one will still ask what it would have found,
so the benchmark scores what can fairly be read out of their output, and says what cannot.

What the adapter does:

  1. Keeps the results of rules about cryptography and drops the rest. A rule is about
     cryptography when its id, tags or description say so (crypto, cipher, hash, a CWE for weak or
     broken cryptography, or an algorithm name).
  2. Reads the algorithm each kept result names. The rule id comes first
     ("...insecure-hash-algorithm-md5" names MD5). When the id names none, the result's message is
     read, up to the point where it starts recommending something: "MD5 is weak. Use SHA-256
     instead" names MD5, not SHA-256. When the message names none either, the flagged code itself
     is read, if the tool included it: a padding-oracle rule does not say which cipher, the line
     `Cipher.getInstance("AES/CBC/PKCS5Padding")` does. The rule's description comes last.
  3. Emits one CycloneDX cryptographic-asset component per algorithm, with each result's file and
     line as an occurrence. A key size stated in the message ("uses 1024 bits") is kept for RSA,
     DSA and DH, and a mode named with a cipher (ECB, CBC) is kept.

What it cannot do, and does not pretend to:

  - A result that names no algorithm ("use of a broken or risky cryptographic algorithm") becomes
    no component. It is counted in the notes as `unnamed`.
  - These tools mostly report what a rule calls weak. AES-256-GCM used correctly produces no
    result, so it produces no component, and the scorer counts it as missed. That is the honest
    answer to "why not use what we already have": the tool was never asked for an inventory.

Nothing here is specific to one tool's rule pack. Checked against the SARIF Semgrep 1.x, Opengrep
1.x and the CodeQL CLI write.
"""
from __future__ import annotations

import re

ADAPTER_VERSION = "0.1"
BUILT_FOR = "SARIF 2.1.0 (Semgrep, Opengrep, CodeQL)"

# Token in a rule id or message -> the name the scorer's normalizer knows. Longest first where one
# token contains another.
_ALGORITHMS = [
    (r"sha[-_ ]?3[-_ ]?(224|256|384|512)", lambda m: f"SHA3-{m.group(1)}"),
    (r"sha[-_ ]?(224|256|384|512)", lambda m: f"SHA-{m.group(1)}"),
    (r"sha[-_ ]?1(?![0-9])", lambda m: "SHA-1"),
    (r"md5", lambda m: "MD5"), (r"md4", lambda m: "MD4"), (r"md2", lambda m: "MD2"),
    (r"3des|triple[-_ ]?des|des[-_ ]?ede3?|desede|tdea", lambda m: "3DES"),
    (r"(?<![a-z0-9])des(?![a-z0-9])", lambda m: "DES"),
    (r"rc4|arcfour|arc4", lambda m: "RC4"), (r"(?<![a-z0-9])rc2(?![a-z0-9])", lambda m: "RC2"),
    (r"blowfish", lambda m: "Blowfish"),
    (r"(?<![a-z0-9])aes(?![a-z])", lambda m: "AES"),
    (r"chacha20", lambda m: "ChaCha20-Poly1305"),
    (r"ecdsa", lambda m: "ECDSA"), (r"ecdh", lambda m: "ECDH"),
    (r"ed25519", lambda m: "Ed25519"), (r"x25519|curve25519", lambda m: "X25519"),
    (r"(?<![a-z0-9])rsa(?![a-z])", lambda m: "RSA"),
    (r"(?<![a-z0-9])dsa(?![a-z])", lambda m: "DSA"),
    (r"diffie[-_ ]?hellman|(?<![a-z0-9])dh(?![a-z0-9])", lambda m: "DH"),
    (r"pbkdf2", lambda m: "PBKDF2"), (r"hmac", lambda m: "HMAC"),
    (r"ml[-_ ]?kem", lambda m: "ML-KEM"), (r"ml[-_ ]?dsa", lambda m: "ML-DSA"),
]
_ALG_RE = [(re.compile(p, re.I), f) for p, f in _ALGORITHMS]
_CRYPTO_RULE = re.compile(
    r"crypt|cipher|hash|digest|(?<![a-z])tls|(?<![a-z])ssl|key[-_ ]?size|key[-_ ]?length|weak[-_ ]?key|"
    r"cwe-?(?:326|327|328|916|780|310|1240)(?![0-9])|md5|sha-?1|(?<![a-z0-9])des(?![a-z0-9])|rc4|(?<![a-z0-9])rsa(?![a-z])|"
    r"(?<![a-z0-9])ecb(?![a-z0-9])|pbkdf|hmac|bcrypt", re.I)
# Where a message stops describing what it found and starts recommending something else.
_ADVICE = re.compile(r"(?:(?:^|[.;:!]\s+)(?:please\s+)?(?:use|switch|replace|migrate|upgrade|prefer|choose|try)\b)|\b(?:instead|use (?:of )?(?:a |an |the )?(?:stronger|secure|safer|modern)|should (?:be )?(?:use|switch|replac|migrat)|"
                     r"recommend|consider|prefer|such as|switch to|replace (?:it )?with|upgrade to|like sha|e\.g\.)", re.I)
_BITS = re.compile(r"\b(512|768|1024|1536|2048|3072|4096|7680|8192)\s*-?\s*bits?\b|\bkey (?:size|length) (?:of )?(512|768|1024|1536|2048|3072|4096)\b", re.I)
_MODE = re.compile(r"(?<![a-z0-9])(ECB|CBC|GCM|CTR|CFB|OFB)(?![a-z0-9])", re.I)


def algorithms_in(text: str) -> list[str]:
    """Algorithm names in a piece of text, in the order written, without repeats."""
    hits = []
    for rx, name in _ALG_RE:
        for m in rx.finditer(text):
            hits.append((m.start(), m.end(), name(m)))
    hits.sort(key=lambda h: (h[0], -h[1]))      # at one position the longest name wins: des-ede3 is 3DES
    out, covered_to = [], -1
    for start, end, name in hits:
        if start < covered_to:
            continue                      # inside a longer match already taken ("des" in "3des")
        covered_to = end
        if name not in out:
            out.append(name)
    return out


def _described(text: str) -> str:
    """The part of a message that says what was found, before any advice."""
    m = _ADVICE.search(text or "")
    return (text or "")[: m.start()] if m else (text or "")


def _rule_text(rule: dict) -> str:
    props = rule.get("properties") or {}
    parts = [rule.get("id", ""), rule.get("name", ""), (rule.get("shortDescription") or {}).get("text", ""),
             " ".join(str(t) for t in props.get("tags") or [])]
    return " ".join(p for p in parts if p)


def _location(result: dict) -> tuple[str, int | None]:
    for loc in result.get("locations") or []:
        phys = loc.get("physicalLocation") or {}
        uri = (phys.get("artifactLocation") or {}).get("uri") or ""
        if uri:
            return uri.replace("file://", ""), (phys.get("region") or {}).get("startLine")
    return "", None


def _snippet(result: dict) -> str:
    """The flagged code, when the tool included it. Only the flagged region, never its context."""
    for loc in result.get("locations") or []:
        text = ((((loc.get("physicalLocation") or {}).get("region") or {}).get("snippet") or {}).get("text")) or ""
        if text:
            return text[:400]
    return ""


def translate(sarif: dict) -> tuple[dict, list[dict], dict]:
    """-> (CycloneDX bom for the scorer, signals, notes)."""
    notes = {"results": 0, "crypto_results": 0, "named": 0, "unnamed": 0, "tools": [], "unnamed_rules": {}, "rules_used": {}}
    found: dict[tuple, dict] = {}
    for run in sarif.get("runs") or []:
        driver = (run.get("tool") or {}).get("driver") or {}
        tool = " ".join(x for x in (driver.get("name"), driver.get("semanticVersion") or driver.get("version")) if x)
        if tool and tool not in notes["tools"]:
            notes["tools"].append(tool)
        rules = {r.get("id"): r for r in driver.get("rules") or []}
        for ext in (run.get("tool") or {}).get("extensions") or []:
            rules.update({r.get("id"): r for r in ext.get("rules") or []})
        for res in run.get("results") or []:
            notes["results"] += 1
            rule_id = res.get("ruleId") or (res.get("rule") or {}).get("id") or ""
            rule = rules.get(rule_id) or {"id": rule_id}
            # SARIF messages link to related locations as [text](1); the text is what was found.
            message = re.sub(r"\[([^\]]+)\]\(\d+\)", r"\1", (res.get("message") or {}).get("text") or "")
            if not _CRYPTO_RULE.search(_rule_text(rule)):
                continue
            notes["crypto_results"] += 1
            # The last segment of a dotted or slashed id is the rule's own name; the rest is its path.
            own = re.split(r"[./]", rule_id)[-1]
            # Then the code the result points at, which is what a person reading the finding sees:
            # a rule about CBC padding says nothing of the cipher, the flagged line says AES.
            names = algorithms_in(own) or algorithms_in(_described(message)) or algorithms_in(_snippet(res)) \
                or algorithms_in(_described((rule.get("shortDescription") or {}).get("text", "")))
            if not names:
                notes["unnamed"] += 1
                notes["unnamed_rules"][rule_id] = notes["unnamed_rules"].get(rule_id, 0) + 1
                continue
            notes["named"] += 1
            notes["rules_used"][rule_id] = notes["rules_used"].get(rule_id, 0) + 1
            uri, line = _location(res)
            said = _described(message)
            bits = _BITS.search(said)
            mode = _MODE.search(own) or _MODE.search(said) or _MODE.search(_snippet(res))
            for name in names:
                props = {}
                if bits and name in ("RSA", "DSA", "DH"):
                    props["parameterSetIdentifier"] = bits.group(1) or bits.group(2)
                if mode and name in ("AES", "DES", "3DES", "Blowfish"):
                    props["mode"] = mode.group(1).lower()
                key = (name, tuple(sorted(props.items())))
                comp = found.setdefault(key, {
                    "type": "cryptographic-asset", "name": name, "bom-ref": f"sarif-{len(found) + 1}",
                    "cryptoProperties": {"assetType": "algorithm", "algorithmProperties": dict(props)},
                    "evidence": {"occurrences": []},
                    "properties": [{"name": "cbom-testbench:sarif_rule", "value": rule_id}],
                })
                occ = {"location": uri}
                if isinstance(line, int):
                    occ["line"] = line
                if occ not in comp["evidence"]["occurrences"]:
                    comp["evidence"]["occurrences"].append(occ)
    bom = {
        "bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
        "metadata": {"properties": [{"name": "cbom-testbench:adapter", "value": f"sarif {ADAPTER_VERSION} ({', '.join(notes['tools']) or 'unknown tool'})"}]},
        "components": list(found.values()),
    }
    return bom, [], notes
