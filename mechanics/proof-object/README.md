# Proof Object Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/proof-object/` routes the operation that keeps source eval package
meaning complete, bounded, and stronger than generated or emitted companions.

It is not the source eval package directory, generated catalog, report sink,
release gate, or doctrine center.

## Owned Operation

`origin proof pressure -> source eval package -> proof-object completeness review -> generated reader derivation -> bundle-local report or downstream route`

The source proof object remains:

- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- bundle-local notes, fixtures, runners, schemas, reports, and examples when
  they exist

This package routes the operation around those objects. It does not move them.

## Source Surfaces

- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- `mechanics/proof-object/PARTS.md`
- `mechanics/proof-object/PROVENANCE.md`
- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
- `mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json`
- `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`
- `docs/ARCHITECTURE.md`
- `docs/EVAL_PHILOSOPHY.md`
- `docs/EVAL_RUBRIC.md`
- `docs/EVAL_REVIEW_GUIDE.md`
- `docs/SCORE_SEMANTICS_GUIDE.md`
- `docs/VERDICT_INTERPRETATION_GUIDE.md`
- `docs/BLIND_SPOT_DISCLOSURE_GUIDE.md`
- `docs/PORTABLE_EVAL_BOUNDARY_GUIDE.md`
- `docs/COMPARISON_SPINE_GUIDE.md`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`

## Inputs

- an origin need, regression pressure, sibling proof reference, runtime
  candidate, quest obligation, or review finding
- one existing eval package or a clearly marked proof-object draft
- manifest metadata from `eval.yaml`
- bounded claim text from `EVAL.md`
- evidence entries, fixtures, examples, reports, schemas, runners, or scorers
  when the eval package claims them
- baseline or comparison posture when the claim depends on comparison

## Outputs

- a reviewable bounded claim
- source-aligned `EVAL.md` and `eval.yaml`
- explicit object under evaluation
- verdict or score logic with interpretation limits
- status and maturity posture
- report contract or support artifact route when needed
- generated reader entries derived from source
- bundle-local review boundary for candidate evidence, reports, and receipts

## Active Parts

- `eval-authoring`: starter scaffold for bounded `EVAL.md` authoring.
- `eval-contracts`: frontmatter and `eval.yaml` schema contracts for source
  proof objects.

## Stronger Owner Split

The proof object may cite skills, techniques, memory surfaces, runtime
artifacts, routing hints, stats envelopes, agent roles, playbooks, or AoA
center law.

Those cited owners keep their stronger truth. The proof object owns only the
bounded claim that local evidence and verdict logic can support.

## Boundaries

- Do not move `evals/` into this package.
- Do not treat this package as permission to promote or deprecate evals by
  route-card edit alone.
- Do not make generated catalogs, capsules, sections, receipts, runtime
  candidates, or sibling refs stronger than bundle-local meaning.
- Do not use one proof object as a universal agent ranking.
- Do not let `status` imply more maturity than the evidence and portability
  checks support.
- Do not hide blind spots behind compact generated readers.

## Lifecycle Posture

The current public maturity vocabulary remains:

- `draft`
- `bounded`
- `portable`
- `baseline`
- `canonical`
- `deprecated`

Status movement must be backed by source evidence, public-safety posture,
portability expectations, comparison contract where relevant, and validation.

This package records the route for lifecycle work. Actual eval status remains
in source eval metadata and must pass repository validation.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package before:

- adding a new bundle;
- changing `eval.yaml` status, category, dependencies, evidence, or comparison
  posture;
- changing a bundle's bounded claim, object under evaluation, scoring logic,
  report contract, blind spots, or interpretation guidance;
- accepting candidate evidence into bundle-local review;
- designing later proof-object completeness validators.
