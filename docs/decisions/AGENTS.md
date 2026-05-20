# AGENTS.md

## Applies to

`docs/decisions/` and durable decision notes inside it.

## Role

This lane preserves structural, workflow, topology, authority, validation, and
compatibility decisions for `aoa-evals`.

Decision notes explain why a route was chosen. They do not replace proof
bundles, root design, architecture docs, validators, generated readers, runtime
candidates, receipts, or sibling owner truth.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/decisions/README.md`
5. `docs/decisions/TEMPLATE.md`
6. the source surface whose route or authority the decision records

## Boundaries

- Record a decision only when future contributors need the rationale.
- Keep evidence, working notes, generated output, and runtime facts as context;
  do not promote them into decision authority.
- Name rejected options or accepted tradeoffs when they shaped the decision.
- Route sibling-owner meaning back to that sibling. A local decision may define
  compatibility posture, not sibling truth.
- Avoid decision clutter for ordinary implementation details that are already
  obvious from the diff and validation.

## Validation

Run the narrow docs checks after editing this lane:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If a decision changes generated, schema, quest, bundle, receipt, runtime, or
sibling-reference surfaces, run the owning builder or validator for that surface
too.

## Closeout

Report which decision was added or changed, which source surface it constrains,
what validation ran, what existing drift remains, and which follow-up route the
decision enables.
