# AGENTS.md

## Applies to

Everything under `stats/` in `aoa-evals`.

## Role

This directory owns eval-local statistical questions, their embedded
measurement contracts, and evidence-linked reference packets. Shared
statistical grammar and cross-owner composition remain owned by `aoa-stats`.

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
## Boundaries

- `port.manifest.json` owns the eval-local question and measurement meaning.
- Reference packets are derived snapshots and remain weaker than bundle-local
  `eval.yaml`, `EVAL.md`, reports, and verdict review.
- A status ratio describes source labels only. It is not a proof verdict,
  quality score, readiness claim, or comparison baseline.
- Keep packet refs repository-relative and keep fixture or report content out
  of the packet.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Inspect the owner evidence first:

Then validate the port and its referenced packets with the central owner:

## Closeout

Report the question or contract changed, the source status inventory inspected,
whether the reference packet was refreshed, and which validation route ran.
