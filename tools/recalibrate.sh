#!/usr/bin/env bash
# Five-seed holdout recalibration.
# Requires: the QCI scanner checkout, CBOM_HOLDOUT_SEED or --seed, and a published scorecard.
# Usage: ./tools/recalibrate.sh /path/to/qci-pqc-scan reports/qci-pqc/scorecard.json
set -euo pipefail
SCANNER="${1:?scanner checkout}"
PUBLISHED="${2:?published scorecard}"
SEEDS=(8410375 1902847 5529103 7741208 3084716)
mkdir -p recalibration
for seed in "${SEEDS[@]}"; do
  echo "=== seed $seed ==="
  python tools/holdout.py generate --seed "$seed" --out "recalibration/$seed"
  python tools/run_qci_pqc.py --scanner "$SCANNER" --holdout-seed "$seed" \
      --out "recalibration/$seed/scan" || echo "scan failed for $seed"
  python tools/holdout.py score "recalibration/$seed/scan/cbom.json" \
      --dir "recalibration/$seed" --published "$PUBLISHED" \
      > "recalibration/$seed/gap.txt" || echo "score failed for $seed"
done
echo "=== summary ==="
grep -H "overfit" recalibration/*/gap.txt || true
