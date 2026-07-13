# AGENTS.md

## Applies to

Everything under `stats/` in `aoa-evals`.

## Role

This directory owns eval-local statistical questions, their embedded
measurement contracts, and evidence-linked reference packets. Shared
statistical grammar and cross-owner composition remain owned by `aoa-stats`.

## Read before editing

1. Root `AGENTS.md`, `DESIGN.md`, and the proof boundary docs they route to.
2. `stats/README.md` and `stats/port.manifest.json`.
3. The referenced source eval bundles and status fields.
4. The central measurement and packet contracts under `aoa-stats/stats/`.

## Boundaries

- `port.manifest.json` owns the eval-local question and measurement meaning.
- Reference packets are derived snapshots and remain weaker than bundle-local
  `eval.yaml`, `EVAL.md`, reports, and verdict review.
- A status ratio describes source labels only. It is not a proof verdict,
  quality score, readiness claim, or comparison baseline.
- Keep packet refs repository-relative and keep fixture or report content out
  of the packet.

## Validation

Inspect the owner evidence first:

```bash
rg -N '^status: ' evals -g 'eval.yaml' | sort
```

Then validate the port and its referenced packets with the central owner:

```bash
python scripts/validate_local_stats_port.py
```

## Closeout

Report the question or contract changed, the source status inventory inspected,
whether the reference packet was refreshed, and which validation route ran.
