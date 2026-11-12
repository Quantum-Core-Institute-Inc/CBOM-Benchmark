# Submitting third-party scanner results

The public comparison table currently shows QCI, cdxgen and the grep baseline. External teams can contribute results without forking the methodology.

## How to submit

1. Produce a CycloneDX 1.6 CBOM against the released corpus (or use an adapter).
2. Run:
   ```bash
   python tools/bench.py run --name "YourScanner" \
       --scanner-cmd "your-scanner {corpus} -o {out}/cbom.json" \
       --bundle bundles/your-scanner \
       --require-isolation
   python tools/bench.py verify bundles/your-scanner
   ```
3. Open a pull request that adds:
   - `reports/your-scanner.md` and `.json`
   - `evidence/your-scanner/` (the verified bundle)
   - an entry in `reports/comparison.md` (or let `tools/render_docs.py` regenerate it)
   - a short note in `integrations/your-scanner/README.md` describing version, adapter and any declared scope

## Adapters

If your scanner does not emit CycloneDX 1.6 natively, add an adapter under `tools/adapters/`. Existing examples: `qci-pqc`, `cdxgen`.

## CI

`.github/workflows/third-party-scanners.yml` already runs a few open-source scanners as artifacts. Once a result has been reviewed it can be promoted into the published comparison table.

## Rules

- The stamp (release, methodology, finding set, answer-key hash) must match the release being scored.
- Declared scope is allowed and will be labeled.
- Results are published as measured; gate failures stay visible.
