# 0062 Checkpoint Part Contract Guard

## Status

Accepted.

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

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k checkpoint_part_readmes
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
