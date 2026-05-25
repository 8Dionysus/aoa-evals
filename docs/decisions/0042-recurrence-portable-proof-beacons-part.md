# Recurrence Portable Proof Beacons Part

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/recurrence/parts/portable-proof-beacons/`

## Index Metadata

- Surface classes: mechanic part
- Mechanic parents: recurrence
- Guard families: part and payload
- Posture: active rationale

## Context

The former root `manifests/recurrence/` district carried
`component.evals.portable-proof-beacons.json` and its hook binding after nearby
recurrence and Agon manifests had moved into part-local homes.

The component names portable proof pressure, progression-evidence pressure, and
overclaim alarms. Its operation is a recurrence-style beacon ladder:
`hint -> watch -> candidate -> review_ready`. The audit and RPG surfaces it
references are inputs, not owners of the recurrence manifest.

## Options Considered

- Leave the files in former root `manifests/recurrence/`: preserves old
  placement but leaves an active recurrence operation outside the recurrence
  package.
- Create a `portable-proof-beacons` parent mechanic: names an artifact form and
  would repeat the earlier parent-package mistake.
- Move the component into `mechanics/audit/` or `mechanics/rpg/`: follows some
  inputs but steals the recurrence beacon operation from its owner route.
- Add a recurrence part at
  `mechanics/recurrence/parts/portable-proof-beacons/`.

## Decision

`component:evals:portable-proof-beacons` lives under the AoA-aligned
`recurrence` mechanic as the `portable-proof-beacons` part.

The part owns the recurrence beacon manifest, hook binding, and decision-closure
guidance. It does not own audit candidate packet curation, RPG progression
support, source proof bundle claims, runtime truth, or portable proof
acceptance.

## Rationale

This route keeps the parent mechanic name honest. The parent is `recurrence`
because the live operation is repeated proof-pressure observation and review
readiness. `portable-proof-beacons` describes a part-local artifact family, not
an independent proof organ.

Part-local placement also makes legacy accounting clearer: old root manifest
paths remain traceable through recurrence provenance while active edits start
from the recurrence package.

## Consequences

- Positive: the former root manifest path no longer carries an active
  recurrence component that already has a narrower mechanic owner.
- Tradeoff: the part crosses audit and RPG inputs, so the README and AGENTS card
  must keep those stronger owner splits visible.
- Follow-up: future portable proof machinery should strengthen source bundles,
  reports, or audit/RPG parts only after a separate evidence pass proves the
  owning operation.

## Current Applicability

As of 2026-05-24:

- Still valid: `portable-proof-beacons` remains a part-local recurrence beacon
  route under `mechanics/recurrence/`.
- Changed: the active part README now routes runtime-canon, accepted portable
  proof, universal-score, beacon-verdict, manifest-ownership, and overclaim
  repair pressure to owner routes, with validator tokens guarding those rows.
- Changed: descendant `AGENTS.md` now exposes an Operating Card and owner route
  table for low-context agents while routing executable checks to the parent
  `parts/AGENTS.md` lane.
- Superseded by: none.

## Review Log

### 2026-05-24 - Beacon boundary route wording

- Previous assumption: the beacon part could preserve its authority split as
  exclusion prose.
- New reality: the beacon part now exposes the same authority split as direct
  pressure-to-owner routes.
- Reason: portable-proof pressure crosses audit, RPG, runtime, source bundles,
  recurrence manifests, and proof-object repair; the active part should show
  the handoff route instead of burying it in negative wording.
- Source surfaces updated:
  `mechanics/recurrence/parts/portable-proof-beacons/README.md` and
  `scripts/validate_repo.py`.
- Validation: recurrence validator focus, recurrence part runners and tests,
  catalog check, root validation, semantic AGENTS validation, diff whitespace
  check, and full pytest passed.

### 2026-05-24 - Agent route-card applicability

- Previous assumption: the descendant portable-proof-beacons `AGENTS.md` could
  repeat authority limits and command blocks locally.
- New reality: the parent `parts/AGENTS.md` already owns centralized child
  validation commands, so the descendant card is clearer as an Operating Card
  plus owner routes.
- Reason: beacon pressure crosses audit intake, RPG progression, source
  bundles, runtime truth, recurrence doctrine, and portable eval authoring; a
  low-context agent needs the next owner route at the file boundary.
- Source surfaces updated:
  `mechanics/recurrence/parts/portable-proof-beacons/AGENTS.md`,
  `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: root validator, semantic AGENTS validation, catalog and generated
  reader checks, and focused validator tests.

## Boundaries

This decision does not make runtime evidence proof canon. It does not promote a
beacon to a verdict, create a universal progression score, or let recurrence
own audit/RPG/runtime truth.

## Validation

Planned checks for this slice:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_semantic_agents.py
```
