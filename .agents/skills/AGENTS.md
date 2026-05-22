# AGENTS.md

## Purpose

`.agents/skills/` is an agent-facing companion surface for operating on eval bundles.

It may help agents run audits, inspect bundles, or publish bounded reports.
Eval doctrine stays with bundle-local `EVAL.md` and `eval.yaml`.

## Operating Card

| Field | Route |
| --- | --- |
| role | exported support guidance for agents working on proof surfaces |
| input | support-skill guidance, audit route help, bundle inspection help, and bounded report workflows |
| output | support guidance that routes back to source proof owners |
| owner | source audit, bundle, or builder surface behind the exported guidance |
| next route | target bundle, audit mechanic, report owner, or builder source |
| tools | root validation and semantic AGENTS validation |
| validation | this card's `Verify` section |

Keep exported guidance bounded: an eval proves only the stated object, claim type, fixtures, scoring posture, and blind spots.

Source changes route to the source audit, bundle, or builder before exported
skill files change.

Keep public-safe examples and commands. Hidden telemetry, private benchmark
data, and secret-bearing fixtures stay outside checked-in support guidance.

## Verify

Run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
