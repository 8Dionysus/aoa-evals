# Anchor Return

## Role

`anchor-return` routes the support surface for `aoa-return-anchor-integrity`.

It asks whether a return-capable route names a real return reason, points to a
reviewable anchor, rebuilds only bounded context, and then re-enters or stops
honestly.

## Source Surfaces

- `bundles/aoa-return-anchor-integrity/EVAL.md`
- `bundles/aoa-return-anchor-integrity/fixtures/contract.json`
- `bundles/aoa-return-anchor-integrity/runners/contract.json`
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

`aoa-evals` owns only the bounded return-anchor proof interpretation.

## Stop-Lines

Do not use this part to claim final task quality, broad workflow safety, hidden
continuity, automatic runtime recovery, or general long-horizon competence.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-return-anchor-integrity
python scripts/build_catalog.py --check
```
