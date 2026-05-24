# 0055 Titan Seed-boundary Contract

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/titan/parts/seed-boundary/`

## Context

`mechanics/titan/` is the active parent mechanic, not `titan-canaries`.
The current Titan artifacts are still seed-defined canary YAML files, but they
carry high-risk pressure: named Titan identity, summon discipline, memory
posture, runtime roster, gate payloads, bridge payloads, and closeout receipts.

The parent README and `PARTS.md` already described the route. The local
`seed-boundary` part README was still too thin: it named the seed family and
validation commands, but did not directly expose inputs, outputs, stronger
owner split, and stop-lines at the point where future canary work enters.

## Decision

Make `mechanics/titan/parts/seed-boundary/README.md` carry the active
part-level contract for Titan seed canaries:

- inputs from Titan boundary pressure and seed-local route law;
- outputs as validator-visible seed shape and future scorer conversion posture;
- stronger owner split against `aoa-agents`, `aoa-memo`, and runtime owners;
- stop-lines against incarnation proof, summon authority, memory sovereignty,
  runtime activation, hidden arena permission, mutation-gate bypass, and
  judgment-gate bypass.

Add validator and test coverage so that the seed-boundary README cannot lose
that local contract while `titan` remains the parent mechanic.

## Rationale

Canary is an artifact form. Titan is the mechanic parent. Keeping the contract
at the part boundary lets the canary family grow without reintroducing
`titan-canaries` as active topology.

The local eval layer can shape and validate seed canaries. It cannot certify
Titan incarnation, lawful summon, memory authority, runtime activation, or
stronger owner law.

## Consequences

- Positive: future Titan seed work starts from `seed-boundary`, not a new parent
  named after the artifact form.
- Positive: the stronger-owner split is visible before editing a canary route.
- Positive: `python scripts/validate_repo.py` now catches drift in the
  seed-boundary part README.
- Tradeoff: Titan seed-boundary wording is now tighter than a short route card.

## Boundaries

This decision does not convert Titan seed canaries into executable scorers,
full eval bundles, runtime receipts, summon authorization, memory write
permission, or incarnation proof.

It does not transfer `aoa-agents` Titan role/bearer/incarnation law,
`aoa-memo` memory authority, or runtime activation truth into `aoa-evals`.

## Validation

- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_validate_repo.py -k 'titan_seed_boundary or titan_canary'`

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/titan/parts/seed-boundary/README.md` owns the
  part-level contract for Titan seed canaries.
- Still valid: `titan` remains the parent mechanic; canary YAML payloads remain
  under `mechanics/titan/parts/seed-boundary/seeds/`.
- Changed: Titan seed-boundary route surfaces now express claim-limit pressure
  as owner routes instead of negative boundary prose.
- Changed: `scripts/validate_repo.py` requires the current seed-boundary route
  wording and rejects stale negative claim-limit phrases on the active Titan
  seed-boundary route surfaces.
- Changed: seed-local `AGENTS.md` now exposes an Operating Card and boundary
  route table while executable checks route to the parent `parts/AGENTS.md`
  lane.
- Source surfaces updated: `mechanics/titan/AGENTS.md`,
  `mechanics/titan/DIRECTION.md`, `mechanics/titan/PARTS.md`,
  `mechanics/titan/parts/README.md`,
  `mechanics/titan/parts/seed-boundary/README.md`,
  `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`,
  `mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md`,
  `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`,
  `mechanics/titan/parts/seed-boundary/seeds/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.

## Review Log

### 2026-05-24 - Seed-boundary route tables

- Previous assumption: Titan seed-boundary claim limits could stay as direct
  negative boundary prose once the part contract existed.
- New reality: Titan seed surfaces are safer for low-context agents when each
  high-risk pressure names its owner route.
- Reason: Titan canary language touches incarnation, summon, memory, runtime,
  mutation-gate, and judgment-gate authority. The active route surface should
  tell the agent where each pressure belongs before it edits seed wording.
- Source surfaces updated: Titan package, part, seed, and guide route wording;
  validator tokens; validator regression coverage.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k "titan_seed_boundary or titan_canary"`,
  `python scripts/validate_repo.py`, `python scripts/validate_semantic_agents.py`,
  generated-surface `--check` commands, `python -m pytest -q`, and
  `git diff --check`.

### 2026-05-24 - Seed-local agent route card

- Previous assumption: the seed-local `AGENTS.md` could remain a compact
  boundary list because the parent and part surfaces already carried the
  stronger owner map.
- New reality: this was the last mechanics `AGENTS.md` without an Operating
  Card, so low-context agents still lacked a uniform role/input/output/owner
  route at the seed payload boundary.
- Reason: Titan seed canaries are high-pressure payloads; the file that guards
  `titan*.yaml` must name seed-local input, output, owner, next route, tools,
  and validation ownership before canary edits begin.
- Source surfaces updated:
  `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`,
  `mechanics/titan/parts/seed-boundary/seeds/README.md`,
  `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: root validator, semantic AGENTS validation, titan canary focused
  tests, generated-surface checks, full pytest, and diff whitespace check.

### 2026-05-24 - Lower parts index operating route

- Previous assumption: the lower Titan parts README could stay as a short
  pointer to `seed-boundary` because parent, part, guide, and seed-local route
  surfaces carried the stronger-owner map.
- New reality: `mechanics/titan/parts/README.md` now exposes the lower-index
  operating card for Titan proof-seed parts, including owner pressure routes
  and admission tests for future scorer or topic-split pressure.
- Reason: Titan canary edits are high-pressure even before an agent opens the
  seed files. The lower parts index now names seed payload home, validation
  lane, stronger-owner route, and the conditions for future part growth.
- Source surfaces updated: `mechanics/titan/parts/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: focused lower-index validator tests, Titan canary validation,
  root validation, semantic AGENTS validation, generated catalog check, diff
  whitespace check, and full pytest.
