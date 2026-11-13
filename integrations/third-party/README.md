# Third-party scanners

Open-source CBOM scanners that QCI doesn't maintain, run against the corpus by
`.github/workflows/third-party-scanners.yml`. Commercial scanners aren't run here: a vendor runs
`bench.py run` on its own product and submits the evidence bundle, which `bench.py verify` checks.

| Scanner | Pinned | Source | Command | Output |
|---|---|---|---|---|
| cbom-scan | 0.1.0 | PyPI | `cbom-scan scan {corpus} --format json --fail-on never --output {out}/cbom.json` | CycloneDX, declares spec 1.7 |
| pqcheck | 0.1.0 | PyPI | `pqcheck scan {corpus} --format cbom --output {out}/cbom.json` | CycloneDX CBOM |
| quantascan | 1.0.1 | npm | `quantascan {corpus} --format cyclonedx-cbom --output {out}/cbom.json` | CycloneDX 1.6 CBOM |
| cryptoscan | 1.5.0 | Go module `github.com/csnp/cryptoscan` (repository `csnp/qramm-cryptoscan`) | `cryptoscan scan {corpus} --format cbom --output {out}/cbom.json` | CycloneDX CBOM |
| qScan | 0.12.0 | npm `@quantakrypto/qscan` | `qscan {corpus} --cbom -o {out}/cbom.json` | CycloneDX 1.6 CBOM |

The commands were written from each package's command-line definition and all three run to
completion in the sandbox. First results, on benchmark 2.4.0 (393 findings, no adapter, no declared
scope, nobody has read the bundles yet):

| Scanner | Recall | Precision | Parameters correct | Verified migrations |
|---|---|---|---|---|
| cbom-scan 0.1.0 | 12.5% | 83.1% | 55.1% | 0 of 2 eligible |
| pqcheck 0.1.0 | 20.6% | 98.8% | 56.8% | 1 of 4 eligible |
| quantascan 1.0.1 | 15.3% | 70.6% | 61.7% | 0 of 2 eligible |

These are raw numbers, not published results. A scanner that names algorithms in a vocabulary the
normalizer doesn't know scores low here for a reason an adapter would fix, and none of the three has
been checked for that.

cryptoscan and qScan are the two open scanners chosen for the leaderboard, next to QCI PQC (the
reference product), cdxgen (existing baseline) and grep (calibration baseline). Both were measured on
benchmark 2.6.4 (410 findings), verified and read on 13 Nov 2026, and published in 2.6.4.1. A new
release does not carry their bundles forward: on 2.6.5 they are rerun by the workflow and return to
`reports/comparison.md` when the new bundles are read and committed. The corpus, answer key and
scorer did not change in 2.6.5, so the numbers below are expected to repeat.

| Scanner | Recall | Precision | Parameters correct | False positives | Adapter |
|---|---|---|---|---|---|
| cryptoscan 1.5.0 | 34.6% | 59.2% | 37.3% | 98, 26 in negative controls | none |
| qScan 0.12.0 | 18.3% | 83.3% | 17.3% | 15, 1 in negative controls | `tools/adapters/qscan.py` |

What reading them found:

- **cryptoscan** scores without an adapter. Of its 90 unrecognized occurrences, most are rule labels
  and not algorithms (`Hardcoded Key Size`, `TLS`, `Private Key Header`). It reports `SHA-3` with no
  output size 19 times and `Hybrid-KEM` 4 times; the answer key expects `SHA3-256` and a named
  hybrid group, and an adapter can't supply a detail the scanner didn't report. It has 18 PQC
  over-claims.
- **qScan** needs its adapter to be scored at all. It names components `DH (key-agree)` and writes
  locations as `path/File.java:12`; the adapter strips the suffix and splits the line, and nothing
  else. It reports asymmetric algorithms only, so it scores no symmetric, hash or MAC finding. It
  names 65 occurrences in scored files `unknown` in every field of its CBOM, so those can't be
  credited. It marks the corpus's LMS, XMSS and ML-KEM public keys as
  quantum-vulnerable without naming them. It skips minified files unless given `--scan-minified`;
  the workflow runs it with its defaults.

The other three were read the same way and their scores stand. pqcheck's and cbom-scan's
unrecognized names are categories or absent. quantascan names DSA as `Java JCA DSA` in 4 places,
which an adapter would fix for at most 4 findings. Their numbers on 2.6.4: pqcheck 19.8% recall,
98.8% precision; quantascan 14.6%, 70.6%; cbom-scan 12.0%, 83.1%.

## How a scanner gets into the comparison

A scanner goes into `reports/comparison.md` and the README when its bundle has been read by a
person, not when a job goes green. Before publishing a column for one of these:

1. Download its bundle from the workflow run and run `python tools/bench.py verify <bundle>`.
2. Read `scorecard.md` and the `unrecognized` list in `scorecard.json`. Names the normalizer can't
   classify are not penalized, so a scanner that names algorithms in its own vocabulary can score
   low for a reason an adapter would fix. If so, write the adapter (`tools/adapters/`), document
   every translation, and rerun.
3. Check that what the scanner declares it doesn't cover is handled as a declared scope, not as
   misses.
4. Commit the bundle under `evidence/`, add the scanner to `tools/compare.py`'s inputs and rerun
   `tools/render_docs.py`.

## Looked at and left out

| Scanner | Why |
|---|---|
| crypto-scanner 0.1.2 (PyPI) | Emits its own JSON or HTML report, not CycloneDX. Scoring it means writing a translation, and a translation written without seeing real output would be a guess. |
| CBOMkit-theia (IBM) | Scans container images and directories, and ships as a container image. Its registry couldn't be reached where this was written, so nothing about its command line is verified. It belongs in a container-lane job (`--scanner-image`), which is the next thing to add here. |
| sonar-cryptography (IBM) | A SonarQube plugin: needs a SonarQube server and a build of each corpus project. A different kind of integration from "point a command at a directory". |
| CodeQL cryptography queries | Needs a CodeQL database per language and a query pack; output is SARIF, not a CBOM. |

Runs on a scanner's holdout behaviour aren't made here (`--without-holdout`): the seed is a secret,
and this workflow is deliberately secret-free so that it can install and run code nobody at QCI wrote.
