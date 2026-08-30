# Comparison Contract

Use this bundle with the fixed baseline target:

- baseline: one canonical `continuity_capsule_v1`
- candidate: its portable and private materializations
- comparison: exact field, reference, digest, and protected-tail parity
- route: fixed-baseline and field-level, not provider- or quality-level

The readout must preserve:

- goal, constraints, completed work, current work, blockers, exact decisions,
  open obligations, evidence refs, and omissions or uncertainty
- source watermark and compaction-event metadata
- protected-tail omission in the portable view
- verbatim protected-tail digest and byte count in the private view

The runner may say that a supplied packet is internally preserved. It may not
say that a real session compacted, that a provider rehydrated it, or that the
direction improved runtime economy.

The canonical baseline target stays visible in every readout. Missing or
unknown fields remain failures or explicit omissions; noisy variation and
style-only presentation changes are not converted into a stronger continuity,
runtime, or economy claim.
