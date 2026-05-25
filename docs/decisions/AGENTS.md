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
| output | accepted rationale, source-owned index metadata, and generated lookup index parity |
| owner | decision record for why; source surface for what; `docs/decisions/indexes/` for generated lookup only |
| next route | decision index, generated lookup indexes, decision template, source surface being explained, or root/docs/mechanics route card |
| tools | `scripts/generate_decision_indexes.py`, root validator, and semantic AGENTS validator |
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
| root design or architecture meaning | `DESIGN.md`, `DESIGN.AGENTS.md`, or `docs/architecture/ARCHITECTURE.md` |
| validator behavior | `scripts/AGENTS.md`, validator source, and focused tests |
| generated reader meaning | source surface, builder, generated reader, and validator |
| runtime candidate, receipt, or sibling truth | owning mechanic, receipt surface, runtime owner, or sibling repository |
| decision rationale | this lane plus `docs/decisions/TEMPLATE.md` |
| decision lookup | source decision `Index Metadata`, then generated `docs/decisions/indexes/` read models |

## Route Rules

- Record a decision only when future contributors need the rationale.
- Give every numbered decision an `## Index Metadata` block so lookup indexes
  can be regenerated from source notes instead of hand-maintained crosswalks.
- Keep evidence, working notes, generated output, and runtime facts as context;
  do not promote them into decision authority.
- Name rejected options or accepted tradeoffs when they shaped the decision.
- Route sibling-owner meaning back to that sibling. A local decision may define
  compatibility posture, not sibling truth.
- Avoid decision clutter for ordinary implementation details that are already
  obvious from the diff and validation.

## Amendment Route

When an accepted decision needs a current-route update, preserve the original
record and add the change as review history.

Use `## Review Log` for dated reviews:

```markdown
## Review Log

### YYYY-MM-DD - Route or behavior changed

- Previous assumption:
- New reality:
- Reason:
- Source surfaces updated:
- Validation:
```

Use `## Current Applicability` when the decision still matters but its active
route narrowed, moved, or was partly superseded:

```markdown
## Current Applicability

As of YYYY-MM-DD:

- Still valid:
- Changed:
- Superseded by:
```

Use this decision maintenance route:

- small clarification of the same decision: add a dated `Review Log` entry;
- application changed while the rationale still holds: add `Review Log` and
  `Current Applicability`;
- direction replaced by a new route: create the next numbered decision, set the
  old record `Status` to `Superseded`, and add `Superseded by: NNNN-...`;
- material made obsolete: record what aged out, why, and what replaces it in a
  dated review entry.

Use strikethrough only on the old operational line or block that would misroute the
next agent. Keep the original `Context`, `Options Considered`, `Decision`, and
`Rationale` readable as historical cause.

Update the source surface that owns active behavior in the same slice.

Closeout and pull request text should state the active route, owner surface, and
validation evidence.

## Validation

Run the narrow docs checks after editing this lane:

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

When decision metadata changes, run `python scripts/generate_decision_indexes.py`
before the `--check` form.

If a decision changes generated, schema, quest, bundle, receipt, runtime, or
sibling-reference surfaces, run the owning builder or validator for that surface
too.

## Closeout

Report which decision was added or changed, whether generated lookup indexes
were refreshed, which source surface it constrains, what validation ran, what
existing drift remains, and which follow-up route the decision enables.
