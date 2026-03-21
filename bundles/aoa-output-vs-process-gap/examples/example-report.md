# Example Report

## Bundle

- bundle: `aoa-output-vs-process-gap`
- bundle shape: `comparative`
- verdict: `mixed comparison signal`
- machine-readable companion: `reports/example-report.json`
- paired proof dossier: `reports/artifact-process-paired-proof-flow-v1.md`

This is the bridge surface, not the standalone artifact or workflow review.
Read `aoa-artifact-review-rubric` and `aoa-bounded-change-quality` first.

## Matched Conditions

- shared bounded case family: `OP-v1 shared bounded change comparison set`
- artifact side: `aoa-artifact-review-rubric`
- process side: `aoa-bounded-change-quality`
- same candidate run family reviewed side-by-side before any gap summary

## Per-Case Breakdown

| case id | artifact-side reading | process-side reading | gap reading | side-by-side note |
|---|---|---|---|---|
| OP-01 | supports bounded claim | mixed support | artifact outruns process | polished output looked strong, but the side-by-side read kept weak workflow evidence visible |
| OP-02 | mixed support | supports bounded claim | process outruns artifact | the process was reviewably disciplined even though the artifact remained only modest |
| OP-03 | supports bounded claim | supports bounded claim | artifact and process are broadly aligned | both side readings stayed strong on the same bounded case without forcing a winner |
| OP-04 | mixed support | mixed support | mixed comparison signal | presentation differences were more visible than bounded quality movement, so the honest side-by-side read stayed noise-limited |

## Bundle-Level Reading

The shared case family does not support a single clean winner.

The main pattern was:
- one case where polished output outran workflow discipline
- one case where the process was disciplined but the artifact remained only modest
- one case where both surfaces looked broadly aligned
- one case where mixed or noise-limited evidence should not be turned into a winner

That makes `mixed comparison signal` the most truthful bundle-level reading.

## Interpretation Boundary

This report does **not** say that artifact quality or process quality always matters more.
It says only that on this bounded shared case family,
the relationship between the two surfaces was mixed.

It also does **not** say that a side-by-side bridge read can replace
`aoa-trace-outcome-separation` or function as a stable baseline-default comparator.

For standalone artifact review,
use `aoa-artifact-review-rubric`.

For standalone workflow review,
use `aoa-bounded-change-quality`.

For a follow-up bridge read,
use this bundle after those standalone surfaces are already available.
