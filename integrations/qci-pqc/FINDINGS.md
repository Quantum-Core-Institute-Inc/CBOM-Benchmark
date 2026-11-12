# qci-pqc-scan v2.3.4.1 on the QCI CBOM Benchmark: findings for the scanner team

Scanner: `qci-pqc-scan` 2.3.4.1, internal adapter, run in the sandbox. Benchmark 2.6.0 (410
findings, methodology 2.3, NIST policy), declared scope from `integrations/qci-pqc/scope.json`,
holdout generator 1.2. Reproduce with `python tools/run_qci_pqc.py --scanner <checkout>` and
`CBOM_HOLDOUT_SEED` set. Evidence: `evidence/qci-v2.3.4.1/` and `evidence/perf-qci-v2.3.4.1/`; the
numbers below are in `reports/qci-pqc/SUMMARY.md`.

## The short version

| | In declared scope | Everything |
|---|---|---|
| Recall | 64.2% | 61.0% |
| At primary site | 61.9% | 58.8% |
| Parameters correct (of detected) | 54.5% | 54.4% |
| Precision | 99.6% (1 false positive) | 99.6% |
| Ticket-ready (of detected) | 45.9% | 45.2% |
| Deadline-weighted recall | 65.1% | 61.8% |
| Missed findings due by 2030 | 46 | 56 |
| Crypto libraries in the right manifest | 96.4% | |
| Overfit gap | -0.8 (interval -5.9 to +4.3), not significant | |
| Negative-control gap | 0.0 per file | |

What works: precision is where it should be, with no false positives in negative controls and no
PQC over-claims; libraries are found in the right manifest; the published score carries over to
unseen code; the CBOM validates as CycloneDX 1.6; and on the large tree it finds all 60 planted uses
in 115 seconds with no fall-off toward the end.

The gate floors were reset on this release to v2.3.4.1's own numbers, at the scanner owner's
request, so it passes every gate by construction. What the old floors would have flagged is item 1:
six findings this release no longer reports.

## 1. Binaries are read and nothing is reported from them

The corpus now has three stripped binaries and a Go binary: 15 findings, none reported.

Six findings that the scanner used to report are gone: MD5 and 3DES in the stripped binary
(`corpus/tier5/c/bin/meterd`), and RSA, HMAC, SHA-1 and SHA-256 in the Go binary of the system
fixture. Run on `corpus/tier5/c` alone, 2.3.4.1 reports nothing where the release before it reported
MD5 and 3DES.

Two things make this worse than a plain miss:

- **The coverage file says nothing happened.** `scan-coverage.json` counts the binary as read,
  lists the `artifact` parser, and shows `skipped: []` and `partial: false`. A reader of that file
  concludes the binary was inspected and is clean.
- **The release notes don't mention it.** They list a symlink check and a change to wrapper
  matching.

**The cause is one added check.** In `scanner.py`, the source pass now reads each file as bytes
and moves on if there is a NUL in the first 1,024 (`if b"\x00" in raw[:1024]: continue`). Before,
it decoded everything as text and ran the source patterns over it, which is how `EVP_md5` in a
binary's symbol table became an MD5 finding, and also how "DH" somewhere in the bytes became a DH
finding. The check removed both at once: the two false positives are gone (precision 98.8% to
99.6%) and so are the six real findings. The `continue` records nothing, which is why the coverage
file still shows the binary as read.

Two changes fix it properly. Record the skip (`skip(rel, "binary: not scanned as source")`), so the
coverage file is true. Then get the findings back from evidence that can't produce the old false
positives: `artifacts.py` already parses ELF headers for needed libraries; reading the dynamic symbol
table next to it (`EVP_md5`, `EVP_des_ede3_cbc`, `EVP_PKEY_CTX_set_rsa_keygen_bits`) gives exact
names where the byte matcher gave substrings.

## 2. Parameters: found, but not sized

Parameters are right on 54.5% of what is detected. The pattern is consistent: the algorithm is
named and the key size, curve or mode is left out.

| Where | Parameters right |
|---|---|
| Python, Tier 1 | 100% |
| Java, Tier 1 | 66.7% |
| Go, C, JavaScript, Tier 1 | 42.9% to 46.7% |
| C#, Tier 1 | 11.1% |
| C, C#, TypeScript, Tier 2 | 0% |
| Mixed files | 0% to 54.5% by language |

Examples: `RSA.Create(2048)` reported as RSA with no size; `new AesGcm(key, 16)` as AES with no mode;
`tune.ssl.default-dh-param 1024` as DH with no size. A finding without its parameters can't be dated
(RSA-1024 is out now, RSA-3072 is not) and can't become a ticket, which is most of why ticket-ready
is 45.9%.

The same gap shows in the asset fields a ticket needs: certificate expiry and subject are correct on
2 of 11 detected certificates, and the protocol version is given on none of 8 detected TLS findings.

## 3. Formats and languages it doesn't read yet

| Area | Found | What happens |
|---|---|---|
| Apache httpd (5) | 0 | `SSLProtocol` and `SSLCipherSuite` aren't read. The nginx equivalents are. |
| HAProxy (6) | 1 | Finds the DH group, without its size. Misses `ssl-min-ver` and both cipher lines. |
| IPsec (9) | 1 | Finds `chacha20poly1305` in `swanctl.conf`. `aes256-sha256-modp2048` and `3des-sha1-modp1024!` aren't parsed. |
| LMS and XMSS (8) | 0 | Not in Bouncy Castle code, not in the pure-Python implementation, not by OID in the two public keys, not by name in the signing policy. The P-384 signer in that policy is missed too. |
| Minified JavaScript (11) | 0 | Three one-line bundles. `e.createHash("md5")` isn't found, though the same call is in ordinary source. cdxgen finds 6 of these 11 and grep 8. |
| Stripped binaries (11) | 0 | See item 1. Grep finds 7 of 11 from symbol and name strings. |
| C#, direct (13) | 9 | Misses `MD5.HashData`, `SHA256.HashData` and `SHA3_256.HashData` in a file where it finds `SHA1.HashData`, and `new HMACSHA256(...)`. |
| C#, indirection (6) | 3 | Misses `IncrementalHash.CreateHash(new HashAlgorithmName(Fingerprint))` and both entries of a `Func<HashAlgorithm>` table. |
| TypeScript and C, indirection | 3 of 7, 2 of 6 | `as const` config objects, template literals, macros and function pointers. |
| Go PQC (4) | 1 | `crypto/mlkem` and the hybrid group in `tls.Config`. |
| Tier 5, source (12) | 2 | Runtime-assembled names, reflection, hand-rolled algorithms. Expected to be hard. |

## 4. The one false positive

**SHA-256 reported for `SHA512.Create`** (`corpus/tier2/csharp/DispatchTable/Program.cs`, line 10).
The file has no SHA-256 in it. Something maps a SHA-2 constructor reference to the default member of
the family.

## 5. Routing and links in the system fixture

- **Five of 13 detected system findings route to the wrong team.** Where the shared wrapper and its
  config decide the algorithm, the scanner reports the wrapper, so the ticket goes to
  platform-security instead of the edge, payments or ledger team that has to change its code.
  Reporting the calling service as well fixes it.
- **No asset links.** The CBOM doesn't connect the nginx config to the certificate it serves, or the
  certificate to its key (0 of 2).

## 6. Fix and rescan

4 of 8 eligible migrations verify. The other four fail for the reason in item 2: after the fix the
scanner finds the new algorithm and not its parameters (ML-DSA-65 in Python, AES-256-GCM in Go,
JavaScript and C). The nginx and sshd migrations aren't eligible, because the scanner didn't find
everything they retire beforehand. Nothing outside the migrated files changed between the two scans.

## Where to spend effort

1. **Decide what the scanner does with binaries, and say so.** Either restore the findings from
   imported symbols or declare binaries out of scope and list them as not inspected. Six findings.
2. **Carry parameters through.** The detections exist; sizes, curves and modes at the call site are
   the cheapest points on the board, and they move parameters, ticket-ready and four migrations at
   once.
3. **Apache and HAProxy directives.** Eleven findings, and the nginx parser is already there.
4. **IPsec proposal strings.** Nine findings behind one small grammar.
5. **LMS and XMSS.** Eight findings, and the first thing a CNSA 2.0 firmware-signing audit asks about.
   A scanner that can't name them reports that estate as empty.
