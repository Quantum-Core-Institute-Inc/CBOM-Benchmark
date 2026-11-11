# Third-party scanners

Open-source CBOM scanners that QCI doesn't maintain, run against the corpus by
`.github/workflows/third-party-scanners.yml`. Commercial scanners aren't run here: a vendor runs
`bench.py run` on its own product and submits the evidence bundle, which `bench.py verify` checks.

| Scanner | Pinned | Source | Command | Output |
|---|---|---|---|---|
| cbom-scan | 0.1.0 | PyPI | `cbom-scan scan {corpus} --format json --fail-on never --output {out}/cbom.json` | CycloneDX, declares spec 1.7 |
| pqcheck | 0.1.0 | PyPI | `pqcheck scan {corpus} --format cbom --output {out}/cbom.json` | CycloneDX CBOM |
| quantascan | 1.0.1 | npm | `quantascan {corpus} --format cyclonedx-cbom --output {out}/cbom.json` | CycloneDX 1.6 CBOM |

The commands were written from each package's command-line definition, not from a run: none of
these has been executed against the corpus yet. The first run of the workflow is the test of this
table. If a command is wrong the job fails and `run.log` in the uploaded bundle says why.

## Why they aren't in the comparison yet

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
