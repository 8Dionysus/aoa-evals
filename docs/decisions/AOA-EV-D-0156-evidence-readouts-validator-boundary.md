# Evidence Readouts Validator Boundary

- Decision ID: AOA-EV-D-0156
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/evidence_readouts.py`, repo-wide and target-eval evidence/readout validation orchestration

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, projection/generated, observability/audit
- Mechanic parents: audit, boundary-bridge, publication-receipts, release-support, titan, cross-parent
- Guard families: projection/generated, runtime-policy route, observability/audit, release/nightly
- Posture: active rationale

## Context

After the root context and mechanics route-domain splits,
`scripts/validate_repo.py` still carried the repo-wide and target-eval readout
domain: runtime audit context, generated read-model context, JSON read helper,
runtime evidence selection, runtime integrity review, receipt and live-log
checks, release-support audit reports, runtime candidate readers, report index
parity, phase-alpha matrix parity, Titan canary checks, and generated catalog,
capsule, section, and comparison-spine parity.

That domain was not CLI behavior. It was evidence/readout orchestration sitting
in the command entrypoint because the historical root validator had accumulated
every gate.

## Decision

Repo-wide and target-eval readout orchestration lives in
`scripts/validators/evidence_readouts.py`.

The module owns:

- runtime audit context construction from `root_context.py`;
- generated read-model context construction from source eval contract builders;
- catalog JSON parse issue adaptation into `ValidationIssue`;
- repo-wide readout validation across runtime audit, publication receipts,
  release support, runtime candidate readers, report index, phase-alpha matrix,
  Titan canaries, and generated read models;
- target-eval readout validation for runtime evidence selection and generated
  read-model parity.

`scripts/validate_repo.py` remains the CLI entrypoint. It discovers source eval
records and calls the readout orchestrator when the selected validation scope
requires readout checks.

## Rationale

Evidence/readout checks verify projections, runtime-adjacent audit surfaces,
receipt/release support artifacts, and target-eval readout freshness. They do
not define source proof meaning or accept live runtime outcomes.

Moving the orchestration out of the CLI keeps source record discovery separate
from readout validation, and it gives runtime/generated/release readout checks a
single named owner without turning generated validators into source meaning
owners.

## Consequences

- Positive: `scripts/validate_repo.py` no longer owns runtime audit context,
  generated read-model context, repo-wide readout orchestration, target-eval
  readout orchestration, or catalog JSON parse adaptation.
- Positive: runtime evidence tests import the readout context owner directly.
- Positive: generated parity remains focused on projection rules while this
  module wires the context needed for repo-wide and target-eval runs.
- Tradeoff: this module intentionally imports several focused validators; new
  rule meaning must stay in those focused modules or owning mechanic surfaces.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  command and source eval scope selector.
- Changed: evidence/readout context construction and repo-wide/target-eval
  readout orchestration moved to `scripts/validators/evidence_readouts.py`.
- Superseded by: none.

## Boundaries

This decision does not let `evidence_readouts.py` define source eval contracts,
generated source meaning, runtime policy acceptance, trace/eval grading, live
receipt publication truth, release artifact identity, sibling compatibility
truth, or mechanic payload meaning.

It is an orchestration boundary for evidence/readout validators, not a new
release gate or a replacement for generated builders.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/evidence_readouts.py tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py tests/test_generated_parity.py tests/test_report_schema_contracts.py`
