# 0041 Proof Infra Fixture Families

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-infra/parts/fixture-families/`

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

Keep source proof bundles under `bundles/`. Keep bundle-local
`bundles/<bundle>/fixtures/contract.json` as the contract surface that names each active family
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

This decision does not move `bundles/`, bundle-local contracts, runner
contracts, report schemas, reviewed reports, schemas, scorers, templates, or
generated readers into `proof-infra`.

It does not make fixture families stronger than bundle-local meaning, report
interpretation, audit candidate intake, memo truth, runtime evidence, sibling
owner truth, or AoA center mechanics.

It does not authorize route-card-only root `fixtures/<family>/` aliases.

## Validation

- `mechanics/proof-infra/PARTS.md`
- `mechanics/proof-infra/parts/fixture-families/README.md`
- `mechanics/proof-infra/PROVENANCE.md`
- owning proof-infra legacy archive for former root fixture placement
- affected bundle `bundles/<bundle>/fixtures/contract.json` paths
- generated catalog `proof_artifacts`
- `python scripts/build_catalog.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
