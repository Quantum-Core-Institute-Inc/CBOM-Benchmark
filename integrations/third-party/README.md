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

All five run to completion in the sandbox with these commands.

## Results

cryptoscan and qScan are the two open scanners chosen for the leaderboard, next to QCI PQC (the
reference product), cdxgen (existing baseline) and grep (calibration baseline). Both were measured
on benchmark 2.6.5 (410 findings) by the workflow, verified and read on 13 Nov 2026, and are
committed as `evidence/cryptoscan-1.5.0` and `evidence/qscan-0.12.0`. Both are columns in
`reports/comparison.md` as of 2.6.5.1. Their scores are the same as on 2.6.4.

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
  credited. It marks the corpus's LMS, XMSS and ML-KEM public keys as quantum-vulnerable without
  naming them. It skips minified files unless given `--scan-minified`; the workflow runs it with its
  defaults.

Neither has a holdout run or a timing run, so neither has an overfit gap or a row in the operations
table.

The other three run in the same workflow and were read the same way on 2.6.4, but are not published:
their bundles are not committed. Their scores stand as measured. pqcheck's and cbom-scan's
unrecognized names are categories or absent. quantascan names DSA as `Java JCA DSA` in 4 places,
which an adapter would fix for at most 4 findings.

| Scanner | Recall | Precision | Parameters correct | Status |
|---|---|---|---|---|
| pqcheck 0.1.0 | 19.8% | 98.8% | 56.8% | measured on 2.6.4, read, not published |
| quantascan 1.0.1 | 14.6% | 70.6% | 61.7% | measured on 2.6.4, read, not published |
| cbom-scan 0.1.0 | 12.0% | 83.1% | 55.1% | measured on 2.6.4, read, not published |

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

## Not yet measured

Tools a reader might expect to see here, and what each needs before it can be run. This list says
nothing about what any of them can do: a tool is described by its score once it has one, and by
nothing until then.

| Tool | Kind | What it needs to be measured |
|---|---|---|
| Semgrep, Opengrep | Open-source static analysis | A SARIF adapter (their output is findings, not a CBOM) and a chosen rule set, pinned. Both install from a package registry, so they fit the existing workflow. |
| CodeQL | Static analysis, free for public repositories | The same SARIF adapter, a CodeQL database built per language, and a pinned query pack. Its own workflow job. |
| SCANOSS crypto-finder | Open-source CBOM scanner | A pinned release and its local rule set, so the run needs no API key. |
| Mondoo xgrep | CBOM scanner | Its license confirmed for this use, then a pinned release. |
| CBOMkit-theia (IBM, PQCA) | Open-source, scans images and directories | A container-lane job (`--scanner-image`). Its registry couldn't be reached where this was written, so nothing about its command line is verified. |
| sonar-cryptography (IBM, PQCA) | Open-source SonarQube plugin | A SonarQube server and a build of each corpus project. A different kind of integration from pointing a command at a directory. |
| crypto-scanner 0.1.2 (PyPI) | Open-source | Emits its own JSON or HTML report, not CycloneDX. Needs a translation written against real output. |
| Commercial platforms | Vendor products | The vendor runs `bench.py run` on its own product and submits the evidence bundle; `bench.py verify` checks it. QCI does not run commercial products here and publishes nothing about one without a verified bundle. Check the vendor's terms before publishing a score. |

Runs on a scanner's holdout behaviour aren't made here (`--without-holdout`): the seed is a secret,
and this workflow is deliberately secret-free so that it can install and run code nobody at QCI wrote.
