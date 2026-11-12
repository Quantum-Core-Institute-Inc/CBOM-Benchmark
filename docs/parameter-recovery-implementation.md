# Parameter Recovery Scorecard Section

## Goal
Emit a dedicated **Parameter Recovery** section in every scorecard (`tools/score.py` + renderer).

## Required output

```markdown
## Parameter Recovery

| Bucket | Detected | Parameters correct | % |
|--------|----------|--------------------|---|
| Overall | 250 | 136 | 54.4% |
| Tier 1 | … | … | … |
| Tier 2 | … | … | … |
| C# | … | … | … |
| Mixed | … | … | … |
| RSA | … | … | … |
| AES-GCM | … | … | … |
```

## Implementation notes
- Reuse existing `params_ok` logic.
- Add per-tier, per-language, and per-family breakdowns.
- Keep methodology 2.3 (additive metric).
- Update `tools/render_docs.py` so comparison tables can include the new section.
- Link to `PARAMETER_CHEATSHEET.md`.

## Acceptance
- Reference CBOM scores 100% parameter recovery.
- Existing scorecard numbers unchanged except for the new section.
- Tests in `tools/test_scorer.py` cover the new section.
