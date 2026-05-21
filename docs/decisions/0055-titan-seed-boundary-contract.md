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
