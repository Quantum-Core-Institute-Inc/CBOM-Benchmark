# QCI CBOM Benchmark

> A graded test corpus and scoring harness for Cryptographic Bill of Materials (CBOM) scanners. It scores a scanner's CycloneDX 1.6 output against 410 known findings. Not a certification.

[![testbench](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/testbench.yml/badge.svg)](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/testbench.yml)
[![image](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/image.yml/badge.svg)](https://github.com/Quantum-Core-Institute-Inc/CBOM-Benchmark/actions/workflows/image.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Methodology 2.3](https://img.shields.io/badge/methodology-2.3-informational.svg)](METHODOLOGY.md)

**Version:** 2.6.6 · **Author:** Quantum Core Institute · **License:** Apache-2.0 ([LICENSE](LICENSE))

2.6.6 measures QCI PQC Scanner v2.3.4.5, which reads TLS cipher suites, minified JavaScript, compiled Java and native binaries: 76.6% recall (62.2% for v2.3.4.3), parameters correct on 92.7% of detections, no false positives. Every published number was measured on this release by `tools/release_run.sh`. cryptoscan and qScan return to the comparison when their bundles are rerun on 2.6.6. See [CHANGELOG.md](CHANGELOG.md).

[Release notes](CHANGELOG.md) · [Methodology](METHODOLOGY.md) · [Versioning](VERSIONING.md) · [Parameter cheat-sheet](PARAMETER_CHEATSHEET.md) · [Results](reports/comparison.md) · [Evidence](evidence/) · [Holdout sets](HOLDOUT.md) · [Bring your own code](BYOC.md)

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

QCI also publishes a scanner that this benchmark grades (`qci-pqc-scan`, currently v2.3.4.5). The
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
  v2.3.4.5 scores the same in both lanes (`evidence/qci-v2.3.4.5-container/`).
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

## Parameter recovery

Parameter completeness is now a first-class scorecard section. See [PARAMETER_CHEATSHEET.md](PARAMETER_CHEATSHEET.md) for the exact fields required.

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
| **Mixed** | Real-sized files that use several algorithms. A scanner that reports every occurrence of a family in the file, or only the first, is judged per site. | 62 |
| **System** | One application: three services sharing a crypto wrapper and its config, lockfiles, a built JAR and Go binary, TLS termination, a Kubernetes TLS secret, KMS keys in Terraform, a certificate embedded in source, and a CODEOWNERS file. | 26 |
| **Dead code** | Unreachable crypto (an uncalled function, a branch behind a constant false, statements after a return). | 10 |
| **Negatives** | Files that contain no crypto. | 28 |

## Versioning

Ordinary work stays on the 2.6 line as patch releases. See [VERSIONING.md](VERSIONING.md).

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
