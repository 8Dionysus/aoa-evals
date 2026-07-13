# aoa-evals local stats port

This directory exposes statistical questions whose domain meaning belongs to
`aoa-evals`. It uses the shared `aoa-stats` measurement grammar without moving
bundle status meaning or proof authority into the central organ.

## Current reference measurement

| Measurement | Question | Reference value |
| --- | --- | --- |
| `aoa-evals/non-draft-bundle-ratio` | What fraction of source eval bundles have a status other than `draft`? | `12 / 39` at source revision `f8e9a263f6890202a24da0ed4abf313e65e0d919` |

The reference packet is a census of `evals/**/eval.yaml`. It counts the current
source status labels; each bundle remains the owner of what its status and
bounded claim mean.

## Authority

The ratio does not measure eval quality, proof strength, readiness, or verdict
support. `aoa-stats` may validate and compose the packet without turning the
status inventory into a proof conclusion.

## Surfaces

- `port.manifest.json` declares the local question, measurement contract, and
  export.
- `packets/non-draft-bundle-ratio.reference.json` records the evidence-linked
  reference observation.
- `evals/**/eval.yaml` remains the source inventory for bundle status.
