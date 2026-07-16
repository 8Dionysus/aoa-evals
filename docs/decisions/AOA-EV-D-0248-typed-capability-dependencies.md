# Typed Capability Dependencies

- Decision ID: AOA-EV-D-0248
- Status: Accepted
- Date: 2026-07-16
- Owner surface: `evals/**/EVAL.md`, `evals/**/eval.yaml`, and the generated
  eval catalog and capsule readers

## Index Metadata

- Original date: 2026-07-16
- Surface classes: proof topology, source/topology, generated/readout, sibling reference
- Mechanic parents: proof-object
- Guard families: source eval dependency, owner boundary, generated parity
- Posture: accepted typed-dependency rationale

## Context

After the shared skill consolidation, 21 eval bundles still named five former
skills through `skill_dependencies`. Owner-current `aoa-skills` evidence gives
those names different dispositions:

- `aoa-change-protocol` became
  `workflow.operations.repository-change`;
- `aoa-bounded-context-map` became
  `mode.engineering-shape.contexts`;
- `aoa-contract-test` became `mode.verification.contract`;
- `aoa-checkpoint-closeout-bridge` became
  `workflow.operations.checkpoint-closeout`;
- `aoa-approval-gate-check` became `guard.operations.approval`.

Manual review of representative workflow, boundary, stress, and capability
evals confirmed that the eval claims still need those current procedural or
enforcement surfaces, but none of the five remains a standalone callable
skill. Keeping the old names made downstream routing resolve retired packages
and blurred the distinction between a skill, mode, workflow, and runtime
guard.

## Options Considered

- Keep the legacy names until every downstream consumer changes. This preserves
  a green historical projection by publishing dependencies that no longer
  exist.
- Replace merged modes with their containing skill and drop workflow and guard
  dependencies. This restores path validity but loses the exact object the eval
  depends on.
- Add one typed capability dependency lane while retaining
  `skill_dependencies` only for actual callable skills.

## Decision

Use `skill_dependencies` only for callable skills. Add optional
`capability_dependencies` to eval frontmatter and manifests for typed
capability-graph nodes.

Each manifest capability ref records:

- stable capability `id` and `kind`;
- the `aoa-skills` registry repository and authored family path;
- the actual `target_owner`, which may differ from the registry owner.

Generated catalogs and capsules project both the compact ordered IDs and the
full refs. Existing dependency validation is extended to check ordered
frontmatter/manifest parity, registry-path reachability, and exact registry
entry parity for `id`, `kind`, and `target_owner`. The existing Eval Forge
proposal and scaffold route carries the same typed refs into both source files.
No parallel validator or second graph is introduced.

## Rationale

The split preserves the real object type instead of treating every reusable
procedure or enforcement boundary as a skill. It keeps `aoa-evals` responsible
for its dependency claim, `aoa-skills` responsible for the semantic capability
registry, and the target owner responsible for execution or enforcement.

The field was introduced only after manual bundle inspection exposed the same
misclassification across 21 source packages and a real downstream routing
failure. Extending the existing source-reference and generated-parity checks
protects a durable ABI; it is not a temporary test scaffold.

## Consequences

- Positive: retired skill paths disappear from active eval truth and generated
  readers.
- Positive: modes, workflows, and guards remain distinguishable to routing,
  KAG, and future task-local composition.
- Positive: registry provenance and execution ownership stay separate.
- Tradeoff: consumers of the eval catalog must understand the additive
  capability fields before deriving cross-kind adjacency.
- Tradeoff: registry-entry parity proves the declared semantic node and owner
  mapping, not that the target runtime or workflow is currently available.
- Follow-up: `aoa-routing` can now ingest current callable skills and preserve
  typed eval dependencies without resurrecting the retired 57-skill catalog.

## Current Applicability

As of 2026-07-16:

- Still valid: source eval packages own dependency meaning and generated
  readers remain derived.
- Changed: source dependencies may now target typed capability nodes instead
  of being forced through `skill_dependencies`.
- Superseded by: none.

## Boundaries

This decision does not change any eval category, status, baseline, verdict,
report format, maturity, or bounded claim. It does not make the capability
graph proof authority, make an external workflow executable, or allow a
generated reader to outrank the source bundle or target owner.

## Validation

Validation combines the manual 21-bundle dependency disposition with schema
validation, source dependency parity and reachability, catalog/capsule rebuild
parity, decision-index parity, repository validation, focused catalog tests,
the full test suite, CI, and downstream `aoa-routing` reconstruction against
owner-current checkouts.
