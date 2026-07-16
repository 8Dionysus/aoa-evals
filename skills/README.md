# aoa-evals Skill Home

This directory is the canonical home for callable procedures owned specifically
by `aoa-evals`. It is not a mirror of the shared AoA skill catalog.

## Admitted bundle

| Bundle | Internal modes | Visibility | Admission |
| --- | --- | --- | --- |
| `aoa-evals` | `select`, `review`, `evolve` | repo-advertised | `docs/decisions/AOA-EV-D-0247-aoa-evals-owner-skill-bundle.md` |

The modes share one central-proof trigger family, authority ladder, typed
relations, result ABI, and coexistence boundary. They remain one bundle until
held-out manual work proves that separate prompt-visible procedures improve
outcomes.

`port.manifest.json` declares the admitted source and exact derived Codex
projection. Canonical files live under `skills/aoa-evals/`; files under
`.agents/skills/aoa-evals/` are generated copies.

## Verification posture

Manual tasks establish usefulness. Working validation guidance lives in
`skills/AGENTS.md`. Projection parity is checked in CI by the exact
`aoa-skills` action commit pinned in `.github/workflows/repo-validation.yml`.
A green structural check does not prove routing, model portability, safety, or
outcome benefit.
