# cdxgen 12.9.1 on the CBOM Testbench

Run with `python tools/run_cdxgen.py` (`cbom --spec-version 1.6 --no-install-deps --evidence` on a copy
of `corpus/`), 2026-11-10, Node 22, outside cdxgen's container image. Full scorecard:
`reports/cdxgen/`. Side-by-side with QCI: `reports/comparison.md`.

## What it does well

JavaScript and TypeScript get real AST analysis: an exact line, the calling symbol
(`node:crypto.createHash`) and the role (`hash`, `hmac`, `kdf`, `signature`, `key-generation`). On
what it reports, nothing is wrong. Zero false positives, zero PQC over-claims across all twelve
negative-control files, 80% of detections ticket-ready. It also reads an HMAC's hash out of a module
constant (`createHmac(WEBHOOK_DIGEST, ...)`), which is a Tier 2 case.

## Dependencies: the strongest result in this testbench

On the 26 crypto libraries in `corpus/deps/`, cdxgen finds 20 in the right manifest and 23 in
total, with every reported version correct, including Maven's `${bc.version}` property resolved to
1.70, and all four transitive npm libraries from the lockfile. No false positives: the commented-out
`pycrypto` and Jasypt lines are ignored, and `hashids` is listed as a plain library, not as crypto.
It also carries upstream's deprecation notice on crypto-js (`cdx:npm:deprecated`: "Active development of
CryptoJS has been discontinued.").

What it misses, in this configuration (`--no-install-deps`, no Gradle on the path):
`pyproject.toml`'s PEP 621 dependencies (cryptography range, liboqs-python) and `build.gradle`
(Bouncy Castle 1.80). The three Go modules are listed with correct versions but no location, so they
can't be attributed to an application. It gives no post-quantum verdict for any library, which is
fair for an SBOM tool and the gap a CBOM tool should fill.

## Where the 10 of 242 comes from

| Area | Result | What happens |
|---|---|---|
| JavaScript / TypeScript | 10 of 24 | Hashes, HMAC, PBKDF2, RSA and Ed25519 key generation found. Nothing for `createCipheriv` (AES, 3DES, ChaCha20-Poly1305 by name), `generateKeyPairSync("ec" / "x25519")`, `getDiffieHellman`, or Web Crypto `subtle.generateKey` / `subtle.digest`. |
| Java, Python | 0 located | atom finds the call sites (348 line-numbered slices for Java Tier 1 alone), and cdxgen names algorithms from them (`aes`, `des`, `hmacSHA`, `P-256`, `PBKDF2`). But no slice is tagged, so no component gets a location: "Unable to identify component evidence ... slices ... lack appropriate tags". Same with `--profile research`. Unlocated components can't be scored or acted on. |
| Go, C | 0 | Dependency inventory only: `libssl-dev`, header names, and one "library" per C source file. |
| Certificates, keys, keystores, SSH keys | 16 files found, 0 algorithms | Each file becomes a `certificate` component named after the file, with no algorithm, key size, subject or expiry. Private keys, public keys and keystores are all typed `certificate`. Credited separately as file-level signals: 23 expected findings sit in those files. |

The Java/Python result may be an environment issue (cdxgen recommends its container image, which
couldn't run here). Worth rerunning in the official image before quoting it.

## Smaller things worth reporting upstream

- **RSA key size is dropped.** `generateKeyPairSync("rsa", { modulusLength: 2048 })` is found; the
  2048 on the same call isn't recorded.
- **Nonstandard OIDs.** SHA-1 is given `2.16.840.1.113719.1.2.8.82` (a vendor arc) rather than
  `1.3.14.3.2.26`; RSA gets `2.5.8.1.1` (the old X.500 one) rather than `1.2.840.113549.1.1.1`; DES gets
  a TeleTrusT OID. A consumer matching on OID will miss these.
- **One component per algorithm name, many locations.** `sha-256` is one component with five
  occurrences that are hashing, HMAC, two signatures and a key derivation. Fine for an inventory; it
  means the role lives only in `additionalContext`, which the adapter has to read to tell an HMAC from
  a hash.
- **Located and unlocated components share a name.** There are two `sha-256` components, one with
  evidence and one without.

## How the adapter treats this output

See `tools/adapters/cdxgen.py`. Algorithms with locations are scored as reported, except that a
hash in an `hmac` or `kdf` context becomes `HMAC-<hash>` / `PBKDF2-<hash>`: cdxgen says so explicitly
in the occurrence. Unlocated algorithms are left alone (neither credited nor penalized).
Filename-only `certificate` entries become crypto-file signals and are renamed, so
`telemetry_ecdsa.pem` is never read as an EC finding.
