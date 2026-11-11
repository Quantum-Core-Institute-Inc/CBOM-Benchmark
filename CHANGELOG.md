# Changelog

## 2.4.0 (2026-11-11): more of what's deployed

55 new findings, 393 in all. No scoring rule changed, so the methodology stays 2.3; the release, the
corpus and the answer key are part of every stamp, so 2.3.0 scorecards and gates don't carry over.
Every scanner rescanned; gates rebaselined; evidence rebuilt.

- **C#.** A seventh language. 14 single-file .NET 8 projects, 19 findings: Tier 1 (`MD5.HashData`,
  `RSA.Create(2048)`, `ECDiffieHellman`, `AesGcm`, `TripleDES`, `Rfc2898DeriveBytes.Pbkdf2`, `DSA`)
  and Tier 2 (constants, `IncrementalHash` by name, a `Func<HashAlgorithm>` table, a settings class
  behind a wrapper, a curve picked by a helper). Two negative controls. Each project builds with an
  empty package source list, so nothing is fetched.
- **LMS and XMSS.** The stateful hash-based signatures of SP 800-208, which CNSA 2.0 wants for
  firmware signing first. Bouncy Castle signing code for each, an HSS/LMS and an XMSS public key
  recognisable only by OID, and a firmware signing policy naming both beside a P-384 signer kept for
  old devices: 7 findings. The NIST and CNSA 2.0 policies gain a rule for them (approved, for
  software and firmware signing, state kept in hardware). The normalizer reads `LMS_SHA256_M32_H10`
  as LMS, not SHA-256. There's no Python case yet: installing the PyPI LMS package was blocked where this was built.
- **Harder Tier 5.** Three artifacts with no source in the corpus, 9 findings: a ProGuard-obfuscated
  jar (names replaced, algorithm strings intact), a minified JavaScript bundle, and a stripped ELF
  binary that shows MD5 and 3DES only as imported libcrypto symbols and its RSA key size only as an
  immediate operand. Sources are in `tier5-sources/`; `build_tier5_compiled.py` rebuilds them.
- **More config formats.** Apache httpd (`SSLProtocol -all +TLSv1.1 +TLSv1.2`), HAProxy (a minimum
  version, TLS 1.2 and 1.3 suites on separate lines, the DH group size on a tuning line), and
  strongSwan in both spellings (`swanctl.conf` proposals and a legacy `ipsec.conf` with
  `3des-sha1-modp1024!`): 20 findings. The normalizer reads `modp2048` as a 2048-bit DH group.
- **Toolchain.** The corpus check needs the .NET 8 SDK and Bouncy Castle's provider jar
  (`libbcprov-java`); CI and the Dockerfile install both. The Dockerfile's new .NET stage is
  untested here, like the rest of the image.
- **QCI v2.3.4 on the new cases:** 68.6% recall in scope (74.7% on 2.3.0), two new false positives,
  three gates failed. Details in `integrations/qci-pqc/FINDINGS.md`.
- **Fixes.** The docs check reports a missing or half-written evidence bundle instead of crashing on
  it. Calibration cases are only generated for languages that have a generator.
- **Not covered by the holdout generator.** None of the above has a generator yet, so these 55
  findings don't enter the overfit gap (HOLDOUT.md says so).

## 2.3.0 (2026-11-11): three positions

Methodology 2.3. The headline denominator is now 338 findings (330, plus 10 dead-code, minus 2
password-gated). Every scanner rescanned; gates rebaselined; evidence rebuilt.

- **Dead code counts.** New tier, ten findings in five languages: uncalled functions, branches behind
  a constant false, statements after a return. Every file runs.
- **Password-gated findings are scored separately.** The RSA key and SHA-256 signature inside the
  PKCS#12 keystore, readable only with the default password, are reported on their own line and are
  out of every headline number, gate and comparison. Holdout sets mark PKCS#12 contents the same way.
- **A hybrid must be reported as the hybrid.** Already the scoring rule; now written down as QCI's
  position in METHODOLOGY.md, section 6a, with the other two.

## 2.2.0 (2026-11-11): evidence that fails when it should

The response to the external review of 2.1.0. All five of its findings reproduced, and each fix has
a regression test built from the reviewer's own reproduction. Methodology 2.2. Every scanner was
rescanned, the gates rebaselined first and the scanners run after, and all evidence rebuilt.

**P0: a current baseline could pass with nothing measured**
- Every gate is now a required measurement. A missing one makes the run "not evaluated" (exit 3),
  or "fail" if another gate failed, and is listed by name. A skip needs a reason on record:
  `--without-holdout`, or `when_missing: skip` in the gates file. The shipped baseline with no
  metrics now exits 3 with every gate listed.

**P0: a bundle could verify without its evidence**
- `bench.py verify` requires the artifacts each claim rests on (a scored or finished bundle without
  its raw CBOM fails) and re-derives every section of every scorecard, including libraries and
  linkage, plus the fix-and-rescan result, the schema verdict and the gate verdict (the gates file
  and the metrics it was applied to are in the bundle).
- The holdout result can't be re-derived without the private seed; verify now says so instead of
  staying silent, and `verify --holdout-seed --holdout-cbom` re-derives it after a reveal.

**P0 for external submissions: isolation**
- The sandbox has a filesystem boundary: home and temp directories, the testbench tree with its
  answer key, and any holdout set are hidden behind empty mounts. `--allow-path` names exceptions,
  and they're recorded. `--require-isolation` now requires the boundary as well as the network cut.
- The scanner's `--version` call runs in the sandbox. The install step, which can't, gets an
  environment with the seed and credentials removed.
- The scanner workflow is two jobs: build wheels with no secrets, then install the wheels (no build
  code) and score with the seed. Tested locally: the wheel hand-off installs and runs.

**P1: the image and the bytecode**
- The Dockerfile used Python 3.12 while the corpus ships Python 3.13 bytecode, and the strict check
  counts that as a skip: the first image build would have failed. The image and the main CI job now
  use 3.13; a separate CI job proves the harness on 3.11. The image is still unbuilt (no registry
  access from here), so a clean tagged build remains the outstanding proof.

**P1: reports and evidence disagreed about the gates**
- `tools/rebaseline.py` replaces an ad hoc script. Each run writes `gates-result.json`; SUMMARY.md
  and the bundle's `gates.md` are rendered from the same function; the docs check fails if a report
  directory and its bundle give different verdicts, or if a published report is report-only.

**Closing the items first reported as open (same day, same stamp)**
- **Container lane.** `bench.py run --scanner-image` runs the scanner in its own container: only the
  corpus (read-only) and an output directory, no network, no capabilities, read-only root. This is
  the answer to "system directories stay readable". QCI v2.3.4 scores identically in it.
- **The boundary inside a container is now tested, and was broken.** It depended on a `/mnt`
  directory; an image without one silently ran unconfined even with `SYS_ADMIN`. Fixed, and tested
  in three container configurations.
- **The release Dockerfile builds.** Registries are blocked here, so the official bases can't be
  pulled; the Dockerfile was built unmodified against stand-in bases with the same layout (strict
  corpus check included), and the release workflow's container steps were run against that image.
  Not yet proven: the real base images, the apt step, a digest from a tagged build.
- **The scanner workflow's steps were run locally** end to end (wheels, binary-only install, gated
  scoring with holdout and fix-and-rescan, bundle verify). Not yet proven: the workflow on GitHub.

**From the reviewer's "world class" list**
- The rubric now checks the value of a certificate's issuer and start date and a key's format,
  not just that the field is filled in.

## 2.1.0 (2026-11-11): real systems

Phase 3. Methodology 2.1. 26 new findings (330 in all), so every number moved a little; every
scanner was rescanned and rescored, the gates were rebaselined (the better of QCI v2.2 and v2.3 on
each metric, measured on 2.1), and the holdout was recalibrated over five seeds.

**A system, not a file**
- `corpus/system/payments-platform/`: a Go API, a Python worker and a Java service sharing one crypto
  wrapper (in three languages) and one config; lockfiles; a built JAR and a stripped Go binary;
  nginx TLS termination with its certificate and key; a Kubernetes TLS secret; KMS keys in Terraform
  (one relying on the AWS default, AES-256-GCM); a partner CA pasted into Python source; CODEOWNERS.
  `tools/build_system.py` rebuilds the keys and artifacts; `verify_corpus.py` runs all of it.
- Two new scores: **routable** (a reported location resolves through CODEOWNERS to the team that
  owns the fix; reporting only the shared wrapper or config doesn't) and **asset links** (the CBOM
  connects the nginx config to its certificate, and the certificate to its key).

**Fix and rescan**
- `remediation/`: ten reference migrations (RSA to ML-DSA-65, ECB/CBC/3DES to AES-256-GCM in five
  languages, nginx to TLS 1.3 with X25519MLKEM768, sshd to ML-KEM hybrid KEX), every after-file runs.
  `bench.py run --remediation` rescans and scores verified remediation per migration.

**Big trees**
- `bench.py perf`: a generated tree (600 / 3,000 / 12,000 code files plus large data files) with
  planted uses spread evenly, a time budget, and recall by quarter of the tree to catch scanners that
  give up partway. Wall time, CPU, peak memory and throughput are recorded; the bundle re-verifies.

**Holdout generator 1.1**
- Certificates, keys and keystores with random algorithms and containers, TLS/SSH configs with random
  suites and groups, ML-DSA certificates, and compiled `.pyc`/`.jar` artifacts. They feed the overfit
  gap where the published corpus has the same cell (Tier 4, Tier 5, PQC assets). Recalibrated:
  never significant for grep or any QCI release, interval width 9.0 to 10.2 points.

**Uncertainty and traceability**
- Every scorecard bucket has a 95% Wilson interval on recall; buckets under ten findings are marked
  thin, and comparison tables mark thin cells with †.
- Every result records the rule that decided it, and every false positive the rule that made it one.

**QCI v2.3.4 (added after release, same stamp)**
- The published QCI column, `reports/qci-pqc/` and its evidence bundles are now v2.3.4, which scores
  identically to v2.3.0 on every measure. Review in `integrations/qci-pqc/FINDINGS.md`.

**Fixes found on the way**
- A certificate embedded in source is judged on asset fields, not code fields; PKCS#1 private keys
  report their format.
- `reports/reference-names-only.cdx.json` now has a generator (`tools/make_names_only.py`).

## 2.0.0 (2026-11-11): reproducible runs

Phase 2. No scoring rule changed, so every number from 1.17 stands; the release and methodology are
now part of every stamp, so 1.17 scorecards and gates need a rescore (done for everything shipped).

**One command, one bundle**
- `tools/bench.py run`: scans in the sandbox, scores, and writes an evidence bundle (raw output,
  adapted CBOM, scorecards, manifest, `SHA256SUMS`). `bench.py verify` re-derives every number from
  the raw CBOM and names any file that differs from the release it was scored on; a doctored number
  fails even with recomputed checksums. `bench.py checks` runs the required checks.
- `evidence/` ships a bundle for every published scorecard, with the required-check results.

**Secure lane**
- `tools/sandbox.py`: scrubbed environment (no credentials, never the holdout seed), a private
  corpus copy hashed before and after (read-only mount where possible), no network (namespace or
  `--network none`), wall/CPU/memory/file-size limits, and exit status, time and peak memory
  recorded. Scanner runs (`bench.py`, `run_qci_pqc.py`), holdout scans and BYOC commands use it.
- The holdout seed stays in the process that generates the set; bundles carry a commitment to it.

**Methodology and environment**
- `METHODOLOGY.md`, versioned (2.0). Every scorecard and stamp records the version; `compare.py`
  and the gates refuse mismatches.
- `Dockerfile`: pinned toolchains, the whole corpus verified at build time, toolchain versions
  recorded into every bundle. Not built yet: the environment this release was prepared in can't
  reach Docker Hub, so the first tagged build on GitHub is the first build. The bundles in
  `evidence/` say "not containerized" for that reason.
- `.github/workflows/release.yml`: on a tag, build the image, run the checks inside it with no
  network, build reference bundles, attach the evidence to the release; push and cosign signing
  are switches. `testbench.yml` now runs the same check list (`bench.py checks`).
- The scanner-side workflow template uploads an evidence bundle and pins `v2.0.0`.

## 1.17.0 (2026-11-11): score integrity

Phase 1 of the response to the external review of 1.16.1. Every scanner was rescanned and rescored
on this release; older scorecards can't be compared with these (compare.py refuses them).

**Gates and comparisons can't pass silently any more**
- Gates carry a release stamp (`tools/release.py`: version, finding count, answer key, corpus,
  scorer, policy and adapter hashes) and are enforced only on that stamp. A stale or missing
  baseline exits **3**, not 0. `--report-only` (alias `--no-gate`) exits 0 and says so.
- `gates.json` rebaselined on 1.17: each ratchet floor is the better of QCI v2.2 and v2.3.
- Every scorecard has a manifest. `compare.py` refuses scorecards with different finding sets,
  corpus, answer key, scorer, policy or scope (exit 2); `--allow-scoped` labels each denominator.
- The scanner-side workflow template pins `TESTBENCH_REF: v1.17.0` and installs `requirements.txt`.

**Precision is counted per occurrence where the truth is per site**
- In mixed files, a report more than 3 lines from every site of its family is a false positive
  even if the file uses that family elsewhere. Import lines and a hash/MAC at another algorithm's
  site are neutral.
- Declared-scope exclusions by id no longer suppress a file's false positives; only glob rules do.
- The reviewer's three reproductions are regression tests in `test_scorer.py`.

**Provenance**
- NIST, CNSA 2.0 and EO 14412 policies cite primary sources with revision, publication date and a
  section on every rule; `test_policy.py` enforces it. SP 800-131A now links Rev. 2 (final), with
  the Rev. 3 draft listed separately; IR 8547 links CSRC. TLS 1.0/1.1 and secp256k1 are `review`;
  SSL 2/3 are not approved.
- Pre-standard PQC names (Kyber, Dilithium, SPHINCS+, Falcon, X25519Kyber768Draft00) keep discovery
  credit and fail the new **PQC by standard name** metric.

**Setup, verification and docs**
- `requirements.txt` / `requirements-verify.txt` pin dependencies; tools require Python 3.11+.
- `verify_corpus.py` reports pass/fail/skip per area; `--strict` exits 4 on any skip.
- `.github/workflows/testbench.yml` verifies the testbench itself: strict corpus run, reproducible
  answer key and generated corpora, every test suite, a 100% reference replay, and a docs check.
- `tools/render_docs.py` generates the README's result tables from the release scorecards
  (`--check` in CI). The grep 70.8% vs 70.4% mismatch is gone: every table is the 304-finding
  shipped corpus.
