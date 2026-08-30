# Refactor contract

The shared `refactor-torture-v1` family is intentionally provider-neutral. It
requires the report to expose the fields a later owner-specific proof route
would need: semantic identity, lineage posture, freshness against a source
epoch, invalidation scope, provenance, metric presence, and affected-test or
parity evidence where the case demands it.

The family does not decide whether a provider's observations are true. It
only rejects incomplete or internally inconsistent envelopes.
