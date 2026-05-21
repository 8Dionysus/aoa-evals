# Agon Court Prebinding

## Role

This source note defines the pre-verdict court-facing check surface for Agon
work inside `aoa-evals`.

It prepares candidate checks for closure legality, evidence floor, trace
integrity, contradiction status, assistant boundary drift, summon intent, and
delta legitimacy.

## Route

```text
court pressure
-> prebinding seed
-> generated prebinding registry
-> precheck validation
-> bundle-local review or stronger-owner handoff
```

## Reads

Use this note when a future Agon bundle or registry record needs to explain why
court pressure is inspectable here before any arena authority exists.

The prebinding may describe what would need review. It does not make the review
decision.

## Boundary

`aoa-evals` owns prebinding shape, deterministic registry derivation, and local
proof-review boundaries.

Agents-of-Abyss owns Agon law, court meaning, closure authority, arena protocol,
and any future live verdict route.

## Validation

Use the validation route in:

- `mechanics/agon/parts/court-prebinding/README.md`
- `mechanics/agon/parts/court-prebinding/VALIDATION.md`
- `mechanics/agon/parts/AGENTS.md`

Registry output should remain a candidate surface. It is not court law, closure
grant, live summon, scar, memory write, rank mutation, or Tree of Sophia
promotion.
