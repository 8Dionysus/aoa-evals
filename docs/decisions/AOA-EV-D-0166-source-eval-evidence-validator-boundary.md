# Source Eval Evidence Validator Boundary

- Decision ID: AOA-EV-D-0166
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_evidence.py`, source eval evidence and review-policy contract guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-object
- Guard families: source/topology
- Posture: active rationale

## Context

`scripts/validators/source_eval_contracts.py` still carried evidence and
review-policy checks after artifact contracts moved out:

- manifest evidence path reachability;
- status-to-portability monotonicity;
- required evidence kinds for bounded, portable, baseline, and canonical
  records;
- `public_safety_reviewed_at` date freshness; and
- comparative-summary support-note interpretation limits.

Those checks are source-fast and bundle-local, but they are not the same
boundary as `EVAL.md` parsing, manifest schema validation, command ownership,
dependency reachability, source tree location, or catalog-record projection
inputs.

## Decision

Source eval evidence and review-policy validation lives in
`scripts/validators/source_eval_evidence.py`.

The module owns:

- bundle-local manifest evidence path checks;
- status/portability monotonicity;
- required evidence-kind checks for promotion status;
- public safety review date shape and future-date rejection; and
- comparative-summary support-note posture for fixed-baseline, peer-compare,
  and longitudinal-window bundles.

`scripts/validators/source_eval_contracts.py` remains the source eval
proof-object orchestrator. It keeps compatibility adapters for existing public
helper names and delegates evidence/review checks to
`source_eval_evidence.py` during bundle validation.

## Rationale

Evidence and review policy protect whether a bundle has enough authored support
to make its status and comparative claims, but they should not define the
bundle's schema meaning or dependency authority.

The split keeps three adjacent questions separate:

- `source_eval_contracts.py`: is the source proof object structurally coherent?
- `source_eval_evidence.py`: is the authored evidence/review posture sufficient
  for the bundle's status and report mode?
- `source_eval_report_artifacts.py`: are materialized report artifacts coherent?
- `source_eval_fixture_contracts.py`: are fixture contracts coherent?
- `source_eval_runner_contracts.py`: are runner contracts coherent?

This prevents source eval validation from regrowing into one historical
validator block.

## Consequences

- Positive: evidence/review-policy checks have a named validator, inventory
  entries, mechanics ledger row, and decision rationale.
- Positive: `source_eval_contracts.py` now delegates authored record structure
  to `source_eval_records.py`, dependency/relation checks to
  `source_eval_references.py`, and evidence/review policy to this module while
  preserving aggregate catalog-record APIs.
- Positive: existing callers can still import evidence helper names from
  `source_eval_contracts.py` through thin compatibility adapters.
- Tradeoff: `source_eval_contracts.py` still calls the evidence validator during
  aggregate bundle validation because a source eval record is incomplete without
  coherent authored evidence.

## Current Applicability

As of 2026-06-04:

- Still valid: source eval bundles must carry evidence that matches status,
  portability, public safety review, and comparative-summary posture.
- Changed: evidence/review-policy logic moved out of
  `source_eval_contracts.py` and into `source_eval_evidence.py`.
- Superseded by: none.

## Boundaries

This decision does not let evidence support notes define `EVAL.md` frontmatter,
`eval.yaml` schema meaning, dependency refs, bundle artifact contracts,
generated reader freshness, release packaging, runtime policy, trace grading, or
eval outcome quality.

It does not move report, fixture, runner, or proof-artifact checks out of their
focused artifact validators.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
