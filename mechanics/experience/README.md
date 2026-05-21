# Experience Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Owned Operation

`mechanics/experience/` owns the eval-side Experience proof operation:

`experience pressure -> bounded experience proof question -> part-local verdict support -> bundle-local review -> bounded report or owner handoff`

This package is AoA-aligned. It keeps the parent name `experience` because the
operation materializes the center Experience mechanic on the proof side.

## Source Surfaces

- `bundles/aoa-experience-protocol-integrity/EVAL.md`
- `bundles/aoa-experience-certification-gate-integrity/EVAL.md`
- `mechanics/experience/parts/protocol-integrity/README.md`
- `mechanics/experience/parts/certification-gate/README.md`
- `mechanics/experience/parts/adoption-federation/README.md`
- `mechanics/experience/parts/governance-runtime-boundary/README.md`
- `mechanics/experience/parts/office-release-train/README.md`

## Parts

See [PARTS.md](PARTS.md).

The current active parts are `protocol-integrity`, `certification-gate`,
`adoption-federation`, `governance-runtime-boundary`, and
`office-release-train`.

## Inputs

- experience verdict bundles, certification gate packets, adoption requests,
  owner consent refs, shadow proofs, compatibility refs, governance verdict
  packets, office contours, release train packets, rollback drills, watchtower
  alarms, runtime-boundary verdicts, and ToS/KAG boundary refs;
- public-safe schemas and examples that shape verdict packets;
- source proof bundles that explicitly name Experience proof boundaries.

## Outputs

- bounded Experience proof readings;
- protocol, certification, adoption, governance, office, and release-train
  verdict support packets;
- fixture family contracts and schema/example pairs for local validation;
- owner handoff notes or adjacent bundle route notes;
- no live workspace runtime, office installation, release approval, operator
  certification, memory canon, route activation, or owner-local adoption.

## Stronger Owner Split

`Agents-of-Abyss` owns Experience law, release posture, adoption route language,
owner-routing grammar, and stop-lines.
`abyss-stack` owns live workspace runtime, services, storage, lifecycle, and
deployment behavior.
`aoa-agents` owns actor, office, role, assistant, and handoff posture.
`aoa-playbooks` owns recurring adoption, release, office, service, and rollback
choreography.
`aoa-routing` owns live routing behavior and context-router implementation.
`aoa-memo` owns memory objects, recall, provenance, and candidate adoption truth.
`aoa-sdk` owns typed helper and compatibility APIs.
`aoa-stats` owns derived observability and movement summaries.
`aoa-skills` owns executable workflow skill truth.
`aoa-techniques` owns reusable practice and technique truth.
`Tree-of-Sophia` owns authored meaning and canon.
Owner-local repositories accept or reject live adoption, offices, releases, and
service behavior.

`aoa-evals` owns bounded adoption proof, certification checks, regression
evidence, verdict packet contracts, report interpretation, and local
support-surface validation.

Reviewed runtime distillation candidate adoption now routes through
`mechanics/distillation/parts/runtime-candidate-adoption/`. Experience keeps
generic adoption, consent, shadow, compatibility, federation, and KAG/ToS
boundary proof support.

## Stop-Lines

Do not use this package to claim:

- live workspace runtime or service dispatch;
- office installation or assistant operational authority;
- operator certification, release approval, deployment approval, or rollout
  promotion;
- owner-local adoption, consent, or acceptance;
- hidden memory sovereignty, recall authority, or memo canon;
- live router behavior or routing-layer authorship of meaning;
- direct KAG promotion into owner repos;
- direct Tree-of-Sophia runtime write or ToS-authored meaning;
- broad Experience success beyond the bounded proof object.

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) only when old root docs, examples, schemas,
fixtures, or test placement must be audited. New Experience proof work starts
from this README, [PARTS.md](PARTS.md), and the active parts.

## Validation

```bash
python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py
python -m pytest -q mechanics/experience/parts/certification-gate/tests
python -m pytest -q mechanics/experience/parts/adoption-federation/tests
python -m pytest -q mechanics/experience/parts/governance-runtime-boundary/tests
python -m pytest -q mechanics/experience/parts/office-release-train/tests
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
