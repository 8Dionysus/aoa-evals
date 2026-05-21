# 0063 Experience Part Contract Guard

## Status

Accepted.

## Context

`mechanics/experience/` is the active AoA-aligned parent for eval-side
Experience proof. The parent README and `PARTS.md` already name the owner
split and stop-lines, but the five active part README files still used thin
`Boundary` sections.

That is risky because Experience proof touches adoption, certification,
governance, runtime-boundary, office, service, release-train, KAG, ToS, memo,
and routing surfaces. Without part-local contracts, future edits can turn
bounded verdict support into live runtime activation, operator certification,
owner-local adoption, governance authority, memory canon, routing authorship,
or broad Experience success.

## Decision

Require each active Experience part README to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The protected parts are:

- `mechanics/experience/parts/protocol-integrity/README.md`
- `mechanics/experience/parts/certification-gate/README.md`
- `mechanics/experience/parts/adoption-federation/README.md`
- `mechanics/experience/parts/governance-runtime-boundary/README.md`
- `mechanics/experience/parts/office-release-train/README.md`

The parts keep their current active routes. No new parent packages are created
for certification, adoption, governance, office, service, release, KAG, ToS,
memo, or routing verdict forms.

## Consequences

- Future Experience part edits must keep owner split and stop-lines explicit.
- Bounded verdict support remains below live runtime, office, release,
  adoption, certification, governance, memory, routing, KAG, and ToS authority.
- Runtime distillation candidate adoption remains outside Experience and
  routes through `mechanics/distillation/parts/runtime-candidate-adoption/`.
- Experience support surfaces remain parts under `experience`, not
  proof-adjective parent mechanics.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k experience_part_readmes
python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py mechanics/experience/parts/certification-gate/tests/test_experience_certification_gate_integrity.py mechanics/experience/parts/certification-gate/tests/test_experience_wave2_seed_contracts.py mechanics/experience/parts/adoption-federation/tests/test_experience_wave3_seed_contracts.py mechanics/experience/parts/governance-runtime-boundary/tests/test_experience_wave4_seed_contracts.py mechanics/experience/parts/office-release-train/tests/test_experience_wave5_seed_contracts.py
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
