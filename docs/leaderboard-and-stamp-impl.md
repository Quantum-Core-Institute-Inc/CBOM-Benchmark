# Leaderboard Refresh under Current Stamp

## Goal
Update the published comparison so it no longer says “Testbench 2.6.0” and includes more than QCI + cdxgen + grep. All published numbers must carry the current release stamp.

## Tasks

1. Regenerate `reports/comparison.md` under the current stamp (2.6.1 or later) via `tools/render_docs.py`.
2. Promote reviewed results from `.github/workflows/third-party-scanners.yml` artifacts into the published table once they have been read.
3. Add adapters (if needed) for at least two additional open CycloneDX 1.6 producers.
4. Ensure every published scorecard carries a matching evidence bundle with the current stamp.
5. Document the submission path in `THIRD_PARTY.md` (already present).

## Acceptance

- Comparison header matches current VERSION and methodology.
- At least one additional open scanner appears with verified numbers (or a clear “artifact only” label if not yet promoted).
- Stamp checks pass (`tools/compare.py` refuses mismatches).
- `python tools/render_docs.py --check` exits 0.
