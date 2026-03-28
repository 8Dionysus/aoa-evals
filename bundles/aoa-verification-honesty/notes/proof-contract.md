# Proof Contract

This bundle now ships a machine-readable `summary-with-breakdown` report surface,
plus bundle-local fixture and runner contracts, while remaining `bounded` and `local-shaped`.

Canonical per-case fields for the materialized read:
- `claimed_verification`
- `executed_checks`
- `skipped_checks`
- `blocked_checks`
- `inference_boundary`
- `failure_vs_readout`
- `outcome`

Public report discipline:
- keep executed, skipped, blocked, and inferential verification separate
- do not collapse blocked and skipped checks into one bucket
- do not promote inspection or static reasoning into executed verification
- keep the schema-backed report weaker than the bundle-local interpretation boundary
- keep the shared family anchored in `fixtures/verification-honesty-v1/README.md`

Bounded replacement discipline:
- another repo may replace the concrete cases only if it preserves the same honesty pressure across fully executable, partially executable, environment-blocked, and inspection-overclaim cases
- another repo may rename local verification commands and blocked-check labels
- another repo must preserve inspectable evidence for the claimed-vs-actual verification split

This materialized proof surface prepares the next portability wave.
It does **not** by itself promote this bundle beyond `bounded`.
