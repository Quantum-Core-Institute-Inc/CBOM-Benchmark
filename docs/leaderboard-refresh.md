# Leaderboard Refresh

## Goal
Update the published comparison so it no longer says “Testbench 2.6.0” and includes more than QCI + cdxgen + grep.

## Tasks
1. Regenerate `reports/comparison.md` under the current stamp (2.6.1 or later).
2. Promote reviewed results from `.github/workflows/third-party-scanners.yml` artifacts into the published table.
3. Add adapters (if needed) for at least two additional open CycloneDX 1.6 producers.
4. Document the submission path in `THIRD_PARTY.md` (already present).
5. Ensure every published scorecard carries a matching evidence bundle.

## Acceptance
- Comparison header matches current VERSION and methodology.
- At least one additional open scanner appears with verified numbers.
- Stamp checks pass (`tools/compare.py` refuses mismatches).
