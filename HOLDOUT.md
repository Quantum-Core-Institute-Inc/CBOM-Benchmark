# Holdout sets: is the published score still telling the truth?

The corpus is public, and so is every scorecard. A scanner team that works from one will fix the
lines it misses. That's what a scorecard is for, but after a few releases the published score
measures how well the scanner knows *this corpus*, not how it does on code it has never seen.

`tools/holdout.py` generates fresh test code from a private seed, scores the scanner on it, and
compares the two. The difference is the **overfit gap**.

```bash
python tools/holdout.py generate --out holdout-run          # prints a random seed; keep it private
<scanner> holdout-run/corpus  ->  holdout-run/scan.cdx.json   # any scanner, same as the main corpus
python tools/holdout.py score holdout-run/scan.cdx.json --dir holdout-run \
    --published reports/<scanner>.json [--scope <scope.json>]
```

For the QCI scanner it's built in: set `CBOM_HOLDOUT_SEED` (a CI secret) and `run_qci_pqc.py`
generates, scans and scores a holdout set on every run, and gates on the gap. For any other
scanner, `bench.py run` does the same when the seed is set.

**Who sees the seed.** Only the process that generates the set. The scanner scans it in the
sandbox (`tools/sandbox.py`) with a scrubbed environment, so a scanner can't read the seed and
regenerate the answers, and evidence bundles record `sha256("cbom-holdout:" + seed)` instead of the
seed: reveal the seed later and anyone can check it was the one used.

## What gets generated

Five matched tiers, a broad set, negative controls and dependency manifests, in every language the
published corpus has: Python, Java, Go, JavaScript/TypeScript, C/OpenSSL and, since generator 1.2,
C#. Every file executes or compiles, like the published corpus (`go build`, `node`,
`cc -Werror -lcrypto`, `javac`, `dotnet build` with no package source).

**Matched** (`holdout-t1`, `holdout-t2`, `holdout-t3`, `holdout-pqc`, `holdout-mixed`). The same API spellings,
values and kinds of indirection as the published cases, with new code around them: new
identifiers, filler functions, file names, ordering, and which constant, config map, struct field,
default argument, enum, overload, macro or aliased import does the hiding. Tier 2 hides what the
published Tier 2 hides. Tier 3 builds multi-file projects in the three published shapes (a constant
module, a wrapper class, a registry with a factory), with every class, package and file name new.
The PQC tier uses the published post-quantum calls and parameter sets: Go `crypto/mlkem` at 1024,
Java `KeyPairGenerator` ML-KEM and ML-DSA. A hidden JavaScript case becomes TypeScript about half the
time, since the published TypeScript cases are where JavaScript hides things. The mixed tier is 12
realistic-size files from the same generator as the published `corpus/mixed/`, limited to the
families the published mixed files use in each language, and scored per site the same way. The gap
is computed only on these.

**Broad** (`holdout-broad`). Every spelling the generator knows: `hashlib.new`, PyCA `HMAC`,
`AES/CTR`, bare `Cipher.getInstance("AES")` (which is ECB), `"SHA1"` and `"SHA"` aliases, Go
`mlkem.GenerateKey768`, OpenSSL `EVP_CIPHER_fetch`, every import style. This reports recall only:
coverage beyond the corpus, not compared with anything.

**Assets and artifacts** (generator 1.1, its own random stream so nothing above changed). About
20 certificates, keys and keystores with random algorithms, sizes, curves, signature hashes and
containers: PEM, DER, chains, Kubernetes TLS secrets, PKCS#12 (AES-256-CBC and PBKDF2), PKCS#1,
SEC1, PKCS#8 plain and encrypted, SPKI, OpenSSH private and public keys, JWKS. Eight TLS and SSH
configs (nginx, `openssl.cnf`, Spring `application.yml`, sshd) with random protocol, suite and group
lists in the published spellings, plus ML-DSA certificates and post-quantum nginx and sshd configs.
Three `.pyc` and three `.jar` files compiled from generated programs that are run once and then
thrown away. A finding joins the gap only where the published corpus has the same cell (Tier 4
assets, Tier 5 Python and Java, PQC assets); other families go to holdout-broad. Key material is
fresh every run; the answer key for a seed is identical. The generator's leak checks don't apply to
these files, which name algorithms by design: config syntax does.

**Generator 1.2** covers what benchmark 2.4.0 added. C# cases, one project per case with its own file
name: one-shot `HashData`, `IncrementalHash` by name, a `Func<HashAlgorithm>` held in a field, a
settings class, a table or a parameter, `RSA.Create`, `ECDsa` and `ECDiffieHellman` on named curves,
`Aes` with key size and mode set separately, `AesGcm`, `TripleDES`, the `HMAC*` classes,
`Rfc2898DeriveBytes.Pbkdf2` and `DSA`. Sixteen configs instead of eight, now including Apache httpd
(`SSLProtocol -all +...`), HAProxy (a minimum version, TLS 1.2 and 1.3 suites on separate lines, the
DH group size on a tuning line) and strongSwan proposals in both `swanctl.conf` and legacy
`ipsec.conf` spelling. Firmware signing policies naming LMS and XMSS parameter sets, sometimes
beside a classical signer. Three minified JavaScript bundles (one line, one-letter names) and three
stripped native binaries linked to libcrypto. C# negatives join the others.

**Negatives.** 28 files across all seven languages: algorithm names in log lines, constants,
returned values, struct fields and changelog comments, including post-quantum claims
("ML-KEM-768 rollout approved"), and no crypto.

**Dependency manifests.** Six apps per seed, each with one manifest in a format the published corpus
uses (`requirements.txt`, `pyproject.toml`, `package.json`, `pom.xml` with and without a version
property, `build.gradle`, `go.mod`, `conanfile.txt`), two to four crypto libraries at real versions on
either side of their post-quantum thresholds, filler packages, and sometimes a commented-out
decoy or a crypto-sounding non-crypto package (`hashids`). Every version exists; they were checked
against PyPI, npm, Maven Central and the projects' tags.

Generated code files never contain comments past a one-line file header, never name identifiers after algorithms, and never
contain the seed. `tools/test_holdout.py` checks all of that.

## How the gap is computed

Findings are grouped into cells of (tier, language, family). Only cells present in both the
published corpus and the holdout count. Each cell is weighted by its holdout size, so the two recall
numbers describe the same mix. The gap is published minus holdout, in points.

The published side of a cell is the hand-written cases plus the generated calibration cases in
`corpus/calibration/` (generated by `tools/build_calibration.py`), which top every Tier 1-2 cell up to four. Without
them 155 of 191 cells held one case, and the published side was the larger share of the uncertainty.
Tier 3, PQC and mixed cells have no calibration cases and hold one to four. The 95% interval draws
every cell's rate from its Beta posterior on both sides, which treats a small cell as the weak
evidence it is, and is centered on the observed gap. A gap counts as significant when the whole
interval is above zero.

## Calibration

A metric like this is only worth something if it reads zero for a scanner that can't have overfit,
and reads high for one that has. Measured, not assumed:

| Scanner | What it is | Gap across seeds |
|---|---|---|
| Reference CBOM | the answer key | 0, every seed |
| `baseline_grep.py` | regexes with no file knowledge | -0.5 to +2.9, none significant (a weak control: it flags every name it sees) |
| qci-pqc-scan 0.3.0 | written before this testbench existed | -4.3 to -0.5, none significant |
| qci-pqc-scan v0.7 | the scanner team's release after reading the scorecards | -2.1 to -0.4, none significant |
| qci-pqc-scan v2.2 | the next release, measured on the same five seeds | -3.1 to +3.4, none significant |
| *Testbench 2.1, generator 1.1 (assets and artifacts in the gap):* | | |
| `baseline_grep.py` | | -2.3 to +1.0, none significant |
| qci-pqc-scan v0.7 | | -1.9 to +0.5, none significant |
| qci-pqc-scan v2.2 | | -2.1 to +3.5, none significant |
| qci-pqc-scan v2.3 | | -0.9 to +3.8, none significant |
| *Benchmark 2.4.0, generator 1.2 (C#, more configs, signing policies, minified and native artifacts in the gap):* | | |
| Reference CBOM | | 0, every seed |
| `baseline_grep.py` | | -4.0 to -2.2, none significant |
| qci-pqc-scan v0.7 | | -1.8 to -0.4, none significant |
| qci-pqc-scan v2.2 | | -3.1 to +0.7, none significant |
| qci-pqc-scan v2.3.4 | | -0.9 to +1.0, none significant |
| A scanner that memorized the answer key | | +100 |

Five seeds (1234, 4242, 55, 777, 90210), default sizes: 120 matched files, 48 broad, 10 Tier 3
projects, 12 mixed files, 28 negatives, 6 manifests, about 440 findings since generator 1.2 (about
350 before). Intervals are about ±5 points. How they narrowed:

| Testbench | What changed | Interval width |
|---|---|---|
| v1.14 | holdout extended to every language and tier | 14 to 15 |
| v1.15 | mixed tier added | 11.6 to 13.1 |
| v1.16 | calibration cases on the published side | 9.4 to 10.5 |
| 2.1 | assets, configs and compiled artifacts in the gap (129 to 148 cells) | 9.0 to 10.2 |
| 2.4, generator 1.2 | C#, more config formats, signing policies, minified and native artifacts in the gap (133 to 157 cells) | 8.9 to 10.5 |

Generator 1.2 added cells without narrowing the interval for QCI (9.7 to 10.5 in its declared scope):
the published side of the new cells is the hand-written cases alone, a few findings each. The grep
baseline now reads a little negative on every seed, -4.0 to -2.2, with the upper end of its interval
as low as +0.3: it does a little better on generated code than on the published cases in the same
cells. That is the direction that doesn't matter for overfitting, but it is closer to the line than
it was (-2.3 to +1.0 on generator 1.1), and which new cells moved it hasn't been worked out. A control
that reads significantly negative would mean the generated cases are easier than the published ones
they are matched to, which is a generator fault to fix, not a scanner result.

The holdout side is now the larger share. One seed with three times the matched files (360, seed
4242, v0.7) reads -0.5, interval -4.3 to +3.1: about ±3.7. Use `--files 360` when a release is close
to the line.

On the earlier, Python-and-Java-only generator, two simulated tuning runs read as they should:
QCI 0.3.0 plus hardcoded fixes for half its published misses read +25 to +41, and for all of them
+63 to +76, all significant. v0.7 read -9.4 to +3.2 there.

It took three rounds to get there. The first version showed QCI 0.3.0 "overfit" by 15 to 18 points,
which it can't be. The holdout's Tier 1 used aliased imports and rarer APIs that the published Tier
1 doesn't, so the gap was measuring "the holdout is harder", not fitting. The fix was to split
matched from broad and compare cell by cell. If you change the generator, rerun this table.

## Negative controls: the gap recall can't see

The recall gap misses one kind of fitting entirely: suppressing false positives until the
*published* negative files are clean. So the holdout also compares false positives per negative file,
published (all six languages) against freshly generated ones that say the same kind of thing in new
words: algorithm names in log lines, string constants and returned values, post-quantum claims.

| Scanner | Published, per file | Holdout, per file (5 seeds) | Gap |
|---|---|---|---|
| `baseline_grep.py` | 4.3 | 4.3 to 4.5 | -0.01 to +0.24 |
| QCI 0.3.0 | 0.60 | 0.33 to 0.75 | -0.27 to +0.15 |
| QCI v0.7 | 0.40 | 1.12 to 1.58 | **+0.72 to +1.18** |
| QCI v2.2 | 0.00 | 0.79 to 1.08 | **+0.79 to +1.08** |

The first version used 12 Python and Java negatives and the margin was thin: v0.7 read +0.52 on one
seed against a limit of 0.5. With 24 files in six languages the controls stay within -0.3 to +0.25
and v0.7 never comes within 0.2 of the limit.

On generator 1.2 (28 files, seven languages, benchmark 2.4.0) the gaps are: grep 0.00 to +0.36, QCI
v2.3.4 0.00 to +0.04, v2.2 **+0.64 to +0.79**, v0.7 **+0.60 to +0.92**. The same verdicts as before,
with less room on both sides of the 0.5 limit: grep's worst seed is 0.14 under it and v0.7's best
seed 0.10 over. If a later generator change moves either closer, the answer is more negative files
per seed (`--negatives`), not a different limit.

v0.7 added filters for the statement shapes in the published negatives (log calls, docstring lines,
string catalogs) and bare-word patterns (`HMAC\b`, `PBKDF2`) that fire on any mention. The
`negative_fp_gap` gate fails above +0.5 per file, set between those two. This check was added after
v0.7 showed the problem; the recall gap had read it as clean.

## Dependency manifests: reported, not gated

The holdout's libraries are scored like the published ones: a crypto library counts when the
scanner reports it from the right manifest. The gap is published minus holdout, weighted to the
holdout's ecosystem mix. Six manifests per seed is too few to gate on: QCI 0.3.0 and v0.7 both read 0
to +11 points across five seeds, with an identical `deps.py`. It's in the summary for the trend.

## Mixed files: a low score that carries over

The mixed tier is where v0.7's parameter accuracy collapses: 38% of detections on the published
mixed files. On the holdout's mixed files it's 19 to 36% across the five seeds, and its mixed recall
matches the published side within about 2 points every seed. That's the other thing a holdout is for: a
bad number that reproduces on unseen code is a real weakness, not an artifact of the corpus.

## Same-named files

Generated Go programs used to be `main.go`, as in real Go repositories. That surfaced a scanner bug
rather than overfitting: v0.7's de-duplication keys on the file's basename, so the same algorithm
near the same line in two different `main.go` files becomes one finding. On the PQC tier this read
as 77 to 93% holdout recall against 100% published. With the one-line fix (full path in the key),
matched holdout recall on seed 4242 goes from 59.9% to 67.6% and published from 59.7% to 61.5%.

The bug grows with the number of same-named files, so a large holdout made it look like fitting: at
360 files, v0.7 read +4.1 with an interval of +0.1 to +8.1, significant, and -0.1 with the fix. The
generator now gives every Go file a unique name, so the gap measures fitting and not this, and v0.7
reads 100% on the holdout PQC tier. Any per-tier drop on the holdout is still worth reading at the
file level before calling it fitting.

## What it can and can't tell you

Identifiers that only exist in the published Tier 3 projects, if hardcoded into a scanner, don't
help on the holdout's Tier 3, which shows up as a Tier 3 gap. v0.7 did hardcode some
(`AesCbcCipher`, `LegacyDesede`, `digest_factory`); they turned out to contribute nothing, and its
Tier 3 reads 79 to 100% on both sides. Reading the diff of each release is still part of the job.

TLS protocol settings in code (Tier 1 `TLS-` cases) have no generator yet, so they don't enter the gap.

Of the 55 findings added in 2.4.0, generator 1.2 covers the C# cases, the Apache, HAProxy and IPsec
configs, LMS and XMSS in signing policies, minified JavaScript and native binaries. Still without a
generator: the ProGuard-obfuscated jar (the generator's jars are compiled, not obfuscated), LMS and
XMSS in Java code, and the two stateful public keys identified by OID. A scanner could fit to those
eight findings and the gap wouldn't show it. C# also has no calibration cases on the published side
and no mixed or cross-file cases on either, so its cells are thin: read a C# jump with the interval
in view.

With the default 120 matched files the interval is about ±5 points; with 360, about ±3.7. That
catches a team that has fixed a meaningful share of the published misses in ways that don't carry
over. It won't catch a couple of overfit rules.

A real improvement shows up on both sides. Adding `\bEd25519PrivateKey\b` raises published and
holdout recall together, and the gap stays put. A rule that keys on a corpus file name, an
identifier like `legacy_checksum`, or one exact line raises only the published side.

The generator is public. Anyone can read it and cover every pattern it emits, and that's fine:
covering every pattern it emits *is* broad API coverage. What it prevents is fitting to particular
files. Keep the seed private, never publish the holdout files or per-finding results, and rotate the
seed if they leak. `run_qci_pqc.py` keeps them out of `reports/` and the CI artifacts unless you pass
`--holdout-detail` to a private location.
