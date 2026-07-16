# AGENTS.md

## Applies to

`.agents/` agent-facing lanes and companion guidance.

## Role

`.agents/` is the durable home for maintained agent-facing lanes in
`aoa-evals`.

It routes agents that operate on proof surfaces. Proof authority stays with the
source bundle, generated reader, runtime owner, receipt owner, sibling owner,
or repo doctrine surface named by the task.

## Operating Card

| Field | Route |
| --- | --- |
| role | maintained agent-facing lane district |
| input | agent-lane guidance, Spark lane work, and proof-surface route pressure |
| output | scoped agent route or handoff toward the proof owner |
| owner | `.agents/AGENTS.md` for lane placement; lane-local `AGENTS.md` for local posture |
| next route | `.agents/spark/AGENTS.md`, the proof owner surface, or top-level `skills/` after an owner-admitted repository skill exists |
| tools | root validation, semantic AGENTS validation, nested AGENTS validation |
| validation | this card's `Validation` section |

Current maintained lanes:

- `.agents/spark/` for the Spark fast-loop lane.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.AGENTS.md`
3. `docs/architecture/PROOF_TOPOLOGY.md`
4. `docs/architecture/LEGACY_NAMING.md`
5. the target lane's `AGENTS.md`
6. `docs/decisions/AOA-EV-D-0017-spark-agent-lane-placement.md` for Spark lane
   placement changes
7. `docs/decisions/AOA-EV-D-0246-owner-skill-projection-boundary.md` before
   adding a repository skill home or projection

## Owner Routes

- Keep maintained lanes under `.agents/<lane>/`.
- Keep an owner-admitted repository skill's canonical source under top-level
  `skills/`, never under `.agents/`.
- Keep `.agents/skills/` absent unless it is a derived projection of that
  admitted home. No repository skill home is currently admitted.

| Need | Owner route |
| --- | --- |
| bundle proof meaning | bundle-local `EVAL.md` and `eval.yaml` |
| generated reader updates | `generated/AGENTS.md` and the owning builder |
| receipt authority | publication-receipts mechanic or bundle-local report surface |
| runtime authority | runtime owner or audit intake route |
| sibling-owner truth | owning sibling repository |
| repo doctrine or topology | root/docs source surfaces |

Fast-loop lane guidance stays below bounded proof claims. Public-safe wording is
the lane standard; private logs, hidden benchmark data, and host-local secrets
stay outside checked-in agent lanes.

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

Report which agent lane changed, which proof owner surface
it routes, what validation ran, and which proof authority stayed outside
`.agents/`.
