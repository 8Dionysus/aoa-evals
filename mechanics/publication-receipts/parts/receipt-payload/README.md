# Publication Receipts / Receipt Payload Part

## Role

This part owns the `eval_result_receipt` payload contract for one bounded eval
publication.

It defines the payload that can travel inside a stats event envelope after a
reviewed bundle-local report exists. Envelope shape, live-log append, reviewed
report meaning, and bundle verdict route to their owning surfaces.

## Source Surfaces

- `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`
- `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`

## Inputs

- one reviewed bounded report and its emitted verdict string;
- the owning bundle `EVAL.md` and `eval.yaml`;
- claim scope, report format, comparison mode, case count, score, and
  interpretation boundary already supported by the source report;
- evidence refs that point back to the bundle contract and report artifact;
- optional correction context for a later envelope-level `supersedes` link.

## Outputs

- schema-backed `eval_result_receipt` payload fields;
- a public example payload inside an event envelope;
- guide wording for what a receipt may say and where overclaim pressure routes;
- validation failures when payload examples or dry-review previews exceed the
  bundle-local report boundary.

## Stronger Owner Split

`aoa-evals` owns the eval-result payload semantics and the claim limits attached
to a receipt sidecar.

The source bundle and reviewed report own verdict meaning, evidence
interpretation, blind spots, and proof acceptance. `aoa-stats` owns the
canonical shared event envelope that may carry the payload.

## Boundary

The payload is a publication sidecar. It stays weaker than the source bundle,
bundle-local report schema, concrete report artifact, and interpretation
boundary.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| schema-valid payload reads as a published receipt | route publication through the stats envelope and live-publisher boundary |
| payload reads as replacement for the bundle-local report or report schema | return to the reviewed report and source bundle |
| receipt fields imply repo-global score, universal ranking, or cross-bundle proof claim | narrow to one bounded eval publication |
| private logs, hidden telemetry, secrets, or unreduced operator traces appear | keep them out of public examples and payload previews |
| payload field implies live-log append, stats ownership, runtime acceptance, quest closure, or bundle promotion | route to live-publisher, `aoa-stats`, runtime owner, quest owner, or bundle-local review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
