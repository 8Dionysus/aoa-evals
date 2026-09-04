# Owner Skill Validation

This on-demand route checks the repository skill source and the stronger
`aoa-skills` port contract. Structural success does not prove usefulness,
routing quality, installed parity, or outcomes.

## Repository checks

```bash
python skills/aoa-evals-skills/scripts/eval_contract_packet.py --help
```

## Cross-owner port check

Set `AOA_SKILLS_ROOT` to the exact prepared `aoa-skills` checkout.

```bash
python "${AOA_SKILLS_ROOT:?set AOA_SKILLS_ROOT}/scripts/validate_home_skill_port.py" --owner-root . --manifest skills/port.manifest.json
```

When `skills-ref` is installed, its portable-shape check is an additional
environment-specific observation:

```bash
skills-ref validate skills/aoa-evals-skills
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../VALIDATION.md#non-mutating-checks).
