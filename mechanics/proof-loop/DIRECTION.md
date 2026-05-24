# Proof Loop Direction

Proof Loop in `aoa-evals` should make one local proof question travel to one
bounded result without importing authority from machine, runtime, sibling, or
receipt layers.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-loop route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active proof-loop part map.
- `parts/`: route-smoke support and reports.
- `PROVENANCE.md`: controlled bridge from active route to old proof-loop report placement.
- `legacy/`: archive-local route for old proof-loop report placement after
  `PROVENANCE.md`.
- owning packages: source truth for each step in the loop.

## Current contour

- Keep the loop routeable: selection, source proof object, support contract,
  candidate evidence, bundle-local review, bounded report, optional receipt.
- Keep each step owned by the package that actually owns it.
- Keep route-smoke as routeability proof, not bundle promotion.

## Growth rule

Add a proof-loop part only when a recurring loop step needs proof-side support
that is not already owned by proof-object, audit, receipts, comparison,
release-support, or another mechanic.

## Stop-lines

- Do not turn proof-loop into a bundle, report directory, runtime intake,
  questbook, receipt publisher, or release process.
- Do not claim proof completion from routeability alone.

## Validation

Use the validation lane in [mechanics/proof-loop/AGENTS.md](AGENTS.md#validation).
