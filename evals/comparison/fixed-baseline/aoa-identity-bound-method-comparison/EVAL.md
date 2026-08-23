---
name: aoa-identity-bound-method-comparison
category: comparative
status: draft
summary: Checks whether method-effect observations remain identity-bound and comparable across a declared validation-method set without turning unmatched or synthetic rows into observed performance claims.
object_under_evaluation: identity-bound comparison of validation methods under an explicit workload, candidate, environment, treatment, evidence, acceptance, cache, and resource contract
claim_type: comparative
baseline_mode: fixed-baseline
report_format: comparative-summary
technique_dependencies: []
skill_dependencies: []
comparison_surface:
  shared_family_path: mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md
  paired_readout_path: mechanics/comparison-spine/parts/fixed-baseline/reports/identity-bound-method-comparison-proof-flow-v1.md
  integrity_sidecar: aoa-eval-integrity-check
  anchor_surface: aoa-runtime-latency-tradeoff
  baseline_target_label: legacy serial full-release path
  selection_question: Do you need a fixed-baseline contract that admits method-effect observations only when identity, evidence, cache, and resource posture are matched?
---

# aoa-identity-bound-method-comparison

## Intent

Use this draft eval to design and later apply a bounded comparison of
validation methods when a method-effect row is meaningful only under an exact
identity and parity contract.

The pressure for this bundle is an identity-bound comparison ABI, not a list of
commands. A method row is admissible only when the workload, exact
candidate/source, environment, route or treatment, evidence class, acceptance
target, cache posture, and resource posture are explicit and matched. The
bundle therefore preserves rejected, unmatched, unknown, null, excluded, and
unobservable states instead of filling gaps with zeros or inferred telemetry.

This is a design-and-application contract. It carries no real-session
telemetry in the repository and cannot issue a universal winner, causal
effect, central proof verdict, runtime-health verdict, or owner acceptance.

## Object under evaluation

This eval covers the identity-bound comparison contract for these method
shapes:

- `legacy_serial_full_release`
- `owner_focused_affected_only`
- `claim_evidence_activated_subgraph_or_tiered`
- `bounded_stable_prefix_session_measurement`
- `retry_after_fix_first_failure`
- `controlled_same_candidate_seeded_fault`

The method IDs are compared as named observation routes. They are not
capability or quality rankings. A method may produce a controlled accounting
row, an observed row, or no admissible row for a particular unit.

## Bounded claim

When a complete apply packet supplies the required identity tuple, explicit
source and environment identity, known cache and resource posture, reviewed
or controlled evidence, and matched method observations, the runner can
report a bounded observation disposition for that unit.

The result is either `matched_observation_only`,
`controlled_accounting_only`, or `unmatched`; the top-level draft report is
`not_admitted` until a matched observation is actually present. A matched
observation requires at least one schema-valid identity-provenance binding,
and the generated report preserves exactly one fixed-baseline binding per
admitted pair. Each binding contains the baseline and exactly one candidate,
and its methods must belong to the enclosing comparison unit. Each binding's
provenance must cover both bound method IDs and must not introduce a third
method ID. Binding identity evidence class is restricted to the published
two-class allowlist and must match every bound evidence-provenance class. The
schema bounds that parity to the six-method set: one baseline plus at most five
candidate pairs. A positive top-level verdict also requires a positive matched
unit and observed-pair count. Admitted units must declare identity matched, and
a positive observed unit must expose at least one jointly measured metric whose
values include the baseline and a candidate method from an admitted binding.
The report schema also binds each named metric to its canonical unit, caps
observed-pair count at admitted-pair count, requires distinct matched bindings,
allows each candidate method in at most one admitted binding, and requires every
observed or controlled metric value to name a method from that unit's admitted
bindings,
requires known cache and resource posture in positive bindings, requires
controlled-only units to have empty observed-value buckets, requires unmatched
units to declare zero pair counts, no matched bindings, and empty observed or
controlled value buckets, preserves an `unmatched_cases` entry for every unit
with an unmatched disposition or mismatch reason, and rejects a `not_admitted`
verdict that still contains an observed match. The runner's `validate_report`
semantic validator additionally binds every admission counter to the
corresponding `comparison_units` cardinality or sum, checks metric-value method
coverage against admitted bindings, and preserves those unmatched-reason unit
entries at both rejected-method and mismatch-reason level, rejects duplicate
unit IDs, non-finite report metric values, and metric buckets with duplicate
method IDs, rejects report-global digest conflicts for one provenance ref across
comparison units, requires one `method_states` entry for every method in every
metric, derives each metric's state counts and synthetic count from those entries,
and requires observed and controlled value buckets to match the corresponding
known method states. It also requires every counted observed pair to
have jointly measured values in at least one metric bucket and requires all
bindings in a unit to preserve one identity snapshot. Each unit carries
candidate-specific `unmatched_case_expectations`, and `validate_report`
requires the top-level `unmatched_cases` entries to match those expectations
per method, reason, and mismatch field; `build_report` invokes that validator
before returning a report. It is not a speedup,
causal effect, proof result, or winner verdict.

This eval does **not** support claims that:

- one validation method is universally faster, safer, or better
- synthetic or controlled fixture latency is observed real-session latency
- a stable-prefix measurement proves a whole-session or cross-host effect
- a missing, unknown, null, excluded, or unobservable field is zero
- a green validator, generated reader, or delivery receipt is semantic
  acceptance
- the comparison is central proof, runtime health, policy, or human acceptance

## Trigger boundary

Use this eval when:

- a proposed method comparison needs a complete identity-bound apply ABI
- multiple validation shapes must be compared without collapsing evidence
  classes or retry/failure/resource posture
- manual positive, negative, collision, and regression cases need a durable
  owner-local contract
- a future caller needs a deterministic report without letting the runner
  execute an arbitrary command

Do not use this eval when:

- the question is only a same-task regression with no method identity pressure
- the evidence is a broad runtime benchmark or health claim
- a method result is being used to rank agents, models, hosts, or owners
- a central proof verdict or human acceptance is required
- raw private session telemetry has not been reduced to a public-safe packet

## Inputs

Every comparison unit carries these exact identity fields:

`workload_id`, `candidate_or_source_identity`, `source_ref_or_digest`,
`environment_id`, `route_or_treatment_identity`, `evidence_class`,
`acceptance_target`, `cache_posture`, and `resource_posture`.

The baseline and each method row must match these values exactly. Cache and
resource posture must have `status: known` for an eligible observed pair.
The `candidate_or_source_identity` field must itself be a SHA-256 digest;
mutable candidate labels are not an admissible identity binding.
The `source_ref_or_digest` identity field must carry the packet's exact
`source_digest`; a mutable source ref is not an admissible observation binding.
Every row must be `reviewed` or `controlled`; provisional rows remain
unmatched. An `unobservable`-origin row is never an eligible method pair, and
known metric values under that origin are a contract error rather than an
observed value.

Named metrics use canonical units: seconds, milliseconds, kibibytes, bytes, or
ratio as declared by the metric name. An observed pair is eligible only when
at least one metric is jointly known for baseline and candidate under the same
canonical unit. `matched_pair_count` includes all admitted origin pairs, while
`eligible_real_pairs` counts only jointly measured observed pairs.
Each metric's `method_states` preserves one state and `measurement_origin` for
every method in the unit, including rejected rows. The `state_counts` and
`synthetic_count` fields are derived summaries of those per-method states; only
eligible known observed or controlled methods populate `observed_values` or
`controlled_values`, and those buckets must remain in exact parity with the
canonical method states. Rejected rows remain visible through the state entries,
state counts, and `unmatched_cases`.

Every observation `evidence_ref` must resolve to a declared packet artifact
with `kind: public-safe-observation` and a SHA-256 digest. Only
`public-safe-contract` and `reviewed-owner-packet` evidence classes are
admissible, and the artifact class must match the row identity class. Generated
readers, validation receipts, and other derived surfaces cannot bind a positive
observation disposition. Reports publish this complete two-class allowlist,
even when one packet uses only one class. Matched report bindings preserve the
same class in their identity snapshot and every evidence-provenance row.

The contract keeps all of these states distinct:

- known observed values
- unknown values
- semantic null values
- excluded evidence
- unobservable values
- missing fields
- controlled or synthetic accounting values
- unmatched identity or parity

Synthetic values may demonstrate that accounting is wired, but they never
enter `observed_values` and never produce an effect or policy verdict.

## Fixtures and case surface

The full apply input ABI is in `fixtures/apply-packet.schema.json`. It is deliberately
larger than a selection result. It requires `verdict: exact_fit`, owner and
source identity, environment, command shape, prerequisites, artifacts,
pass criteria, effect authority, expected effect, proof limit, the complete
method set, and explicit observations.

`runners/run_identity_bound_method_comparison.py` validates and consumes this
packet. It never invokes `command.argv`, reads live runtime state, invents
telemetry, or repairs absent fields. It deterministically emits the report
schema at `reports/summary.schema.json`, with comparison units ordered by
`unit_id` and row-derived arrays ordered by canonical `method_id`. Every
admitted pair also carries its exact matched identity tuple and the digest,
kind, class, and reference of each bound public-safe observation artifact;
matched positive units require at least one such binding, controlled matched
units preserve the same binding invariant with empty observed-value buckets,
and unmatched units carry an empty matched-binding list, zero pair counts, and
empty metric value buckets. The report schema binds the binding-array
cardinality to the admitted-pair count and requires a matched unit for a
positive top-level verdict. It also requires identity-match truth for admitted
units, known cache and resource posture in positive bindings, distinct binding
objects with no candidate repeated across bindings, canonical units for named
report metrics, and measured coverage for positive observed units whose
measured methods are present in admitted bindings. Every observed or controlled
metric value must likewise be covered by an admitted binding, and each unit
with an unmatched disposition or mismatch reason must remain represented in
`unmatched_cases`, with candidate-specific mismatch reasons preserved in each
unit's `unmatched_case_expectations`. `validate_report` checks the report schema
and verifies that
observation, unit, disposition, matched-pair, and eligible-real-pair admission
counters equal the derived `comparison_units` values, and that every metric
state-count plus synthetic-count total equals the unit method cardinality. The
declared command timeout and report metric values must also be finite;
non-finite literals and numeric overflow are rejected before admission. An
observed matched unit must retain a `reviewed` status, controlled bindings must
retain known cache and resource posture, and each metric value bucket has at
most one value per method. Every binding counted by `observed_pair_count` must
have a jointly measured metric bucket, and all bindings in one unit must carry
the same identity snapshot. Swapping mismatch fields between rejected
candidates is rejected because each case must match its unit expectation.
The report-level `claim_boundary`, `limitations`, and each unit's `claim_limit`
are canonical contract text; replacements that broaden the claim are rejected.

The apply packet is therefore a contract for a future owner-local run, not
evidence that a run occurred. The checked-in example report is intentionally
an unmatched design example.

The shared fixture family and replacement boundary are declared in
`fixtures/contract.json`.

## Scoring or verdict logic

`fixtures/manual-case-trace.json` turns the evaluator pressure into durable
public-safe cases:

- a positive exact identity match
- a negative identity mismatch
- a duplicate-unit or duplicate-method collision
- a regression where cache, resource, or first-failure posture is incomplete
- a synthetic-latency accounting seal with the baseline row visible
- an unmatched evidence-class or review-state case

The cases preserve the reason for rejection and the claim limit. They contain
no raw session transcript, private host fingerprint, or fabricated measurement.
The controlled/synthetic accounting case declares the baseline method so its
expected `controlled_accounting_only` disposition remains executable by a
future harness rather than silently becoming a one-sided unmatched case.

The runner uses these dispositions:

- `matched_observation_only` when an observed baseline/candidate pair passes
  identity, parity, canonical-unit, and joint-metric coverage checks;
- `controlled_accounting_only` when the pair is controlled or synthetic;
- `unmatched` when identity, review, posture, origin, or comparison coverage is
  not eligible;
- `contract_error` when the packet collides or fails its schema.

No disposition creates `policy_verdict`; it remains JSON `null`.

## Baseline or comparison mode

This bundle uses the existing `fixed-baseline` comparison part. The baseline
label is the declared `legacy_serial_full_release` method. The comparison
surface is anchored to `aoa-runtime-latency-tradeoff` only as the nearest
existing routing neighbor; that anchor is not an evidence input and its
runtime measurements are not reused for this contract.

The paired readout is
`mechanics/comparison-spine/parts/fixed-baseline/reports/identity-bound-method-comparison-proof-flow-v1.md`.
The readout explains how the identity ABI constrains interpretation; it does
not promote the draft bundle or create a repo-global score.

## Execution contract

Validation must cover the source bundle, fixture and runner contracts, report
schema/example, manual cases, deterministic runner behavior, generated
catalog/readers, and the repository's semantic checks. A green check proves
only the declared contract. It does not prove that a matched real-session
cohort exists.

## Outputs

The runner emits one schema-backed report with:

- the declared baseline and complete method set;
- identity contract and apply-field admission summary;
- per-unit disposition, identity mismatches, evidence refs, and metric-state
  coverage;
- unmatched cases and explicit limitations;
- `policy_verdict: null` and no universal winner field.

`reports/example-report.json` is an unmatched design-only example. A future
actual report must be separately reviewed before it is used outside this
owner-local contract.

## Failure modes

The instrument must fail closed on:

- `partial_fit` or any apply packet missing the complete exact-fit ABI;
- source or environment digest/ref drift;
- duplicate unit/method observations;
- unknown cache or resource posture used as if it were zero;
- provisional, unreviewed, excluded, or controlled rows presented as observed;
- synthetic or controlled values placed in observed output;
- a noncanonical metric unit or a baseline/candidate unit mismatch;
- an observed pair with no jointly known comparable metric;
- binding provenance that omits either bound method or names another method;
- one provenance ref with conflicting digests across comparison units;
- a candidate method repeated across admitted bindings;
- an observed or controlled metric value whose method has no corresponding
  admitted binding;
- duplicate comparison unit IDs, duplicate metric values for one method, or a
  non-finite report metric value;
- missing, duplicated, or origin-inconsistent `method_states`, state counts or
  synthetic counts that do not derive from them, or observed/controlled buckets
  that omit or recast a known method;
- an observed-pair count that lacks jointly measured coverage for one of its
  admitted bindings, or bindings in one unit with different identity snapshots;
- an unmatched unit with nonzero pair counts or a matched binding;
- an unmatched unit with observed or controlled metric values;
- an observed-pair count greater than the admitted-pair count;
- a `not_admitted` verdict that retains an observed matched unit;
- an observation reference that is undeclared, digest-unpinned, or from a
  disallowed/derived evidence class;
- an unmatched candidate row or mismatch reason silently dropped from
  `unmatched_cases`;
- candidate-specific mismatch fields or reasons swapped between rejected
  methods;
- a generated reader, delivery receipt, or green validator treated as live
  evidence.

## Blind spots

This eval does not prove:

- that any real-session method pair exists
- first-failure latency or retry amplification when those fields are
  unobservable
- resource or cache parity outside the supplied packet
- causal impact, statistical significance, or a deployment decision
- a universal method winner or owner acceptance
- current Goal readiness or runtime health

## Interpretation guidance

Treat `matched_observation_only` as the narrowest possible positive reading:
the packet contained an identity-, parity-, unit-, and metric-covered observed
pair. Treat
`controlled_accounting_only` as accounting evidence only. Treat
`unmatched` as visible absence of an eligible pair, not as a failed method or
zero cost.

Do not derive a speedup, cost, causal, proof, policy, acceptance, or global
comparison claim from this bundle without a separately owned contract and
fresh evidence.

Do not treat a positive result as:

- a universal method winner or ranking;
- observed real-session latency when the origin is synthetic or controlled;
- proof of first-failure, retry, cache, or resource behavior when those fields
  are unknown or unobservable;
- central proof, runtime health, policy, deployment, or human acceptance;
- evidence that the current Goal is ready or accepted.

## Verification

- run the bundle-local tests and validate both JSON schemas;
- run source, fixture, runner, report, and comparison-surface validators;
- regenerate and check catalogs, selection/report readers, and decision indexes;
- run repository semantic validation and the minimum repository test route;
- keep any missing live cohort or fresh owner receipt as an explicit residual
  risk.

## Technique traceability

Technique linkage is intentionally bounded to the identity/parity comparison
contract. No technique is credited with a performance effect by this draft.

## Skill traceability

Skill linkage is intentionally deferred. The bundle checks a proof ABI and
evidence boundary, not direct agent skill quality.

## Adaptation points

Project overlays may add:

- owner-local method fixtures and reviewed evidence refs;
- a separately approved apply wrapper that still validates this packet;
- local report consumers that preserve the same unknown/null/unmatched states;
- additional manual cases without widening the bounded claim.
