# Source Doctrine Aggregate Removal

- Decision ID: AOA-EV-D-0209
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused source doctrine validators and `source_eval_domains.py`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, comparison/readout, report/readout
- Mechanic parents: proof-object, comparison-spine, proof-infra, audit, cross-parent
- Guard families: source/topology, generated/readout
- Posture: active rationale

## Context

AOA-EV-D-0125 moved authored-source doctrine checks out of
`scripts/validate_repo.py` into `scripts/validators/source_doctrine.py`. That
module then became the broad owner for comparison doctrine, artifact/process
doctrine, repeated-window doctrine, and integrity taxonomy checks.

Those surfaces all protect authored source meaning, but their failure routes are
different. A missing comparison selector question should not route through the
same validator owner as an integrity risk taxonomy enum drift or a
repeated-window guide wording issue.

## Options Considered

- Keep `source_doctrine.py` as a single doctrine owner.
- Keep `source_doctrine.py` as a facade that delegates to focused modules.
- Remove the aggregate and let `source_eval_domains.py` orchestrate focused
  doctrine validators directly.

## Decision

`scripts/validators/source_doctrine.py` is removed.

Active source doctrine validation now routes through focused modules:

- `source_comparison_doctrine.py` owns comparison guide, README/docs route text,
  selector questions, and comparison index posture.
- `source_artifact_process_doctrine.py` owns artifact/process guide, selector
  and index wording, and relevant bundle phrasing.
- `source_repeated_window_doctrine.py` owns repeated-window guide, selector and
  index wording, and longitudinal bundle phrasing.
- `source_integrity_taxonomy.py` owns the integrity risk taxonomy enum and
  wording across the integrity eval bundle, review contract, example report,
  and report schema.
- `source_doctrine_common.py` owns helper-only path constants, text/JSON
  loading, eval-dir lookup, and issue type access.

`source_eval_domains.py` remains the source-eval doctrine orchestrator and calls
these focused validators directly.

## Rationale

The shared pressure is authored-source doctrine, but the durable boundaries are
smaller: comparison routing, artifact/process separation, repeated-window
discipline, and integrity taxonomy. Splitting these validators keeps generated
readers and runtime reports outside source doctrine while also preventing
source doctrine from becoming a broad historical bin.

## Consequences

- Positive: doctrine failures now route to the specific source surface that
  owns the rule.
- Positive: `source_eval_domains.py` still provides one source-eval orchestration
  entrypoint without owning doctrine semantics.
- Positive: `source_doctrine_common.py` is helper-only and has no rule meaning.
- Tradeoff: source-eval doctrine orchestration imports more focused modules.

## Current Applicability

As of 2026-06-04:

- Still valid: source doctrine remains an authored source/topology gate below
  generated readers and runtime evidence.
- Changed: the broad `source_doctrine.py` module no longer exists.
- Supersedes: AOA-EV-D-0125 for aggregate source-doctrine module shape.

## Boundaries

This decision does not move bundle parsing, manifest schema validation,
generated catalog parity, runtime integrity review, receipt publication, or
release evidence into source doctrine.

It also does not make doctrine guides stronger than bundle-local source truth.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
