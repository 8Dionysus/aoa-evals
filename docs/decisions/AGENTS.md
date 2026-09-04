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
| role | durable decision rationale lane plus generated lookup-index route |
| input | structural choices, owner splits, topology changes, validation authority, workflow route changes, and compatibility decisions |
| output | accepted rationale, canonical decision ID, source-owned index metadata, and generated lookup index parity |
| owner | decision record for why; source surface for what; `docs/decisions/indexes/` for generated lookup only |
| next route | decision index, generated lookup indexes, decision template, source surface being explained, or root/docs/mechanics route card |
| tools | `scripts/generate_decision_indexes.py`, root validator, and semantic AGENTS validator |
| validation | this card's `Validation` section |

## Owner Routes

| Need | Owner route |
| --- | --- |
| current proof claim | bundle-local `EVAL.md` and `eval.yaml` |
| root design or architecture meaning | `DESIGN.md`, `DESIGN.AGENTS.md`, or `docs/architecture/ARCHITECTURE.md` |
| validator behavior | `scripts/AGENTS.md`, validator source, and focused tests |
| generated reader meaning | source surface, builder, generated reader, and validator |
| runtime candidate, receipt, or sibling truth | owning mechanic, receipt surface, runtime owner, or sibling repository |
| decision rationale | this lane plus `docs/decisions/TEMPLATE.md` |
| decision lookup | source decision `Index Metadata`, then generated `docs/decisions/indexes/` read models |

## Route Rules

- Record a decision only when future contributors need the rationale.
- Give every decision a canonical `Decision ID: AOA-EV-D-####` whose filename
  prefix matches the ID exactly.
- Give every decision an `## Index Metadata` block so lookup indexes can be
  regenerated from source notes instead of hand-maintained crosswalks.
- Keep old short numbered decision paths in git/PR history only. Do not add
  compatibility maps or stub files for retired paths.
- Keep evidence, working notes, generated output, and runtime facts as context;
  do not promote them into decision authority.
- Name rejected options or accepted tradeoffs when they shaped the decision.
- Route sibling-owner meaning back to that sibling. A local decision may define
  compatibility posture, not sibling truth.
- Avoid decision clutter for ordinary implementation details that are already
  obvious from the diff and validation.

## Amendment Route

Use the human [decision index amendment route](README.md#amendment-route). This
card keeps only the stop-line: preserve historical rationale, update the
current owner source in the same slice, and regenerate indexes from decision
source rather than patching generated lookup files.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.
The route covers `validate_repo.py` and decision-index parity without copying command sequences into this card.

After editing this lane, follow the narrow docs checks in [VALIDATION.md](VALIDATION.md).

When decision metadata changes, run the local validation route
before the `--check` form.

If a decision changes generated, schema, quest, bundle, receipt, runtime, or
sibling-reference surfaces, run the owning builder or validator for that surface
too.

## Closeout

Report which decision was added or changed, whether generated lookup indexes
were refreshed, which source surface it constrains, what validation ran, what
existing drift remains, and which follow-up route the decision enables.
