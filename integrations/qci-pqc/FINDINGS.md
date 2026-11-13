# qci-pqc-scan v2.3.4.3 on the QCI CBOM Benchmark: findings for the scanner team

Scanner: `qci-pqc-scan` 2.3.4.3, internal adapter, run in the sandbox and in its own container.
Benchmark 2.6.5 (410 findings, methodology 2.3, NIST policy), declared scope from
`integrations/qci-pqc/scope.json`, holdout generator 1.4. Reproduce with `tools/release_run.sh`.
Evidence: `evidence/qci-v2.3.4.3/`, `evidence/qci-v2.3.4.3-container/` and
`evidence/perf-qci-v2.3.4.3/`; the numbers below are in `reports/qci-pqc/SUMMARY.md`.

## The short version

| | v2.3.4.1 on 2.6.4 | v2.3.4.3 on 2.6.5 |
|---|---|---|
| Recall, everything | 61.0% | 62.2% |
| Recall, declared scope | 64.2% | 65.5% |
| Parameters correct (of detected) | 54.4% | 90.2% |
| Precision | 99.6% (1 false positive) | 100% (none) |
| Ticket-ready (of detected) | 45.2% | 80.0% |
| Actionable recall | 27.6% | 49.8% |
| Config findings complete (of found) | 20 of 24 | 24 of 24 |
| Crypto libraries in the right manifest | 96.4% | 96.4% |
| Overfit gap | -0.8 (-5.7 to +4.2) | -0.8 (-5.6 to +4.2) |
| Negative-control gap | 0.0 per file | 0.0 per file |

Parameters were the gap and are mostly closed. The scanner now reads the whole statement, follows
names a file defines once, and follows the object a call creates. Of 255 detections, 230 carry the
right parameters, 25 carry none, and none carries a wrong one. The gain holds on code the scanner
has not seen: on a public-seed holdout set, parameters went from 47.4% to 88.1% with recall and false
positives unchanged.

Recall moved by five findings. Three are RC4, and those are the benchmark's correction, not the
scanner's: the adapter's name table lacked `RC4`, so detections the scanner had always made were
scored as misses (adapter 1.2 fixes it). Two are the scanner's: SHA-512 in C# (`SHA512.Create` was
reported as SHA-256, the one false positive on 2.6.4) and HMAC in the system fixture.

The gate floors were reset to v2.3.4.3's own numbers on this release, so it passes every gate by
construction. The floors now protect 90.8% on parameters and 100% precision.

## 1. Binaries are skipped, and now the scanner says so

2.3.4.1 skipped any file with a NUL byte in its first 1,024 bytes and recorded nothing. 2.3.4.3
still skips them, but `scan-coverage.json` lists each one (eight on this corpus), marks the scan
`partial`, and the command exits 1 with "Incomplete scan: 8 skipped". That is the honest half of the
fix. The findings are still missing: 14 of the 15 in the four native binaries (the one found is HMAC in
the system fixture's Go binary, through the artifact parser), and the scanner finds 4 of 42 Tier 5
findings overall. Reading the dynamic symbol table and the string table of an ELF file would
recover most of them without bringing back the two DH false positives that plain text matching
over binary bytes produced.

Anything that wraps the scanner must expect exit code 1 on a tree with binaries. The benchmark
scores the run as long as the CBOM was written.

## 2. Compiled Java and minified JavaScript

Two of the 3 findings in `billing-core.jar` are detected; none of the 5 in `token-vault.jar` and the
system fixture's `ledger-service.jar`, and none of the 11 in the three minified bundles. Minified code is
text, so this is a pattern problem and not a file-reading one: the calls are there with shortened
receiver names.

## 3. Non-code assets

22 of 66 Tier 4 findings. In configuration files the scanner finds 24 of 62; every one it finds is
now complete. TLS cipher suites named in server configs remain unreported: all eight suite families
in the corpus score zero.

## 4. The 25 detections without parameters

| Where | Count | Why |
|---|---|---|
| Python | 9 | constants and wrappers in another module (Tier 3), a JWT algorithm table |
| Java | 8 | constants in another class, a strategy factory, compiled code |
| Go | 4 | a block cipher returned from a factory, a value read from config |
| Certificates and keys | 2 | a PKCS#1 RSA key with no size, a secp256k1 key |
| TypeScript, C# | 2 | a table indexed by a runtime value, a ternary between two curves |

Most need cross-file resolution, which `resolve.py` does for some Python shapes already. The last
row is correct behavior: with two possible values, the scanner should stay silent.

## 5. Still not detected at all

SHA3-256 (7 findings), LMS and XMSS public keys, and the TLS cipher suites above.
