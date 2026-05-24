# Proof Object Legacy Index

## Role

This index maps old proof-object contract paths to the current active route.

It returns template, schema, and alias questions to active proof-object parts.

## Path Map

| Former path | Current active route | Posture |
| --- | --- | --- |
| `templates/EVAL.template.md` | `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md` | historical root template placement |
| `schemas/eval-frontmatter.schema.json` | `mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json` | historical root schema placement |
| `schemas/eval-manifest.schema.json` | `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json` | historical root schema placement |

## Current Route Expectations

| Pressure | Route |
| --- | --- |
| root template alias | current `eval-authoring` template route |
| root eval schema alias | current `eval-contracts` schema route |
| proof bundle maturity question | bundle-local `EVAL.md`, `eval.yaml`, and review route |

## Validation

Use [AGENTS.md](AGENTS.md#validation).
