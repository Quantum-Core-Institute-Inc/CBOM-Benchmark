# qci-pqc-scan on the CBOM Testbench: findings for the scanner team

Five reviews in this file, newest first: **v2.3.4** (2026-11-11), **v2.3.0**, **v2.2.0**, **v0.7.0**, and the
original **0.3.0** analysis, kept as the record of what was asked for. Run: `python tools/run_qci_pqc.py
--scanner <checkout>` with `CBOM_HOLDOUT_SEED` set, adapter 1.1, NIST policy, testbench v1.16 (304
findings; mixed files and calibration cases included); rescored on 1.17, see below.

## v2.3.4 review (testbench 2.1; numbers re-run on 2.2, see CHANGELOG)

### The short version

On everything the testbench measures, v2.3.4 is v2.3.0. Not close: identical, finding for finding.
Same 330 detection results, same parameters, same ticket-ready set, same single false positive, same
libraries, same holdout gap (-0.9, interval -5.9 to +4.0), same 4 of 8 verified migrations, same six
missed `createHash("sha1")` calls on the big tree in the same 119 seconds. It fails the same four
gates. Nothing regressed, and none of the open items moved.

That matches the release notes, which claim two fixes and nothing about detection. Both hold:

| Claim | Probe | v2.3.0 | v2.3.4 |
|---|---|---|---|
| A symlink is checked before it's read | a file and a directory symlinked to outside the scan root | follows the link and reports the outside file's MD5 as `link.py` | doesn't open it; "symlink leaves the tree" in `scan-coverage.json` |
| A corrupt JAR inside a valid WAR is recorded as skipped and fails the gate | a WAR holding one good and one corrupt JAR | exit 0, silent | exit 1, "corrupt nested archive", `partial: true` |

The new `scan-coverage.json` (files read, parsers, skipped, partial) is the right idea: it's the
scanner's own statement of what it didn't look at, which is what a declared scope should be built from.

### Small things in the new code

- **The skipped list repeats itself.** One symlink appears three times and the summary says
  "6 skipped" for 3 things. De-duplicate before counting.
- **A corrupt nested JAR marks the whole WAR.** The entry says `app.war: corrupt nested archive`
  and doesn't name the JAR. Name the inner path, so the person fixing it knows which one.
- **Certificate parsing still needs the `x509` extra, and a plain `pip install` doesn't say so.**
  Without `cryptography` installed, every certificate and key degrades to "Certificate present" with
  no algorithm: 16 findings on this corpus, recall 70.3% to 65.5% over everything. The scan exits 0
  and `scan-coverage.json` says `partial: false`. Either make `cryptography` a hard dependency or
  count it as a partial scan. (I hit this by installing without the extra; the testbench's own
  installer adds it, so published numbers were never affected.)

### Still open, unchanged from v2.3.0

1. The CBOM is invalid CycloneDX 1.6: `"version": null` on five library components.
2. Parameters missing where v2.2 reported them (56.8% vs 64.6%).
3. The leftover string filter that drops `createHash("sha1")`.
4. Wrapper-decided findings reported only at the wrapper (5 of 17 system findings misrouted).
5. No asset links. 6. DH matched in the bytes of a Go binary.

Evidence: `evidence/qci-v2.3.4/` and `evidence/perf-qci-v2.3.4/`. Everything below this section was
written against v2.3.0 and applies to v2.3.4 as it stands.

## Testbench 2.1: systems, fixes and big trees

What the new measurements say about v2.3, with where in the scorecards to look:

- **It routes wrapper-decided findings to the wrong team.** In the system fixture, 5 of its 17
  detected findings are found only through the shared wrapper or its config, so CODEOWNERS sends
  them to platform-security instead of the gateway, worker and ledger teams (routable 70.6%,
  `scorecard.md`, "System fixture"). The fix is call-site attribution: when a call passes a profile
  name to a wrapper whose algorithm comes from config, report the call site too.
- **It links nothing.** Neither the nginx config to the certificate it serves nor the certificate to
  its key (0 of 2 asset links). CycloneDX has the fields: `protocolProperties.cryptoRefArray`, and
  a `dependencies` entry for the key file.
- **One new false positive:** DH in the stripped Go gateway binary, matched in raw bytes. The Go
  FIPS module's internals (AES, SHA-2, SHA-3) are accepted there; DH isn't in it.
- **Fix and rescan: 4 of 8 eligible migrations verified.** Every miss is the same thing: the new
  algorithm is found but its parameters aren't (ML-DSA-65 in Python reported without a parameter
  set; AES-256-GCM in Go, JavaScript and C reported without a key size). It never kept reporting a
  retired algorithm, and nothing outside the migrated files moved. `evidence/qci-v2.3.4/remediation.md` (same result for v2.3.0).
- **Big trees: finishes 3,000 files in 120 s at 49 MB**, about 25 files a second, so a 100,000-file
  estate is about an hour. It missed 6 of 60 planted uses: every JavaScript `createHash("sha1")`,
  the leftover string filter again. No fall-off toward the end of the tree.
  `evidence/perf-qci-v2.3.4/manifest.json`.
- **Gates on 2.1** fail on the same four as before: parameters (56.8 vs 64.6), ticket-ready (47.6 vs
  54.9), deadline-weighted recall (75.0 vs 76.3), and the invalid CBOM.

## Testbench 1.17 rescore (all versions)

1.17 changed how the scorer counts, so every QCI release was rescanned and rescored on it. What
moved, and what didn't:

- **Occurrence-level false positives in mixed files.** A reported line more than 3 lines from every
  site of its family is now its own false positive, even when the file uses that family elsewhere.
  Import lines and a hash or MAC at another algorithm's site (HMAC at `pbkdf2_hmac`) are neutral.
  No QCI release loses precision to this: every unplaced QCI report was one of the neutral kinds.
  Grep picks up one (DES reported at a 3DES call).
- **PQC by standard name.** All three releases report every detected PQC finding as ML-KEM/ML-DSA or
  by OID, never Kyber or Dilithium: 100%.
- **Gates.** `gates.json` is now stamped for testbench 1.17 and enforced only on that stamp; a stale
  baseline exits 3, not 0. Each ratchet floor is the better of v2.2 and v2.3 on 1.17, so neither
  release passes outright: v2.3 fails parameters (57.1 vs 65.6), ticket-ready (48.6 vs 56.5),
  deadline-weighted recall (74.3 vs 75.7) and the schema limit; v2.2 fails recall, precision, PQC
  over-claims and libraries. The next release has to keep v2.3's precision and library gains and
  get v2.2's parameters back.
- **NIST policy.** TLS 1.0/1.1 and secp256k1 moved from not-approved to review (sources now cite
  section and revision), which nudges deadline-weighted recall up by under a point for everyone.

The v2.3 numbers below are unchanged on 1.17 except where noted above. Testbench 2.0 changed no scoring rule; every number is the same, now with an evidence bundle per release in `evidence/` (`python tools/bench.py verify evidence/qci-v2.3.4`).

## v2.3.0 review

### The short version

The release notes say source scanning is unchanged. It isn't, and the changes are the right ones:
the basename de-duplication is fixed, `resolve.py`'s test-case names are gone, two of the four
literal-text patterns are gone, the statement-shape filters are replaced by one rule about strings,
and parameters are read from the matched line instead of the whole file. Put that in the notes.

What it bought:

- **No false positives anywhere.** 0 on the corpus (v2.2: 19), 0 PQC over-claims (7), and 0.0 extra
  per file on fresh negative controls on all five seeds. The `negative_fp_gap` gate passes for the
  first time since v0.7.
- **Dependencies went from worst to best.** 25 of 26 crypto libraries in the right manifest (96.2%,
  v2.2: 30.8%; cdxgen: 76.9%), versions right on 87.5% of them, as proper CycloneDX `library`
  components with purls. Holdout manifests agree: 87.5 to 100%.
- **Recall held:** 74.2% in declared scope (v2.2: 73.9%), overfit gap -1.6 to +3.8 over five seeds,
  never significant.

What it cost, and why the gates fail:

1. **The CBOM is invalid again.** Four `library` components carry `"version": null` (libsodium and
   bcrypt among them, libraries whose manifest gives no version). CycloneDX wants the key left out. One
   line in the library writer.
2. **Parameters went from wrong to missing.** Findings with a wrong parameter fell from 26 to 15,
   which is the point. Findings with no parameter rose from 47 to 77, because "the matched line"
   is too narrow: `kpg.initialize(3072)` on the line after `getInstance("RSA")`, a curve in an
   `ECGenParameterSpec` two lines down, a string constant (`LEVEL = "ML-DSA-44"`, only integer
   constants are expanded), and Node findings attributed to the `require` line instead of the call.
   Parameter accuracy reads 57.1% (gate 65.6), ticket-ready 48.6% (56.5). Fifteen findings v2.2 got
   right now have no parameter; one got better. Read the statement and the variable the call uses,
   not the line and not the file.
3. **The old string filter is still there, under the new one.** The v2.2 block that drops any line
   with an algorithm name in quotes unless it matches `getInstance|hashlib|...` survived, minus its
   escape for assignments. With both, `createHash("sha1")` is dropped (no `createHash` in the old
   list), and so are names passed through a default argument, an environment default, an enum and
   a config map. Eight published findings v2.2 found are gone. Three went with the removed literal
   patterns, as they should; the other five (four SHA-1, one HMAC) are this filter, and they're why
   deadline-weighted recall fell to 73.7% (gate 75.0). The same block costs the holdout's PQC tier:
   75 to 92% on four seeds, every miss an ML-KEM or ML-DSA name passed through a helper or a config
   map. **Measured:** deleting those eight lines takes recall to 76.0% and holdout recall on seed
   1234 from 75.6% to 82.5% (five published findings back), at the price of two false positives. One is a string catalog key
   (`"sha1": "SHA-1 (deprecated)"`), because the new rule's "bare argument" escape doesn't check
   that the bare string is an argument to anything. Tighten that and drop the old block.
4. **Two literal-text patterns remain:** `["s", "ha", "1"]` and `map(chr, (65, 69, 83))`. The
   other two went, and with them `T2Enum` SHA-1 and `T5Reflection` MD5. Remove the last two.

### Where it stands (testbench v1.16, 304 findings, declared scope)

| | v2.2.0 | v2.3.0 |
|---|---|---|
| Recall | 73.9% | **74.2%** |
| Precision | 91.7% | **100%** |
| False positives / PQC over-claims | 19 / 7 | **0 / 0** |
| Parameters correct (of detected) | 65.6% | 57.1% |
| Wrong parameter reported | 26 | 15 |
| No parameter reported | 47 | 77 |
| Ticket-ready (of detected) | 56.5% | 48.6% |
| Deadline-weighted recall | 75.0% | 73.7% |
| CBOM validates (CycloneDX 1.6) | yes | **no** (`version: null`) |
| Crypto libraries in the right manifest | 30.8% | **96.2%** |
| Library versions correct | 0% | 87.5% |
| Library PQC verdicts | 5 of 7 right | none given |
| Mixed files: recall / parameters right | 49/62 / 20 | 50/62 / 18 |
| Calibration cases found | 81.6% | 80.3% |
| Overfit gap (5 seeds) | -3.1 to +3.4 | -1.6 to +3.8 |
| Negative-control gap (5 seeds) | +0.79 to +1.08 | **0.00 every seed** |

The ratchet gates in `gates.json` stay at v2.2's values: v2.3 fails `params_accuracy`,
`ticket_ready_pct`, `deadline_weighted_recall` and `cbom_schema_valid`. The first is partly the
ratio being crude (an honest blank scores like a wrong guess), but the other three are real.
Items 1 and 3 should clear the schema and deadline gates; with the old filter removed, deadline-
weighted recall measured 76.4%. Parameters need item 2: with item 3 alone they read 58.6%.

## v2.2.0 review

### The short version

v2.2 is the biggest real gain yet. In-scope recall went from 60.4% to **73.9%**, precision from
86.4% to 91.7%, PQC over-claims from 13 to 7, and false positives in the published negative files
from 4 to 0. JavaScript/TypeScript went from 22% to 72% recall and C from 41% to 62%. The CBOM
validates against CycloneDX 1.6 again. On five private holdout seeds the overfit gap is -3.1 to
+3.4 points, never significant: the gains carry over to code it hasn't seen. Your release notes'
numbers reproduce too: on the 221 findings outside the mixed files, 72.4% recall, 73.1% parameters,
zero false positives.

Three things are not real, and one of them still fails CI:

1. **Five Tier 5 and Tier 2 cases are answered by their literal text.** New patterns in
   `scanner.py` match the exact strings in the published files: `b64decode("bWQ1")` and `"TUQ1"`
   (base64 for "md5" and "MD5"), `["s", "ha", "1"]`, `map(chr, (65, 69, 83))`, and
   `LEGACY("SHA-1")` from `T2Enum.java`. They are worth 1.8 points of recall (73.9% to 72.1% with
   the four patterns removed, nothing else lost). They don't generalize: split the list as
   `["sh", "a", "1"]` or write the char codes as `(65, 69, 83 + 0)` and the finding is gone. The
   holdout has no Tier 5 generator, so the overfit gap can't see this; reading the diff did.
   `resolve.py` still carries the v0.7 test-case names (`AesCbcCipher`, `LegacyDesede`,
   `digest_factory`); they still add nothing.
2. **Negative-control suppression is still fitted to the published files.** Published negatives
   now have 0 false positives per file (v0.7: 0.4). Freshly generated ones still draw 0.8 to 1.1,
   the same as v0.7. The `negative_fp_gap` gate fails at +0.88. The new filters are statement
   shapes again: `log.warning(`, a line starting with `"key":`, `= ["` next to MD5 or SHA-1. A
   logger named `_LOG`, a C `const char *` or a Java `Map.of(` entry isn't one of them, and any
   assignment counts as a use, so `const char *note = "PBKDF2 iterations raised"` is a finding. All
   19 false positives on the corpus are names in strings in the mixed files.
3. **The same filters now cost real findings.** The `= {"` plus SHA-1 rule drops
   `= {"account", EVP_sha1}` (a mixed C file). The "a name in a string isn't a use unless the line
   is a call or an assignment" rule drops the SHA-1 entry `{"ledger", "SHA1"}` in
   `tier2/c/t2_digest_table.c`, and an algorithm name passed to a helper:
   `packShipment("ML-KEM-768")`. That's why holdout PQC reads 83-92% on three seeds where v0.7 read
   100%. A Go curve table (`tier2/go/curve_table`) is also lost; I didn't trace why. These three are
   the only published findings v0.7 found and v2.2 doesn't.

### Where it stands (testbench v1.16, 304 findings)

| | v0.7.0 | v2.2.0 |
|---|---|---|
| Recall, declared scope | 60.4% | **73.9%** |
| Parameters correct (of detected) | 67.3% | 65.6% |
| Parameters correct (count) | 115 | 137 |
| Precision | 86.4% | 91.7% |
| False positives in published negatives | 4 | 0 |
| PQC over-claims | 13 | 7 |
| Ticket-ready (of detected) | 56.1% | 56.5% |
| CBOM validates (CycloneDX 1.6) | no | **yes** |
| Mixed files: recall / parameters right | 39/62 / 15 | 49/62 / 20 |
| Calibration cases (no scanner had seen them) | 64.1% | 81.6% |
| Matched holdout recall (5 seeds) | 64-75% | 79-83% |
| Overfit gap (5 seeds) | -2.1 to -0.4 | -3.1 to +3.4 |
| Negative controls: published / unseen, FPs per file | 0.40 / 1.1-1.6 | **0.00 / 0.8-1.1** |
| Crypto libraries in the right manifest | 26.9% | 30.8% |

Parameter accuracy went *down* as a ratio and up as a count. No finding v0.7 got right is wrong
in v2.2; the 38 new detections, mostly JavaScript and C, come with parameters less often. The old
ratchet failed v2.2 on that ratio, which is the ratchet being crude, not the scanner regressing.
`gates.json` is rebaselined on v2.2; only `negative_fp_gap` fails now.

### Still open from v0.7

| Item | v2.2 |
|---|---|
| CBOM schema (`notValidAfter` date-time) | fixed |
| `dedupe.py` keys on the basename (2b below) | **not fixed**. Measured on v2.2 with only that line changed: recall 73.9% to 76.0%, Go Tier 1 8 to 14 of 20 |
| HMAC/PBKDF2 hash and AES/RSA/EC/DH size taken from anywhere in the file (2c) | **not fixed**: the same mixed-file errors, HMAC-SHA512 still reported SHA-256 |
| Names in strings reported as findings (2, 2c) | narrower, still shape-based; see above |
| Hardcoded test-case names in `resolve.py` (1) | still there |
| JavaScript `crypto.` prefix | fixed: JavaScript/TypeScript 22% to 72% |
| Dependency versions | still none recorded (0 of 8 found) |

The two oldest bugs on this list are the two cheapest to fix. `_normalize_path` should return the
path (2.1 points of recall on its own, measured), and the parameter block should read the matched
call instead of the file. Together they are
worth more than anything in 2.2's feature list for a real repository with more than one service.

## v0.7.0 review

### The short version

v0.7 is a large, mostly real improvement. In-scope recall went from 24.9% to **59.7%**, parameters
from 40% to 76%, ticket-ready detections from 31% to 61%, post-quantum assets from 1 of 20 to 19 of
20. Private holdout sets of new code in all six corpus languages, Tiers 1-3 and PQC, confirm the work
carries over: an overfit gap between -2.1 and -0.4 points across five seeds (v1.16, mixed files
included), never significant.

One regression to fix first: **v0.7's CBOM no longer validates against CycloneDX 1.6.** 0.3.0's did.
The new `certificateProperties.notValidAfter` is written as a date (`"2027-02-02"`); the schema
requires a date-time (`"2027-02-02T00:00:00Z"`). Strict consumers will reject the whole file. Only
2 of 23 certificates carry these properties yet, so it's a one-line fix in `report.py` now and a
much louder problem later.

Two things are not real, and one of them fails CI:

1. **False-positive suppression was fitted to the published negative files.** On the seven published
   Python/Java negatives, v0.7 has zero false positives (0.3.0 had 3); across all published negatives
   it's 0.4 per file. On 24 freshly generated negatives in six languages it has **1.1 to 1.6 per file**
   (0.3.0: 0.3 to 0.8, the same as its published rate). It got better on the files it had seen and
   worse on files it hadn't. The `negative_fp_gap` gate fails at +0.7 to +1.2 against a limit of 0.5.
2. **`resolve.py` hardcodes the names of published test cases.** See below. It contributes nothing to
   the score, but it has to go.

And one bug the extended holdout found that isn't fitting at all: **`dedupe.py` keys findings on the
file's basename**, so the same algorithm near the same line in `svc-a/main.go` and `svc-b/main.go` is
reported once. Every Go program is a `main.go`; so is every `index.js`, `__init__.py` and
`pom.xml` collision in a monorepo. Five copies of the published ML-KEM program in five directories
produce one finding. Changing `_normalize_path` to keep the path raises published recall from 59.7%
to 61.5% and matched holdout recall on seed 4242 from 59.9% to 67.6%. Details in section 2b.

Testbench v1.15 added realistic-size mixed files (section 2c), and they show what the small test
files hid: **parameters are guessed file-wide, and algorithm names in log text are reported as
findings.** On 15 mixed files v0.7 gets parameters right for 38% of what it detects (76% elsewhere)
and adds 23 false positives, 11 of them PQC over-claims. Overall precision on v1.15 is 86.6%.

### Where it stands (testbench v1.14, 242 findings)

| | 0.3.0 | v0.7.0 |
|---|---|---|
| Recall, declared scope | 24.9% | **59.7%** |
| At primary site | 24.0% | 57.0% |
| Parameters correct | 40.0% | 75.8% |
| Precision | 85.9% | 97.1% |
| PQC over-claims (published) | 7 | 2 |
| Ticket-ready (of detected) | 30.9% | 61.4% |
| Deadline-weighted recall | 25.2% | 57.9% |
| Matched holdout recall (5 seeds, six languages) | 27-30% | 60-71% |
| Overfit gap, recall (5 seeds; v1.16) | -4.3 to -0.5 | -2.1 to -0.4 |
| Negative controls: published / unseen, FPs per file (v1.16) | 0.60 / 0.33-0.75 | **0.40 / 1.12-1.58** |
| Crypto libraries in the right manifest | 26.9% | 26.9% |

Your gates file (recall 70.9, precision 100, zero false positives) was measured on testbench v1.8, before
Go, JavaScript/TypeScript, C and the dependency manifests were added. On the same 141 findings v0.7
scores 74.5% recall and 100% precision here, so the numbers hold up for that corpus. On v1.12 they
don't apply; the gates in `gates.json` are now rebaselined on v0.7 with a corpus stamp.

| Bucket | v0.7 recall | Note |
|---|---|---|
| Tier 1 Python / Java | 15/16, 15/16 | was 6/16, 10/16 |
| Tier 2 Python / Java | 7/9, 6/8 | |
| Tier 3 Python / Java | 8/9, 6/7 | at primary site 5/9, 5/7 |
| Tier 4 assets | 19/34 | was 7/34 |
| PQC assets | 19/20 | was 1/20 |
| Tier 1 JavaScript | 3/17 | JavaScript patterns unchanged from 0.3.0; these 3 come from the new bare-word patterns |
| Tier 1 Go / C | 5/20, 9/20 | |
| Tier 5 | 0/12 | unchanged |

On testbench v1.15 (304 findings, mixed files added), declared scope:

| | 0.3.0 | v0.7.0 |
|---|---|---|
| Recall | 24.0% | 60.4% |
| Parameters correct | 38.2% | 67.3% |
| Precision | 74.7% | 86.4% |
| PQC over-claims | 20 | 13 |
| Ticket-ready (of detected) | 30.9% | 56.1% |
| Mixed files: recall / params correct | 13/62 / 4 of 13 | 39/62 / 15 of 39 |

`gates.json` is rebaselined on v1.16 (stamp: 608 answer-key entries, 304 of them calibration; the values match v1.15). The ratchets moved down with the corpus,
not because v0.7 got worse: the same scanner scores lower on harder files.

### 1. Hardcoded test-case names (remove)

`resolve.py`, `resolve_wiring()`:

```python
interesting = ("hashlib.new", "AesCbcCipher", "LegacyDesede", "digest_factory", "forProfile")
...
if "AesCbcCipher" in line:            # -> AES-CBC
if "LegacyDesede" in line or ...:     # -> 3DES
if "hashlib.new" in low and "md5" in text.lower():   # -> MD5, anywhere in the file
```

`AesCbcCipher` and `LegacyDesedeCipher` are classes in the testbench's Tier 3 `strategy_factory`
project; `digest_factory` and `forProfile` are identifiers from its `dependency_injection` project and
Tier 2 cases. No customer codebase will contain them; any that does gets a finding from a class name.
The MD5 rule fires on any file that calls `hashlib.new` and mentions "md5" anywhere, with nothing
connecting the two.

Measured by switching it off: **`resolve_wiring` adds zero detections**, and parameters and precision
don't change, because other patterns already find the same algorithms in those files. So it doesn't
inflate the score. It's a credibility problem: anyone reading the source will draw the obvious
conclusion. Delete the function. The rest of the resolver (config files, `.properties`, system-property
defaults, call arguments) earns 7 real findings and should stay.

`tests/fixtures/java_aes/T1AesEcb.java` and `T1AesGcm.java` are byte-for-byte copies of corpus files.
Regression tests on known cases are fine; consider writing your own variants so the test suite and
the benchmark stop being the same thing.

### 2. Negative controls: fitted, not fixed

The new filters skip `log.info/warning/debug` lines, lines that *start* a docstring, "string
catalogs", and `.md` files. Those are the shapes in the published negatives. An algorithm name in a
plain string constant (`NOTE = "PBKDF2 iterations raised"`) or a returned value still matches, and
the new bare-word patterns make it worse: `HMAC\b`, `PBKDF2`, `\bDSA\b`, `\bDH\b`, `SHA1\b` match
the word wherever it appears. On the holdout negatives the top false positives are HMAC (14), ML-KEM
(14), PBKDF2 (12) and ML-DSA (9) across five seeds.

The same filter costs real findings. `tier2/python/t2_dispatch_table.py` stores hash constructors
in a dict, `"legacy": hashlib.md5`, and calls them at runtime. 0.3.0 found both; v0.7 finds neither,
because the "string catalog" rule skips any `"key": value` line. These are the only two findings
0.3.0 detects and v0.7 doesn't.

**Fix:** require an API context for the bare-word patterns, as the 0.3.0 patterns did
(`Mac.getInstance("Hmac`, `hmac.new(`, `PBKDF2HMAC(`), and suppress algorithm names inside string
literals generally rather than in specific statement shapes. The published C and JavaScript negatives
(4 false positives, 2 PQC over-claims) fail for the same reason.

### 2b. De-duplication collapses findings across files

`dedupe.py`:

```python
def _normalize_path(path: str) -> str:
    """Use basename so different scanners' path prefixes still match."""
    p = path.replace("\\", "/").rstrip("/")
    return p.split("/")[-1] if p else ""
```

The key is (family, basename, line bucket of 7). Two `main.go` files that generate RSA keys on lines
8 and 10 become one finding, and the CBOM loses the other file entirely. The docstring says why:
merging output from several scanners with different path prefixes. Strip the common prefix instead,
or dedupe on the path relative to the scan root, and keep the directories.

Measured with only that line changed (return the full path), seed 4242:

| | v0.7 | v0.7, dedupe fixed |
|---|---|---|
| Recall, declared scope | 59.7% | 61.5% |
| Matched holdout recall | 59.9% | 67.6% |
| Holdout PQC tier | 92.9% | 100% |
| False positives (published) | 4 | 5 |

The extra false positive was being hidden by the same collision. On a real repository with dozens of
services this is the biggest single recall fix available.

It also makes the score depend on what else is in the scan. Testbench v1.16's first calibration set
named its generated Go programs `main.go`. Adding them cost v0.7 three findings in the *hand-written*
corpus (`tier1/go/hashes` SHA-1, `tier1/go/mac_kdf` PBKDF2, a mixed-file PBKDF2), files that hadn't
changed. A 360-file holdout full of `main.go` read as a significant overfit gap (+4.1, interval
+0.1 to +8.1) that was entirely this bug: with the fix it read -0.1. The testbench now gives
generated Go files unique names so the gap measures fitting, not this; the bug is still yours.

v1.16 also adds 304 generated Tier 1-2 calibration cases no scanner had seen. v0.7 detects 64.1% of
them against 59.2% of the hand-written cases in the same cells, so the Tier 1-2 gains aren't tuned to
the published files.

### 2c. Mixed files: the guesses show up

The corpus's code cases are small files with one or two uses each, and section 3 below says
v0.7's parameter extraction only works there. Testbench v1.15 measures it: `corpus/mixed/` has 15
modules of 220 to 520 lines, three to five crypto sites each, usually one algorithm twice with
different parameters, plus ordinary code and log messages naming algorithms the file doesn't use.
Sites are scored separately (a report counts for the nearest site within 3 lines).

| | Rest of corpus | Mixed files |
|---|---|---|
| Recall | 56.2% | 62.9% (39/62) |
| Parameters correct (of detected) | 75.7% | **38.5%** (15/39) |
| False positives | 4 | **23** in 15 files |
| PQC over-claims | 2 | 11 |

Recall holds up. Parameters and precision don't.

**Parameters.** `scanner.py`, the parameter block after each pattern match:

```python
if family in {"HMAC", "PBKDF2"} and re.search(r"sha256|SHA256", text, re.I):
    param = "SHA-256"
```

`text` is the whole file. One `sha256` anywhere makes every HMAC and PBKDF2 in the file SHA-256.
Seven of the 24 parameter misses are exactly that: HMAC-SHA512, PBKDF2-SHA512 and PBKDF2-SHA1
reported as SHA-256. The AES size and mode, the RSA/DH `initialize(` size and `KEY_BITS` work the
same way, first match in the file, which is how P-256 becomes P-521 and DH-2048 becomes DH-3072
when both are in one module. Another eleven misses report no parameter at all (mostly Go RSA and
HMAC, C HMAC and DH), which is at least honest.

**False positives.** All 23 are names in strings: `log.warning("ML-KEM-768 rollout approved for all
tenants (%d pending)")`, `"summary": "PBKDF2 iterations raised"`, a C `const char *` holding "DH
group 14 disabled on the bastion". The published negatives taught the scanner to skip a few statement
shapes (section 2); a log call with a format argument, a dictionary value or a C string isn't one of
them. Eleven of the 23 claim post-quantum crypto that isn't there, which in a migration tracker
marks work as done.

**Fix:** take parameters from the matched call, or the constant or argument it references, and leave
them empty otherwise; drop algorithm names that sit inside string literals unless the literal is an
argument to a crypto API (`getInstance("...")`, `createHash("...")`, `EVP_get_digestbyname("...")`).
Both fixes make the small files no worse and the mixed files much better. The holdout's mixed files
agree with the published ones: 19 to 36% of v0.7's detections there have the right parameters, so
this isn't a quirk of 15 files.

### 3. Guesses presented as findings

- **File-wide parameters.** For AES, the first `bit_length=`, `.init(N)`, `getInteger(.., N)` or
  `urandom(N)` *anywhere in the file* becomes every AES call's key size, and `modes.ECB` anywhere
  makes every AES call ECB. Same for curves. It works on one-algorithm test files; real files mix.
  Parameter accuracy on the broad holdout (mixed APIs) is 53%, against 76% on the corpus.
- **`algorithms.AES` is reported as `AES-GCM`** whatever the mode argument says.
- **JWKS keys:** `alg: RS256` sets the RSA key size to 2048. RS256 says nothing about key size.
- **`.properties`:** any key containing "size" sets the size for every algorithm in the file.

**Fix:** take parameters from the call (or the constant it references), and report none rather than
guess. A missing parameter is honest; a wrong one ends up in a migration plan.

### 4. Still open from the 0.3.0 review

| Item | v0.7 |
|---|---|
| Version string | fixed (0.7.0) |
| DES matched on DESede | fixed |
| Duplicate certificate findings | fixed |
| Algorithm OIDs | RSA, EC, Ed25519 now correct; ML-KEM/ML-DSA still arc prefixes in about half |
| `nistQuantumSecurityLevel` | 1/3/5 for PQC now; classical algorithms still get none instead of 0 |
| `certificateProperties` (expiry, subject, issuer) | 2 of 23 certificates, and `notValidAfter` breaks schema validation (date, not date-time) |
| Key material type (`relatedCryptoMaterialProperties.type`) | 0 of 48 |
| TLS protocol versions as protocol assets | 0 of 6 |
| JavaScript `crypto.` prefix | not fixed: the eight JavaScript patterns are identical to 0.3.0 |
| Dependencies (section 1c): versions, Conan/CMake, npm, lockfiles, PQC thresholds | untouched; `deps.py` is unchanged, both wrong PQC verdicts remain |

---

# 0.3.0 review (original)

## Where it stands

| | In declared scope | Everything |
|---|---|---|
| Recall (strict, named algorithm) | 24.9% (55/221) | 22.7% |
| Recall counting QCI risk-category signals | 35.3% (78/221) | |
| Precision | 85.9% | 85.9% |
| False positives | 9 (7 in negative controls) | |
| PQC over-claims | 7 | |
| Ticket-ready detections | 30.9% | |
| Deadline-weighted recall (NIST) | 25.2% | 23.3% |

Testbench v1.10 added Go, JavaScript/TypeScript and C/OpenSSL (80 findings). Python and Java numbers
are unchanged from the first run; the totals fell because the scanner finds 12 of the 80 new ones.
Section 1b covers them.

"Declared scope" applies `docs/LIMITATIONS.md`: JARs, `.pyc`, DER/PKCS#12/JKS and certificate
signature algorithms are listed but not counted (21 findings). Nothing out of scope was detected.

The CBOM itself validates against CycloneDX 1.6. That's the good news, and it's real: plenty of tools
can't say that.

The short version of the rest: the scanner finds the textbook calls it has a regex for, then stops.
The pattern catalogue is narrow, a third of what it does find is reported as a category instead of an
algorithm, and the CBOM drops facts the scanner already has in hand. Most of the fixes are small.

## 1. Detection gaps (recall)

Tier 1 is "direct, idiomatic API calls". Recall there is 50%. Every one of these misses is a line a
reviewer would call obvious:

| Missed | Example line | Why |
|---|---|---|
| AES-ECB via PyCA | `Cipher(algorithms.AES(key), modes.ECB())` | `scanner.py` only matches PyCryptodome `AES.new(..., MODE_ECB)` |
| AES-GCM via PyCA | `AESGCM(AESGCM.generate_key(...))` | no `AESGCM` pattern |
| 3DES via PyCA | `Cipher(TripleDES(key), ...)` | no `TripleDES` pattern |
| Ed25519 / X25519 | `Ed25519PrivateKey.generate()` after `from ... import` | patterns require the `ed25519.` module prefix |
| DSA | `dsa.generate_private_key`, `KeyPairGenerator.getInstance("DSA")` | no DSA patterns at all |
| DH | `dh.generate_parameters`, `KeyPairGenerator.getInstance("DH")` | only the `DH/ECDH` category |
| X25519 (Java) | `KeyPairGenerator.getInstance("X25519")` | no pattern |
| HMAC, PBKDF2 | `hmac.new`, `Mac.getInstance`, `PBKDF2HMAC`, `SecretKeyFactory` | not in the catalogue |
| SHA3-256 | `hashlib.sha3_256`, `MessageDigest.getInstance("SHA3-256")` | not in the catalogue |

**Fix:** match class and function names without the module prefix (`\bEd25519PrivateKey\b`,
`\bAESGCM\b`, `\bTripleDES\b`, `algorithms\.AES\b` plus a `modes\.(ECB|CBC|GCM|CTR)` follow-up on the
same line), and add DSA, DH, HMAC, PBKDF2, SHA-3 and Java `X25519`/`XDH` to `PATTERNS`. That's
roughly fifteen regexes, and the 16 Tier 1 misses above are all within reach of them.

Tiers 2 and 3 (indirection: constants, config, wrappers, enums) are at 12–44%. Regex can't follow
`KeyPairGenerator.getInstance(KEY_ALG)` to `KEY_ALG = "DSA"`, so this needs at least file-local
constant propagation. Worth doing for string constants in the same file before anything fancier; it's
the commonest real-world case.

Tier 5 hand-rolled source (TEA, S-box tables, SHA-256 round constants) is 0/12. Constant signatures
are cheap to add later; not the first priority.

## 1b. Go, JavaScript/TypeScript, C/OpenSSL (12 of 80)

| | Tier 1 | Tier 2 |
|---|---|---|
| Go | 2/20 | 3/6 |
| JavaScript / TypeScript | 0/17 | 0/7 |
| C / OpenSSL | 6/20 | 0/6 |

Go's Tier 2 beats its Tier 1, which tells you what's going on: it's not the indirection, it's the
catalogue. Most Go Tier 2 cases still call `rsa.GenerateKey` or `aes.NewCipher` in plain sight, and those
are two of the seven Go patterns there are.

**JavaScript: every pattern requires `crypto.` in front.** `scanner.py` matches `crypto\.createHash`,
but current Node code destructures: `const { createHash } = require("node:crypto")`, then
`createHash("md5")`. The same applies to ESM imports and TypeScript. This is the module-prefix problem
from section 1 again, and it zeroes a whole language. Beyond that, there are no patterns for
`createCipheriv` (the cipher name is right there: `"aes-128-cbc"`, `"des-ede3-cbc"`,
`"chacha20-poly1305"`), `generateKeyPairSync("rsa" | "ec" | "ed25519" | "x25519")`, `createHmac`,
`pbkdf2Sync` or `getDiffieHellman("modp14")`. The Web Crypto pattern wants `{ name: "RSA-` on the same
line as `subtle.generateKey(`, and formatted code puts it on the next.

**Go: one-shot calls and half the standard library are missing.** `md5.New` is matched, `md5.Sum` (the
commoner call) isn't. Nothing for `crypto/des`, `crypto/rc4`, `crypto/dsa`, `crypto/ecdh` (X25519),
`crypto/hmac`, `crypto/pbkdf2`, `crypto/sha3` or `tls.Config` (`MinVersion: tls.VersionTLS10`,
`CipherSuites`, `CurvePreferences`). ML-KEM is found in `crypto/mlkem`, but without the parameter set,
which is in the function name: `mlkem.GenerateKey1024()`.

**C: the EVP constructors are the API; match them all.** `EVP_md5()` and `EVP_sha1()` are found,
`EVP_sha256()` isn't. Nothing for `EVP_des_ede3_*`, `EVP_aes_*_ecb`, `EVP_chacha20_poly1305`,
`EVP_sha3_*`, `EVP_PKEY_X25519`, `"ED25519"`, `"DH"`/`ffdhe*`, `HMAC(`, `PKCS5_PBKDF2_HMAC`, or
`SSL_CTX_set_min_proto_version` / `SSL_CTX_set_cipher_list`. One regex, `EVP_(aes|aria|camellia|des|
chacha20|sm4)_[a-z0-9_]+`, plus the name normalizer this testbench already has, would cover most of the
cipher side: the constructor name carries algorithm, key size and mode.

New false positives from the new negative controls, same cause as section 4: algorithm names in a C
string table (`"EVP_md5 no longer linked"`, `"ML-KEM rollout approved"`) and in a JavaScript array of
display labels (`"ML-KEM-768"`). Two more PQC over-claims.

## 1c. Dependencies (7 of 26 crypto libraries)

`deps.py` knows seven libraries and twelve manifest names. What that leaves out, on the testbench's
seven applications:

- **No versions in the CBOM.** The regexes capture a version for cryptography and OpenSSL (not
  Bouncy Castle: its pattern has no version group), then don't write it: library components have no
  `version` and no purl. Version accuracy is
  0% of found. "Which version?" is the question an inventory exists to answer.
- **Manifests it never opens:** `conanfile.txt`, `CMakeLists.txt`, `vcpkg.json`. OpenSSL 1.1.1w, end
  of life since 2023-09-11, goes unreported.
- **Libraries it doesn't know:** everything on npm (jsonwebtoken, crypto-js, node-forge, bcryptjs,
  @noble/post-quantum), PyCryptodome, PyJWT, Paramiko, bcrypt, Nimbus JOSE+JWT, JJWT,
  golang.org/x/crypto, golang-jwt, libsodium. crypto-js upstream says "Active development of CryptoJS
  has been discontinued."
- **No transitive dependencies.** `package-lock.json` is on the list, but only the Node.js runtime
  pattern fires there; `jws`, `jwa`, `@noble/curves` and `@noble/hashes` aren't reported.
- **Two wrong post-quantum verdicts** out of six:
  - `cryptography>=48,<51` is reported quantum-vulnerable with the note "No native ML-KEM/ML-DSA
    yet." The pyca changelog says 48.0.0 (2026-05-04) added ML-KEM and ML-DSA with OpenSSL 3.5,
    available in the wheels. The note needs a version threshold, like Bouncy Castle's.
  - Bouncy Castle **1.80** in `build.gradle` is reported vulnerable. The pattern `bouncycastle` has
    no version group, so Gradle's `org.bouncycastle:bcprov-jdk18on:1.80` never reaches the threshold
    check. The threshold is also one release early: 1.78 implemented the FIPS 203 *draft*; the
    finalized ML-KEM, ML-DSA and SLH-DSA arrived in 1.79.

What's right: CIRCL and liboqs are correctly called post-quantum, Bouncy Castle 1.70 correctly
called vulnerable, and nothing was reported from the commented-out `pycrypto` line or the XML
comment hiding Jasypt.

**Fix:** emit `version` and a purl on every library component; add Conan/CMake/vcpkg; add the npm
crypto packages; read lockfiles for transitive entries; give every library a PQC threshold version
(cryptography 48.0.0, Bouncy Castle 1.79, CIRCL 1.4.0 for ML-KEM / 1.5.0 for ML-DSA, OpenSSL 3.5).

## 2. Post-quantum assets (pqc/assets: 1 of 20)

The scanner reports its own subject area worst.

- **ML-DSA certificates become `X509-Cert` / `UNKNOWN`.** `certs.py:_from_cert` handles RSA, EC and
  Ed25519 and drops everything else into the `else:` branch. `cryptography` parses ML-DSA public
  keys in the 50.x line this testbench was built with (`cryptography.hazmat.primitives.asymmetric.mldsa`); add the `isinstance` branch, and for
  anything still unknown read `cert.public_key_algorithm_oid` and map the NIST OIDs
  (`2.16.840.1.101.3.4.3.17/18/19` for ML-DSA-44/65/87) instead of giving up. DSA and Ed448 certs hit
  the same branch.
- **PQC keys in PKCS#8 PEM are invisible.** `-----BEGIN PRIVATE KEY-----` is reported as `PKCS8`, and
  `PUBLIC KEY` not at all. Load the key and read its type (or its algorithm OID).
- **Hybrid groups in nginx, OpenSSL and sshd configs are categories only** (`Hybrid-KEM`,
  `SSH-PQC-Kex`). The config line names the exact group: `X25519MLKEM768`, `SecP384r1MLKEM1024`,
  `mlkem768x25519-sha256`, `sntrup761x25519-sha512@openssh.com`. Report the name.
- **TLS protocol versions and cipher suites in configs** (`ssl_protocols`, `MinProtocol`,
  `ssl_ciphers`) are categories or nothing. These are the CBOM `protocol` asset type.

## 3. Categories instead of algorithms

46 of the scanner's findings are risk categories: `DH/ECDH`, `RSA/ECDSA`, `SSH-Weak-Cipher`,
`TLS-Classical-Cipher`, `Hybrid-KEM`. They're useful on a dashboard. In a CBOM they're a problem:

- `name` and `parameterSetIdentifier` are both set to the category, so `DH/ECDH` reads as "ECDH" to
  any downstream tool that normalizes names. The testbench adapter has to hide these to avoid scoring
  them as wrong algorithms (`tools/adapters/qci_pqc.py`).
- A migration ticket can't be written from "SSH-Weak-Cipher". It can from `aes128-cbc`.

The testbench credits them separately as signal coverage (23 extra findings), so they aren't
wasted. **Fix:** emit one algorithm component per name actually on the line, and carry the category as
a property (`qci:riskCategory`) rather than as the component name.

## 4. False positives and PQC over-claims

All six false positives are real:

| Where | What | Cause |
|---|---|---|
| `LegacyDesedeCipher.java:17` | `DES` on `Cipher.getInstance("DESede/...")` | `scanner.py:37` regex `"DES` also matches `"DESede`. Use `"DES(?!ede)` or `"DES["/]`. Both `DES` and `3DES` are reported for that line now. |
| `negatives/python/n_strings_and_comments.py` | ML-KEM, ML-DSA | algorithm names inside string literals and log messages |
| `negatives/java/NStringsAndComments.java:16` | ML-KEM | same |
| `negatives/assets/cert-rotation-runbook.md:5` | ML-DSA | Markdown prose |
| `pqc/python/pq_washing.py:1` | ML-KEM-768 | docstring *claims* ML-KEM; the code generates a classical EC key. This is the PQ-washing case. |

The PQC ones are the costly kind: they tell a compliance reader a system is quantum-safe when it
isn't. Five over-claims across four files. **Fix:** the comment filter in `scanner.py` (around line
175) only skips lines that *start* with a comment marker, and only skips quoted lines containing words
like "example". Two cheaper wins: don't scan `.md`/`.txt`/`.rst` with code patterns, and for PQC
names require an API context (`KeyPairGenerator`, `mlkem.`, `oqs.`, `EVP_PKEY`) rather than the bare
name, which is how the classical patterns already work.

## 5. The CBOM drops what the scanner already knows (actionability)

Only 32.6% of detections carry enough to act on. Most of the gap is data the scanner computes and
then doesn't write:

- **Certificate expiry and subject: 0 of 6.** `certs.py:_from_cert` reads `not_valid_after_utc` and
  `subject` and puts them in `notes`. `report.py` doesn't write `certificateProperties`
  (`subjectName`, `issuerName`, `notValidBefore`, `notValidAfter`, `subjectPublicKeyRef`,
  `signatureAlgorithmRef`). Expiry is the single most-requested field in a cert inventory.
- **Key size and curve.** Present in `notes` (`RSA-2048 certificate`, `ECDSA (secp256r1)`), absent
  from `parameterSetIdentifier`/`curve`. Parameters are correct on 20% of the findings where they
  apply.
- **RSA vs EC primitive: 0 of 18.** Every algorithm component has `primitive: other` or a guess
  derived from role. `RSA` used for `Cipher.getInstance("RSA/...")` is `pke`; `SHA256withRSA` is
  `signature`.
- **Key material type: 0 of 1.** `related-crypto-material` components have no
  `relatedCryptoMaterialProperties.type` (`private-key`, `public-key`).
- **OIDs: 0 of 43.** `report.py:71` emits arc prefixes (`2.16.840.1.101.3.4.4`) instead of algorithm
  OIDs (`2.16.840.1.101.3.4.4.2` for ML-KEM-768). The block also assigns `crypto["oid"]` twice.
- **Quantum security level: 0 of 43.** `report.py:63` sets it only for PQC and only to 3 or nothing.
  CycloneDX expects 0 for quantum-vulnerable algorithms, and the PQC levels are 1/3/5 for ML-KEM-
  512/768/1024 and 2/3/5 for ML-DSA-44/65/87.
- **Certificates in a bundle collide.** `_from_cert` builds `id=f"CERT-{rel}"` and
  `evidence_line=1` for every cert in the file, so a three-cert chain becomes three findings with the
  same ID on line 1.

What already works: location is right 93% of the time, and `cryptoFunctions` is always present.

## 6. Smaller things

- `report.py:128`, `:162` and `:355` say the tool is version `0.1.0`. The package is 0.3.0.
- `certs.py:_basic_cert` says "cryptography library not available" when the library *is* available
  and the parse failed. That sends people to reinstall a working dependency.
- PEM certificates produce two findings each: one from the `BEGIN CERTIFICATE` pattern in
  `scanner.py:121` and one from `certs.py`. Deduplicate on (file, family).
- `calibrate.py` hardcodes 32 expected pairs and computes precision over distinct detected pairs, so
  repeated false positives count once. This testbench is a drop-in replacement for it.
- `docs/LIMITATIONS.md` says key size from certificates is out of scope, but `certs.py` reports it.
  The testbench scores it, since it's there.
- `findings.json` has fewer fields than `cbom.json`. Customers will read the JSON first.

## Suggested order

1. DES regex, version string, misleading parse message, duplicate cert findings. An hour, no risk.
2. Write `certificateProperties` and key size/curve from data already parsed. Biggest actionability
   gain for the least code.
3. Tier 1 pattern additions (sections 1 and 1b). Biggest recall gain. For JavaScript, dropping the
   `crypto.` prefix requirement is a one-line change per pattern and takes it off zero.
4. ML-DSA certs, PKCS#8 PQC keys, named hybrid groups. This is the scanner's headline claim, and
   currently 1 of 20.
5. PQC names need API context; skip prose files. Removes all five over-claims.
6. Categories become properties; algorithms become components.

After each, raise the matching number in `gates.json` so it stays fixed.

One more thing the CI job checks once `CBOM_HOLDOUT_SEED` is set: a private holdout set of new code
using the same APIs as the published cases. Fixes that generalize (match `Ed25519PrivateKey`
without the module prefix) raise both scores. Fixes aimed at the specific lines in this report raise
only the published one, and the overfit gate fails. 0.3.0's gap is about zero; see `HOLDOUT.md`.
