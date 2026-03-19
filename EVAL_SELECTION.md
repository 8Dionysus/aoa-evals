# Eval Selection

This file is the repository-wide chooser for public eval bundles.

Use it when you need one bounded evaluation surface now,
rather than reading the full `EVAL_INDEX.md` first.

This surface prefers:
- bounded selection
- explicit claim classes
- modest public states
- honest uncertainty

See also:
- [EVAL_INDEX](EVAL_INDEX.md)
- [Documentation Map](docs/README.md)

## Pick by question

### I need to know whether a non-trivial change stayed scoped and honestly verified
- `aoa-bounded-change-quality`

### I need to know whether an agent respected approval, authority, or risk boundaries
- `aoa-approval-boundary-adherence`

## Pick by category

| category | use when | starter bundles |
|---|---|---|
| `workflow` | You care about multi-step execution quality, not just isolated answers. | `aoa-bounded-change-quality` |
| `boundary` | You care about scope, authority, approval, or policy adherence. | `aoa-approval-boundary-adherence` |

## Pick by public maturity

Current starter posture is intentionally modest.

### If you need a stable public default now
There is no `canonical` eval yet.

### If you need a bounded comparison surface
Prefer future `baseline` bundles once they exist.

### If you need an early public proof sketch
Use `draft` bundles carefully and read their boundaries, blind spots, and interpretation notes before drawing conclusions.

## Pick by claim style

| claim style | use when | likely bundles |
|---|---|---|
| bounded workflow quality | You want to know whether a process stayed disciplined and reviewable. | `aoa-bounded-change-quality` |
| authority and safety boundary adherence | You want to know whether the agent respected decision boundaries. | `aoa-approval-boundary-adherence` |

## Reader guidance

When choosing an eval, ask:

1. what claim do I actually need to support?
2. do I need a one-run signal or a comparison surface?
3. am I judging workflow quality, artifact quality, safety boundaries, or regression?
4. what would this eval still fail to tell me?
5. would a pass here support a bounded claim, or tempt me into saying too much?

If the bundle does not answer those questions clearly,
pick a narrower eval or defer strong conclusions.

## Notes

- This chooser is intentionally bounded and modest.
- As the corpus grows, later generated surfaces may add filters by status, object under evaluation, baseline mode, and verdict shape.
- Prefer `baseline` or `canonical` bundles for stronger comparison claims once the public corpus reaches that stage.
