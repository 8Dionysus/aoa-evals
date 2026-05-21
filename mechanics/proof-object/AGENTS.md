# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/proof-object/DIRECTION.md` for current operating direction, `mechanics/proof-object/PARTS.md` for active parts, and `mechanics/proof-object/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/proof-object/` and proof-object route guidance.

## Role

This package routes source proof-object work for eval bundles.

It does not own the actual bundle meaning. Bundle meaning stays in
`bundles/*/EVAL.md` and `bundles/*/eval.yaml`, with bundle-local support
artifacts where present.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `docs/decisions/0002-proof-object-authority-contract.md`
6. `mechanics/README.md`
7. `mechanics/proof-object/README.md`
8. `mechanics/proof-object/PARTS.md`
9. `mechanics/proof-object/PROVENANCE.md`
10. affected `bundles/*/EVAL.md` and `bundles/*/eval.yaml`
11. `mechanics/proof-object/parts/bundle-authoring/templates/EVAL.template.md` when authoring or reshaping bundle anatomy
12. `mechanics/proof-object/parts/bundle-contracts/schemas/eval-frontmatter.schema.json`
13. `mechanics/proof-object/parts/bundle-contracts/schemas/eval-manifest.schema.json`
14. `docs/decisions/0048-proof-object-contract-parts.md`

## Local Law

- Keep source proof objects stronger than generated readers, reports,
  receipts, runtime candidates, and sibling refs.
- Keep EVAL.md and eval.yaml aligned when claim, object under evaluation,
  status, baseline mode, comparison surface, dependencies, evidence, or report
  contract changes.
- Keep blind spots and interpretation limits explicit.
- Keep comparison claims tied to comparison posture.
- Keep status movement evidence-backed.
- Route skill, technique, memory, runtime, routing, stats, role, playbook, and
  AoA law meaning back to stronger owners.

## Boundaries

- Do not move `bundles/` into `mechanics/proof-object/`.
- Keep former root template and schema aliases as historical compatibility
  vocabulary; the active template and schema surfaces are mechanic-local.
- Do not hand-edit generated reader surfaces as proof authority.
- Do not promote a candidate, receipt, or report into accepted verdict meaning
  without bundle-local review.
- Do not make this package a bundle registry or release note surface.
- Do not use one proof object as a universal agent ranking.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```

If the change touches generated runtime candidate, quest, comparison, receipt,
or phase-alpha surfaces, also run the owning builder or validator.

## Closeout

Report which proof-object route changed, which source bundle or source class it
routes, whether `EVAL.md` and `eval.yaml` alignment changed, which generated
readers were checked, what validation ran, and what proof claim remains
bounded.
