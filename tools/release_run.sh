#!/usr/bin/env bash
# Measure a release: rescan every published scanner, set the gate floors, time the scanners on the
# large tree, run the required checks, and rebuild every evidence bundle. This is the only way a
# published number gets onto a new release; nothing is restamped. About 30 minutes on two cores.
#
#   QCI_BIN=/path/to/venv/bin/qci-pqc CDXGEN_BIN=/path/to/node_modules/.bin/cbom \
#   CBOM_HOLDOUT_SEED=<private seed> tools/release_run.sh
#
# Optional:
#   QCI_IMAGE=qci-scanner:<version>   also build the container-lane bundle (needs Docker and the image)
#   QCI_NAME="QCI v2.3.4.1"           name in reports; default asks the scanner for its version
#   CARRY=1                           keep existing gate floors as candidates (same corpus and answer key only)
#   LOGS=dir                          where the per-step logs go (default: a temp directory)
#   RESUME=checks                     skip the scans; rerun the required checks and rebuild the bundles around them
#
# Install the scanner non-editable, with its certificate extra: pip install "<checkout>[x509]".
set -euo pipefail
cd "$(dirname "$0")/.."
: "${QCI_BIN:?set QCI_BIN to the qci-pqc executable}"
: "${CDXGEN_BIN:?set CDXGEN_BIN to the cbom executable that cdxgen installs}"
: "${CBOM_HOLDOUT_SEED:?set CBOM_HOLDOUT_SEED (the private holdout seed)}"
# A measured release starts at revision 0; REVISION counts results added afterwards without rescoring.
if [ "$(cat REVISION 2>/dev/null || echo 0)" != "0" ]; then
  echo "REVISION is $(cat REVISION): bump VERSION and set REVISION to 0 before measuring a release." >&2; exit 1
fi
SEED="$CBOM_HOLDOUT_SEED"
unset CBOM_HOLDOUT_SEED   # only the scanner runs below get it; the benchmark's own tests must not
LOGS="${LOGS:-$(mktemp -d)}"; mkdir -p "$LOGS"
VERSION="$(cat VERSION)"
QCI_VERSION="$("$QCI_BIN" --version | awk '{print $NF}')"
QCI_NAME="${QCI_NAME:-QCI v$QCI_VERSION}"
QCI_SLUG="qci-v$QCI_VERSION"
[ -n "${QCI_IMAGE:-}" ] && export CBOM_TEST_SCANNER_IMAGE="$QCI_IMAGE"
QCI_CMD="scan {corpus} --reproducible --adapter internal --out {out} --json"
CDX_CMD="$CDXGEN_BIN --spec-version 1.6 --no-install-deps --evidence -o {out}/cbom.json {corpus}"
GREP_CMD="python3 $PWD/tools/baseline_grep.py {corpus} -o {out}/cbom.json"
step() { echo "== $1 $(date +%H:%M:%S)"; }
qci() { python3 tools/run_qci_pqc.py --qci-bin "$QCI_BIN" --out reports/qci-pqc --holdout-seed "$SEED" $1 > "$LOGS/qci-$2.log" 2>&1 || true; }

bundles() {
  local C=""; [ -n "$1" ] && C="--checks $1"
  CBOM_HOLDOUT_SEED="$SEED" python3 tools/bench.py run --name "$QCI_NAME" --adapter qci-pqc --scanner-cmd "$QCI_BIN $QCI_CMD" --version-cmd "$QCI_BIN --version" \
    --scope integrations/qci-pqc/scope.json --gates integrations/qci-pqc/gates.json $C --remediation --require-isolation --bundle "evidence/$QCI_SLUG" --force > "$LOGS/bundle-qci.log" 2>&1 || true
  if [ -n "${QCI_IMAGE:-}" ]; then
    CBOM_HOLDOUT_SEED="$SEED" python3 tools/bench.py run --name "$QCI_NAME (own container)" --adapter qci-pqc --scanner-image "$QCI_IMAGE" --scanner-cmd "qci-pqc $QCI_CMD" --version-cmd "qci-pqc --version" \
      --scope integrations/qci-pqc/scope.json --gates integrations/qci-pqc/gates.json $C --remediation --require-isolation --bundle "evidence/$QCI_SLUG-container" --force > "$LOGS/bundle-qci-container.log" 2>&1 || true
  fi
  python3 tools/bench.py run --name "cdxgen 12.9.1" --adapter cdxgen --scanner-cmd "$CDX_CMD" --version-cmd "$CDXGEN_BIN --version" $C --remediation --require-isolation --bundle evidence/cdxgen-12.9.1 --force > "$LOGS/bundle-cdxgen.log" 2>&1
  python3 tools/bench.py run --name "grep baseline" --scanner-cmd "$GREP_CMD" --allow-path tools --scanner-version "benchmark $VERSION" $C --remediation --require-isolation --bundle evidence/grep-baseline --force > "$LOGS/bundle-grep.log" 2>&1
  python3 tools/bench.py run --name "answer key" --scanner-cmd "cp $PWD/expected/expected.cdx.json {out}/cbom.json" --allow-path expected --scanner-version "benchmark $VERSION" $C --require-isolation --bundle evidence/answer-key --force > "$LOGS/bundle-key.log" 2>&1
}

if [ "${RESUME:-}" != checks ]; then

step baselines
python3 tools/build_expected.py > /dev/null
python3 tools/baseline_grep.py > /dev/null
python3 tools/score.py reports/baseline_grep.cdx.json --name "grep baseline" --exclude-custom --out reports/baseline_grep > /dev/null
python3 tools/score.py expected/expected.cdx.json --name reference --exclude-custom --out reports/reference > /dev/null
python3 tools/make_names_only.py > /dev/null
python3 tools/score.py reports/reference-names-only.cdx.json --name "reference, names only" --exclude-custom --out reports/reference-names-only > /dev/null

step "scanner runs (report only)"
qci --report-only report &
python3 tools/run_cdxgen.py --cbom-bin "$CDXGEN_BIN" > "$LOGS/cdxgen.log" 2>&1 &
wait
grep -q "Traceback" "$LOGS/qci-report.log" && { tail -5 "$LOGS/qci-report.log"; echo "the QCI run failed; see $LOGS/qci-report.log"; exit 1; }

step rebaseline
python3 tools/rebaseline.py ${CARRY:+--carry} reports/qci-pqc/scorecard.json

step "scanner run (gated)"
qci "" gated
grep -h "GATES" "$LOGS/qci-gated.log" || true

step perf
rm -rf evidence; mkdir evidence
python3 tools/bench.py perf --name "$QCI_NAME" --adapter qci-pqc --scanner-cmd "$QCI_BIN $QCI_CMD" --size medium --require-isolation --bundle "evidence/perf-$QCI_SLUG" --force | tail -1
python3 tools/bench.py perf --name "cdxgen 12.9.1" --adapter cdxgen --scanner-cmd "$CDX_CMD" --size medium --require-isolation --bundle evidence/perf-cdxgen-12.9.1 --force | tail -1
python3 tools/bench.py perf --name "grep baseline" --scanner-cmd "$GREP_CMD" --allow-path tools --size medium --require-isolation --bundle evidence/perf-grep-baseline --force | tail -1

step "bundles (first pass)"
bundles ""
python3 tools/render_docs.py | tail -1

fi

step checks
python3 tools/bench.py checks --out "$LOGS/checks.json" > "$LOGS/checks.log" 2>&1 || { grep "FAIL" "$LOGS/checks.log" || true; echo "REQUIRED CHECKS FAILED: see $LOGS/checks.log"; exit 1; }
tail -1 "$LOGS/checks.log"
cp "$LOGS/checks.json" evidence/checks.json

step "bundles (with checks)"
bundles evidence/checks.json
python3 tools/render_docs.py --check | tail -1
fail=0
for b in evidence/*/; do r="$(python3 tools/bench.py verify "$b" | tail -1)"; echo "$b $r"; case "$r" in *"does NOT"*) fail=1;; esac; done
python3 tools/stamp.py | tail -1
step done
exit $fail
