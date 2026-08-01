# Rollback-readiness contract

This bundle may review one exact private
`abyss_stack_mcp_rollback_candidate_v1` emitted by `abyss-stack` for a single
organ capability and policy plane.

The review answers only whether the candidate satisfies the checked-in source
contract: it names an immutable deployment record, preserves exact
source/deployed/last-known-good package identity, names a stable restorable
unit and executable rather than a transient PID, carries no credentials, uses
a distinct owner-grounded last-known-good canary, remains inside its evidence
window, and keeps execution, admission, rollback, and higher-effect authority
false.

The runner deliberately does not open the deployment record, inspect the live
unit, probe the endpoint, read credentials, mutate the registry, restart a
process, or execute restoration. A positive review is therefore candidate
support, not rollback proof. The stack-owned projector must independently
revalidate the unchanged private candidate and every referenced live input
before it may publish a temporary readiness observation. Only a separately
authorized restoration plus post-rollback health evidence may support an
executed rollback claim.

This support surface extends the existing admission-integrity bundle because
it protects the same forbidden inference: readiness evidence cannot silently
become admission or effect authority. It is not the future pair-specific live
rollback suite required by `AOA-EV-D-0249`.
