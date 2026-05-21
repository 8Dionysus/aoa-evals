# Agon Eval Prebinding Model

## Role

This model describes what a single Agon prebinding record is allowed to carry.

Each prebinding maps recurrence review pressure, lawful moves, gate triggers,
mechanical trial playbooks, and evidence floors into a review candidate.

## Record Shape

A useful prebinding keeps these axes visible:

- source pressure or owner ref;
- gate trigger;
- lawful move candidates;
- required evidence floor;
- forbidden effects;
- review output that remains candidate-only.

## Reads

Read the model from the part README first, then use this note to understand why
prebindings exist as prepared proof surfaces rather than verdicts.

## Boundary

A prebinding can prepare a question that a future Agon session may call when
protocol law exists. It does not answer the question by itself.

The live verdict, closure, summon, arena, scar, rank, memory, and Tree of Sophia
routes remain with their stronger owners.

## Validation

Use:

- `mechanics/agon/parts/court-prebinding/README.md`
- `mechanics/agon/parts/court-prebinding/schemas/`
- `mechanics/agon/parts/court-prebinding/generated/`

The schema and registry should preserve the candidate-only shape described
here.
