# Validation-routing bounded fixtures v1

This fixture family extends the `peer-compare` part with a public-safe,
measurement-only comparison of candidate validation activation methods.

The contract holds `(workload_id, candidate_set_id, environment_id,
source_ref)` constant for every peer method within one scenario. The scenario
declares a `full_owner_proof` oracle/fallback and keeps stale, unknown,
malformed, wrong-identity, and unavailable external evidence explicit.

The cases are seeded fixtures. The validation-activation shadow report is
bounded input metadata only; it does not become a real-session case, a receipt,
an eval verdict, or a routing policy.

The v1 evidence policy admits only `evidence_kind=seeded_fixture` and records
`real_session` as not admitted. Latency values are synthetic fixture-event
proxies and use the `_synthetic_proxy` field suffix; they do not describe
observed runtime performance. A generic method explanation cannot explain a
missing node: the runner requires a non-empty node-keyed
`missing_explanations[node]` entry.

Owner-contract receipt states are derived from inspected receipt shape and the
complete scenario identity tuple before any declared state label is trusted.
Therefore a mislabeled complete receipt cannot fabricate malformed or
wrong-identity adversarial coverage, and partial or mismatched receipts remain
fail-closed.

Required adversarial classes:

- stale graph;
- unknown dependency;
- wrong candidate/environment receipt;
- malformed receipt; and
- unexplained miss; and
- unbound external owner.

The family intentionally records unsupported candidates for API/ABI, coverage,
mutation, live KAG relations, and LLM-proposed additions rather than inventing
evidence for them.
