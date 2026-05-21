# Recurrence / Recursor Boundary Part

## Role

`recursor-boundary` routes the support surface for recursor readiness boundary
checks inside recurrence proof work.

It keeps witness/executor recursor seeds readiness-only: no live spawn, no
Codex install by default, no assistant contestant drift, no scar/verdict/rank
authority, no executor self-certification, and no hidden scheduler.

## Source Surfaces

- `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`
- `evals/boundary/aoa-recurrence-control-plane-integrity/RECURSOR_READINESS_BOUNDARY_EXTENSION.md`
- `mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/`
- `mechanics/recurrence/parts/recursor-boundary/scorers/recursor_readiness_boundary.py`
- `mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py`
- `mechanics/recurrence/parts/recursor-boundary/tests/test_recursor_readiness_boundary_eval_seed.py`

## Inputs

- recursor role contracts;
- witness/executor pair separation contracts;
- Codex projection candidate payloads;
- expected pass or fail axes for readiness-only boundary cases.

## Outputs

- per-case recursor readiness boundary run reports;
- failed-axis notes for candidate-only projection, pair separation,
  no-spawn, no-scar/verdict/rank, or executor self-verification drift.

## Stronger Owner Split

`aoa-agents` owns role truth and current Codex projection wiring such as
`repo:aoa-agents/config/codex_subagent_wiring.v2.json`. `aoa-sdk` owns typed read-only
readiness and boundary scan helpers over those sibling-owned surfaces.
`Agents-of-Abyss` owns recurrence and recursor boundary law. `aoa-evals` owns
only the bounded readiness-boundary scorer and proof route.

## Stop-Lines

Do not use this part to claim live recursor activation, agent spawn authority,
arena eligibility, scar ownership, verdict authority, rank mutation, hidden
scheduling, or runtime readiness.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
