# Proof Infra Fixture Families

- Decision ID: AOA-EV-D-0041
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-infra/parts/fixture-families/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part
- Mechanic parents: proof-infra
- Guard families: none
- Posture: active rationale

## Context

After comparison, recurrence, checkpoint, Experience, Antifragility,
Method-growth, RPG, Growth Cycle, and Distillation support moved into narrower
active mechanic parts, root `fixtures/` still held a set of public-safe shared
fixture families.

Those remaining families are real proof support, but they do not prove new
parent mechanics. Their claims are owned by source bundles such as
`aoa-ambiguity-handling`, `aoa-verification-honesty`,
`aoa-trace-outcome-separation`, and memo pilot bundles. Some are adjacent to
audit, proof-loop, memo, or distillation, but the current evidence shows
bundle-local proof support rather than an independent parent operation.

The old proof-infra decision said not to move root infrastructure directories.
That was correct as an anti-junk-drawer rule, but too broad for the current
refactor: generic shared fixture families now have an active proof-infra part
that can own their reusable support path while leaving bundle meaning stronger.

## Options Considered

- Leave the remaining families in root `fixtures/` as loose shared support.
- Create new parent mechanics from fixture names or nearby bundle themes.
- Move all support directories into `proof-infra`.
- Move only the generic shared fixture families into a `proof-infra` part.

## Decision

Move the remaining generic shared fixture families to:

`mechanics/proof-infra/parts/fixture-families/fixtures/<family>/README.md`

This route applies only when there is no narrower active mechanic that owns the
family operation.

Keep source proof bundles under `evals/`. Keep bundle-local
`evals/<family>/<eval>/fixtures/contract.json` as the contract surface that names each active family
path. Keep generated catalog `proof_artifacts` derived from those contracts.

Root `fixtures/` remains a compatibility route card and must not regain active
fixture-family directories by habit.

## Rationale

This route preserves the distinction between reusable proof support and proof
meaning. The bundle still owns the bounded claim, object under evaluation,
verdict logic, and report interpretation. The `proof-infra` part owns only the
generic fixture-family library path.

It also avoids the earlier failure mode of inventing mechanics from artifact
forms. `trace-outcome-bounded-v1`, `witness-trace-v1`, memo guardrails, and
verification honesty fixture families are support surfaces, not parent
mechanics.

## Consequences

- Positive: no active fixture-family directories remain stranded in root
  `fixtures/`.
- Positive: generic fixture support now has a clear part, provenance bridge,
  and validation route.
- Tradeoff: paths are longer, so bundle contracts, generated readers, tests,
  and guide text must stay aligned.
- Follow-up: if a later family proves a narrower active mechanic owner, move it
  out of `proof-infra` with its own decision and provenance map.

## Boundaries

This decision does not move `evals/`, bundle-local contracts, runner
contracts, report schemas, reviewed reports, schemas, scorers, templates, or
generated readers into `proof-infra`.

It does not make fixture families stronger than bundle-local meaning, report
interpretation, audit candidate intake, memo truth, runtime evidence, sibling
owner truth, or AoA center mechanics.

It does not authorize route-card-only root `fixtures/<family>/` aliases.

## Current Applicability

As of 2026-05-24:

- Still valid: generic shared fixture families route through
  `mechanics/proof-infra/parts/fixture-families/` when no narrower active
  mechanic owns the family operation.
- Still valid: bundle-local `EVAL.md`, `eval.yaml`, fixture contracts, and
  reviewed reports own proof meaning.
- Changed: active part route text now expresses the family-name and
  domain-owned pressure as boundary routes instead of a list of prohibitions.
- Changed: descendant `AGENTS.md` now exposes an Operating Card and boundary
  route table for low-context agents while routing executable checks to the
  parent `parts/AGENTS.md` lane.
- Source surfaces updated:
  `mechanics/proof-infra/PARTS.md`,
  `mechanics/proof-infra/parts/fixture-families/README.md`,
  `mechanics/proof-infra/parts/fixture-families/AGENTS.md`,
  `scripts/validate_repo.py`.

## Review Log

### 2026-05-24 - Boundary-route wording

- Previous assumption: the proof-infra fixture-family contract needed an
  explicit negative token such as creating a parent mechanic from a family name.
- New reality: the same invariant is clearer for agents when written as a
  pressure-to-route map: family-name parent pressure goes first to
  `mechanics/EVIDENCE_CLUSTERS.md`, while the fixture-family part stays
  reusable support.
- Reason: the active topology is now strong enough that owner routes carry the
  boundary without repeating negative prose at every entry point.
- Validation: `python scripts/validate_repo.py`, focused validator tests, and
  semantic AGENTS validation.

### 2026-05-24 - Agent route-card applicability

- Previous assumption: the descendant fixture-family `AGENTS.md` could repeat
  role limits and command blocks locally.
- New reality: the parent `parts/AGENTS.md` already owns centralized child
  validation commands, so the descendant card is clearer as an Operating Card
  plus boundary routes.
- Reason: low-context agents need role, input, output, owner, next route,
  tools, and validation ownership at the file boundary without duplicating the
  parent command lane.
- Source surfaces updated:
  `mechanics/proof-infra/parts/fixture-families/AGENTS.md`,
  `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: root validator, semantic AGENTS validation, catalog check, and
  focused validator tests.

## Validation

- `mechanics/proof-infra/PARTS.md`
- `mechanics/proof-infra/parts/fixture-families/README.md`
- `mechanics/proof-infra/PROVENANCE.md`
- owning proof-infra legacy archive for former root fixture placement
- affected bundle `evals/<family>/<eval>/fixtures/contract.json` paths
- generated catalog `proof_artifacts`
- `python scripts/build_catalog.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
