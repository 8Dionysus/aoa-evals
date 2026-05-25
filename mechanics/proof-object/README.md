# Proof Object Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/proof-object/` routes the operation that keeps source eval package
meaning complete, bounded, and stronger than generated or emitted companions.

Source eval packages stay under `evals/`; generated catalogs, reports, release
gates, and doctrine surfaces keep their own roles. This package keeps the
authoring, contract, completeness, lifecycle, and generated-reader derivation
route clear around source proof objects.

## Owned Operation

`origin proof pressure -> source eval package -> proof-object completeness review -> generated reader derivation -> bundle-local report or downstream route`

The source proof object remains:

- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- bundle-local notes, fixtures, runners, schemas, reports, and examples when
  they exist

This package routes the operation around those objects. Source eval packages
stay under `evals/`.

## Source Surfaces

- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- `mechanics/proof-object/PARTS.md`
- `mechanics/proof-object/PROVENANCE.md`
- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
- `mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json`
- `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`
- `docs/architecture/ARCHITECTURE.md`
- `docs/guides/EVAL_PHILOSOPHY.md`
- `docs/guides/EVAL_RUBRIC.md`
- `docs/guides/EVAL_REVIEW_GUIDE.md`
- `docs/guides/SCORE_SEMANTICS_GUIDE.md`
- `docs/guides/VERDICT_INTERPRETATION_GUIDE.md`
- `docs/guides/BLIND_SPOT_DISCLOSURE_GUIDE.md`
- `docs/guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md`
- `docs/guides/COMPARISON_SPINE_GUIDE.md`
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

| Pressure | Route |
| --- | --- |
| source eval package movement appears | keep source eval packages under `evals/` and route support work through this package |
| route-card edit appears to promote or deprecate an eval | route lifecycle movement through source metadata, review evidence, and validation |
| generated catalog, capsule, section, receipt, runtime candidate, or sibling ref appears stronger than bundle meaning | return to bundle-local `EVAL.md`, `eval.yaml`, and review evidence |
| one proof object reads like a universal agent ranking | narrow it to the bounded claim and comparison posture named by the source package |
| `status` reads stronger than evidence or portability checks | route status movement through source evidence, public-safety posture, portability, comparison, and validation |
| compact generated reader hides blind spots | return to source blind spots and interpretation guidance |

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
