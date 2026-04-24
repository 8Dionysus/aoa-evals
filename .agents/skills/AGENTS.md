# AGENTS.md

## Guidance for `.agents/skills/`

`.agents/skills/` is an agent-facing companion surface for operating on eval bundles.

It may help agents run audits, inspect bundles, or publish bounded reports, but it must not change eval doctrine. Bundle-local `EVAL.md` and `eval.yaml` remain the claim-owning surfaces.

Keep exported guidance bounded: an eval proves only the stated object, claim type, fixtures, scoring posture, and blind spots.

Do not hand-edit exported skill files as a substitute for changing the source audit, bundle, or builder.

Keep public-safe examples and commands. No hidden telemetry, private benchmark data, or secret-bearing fixtures.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
