# Publication Receipts / Stats Envelope Mirror Part

## Role

This part owns the local validation mirror for the shared stats event envelope
used by eval-result receipts.

It lets `aoa-evals` validate receipt envelopes locally while keeping the shared
cross-repo event vocabulary with `aoa-stats`.

## Source Surfaces

- `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json`

## Inputs

- the canonical `aoa-stats` event-envelope contract and event-kind vocabulary;
- local `eval_result_receipt` payload validation needs;
- owner-local live receipt log entries that must validate against the mirrored
  envelope shape;
- dry-review evidence that must remain outside publishable envelope form.

## Outputs

- local JSON Schema mirror for stats event envelopes;
- validation support for `eval_result_receipt` live-log entries;
- explicit metadata naming `aoa-stats` as canonical owner;
- failures when envelope entries drift from required event fields, datetime
  format, object refs, evidence refs, or payload shape.

## Stronger Owner Split

The canonical owner remains `aoa-stats` at
`repo:aoa-stats/schemas/stats-event-envelope.schema.json`.

This local mirror supports `aoa-evals` validation only. Cross-repo event
vocabulary routes to the canonical `aoa-stats` owner.

`aoa-evals` owns only the eval-result payload semantics and local receipt
subordination checks.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| mirror edit reads as canonical `aoa-stats` schema work | route canonical schema meaning to `aoa-stats` |
| local convenience wants a new event kind | align with the canonical owner before local mirror changes |
| envelope validation reads as proof acceptance, runtime acceptance, or bundle promotion | return to bundle-local review, runtime owner, and lifecycle route |
| dry-review artifacts read as publishable envelope records | route to intake dry review until publication is intentionally invoked |
| raw live receipt log content appears in docs-only or route-card-only work | leave raw log content outside the docs route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
