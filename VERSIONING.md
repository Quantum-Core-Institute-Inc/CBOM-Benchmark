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

- **Results revision (2.6.4.1, 2.6.4.2, …)** when results are added to the published set and nothing
  is rescored: a new scanner's verified bundle, a new comparison column, documentation of what a
  reading found. The fourth number is the `REVISION` file. `VERSION` does not change, so the stamp
  does not change, and every published scorecard and bundle stays valid without being touched. A
  revision may not change the corpus, the answer key, a scorer file or a policy; `python
  tools/stamp.py` and `bench.py verify` on every bundle fail if it did. The next patch release
  resets `REVISION` to 0.

- **Minor (2.7.0)** only when a scoring rule itself changes in a way that can move numbers on existing findings. That also requires a methodology version bump in `METHODOLOGY.md`.

- **Major** only for breaking changes to the stamp format, the public corpus layout, or the scorecard schema that cannot be handled by the existing comparability checks.

## Stamp (comparability)

Every scorecard and evidence bundle records a stamp (`tools/release.py`):

- release (VERSION; a results revision in `REVISION` is not part of the stamp)
- methodology
- findings count + finding-set hash
- answer-key hash
- corpus hash
- scorer hash
- policy hash

`tools/compare.py` and the gates refuse to compare or enforce against a mismatched stamp. Finding-count or answer-key changes are therefore visible and do **not** by themselves require a minor version bump.

## Next release

The next release is **2.6.7**. Subsequent ordinary work stays on the 2.6 line until a deliberate methodology or breaking change.

## Measuring a release

A stamp says what a number was measured on: the release, the corpus, the answer key, the scorer and
the policy. It is evidence, so it is never edited. Any change to `VERSION`, the corpus, the answer
key, the scorer files or a policy makes every published scorecard, the gates file and every
evidence bundle stale, and the only way to bring them forward is to measure again:

```bash
QCI_BIN=... CDXGEN_BIN=... CBOM_HOLDOUT_SEED=... tools/release_run.sh
```

That rescans every published scanner, sets the gate floors, times the scanners, runs the required
checks, rebuilds the evidence bundles and verifies them: about 30 minutes. `python tools/stamp.py`
lists anything still measured on another tree and exits 1 if there is any.

Releases 2.6.1 to 2.6.3 were published by rewriting the release field and scorer hash in place
instead. Their evidence bundles did not verify and their holdout generator did not run; 2.6.4 is the
first release since 2.6.0 whose numbers were measured on its own code.
