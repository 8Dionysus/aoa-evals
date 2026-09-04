# AGENTS.md

## Applies to

This card applies to `aoa-evals/kag/` and every nested path until a nearer card
narrows the lane.

## Role

`kag/` is the local KAG provider home for `aoa-evals`. It exposes compact,
source-linked records over `eval bundles and proof report index` for `aoa-kag` registry,
composition, and MCP consumers.

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
For provider records, consult `kag/manifest.json` and the generated/eval source routes only when the touched record needs them.

## Boundaries

Keep authored meaning with `aoa-evals` source surfaces. Keep shared KAG schema,
registry, composition, and provider validation with `aoa-kag`. Keep runtime
serving state with `abyss-stack` or the runtime owner named by the consumer.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Use the owner validator named in `manifest.json`, then validate this provider
through the `aoa-kag` local subtree validator.

## Closeout

Report provider records changed, source-return route changed, owner validation,
`aoa-kag` validation, and the next MCP consumer route.
