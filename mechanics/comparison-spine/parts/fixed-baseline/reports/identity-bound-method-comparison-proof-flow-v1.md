# Identity-Bound Method Comparison Proof Flow v1

This dossier defines the fixed-baseline support route for:

- `aoa-identity-bound-method-comparison`

It is a bundle-local design and admission readout. It does not claim that a
real-session cohort exists and does not convert the current partial-fit
assessment into a proof result.

## Shared case family

Use
`mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`
as the shared public-safe fixture-family route only when every method row is
bound to the same workload and exact source/candidate identity.

The identity-bound read must preserve:

- `workload_id`;
- `candidate_or_source_identity` and `source_ref_or_digest`;
- `environment_id`;
- `route_or_treatment_identity`;
- `evidence_class`;
- `acceptance_target`;
- `cache_posture` and `resource_posture`;
- first-failure, retry, and metric state distinctions.

## Read order

1. Read the bundle-local `EVAL.md` and `eval.yaml`.
2. Validate the complete `exact_fit` apply packet.
3. Confirm the baseline method and the declared six-method set.
4. Check source digest, environment identity, and required prerequisites.
5. Group rows by `unit_id`; reject duplicate unit/method collisions.
6. Compare each candidate method to `legacy_serial_full_release` by exact
   identity and parity.
7. Preserve unmatched reasons and all non-known states.
8. Separate observed values from controlled or synthetic accounting.
9. Interpret only the bounded disposition in the generated report.

## Required comparison shapes

- `matched_observation_only` — an identity- and parity-matched observed pair;
- `controlled_accounting_only` — a matched accounting shape with controlled or
  synthetic origin, never observed effect;
- `unmatched` — missing, provisional, excluded, unknown, unobservable, or
  identity-mismatched evidence;
- `contract_error` — duplicate or malformed input rejected before a report.

## Distinctness boundary

The fixed-baseline label names the declared legacy serial method as a local
reference. It does not make that method globally authoritative and does not
reuse measurements from `aoa-runtime-latency-tradeoff`.

The runner is intentionally non-executing: `command.argv` is an apply ABI
field, not permission for the runner to launch work. A report with observed
values is still only a bounded observation. It is not a speedup, causal effect,
statistical result, proof, policy, runtime-health, or human-acceptance claim.

## Route checks

| Pressure | Route |
| --- | --- |
| missing identity or parity field | keep the unit unmatched and record the field |
| unknown cache/resource posture | preserve unknown; do not substitute zero |
| synthetic latency or seeded fault | controlled accounting only; exclude from observed values |
| first-failure or retry not observable | retain null/unobservable state and defer effect claims |
| universal method winner | bundle-local bounded report only; no winner verdict |
| central proof or current Goal acceptance | route to the owning proof/runtime/acceptance surface |
