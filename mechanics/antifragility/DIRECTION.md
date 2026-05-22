# Antifragility Direction

Antifragility in `aoa-evals` should make stress, recovery, and bounded repair
proof reviewable without claiming global resilience or runtime self-healing.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-side route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active antifragility part map.
- `parts/`: posture, stress-window, and repair-proof support contracts.
- `PROVENANCE.md`: controlled bridge from active route to old placement and fixture accounting.
- `legacy/`: lineage only; not a repair backlog.
- `evals/`: source proof objects that remain stronger than support parts.

## Current contour

- Keep the parent name `antifragility`; posture review, stress windows, and
  repair proof are parts under that mechanic.
- Keep runtime and machine evidence candidate-only until bundle-local review
  accepts a bounded interpretation.
- Keep diagnosis pressure routed through `growth-cycle/diagnosis-gate` unless a
  later evidence pass proves a narrower antifragility part.
- Keep repeated-window movement under `comparison-spine`.

## Growth rule

Add detail only when an antifragility proof operation repeats with its own
claim, evidence shape, support payload, and validation. Do not use
antifragility as a generic home for any repair-shaped material.

## Stop-lines

- Do not claim broad resilience, automatic recovery, deletion authority,
  one-score health, or runtime self-healing.
- Do not promote selected runtime evidence into proof canon by placement.
- Do not move diagnosis, growth-cycle, or comparison surfaces here by naming
  similarity alone.

## Validation

Use the validation lane in [mechanics/antifragility/AGENTS.md](AGENTS.md#validation).
