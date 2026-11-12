# Holdout Generator Coverage Extension

## Goal
Extend the holdout generator so the new hard cells enter the overfit gap.

## New cells

| Cell | Generator work |
|------|----------------|
| Minified JavaScript | One-line bundles with hoisted constants and destructured crypto calls |
| Stripped ELF / Go binaries | dynsym symbols, `.rodata` strings, immediate operands |
| LMS / XMSS pure-Python | RFC 8554-style implementation on hashlib alone |
| LMS / XMSS OID-only | Public keys recognisable only by OID |

## Acceptance
- Generator 1.3 (or 1.2.1) produces the new cells.
- Recalibration on five seeds remains non-significant for reference and QCI.
- `HOLDOUT.md` updated.
- Methodology stays 2.3.
