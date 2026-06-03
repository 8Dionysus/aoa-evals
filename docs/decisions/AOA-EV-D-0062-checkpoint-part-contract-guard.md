# Checkpoint Part Contract Guard

- Decision ID: AOA-EV-D-0062

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: mechanic part, validation guard
- Mechanic parents: checkpoint
- Guard families: part and payload
- Posture: active guard rationale

## Context

`mechanics/checkpoint/` is the active AoA-aligned parent for A2A summon return,
restartable inquiry, and self-agent checkpoint posture proof support. The part
README files had two weak spots:

- each part used a thin `Boundary` section instead of explicit
  `Stronger Owner Split` and `Stop-Lines`;
- some source-surface lists still named former root `fixtures/`, `examples/`,
  `tests/`, or `docs/` paths after those payloads had moved into part-local
  homes.

That combination makes future work more likely to route through old root
district names or overread checkpoint artifacts as implementation authority,
memory canon, runtime activation, owner acceptance, or broad long-horizon
competence.

## Decision

Require each active checkpoint part README to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The protected parts are:

- `mechanics/checkpoint/parts/a2a-summon-return/README.md`
- `mechanics/checkpoint/parts/restartable-inquiry/README.md`
- `mechanics/checkpoint/parts/self-agent-posture/README.md`

Their source-surface lists must name current part-local homes for fixture,
example, test, and posture-note payloads. Old root paths remain provenance
only through `mechanics/checkpoint/PROVENANCE.md`; the owning legacy archive
maps the historical placement internally.

## Consequences

- Future checkpoint part edits must keep owner split and stop-lines explicit.
- Root `fixtures/`, `examples/`, `tests/`, and `docs/` payload paths must not
  re-enter the active checkpoint route by inertia.
- A2A checkpoint proof remains below SDK control-plane implementation, summon
  skill truth, memo writeback acceptance, runtime closeout execution, and
  owner child-output acceptance.
- Restartable inquiry proof remains below memo schemas, playbook
  choreography, canon meaning, raw transcript continuity, and final inquiry
  truth.
- Self-agent checkpoint posture proof remains below `aoa-agents`,
  `aoa-playbooks`, `aoa-memo`, runtime activation, and owner acceptance.

## Current Applicability

As of 2026-05-24:

- Still valid: the three active Checkpoint part READMEs remain protected part
  contracts with inputs, outputs, stronger-owner split, stop-lines, and
  validation routes.
- Changed: part-level stop-line coverage now uses pressure-to-owner route rows,
  and validator tokens guard each route row for A2A summon return,
  restartable-inquiry, self-agent-posture, and the self-agent posture note.
- Superseded by: none.

## Review Log

### 2026-05-24 - Part boundary route wording

- Previous assumption: Checkpoint part READMEs and the self-agent posture note
  could keep boundaries as a boundary sentence followed by excluded claims.
- New reality: the part contracts and posture note now expose the same
  boundaries as direct pressure-to-owner routes.
- Reason: a low-context agent should see where checkpoint doctrine, SDK
  control-plane work, memo writeback, runtime execution, owner acceptance,
  long-horizon truth, self-agent contract meaning, and checkpoint ontology route
  next without parsing a prohibition list.
- Source surfaces updated:
  `mechanics/checkpoint/parts/a2a-summon-return/README.md`,
  `mechanics/checkpoint/parts/restartable-inquiry/README.md`,
  `mechanics/checkpoint/parts/self-agent-posture/README.md`,
  `mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`,
  and `scripts/validate_repo.py`.
- Validation: checkpoint validator focus, A2A part-local fixture test,
  candidate-reader checks, catalog check, root validation, semantic AGENTS
  validation, diff whitespace check, and full pytest passed.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_mechanic_surface_contracts.py -k checkpoint_part_readmes
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
