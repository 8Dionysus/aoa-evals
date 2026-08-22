# Eval integrity check

## Source and authority

- `EVAL.md` and `eval.yaml` are the source surfaces for this draft bundle.
- `fixtures/apply-packet.schema.json` owns the future apply input shape.
- `runners/run_identity_bound_method_comparison.py` owns deterministic local
  admission and report construction.
- `reports/summary.schema.json` owns the report shape; the example report is
  design-only and intentionally unmatched.
- The fixed-baseline comparison-spine readout is support, not a replacement
  for bundle-local meaning.

## Integrity assertions

- The method set is explicit and complete.
- The nine identity fields are required on every observation.
- Source and candidate identity uses an explicit SHA-256 digest.
- Cache and resource posture cannot silently become zero.
- Unknown, null, excluded, unobservable, and missing states are preserved.
- Synthetic and controlled values cannot enter `observed_values`.
- Duplicate units or methods fail closed before a report is written.
- The runner never executes a declared command.
- `policy_verdict` is always JSON `null`.
- No report is central proof, runtime health, policy, or human acceptance.

## Verification route

Run the bundle-local tests, JSON schema checks, source validators, generated
catalog/readers, and the repository minimum validation. A successful command
proves only its declared contract; it does not create real-session telemetry.
