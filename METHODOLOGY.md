# CBOM Testbench methodology

Methodology version: **2.3**

This is the normative description of how a scanner's CBOM becomes a score. The code in `tools/`
implements it; where the two disagree, that's a bug in one of them, and the regression suites
(`tools/test_*.py`) say which. Every scorecard records the methodology version that produced it
(`manifest.methodology`), and two scorecards with different versions are never compared.

A methodology version changes when a rule below changes in a way that can move a score. A testbench
release that only adds cases, fixes a case, or changes reporting keeps the version.

## 1. What is measured

**Ground truth.** `expected/ground_truth.json` lists findings: one cryptographic use each, with a
file, an algorithm family, expected parameters, and anchors (code text that resolves to line
numbers at build time). Calibration findings are scored but excluded from every headline number;
they exist for the overfit gap (section 6). BYOC findings (`expected/custom/`) are excluded from
anything compared across organizations.

**Denominator.** The shipped finding set: every finding that is neither calibration nor BYOC. Its
size and a hash of its ids are in every scorecard manifest (`scored_findings`, `finding_set`). A
declared scope (section 5) shrinks it, and the manifest says so.

**Input.** A CycloneDX 1.6 CBOM. All four crypto asset types are read; certificates and related
material are followed through their references. A scanner whose native format differs is translated
by an adapter in `tools/adapters/`, which documents every translation and whose hash is part of the
release stamp.

## 2. Matching

1. **Normalization.** Every reported name is mapped to a family and parameters by
   `tools/cbomlib.py` (`SHA1withRSA`, `sha1WithRSAEncryption`, `RS256` and `ssh-rsa` all mean RSA).
   OIDs count. Names the normalizer can't classify are listed and not penalized.
2. **Detected.** The family is reported in the finding's file, or in one of its listed `alt_files`
   (config and cross-file cases). Paths match by suffix, so absolute and relative paths both work.
3. **Site findings** (mixed files). Each reported occurrence goes to the site of that family whose
   anchor line is nearest, if it is within 3 lines. An occurrence without a line can't be placed.
4. **Parameters correct.** Every expected parameter matches within a single reported component.
5. **Line accurate.** A reported line within ±1 of any anchor. File-level assets aren't judged.
6. **Quantum flag.** If `nistQuantumSecurityLevel` is set, it is 0 exactly when the expected level is 0.
7. **Traceability.** Every result records the rule that decided it (`file+family`,
   `alt-file+family`, `site-match/window=3`, or why it was missed), and every false positive the
   rule that made it one (`unmatched`, `unplaced/window=3`).
8. **Standard name.** A post-quantum finding reported only under a pre-standard name (Kyber,
   Dilithium, SPHINCS+, Falcon, `X25519Kyber768Draft00`) is detected, with its parameters judged, but
   fails the standard-name check.

## 3. False positives

1. A reported (file, family) pair that matches no finding and isn't in that file's `also_ok` list.
2. In a file with site truth, a reported occurrence of a family the file uses that lands on no site
   of that family. Occurrences within 3 lines of each other are one report. Neutral, neither credit
   nor false positive: an occurrence on an import, include or require line, and a hash or MAC within
   3 lines of another algorithm's site.
3. **PQC over-claims** are the false positives whose family is post-quantum or hybrid.
4. False positives in calibration files are reported separately and excluded from precision.

## 4. Metrics

| Metric | Definition |
|---|---|
| Recall | detected / scored findings |
| At primary site | detected in the finding's own file / scored findings |
| Parameters correct | parameters correct / detected |
| Line accuracy | line accurate / detected findings with a judgeable line |
| Precision | detected / (detected + false positives) |
| PQC by standard name | detected PQC findings with at least one standard-name report / detected PQC findings |
| Ticket-ready | detected findings passing every applicable *must* check in `rubric/actionability.json` / detected |
| Actionable recall | ticket-ready / scored findings |
| Field completeness | applicable rubric checks passed / applicable checks |
| Deadline-weighted recall | recall with each finding weighted by when it falls due under the chosen policy: due now 5, by 2030 4, 2031–2033 3, 2034–2035 2, no deadline 1 |
| Library recall | expected crypto libraries reported in the right manifest / expected libraries |

Every bucket's recall carries a 95% Wilson interval, and a bucket with fewer than 10 findings is
marked thin. Comparison tables mark thin cells with †.

Rates are reported to one decimal place. Certificate subject, issuer, start and expiry dates and key formats in the rubric are checked
against the
real files, not just for presence. The rubric is proposed, not official: no official minimum CBOM
elements exist yet.

## 4a. The system fixture

`corpus/system/payments-platform` is one application: three services sharing a crypto wrapper and
its config, lockfiles, a built JAR and Go binary, TLS termination, a Kubernetes TLS secret, KMS keys
in Terraform, a certificate embedded in source, and a CODEOWNERS file. Its findings are scored like
any other (tier `system`), and two more numbers are reported:

- **Routable**: detected system findings with at least one reported location that resolves,
  through CODEOWNERS (last match wins), to the finding's owner. Where the wrapper and config decide
  the algorithm, the finding's file is the service's call site and the wrapper and config are alt
  files: reporting only those is detected but routed to the wrapper's owner.
- **Asset links**: for each linked pair of files in the answer key, a component located in the first
  references a component located in the second (a `*Ref`, `*RefArray` or cipher-suite `algorithms`
  entry in its cryptoProperties, or a `dependencies` entry).

## 4b. Fix and rescan

`remediation/migrations.json` lists reference migrations; each replaces one corpus file with
`remediation/after/<path>`, and every after-file runs. The scanner rescans the migrated corpus. A
migration is **eligible** when the scanner detected everything it retires beforehand, and
**verified** when, after: nothing it retires is still reported in that file (for a same-family
migration, no report there still carries the old parameters), every added algorithm is detected
with correct parameters, and every other finding in the file is detected exactly as before.
Verified remediation = verified / eligible. Changes outside the migrated files are reported as
regressions. Scored unscoped.

## 4c. Performance

`bench.py perf` generates a large tree from a public seed (ordinary code in five languages, large
data files, planted Tier 1 uses spread evenly) and gives the scanner a wall-clock budget. Reported:
whether it finished inside the budget, wall and CPU time, peak memory, files and MB per second,
recall on the planted uses overall and by quartile of position in the tree, and a coverage
fall-off flag when the last quartile is 25 points or more below the first. Not part of the headline.

## 5. Declared scope

A scanner may publish what it doesn't cover. A scope file has rules of three kinds: `glob` (files
the scanner doesn't read), `cert_role` (certificate signatures rather than keys), and `ids`.
Findings a rule matches are listed, not scored. Only `glob` rules also suppress that file's false
positives. Scoped scorecards are labelled as such and are not comparable with unscoped ones.

## 6. Generalization

A holdout set is generated from a private seed: fresh programs in the same tiers, languages and
families, plus fresh negative controls. The process that holds the seed generates the set; the
scanner runs in the sandbox (section 8) and never sees the seed; scoring happens afterwards.

- **Overfit gap.** Cells are (tier, language, family) present on both sides. The published side is
  the hand-written cases plus calibration cases in the same cells. Each cell's rate is drawn from its
  Beta posterior (Jeffreys prior) on both sides, 2,000 draws, each cell weighted by its holdout size
  so both numbers describe the same mix; the gap is published minus holdout, with a 95% interval. "Significant" means the interval excludes zero.
- **Negative-control gap.** False positives per negative file, holdout minus published, over the
  languages the generator covers.
- **Library gap.** Library recall, published minus holdout. Reported, not gated.

Since generator 1.1 a holdout set also holds certificates, keys and keystores with random
algorithms and containers, TLS and SSH configs with random protocol, suite and group lists, and
compiled `.pyc` and `.jar` artifacts. A generated finding enters the overfit gap only where the
published corpus has the same (tier, language, family) cell (Tier 4 assets, Tier 5 compiled, PQC
assets); anything else is scored as holdout-broad.

Evidence bundles record a commitment to the seed (`sha256("cbom-holdout:" + seed)`), never the seed,
so it can be revealed later and checked.

## 6a. Positions

Three questions a CBOM benchmark has to answer one way or the other. These are QCI's positions;
each is one field in the answer key if you need to score it differently.

- **Dead code counts.** Unreachable crypto (an uncalled function, a branch behind a constant false,
  statements after a return) is a finding. It ships, an auditor reads it, and a flag flip runs it.
  Tier `deadcode`; a scanner that prunes by reachability loses these.
- **Password-gated findings are scored separately.** A key or certificate that can only be read by
  trying a well-known default password (`requires_password` in the answer key) is scored and
  reported on its own line, and is in no headline number, bucket, gate or comparison. Whether a
  scanner should guess passwords is a policy choice, so a vendor that won't isn't penalised and one
  that does gets visible credit. The container's own protection (the PKCS#12's AES and PBKDF2),
  which needs no password to read, stays in the headline.
- **A hybrid must be reported as the hybrid.** `X25519MLKEM768` reported as ML-KEM or as X25519
  alone does not earn the hybrid finding (the parts are accepted without penalty). Which of the two
  is in use decides compliance under CNSA 2.0 and what a later migration looks like, so an inventory
  that can't tell them apart hasn't answered the question.

## 7. Comparability and gates

Two scorecards are compared only if their manifests agree on release, methodology, answer key,
corpus, scorer, policy and finding set, and neither is scoped (`tools/compare.py`; `--allow-scoped`
renders scoped ones with each denominator labelled).

Gates are floors or ceilings on metrics, stamped with the release they were measured on. They are
enforced only against that exact stamp; any other stamp means "not evaluated" (exit 3), never a pass.
Every gate is a required measurement. A gate whose metric the run didn't produce is reported as
missing and the run is "not evaluated" (or "fail", if another gate failed). A gate is skipped only
with a recorded reason: the gate declares that the measurement may legitimately be absent, or the
run was explicitly made without a holdout.
Three are policy limits that a rebaseline never moves: the scanner's own CBOM must validate as
CycloneDX 1.6; the lower bound of the overfit gap must not be above 0; and the negative-control gap
must not exceed 0.5 false positives per file.

## 8. Execution

Scanners and BYOC commands run in `tools/sandbox.py`: a private copy of the corpus (read-only mount
where the host allows), a scrubbed environment (no credentials, no holdout seed), no network where
the host allows, CPU, memory, file-size and wall-clock limits, and the input hashed before and after.
Where the host can make a mount namespace the run is also confined: home directories, temp
directories, the testbench tree (answer key, evidence, reports) and any holdout set are replaced by
empty mounts, and only the work directory, the toolchain directories on PATH and paths the
evaluator names are visible under them. The scanner's version command runs under the same rules.
With `--scanner-image` the scanner runs in its own container instead: its image, the inputs mounted
read-only, one output directory, no network, no capabilities; the bundle records the image id.
A scanner's build or install step is not sandboxed (it needs the network): it must run where no
secret exists, which for third-party scanners means a separate job.
Exit status, wall time, CPU time and peak memory are recorded. A run that modified its input, timed
out, or ran without network isolation when isolation was required is not scored. What isolation was
actually applied is recorded in the evidence bundle.

## 9. Version history

| Version | Testbench | Change |
|---|---|---|
| 1.0 | ≤ 1.16 | File-level false positives; id-level scope exclusions also suppressed false positives in the file; pre-standard PQC names fully credited. |
| 2.0 | 2.0.0 | Occurrence-level false positives in site files, with import and component neutrality (introduced in 1.17.0, versioned here); only `glob` scope rules suppress false positives; standard-name metric; comparability requires matching manifests; scanners run in the sandbox. |
| 2.1 | 2.1.0 | System fixture with routing and asset-link scores; fix-and-rescan; performance fixture; per-bucket intervals and thin-cell flags; per-result rule tracing; holdout generator 1.1 (assets, configs, compiled artifacts) feeds Tier 4, Tier 5 and PQC-asset cells into the overfit gap. |
| 2.2 | 2.2.0 | A missing gate measurement is 'not evaluated', never a pass; skips carry a reason. The rubric checks the values of certificate issuer, start date and key format, not their presence (can lower field completeness). Filesystem boundary in the sandbox; the version command runs inside it. |
| 2.3 | 2.3.0 | Dead-code tier (10 findings). Password-gated findings leave the headline and are reported separately (2 findings; also applied to PKCS#12 contents in holdout sets). Hybrid requirement stated as a position; no scoring change. |
