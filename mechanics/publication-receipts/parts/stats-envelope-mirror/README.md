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

This local mirror supports `aoa-evals` validation only. It does not define the
cross-repo event vocabulary.

`aoa-evals` owns only the eval-result payload semantics and local receipt
subordination checks.

## Stop-Lines

- Do not edit this mirror as if it were the canonical `aoa-stats` schema.
- Do not add event kinds for local convenience without current canonical owner
  alignment.
- Do not use envelope validation as proof acceptance, runtime acceptance, or
  bundle promotion.
- Do not turn dry-review artifacts into publishable envelope records.
- Do not read or publish raw live receipt log content for docs-only or
  route-card-only changes.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
