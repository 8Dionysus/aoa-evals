# Recurrence / Recursor Boundary Part

## Role

`recursor-boundary` routes the support surface for recursor readiness boundary
checks inside recurrence proof work.

It keeps witness/executor recursor seeds readiness-only by routing spawn,
Codex-install, contestant-drift, scar/verdict/rank, executor-certification, and
scheduler pressure to stronger owners.

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
the bounded readiness-boundary scorer and proof route. Authority beyond that
proof reading routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep recursor-boundary pressure with the owner that can act on
it:

| Pressure | Owner route |
| --- | --- |
| live recursor activation pressure | `aoa-agents` role route plus `abyss-stack` runtime route |
| agent spawn authority pressure | `aoa-agents` approval and role route |
| arena eligibility pressure | Agon owner surface plus owner acceptance route |
| scar ownership pressure | Agon owner surface plus source-owner evidence route |
| verdict authority pressure | bundle-local proof review plus owner verdict route |
| rank mutation pressure | Agon/ranking owner route |
| hidden scheduling pressure | `aoa-playbooks` choreography route plus runtime owner route |
| runtime readiness pressure | `abyss-stack` runtime readiness route after owner gates |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
