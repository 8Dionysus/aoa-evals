# 0068 Method-growth Part Owner-split Contract

## Status

Accepted.

## Context

`mechanics/method-growth/` is the active AoA-aligned parent for eval-side
Method-growth proof. Its active parts, `candidate-lineage` and `owner-landing`,
are intentionally adjacent but not interchangeable:

- `candidate-lineage` checks whether reviewed work carries visible lineage
  through cluster, candidate, seed, object, dropped branch, or supersession
  evidence.
- `owner-landing` checks whether a reviewed candidate is routed toward a
  plausible owner without turning derivative repositories into first-authoring
  homes.

Both parts already had stop-lines, but the part README files used a softer
`Owner Split` heading. That is risky because Method-growth language can easily
become final owner-object quality, owner-local acceptance, seed truth, memory
canon, derivative first-authoring, or a broad growth score.

## Decision

Require both part README files to expose `## Stronger Owner Split` and keep
their stop-lines part-specific:

- `mechanics/method-growth/parts/candidate-lineage/README.md`
- `mechanics/method-growth/parts/owner-landing/README.md`

`candidate-lineage` remains lineage proof only. `owner-landing` remains
owner-fit routing proof only. Source proof bundles stay under `evals/`, and
final owner truth stays with the owning repositories.

## Consequences

- Future Method-growth part edits must preserve the split between lineage
  integrity, owner-fit routing, and final owner-local truth.
- `aoa-evals` may describe bounded proof wording, fixture/report contracts,
  missing-stage flags, nearest-wrong-target evidence, and claim limits.
- It must not claim final object quality, owner acceptance, hidden promotion,
  derivative first-authoring, seed truth, memory canon, or universal growth.

## Current Applicability

As of 2026-05-24:

- Still valid: `candidate-lineage` and `owner-landing` remain separate guarded
  part contracts under `mechanics/method-growth/`.
- Changed: both part READMEs now express stop-line coverage as
  pressure-to-owner route rows, and validator tokens guard those rows.
- Superseded by: none.

## Review Log

### 2026-05-24 - Part boundary route wording

- Previous assumption: Method-growth part contracts could keep their stronger
  owner split plus stop-line terms as exclusion prose.
- New reality: `candidate-lineage` and `owner-landing` now guard full route
  rows that name each pressure and its owner route.
- Reason: lineage, owner fit, final object truth, derivative first-authoring,
  seed, memory, practice, playbook, and stats pressure each has a different
  owner; the active parts should make the handoff executable for a low-context
  agent.
- Source surfaces updated:
  `mechanics/method-growth/parts/candidate-lineage/README.md`,
  `mechanics/method-growth/parts/owner-landing/README.md`, and
  `scripts/validate_repo.py`.
- Validation: method-growth validator focus, candidate-lineage and owner-fit
  eval validation, catalog check, root validation, semantic AGENTS validation,
  diff whitespace check, and full pytest passed.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k method_growth_part_owner_split
python scripts/validate_repo.py --eval aoa-candidate-lineage-integrity
python scripts/validate_repo.py --eval aoa-owner-fit-routing-quality
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
