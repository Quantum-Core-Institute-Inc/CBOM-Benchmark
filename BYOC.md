# Bring Your Own Code

The shipped corpus tells you how a scanner handles crypto in general. It can't tell you how it
handles *yours*: the wrapper library your platform team wrote in 2017, the HSM SDK everyone calls
through a helper, the config table that turns "LEGACY_COMPAT" into RSA-2048. Those patterns
repeat across hundreds of services, so a scanner that misses one of them misses it everywhere.

This kit lets you add those patterns as scored cases in an afternoon. Your cases live apart from the
shipped ones (`corpus/custom/` and `expected/custom/`), so you get two numbers: one comparable with
anyone else's, and one about your estate.

## What makes a good case

Pick patterns, not projects. Five to ten cases of 20–200 lines each beat one big repository.

Good candidates:

- **In-house crypto wrappers and "profile" tables.** If application code says `seal(data, profile="X")`
  and never names an algorithm, that's the case most worth adding. The shipped example is one.
- **Vendor SDK usage**: HSMs (PKCS#11), cloud KMS, payment HSM libraries, smart-card middleware.
- **Framework configuration**: Spring Security, .NET data protection, Django signing settings,
  service-mesh mTLS configs.
- **Generated code**: protobuf/gRPC stubs, OpenAPI clients with signing baked in.
- **The thing your last audit missed.** If you know a scanner already failed on something, encode it.

Leave out: business logic, whole repositories, anything you can't strip of secrets and hostnames.

## Step by step

### 1. Scaffold

```bash
python tools/byoc.py new treasury_signer --lang python --use firmware-signing \
    --owner "Payments Platform" --description "HSM-backed signing helper used by 40+ services"
```

`--lang` is `python`, `java` or `assets` (configs, certs, keys). `--use` sets the system type that
CNSA 2.0 deadlines depend on: `custom` (default), `web`, `networking`, `firmware-signing`, `os`, `niche`.
This creates `corpus/custom/treasury_signer/` with a runnable template and
`expected/custom/treasury_signer.json`, the case's answer key.

### 2. Trim and sanitize the code

Copy in the real pattern, then cut until only the crypto call shape remains.

- **Keep the call shape.** Same wrapper names, same indirection, same config-driven selection. That
  shape is what you're testing.
- **Keep real SDK names; fake only the behavior.** If production calls a vendor HSM SDK, write a
  small stub module with the same module, class and function names, implemented with ordinary
  `cryptography` or JCA calls. Scanners key on those names; the stub keeps them while letting the case run.
- **Replace hostnames** with `*.example.internal`, emails with `someone@example.com`, IPs with
  `192.0.2.x`.
- **Generate fresh keys for this test.** Never copy production key material, even "expired" keys.
- **Don't name the algorithm in comments.** Describe the pattern ("key size comes from the profile
  table"), not the answer ("uses RSA-2048"). Otherwise a scanner that reads comments gets free credit.
- **It must run.** `check` executes it. A case that doesn't run invites "your test is broken."
  It runs in the sandbox (`tools/sandbox.py`): a read-only copy of the case, no network, no
  credentials from your shell, five minutes. If your case needs a network call or a secret to run,
  it isn't a case yet: stub the call.

### 3. Write the answer key

Read the code and record each algorithm with `byoc.py add`:

```bash
python tools/byoc.py add treasury_signer --file signer/hsm.py --alg ECDSA-P384 \
    --anchor "session.sign(" --alt 'signer/profiles.py:"curve": "p384"' \
    --note "curve comes from the profile table" --confirm
```

- `--alg` takes ordinary names: `RSA-2048`, `AES-256-GCM`, `AES-128-CBC`, `SHA-1`, `HMAC-SHA256`,
  `ECDSA-P384`, `Ed25519`, `ML-KEM-768`, `X25519MLKEM768`, JCA names like `SHA256withRSA`. The tool
  shows how it interpreted the name; check that the parameters are what you meant.
- `--file` is **where the crypto call is made**. For a shared wrapper called with different
  parameters from different places (one wrapper, two key sizes), make one finding per caller,
  located at the caller.
- `--anchor` is text that appears **exactly once** in that file, on the line of the call. Lines are
  resolved from anchors, so editing the file later won't break the answer key.
- `--alt FILE[:ANCHOR]` adds another acceptable location, typically the config or table that names
  the algorithm. A scanner reporting it there still gets credit (but not "primary site" credit).
- One finding per file per algorithm family. Two different AES uses in one file? Split the file.
- `--confirm` says a human read the code. Unconfirmed findings are not scored and `check` fails on them.

Incidental algorithms you don't want to require, such as the SHA-256 inside OAEP, go in the
manifest's `also_ok` list so reporting them isn't a false positive. Files that should contain no
crypto at all need nothing: anything reported there counts as a false positive. That makes your
application files free negative controls.

### 4. (Optional) Ask for a draft

```bash
python tools/byoc.py draft treasury_signer          # print candidates
python tools/byoc.py draft treasury_signer --write  # append them, unconfirmed
```

Drafts come from the naive grep baseline. Use them as a checklist of things you might have missed,
never as the answer. On the shipped example, the draft:

- proposed AES with **no key size** for both bulk ciphers (the sizes live in the profile table),
- flagged RSA in the dispatch `if` statement rather than where the key is generated,
- picked `import` lines as anchors,
- and listed SHA-256 as a finding when it's incidental to OAEP and HKDF.

All four would have made a wrong answer key.

### 5. Check

```bash
python tools/byoc.py check                  # all cases
python tools/byoc.py check treasury_signer  # one case
```

Errors (must fix): unconfirmed findings, anchors that aren't unique, unknown algorithm names,
duplicate findings, missing files, anything that looks like a real credential, and a case that doesn't run.

Warnings (should fix): real-looking hostnames, email addresses and public IPs; comments that name
algorithms; private key blocks (fine in an `assets` case if freshly generated); manifest fields left as TODO.

### 6. Score

```bash
python tools/build_expected.py                       # rebuild the answer key with your cases
your-scanner corpus/ > reports/scanner-x.cdx.json    # scan the whole corpus, custom cases included
python tools/score.py reports/scanner-x.cdx.json --only-custom      # your estate's number
python tools/score.py reports/scanner-x.cdx.json --exclude-custom   # comparable with everyone else
python tools/score.py reports/scanner-x.cdx.json                    # both, one bucket per case
```

Each case gets its own row ("Your case: treasury_signer"), and the deadline view dates your
findings with the `use` you gave the case.

## Reading the result

A miss in your own case means more than a miss in the shipped corpus. The pattern is real and it
repeats. A scanner that can't see through your envelope library won't see through it in any of
the services that use it. When you compare vendors, multiply: "misses the envelope library's key
sizes" times "used by 140 services" is the number that belongs in the evaluation.

Report both scores. `--exclude-custom` is the one you can publish or compare with a peer;
`--only-custom` is the one that predicts what the tool will do in your environment.

## The rules, in one place

| Rule | Why | Enforced by |
|---|---|---|
| Every finding confirmed by a person | Drafts are wrong in predictable ways | `check` (error) |
| Anchors appear exactly once | Lines are resolved from them | `add`, `check` (error) |
| One finding per file and family | The scorer matches on that pair | `add`, `check` (error) |
| The case runs | Otherwise it isn't evidence | `check` (error) |
| No real secrets | It's a test corpus; it will be shared | `check` (error) |
| No real hostnames, emails, public IPs | They map your internal systems | `check` (warning) |
| No algorithm names in comments | They leak the answer | `check` (warning) |
| Freshly generated keys only | Production keys never leave production | `check` (warning) |

## Troubleshooting

- **"anchor appears N times"**: lengthen it until it's unique, e.g. `wrap(content_key, p["wrap_bits"])`
  instead of `wrap(`.
- **"don't recognize 'X'"**: use a standard name (see step 3). If your algorithm genuinely isn't
  covered (a national standard such as SM4 or GOST, say), add it to `FAMILIES` in `tools/cbomlib.py`
  with a normalizer rule and a test in `tools/test_normalize.py`.
- **Java case won't compile**: `byoc.py new --lang java` expects sources under `src/` and an entry
  point `com.acme.Main`; change `java_main` in the manifest if yours differs.
- **The case needs a dependency** (an SDK, a framework): prefer a stub with the same names. If you
  must add a real dependency, set the manifest's `run` to a command that sets it up, and note it in
  the description.

## The shipped example

`corpus/custom/example_envelope/` is a working case to copy from. Application code calls
`seal(data, profile="LEGACY_COMPAT")` or `profile="STANDARD"`. A profile table maps those names to
RSA-2048 key transport with AES-128-CBC, or P-256 key agreement with AES-256-GCM. Nothing in the
application code names an algorithm. Its answer key is `expected/custom/example_envelope.json`.
Delete both when you've added your own, or keep it as a calibration case.
