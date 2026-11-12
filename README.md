# QCI CBOM Benchmark

> A graded test corpus and scoring harness for Cryptographic Bill of Materials (CBOM) scanners. It scores a scanner's CycloneDX 1.6 output against 410 known findings. Not a certification.

[![testbench](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/testbench.yml/badge.svg)](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/testbench.yml)
[![image](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/image.yml/badge.svg)](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/image.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Methodology 2.3](https://img.shields.io/badge/methodology-2.3-informational.svg)](METHODOLOGY.md)

**Version:** 2.6.0 · **Author:** Quantum Core Institute · **License:** Apache-2.0 ([LICENSE](LICENSE))

2.6.0 deepens the hardest rows: two more minified JavaScript bundles and two more stripped native binaries, so each of those rows has 11 findings instead of 3.

[Release notes](CHANGELOG.md) · [Methodology](METHODOLOGY.md) · [Results](reports/comparison.md) · [Evidence](evidence/) · [Holdout sets](HOLDOUT.md) · [Bring your own code](BYOC.md)

## What it does

Point a scanner at `corpus/`, feed its CycloneDX 1.6 output to the scorer, and you get a scorecard
that says *where* it fails: which tier, which language, which algorithm, whether it got the key size
right, and how much noise it made on files that contain no crypto at all. Every expected finding is
dated against NIST, EO 14412 and CNSA 2.0 transition deadlines, and every detected finding is checked
for whether an engineer could open a ticket from it. Because a public corpus gets learned, the
benchmark also generates private holdout sets that show whether a published score still predicts
performance on unseen code.

- **410 findings in seven languages** (Python, Java, Go, JavaScript/TypeScript, C/OpenSSL, C#/.NET)
  plus certificates, keys, keystores, configs and compiled artifacts. Every code case runs and every
  asset parses.
- **Five tiers of difficulty**, from a literal `hashlib.md5()` to a stripped binary, plus a
  post-quantum category, realistic mixed files, dead code, a multi-service system fixture and
  negative controls.
- **Scores that can be checked.** A run produces an evidence bundle; anyone can re-derive every
  number in it from the scanner's raw output.
- **Your own code as scored cases**, kept apart from the shipped answer key.
- **Gates for CI**, stamped to the exact release they were measured on.

QCI also publishes a scanner that this benchmark grades (`qci-pqc-scan`, currently v2.3.4.1). The
benchmark lives in its own repository with its own versioned methodology, and that scanner's results
are published as measured, gate failures included: see
[reports/qci-pqc/SUMMARY.md](reports/qci-pqc/SUMMARY.md) and
[integrations/qci-pqc/FINDINGS.md](integrations/qci-pqc/FINDINGS.md). Earlier releases were called
the CBOM Testbench, and the tools still use "testbench" for the harness itself.

## Requirements

| To do this | You need |
|---|---|
| Score a CBOM, run the tests, build bundles | Python 3.11+ and `pip install -r requirements.txt` (pinned: `cryptography`, the CycloneDX validator, `packaging`) |
| Run every corpus case (`verify_corpus.py --strict`) | Also `requirements-verify.txt` (a Java 25 runtime for the PQC Java cases), Go 1.24+, Node 22.18+, JDK 21, the .NET 8 SDK, Bouncy Castle's provider jar (`apt install libbcprov-java`, or set `BCPROV_JAR`), a C compiler with OpenSSL 3 headers, and Python 3.13 for the shipped `.pyc` |
| Run a scanner in the sandbox with full isolation | Linux with unprivileged user namespaces, or Docker for the container lane |
| Skip all of that | The pinned image (`Dockerfile`), which carries every toolchain and verifies the corpus at build time |

## Quick start

```bash
pip install -r requirements.txt

# 1. Check the benchmark itself (needs the toolchains above)
pip install -r requirements-verify.txt
python tools/verify_corpus.py --strict     # runs every code case, parses every asset; a skip is a failure
python tools/build_expected.py             # resolves the answer key, writes expected/expected.cdx.json
python tools/bench.py checks               # every required check: corpus, answer key, tests, docs

# 2. Score your scanner
your-scanner --format cyclonedx-1.6 corpus/ > reports/scanner-x.cdx.json
python tools/score.py reports/scanner-x.cdx.json --name "Scanner X"
#   -> reports/scanner-x.md and reports/scanner-x.json

# 3. Or do it in one step, in the sandbox, with an evidence bundle
python tools/bench.py run --name "Scanner X" \
    --scanner-cmd "scanx {corpus} -o {out}/cbom.json" --bundle bundles/scanner-x
python tools/bench.py verify bundles/scanner-x

# 4. Date any CBOM, including your own estate's, against one or more policies
python tools/policy_report.py your-scan.cdx.json --policy nist --policy cnsa2
```

## Usage

### Scoring a scanner

`tools/score.py` takes a CycloneDX 1.6 CBOM and writes a scorecard. It is the quick path: no sandbox,
no bundle.

| Option | What it does |
|---|---|
| `--name NAME` | Scanner name for the report title |
| `--policy nist\|eo14412-hva\|cnsa2` | Which deadline policy dates the findings (default `nist`) |
| `--scope FILE` | Declared scope: findings the scanner says it doesn't cover are listed, not scored |
| `--exclude-custom` / `--only-custom` | The shipped benchmark only (comparable with anyone's), or your own cases only |
| `--tolerance N` | Line-number tolerance (default 1) |
| `--as-of DATE` | The date deadlines are judged from |
| `--out PREFIX` | Output path prefix (default `reports/<cbom stem>`) |

A scanner whose native format isn't CycloneDX 1.6 needs an adapter in `tools/adapters/`; two ship
(`qci-pqc`, `cdxgen`). `tools/compare.py` puts scorecards side by side and refuses ones measured on
different releases.

### Reproducible runs and evidence bundles

For a score someone else has to trust, use `tools/bench.py`. `run` scans in the sandbox, scores and
writes a bundle; `verify` re-derives every number in a bundle; `checks` runs the benchmark's own
required checks; `perf` times a scanner on a large generated tree.

| Option (`bench.py run`) | What it does |
|---|---|
| `--scanner-cmd "..."` | The command line; `{corpus}` and `{out}` are filled in |
| `--bundle DIR` | Where the evidence bundle goes |
| `--adapter qci-pqc\|cdxgen` | Translate the scanner's native output first |
| `--scope FILE`, `--gates FILE` | Declared scope; gates to evaluate (exit 1 fail, 3 not evaluated) |
| `--remediation` | Also apply the ten reference migrations, rescan, and score verified remediation |
| `--require-isolation` | Refuse to run without both the network cut and the filesystem boundary |
| `--allow-path PATH` | A path the scanner may read although it sits in a hidden location (recorded) |
| `--scanner-image IMAGE` | Run the scanner in its own container: the strongest lane |
| `--version-cmd`, `--scanner-version` | How the scanner's version gets into the bundle |
| `--without-holdout` | No holdout on purpose: the holdout gates are recorded as skipped, not missing |

- **The sandbox** (`tools/sandbox.py`) gives the scanner a private copy of the corpus, read-only
  where the host allows, hashed before and after: a scanner that changes its input isn't scored. The
  environment is scrubbed (no credentials, never the holdout seed), the network is cut, and
  wall-clock, CPU, memory and file-size limits apply.
- **The filesystem boundary** hides home and temp directories, the whole benchmark tree (answer key,
  evidence, reports) and any holdout set behind empty mounts. It needs a mount namespace; without
  one the run is recorded as "not confined" and `--require-isolation` refuses.
- **The container lane** is for a scanner you don't trust at all. It runs in an image that holds only
  the scanner (`integrations/scanner-image.Dockerfile` builds one from wheels), with no network, a
  read-only root, no capabilities, the corpus mounted read-only and one output directory. QCI
  v2.3.4.1 scores the same in both lanes (`evidence/qci-v2.3.4.1-container/`).
- **The build step isn't sandboxed**: `pip install` runs the scanner's code and needs the network.
  For someone else's scanner, build in a job with no secrets and score in another;
  `integrations/qci-pqc/github-workflow.yml` does that, and
  `.github/workflows/third-party-scanners.yml` runs three open-source scanners with no secrets at all.
- **The bundle** holds the scanner's raw output, the adapted CBOM, the scorecards, a manifest (the
  release stamp, the hash of every file that decides a score, the scanner's command and version, the
  sandbox record) and `SHA256SUMS`. `bench.py verify` re-derives every scorecard section from the raw
  CBOM, so a doctored number fails even with recomputed checksums. The one thing a bundle can't prove
  alone is the holdout result, because the seed is private; verify says so, and re-derives it once
  the seed is revealed.
- **Big trees.** `bench.py perf` generates 600, 3,000 or 12,000 code files with Tier 1 uses planted
  evenly, gives the scanner a time budget, and reports time, memory, throughput and recall by
  quarter of the tree. A scanner that gives up partway shows it as a drop in the last quarter.
- **The image** (`Dockerfile`) pins every toolchain and verifies the corpus at build time.
  `.github/workflows/image.yml` builds it from the real base images on pull requests that touch it;
  on a version tag, `release.yml` builds it, runs the required checks inside with no network, and
  attaches the evidence to the GitHub release.

### Policies and deadlines

Detection rates treat a missed MD5 checksum the same as a missed key exchange that has to be gone by
2030. Organizations don't, so every expected finding is dated under a transition policy, and the
scorecard adds recall by due date, a deadline-weighted recall, and the list of findings due by 2030
that the scanner missed. `tools/policy_report.py` does the same for any CycloneDX 1.6 CBOM, not just
this corpus.

| Option (`policy_report.py`) | What it does |
|---|---|
| `--policy ID` | Policy in `policies/` (repeatable; default `nist`) |
| `--use-map FILE` | `[glob, use]` pairs for CNSA 2.0, whose dates depend on system type (firmware-signing, networking, web, os, niche, custom) |
| `--as-of DATE` | The date deadlines are judged from |
| `--name`, `--out` | Report title and output prefix (writes `.md`, `.csv`, `.json`) |

| Policy | Covers | Key dates |
|---|---|---|
| `nist` (default) | NIST IR 8547 **final** (Oct 27, 2026), SP 800-131A Rev. 2, FIPS 186-5, SP 800-52 Rev. 2, NIST's 2022 SHA-1 notice | All quantum-vulnerable public-key crypto deprecated after 2030, disallowed after 2035, at any key size. SHA-1 ends Dec 31, 2030. RSA/DH below 2048, DSA signing, 3DES, MD5, TLS < 1.2 are already out. |
| `eo14412-hva` | Executive Order 14412 (June 22, 2026) for federal high value assets and high impact systems; inherits `nist` | PQC key establishment by Dec 31, 2030; PQC signatures by Dec 31, 2031. |
| `cnsa2` | NSA CNSA 2.0 | Only AES-256, ML-KEM-1024, ML-DSA-87, SHA-384/512 (and LMS/XMSS). CNSA 1.0 strengths (RSA-3072+, P-384) until the system type's exclusive-use date: 2030 for firmware signing and networking, 2033 for web/cloud, OS, niche and custom. |

- **The final IR 8547 is stricter than the draft.** The November 2024 draft let 128-bit-and-up keys
  (RSA-3072, P-256, Ed25519) run to 2035 while 112-bit keys stopped in 2030. The final deprecates
  all of them after 2030. Tools and slide decks built on the draft are now wrong.
- **Overlays only tighten.** `eo14412-hva` inherits `nist`, and the stricter verdict wins, so DSA
  stays disallowed since 2023 even though the order's signature date is 2031.
- **The same scan reads very differently by policy.** Grep misses 28 findings due by 2030 under
  `nist`, 48 under `eo14412-hva`, and 60 under `cnsa2`, where nearly everything that isn't CNSA
  grade is non-compliant today.
- **CNSA dates depend on system type.** `policy_report.py --use-map` takes `[glob, use]` pairs;
  the default guesses from the path (`*/ssh/*` → networking, `*firmware*` → firmware signing).
  Uses are firmware-signing, networking, web, os, niche and custom.
- **Missing parameters are judged honestly.** An RSA key of unknown size is dated as quantum-vulnerable
  under NIST, but can't be shown CNSA 1.0-strong, so CNSA marks it non-compliant. A scanner that
  doesn't report key sizes pays for it here.
- **What's deliberately not encoded**: SP 800-131A Rev. 3 is still a draft, so its proposals (retire
  ECB, SHA-224, 112-bit security) appear only as notes. ChaCha20-Poly1305 is "not approved" under
  NIST; that's a FIPS-scope finding, not a security one.

Policies are data in `policies/*.json`. Every rule names its source document, revision and section,
and `tools/test_policy.py` enforces that. `reports/corpus-deadlines.md` is a sample run on the whole
corpus.

### BYOC

The shipped corpus measures crypto in general. `tools/byoc.py` adds your organization's own patterns
(in-house wrappers, vendor SDK usage, framework configs) as scored cases, kept in `corpus/custom/`
and `expected/custom/` so upgrades never collide. Walkthrough in [BYOC.md](BYOC.md).

| Command | What it does |
|---|---|
| `byoc.py new CASE --lang LANG` | Scaffolds a runnable case and its answer key |
| `byoc.py draft CASE [--write]` | Proposes candidate findings from a naive scan, marked unconfirmed |
| `byoc.py add CASE --file F --alg RSA-2048 --anchor TEXT [--confirm]` | Records a finding by its ordinary name; rejects ambiguous anchors and duplicates |
| `byoc.py check [CASE...]` | Runs each case and lints for credentials, real hostnames, and comments that name the algorithm |
| `byoc.py list` | Lists your cases |

Nothing is scored until a person confirms it. A worked example ships in
`corpus/custom/example_envelope/`: an in-house envelope library where application code picks
`profile="LEGACY_COMPAT"` and never names an algorithm.

## Outputs

| File | Written by | What it is |
|---|---|---|
| `reports/<name>.md`, `.json` | `score.py` | The scorecard: recall, primary-site recall, parameters, precision, PQC over-claims, actionability, deadlines, libraries, per bucket with 95% intervals |
| `<bundle>/` | `bench.py run` | Evidence bundle: raw output, adapted CBOM, scorecards, `manifest.json`, `SHA256SUMS`, and `remediation.*`, `gates.*`, `checks.json` when asked for |
| `<bundle>/gates.md`, `gates-result.json` | `bench.py run --gates` | Gate verdict: pass, fail, or not evaluated, with every gate listed |
| `reports/comparison.md`, `.json` | `compare.py`, `render_docs.py` | Scanners side by side on one denominator |
| `reports/<name>-deadlines.md`, `.csv`, `.json` | `policy_report.py` | Every finding dated under each policy |
| `checks.json` | `bench.py checks` | The benchmark's own required checks, pass or fail |
| `expected/expected.cdx.json` | `build_expected.py` | The reference CBOM: what a perfect scanner would produce |

## What the tiers test

Each tier removes something a scanner could lean on: first the literal at the call site, then the
file boundary, then source code altogether, then the name itself.

| Tier | What it tests | Findings |
|---|---|---|
| **1. Direct** | Algorithm and parameters are literals at the call site. `hashlib.md5()`, `Cipher.getInstance("AES/ECB/PKCS5Padding")`, `kpg.initialize(3072)`, Go's `md5.Sum` and `rsa.GenerateKey(rand.Reader, 2048)`, Node's `createCipheriv("des-ede3-cbc", ...)` and Web Crypto, .NET's `MD5.HashData`, `RSA.Create(2048)` and `new AesGcm(key, 16)`, OpenSSL's `EVP_aes_128_ecb()`, the pre-3.0 `RSA_generate_key_ex`, and TLS versions and suites set in code (`tls.Config`, `SSL_CTX_set_cipher_list`). | 102 (16 Python, 16 Java, 20 Go, 17 JavaScript, 20 C, 13 C#) |
| **2. Indirection** | Same file, but the algorithm or its parameters arrive via a constant, alias import, config file, env var or system property default, wrapper function, dispatch table, enum, `functools.partial`, or string concatenation. Go adds a `crypto.Hash` value in a variable and constructors passed as function values; TypeScript adds `as const` config objects and template literals; C adds macros, OpenSSL 3 `EVP_CIPHER_fetch` by name, function pointers and constructor tables. C# adds `const` settings, `IncrementalHash` by name, a `Func<HashAlgorithm>` table and a curve chosen by a helper. | 42 (9 Python, 8 Java, 6 Go, 7 TypeScript, 6 C, 6 C#) |
| **3. Cross-file flow** | Multi-file projects. Algorithm names and key sizes defined in one module and used in another; a shared wrapper called with two different key sizes; decorator registries and strategy factories; constructor dependency injection; JWT `alg` read from `.ini` / `.properties` and resolved through a lookup table. | 16 (9 Python in 5 projects, 7 Java in 4 projects) |
| **4. Non-code assets** | X.509 certificates (PEM, DER, a two-cert chain, one SHA-1-signed); private keys (PKCS#8, SEC1 on secp256k1, password-encrypted PKCS#8); a JWKS; a PKCS#12 keystore and a JKS truststore; an sshd_config, an SSH host public key and an OpenSSH private key; nginx, Apache httpd, HAProxy, Spring Boot and OpenSSL TLS configs (HAProxy sets its DH group size on a tuning line, away from the ciphers); strongSwan IPsec proposals in both `swanctl.conf` and legacy `ipsec.conf` spelling (`aes256-sha256-modp2048`); a Kubernetes TLS secret with the certificate base64-encoded inside YAML. | 68 |
| **5. Adversarial** | Names assembled at runtime (fragments, base64, `chr()` codes, reversed strings, char arrays); `importlib` and Java reflection; hand-rolled RC4, SHA-256, TEA and textbook RSA with no crypto library call at all; a `.pyc` and a `.jar` with no source; a ProGuard-obfuscated `.jar` (every name replaced, algorithm strings intact); three minified JavaScript bundles (one line each; algorithm names hoisted into one-letter constants, crypto functions destructured so no call names its module); three stripped ELF binaries, where an algorithm is an imported libcrypto symbol, a name string fetched at runtime, or a number passed as an immediate operand. | 42 (9 Python, 11 Java, 11 JavaScript, 11 C) |
| **PQC** | ML-KEM-768/1024 and ML-DSA-44/65/87 via `cryptography`, the JDK 24+ JCA and Go's `crypto/mlkem`; Go `tls.Config` preferring `X25519MLKEM768` with an X25519 fallback; including a parameter set passed through a constant or `NamedParameterSpec`; an application-level X25519 + ML-KEM hybrid; ML-DSA certificates, one PQ key signed by a classical RSA CA; ML-KEM and ML-DSA key files; hybrid groups (`X25519MLKEM768`, `SecP384r1MLKEM1024`) in nginx and OpenSSL configs; `mlkem768x25519-sha256` and `sntrup761x25519` in sshd_config; two PQC-washing decoys plus a washing config; and LMS and XMSS: Bouncy Castle signing code, HSS/LMS and XMSS public keys identified only by OID, and a firmware signing policy that names both next to the P-384 signer it keeps for old devices. | 44 (7 Python, 6 Java, 4 Go, 27 assets) |
| **Mixed** | Realistic-size modules, 220 to 520 lines, with three to five crypto uses spread through ordinary code: CSV parsing, pagination, retries, money formatting, logging. Most files use one family twice with different parameters (AES-128-CBC and AES-256-CTR, HMAC-MD5 and HMAC-SHA512, P-256 and P-521); the surrounding code has numbers a guesser will grab (page sizes of 256, buffers of 32 bytes, `bit_length()`); log lines and note dictionaries name algorithms the file doesn't use, including PQC claims. Scored per site, not per file. | 62 sites in 15 files (3 Python, 3 Java, 3 Go, 2 JavaScript, 1 TypeScript, 3 C) |
| **Dead code** | Crypto that ships and never runs: a function nothing calls, a branch behind a constant that is always false, statements after a `return`. It counts, because it's in the artifact an auditor will read and one config flip away from running. A scanner that prunes unreachable code misses all of it. | 10 (2 each in Python, Java, Go, JavaScript, C) |
| **Negatives** | Algorithm names in docstrings, comments, UI labels, log messages, identifiers and a Markdown runbook; known-answer test vectors; CRC32, Adler32, Base64, `hash()`; a file with valid PEM armor around base64 that isn't a certificate; and code that reuses crypto's constants and math for other jobs (Fibonacci hashing with TEA's constant, `pow()` for an IBAN check, `modPow` in a primality test); in Go, JavaScript and C, algorithm names in string tables, display labels and changelog comments next to FNV, CRC32 and djb2. Zero real crypto. | 12 files |

Positive files also carry **decoys**: comments mentioning ML-DSA and X25519MLKEM768 in files that
use neither, and commented-out `SSLv3` and RC4 lines in `nginx.conf`. A scanner reporting
post-quantum algorithms where none exist is flattering the codebase, which is worse than missing
something.

**Test files never describe their own crypto.** Comments say what pattern a case tests ("key size
held in a constant"), never which algorithm or size it uses. Earlier versions did, and grep was
reading key sizes out of comments: cleaning them up dropped its Tier 1 Java parameter score from
87.5% to 56.2%. Case descriptions live in this README and in the ground truth's `note` fields.

Coverage: MD5, SHA-1, SHA-256, SHA3-256, RSA, DSA, ECDSA, Ed25519, X25519, DH, AES, 3DES, HMAC and
PBKDF2 have at least one case in each code language. 147 of the 410 findings are Shor-vulnerable, 97
are classically broken, and 28 are post-quantum (6 hybrids, 7 stateful). 304 generated calibration
cases top up the Tier 1-2 cells for the overfit gap; they are scored but kept out of every headline
number.

### Tier 4 cases worth knowing about

- **`keystores/orders_keystore.p12`**: the container's own protection (AES-256-CBC, PBKDF2-HMAC-SHA256)
  is visible without a password. The RSA key and its certificate are inside encrypted bags and need
  the password, which is `changeit`, the Java default. Two findings are marked `requires_password`.
  A scanner that tries default passwords finds them. One that doesn't should at least report the
  container. Real estates are full of `changeit`.
- **`keystores/partner_truststore.jks`**: JKS trusted-certificate entries are readable *without* the
  store password. It holds a SHA-1-signed, 1024-bit RSA root, with no excuse for missing it.
- **`keys/backup_signing_encrypted.pem`**: an encrypted PKCS#8 key. The key's own type is unknowable
  without the password; the PBES2 parameters (PBKDF2-HMAC-SHA256, AES-256-CBC) are the findings.
- **`keys/treasury_hot_wallet.key`**: an EC key on secp256k1. Naive curve matching reads `SECP256K1`
  as NIST P-256 because the string contains `P256`. This testbench's own normalizer had exactly that
  bug until a test caught it.
- **`certs/portal_fullchain.pem`**: two certificates in one file. The leaf is EC P-384, signed with
  SHA-384 by an RSA-3072 intermediate; the intermediate is SHA-256-signed by a root that isn't in the
  file. A scanner reading only the first certificate misses half of it.
- **`k8s/ingress-tls-secret.yaml`**: a PEM certificate, base64-encoded again inside YAML. Scanners
  have to decode twice.
- **`tls/openssl.cnf`**: `default_bits = 1024` and `default_md = sha1` mean every CSR built in that
  image gets a 1024-bit RSA key and a SHA-1 signature. Nothing in the file says "RSA".

### Tier 5 cases worth knowing about

Expect low scores here. Nobody has run commercial scanners through this tier yet, so that's a
prediction, not a result. A low score is less a failure than a map of what the scanner can't see.
What matters is whether the vendor knows where its blind spots are, and says so.

- **Runtime assembly** (`t5_string_assembly.py`, `t5_char_codes.py`, `T5StringAssembly.java`):
  the call is a normal library call; only the name is hidden. Constant folding and simple
  string evaluation recover all of these. A scanner that resolves `"s" + "ha" + "1"` but not
  `base64.b64decode("bWQ1")` tells you exactly how deep its evaluator goes.
- **Reflection and dynamic import** (`T5Reflection.java`, `t5_dynamic_import.py`): no static call
  graph edge to the crypto API exists. Plugin systems and DI frameworks look like this for
  legitimate reasons, so it's common in real code.
- **Hand-rolled algorithms** (`t5_handrolled_keystream.py` is RC4, `t5_handrolled_digest.py` is
  SHA-256, `T5BlockTransform.java` is TEA, the two `*_pubkey` files are textbook RSA): no import, no
  API, no name. Detection needs structure or constants: the 64 SHA-256 round constants, TEA's
  `0x9E3779B9`, RC4's 256-entry swap loop, `pow(m, 65537, N)`. Each is verified against a reference
  implementation by `verify_corpus.py`, so "that isn't really RC4" isn't an available excuse.
- **Lookalike negatives** pair with the hand-rolled cases. `n_fibonacci_hash.py` uses
  `0x9E3779B9` for hashing, and `n_iban_check.py` and `NPrimeCapacity.java` use modular
  exponentiation for checksums and primality. A scanner that flags constants or `pow()` without
  context will light these up.
- **Compiled-only** (`compiled/ledger_sync.pyc`, `compiled/billing-core.jar`): the source is in
  `tier5-sources/`, outside the corpus. The jar is compressed, so plain grep sees nothing. The
  `.pyc` still carries literal strings in its constant table. Bytecode analysis finds both;
  source-only scanners find neither. The `.pyc` is tied to Python 3.13; rebuild it with
  `tools/build_tier5_compiled.py` for another version.
- **Obfuscated jar** (`compiled/token-vault.jar`): ProGuard replaced every class, method and field
  name and flattened the packages. Algorithm strings survive (`"DES/ECB/PKCS5Padding"`,
  `"secp256r1"`), so the findings are there for a scanner that reads the constant pool, and nowhere
  for one that relies on class names.
- **Minified JavaScript** (`dist/*.min.js`, three bundles): one line each. In `session-tokens` the
  cipher name is hoisted into a one-letter constant. In `payments-sdk` the names were values of a
  config object and are now four constants, one of them two hops from the `createHmac` call. In
  `webhook-relay` the crypto functions were destructured, so `createCipheriv("aes-256-gcm", ...)`
  reads `e("aes-256-gcm",t,n)` and `getDiffieHellman("modp2")` reads `n("modp2")`: nothing at the
  call says which module it belongs to, and `modp2` has to be known as a 1024-bit group.
- **Stripped native binaries** (`c/bin/`, three ELF files linked to libcrypto), each a different
  kind of evidence. `meterd` and `keyd` call `EVP_md5()`, `EVP_aes_256_gcm()` and the like, so the
  algorithms are imported symbol names; key size and curve are numbers passed as immediate operands
  (1024, NID 415). `fwcheck` fetches everything by name (`EVP_MD_fetch(NULL, "SHA2-512", NULL)`), so
  it imports no algorithm-specific symbol at all and the names are strings in read-only data,
  including `ffdhe2048` for the DH group. Each binary runs a self-test in `verify_corpus.py`.

Where a hand-rolled finding lives: the function that implements it, with the constant table or
modulus as an alternate anchor. Reporting the caller instead counts as a miss at the primary
site, which matches what an engineer needs: the code to delete.

## The PQC category

Detection of classical crypto answers "what do we have to replace?" This category answers the
question that follows for the next decade: "how much have we replaced?" A scanner that can't see
deployed PQC reports 0% migrated forever. One that believes labels reports progress that isn't there.

- **Hybrids are their own thing.** `X25519MLKEM768`, `SecP384r1MLKEM1024`, OpenSSH's
  `mlkem768x25519-sha256` (the same combination under another name) and `sntrup761x25519` are each
  a family. Reporting only the X25519 half calls a migrated endpoint vulnerable; reporting only
  ML-KEM overstates it. In code, an application-level hybrid (`pq_hybrid_kem.py`) is scored as its
  two components, because that is how it's written.
- **Classical fallbacks are required findings.** `ssl_ecdh_curve X25519MLKEM768:X25519` still
  negotiates plain X25519 with any client that lacks PQ support. An inventory that lists only the
  hybrid hides the exposure.
- **`certs/migrated_leaf.pem`** carries an ML-DSA-65 key but is signed by an RSA CA. The key is
  post-quantum; the certificate's authenticity isn't. Expect scanners to report it as "PQC" and stop.
- **`ssh/sshd_config_pq`** has post-quantum key exchange and classical Ed25519 host authentication.
  Recorded traffic is protected; host impersonation by a future quantum adversary isn't.
- **Parameter sets matter.** ML-KEM-512 and ML-KEM-1024 are different security levels, and CNSA 2.0
  asks for 1024. Wrong or missing parameter sets count as wrong parameters.
- **OIDs.** Crypto libraries that predate PQC (OpenSSL 3.0, for one) show an ML-DSA key as
  `2.16.840.1.101.3.4.3.18`. The scorer accepts ML-KEM and ML-DSA OIDs in a component's name or
  `cryptoProperties.oid`. The pre-standard names (Kyber, Dilithium, SPHINCS+, Falcon, the
  `X25519Kyber768Draft00` codepoint) still earn discovery credit, but fail the separate
  **PQC by standard name** check: they aren't the FIPS 203/204/205 algorithms.
- **ML-DSA is not DSA.** A naive matcher reads `ML-DSA` as classical DSA and flags a migrated
  signer as legacy. Grep does exactly this on both Java signature cases.
- **PQC-washing decoys** (`pq_washing.py`, `PqWashing.java`, `nginx_pq_washing.conf`) have names,
  comments and docstrings that claim ML-KEM, over code and configs that are purely classical. Every
  PQ finding a scanner reports there is a **PQC over-claim**, scored separately because it's the
  most expensive false positive a migration program can have: it marks unfinished work as done.

The Java PQC cases use the standard JCA names that arrived in JDK 24 (`KeyPairGenerator.getInstance("ML-KEM-1024")`,
`KEM`, `Signature.getInstance("ML-DSA")`). They compile on JDK 21 and fail at runtime without a 24+
runtime; `verify_corpus.py` uses `jdk4py`'s Java 25 runtime when the system Java is older, and skips
them with a note when neither is available.

The LMS and XMSS cases use Bouncy Castle (`KeyPairGenerator.getInstance("LMS", "BCPQC")`), because the
JDK has neither. Both are stateful: each signature spends a one-time key, and signing twice from the
same state breaks the scheme. That is the reason to inventory them separately from ML-DSA, and why the
corpus ships their public keys only.

There is also LMS with no library at all: `corpus/pqc/python/firmware_verify_lms.py` implements RFC
8554 signing and verification on `hashlib` alone, the way firmware verifiers often do. Nothing in
it is an API call a scanner knows; what identifies it is the parameter-set constants
(`LMS_SHA256_M32_H5`, `LMOTS_SHA256_N32_W8`) and the shape of the code. Its signatures verify under
Bouncy Castle and Bouncy Castle's verify under it.

## How scoring works

The normative rules are in [METHODOLOGY.md](METHODOLOGY.md), versioned separately from the
benchmark. Every scorecard records the version it was produced under, and scorecards from different
versions are never compared.

> **Recall is not the number to trust. Primary-site recall is.**
> Grep scores 100% recall through Tier 3 in Python and Java. That isn't a corpus bug: somewhere in
> every project the algorithm name is a string, and text search finds strings. So the scorecard has
> two recall numbers. **Recall** gives credit for reporting the finding anywhere acceptable,
> including the config file that names it. **At primary site** gives credit only when it lands in
> the file the answer key anchors it to: the crypto call, or for a shared wrapper, the caller that
> binds the parameters. "SHA-1, somewhere in `settings.py`" is correct and useless to the engineer
> who has to fix it. Three Tier 3 cases exist to punish name-only matching: `wrapper_two_callers`
> (one RSA wrapper called with 1024 and 3072), `cross_class_constant` (no algorithm string in the
> file at all) and `jwt_alg_mapping` (resolvable only by following config, lookup table, call).

- **Detected:** the scanner reports the same algorithm *family* in the expected file. For config-
  driven and cross-file cases, reporting it in a listed `alt_files` location also counts. Names are
  normalized first, so `SHA1withRSA`, `sha1WithRSAEncryption`, `RSA-2048`, `ssh-rsa` and the JWS name
  `RS256` all count as RSA. See `tools/cbomlib.py`.
- **Mixed files are scored per site.** A mixed file can hold two findings of one family (AES-128 in
  one helper, AES-256 in another). Each reported occurrence is credited to the site whose anchor line
  is nearest, if it is within 3 lines, and parameters are judged on that site's occurrences only. So
  "AES-256" reported once at the top of the file finds neither site, and the first site's parameters
  copied to the second are wrong for the second. An occurrence with no line can't be placed. A report
  in the right file but nowhere near a site credits nothing and is counted as a false positive (see
  **False positive** below).
- **At primary site:** detected in the finding's own `file`, not just an alt file.
- **Params correct:** every expected parameter matches (key size, curve, mode, HMAC/PBKDF2 hash, or
  PQC parameter set such as ML-KEM-768)
  **within a single reported component**. Read from the component name or from `algorithmProperties`
  (`parameterSetIdentifier`, `curve`, `mode`). Reporting "AES-CBC" in one place and "AES 256" in
  another does not add up to AES-256-CBC.
- **Line accurate:** a reported line is within ±1 (`--tolerance`) of any anchor line. Both the
  usage site and the defining constant are valid anchors. Binary and PEM assets are file-level and
  aren't judged on lines.
- **Quantum flag:** if the scanner sets `nistQuantumSecurityLevel`, it must be 0 exactly when the
  expected level is 0 (Shor-vulnerable or classically broken).
- **False positive:** a (file, family) pair the scanner reports that matches no finding and isn't
  listed in `also_ok`. Example of `also_ok`: SHA-256 reported inside `SHA256withRSA` isn't noise.
  In mixed files, where the truth is per site, it's per occurrence: a reported line that belongs to
  no site of that family (more than 3 lines from every anchor) is its own false positive, even when
  the file genuinely uses the family elsewhere. Lines close to each other count once. Two cases are
  neutral, neither credit nor noise: a report on an import/include/require line, and a hash or MAC
  reported at another algorithm's site (HMAC at a `pbkdf2_hmac` call). DES reported at a 3DES site is
  still a false positive.
- **Declared scope** (`--scope`): findings excluded by id are listed, not scored, but only a glob
  rule (the scanner says it doesn't read that file) also suppresses the file's false positives.
  Excluding one RSA finding on a certificate doesn't silence a false ML-KEM on the same file.
- **PQC over-claims:** the subset of false positives whose family is post-quantum or hybrid. Shown on
  its own line in every scorecard.
- **PQC by standard name:** detected post-quantum findings where at least one report uses the FIPS
  203/204/205 name or OID rather than Kyber, Dilithium, SPHINCS+ or Falcon.
- **Unrecognized:** names the normalizer can't classify (padding schemes, RNGs, container formats
  like `PKCS12`) are listed for manual review and **not** penalized.

All four CycloneDX 1.6 asset types are read:

| Asset type | What the scorer extracts |
|---|---|
| `algorithm` | The algorithm, from `name` plus `algorithmProperties`. |
| `certificate` | Follows `subjectPublicKeyRef` (the key) and `signatureAlgorithmRef` (the signature). |
| `related-crypto-material` | Follows `algorithmRef`; `size` becomes the key size. |
| `protocol` | TLS `version` becomes a family like `TLS-1.0`; each `cipherSuites[].name` becomes a suite family, in IANA or OpenSSL spelling. |

Compound signature names also yield their hash, so a `sha1WithRSAEncryption` certificate surfaces
SHA-1 as well as RSA. A certificate reported as a bare container, with no key or signature
references, yields nothing. That's deliberate: "there is a certificate here" isn't an inventory.

Locations inside an archive (`billing-core.jar!/com/acme/billing/Settlement.class`, with or without
a `jar:file:` prefix) are attributed to the archive file.

Duplicates don't hurt: five occurrences of HMAC in one file collapse to one finding (in a mixed
file, to one finding per site).

### Actionability

Detection asks whether the scanner found it. Actionability asks whether an engineer could open a
migration ticket from what it reported. Every detected finding is checked against
`rubric/actionability.json`:

| Must have (no ticket without it) | Should have (the ticket bounces back without it) |
|---|---|
| Exact location: the line for code, the file for assets | OID |
| Correct parameters | Crypto functions (`sign`, `encrypt`, `keyderive`...) |
| Primitive, where the family is ambiguous (RSA: ML-KEM or ML-DSA replacement? EC: ECDH or ECDSA?) | Correct quantum security level |
| Certificates: **correct** expiry date and subject | Code context (`symbol` or `additionalContext`) |
| Keys: key material type (private or public) | Providing library (`dependencies[].provides`) |
| Protocols: version | Certificate issuer, start date, key and signature both linked; key format; suites inside a protocol |

Certificate facts are checked against the real files, not for presence: a wrong expiry date fails.
The scorecard reports **ticket-ready** (every must-have present and correct), **actionable recall**
(found and ticket-ready, over all expected findings) and **field completeness**. The rubric is
proposed, not official: no official minimum CBOM elements exist yet.

## Calibration / baseline

Three runs ship with every release, so a new scorecard has something to be read against:

<!-- generated:calibration-points (tools/render_docs.py; edit the scorecards, not this table) -->
| Run | Findings | Recall | At primary site | Params correct | False positives | Precision | PQC over-claims | Ticket-ready | Actionable recall |
|---|---|---|---|---|---|---|---|---|---|
| `expected/expected.cdx.json` (the answer key) | 410 | 100.0% | 100.0% | 100.0% | 0 | 100.0% | 0 | 100.0% | 100.0% |
| `reports/reference-names-only.cdx.json` (answer key, names and locations only) | 410 | 100.0% | 100.0% | 100.0% | 0 | 100.0% | 0 | 75.6% | 75.6% |
| `tools/baseline_grep.py` (naive regex) | 410 | 67.1% | 63.4% | 56.0% | 171 | 61.7% | 28 | 51.3% | 34.4% |

Shipped corpus only (BYOC example cases excluded), so every row has the same denominator.
<!-- /generated:calibration-points -->

Grep by tier, which is the shape to expect from a weak scanner:

<!-- generated:grep-by-tier (tools/render_docs.py; edit the scorecards, not this table) -->
| Tier | Findings | Recall | At primary site | Params correct |
|---|---|---|---|---|
| 1. Direct, Python and Java | 32 | 100% | 100% | 56.2–75% |
| 1. Direct, Go / JavaScript / C | 57 | 65–82.4% | 65–82.4% | 42.9–85.7% |
| 1. Direct, C# | 13 | 92.3% | 92.3% | 58.3% |
| 2. Indirection, Python and Java | 17 | 100% | 87.5–88.9% | 50–55.6% |
| 2. Indirection, Go / TypeScript / C | 19 | 83.3–100% | 83.3–100% | 33.3–60% |
| 2. Indirection, C# | 6 | 83.3% | 83.3% | 40% |
| 3. Cross-file | 16 | 100% | 42.9–55.6% | 33.3–42.9% |
| 4. Non-code assets | 66 | 34.8% | 34.8% | 69.6% |
| 5. Adversarial, source and bytecode | 20 | 0% | 0% | n/a |
| 5. Adversarial, minified JS and native binary | 22 | 63.6–72.7% | 63.6–72.7% | 57.1–75% |
| PQC, code | 17 | 50–85.7% | 50–85.7% | 25–50% |
| PQC, assets | 27 | 37% | 37% | 90% |
| Mixed files | 62 | 69.2–100% | 69.2–100% | 18.2–50% |
| System fixture | 26 | 18.2–100% | 0–66.7% | 33.3–100% |
| Dead code | 10 | 50–100% | 50–100% | 100% |

Ranges run across the languages in each row.
<!-- /generated:grep-by-tier -->

> **Grep is the floor.** The reference run proves the scorer agrees with the answer key. The grep
> run is what regular expressions get with no analysis at all. A commercial scanner that can't beat
> it on parameters and precision is a grep with a logo. The names-only row is the answer key with
> OIDs, functions, quantum levels and certificate metadata stripped: it finds everything, and a
> quarter of what it finds can't become a ticket.

## Holdout and overfit gap

`tools/holdout.py` generates fresh, executable variants of the published patterns from a private
seed (new code, same APIs and kinds of indirection), scores a scanner on them, and reports the
**overfit gap**: published recall minus holdout recall, cell by cell, with a 95% interval. A second
gap compares false positives per negative-control file (gated at +0.5), which catches a scanner that
suppressed false positives only until the published negatives were clean.

Generator 1.2 covers every code language, certificates, keys, keystores, TLS, SSH and IPsec configs,
firmware signing policies, and compiled, minified and native artifacts. Calibrated over five seeds on
this release: the answer key reads 0 on every seed, a memorizer +100, grep -4.0 to -2.2 and QCI
v2.3.4.1 -0.9 to +1.0, none significant. On the negative controls grep reads 0 to +0.36 per file and
QCI 0 to +0.04. Details, the generator's limits and how to keep a seed private are in
[HOLDOUT.md](HOLDOUT.md).

## Crypto libraries / system fixture

**Crypto libraries.** `corpus/deps/` holds dependency manifests for seven applications declaring 26
crypto libraries; `expected/libraries.json` records each one's version, whether that version ships
ML-KEM and ML-DSA, and the primary source that says so. The scorecard reports libraries found in the
right manifest, version accuracy, transitive coverage and, where a scanner gives one, whether its
post-quantum verdict is right.

| Manifest | What it tests |
|---|---|
| `python-billing/requirements.txt` | Six pinned crypto libraries (cryptography 41.0.7, PyCryptodome, pyOpenSSL, PyJWT[crypto], Paramiko, bcrypt), a commented-out `pycrypto` line, and `hashids`, which sounds like crypto and isn't |
| `python-signer/pyproject.toml` | PEP 621 dependencies: a version *range* (`cryptography>=48,<51`) and liboqs-python |
| `java-gateway/pom.xml` | Bouncy Castle 1.70 through a `${bc.version}` property, on the superseded `-jdk15on` artifacts; Nimbus JOSE+JWT; JJWT; Jasypt inside an XML comment |
| `java-pq/build.gradle` | Bouncy Castle 1.80 (`-jdk18on`), which has the final ML-KEM and ML-DSA |
| `node-api/package.json` + `package-lock.json` | jsonwebtoken, crypto-js (discontinued upstream), node-forge, bcryptjs, @noble/post-quantum; and four *transitive* crypto libraries that only the lockfile shows. The lockfile was generated by npm, not typed |
| `go-service/go.mod` | golang.org/x/crypto, Cloudflare CIRCL, golang-jwt |
| `c-agent/conanfile.txt` + `CMakeLists.txt` | OpenSSL 1.1.1w (end of life since 2023-09-11) and libsodium |

**The system fixture.** `corpus/system/payments-platform/` is one application instead of one file: a
Go API, a Python worker and a Java service sharing a crypto wrapper and its config, with lockfiles,
a built JAR and a stripped Go binary, nginx TLS termination, a Kubernetes TLS secret, KMS keys in
Terraform, a certificate pasted into source, and CODEOWNERS. It adds two numbers only a system can
produce: **routable** (a reported location resolves, through CODEOWNERS, to the team that owns the
fix; reporting only the shared wrapper doesn't) and **asset links** (the CBOM connects the nginx
config to its certificate and the certificate to its key). Definitions in
[METHODOLOGY.md](METHODOLOGY.md) section 4a.

## Documentation index

| Document | What's in it |
|---|---|
| [METHODOLOGY.md](METHODOLOGY.md) | The scoring rules, versioned: matching, false positives, metrics, scope, gates, execution |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each release |
| [HOLDOUT.md](HOLDOUT.md) | Holdout sets, the overfit and negative-control gaps, calibration, limits |
| [BYOC.md](BYOC.md) | Adding your own code as scored cases |
| [reports/comparison.md](reports/comparison.md) | Published results, scanners side by side |
| [reports/qci-pqc/SUMMARY.md](reports/qci-pqc/SUMMARY.md) | QCI scanner v2.3.4.1: scorecard summary and gate verdict |
| [integrations/qci-pqc/FINDINGS.md](integrations/qci-pqc/FINDINGS.md) | What the QCI scanner misses and gets wrong, for its team |
| [integrations/cdxgen/NOTES.md](integrations/cdxgen/NOTES.md) | What cdxgen 12.9.1 finds, misses and gets wrong |
| [integrations/third-party/README.md](integrations/third-party/README.md) | Open-source scanners run on GitHub, and what must be read before one is published |
| [evidence/](evidence/) | An evidence bundle for every published scorecard; check one with `bench.py verify` |

## Layout

```
corpus/                     what a scanner reads
  tier1/ tier2/               single-file cases per language (C# is one project per case)
  tier3/                      multi-file Python and Java projects
  tier4/assets/               certs/ keys/ keystores/ ssh/ tls/ ipsec/ k8s/
  tier5/                      obfuscated and hand-rolled source; compiled, minified and native artifacts
  pqc/                        ML-KEM, ML-DSA, LMS, XMSS, hybrids, PQC-washing decoys; code and assets
  mixed/ deadcode/            realistic-size modules with several sites; crypto that never runs
  system/payments-platform/   one multi-service application
  deps/                       dependency manifests for seven applications
  negatives/                  zero-crypto controls
  calibration/                generated siblings of Tier 1-2 cases; not in headline numbers
  custom/                     your own cases (BYOC)
tier5-sources/              source of the Tier 5 artifacts. Never scan this.
expected/                   ground_truth.json (the answer key), libraries.json, custom/, generated reference CBOM
tools/
  score.py  bench.py          the scorer; sandboxed run, verify, checks, perf
  cbomlib.py  truth.py        normalizer and family tables; answer-key loading
  sandbox.py  release.py      the secure lane; the release stamp
  policy.py  policy_report.py deadline engine and report
  byoc.py  compare.py         your own cases; side-by-side scorecards
  holdout*.py                 private holdout sets and the overfit gap
  build_*.py  generate_*.py   regenerate the answer key, assets, artifacts, mixed and calibration cases
  verify_corpus.py            runs every code case, parses every asset
  adapters/                   translations for scanners that don't emit plain CycloneDX 1.6
  test_*.py                   regression suites (bench.py checks runs them all)
policies/                   nist.json, eo14412-hva.json, cnsa2.json
rubric/actionability.json   what a ticket needs
remediation/                the ten reference migrations for fix-and-rescan
integrations/               qci-pqc/, cdxgen/, third-party/, scanner-image.Dockerfile
reports/  evidence/         published scorecards; a verifiable bundle for each
.github/workflows/          testbench (CI), image, release, third-party scanners
```

## Adding a case / Contributing

1. Write the file under `corpus/tierN/...`. Code must run, and assets must parse;
   `verify_corpus.py` checks both. Multi-file cases go in their own directory under `tier3/`
   (Python: `main.py` entry point; Java: sources under `src/`, entry point `com.acme.Main`).
   Don't name the algorithm, key size or mode in comments. A hand-rolled Tier 5 algorithm also
   needs a correctness check against a reference implementation in `verify_corpus.py`.
2. Add a finding to `expected/ground_truth.json`. For text files, give an `anchors` list of
   substrings that appear **exactly once** in the file; lines are resolved from anchors, so editing
   the file later won't silently break the answer key. Binary and PEM assets have no anchors.
3. One finding per (file, family). If a file needs two AES uses with different key sizes, split it.
4. For a Tier 4 certificate or key, add an entry to `materials` so the reference CBOM models it as a
   `certificate` or `related-crypto-material` component.
5. Run `build_expected.py`, then `test_scorer.py`. The reference must still score 100%.

Tier 4 key material is regenerated by `generate_tier4_assets.py`. Key bytes change on every run;
the ground truth doesn't depend on them. SHA-1 certificates are built by re-signing the TBS bytes,
because modern `cryptography` (correctly) refuses to sign with SHA-1.

Before opening a pull request, run `python tools/bench.py checks`: it is what CI runs. A change to
the corpus, the answer key, the scorer or a policy changes the release stamp, which means every
published scorecard has to be rescored and the gates rebaselined in the same change; a change to
anything else doesn't. Rules that can move a score belong in METHODOLOGY.md with a version bump.

## License

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). It covers the tools, the corpus, the answer
key, the policies and the documentation. The keys and certificates in the corpus are test fixtures:
they protect nothing, so don't use them for anything else.
