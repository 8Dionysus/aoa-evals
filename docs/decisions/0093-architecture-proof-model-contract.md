# Architecture Proof Model Contract

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `docs/ARCHITECTURE.md`

## Context

`docs/ARCHITECTURE.md` predated most of the mechanics refactor and mainly
explained portable eval bundles. That was useful, but too weak for the current
repository shape: `DESIGN.md` now owns the system form,
`docs/PROOF_TOPOLOGY.md` owns authority classes, and
`mechanics/EVIDENCE_CLUSTERS.md` owns the evidence gate before mechanic parent
growth.

Without an explicit contract, Architecture could quietly drift back into a
bundle-only model or compete with the topology and mechanics ledgers.

## Decision

Keep `docs/ARCHITECTURE.md` as the technical proof model. It must describe:

- portable eval bundles as source proof surfaces;
- mechanics as operation support, not replacement bundle authority;
- AoA-aligned mechanics versus evals-native mechanics as parent-name routes;
- the owner-named evals-native subcase, where a stronger-owner subject name
  can stay local only when `aoa-evals` owns the proof-side operation and the
  stronger owner split remains visible;
- artifact forms as parts or payloads under an owning parent;
- legacy bridge layering through `PROVENANCE.md` as the single controlled
  bridge into archive lineage.

`scripts/validate_repo.py` now checks those tokens through
`validate_root_design_surfaces`.

## Consequences

- Positive: Architecture can evolve technically without stealing the role of
  `DESIGN.md`, `docs/PROOF_TOPOLOGY.md`, or
  `mechanics/EVIDENCE_CLUSTERS.md`.
- Positive: future edits cannot erase mechanics and legacy bridge layering from
  the technical model while tests still pass.
- Tradeoff: small Architecture wording edits now need to keep the proof-model
  contract visible.

## Current Applicability

As of 2026-05-24:

- Still valid: `docs/ARCHITECTURE.md` owns the technical proof model, while
  repository form, authority classes, and mechanic-parent evidence route to
  their owner surfaces.
- Changed: the long-term direction now names `regression visibility with
  bounded comparison semantics` and `growth tracking with explicit claim limits`
  as the desired proof outcomes.
- Source surfaces updated: `docs/ARCHITECTURE.md`, `scripts/validate_repo.py`,
  and `tests/test_validate_repo.py`.
- Validation route: `python -m pytest -q tests/test_validate_repo.py -k architecture`
  and `python scripts/validate_repo.py`.

## Review Log

### 2026-05-24 — Long-term direction route language clarified

- Previous assumption: `regression visibility without metric theater` and
  `growth tracking without inflated claims` were sufficient shorthand for the
  architecture direction.
- New reality: this active route surface reads better for low-context agents
  when it names the proof output: bounded comparison semantics and explicit
  claim limits.
- Reason: architecture is used as a technical operating map, so its direction
  bullets should expose the route an agent can follow.
- Source surfaces updated: `docs/ARCHITECTURE.md`, `scripts/validate_repo.py`,
  and `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k architecture`
  and `python scripts/validate_repo.py`.

## Boundaries

This decision does not create a new mechanic parent.

It does not make Architecture the source of active mechanics. Parent mechanics
still require evidence in `mechanics/EVIDENCE_CLUSTERS.md`, local route cards,
parts, validation, and decision review.

It does not make legacy active. Legacy remains provenance behind the active
route.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k architecture_proof_model
python scripts/validate_repo.py
```
