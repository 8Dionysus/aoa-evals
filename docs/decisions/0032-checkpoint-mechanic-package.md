# 0032 Checkpoint Mechanic Package

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/checkpoint/`

## Context

Checkpoint is a named AoA mechanic, and `aoa-evals` has enough local
proof-side evidence to route it as a live mechanic package.

The evidence cluster spans the `aoa-a2a-summon-return-checkpoint` bundle,
`aoa-long-horizon-depth`, self-agent checkpoint posture, fixture family
contracts, artifact-to-verdict hook examples, generated candidate readers,
quest proof pressure, and validation tests.

## Options Considered

- Leave checkpoint as a candidate family in `mechanics/EVIDENCE_CLUSTERS.md`.
- Move all checkpoint-named bundles into `mechanics/checkpoint/`.
- Create `mechanics/checkpoint/` as the AoA-aligned parent, move only
  checkpoint-specific support surfaces into parts, and keep source proof
  bundles plus audit hook schema and candidate-reader builders in their
  stronger routes.

## Decision

Create `mechanics/checkpoint/` for the operation:

`checkpoint pressure -> bounded checkpoint proof question -> part-local support surface -> bundle-local review -> bounded report or owner handoff`

The active parts are:

- `a2a-summon-return` for the A2A summon child-return checkpoint fixture, hook
  example, and validation test;
- `restartable-inquiry` for checkpoint-and-relaunch fixture and hook support
  around `aoa-long-horizon-depth`;
- `self-agent-posture` for the self-agent checkpoint eval posture and
  approval-boundary hook route.

source proof bundles stay under `evals/`. The artifact-to-verdict hook schema
and generated audit candidate readers stay under `mechanics/audit/`, but
checkpoint-specific hook examples live under the checkpoint parts that own
their proof route.

## Rationale

The parent name must be `checkpoint` because the proof-side work materializes
the center AoA checkpoint mechanic. The parts name narrower eval-side
operations rather than artifact forms.

This keeps checkpoint support from being hidden in root fixture directories or
inside `audit` merely because the examples use hook syntax. It also avoids the
opposite error of turning `aoa-evals` into the owner of checkpoint
implementation, memory canon, runtime activation, or self-agent role truth.

## Consequences

- Positive: future checkpoint proof work now has a current active route, part
  map, local agent guidance, legacy bridge, and validator-backed discovery
  surface.
- Tradeoff: audit candidate readers now scan mechanic-local hook examples as
  source inputs, so generated surfaces must be rebuilt when checkpoint hook
  examples move.
- Follow-up: candidate-lineage, return-anchor, and closeout checkpoint pressure
  remain bundle-local or adjacent until their support artifacts justify a
  distinct part.

## Boundaries

This decision does not move checkpoint source proof bundles into
`mechanics/checkpoint/`.

It does not move the artifact-to-verdict hook schema or audit candidate-reader
builders out of `mechanics/audit/`.

It does not authorize checkpoint implementation authority, memory canon, recall
sovereignty, live runtime activation, owner acceptance, hidden scheduler
behavior, autonomous self-repair, final child-output quality grading, or broad
long-horizon competence claims.

It does not transfer `Agents-of-Abyss`, `aoa-sdk`, `aoa-skills`,
`aoa-agents`, `aoa-memo`, `aoa-playbooks`, `aoa-routing`, `aoa-stats`, or
`abyss-stack` owner truth into `aoa-evals`.

## Validation

- `mechanics/checkpoint/README.md` names the owned operation, source surfaces,
  inputs, outputs, stronger-owner split, stop-lines, legacy route, and
  validation.
- `mechanics/checkpoint/AGENTS.md` names local editing law.
- `mechanics/checkpoint/PARTS.md` names the active part topology.
- `mechanics/checkpoint/PROVENANCE.md` bridges old root or audit placement
  questions into the owning legacy archive after the active route.
- `scripts/validate_repo.py` checks the package, parts, provenance bridge,
  decision, mechanic-local hook examples, and stale root paths.
- `python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
