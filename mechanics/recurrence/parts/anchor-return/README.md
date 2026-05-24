# Recurrence / Anchor Return Part

## Role

`anchor-return` routes the support surface for `aoa-return-anchor-integrity`.

It asks whether a return-capable route names a real return reason, points to a
reviewable anchor, rebuilds only bounded context, and then re-enters or stops
honestly.

## Source Surfaces

- `evals/workflow/aoa-return-anchor-integrity/EVAL.md`
- `evals/workflow/aoa-return-anchor-integrity/fixtures/contract.json`
- `evals/workflow/aoa-return-anchor-integrity/runners/contract.json`
- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`
- `mechanics/recurrence/parts/anchor-return/fixtures/return-anchor-v1/README.md`
- `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.return-anchor-integrity.example.json`

## Inputs

- explicit return decisions or equivalent return artifacts;
- anchor refs, bounded plans, route packs, re-entry notes, or safe-stop notes;
- selected runtime return evidence when audit has kept it candidate-only.

## Outputs

- bundle-local anchor-fidelity reports;
- fixture replacement constraints for return-aware routes;
- adjacent-route notes when the real issue is checkpoint, approval, scope,
  verification, or final artifact quality.

## Stronger Owner Split

`Agents-of-Abyss` owns recurrence return law. `aoa-routing` owns local routing
behavior. `aoa-memo` owns durable memory anchors. Runtime owners own logs and
runtime return wrappers.

`aoa-evals` owns the bounded return-anchor proof interpretation. Authority
beyond that proof reading routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep anchor-return pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| final task quality pressure | owner repository acceptance route |
| broad workflow safety pressure | source-owner review plus relevant skill/playbook route |
| hidden continuity pressure | `aoa-memo` anchor route plus `aoa-agents` handoff posture route |
| automatic runtime recovery pressure | `abyss-stack` runtime recovery route after owner gates |
| general long-horizon competence pressure | bundle-local proof object plus source-owner evidence review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
