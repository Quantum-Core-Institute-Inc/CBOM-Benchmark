#!/usr/bin/env bash
# Run CodeQL over a mixed-language tree and write one SARIF file.
#   codeql-scan <source dir> <output dir>
# CodeQL analyzes one language at a time, so this builds a database per language, runs that
# language's security-extended suite, and merges the runs into <output dir>/results.sarif.
# Nothing is compiled: every language that allows it is extracted with --build-mode=none, which is
# what GitHub's default setup does for a repository with no build configured. Go has no such mode
# and uses CodeQL's own build tracing. A language that fails is reported and skipped, not fatal.
# The workflow replaces @CODEQL@ with the path of the CLI on the runner.
set -u
CODEQL="@CODEQL@"
SRC="$1"; OUT="$2"
WORK="$(mktemp -d)"
mkdir -p "$OUT/codeql"
status=0
for spec in python:none java-kotlin:none javascript-typescript:none c-cpp:none csharp:none go:autobuild; do
  lang="${spec%%:*}"; mode="${spec##*:}"
  pack="${lang%%-*}"; [ "$lang" = "c-cpp" ] && pack=cpp
  echo "== $lang ($mode)"
  if ! "$CODEQL" database create "$WORK/db-$lang" --language="$lang" --build-mode="$mode" \
        --source-root "$SRC" --threads=0 --overwrite >"$OUT/codeql/$lang.create.log" 2>&1; then
    echo "   database create failed:"; tail -n 8 "$OUT/codeql/$lang.create.log" | sed 's/^/   /'; status=1; continue
  fi
  if ! "$CODEQL" database analyze "$WORK/db-$lang" "codeql/$pack-queries:codeql-suites/$pack-security-extended.qls" \
        --format=sarif-latest --output="$OUT/codeql/$lang.sarif" --threads=0 --sarif-add-snippets \
        >"$OUT/codeql/$lang.analyze.log" 2>&1; then
    echo "   analyze failed:"; tail -n 8 "$OUT/codeql/$lang.analyze.log" | sed 's/^/   /'; status=1; continue
  fi
  echo "   ok"
done
python3 - "$OUT" <<'PY'
import glob, json, sys
out = sys.argv[1]
merged = {"$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0", "runs": []}
for path in sorted(glob.glob(out + "/codeql/*.sarif")):
    runs = json.load(open(path)).get("runs") or []
    print(path.rsplit("/", 1)[-1], "results:", sum(len(r.get("results") or []) for r in runs))
    merged["runs"] += runs
json.dump(merged, open(out + "/results.sarif", "w"))
PY
rm -rf "$WORK"
exit $status
