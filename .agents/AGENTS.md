# AGENTS.md

## Applies to

`.agents/` agent-facing lanes and companion guidance.

## Role

`.agents/` is the durable home for maintained agent-facing lanes and exported
support skills in `aoa-evals`.

It routes agents that operate on proof surfaces. It does not own eval bundle
meaning, generated proof truth, runtime authority, receipt authority, sibling
owner truth, or repo doctrine.

Current maintained lanes:

- `.agents/spark/` for the Spark fast-loop lane.

This district is not proof canon.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.AGENTS.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `docs/LEGACY_NAMING.md`
5. the target lane or support-surface `AGENTS.md`
6. `docs/decisions/0017-spark-agent-lane-placement.md` for Spark lane
   placement changes

## Boundaries

- Keep maintained lanes under `.agents/<lane>/`.
- Keep exported skill guidance under `.agents/skills/`.
- Do not move bundle, generated, receipt, runtime, or sibling-owner truth into
  `.agents/`.
- Do not hand-edit generated readers from an agent lane.
- Do not let fast-loop lane guidance strengthen a bounded proof claim.
- Preserve public-safe wording; no private logs, hidden benchmark data, or
  host-local secrets.

## Validation

After editing `.agents/` route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
```

If a lane changes generated readers, bundle contracts, or proof reports, also
run the owning builder or test for that surface.

## Closeout

Report which agent lane or support surface changed, which proof owner surface
it routes, what validation ran, and which proof authority stayed outside
`.agents/`.
