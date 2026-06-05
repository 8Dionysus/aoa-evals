# Phase Alpha Matrix Aggregate Removal

- Decision ID: AOA-EV-D-0207
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused Phase Alpha matrix validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, generated/readout, boundary/runtime/sibling
- Mechanic parents: boundary-bridge, cross-parent
- Guard families: generated/report/receipt/runtime, sibling and boundary
- Posture: active rationale

## Context

AOA-EV-D-0119 moved Phase Alpha eval matrix validation out of root validation
and into `scripts/validators/phase_alpha_matrix.py`.

That module still mixed three surfaces:

- shared JSON/schema, repo-ref, support-ref, and builder loading helpers;
- local generated matrix schema/runtime-lane projection checks; and
- strict `aoa-playbooks` sibling compatibility, rebuild parity, run alignment,
  and support-ref checks.

The local generated projection and strict sibling compatibility are related,
but they have different repair routes and different runtime posture. The local
projection can run without the sibling checkout. Strict compatibility is only
valid when the sibling source is available and explicitly enabled.

## Decision

`scripts/validators/phase_alpha_matrix.py` is removed.

Phase Alpha matrix validation now routes through focused modules:

- `phase_alpha_matrix_projection.py` owns local generated matrix object shape,
  schema validity, schema conformance, and runtime-lane posture.
- `phase_alpha_matrix_sibling_compat.py` owns strict sibling compatibility:
  builder parity, `aoa-playbooks` run alignment, support-ref resolution, and
  strict sibling root availability.
- `phase_alpha_matrix_common.py` is helper-only JSON/schema, repo-ref,
  support-ref, path, and builder loading support.

`evidence_readouts.py` calls projection validation and sibling compatibility
validation separately.

## Rationale

Generated validators should make projection drift visible without silently
requiring sibling state. Sibling compatibility should remain a stronger,
explicit mode that checks the playbooks source of truth and support refs.

Keeping both surfaces behind one aggregate hid that distinction and made a
generated read-model validator look like a broad sibling boundary owner.

## Consequences

- Positive: no Phase Alpha matrix aggregate validator remains.
- Positive: local generated matrix failures and strict sibling failures now
  name separate owner modules.
- Positive: strict sibling compatibility can remain opt-in without weakening
  local generated checks.
- Tradeoff: `evidence_readouts.py` imports two focused Phase Alpha validators.

## Current Applicability

As of 2026-06-04:

- Still valid: `aoa-playbooks` owns Phase Alpha run truth, reviewed-run refs,
  and scenario composition.
- Changed: Phase Alpha matrix behavior no longer lives in
  `phase_alpha_matrix.py`; it is split across local projection, strict sibling
  compatibility, and helper-only modules.
- Supersedes: the aggregate module shape left by AOA-EV-D-0119.

## Boundaries

This decision does not make the generated matrix a verdict, acceptance record,
receipt, or runtime policy decision.

It does not authorize sibling repository edits.

It does not turn strict sibling compatibility into the default source-fast
posture.

It does not create a replacement Phase Alpha matrix aggregate under another
name.

## Validation

- `python -m py_compile scripts/validators/phase_alpha_matrix_common.py scripts/validators/phase_alpha_matrix_projection.py scripts/validators/phase_alpha_matrix_sibling_compat.py scripts/validators/evidence_readouts.py tests/test_downstream_feed_contracts.py`
- `python -m pytest -q tests/test_downstream_feed_contracts.py -k phase_alpha`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py tests/test_validate_repo.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
