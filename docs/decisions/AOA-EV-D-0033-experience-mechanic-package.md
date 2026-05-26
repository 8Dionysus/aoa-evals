# Experience Mechanic Package

- Decision ID: AOA-EV-D-0033
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/experience/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic package
- Mechanic parents: experience
- Guard families: none
- Posture: active rationale

## Context

Experience is a named AoA mechanic, and `aoa-evals` has enough local proof-side
evidence to route it as a live mechanic package rather than a scattered root
support family.

The evidence cluster spans `aoa-experience-protocol-integrity`,
`aoa-experience-certification-gate-integrity`,
protocol fixtures, certification and adoption docs, governance/runtime-boundary
verdict packets, office release-train support, examples, schemas, fixtures,
tests, and generated references.

Later decision `AOA-EV-D-0038-distillation-mechanic-package.md` split the reviewed
runtime distillation candidate adoption fixture family out of Experience and
into `mechanics/distillation/parts/runtime-candidate-adoption/`. Experience
continues to own generic adoption, consent, compatibility, federation, shadow,
and KAG/ToS boundary proof support.

## Options Considered

- Leave Experience as a candidate family in `mechanics/EVIDENCE_CLUSTERS.md`.
- Create proof-adjective parents such as `experience-proof`,
  `certification-proof`, or `adoption-proof`.
- Move every Experience-related source proof bundle into
  `mechanics/experience/`.
- Create `mechanics/experience/` as the AoA-aligned parent, move only
  Experience support surfaces into parts, and keep source proof bundles plus
  stronger-owner truth in their owning routes.

## Decision

Create `mechanics/experience/` for the eval-side Experience proof operation:

`experience pressure -> bounded experience proof question -> part-local verdict support -> bundle-local review -> bounded report or owner handoff`

The active parts are:

- `protocol-integrity` for the experience verdict protocol fixture family and
  validation test;
- `certification-gate` for certification, release-gate,
  deployment-integrity, rollback, watchtower, and certification-adjacent
  verdict support;
- `adoption-federation` for adoption, consent, shadow, compatibility,
  KAG/ToS boundary, federation, and owner adoption proof support;
- `governance-runtime-boundary` for governance, authority-resolution,
  constitution-runtime, sealed-vote, runtime-boundary, and ToS governance
  verdict support;
- `office-release-train` for office scope, multi-office, governed-release,
  handoff, installation, replay, rollback, and train-release verdict support.

Source proof bundles stay under `evals/`. Former root docs, fixtures,
examples, schemas, and tests are mapped inside the owning legacy archive after
the active `PROVENANCE.md` bridge.

## Rationale

The parent name must be `experience` because the proof-side work materializes
the center AoA Experience mechanic. The part names describe narrower eval-side
support operations.

This prevents two errors: leaving a mature Experience proof cluster scattered
through root technical districts, and creating proof-organ adjective parents
that would fragment one center mechanic into future-bug packages.

## Consequences

- Positive: future Experience proof work starts from a clear active route,
  part contract, owner split, stop-lines, validation path, and provenance
  bridge.
- Tradeoff: source proof bundles remain outside the package, so package users
  must keep bundle-local proof authority visible.
- Follow-up: continuity-context, service-mesh, capture-kernel,
  compatibility-bridge, and runtime-boundary pressure should become separate
  parts only after source artifacts, inputs, outputs, owner split, stop-lines,
  and validation prove a recurring operation.

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/experience/` remains the AoA-aligned eval-side parent
  for protocol integrity, certification gate, adoption federation,
  governance/runtime-boundary, and office release-train proof support.
- Changed: parent-level boundary coverage now uses pressure-to-owner routes in
  `README.md`, `PARTS.md`, and `DIRECTION.md`, with validator tokens guarding
  the parent route rows.
- Superseded by: none.

## Review Log

### 2026-05-24 - Parent boundary route wording

- Previous assumption: parent-level Experience surfaces expressed boundaries
  through exclusion prose around live runtime, office installation,
  certification, release approval, owner adoption, memory canon, routing, KAG,
  ToS authorship, and broad Experience success.
- New reality: the parent route keeps the same authority split through
  pressure-to-owner-route rows.
- Reason: AoA center Experience owns law and owner-routing grammar, while
  `aoa-evals` keeps bounded proof support; the active package should show the
  next owner route directly.
- Source surfaces updated: `mechanics/experience/README.md`,
  `mechanics/experience/PARTS.md`, `mechanics/experience/DIRECTION.md`, and
  `scripts/validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k
  experience_mechanic`, `python -m pytest -q
  mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py
  mechanics/experience/parts/certification-gate/tests
  mechanics/experience/parts/adoption-federation/tests
  mechanics/experience/parts/governance-runtime-boundary/tests
  mechanics/experience/parts/office-release-train/tests`, `python
  scripts/build_catalog.py --check`, `python scripts/validate_repo.py`,
  `python scripts/validate_semantic_agents.py`, `git diff --check`, and
  `python -m pytest -q`.

## Boundaries

This decision does not move Experience source proof bundles into
`mechanics/experience/`.

It does not authorize live workspace runtime, service dispatch, office
installation, assistant operational authority, operator certification, release
approval, deployment approval, rollout promotion, owner-local adoption, memory
canon, recall sovereignty, live router behavior, forced KAG promotion, direct
Tree-of-Sophia runtime write, or broad Experience success claims.

It does not transfer `Agents-of-Abyss`, `abyss-stack`, `aoa-agents`,
`aoa-playbooks`, `aoa-routing`, `aoa-memo`, `aoa-sdk`, `aoa-stats`,
`aoa-skills`, `aoa-techniques`, `aoa-kag`, or `Tree-of-Sophia` owner truth
into `aoa-evals`.

## Validation

- `mechanics/experience/README.md` names the owned operation, source surfaces,
  inputs, outputs, stronger-owner split, stop-lines, legacy route, and
  validation.
- `mechanics/experience/AGENTS.md` names local editing law.
- `mechanics/experience/PARTS.md` names the active part topology.
- `mechanics/experience/PROVENANCE.md` bridges old root placement questions
  into the owning legacy archive after the active route.
- `scripts/validate_repo.py` checks the package, parts, provenance bridge,
  decision, and stale root paths.
- `python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py mechanics/experience/parts/certification-gate/tests/test_experience_certification_gate_integrity.py mechanics/experience/parts/certification-gate/tests/test_experience_wave2_seed_contracts.py mechanics/experience/parts/adoption-federation/tests/test_experience_wave3_seed_contracts.py mechanics/experience/parts/governance-runtime-boundary/tests/test_experience_wave4_seed_contracts.py mechanics/experience/parts/office-release-train/tests/test_experience_wave5_seed_contracts.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
