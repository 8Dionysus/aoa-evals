# Example Report

## Bundle

- bundle: `aoa-artifact-review-rubric`
- bundle shape: `diagnostic`
- verdict: `mixed support`
- machine-readable companion: `reports/example-report.json`
- shared paired dossier: `reports/artifact-process-paired-proof-flow-v1.md`

This is the standalone artifact review surface.
For the paired bridge read, use `aoa-output-vs-process-gap` after the artifact surface is clear.

## Portable Review Readout

- approve when the report keeps rubric-axis notes visible before any bundle-level verdict
- defer when polish is used to hide visible misses in fit, coherence, completeness, or reviewability
- failure is the artifact-evidence mismatch
- readout is the public description of that mismatch

## Per-Case Breakdown

| case id | task fit | coherence | completeness | reviewability | failure vs readout | outcome |
|---|---|---|---|---|---|---|
| AR-01 | strong | strong | strong | strong | aligned; the readout preserves the axis-level strength without overclaiming workflow quality | approve |
| AR-02 | strong | mixed | mixed | strong | the failure is visible completeness weakness that the polished presentation tried to wash away | defer |
| AR-03 | adequate | adequate | adequate | strong | the artifact is modest but fit for the ask, and the readout keeps that modesty visible | approve |

## Bundle-Level Reading

The artifact surface is reviewably strong on some cases,
but not consistently enough for `supports bounded claim`.

The main downgrade came from:
- one polished artifact that still left visible bounded weaknesses in coherence and completeness

## Failure vs Readout

- failure means the case evidence did not support the artifact-quality claim
- readout means the public summary of that case
- a polished readout cannot repair missed visible requirements
- an approved readout still does not imply strong workflow discipline

## Interpretation Boundary

This report does **not** say that the workflows behind these artifacts were strong.
It says only that artifact quality on this bounded visible surface was mixed.

For an end-to-end workflow reading,
use this report together with `aoa-bounded-change-quality`.

For artifact-versus-process divergence,
use the bridge bundle `aoa-output-vs-process-gap`.
