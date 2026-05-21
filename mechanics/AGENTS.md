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
5. `mechanics/EVIDENCE_CLUSTERS.md`
6. `mechanics/README.md`
7. the target package `README.md`
8. the target package `DIRECTION.md` for current operating direction
9. the target package `AGENTS.md`
10. `docs/decisions/` for package-creation or package-boundary changes

## Boundaries

- Create packages for live operations, not for decoration.
- Use `mechanics/EVIDENCE_CLUSTERS.md` before turning a form, report, canary,
  or old path family into a parent mechanic.
- Top-level parent directories are validator allowlisted. Do not add
  `mechanics/<new-parent>/` without updating the evidence cluster, package
  route cards, topology docs, decision record, and validator in the same slice.
- Keep source proof objects in `evals/`.
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

If the changed package touches generated quest readers, catalogs, report
indexes, runtime-candidate readers, or boundary-bridge matrices, add the owning
builder check named by the package card, commonly:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
```

Run package-specific builders or checks named in the package card before the
broader mechanics lane.

## Closeout

Report which package operation changed, which source surfaces it routes, which
validators ran, which file movement remains deferred, and which stronger-owner
boundary stayed intact.
