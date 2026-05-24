# Proof Object / Parts Route

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for proof-object authoring and contract support parts |
| input | eval authoring pressure, source metadata contract pressure, template route question, schema route question, or generated-reader drift |
| output | active part route, source proof-object support surface, validation lane, or bundle-local review handoff |
| owner | `mechanics/proof-object/parts/AGENTS.md` for part-lane law; part README for local contract; source eval bundle for proof meaning |
| next route | parent [README](../README.md), [PARTS](../PARTS.md), part README, source `evals/**/EVAL.md` and `evals/**/eval.yaml`, and [proof-object AGENTS validation](../AGENTS.md#validation) |
| validation | `mechanics/proof-object/AGENTS.md#validation`, focused validator tests, and generated-reader freshness checks when source or generated readers move |

The proof-object parts support source eval packages. Source proof meaning stays
with `evals/**/EVAL.md` and `evals/**/eval.yaml`; generated readers stay
derived from source packages.

## Active Parts

| Part | Route |
| --- | --- |
| `eval-authoring/` | starter template for bounded eval package authoring |
| `eval-contracts/` | schema-backed frontmatter and manifest contracts |

## Part Admission Route

A new proof-object part enters this index when the work has a distinct
support operation around source eval packages, a source surface set, a
stronger-owner split, and reachable validation from the proof-object AGENTS
lane.

| Field | Required route |
| --- | --- |
| source surface | template, schema, source-bundle support file, generated-reader input, or validation contract owned together |
| operation | one bounded proof-object support operation around eval authoring, contracts, completeness, or derived-reader parity |
| owner boundary | source eval bundles keep proof meaning; generated readers and reports stay weaker than bundle-local review |
| next route | parent `PARTS.md`, parent `DIRECTION.md`, part README, affected source bundle, and generated-reader check when applicable |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
parts index names the active parts and their roles; the parts route card owns
the command lane.
