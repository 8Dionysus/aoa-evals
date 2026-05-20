# AGENTS.md

## Applies to

`mechanics/` operation packages and package route cards.

## Role

Mechanics route repeatable proof-layer operations.

They do not own eval bundle meaning, root design, roadmap direction, generated
truth, runtime authority, or sibling owner truth.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. the target package `README.md`
7. the target package `AGENTS.md`
8. `docs/decisions/` for package-creation or package-boundary changes

## Boundaries

- Create packages for live operations, not for decoration.
- Keep source proof objects in `bundles/`.
- Keep quest source records in `quests/<lane>/<state>/` and keep generated
  readers aligned with current source paths.
- Keep generated readers weaker than their builders and source surfaces.
- Keep runtime candidates, receipts, and sibling refs below bundle-local review.
- Preserve legacy names as provenance or accepted inputs, not active topology by
  habit.

## Validation

After package route changes, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run the package-specific builder or check named in the package card.

## Closeout

Report which package operation changed, which source surfaces it routes, which
validators ran, which file movement remains deferred, and which stronger-owner
boundary stayed intact.
