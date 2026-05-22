# AGENTS.md

## Applies to

`docs/decisions/` and durable decision notes inside it.

## Role

This lane preserves structural, workflow, topology, authority, validation, and
compatibility decisions for `aoa-evals`.

Decision notes explain why a route was chosen. Current proof, design,
architecture, validation, generated-reader, runtime-candidate, receipt, and
sibling-owner authority stays with the owning source surface.

## Operating Card

| Field | Route |
| --- | --- |
| role | durable decision rationale lane |
| input | structural choices, owner splits, topology changes, validation authority, workflow route changes, and compatibility decisions |
| output | accepted rationale that points back to current source surfaces |
| owner | decision record for why; source surface for what |
| next route | decision index, decision template, source surface being explained, or root/docs/mechanics route card |
| tools | root validator and semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/decisions/README.md`
5. `docs/decisions/TEMPLATE.md`
6. the source surface whose route or authority the decision records

## Owner Routes

| Need | Owner route |
| --- | --- |
| current proof claim | bundle-local `EVAL.md` and `eval.yaml` |
| root design or architecture meaning | `DESIGN.md`, `DESIGN.AGENTS.md`, or `docs/ARCHITECTURE.md` |
| validator behavior | `scripts/AGENTS.md`, validator source, and focused tests |
| generated reader meaning | source surface, builder, generated reader, and validator |
| runtime candidate, receipt, or sibling truth | owning mechanic, receipt surface, runtime owner, or sibling repository |
| decision rationale | this lane plus `docs/decisions/TEMPLATE.md` |

## Route Rules

- Record a decision only when future contributors need the rationale.
- Keep evidence, working notes, generated output, and runtime facts as context;
  do not promote them into decision authority.
- Name rejected options or accepted tradeoffs when they shaped the decision.
- Route sibling-owner meaning back to that sibling. A local decision may define
  compatibility posture, not sibling truth.
- Avoid decision clutter for ordinary implementation details that are already
  obvious from the diff and validation.

## Amendment Route

When an accepted decision needs a current-route update, preserve the original
record and add the change as a dated update near the affected section.

Use this shape:

- keep the original rationale readable;
- strike through the superseded line or block when the old wording would mislead
  the next agent;
- add `### YYYY-MM-DD Update` with the current route, owner surface, and
  validation lane;
- update the source surface that owns active behavior in the same slice.

Closeout and pull request text should state the active route, owner surface, and
validation evidence.

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
