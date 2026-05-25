# Experience Verdict Residue Parts

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/experience/`

## Index Metadata

- Surface classes: mechanic part
- Mechanic parents: experience
- Guard families: part and payload
- Posture: active rationale

## Context

After the Experience mechanic package existed, several root `docs/` verdict
surfaces still had matching part-local examples, schemas, and tests under
Experience:

- appeal review, stay-order enforcement, vote-seal integrity, and replay-history
  integrity matched `governance-runtime-boundary`;
- replay audit and service-mesh regression matched `office-release-train`.

Leaving those docs in root `docs/` made the active topology less convex: the
operation already had a part owner, but the human guidance still sat in a broad
district.

## Options Considered

- Leave the residue in root `docs/`.
- Create new parent mechanics such as `governance-verdicts` or
  `office-verdicts`.
- Move each verdict doc into the existing Experience part that already owns the
  schema/example/test route.

## Decision

Move the remaining Experience verdict residue into the existing active parts:

- `APPEAL_REVIEW_VERDICT.md`, `STAY_ORDER_ENFORCEMENT_VERDICT.md`,
  `VOTE_SEAL_INTEGRITY_VERDICT.md`, and
  `REPLAY_HISTORY_INTEGRITY_VERDICT.md` route through
  `mechanics/experience/parts/governance-runtime-boundary/docs/`;
- `REPLAY_AUDIT_VERDICTS.md` and `SERVICE_MESH_REGRESSION_VERDICTS.md` route
  through `mechanics/experience/parts/office-release-train/docs/`.

## Rationale

The parent stays `experience` because these verdicts materialize Experience
governance, runtime-boundary, office, and release-train proof support. The doc
names describe part-local verdict families; they do not justify new parent
packages.

The move follows already-present local evidence: part READMEs, schema/example
pairs, and part tests already describe the narrower owner routes.

## Consequences

- Positive: root `docs/` no longer carries active Experience verdict docs that
  already have part-local owners.
- Tradeoff: Experience parts now hold more seed-era verdict docs, so the
  provenance and legacy index must stay precise.
- Follow-up: service-mesh or replay families may become narrower parts only if
  a later evidence pass proves independent inputs, outputs, owner split,
  stop-lines, and validation beyond one verdict family.

## Boundaries

This decision does not grant governance authority, runtime enforcement,
office installation, release approval, service dispatch, vote authority,
or replay acceptance. It only routes bounded proof support surfaces.

## Validation

Planned checks for this slice:

```bash
python -m pytest -q mechanics/experience/parts/governance-runtime-boundary/tests/test_experience_wave4_seed_contracts.py mechanics/experience/parts/office-release-train/tests/test_experience_wave5_seed_contracts.py
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
