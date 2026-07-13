# Output Process Bridge Precondition

- Decision ID: AOA-EV-D-0242
- Status: Accepted
- Date: 2026-06-16
- Owner surface: `EVAL_SELECTION.md`

## Index Metadata

- Original date: 2026-06-16
- Surface classes: root chooser, public contract, validation guard
- Mechanic parents: comparison-spine
- Guard families: source doctrine, comparison, artifact/process
- Posture: active rationale

## Context

PR #384 changed the public `aoa-output-vs-process-gap` chooser precondition
from a loose alternative route that allowed frozen-baseline comparison to stand
beside artifact and workflow readings, into a stricter bridge rule: both
standalone artifact review and standalone workflow review must be visible under
matched conditions before the bridge is used.

That PR was authored and merged by `8Dionysus`, but the diff did not include a
recoverable decision note or approval artifact. Codex review thread
`PRRT_kwDORq8AFs6JbX-4` correctly flagged that future agents would not be able
to distinguish approved route correction from comparison-ladder drift.

## Options Considered

- Revert the PR #384 chooser precondition until another explicit approval is
  gathered.
- Keep the landed route and add no durable rationale.
- Keep the landed route and record the rationale, source surfaces, and
  boundaries in the decision lane.

## Decision

Keep the landed PR #384 route and make it durable through this decision note.

`aoa-output-vs-process-gap` is a bridge only after both standalone artifact
review and standalone workflow review have made paired surfaces visible under
matched conditions. Frozen-baseline comparison remains routed to
`aoa-regression-same-task`; it does not satisfy the artifact/process bridge
precondition by itself.

## Rationale

The stricter precondition preserves the proof boundary between three different
questions:

- whether the produced artifact holds up;
- whether the workflow process holds up;
- whether polished output is diverging from process discipline on matched
  cases.

Letting a frozen-baseline comparison substitute for either standalone reading
would make the bridge easier to invoke before the paired evidence exists. The
landed wording keeps `aoa-output-vs-process-gap` below the two readings it
compares, while keeping baseline comparison in its own public chooser route.

## Consequences

- Positive: future agents have a visible rationale for the public chooser
  wording changed by PR #384.
- Positive: validator wording can protect the real bridge-precondition drift
  without treating unrelated `for baseline comparison` guidance as a violation.
- Tradeoff: this note records a post-review rationale for an already merged
  human-authored change; it is not a new blanket approval for future public
  chooser changes.
- Follow-up: future changes to default public baseline or comparison-ladder
  wording still need explicit operator confirmation or a fresh decision note in
  the same slice.

## Current Applicability

As of 2026-06-16:

- Still valid: `aoa-output-vs-process-gap` requires both standalone artifact
  and workflow readings under matched conditions.
- Changed: PR #384's chooser wording now has a durable decision route.
- Superseded by: none.

## Review Log

### 2026-06-16 - Codex review follow-up

- Previous assumption: the PR #384 diff was enough to explain why the bridge
  precondition changed.
- New reality: review thread `PRRT_kwDORq8AFs6JbX-4` showed that the public
  chooser route needed a visible rationale artifact.
- Reason: root `AGENTS.md` treats public baseline and comparison-ladder wording
  as approval-gated.
- Source surfaces updated: this decision note, generated decision indexes,
  source doctrine validator, and focused comparison-surface tests.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

Do not infer that this decision approves any future public chooser,
comparison-ladder, baseline-mode, category, report-format, or starter-selection
change.

Do not infer that `aoa-output-vs-process-gap` proves artifact quality,
workflow quality, or regression truth by itself. It only compares the paired
artifact-side and process-side readings after they already exist.

Do not infer that frozen-baseline comparison is deprecated. It remains owned by
`aoa-regression-same-task`.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
