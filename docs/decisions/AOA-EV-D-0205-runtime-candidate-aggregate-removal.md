# Runtime Candidate Aggregate Removal

- Decision ID: AOA-EV-D-0205
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused runtime-candidate generated reader validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, generated/readout
- Mechanic parents: audit, checkpoint, cross-parent
- Guard families: generated/report/receipt/runtime, runtime-candidate/read-model
- Posture: active rationale

## Context

AOA-EV-D-0118 moved runtime-candidate reader checks out of root validation and
into `scripts/validators/runtime_candidates.py`.

That module still mixed three surfaces:

- JSON/schema/builder helper loading;
- runtime candidate template-index rebuild and source-example parity; and
- runtime candidate intake rebuild, review-ref, and candidate-posture parity.

The template index and intake reader are generated projections over related
source examples, but they fail through different read-model repair routes.

## Decision

`scripts/validators/runtime_candidates.py` is removed.

Runtime-candidate generated reader validation now routes through focused
modules:

- `runtime_candidate_common.py` is helper-only JSON/schema, constants, and
  builder loading.
- `runtime_candidate_template_index.py` owns template-index schema, rebuild
  parity, source example coverage, eval-anchor resolution, artifact
  normalization, and source-example field parity.
- `runtime_candidate_intake.py` owns intake rebuild parity, source-of-truth map,
  template ordering, review-guide refs, owner-review refs, and
  `candidate_until_eval_review` posture.

`evidence_readouts.py` calls the focused validators directly.

## Rationale

Generated validators should check projection parity, not become broad runtime
or audit buckets. Template-index parity proves that source examples and eval
anchors are represented. Intake parity proves that reviewed candidate packets
carry the expected review refs and candidate posture.

Keeping both behind one aggregate made it too easy to add runtime-policy or
acceptance checks to a generated read-model validator.

## Consequences

- Positive: no runtime-candidate aggregate validator remains.
- Positive: template-index and intake failures name the generated surface that
  drifted.
- Positive: inventories and evidence ledger no longer present generated
  candidate readers as one mixed owner surface.
- Tradeoff: `evidence_readouts.py` imports two focused generated validators.

## Current Applicability

As of 2026-06-04:

- Still valid: runtime-candidate readers remain candidate-only generated
  read-models below bundle-local review.
- Changed: runtime-candidate behavior no longer lives in
  `runtime_candidates.py`; it is split across template-index, intake, and
  helper-only modules.
- Supersedes: the aggregate module shape left by AOA-EV-D-0118.

## Boundaries

This decision does not change runtime policy, receipt publication, artifact
verdict authority, bundle-local proof meaning, or human review requirements.

It does not create a replacement runtime-candidate aggregate under another
name.

## Validation

- `python -m py_compile scripts/validators/runtime_candidate_common.py scripts/validators/runtime_candidate_template_index.py scripts/validators/runtime_candidate_intake.py scripts/validators/evidence_readouts.py tests/test_quest_and_reader_surfaces.py`
- `python -m pytest -q tests/test_quest_and_reader_surfaces.py -k runtime_candidate`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py tests/test_validate_repo.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
