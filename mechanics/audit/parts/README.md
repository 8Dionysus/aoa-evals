# Audit / Parts Route

This directory contains the part-local surfaces for the `audit` mechanic.

Each part owns a bounded suboperation in the same candidate-evidence loop:

- `selected-evidence-packets/` curates runtime-owner artifacts into public-safe
  evidence packets.
- `artifact-verdict-hooks/` maps playbook or trace artifacts to eval anchors and
  review expectations.
- `candidate-readers/` generates compact readers from the source packet and hook
  examples.
- `integrity-review/` keeps W10-shaped runtime continuity evidence
  candidate-only and replay-bounded.

Do not create another part unless it has source surfaces, drift-catching
validation, and a clear stop-line against stronger owner truth.
