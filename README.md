# QCI CBOM Benchmark

A graded test corpus and scoring harness for Cryptographic Bill of Materials (CBOM) scanners, maintained by the
Quantum Core Institute. Earlier releases were called the CBOM Testbench, and the tools and documents
still use "testbench" for the harness itself.

QCI also publishes a scanner that this benchmark grades. The benchmark is kept in its own repository
with its own versioned methodology, its results for that scanner are published as measured (it
currently fails four gates), and every published number has an evidence bundle anyone can re-derive.

Point a scanner at `corpus/`, feed its CycloneDX 1.6 output to `tools/score.py`, and you get a
scorecard that says *where* it fails: which tier, which language, which algorithm, whether it
got the key size right, and how much noise it generated on files that contain no crypto at all.

Version 2.2.0 covers **all five tiers, a post-quantum category, realistic mixed files and a multi-service system fixture** in **six languages**: 330 shipped findings, each
dated against NIST, the federal EO 14412 and NSA CNSA 2.0 transition deadlines. It scores whether
each reported finding is **actionable**, not just whether it was found, and it lets you **add your
own code** as scored cases; see [BYOC.md](BYOC.md). It ships wired to the **QCI PQC Readiness
Scanner** (`qci-pqc-scan`): one command installs it, scans the corpus and gates its CI; see
[Scoring the QCI PQC scanner](#scoring-the-qci-pqc-scanner). And because a public corpus gets
learned, it generates **private holdout sets** that show whether a published score still predicts
performance on unseen code; see [HOLDOUT.md](HOLDOUT.md).

- Tiers 1 and 2 are code in Python, Java, Go, JavaScript/TypeScript and C/OpenSSL: 90 single-file
  cases. Tier 3 adds 9 multi-file Python and Java projects.
- Tier 4 is 19 non-code assets: certificates, private keys, keystores, SSH material, a JWKS,
  TLS server configs and a Kubernetes secret.
- Tier 5 is adversarial: 9 obfuscated or hand-rolled source files, plus a `.pyc` and a `.jar`
  shipped without their source.
- The PQC category checks that a scanner recognizes post-quantum cryptography that is already
  deployed: ML-KEM and ML-DSA in Python, Java and Go, ML-DSA certificates and keys, and hybrid key
  exchange in TLS and SSH configs and in Go's `tls.Config`. It also contains "PQC-washing" decoys that claim PQ and aren't.
- Dependency manifests for seven applications (pip, PEP 621, Maven, Gradle, npm with a real
  lockfile, Go modules, Conan) declare 26 crypto libraries, scored for whether a scanner names the
  library, the right manifest and the right version. See [Crypto libraries](#crypto-libraries).
- Mixed files: 15 realistic-size modules (220 to 520 lines) with three to five crypto uses each, often
  one algorithm twice with different parameters, among ordinary code and log messages that name
  algorithms the file doesn't use. 62 site findings. See [Mixed files](#mixed-files).
- 12 negative-control files contain no crypto at all.
- A calibration set of 304 generated Tier 1-2 cases tops each hand-written cell up to four cases, so
  the holdout's overfit gap has something to compare against. They're scored but kept out of every
  headline number. See [Calibration cases](#calibration-cases).

Every code case executes, every Tier 4 asset parses with standard tooling, and every hand-rolled
Tier 5 algorithm is checked against a reference implementation.

## Quick start

```bash
# Python 3.11+ (the tools refuse to start on anything older).
pip install -r requirements.txt              # pinned: cryptography, the CycloneDX validator, packaging
pip install -r requirements-verify.txt       # adds a Java 25 runtime (jdk4py) for the PQC Java cases
# To run every corpus case you also need Go 1.24+, Node 22.18+ (runs .ts directly), JDK 21, and a C
# compiler with OpenSSL 3 headers (libssl-dev). verify_corpus.py counts pass / fail / skip per area;
# --strict turns any skip into a failure (exit 4), which is what a release check uses.
python tools/verify_corpus.py --strict       # runs every code case, parses every Tier 4 asset
python tools/build_expected.py               # resolves ground truth, writes expected/expected.cdx.json
python tools/bench.py checks                 # every required check: strict corpus run, reproducible
                                             # answer key, all test suites, 100% reference replay, docs

# Score your scanner
your-scanner --format cyclonedx-1.6 corpus/ > reports/scanner-x.cdx.json
python tools/score.py reports/scanner-x.cdx.json --name "Scanner X" [--policy nist|eo14412-hva|cnsa2]
# -> reports/scanner-x.md (scorecard) and reports/scanner-x.json

# Add your organization's own patterns as scored cases (walkthrough in BYOC.md)
python tools/byoc.py new my_case --lang python && python tools/byoc.py check
python tools/score.py reports/scanner-x.cdx.json --only-custom      # your cases only
python tools/score.py reports/scanner-x.cdx.json --exclude-custom   # shipped benchmark only, comparable

# Date any CBOM, including your own estate's, against one or more policies
python tools/policy_report.py your-scan.cdx.json --policy nist --policy cnsa2 [--use-map uses.json]
# -> reports/your-scan-deadlines.md / .csv / .json
```

Two calibration points ship with it:

<!-- generated:calibration-points (tools/render_docs.py; edit the scorecards, not this table) -->
| Run | Findings | Recall | At primary site | Params correct | False positives | Precision | PQC over-claims | Ticket-ready | Actionable recall |
|---|---|---|---|---|---|---|---|---|---|
| `expected/expected.cdx.json` (the answer key) | 330 | 100.0% | 100.0% | 100.0% | 0 | 100.0% | 0 | 100.0% | 100.0% |
| `reports/reference-names-only.cdx.json` (answer key, names and locations only) | 330 | 100.0% | 100.0% | 100.0% | 0 | 100.0% | 0 | 72.7% | 72.7% |
| `tools/baseline_grep.py` (naive regex) | 330 | 68.8% | 64.2% | 53.7% | 157 | 59.1% | 28 | 49.3% | 33.9% |

Shipped corpus only (BYOC example cases excluded), so every row has the same denominator.
<!-- /generated:calibration-points -->

Grep by tier, which is the shape you should expect a weak scanner to have:

<!-- generated:grep-by-tier (tools/render_docs.py; edit the scorecards, not this table) -->
| Tier | Findings | Recall | At primary site | Params correct |
|---|---|---|---|---|
| 1. Direct, Python and Java | 32 | 100% | 100% | 56.2–75% |
| 1. Direct, Go / JavaScript / C | 57 | 65–82.4% | 65–82.4% | 42.9–85.7% |
| 2. Indirection, Python and Java | 17 | 100% | 87.5–88.9% | 50–55.6% |
| 2. Indirection, Go / TypeScript / C | 19 | 83.3–100% | 83.3–100% | 33.3–60% |
| 3. Cross-file | 16 | 100% | 42.9–55.6% | 33.3–42.9% |
| 4. Non-code assets | 48 | 31.2% | 31.2% | 66.7% |
| 5. Adversarial | 17 | 0% | 0% | n/a |
| PQC, code | 14 | 50–100% | 50–100% | 25–50% |
| PQC, assets | 22 | 40.9% | 40.9% | 100% |
| Mixed files | 62 | 69.2–100% | 69.2–100% | 18.2–50% |
| System fixture | 26 | 18.2–100% | 0–66.7% | 33.3–100% |

Ranges run across the languages in each row.
<!-- /generated:grep-by-tier -->

The reference run proves the scorer agrees with the ground truth. The grep run is the floor.
A commercial scanner that can't beat it on parameters and precision is a grep with a logo.

## Reproducible runs and evidence bundles

For a score someone else has to trust, use the runner instead of `score.py`. One command scans in
the sandbox, scores, and writes an evidence bundle:

```bash
python tools/bench.py run --name "Scanner X" --scanner-cmd "scanx {corpus} -o {out}/cbom.json" \
    --bundle bundles/scanner-x [--adapter qci-pqc|cdxgen] [--scope scope.json] [--gates gates.json]
python tools/bench.py verify bundles/scanner-x      # anyone can re-derive every number
python tools/bench.py checks --out checks.json      # the testbench's own required checks
```

**The sandbox** (`tools/sandbox.py`) gives the scanner a private copy of the corpus, read-only where
the host can make a mount namespace, and hashes it before and after: a scanner that changes its
input isn't scored. The environment is scrubbed (no credentials, never the holdout seed), the
network is cut (a network namespace, or the container run with `--network none`), and wall-clock,
CPU, memory and file-size limits apply. Exit status, wall time, CPU time and peak memory are
recorded. BYOC run commands, holdout scans and the scanner's `--version` call go through the same
sandbox.

It also puts a filesystem boundary around the run. Home directories, temp directories, `/mnt`,
`/run`, the whole testbench tree (answer key, evidence, reports) and any holdout set are replaced
by empty mounts; what stays visible under them is the work directory, the toolchain directories on
PATH, and anything you name with `--allow-path` (recorded in the bundle). System directories stay
readable, because the scanner needs them to run. This needs a mount namespace: on a host or
container that can't make one the run is recorded as "not confined", and `--require-isolation`
refuses to run unless both the network cut and the boundary are in place.

**The container lane.** The boundary above is a deny-list with exceptions, and system directories
stay readable. For a scanner you don't trust at all, give it its own container:
`bench.py run --scanner-image my-scanner:1.0 --scanner-cmd "..."`. The scanner then runs in an image
that holds only the scanner (`integrations/scanner-image.Dockerfile` builds one from wheels), with
no network, a read-only root, no capabilities, the corpus mounted read-only and one writable output
directory. No testbench file, answer key, holdout set or host file exists inside it. Time and memory
limits apply and are recorded; the image id goes in the bundle. QCI v2.3.4 scores identically in
both lanes (`evidence/qci-v2.3.4-container/`).

What the sandbox can't cover is the scanner's build. `pip install` runs the scanner's own code and
needs the network. `run_qci_pqc.py` strips the seed and anything credential-shaped from that
step's environment, which is enough for your own scanner. For someone else's, build in a job with
no secrets and score in another: `integrations/qci-pqc/github-workflow.yml` does exactly that,
handing wheels and their hashes from one job to the next.

**The bundle** holds the scanner's raw output, the adapted CBOM, the scorecards, a manifest
(testbench release, methodology version, the release stamp, the sha256 of every file that decides a
score, the scanner's command, version and executable hash, the image digest, toolchain versions,
the sandbox record, the required-check status) and `SHA256SUMS`. With a holdout seed it adds the
overfit and negative-control gaps and a commitment to the seed, never the seed itself.
`bench.py verify` checks the sums, checks that the tree it runs on is the release the bundle was
scored on (and lists any file that differs), and re-derives every section of every scorecard from
the raw CBOM: results, false positives, libraries, linkage, deadlines, actionability. It re-derives
the fix-and-rescan result from the second raw CBOM and the gate verdict from the bundled gates
file. A doctored number fails even with recomputed checksums, and so does a bundle missing an
artifact its claims rest on: a scored bundle without its raw CBOM doesn't verify. The one thing a
bundle can't prove alone is the holdout result, because the seed is private; verify says so, and
`verify --holdout-seed N --holdout-cbom FILE` re-derives it once the seed is revealed
(`run --keep-holdout-cbom` keeps the file on the evaluator's side).

Inside the testbench's own image the namespace boundary needs `--cap-add SYS_ADMIN` (tested: without
it the run is "not confined" and `--require-isolation` refuses; with it the answer key is hidden).

**The image** (`Dockerfile`) pins Python 3.13 (the corpus ships 3.13 bytecode), Go 1.24, Node 22.18, JDK 21, a Java 25 runtime and
OpenSSL 3 headers, verifies the whole corpus at build time, and records the toolchain versions. To
score a scanner in it, build `FROM` the testbench image, install the scanner, and run
`bench.py run` with `--network none`. On a version tag, `.github/workflows/release.yml` builds the
image, runs the required checks inside it with no network, produces the answer-key and grep
bundles, and attaches them to the GitHub release; pushing and cosign signing are switches for the
repository owner. `evidence/` in this release holds a bundle for every published scorecard.

**The rules** are in [METHODOLOGY.md](METHODOLOGY.md), versioned separately from the testbench.
Every scorecard records the methodology version it was produced under, and scorecards from
different versions are never compared.

## What the tiers test

| Tier | What it tests | Findings |
|---|---|---|
| **1. Direct** | Algorithm and parameters are literals at the call site. `hashlib.md5()`, `Cipher.getInstance("AES/ECB/PKCS5Padding")`, `kpg.initialize(3072)`, Go's `md5.Sum` and `rsa.GenerateKey(rand.Reader, 2048)`, Node's `createCipheriv("des-ede3-cbc", ...)` and Web Crypto, OpenSSL's `EVP_aes_128_ecb()`, the pre-3.0 `RSA_generate_key_ex`, and TLS versions and suites set in code (`tls.Config`, `SSL_CTX_set_cipher_list`). | 89 (16 Python, 16 Java, 20 Go, 17 JavaScript, 20 C) |
| **2. Indirection** | Same file, but the algorithm or its parameters arrive via a constant, alias import, config file, env var or system property default, wrapper function, dispatch table, enum, `functools.partial`, or string concatenation. Go adds a `crypto.Hash` value in a variable and constructors passed as function values; TypeScript adds `as const` config objects and template literals; C adds macros, OpenSSL 3 `EVP_CIPHER_fetch` by name, function pointers and constructor tables. | 36 (9 Python, 8 Java, 6 Go, 7 TypeScript, 6 C) |
| **3. Cross-file flow** | Multi-file projects. Algorithm names and key sizes defined in one module and used in another; a shared wrapper called with two different key sizes; decorator registries and strategy factories; constructor dependency injection; JWT `alg` read from `.ini` / `.properties` and resolved through a lookup table. | 16 (9 Python in 5 projects, 7 Java in 4 projects) |
| **4. Non-code assets** | X.509 certificates (PEM, DER, a two-cert chain, one SHA-1-signed); private keys (PKCS#8, SEC1 on secp256k1, password-encrypted PKCS#8); a JWKS; a PKCS#12 keystore and a JKS truststore; an sshd_config, an SSH host public key and an OpenSSH private key; nginx, Spring Boot and OpenSSL TLS configs; a Kubernetes TLS secret with the certificate base64-encoded inside YAML. | 48 |
| **5. Adversarial** | Names assembled at runtime (fragments, base64, `chr()` codes, reversed strings, char arrays); `importlib` and Java reflection; hand-rolled RC4, SHA-256, TEA and textbook RSA with no crypto library call at all; a `.pyc` and a `.jar` with no source. | 17 (9 Python, 8 Java) |
| **PQC** | ML-KEM-768/1024 and ML-DSA-44/65/87 via `cryptography`, the JDK 24+ JCA and Go's `crypto/mlkem`; Go `tls.Config` preferring `X25519MLKEM768` with an X25519 fallback; including a parameter set passed through a constant or `NamedParameterSpec`; an application-level X25519 + ML-KEM hybrid; ML-DSA certificates, one PQ key signed by a classical RSA CA; ML-KEM and ML-DSA key files; hybrid groups (`X25519MLKEM768`, `SecP384r1MLKEM1024`) in nginx and OpenSSL configs; `mlkem768x25519-sha256` and `sntrup761x25519` in sshd_config; and two PQC-washing decoys plus a washing config. | 36 (6 Python, 4 Java, 4 Go, 22 assets) |
| **Mixed** | Realistic-size modules, 220 to 520 lines, with three to five crypto uses spread through ordinary code: CSV parsing, pagination, retries, money formatting, logging. Most files use one family twice with different parameters (AES-128-CBC and AES-256-CTR, HMAC-MD5 and HMAC-SHA512, P-256 and P-521); the surrounding code has numbers a guesser will grab (page sizes of 256, buffers of 32 bytes, `bit_length()`); log lines and note dictionaries name algorithms the file doesn't use, including PQC claims. Scored per site, not per file. | 62 sites in 15 files (3 Python, 3 Java, 3 Go, 2 JavaScript, 1 TypeScript, 3 C) |
| **Negatives** | Algorithm names in docstrings, comments, UI labels, log messages, identifiers and a Markdown runbook; known-answer test vectors; CRC32, Adler32, Base64, `hash()`; a file with valid PEM armor around base64 that isn't a certificate; and code that reuses crypto's constants and math for other jobs (Fibonacci hashing with TEA's constant, `pow()` for an IBAN check, `modPow` in a primality test); in Go, JavaScript and C, algorithm names in string tables, display labels and changelog comments next to FNV, CRC32 and djb2. Zero real crypto. | 12 files |

Positive files also carry **decoys**: comments mentioning ML-DSA and X25519MLKEM768 in files that
use neither, and commented-out `SSLv3` and RC4 lines in `nginx.conf`. A scanner reporting
post-quantum algorithms where none exist is flattering the codebase, which is worse than missing
something.

**Test files never describe their own crypto.** Comments say what pattern a case tests ("key size
held in a constant"), never which algorithm or size it uses. Earlier versions did, and grep was
reading key sizes out of comments: cleaning them up dropped its Tier 1 Java parameter score from
87.5% to 56.2%. Case descriptions live in this README and in the ground truth's `note` fields.

### An honest note on recall

Grep scores 100% recall through Tier 3 in Python and Java. That isn't a corpus bug. Somewhere in every project the
algorithm name is a string, usually in a config or constants file, and text search finds strings.
That's why the scorecard has two recall numbers:

- **Recall** gives credit for reporting the finding anywhere acceptable, including the config file
  that names it.
- **At primary site** gives credit only when the finding lands in the file the ground truth
  anchors it to: the crypto call itself or, for a shared wrapper, the caller that binds the
  parameters.

An inventory that says "SHA-1, somewhere in `settings.py`" is technically correct and useless to the
engineer who has to fix it. Through Tier 3, primary-site recall and parameter accuracy are what
separate real analysis from text search. In Tier 4, recall itself collapses, because certificates
and keys are base64-encoded and contain no algorithm names at all. In Tier 5 it hits zero: the
names are broken up, encoded, compiled away, or never existed because nobody called a library.

Three Tier 3 cases are built specifically to punish name-only matching:

- `wrapper_two_callers`: one RSA wrapper, called with 1024 and 3072. Reporting "RSA" once at the
  wrapper without sizes hides the weak key.
- `cross_class_constant/SessionCrypto.java`: no algorithm string in the file at all. The
  transformation and key length both come from `CryptoConfig`.
- `jwt_alg_mapping`: `Mac.getInstance(macName)`. The algorithm is only resolvable by following
  config → lookup table → call.

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

## Your own code

The shipped corpus measures crypto in general. [BYOC.md](BYOC.md) walks an organization through
adding its own patterns (in-house wrappers, vendor SDK usage, framework configs) as scored cases:

- `tools/byoc.py new` scaffolds a runnable case in `corpus/custom/<case>/` and its answer key in
  `expected/custom/<case>.json`, kept apart from the shipped ground truth so upgrades never collide.
- `byoc.py add` records findings using ordinary names (`RSA-2048`, `AES-128-CBC`, `ML-KEM-768`) and
  rejects ambiguous anchors and duplicates. `byoc.py draft` proposes candidates from a naive scan,
  marked unconfirmed; nothing is scored until a person confirms it.
- `byoc.py check` runs each case and lints for what people get wrong when pasting real code:
  credentials (error), real hostnames, emails and public IPs (warnings), and comments that name the
  algorithm, which leak the answer.
- `score.py --only-custom` gives a number about your estate; `--exclude-custom` keeps the shipped
  benchmark comparable with anyone else's. By default each case is its own scorecard row.

A worked example ships in `corpus/custom/example_envelope/`: an in-house envelope library where
application code picks `profile="LEGACY_COMPAT"` and never names an algorithm. Grep finds its
algorithms (they're named in the profile table) but misses both AES key sizes.

## Scoring the QCI PQC scanner

The testbench is set up to score [qci-pqc-scanner](https://github.com/Quantum-Core-Institute-Inc/qci-pqc-scanner)
directly. From a checkout of the scanner:

```bash
python tools/run_qci_pqc.py --scanner ../qci-pqc-scanner     # installs into .qci-venv/, scans, scores
python tools/run_qci_pqc.py --qci-bin qci-pqc                 # or use an installed binary
```

It runs `qci-pqc scan corpus --reproducible`, checks the scanner's CBOM against the CycloneDX 1.6
schema, translates it, scores it twice (inside the scanner's declared scope and over everything), and
writes `reports/qci-pqc/SUMMARY.md`. Exit codes: 0 every gate passed, 1 a gate in
`integrations/qci-pqc/gates.json` failed, 3 the gates were **not evaluated** (the baseline was set
on a different release, answer key, corpus, scorer, policy or adapter, or there is none).
`--report-only` (alias `--no-gate`) always exits 0 and says REPORT ONLY at the top of the summary,
so a green report-only job can't be mistaken for a gated one.

Every gate is a required measurement. If a run didn't produce one (no holdout seed, no schema
validator, a metric the scanner's output can't support) the gate is listed as missing and the run
is not evaluated: exit 3, or 1 if another gate failed. A gate is skipped only with a reason on
record: `--without-holdout` for a run made without a holdout on purpose, or `when_missing: skip` in
the gates file for a measurement a scanner may legitimately not produce. `tools/rebaseline.py`
resets the floors from scored runs; rebaseline first and run the scanners after, because the docs
check refuses a report directory and an evidence bundle that give different verdicts.

Three things are specific to this scanner, all in `integrations/qci-pqc/` and `tools/adapters/qci_pqc.py`:

- **Declared scope.** `scope.json` encodes the scanner's own `docs/LIMITATIONS.md`: JARs, `.pyc`,
  DER/PKCS#12/JKS and certificate signature algorithms are listed in the scorecard but not counted.
  `score.py --scope <file>` works for any scanner that publishes its limits.
- **Categories vs algorithms.** QCI reports many findings as risk categories (`DH/ECDH`,
  `SSH-Weak-Cipher`, `Hybrid-KEM`). Exact algorithm names are scored strictly. Categories can't be
  credited as an algorithm without guessing, so they're scored separately as *signal coverage*: a
  category on the line of an expected finding it plausibly describes. Both numbers are reported.
- **Ratchet gates.** `gates.json` holds a release's measured results as floors. Raise a gate when a
  release improves it.

`github-workflow.yml` is a ready-to-copy CI job for the scanner repo. `FINDINGS.md` is the
write-up for the scanner team: what 0.3.0 misses, why, and where in its source to fix it.

qci-pqc-scan v2.3.4 on testbench 2.1 (identical to v2.3.0 on every measure), in declared scope: recall 74.7% (v2.2: 74.3%), precision 99.6%
with one false positive (DH matched in the bytes of the system fixture's Go binary), no PQC
over-claims, and no extra false positives on fresh negative controls. Crypto libraries in the right
manifest: 96.4%, with versions. The overfit gap is -0.9 to +3.8 over five seeds, never significant.
It fails three ratchet gates and the schema limit: its CBOM is invalid (`"version": null` on five
libraries), parameters are often missing where v2.2 guessed them (56.8%), and a leftover string
filter drops `createHash("sha1")`, which costs ticket-ready and deadline-weighted recall. On the 2.1
measurements it routes 5 of 17 system findings to the wrong team, links no assets, verifies 4 of 8
eligible migrations (every miss is a missing parameter on the new algorithm), and scans 3,000 files
in two minutes at 49 MB. `FINDINGS.md` has the 2.1 notes and the v2.3.4, v2.3.0, v2.2, v0.7 and 0.3.0 reviews.

Gates carry the full release stamp they were measured on (`tools/release.py`: testbench version,
finding count, and hashes of the answer key, corpus, scorer, policy and adapter). They're enforced
only against that exact stamp. When any part changes, the run exits 3 and lists what moved; review
it and reset with `--rebaseline`. Pin a testbench release in CI (`TESTBENCH_REF`) so that happens
when you choose, and treat exit 3 as a failure there. Other scanners follow the
same pattern: write an adapter in `tools/adapters/` only if the output needs translating, and a
`scope.json` if the scanner documents what it skips.

## Crypto libraries

The first question a CISO asks is often not "where is SHA-1 called" but "which applications ship
which crypto library, at which version, and which of those can't do ML-KEM". `corpus/deps/` holds
manifests for seven applications, and `expected/libraries.json` lists the 26 crypto libraries they
declare:

| Manifest | What it tests |
|---|---|
| `python-billing/requirements.txt` | Six pinned crypto libraries (cryptography 41.0.7, PyCryptodome, pyOpenSSL, PyJWT[crypto], Paramiko, bcrypt), a commented-out `pycrypto` line, and `hashids`, which sounds like crypto and isn't |
| `python-signer/pyproject.toml` | PEP 621 dependencies: a version *range* (`cryptography>=48,<51`) and liboqs-python |
| `java-gateway/pom.xml` | Bouncy Castle 1.70 through a `${bc.version}` property, on the superseded `-jdk15on` artifacts; Nimbus JOSE+JWT; JJWT; Jasypt inside an XML comment |
| `java-pq/build.gradle` | Bouncy Castle 1.80 (`-jdk18on`), which has the final ML-KEM and ML-DSA |
| `node-api/package.json` + `package-lock.json` | jsonwebtoken, crypto-js (discontinued upstream), node-forge, bcryptjs, @noble/post-quantum; and four *transitive* crypto libraries that only the lockfile shows. The lockfile was generated by npm, not typed |
| `go-service/go.mod` | golang.org/x/crypto, Cloudflare CIRCL, golang-jwt |
| `c-agent/conanfile.txt` + `CMakeLists.txt` | OpenSSL 1.1.1w (end of life since 2023-09-11) and libsodium |

Each entry says whether that version ships ML-KEM/ML-DSA (`pq_capable`) and, where a primary source
says so, its support status. Those facts are cited in the file's `sources` block: the
pyca/cryptography changelog (ML-KEM and ML-DSA in the wheels from 48.0.0), Bouncy Castle's release
notes (1.78 had the FIPS 203 draft, 1.79 the final standards), CIRCL's releases (ML-KEM from 1.4.0,
ML-DSA from 1.5.0), crypto-js's README, and OpenSSL's own end-of-life and 3.5 announcements. Every
pinned version was checked against PyPI, npm, Maven Central or the project's Git tags.

`score.py` adds a section to every scorecard: libraries found in the right manifest, found anywhere
(an inventory that can't say which application isn't much use, so it's reported separately),
transitive coverage, version accuracy (a found library with no version counts as not correct), and,
when a scanner states whether a library is post-quantum capable, whether that verdict is right. False
positives are a commented-out dependency reported, a look-alike reported *as cryptography*, or a
crypto library attributed to a manifest that doesn't declare it. `verify_corpus.py` checks every
manifest parses with its ecosystem's rules and lists what the answer key says it lists.

## Comparing scanners

`tools/compare.py` puts any number of scorecards side by side, recomputed from per-finding results
on the shipped corpus so every scanner has the same denominator (no declared scopes, no BYOC cases):

```bash
python tools/run_qci_pqc.py --scanner ../qci-pqc-scanner     # -> reports/qci-pqc/scorecard-full.json
python tools/run_cdxgen.py --install                          # -> reports/cdxgen/scorecard.json
python tools/compare.py --scanner "QCI 0.3.0=reports/qci-pqc/scorecard-full.json" \
    --scanner "cdxgen 12.9.1=reports/cdxgen/scorecard.json" \
    --baseline "grep baseline=reports/baseline_grep.json" --out reports/comparison
```

Current result (`reports/comparison.md`):

<!-- generated:comparison (tools/render_docs.py; edit the scorecards, not this table) -->
| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Recall | 70.3% | 69.7% | 57.3% | 4.2% | 68.8% |
| incl. findings reported without an algorithm name | 73.6% | 73.0% | 60.0% | 11.5% | n/a |
| Parameters correct (of detected) | 56.9% | 64.8% | 67.2% | 78.6% | 53.7% |
| Precision | 99.6% | 92.0% | 87.1% | 100.0% | 59.1% |
| False positives | 1 | 20 | 28 | 0 | 157 |
| PQC over-claims | 0 | 7 | 13 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% | 100.0% | n/a | 100.0% |
| System fixture: recall | 65.4% (17/26) | 65.4% (17/26) | 53.8% (14/26) | 0.0% (0/26) | 50.0% (13/26) |
| System fixture: routable to the owning team | 70.6% | 70.6% | 64.3% | n/a | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 47.0% | 54.3% | 54.5% | 78.6% | 49.3% |
| Mixed files: recall | 80.6% (50/62) | 79.0% (49/62) | 62.9% (39/62) | 6.5% (4/62) | 88.7% (55/62) |
| Crypto libraries, right manifest | 96.4% (27/28) | 28.6% (8/28) | 25.0% (7/28) | 75.0% (21/28) | 0.0% (0/28) |
| Library versions correct (of found) | 84.6% | 0.0% | 0.0% | 100.0% | n/a |

Shipped corpus, 330 findings for every column, no declared scopes. Full tables, by language and tier, in `reports/comparison.md`.
<!-- /generated:comparison -->

Fixing things, and finishing big trees:

<!-- generated:operations (tools/render_docs.py; edit the scorecards, not this table) -->
| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Verified remediation (of eligible migrations) | 4/8 (50.0%) | 4/7 (57.1%) | 4/5 (80.0%) | none eligible | 0/7 (0.0%) |
| Migrations eligible (of 10) | 8 | 7 | 5 | 0 | 7 |
| Large repo: finished inside the budget | yes | yes | yes | yes | yes |
| Large repo: wall time | 118 s | 123 s | 83 s | 105 s | 4 s |
| Large repo: peak memory | 50 MB | 49 MB | 49 MB | 1692 MB | 34 MB |
| Large repo: planted uses found | 54/60 | 60/60 | 49/60 | 8/60 | 55/60 |
| Large repo: found, first vs last quarter of the tree | 91.7% / 100.0% | 100.0% / 100.0% | 83.3% / 83.3% | 8.3% / 0.0% | 100.0% / 88.9% |

Fix and rescan: the 10 reference migrations in `remediation/`, scored as in METHODOLOGY.md 4b. Large repo: `bench.py perf --size medium` (3,000 code files, 17 MB, 60 planted Tier 1 uses, seed 2026), 600 s budget, same host for every scanner.
<!-- /generated:operations -->

Recall is over the whole corpus here, so QCI's numbers are a little below its declared-scope ones.
The overlap section of `reports/comparison.md` shows who finds what: cdxgen's unique findings are all
JavaScript/TypeScript, it remains far ahead on version accuracy, and most of what no product finds
sits in certificates, keys and configs, C and Go.

The QCI false positives in older releases are almost all in the mixed files: algorithm names in log
messages and notes dictionaries. v2.3 drops them, which is where its precision gain comes from. Its
parameter accuracy fell because it stopped guessing file-wide and now often reports none, which is
the honest failure but still a failure. See [Mixed files](#mixed-files) and `integrations/qci-pqc/FINDINGS.md`.
Notes on cdxgen are in `integrations/cdxgen/NOTES.md`.

Read the grep column carefully. It matches the products on recall because most of this corpus names
its algorithms somewhere, and it pays for that in false positives and PQC over-claims (see the table). It was
also written alongside the corpus, so it isn't an independent product: it shows how much is findable
by name alone, which is the bar a real scanner should clear on precision *and* recall.

A scanner whose output is standard CycloneDX 1.6 with `evidence.occurrences` needs no adapter: score
its CBOM with `score.py --exclude-custom` and pass the JSON to `compare.py`. Adapters
(`tools/adapters/`) exist only where a scanner's output needs translating, and each one documents
every translation it makes. IBM/PQCA's CBOMkit-theia isn't included: building it here requires
fetching and compiling its source, which this environment didn't permit. Run it wherever you can and
add its CBOM the same way.

## The system fixture

`corpus/system/payments-platform/` is one application instead of one file: a Go API, a Python
worker and a Java service that all get their crypto from a shared wrapper (`libs/cryptokit`, in
three languages) driven by one config file. Around them: lockfiles, a built JAR and a stripped Go
binary, nginx TLS termination with its certificate and key, a Kubernetes TLS secret, KMS keys in
Terraform (one with no key spec, which AWS defaults to AES-256-GCM), a partner CA certificate
pasted into Python source, and a CODEOWNERS file. 26 findings, scored like any other.

Two numbers only a system can produce:

- **Routable.** Each finding's owner comes from CODEOWNERS. When the wrapper and config decide the
  algorithm, the answer key's file is the service's call site and the wrapper and config are alt
  files: a scanner that reports only the wrapper still gets the detection, but the ticket goes to
  platform-security instead of the team that has to change its code. The config line for webhook
  signatures is shared by two services, so one report there routes neither.
- **Asset links.** Does the CBOM connect the nginx config to the certificate it serves, and the
  certificate to its private key? Found when a component in one file references a component in the
  other (a CycloneDX `*Ref`, a suite's `algorithms`, or a `dependencies` entry).

`tools/build_system.py` regenerates the keys and certificates and rebuilds the binary and JAR from
the fixture's own source; `verify_corpus.py` runs every service, both artifacts, and parses every
key. Grep's result is the point: it finds the wrapper-decided findings through the config and routes
every one of them to the wrong team.

## Fix and rescan

`remediation/` holds ten reference migrations: RSA signing to ML-DSA-65 in Python and Java,
AES-ECB, AES-CBC and 3DES to AES-256-GCM in five languages, an nginx config moved to TLS 1.3 with
`X25519MLKEM768`, and an sshd config moved to Ed25519 host keys, ML-KEM hybrid key exchange,
AES-GCM and HMAC-SHA-512. Each after-file runs (`tools/test_remediation.py`).
`bench.py run --remediation` applies them all, rescans, and scores each migration: the old
algorithm (or, for AES-ECB to AES-GCM, the old parameters) must be gone from that file, the new
algorithm reported with the right parameters, and nothing else in the file may change. A migration
counts only if the scanner found what it retires in the first place; otherwise it's "not eligible",
not a failure. Anything that changes outside the migrated files is reported as a regression. The
migrated files keep a "Migrated: X replaced with Y" comment, the way real migrations do, so a scanner
that reads comments still sees the old name; that's most of why grep verifies none.

## Big trees

`bench.py perf` generates a tree from a public seed (600, 3,000 or 12,000 code files in five
languages plus large CSV exports) with Tier 1 uses planted evenly through it, runs the scanner in
the sandbox under a time budget, and reports whether it finished, wall and CPU time, peak memory,
throughput, and how many planted uses it found by quarter of the tree. A scanner that gives up
partway shows it as a drop in the last quarter. The bundle re-verifies: the fixture regenerates
from its seed and the result re-derives from the raw CBOM.

Every scorecard bucket now carries a 95% interval on recall, and buckets with fewer than ten
findings are marked thin. Every result also records the rule that decided it, so a disputed point
traces to METHODOLOGY.md.

## Holdout sets and the overfit gap

A public corpus gets learned. `tools/holdout.py` generates fresh, executable variants of the Tier 1-3,
PQC and mixed-file patterns in every corpus language, plus negative controls and dependency manifests, from a
private seed (new code, same APIs and kinds of indirection), scores a scanner on them, and reports
the **overfit gap**: published recall minus holdout recall, cell by cell, with a
95% interval. A broad set adds API spellings the corpus doesn't use and reports coverage on its own.

Two more gaps ride along: false positives per negative file (gated at +0.5) and crypto libraries
found in the right manifest (reported only; six manifests a seed is too few to gate on).

Since 2.1 the holdout also generates certificates, keys, keystores, TLS and SSH configs and compiled
`.pyc` and `.jar` files, so Tier 4, Tier 5 and PQC-asset cells are in the gap too.

Calibrated before trusting it: the reference CBOM reads 0 and a memorizer +100. On 2.1, over five
seeds, grep reads -2.3 to +1.0 and QCI v0.7, v2.2 and v2.3 between -2.1 and +3.8, never
significant. On the negatives,
grep and 0.3.0 stay between -0.3 and +0.25 per file and v0.7 reads +0.7 to +1.2. Details, and the limits, in [HOLDOUT.md](HOLDOUT.md).

## Mixed files

Every other code case is a small file built around one or two uses, which is the easy shape for a
scanner. A real module is a few hundred lines with crypto in three or four helpers, the same algorithm
twice with different settings, ordinary code in between, and log messages that mention algorithms
the module doesn't use. `corpus/mixed/` is 15 files of that, 62 sites, in all six languages.

What they catch that the small files can't:

- **File-wide parameter guessing.** A scanner that reads "the first `SHA256` in the file" or "the
  first number after `initialize(`" gets one-algorithm files right and mixed ones wrong. Each site is
  scored on its own parameters.
- **One report per file and family.** Two AES sites need two reports at two lines.
- **Name matching without context.** Every algorithm name in a log line or notes dictionary belongs
  to a family the file doesn't use, so each hit is a plain false positive.
- **Line-window de-duplication.** Sites of the same family are sometimes a few lines apart.

| | Recall | Params correct (of detected) | Sites sharing a family with another site, params correct | False positives |
|---|---|---|---|---|
| QCI v2.2 | 79.0% (49/62) | 40.8% (20/49) | 8 of 22 detected | 19 (7 PQC over-claims) |
| QCI v0.7 | 62.9% (39/62) | 38.5% (15/39) | 7 of 18 detected | 23 (11 PQC over-claims) |
| QCI 0.3.0 | 21.0% (13/62) | 30.8% (4/13) | 0 of 5 | 14 |
| cdxgen 12.9.1 | 6.5% (4/62) | 3 of 4 | none detected | 0 |
| grep baseline | 88.7% (55/62) | 34.5% (19/55) | 5 of 24 | 82 |

QCI v0.7's parameter accuracy drops from 76% on the rest of the corpus to 38% here. The cause is in
its source: `scanner.py` searches the whole file for `sha256` and, if it finds it, labels every HMAC
and PBKDF2 in that file SHA-256; key sizes and AES modes come from the first match anywhere in the
file. On single-purpose test files that's usually right. The FINDINGS file has the details.

The files are generated (`tools/build_mixed.py`, a fixed public seed, checked by `--check`) from the
same code as the holdout's mixed tier, so the holdout can test whether a mixed-file score carries over.
Generated doesn't mean toy: every file runs, and the ordinary code is ordinary code.

## Calibration cases

The overfit gap (next section) compares published and holdout recall cell by cell, a cell being
(tier, language, family). In the hand-written corpus 155 of 191 such cells hold a single case, so the
published side of each comparison is 0% or 100% and most of the gap's uncertainty came from there.
`corpus/calibration/` adds generated siblings, written by the holdout's matched generator from a
fixed public seed (`tools/build_calibration.py`, `--check` to verify), until every Tier 1-2 cell has
four cases. That's 304 cases; one cell (Java Tier 1 DES) has no generator spelling and stays at one.

They are deliberately kept out of the benchmark. Recall, precision, the deadline view, the gates and
`compare.py` see only the hand-written corpus; false positives in `corpus/calibration/` aren't counted.
Every scorecard reports them on one line, and `score.py` returns them as `calibration_results`, which
the overfit gap adds to the published side.

They also give a one-time check that needed no holdout at all, because no scanner had seen them:

| | Hand-written Tier 1-2 | Calibration, same cell mix |
|---|---|---|
| QCI v2.2 | 78.0% | 81.6% |
| QCI v0.7 | 59.2% | 64.1% |
| QCI 0.3.0 | 26.3% | 28.6% |
| cdxgen 12.9.1 | 8.6% | 9.5% |
| grep baseline | 90.1% | 91.1% |

Every scanner does a little better on the generated cases, which are plainer than the hand-written
ones. Neither QCI release is doing better on the cases it was tuned against.

## Is the CBOM actionable?

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

Certificate facts are **checked against the real files**. `tools/assetfacts.py` reads subject,
issuer and validity out of every certificate at build time, including the one inside the PKCS#12,
the one in the JKS (via `keytool`) and the one base64-encoded in the Kubernetes secret. A scanner that
reports the wrong expiry date fails, which is right: a wrong date is worse than none.

The scorecard reports:

- **Ticket-ready**: share of detected findings with every must-have present and correct.
- **Actionable recall**: share of *all* expected findings that were both found and ticket-ready.
  This is the closest single number to "how much of the migration backlog would this tool hand me".
- **Field completeness**: share of all applicable checks passed, plus a per-check table showing
  exactly which fields a scanner leaves empty.

The calibration rows make the point. `reference-names-only` is the answer key with OIDs, functions,
quantum levels, code context, library links and certificate metadata stripped. It finds
everything, and a quarter of what it finds can't become a ticket: no certificate has an expiry date,
and no RSA or EC key says whether it's for key exchange or signing. Grep's actionable
recall is about half its recall (see the calibration table under Quick start).

**The rubric is proposed, not official.** No official minimum elements for a CBOM exist yet;
EO 14412 directs CISA to publish them, due around March 2027. The rubric is a data file: move a check
between `must` and `should`, disable it, or align it to CISA's list when that appears.

## Deadlines and policies

Detection rates treat a missed MD5 checksum the same as a missed key exchange that has to be gone
by 2030. Organizations don't, so every expected finding is also dated under a transition policy,
and the scorecard adds a deadline view:

- **Recall by when it's due**: due now, by end of 2030, 2031–2033, 2034–2035, no deadline.
- **Deadline-weighted recall**: misses weigh 5 if due now, 4 by 2030, 3 for 2031–2033, 2 for
  2034–2035, 1 with no deadline.
- **Findings due by end of 2030 that the scanner missed**, listed by name. This is the number a
  CISO can take to a board.

Three policies ship, as data in `policies/*.json`:

| Policy | Covers | Key dates |
|---|---|---|
| `nist` (default) | NIST IR 8547 **final** (Oct 27, 2026), SP 800-131A Rev. 2, FIPS 186-5, SP 800-52 Rev. 2, NIST's 2022 SHA-1 notice | All quantum-vulnerable public-key crypto deprecated after 2030, disallowed after 2035, at any key size. SHA-1 ends Dec 31, 2030. RSA/DH below 2048, DSA signing, 3DES, MD5, TLS < 1.2 are already out. |
| `eo14412-hva` | Executive Order 14412 (June 22, 2026) for federal high value assets and high impact systems; inherits `nist` | PQC key establishment by Dec 31, 2030; PQC signatures by Dec 31, 2031. |
| `cnsa2` | NSA CNSA 2.0 | Only AES-256, ML-KEM-1024, ML-DSA-87, SHA-384/512 (and LMS/XMSS). CNSA 1.0 strengths (RSA-3072+, P-384) until the system type's exclusive-use date: 2030 for firmware signing and networking, 2033 for web/cloud, OS, niche and custom. |

Things worth knowing:

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

`policy_report.py` works on any CycloneDX 1.6 CBOM, not just this corpus. Run it on a real scan and
you get the same three views of your own estate, plus a CSV to load into a tracker.
`reports/corpus-deadlines.md` is a sample, run on the complete corpus inventory.

When a standard changes, edit the rule in its JSON file and rerun `test_policy.py`; every rule
names its source document, and every source carries its retrieval date.

## Coverage

Algorithms with at least one case in each code language: MD5, SHA-1, SHA-256, SHA3-256, RSA, DSA,
ECDSA (P-256, P-384), Ed25519, X25519, DH, AES, 3DES, HMAC, PBKDF2. Python adds ChaCha20-Poly1305 and
AES-128-CBC / AES-192-CBC; Java adds single DES. Tier 4 adds secp256k1, SHA-384 and SHA-512
certificate signatures, TLS 1.0–1.2, five cipher suites, and SSH key exchange, cipher and MAC names.
Tier 5 adds RC4, TEA and HMAC-MD5. The PQC category adds ML-KEM-768/1024, ML-DSA-44/65/87, four
hybrid key-exchange groups and TLS 1.3.

Quantum-relevant split: 122 of 330 findings are Shor-vulnerable (RSA, DSA, EC, DH, Ed25519, X25519,
and TLS suites with RSA or ECDHE key exchange); 71 are classically broken (MD5, SHA-1, DES, 3DES,
RC4, and HMAC over SHA-1 or MD5); 21 are post-quantum, 6 of them hybrids.

## How scoring works

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

## Layout

```
corpus/
  tier1/{python,java}/      direct, literal usage
  tier2/{python,java}/      same-file indirection (+ config/ files)
  tier1/{go,javascript,c}/  Go: one program per directory under a go.mod; Node .js/.mjs; C linked to OpenSSL 3
  tier2/{go,typescript,c}/  same-file indirection in the other three languages
  tier3/python/<case>/      multi-module projects, entry point main.py
  tier3/java/<case>/        multi-package projects under src/, entry point com.acme.Main
  tier4/assets/             certs/ keys/ keystores/ ssh/ tls/ k8s/
  tier5/{python,java}/      obfuscated and hand-rolled code, plus compiled/ (.pyc, .jar)
  pqc/{python,java}/        ML-KEM, ML-DSA, an app-level hybrid, PQC-washing decoys
  pqc/go/                   crypto/mlkem and a hybrid-group tls.Config
  pqc/assets/               certs/ keys/ tls/ ssh/ with ML-DSA certs and hybrid groups
  calibration/tier{1,2}/    generated siblings of the Tier 1-2 cases for the overfit gap; not in headline numbers
  mixed/<lang>/             realistic-size modules, several sites each (generated: tools/build_mixed.py)
  deps/<app>/               dependency manifests: pip, PEP 621, Maven, Gradle, npm + lockfile, go.mod, Conan
  custom/<case>/            your own cases (BYOC); example_envelope ships as a worked example
  system/payments-platform/ one multi-service application: services, shared wrapper, artifacts, edge, deploy, infra
  negatives/{python,java,go,javascript,c,assets}/  zero-crypto controls
tier5-sources/              source of the compiled artifacts. Never scan this.
expected/
  ground_truth.json         the shipped answer key
  libraries.json            crypto libraries per dependency manifest, with versions, PQC capability, sources
  custom/<case>.json        answer keys for your own cases, one per case (BYOC)
  ground_truth.resolved.json  generated, with line numbers
  expected.cdx.json         generated reference CBOM, schema-valid CycloneDX 1.6
tools/
  cbomlib.py                normalizer, family tables, CycloneDX I/O
  build_expected.py         anchors -> lines -> reference CBOM
  score.py                  the scorer
  baseline_grep.py          naive regex scanner for calibration
  verify_corpus.py          runs every code case, parses every asset
  generate_tier4_assets.py  regenerates Tier 4 keys, certs and keystores
  build_tier5_compiled.py   rebuilds the Tier 5 .pyc and .jar from tier5-sources/
  generate_pqc_assets.py    regenerates the PQC certificates and key files
  policy.py                 deadline engine: rules, inheritance, buckets
  policy_report.py          date any CBOM against one or more policies (md, csv, json)
  test_policy.py            pins each deadline to its source; checks every rule cites a primary source, revision and section
  truth.py                  loads the shipped answer key plus confirmed BYOC cases
  actionability.py          checks reported fields against the rubric (ticket-ready, completeness)
  assetfacts.py             reads real certificate subject/issuer/validity and key formats from the corpus
  byoc.py                   bring your own code: new, draft, add, check, list
  libraries.py              dependency scoring: library names, manifests, versions, PQC verdicts
  run_qci_pqc.py            install, scan, score and gate the QCI PQC scanner in one command
  holdout.py                generate, verify and score private holdout sets; the overfit gap
  mixed.py                  ordinary-code templates and site picking for mixed files
  build_mixed.py            writes corpus/mixed/ and its ground truth from a fixed seed; --check
  release.py                the release stamp: answer key, corpus, scorer, policy and adapter hashes
  compare.py                side-by-side scorecards; refuses ones measured on different things
  render_docs.py            fills the README's generated tables from the release scorecards; --check
  rebaseline.py             resets gate floors from scored runs and stamps them for this release
  bench.py                  the one command: sandboxed scan, score, evidence bundle; verify; checks
  sandbox.py                the secure lane: scrubbed env, private read-only corpus, no network, limits
  linkage.py                system fixture: CODEOWNERS routing and asset links
  remediate.py              fix and rescan: apply the reference migrations, score verified remediation
  perf.py                   the large-repository fixture: generate, score by quarter of the tree
  holdout_assets.py         holdout certificates, keys, keystores, configs and compiled artifacts
  build_system.py           regenerates the system fixture's keys, certificates, binary and JAR
  make_names_only.py        regenerates reports/reference-names-only.cdx.json
  test_gates.py             gate enforcement: stale baselines, exit codes, report-only
  build_calibration.py      writes corpus/calibration/ (Tier 1-2 cells topped up to four); --check
  test_holdout.py           determinism, no answer leaks, metric extremes, every file runs
  adapters/qci_pqc.py       translates qci-pqc's CBOM; scores its risk categories as signals
  adapters/cdxgen.py        translates cdxgen's CBOM; HMAC/PBKDF2 context, crypto-file entries as signals
  adapters/common.py        signal coverage shared by adapters
  run_cdxgen.py             install, run and score cdxgen's CBOM mode
  compare.py                side-by-side comparison of any scorecards on one denominator
  test_normalize.py         108 naming-variant regression tests
  test_scorer.py            17 scorer credit/penalty tests
  test_qci_adapter.py       5 adapter checks (categories never leak into the strict score)
  test_cdxgen_adapter.py    filenames never read as algorithms; HMAC/PBKDF2 renames; unlocated left alone
  test_libraries.py         dependency scoring: decoys, look-alikes, versions, lockfile alt files, PQC verdicts
integrations/qci-pqc/       scope.json, gates.json, github-workflow.yml, FINDINGS.md
integrations/cdxgen/        NOTES.md: what cdxgen 12.9.1 finds, misses and gets wrong
policies/                   nist.json, eo14412-hva.json, cnsa2.json: rules, dates, sources
rubric/actionability.json   what a ticket needs: must/should checks mapped to CycloneDX fields
reports/                    scorecards and deadline reports land here
evidence/                   an evidence bundle per published scorecard (with fix-and-rescan), a perf bundle per
                            scanner, and checks.json (bench.py verify <dir>)
remediation/                migrations.json and after/: the reference migrations for fix-and-rescan
METHODOLOGY.md              the scoring rules, versioned; every scorecard records which version
Dockerfile                  the pinned environment; .github/workflows/ has CI and the release build
```

## Adding a case

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

## Judgment calls you may want to revisit

- **Dead code** isn't tested. Whether unreachable crypto belongs in a CBOM is a policy question
  (it ships, so arguably yes). Decide the policy before writing those cases.
- **Runtime-selectable vs config-selectable.** Branches chosen by a runtime argument or env var
  (`registry_strategy`, `strategy_factory`, `t2_dispatch_table.py`, `T2Enum.java`) make every option
  a required finding. Lookup tables only reached by editing config (`jwt_alg_mapping`'s HS384/HS512)
  count only the configured value; the others are accepted but not required.
- **Cipher suites are scored by name**, not decomposed. A scanner that reports
  `TLS_RSA_WITH_3DES_EDE_CBC_SHA` as RSA + 3DES + SHA-1 gets no suite credit, though the components
  are accepted without penalty. Suites are the unit an engineer edits in a config file.
- **TLS version floors.** `MinProtocol = TLSv1` in `openssl.cnf` requires TLS-1.0 only; higher
  versions are accepted, not required.
- **Default passwords.** Two PKCS#12 findings need `changeit`. If your policy is that scanners must
  not try passwords, filter on `requires_password` and score them separately.
- **Hashes inside signatures** are accepted, not required, in code (`SHA256withRSA` requires RSA).
  For certificates, the signature hash *is* required, because a SHA-1-signed certificate is a
  finding in its own right.
- **TLS cipher-suite names used purely as enum labels** (`NLookalikes.java`) are a negative.

- **Hand-rolled crypto is in scope.** Some would say a CBOM inventories library usage and
  homemade crypto is a code-review problem. The view here is that the inventory exists to find
  what needs replacing, and homemade RSA needs replacing more urgently than anything else in it.
- **Obfuscation vs. ordinary indirection.** Base64-encoded algorithm names are rare in honest code.
  Reflection and dynamic import aren't. If your scanner market only cares about non-hostile code,
  weight `T5Reflection.java` and `t5_dynamic_import.py` above the rest of the tier.

- **Hybrid policy.** A named hybrid group must be reported as the hybrid. If your organization only
  cares whether *some* PQ protection is present, you could accept ML-KEM in its place; that's a
  one-line change to `also_ok`, but it would stop distinguishing a hybrid from pure ML-KEM.
- **Kyber and Dilithium** get family credit as ML-KEM and ML-DSA, so recall doesn't punish a naming
  choice. The round-3 submissions and the FIPS standards are not byte-compatible, though, so every
  scorecard also reports **PQC by standard name**: the share of detected PQC findings reported under
  the FIPS name or OID. If you're auditing for FIPS 203/204 specifically, read that line, not recall.

## Roadmap

- **PQC extensions:** SLH-DSA (not yet in `cryptography`), LMS and XMSS for firmware signing (CNSA 2.0
  approves both), composite ML-DSA certificates once the IETF drafts settle, ML-DSA JWKs, and
  JSSE hybrid groups when the JDK ships them.
- **Tier 5 extensions:** native binaries (C against OpenSSL, Go with its stdlib crypto), minified
  JavaScript, ProGuard-obfuscated jars, algorithm names stored encrypted and decrypted at startup,
  hand-rolled AES with its S-box.
- **Tier 4 extensions:** Apache httpd and HAProxy configs, cipher-string macros (`HIGH:!aNULL`),
  IPsec/strongSwan, cloud KMS key specs in Terraform, certificates embedded in Java and Python
  source as string literals.
- **More languages:** Go and C# are the obvious next two.
- **Integration repo:** one realistic microservice mixing every tier for a headline number. The mixed
  files are the single-file version of this; a multi-file service with config, manifests and
  certificates is the next step.
- **Real scanner runs:** a results table with named tools is what turns this into a published benchmark.
