# Binary / Adversarial Evidence Enforcement

## Goal
Scanners must either report from explicit evidence sources or declare a recorded skip. Coverage files may not claim a binary was inspected and clean when nothing was reported.

## Expected evidence sources (stripped ELF / Go)

| Source | Examples |
|--------|----------|
| dynsym symbols | `EVP_md5`, `EVP_des_ede3_cbc`, `EVP_PKEY_CTX_set_rsa_keygen_bits` |
| `.rodata` strings | algorithm names fetched at runtime |
| Immediate operands | numeric curve ids, key sizes |

## Required behavior
1. If a binary is scanned and no findings are emitted, the scanner (or adapter) must record a skip:
   `skip(path, "binary: not scanned as source / no symbol evidence")`.
2. The scorer treats an unrecorded empty result on a known binary as a coverage honesty failure (visible in the scorecard).
3. Holdout generator will include matching cells (separate PR).

## Acceptance
- A scanner that reports nothing on the three stripped binaries without a recorded skip fails a new honesty check.
- Documented in `FINDINGS.md` item 1.
