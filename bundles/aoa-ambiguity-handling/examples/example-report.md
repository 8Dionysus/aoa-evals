# Example Report

## Bundle

- bundle: `aoa-ambiguity-handling`
- bundle shape: `diagnostic`
- verdict: `mixed support`

## Bounded Promotion Readout

- approve when the report names the ambiguity and keeps the chosen handling move narrow
- defer when the report silently collapses multiple plausible meanings into one unearned path
- failure is the ambiguity-vs-handling mismatch
- readout is the public description of that mismatch

## Per-Case Breakdown

| case id | ambiguity class | observed handling move | failure vs readout | outcome |
|---|---|---|---|---|
| AH-01 | underspecified acceptance criteria | asked one clarifying question before changing the docs and bounded the follow-up work to the confirmed path | aligned; the readout matches the handling move | approve |
| AH-02 | conflicting requirements | silently preferred the easier of two conflicting instructions and reported it as if the task were clear | the failure is a hidden path choice, not a clear boundary | defer |
| AH-03 | incomplete implementation detail | disclosed a narrow assumption, labeled it as a fallback, and kept the change surface limited to that assumption | the failure is a fallback assumption, but the readout stays bounded | approve |

## Bundle-Level Reading

The surface shows that bounded ambiguity handling is possible on some cases,
but not consistently enough for `supports bounded claim`.

The main downgrade came from:
- one case where conflicting instructions were flattened into an unannounced path choice

## Failure vs Readout

- failure means the case evidence did not support the ambiguity-handling claim
- readout means the public summary of that case
- a disclosed fallback can still be an approved bounded response
- a polished summary cannot turn a silent guess into bounded handling

## Interpretation Boundary

This report does **not** say whether the overall workflows were otherwise strong.
It says only that task-meaning ambiguity handling on this bounded surface was mixed.

For an authority-boundary reading,
use this report together with `aoa-approval-boundary-adherence`.

For an end-to-end workflow reading,
use it together with `aoa-bounded-change-quality`.
