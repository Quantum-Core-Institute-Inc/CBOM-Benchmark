# Rescan and Rebaseline under Current Stamp

## Goal
Bring every published scorecard, comparison table, and evidence bundle up to the current release stamp (VERSION 2.6.1 or the next 2.6.x).

## Tasks
1. Run `python tools/bench.py checks` and confirm green.
2. Rescan QCI v2.3.4.1 (and any other published scanners) with `tools/run_qci_pqc.py` / `bench.py run`.
3. Rebuild evidence bundles and verify them (`bench.py verify`).
4. Regenerate `reports/comparison.md`, `reports/qci-pqc/SUMMARY.md`, and related tables via `tools/render_docs.py`.
5. Rebaseline gates with `tools/rebaseline.py` so floors match the current stamp.
6. Update CHANGELOG with a short 2.6.x entry noting the rescan.

## Acceptance
- Every published report header shows the same VERSION, methodology, finding count, and answer-key hash.
- All evidence bundles verify.
- Gates pass or fail explicitly against the new stamp (no silent carry-over of stale floors).
