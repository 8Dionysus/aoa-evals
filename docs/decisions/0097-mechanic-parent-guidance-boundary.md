# Mechanic Parent Guidance Boundary

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Context

The mechanics refactor now makes `mechanics/<parent>/parts/<part>/` the home for
active proof payload. The part payload inventory guard already protects files
below each part, but a parent-level `mechanics/<parent>/docs/` directory could
still become a quiet bypass.

That bypass matters because a guide can be either mechanic-wide guidance or
part-owned payload. If those classes are not separated, artifact-form docs can
sit beside `README.md`, `DIRECTION.md`, `PARTS.md`, and `PROVENANCE.md` and look
like parent authority even when they belong to one concrete part.

## Options Considered

- Forbid every parent-level `docs/` directory.
- Allow parent-level docs whenever a parent package names them.
- Allow only explicitly allowlisted mechanic-wide guidance, and force
  part-owned payload docs under `parts/<part>/docs/`.

## Decision

Parent-level `mechanics/<parent>/docs/` is allowed only for mechanic-wide
guidance that is explicitly allowlisted by repository validation.

Current allowlisted parent guidance:

- `mechanics/agon/docs/AGON_EVAL_OWNER_HANDOFFS.md`
- `mechanics/agon/docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md`
- `mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md`

Part-owned payload docs must live under the owning part. The Titan canary guides
therefore live under
`mechanics/titan/parts/seed-boundary/docs/`, beside the seed-boundary part that
owns the current canary source family.

Allowlisting is not enough by itself. Every mechanic-wide guidance doc must
also expose the parent guidance content contract:

- `## Role`;
- `## Mechanic-wide Scope`;
- `## Source Surfaces`;
- `## Stronger Owner Split`;
- `## Stop-Lines`;
- `## Validation`.

`scripts/validate_repo.py` rejects:

- unallowlisted parent-level docs;
- empty parent-level `docs/` directories;
- unexpected files or directories directly under a mechanic parent;
- missing allowlisted mechanic-wide guidance docs.
- allowlisted parent guidance that lacks the content contract sections.

## Rationale

This preserves convex topology. The parent route holds the mechanic-level map
and current direction; the part route holds the concrete payload that can grow.

The distinction keeps broad Agon and Recurrence boundary/program guidance
available without reopening the earlier mistake where artifact forms such as
canaries became parent-level topology.

## Consequences

- Positive: parent-level docs can no longer become a hidden payload lane.
- Positive: allowlisted mechanic-wide guidance can no longer be a thin
  prose-only authority surface.
- Positive: Titan canary guide ownership is visibly part-local.
- Positive: future parent-wide guidance additions require an explicit topology
  decision and validator allowlist update.
- Tradeoff: moving a guide between parent and part scope now requires updating
  references and validation in the same slice.

## Boundaries

This decision does not forbid mechanic-wide guidance.

It does not let parent guidance replace `DIRECTION.md`, `PARTS.md`,
part-local `README.md`, or part-local validation.

It does not move source proof bundles from `evals/` and does not make a guide
stronger than the proof objects or stronger owners it routes.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_parent_guidance_boundary
python scripts/validate_repo.py
```
