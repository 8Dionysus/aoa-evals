# Comparison Spine Mechanic Package

- Decision ID: AOA-EV-D-0011
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/comparison-spine/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package
- Mechanic parents: comparison-spine
- Guard families: none
- Posture: active rationale

## Context

The proof-object route is now explicit, and the next live pressure is comparison
semantics. `aoa-evals` already has comparison docs, comparison manifest fields,
generated comparison readers, report routes, tests, and validators. The risk is
not missing files; the risk is overreading baseline, peer comparison, or
longitudinal movement as stronger proof than the source bundle supports.

Current comparison pressure is visible in:

- `docs/guides/COMPARISON_SPINE_GUIDE.md`
- `docs/guides/BASELINE_COMPARISON_GUIDE.md`
- `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
- `generated/comparison_spine.json`
- `scripts/validate_repo.py`
- `tests/test_validate_repo.py`
- comparison reports under `reports/`

## Options Considered

- Create `proof-infra` first because shared fixtures, runners, scorers,
  schemas, reports, and templates are broad.
- Leave comparison-spine as docs plus generated validation only.
- Create `mechanics/comparison-spine/` now because comparison semantics have a
  narrow live operation, generated reader, tests, and high overclaim risk.

## Decision

Create `mechanics/comparison-spine/` for the operation:

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

The package routes fixed-baseline, peer-compare, and longitudinal-window
semantics. The initial package did not move bundles, reports, fixtures, or
generated readers; decision `0029` later moved comparison-spine-owned shared
dossiers into package-local parts, and decision `0040` later moved
comparison-spine-owned fixture families into the same active parts.

## Rationale

Comparison is where proof language can become too strong quickly. A single
clean baseline, a polished peer comparison, or a vivid repeated-window sequence
can be mistaken for broad growth, global ranking, or promotion readiness.

Making comparison-spine a package keeps the active route visible while leaving
source truth in the proof object and generated truth in deterministic builders.

## Consequences

- Positive: baseline, peer-compare, and longitudinal-window work now has a
  package route with validator-backed discovery.
- Tradeoff: `proof-infra` remains a candidate even though it owns many shared
  surfaces. That is acceptable until a narrower shared-infra operation becomes
  the live pressure.
- Follow-up: later validators can tighten comparison-mode-specific report and
  evidence contracts without turning comparison metadata into promotion
  authority.

## Boundaries

This decision does not move, rename, promote, deprecate, or rewrite any eval
bundle.

It does not move fixtures, schemas, generated readers, or comparison bundles
into `mechanics/comparison-spine/`.

Comparison-spine report movement is governed by
`docs/decisions/AOA-EV-D-0029-comparison-spine-report-parts.md`.
Comparison-spine fixture family movement is governed by
`docs/decisions/AOA-EV-D-0040-comparison-spine-fixture-parts.md`.

It does not make `generated/comparison_spine.json` source truth.

It does not turn fixed-baseline, peer-compare, or longitudinal-window results
into broad capability growth, repo-global scoring, runtime health, or sibling
owner acceptance.

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/comparison-spine/` remains the active comparison
  operation for fixed-baseline, peer-compare, and longitudinal-window proof
  claims.
- Changed: active comparison-spine route surfaces now express overread,
  generated-reader, broad-growth, repo-global-score, runtime-health, sibling,
  and promotion pressure as pressure-to-route maps.
- Superseded by: none.

## Review Log

### 2026-05-24 - Comparison boundary routes

- Previous assumption: comparison-spine could keep its overread limits legible
  through stop-line prose.
- New reality: the parent and part surfaces now route each pressure class to
  source bundles, mode-specific parts, generated builders, growth/progression
  owners, runtime owners, sibling owners, or release/report owners.
- Reason: comparison outputs are especially easy to overread; routing pressure
  directly to the next owner gives a low-context agent a clearer action path
  than a prohibition list.
- Source surfaces updated: `mechanics/comparison-spine/README.md`,
  `mechanics/comparison-spine/DIRECTION.md`,
  `mechanics/comparison-spine/PARTS.md`, the four active comparison part
  READMEs, and `scripts/validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
