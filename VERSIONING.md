# Versioning policy

The CBOM Benchmark uses **patch-level releases** for ordinary work. The current line is **2.6**.

## Rules

- **Patch (2.6.1, 2.6.2, …)** for:
  - New or improved corpus cases
  - Documentation
  - Tooling, adapters, CI, and evidence
  - Additive metrics and scorecard sections (e.g. a dedicated Parameter Recovery section)
  - Holdout-generator extensions
  - Bug fixes that do not change existing scoring rules

- **Minor (2.7.0)** only when a scoring rule itself changes in a way that can move numbers on existing findings. That also requires a methodology version bump in `METHODOLOGY.md`.

- **Major** only for breaking changes to the stamp format, the public corpus layout, or the scorecard schema that cannot be handled by the existing comparability checks.

## Stamp (comparability)

Every scorecard and evidence bundle records a stamp (`tools/release.py`):

- release (VERSION)
- methodology
- findings count + finding-set hash
- answer-key hash
- corpus hash
- scorer hash
- policy hash

`tools/compare.py` and the gates refuse to compare or enforce against a mismatched stamp. Finding-count or answer-key changes are therefore visible and do **not** by themselves require a minor version bump.

## Next release

The next release is **2.6.2**. Subsequent ordinary work stays on the 2.6 line until a deliberate methodology or breaking change.

## Restamping published artifacts

A patch-level VERSION bump does not change the corpus, answer key, or scorer, but published
scorecards, gates, and evidence manifests still carry the previous release in their stamp.
`python tools/stamp.py` updates the release field in:

- `reports/*/scorecard*.json`
- `integrations/qci-pqc/gates.json`
- every `evidence/*/manifest.json`

Run it after editing `VERSION`, then commit the result. `python tools/stamp.py --check` exits 1
if any file still carries an older release (useful in CI).
