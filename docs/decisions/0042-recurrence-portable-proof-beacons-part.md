# Recurrence Portable Proof Beacons Part

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/recurrence/parts/portable-proof-beacons/`

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
