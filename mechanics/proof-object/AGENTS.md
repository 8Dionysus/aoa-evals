# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/proof-object/DIRECTION.md`, `mechanics/proof-object/PARTS.md`, and `mechanics/proof-object/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/proof-object/` and proof-object route guidance.

## Role

This package routes source proof-object work for source eval packages.

It maps authoring pressure, schema contracts, generated catalog checks, and
bundle-local review back to the source proof objects in `evals/**/EVAL.md` and
`evals/**/eval.yaml`. Eval-local support artifacts stay with the bundle where
present.

## Operating Card

| Field | Route |
| --- | --- |
| role | source proof-object route for eval packages |
| input | eval authoring changes, claim or metadata movement, schema pressure, generated catalog drift, and eval-local support artifacts |
| output | source eval update, template/schema route, generated catalog check, or bundle-local review handoff |
| owner | source proof bundle owns meaning; this package owns proof-object authoring and contract routes |
| next route | `mechanics/proof-object/README.md`, `DIRECTION.md`, `PARTS.md`, `PROVENANCE.md`, affected `evals/**/EVAL.md`, and affected `evals/**/eval.yaml` |
| tools | `validate_repo.py`, `build_catalog.py --check`, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Owner Routes

| Need | Owner route |
| --- | --- |
| source proof object meaning | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| authoring template | `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md` |
| schema-backed eval contract | `mechanics/proof-object/parts/eval-contracts/schemas/` |
| generated catalog or capsule drift | source bundle plus the local validation route |
| historical aliases or former placement | `mechanics/proof-object/PROVENANCE.md` and archive-local legacy surfaces |
| reports, receipts, runtime candidates, or sibling refs | the stronger owner named by the affected surface before proof adoption |

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
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

Each package keeps current operating direction in `DIRECTION.md`; the active-to-archive bridge in `PROVENANCE.md` is consulted only when legacy names are involved.

## Route Rules

- Source eval packages stay under `evals/`.
- Keep former root template and schema aliases as historical compatibility
  vocabulary; the active template and schema surfaces are mechanic-local.
- Check generated reader surfaces against source proof objects and builders.
- Promote candidate, receipt, or report meaning only through bundle-local
  review.
- Route eval registry and release-note questions to their owning surfaces.
- Treat one proof object as bounded evidence for its claim and comparison
  posture.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Run the narrow package route checks:

If the change touches generated runtime candidate, quest, comparison, receipt,
or phase-alpha surfaces, also run the owning builder or validator.

## Closeout

Report which proof-object route changed, which source eval package or source class it
routes, whether `EVAL.md` and `eval.yaml` alignment changed, which generated
readers were checked, what validation ran, and what proof claim remains
bounded.
