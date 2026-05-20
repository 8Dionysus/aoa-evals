# 0023 Eval Report Index Reader

## Status

Accepted.

## Context

`aoa-evals` now has multiple real bundle-local `*.report.json` artifacts.
They are validated against bundle-local report schemas, but without a compact
reader a future agent must search the file tree to find actual reports.

The first proof-loop bundle-local report made that gap sharper: routeability
needs a reader, while proof authority must stay with the source report and
source bundle.

## Decision

Add `generated/eval_report_index.min.json` as a derived reader over
`bundles/*/reports/*.report.json`.

Build it with `scripts/generate_eval_report_index.py`. The index records report
location, bundle, schema, verdict string, case family, claim boundary,
limitations count, and explicit non-receipt posture.

`scripts/validate_repo.py` validates the generated reader against the builder
and checks that every indexed entry remains subordinate:

- source report paths must exist;
- report fields must match the source report;
- bundle and status must match `eval.yaml`;
- `receipt_status` must stay `not_a_receipt`;
- the authority boundary must say the index is derived only.

## Non-Goals

- no report verdict is promoted into generated authority;
- no eval result receipt is published;
- no bundle status changes;
- no runtime candidate is accepted;
- no hidden proof-loop dispatch is created;
- no report is moved out of its owning bundle.

## Consequences

The active proof loop gains a routeable report reader without moving report
meaning into generated output. Readers can find actual reports quickly, but
must still open the source report and bundle before interpreting the verdict.

Release checks now include the report-index `--check` step so generated report
route drift is caught alongside catalog drift.

## Validation

Expected checks:

- `python scripts/generate_eval_report_index.py --check`
- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_downstream_feed_contracts.py tests/test_validate_repo.py -k "eval_report_index or downstream"`
- broad repository checks before closeout.
