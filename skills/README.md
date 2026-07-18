# aoa-evals Skill Home

This directory is the canonical home for callable procedures owned specifically
by `aoa-evals`. It is not a mirror of the shared AoA skill catalog.

## Admitted bundle

| Bundle | Internal modes | Visibility | Admission |
| --- | --- | --- | --- |
| `aoa-evals` | `select`, `review`, `evolve` | OS-user-advertised | `docs/decisions/AOA-EV-D-0247-aoa-evals-owner-skill-bundle.md` |

The modes share one central-proof trigger family, authority ladder, typed
relations, result ABI, and coexistence boundary. They remain one bundle until
held-out manual work proves that separate prompt-visible procedures improve
outcomes.

`port.manifest.json` declares the admitted source and its selection by the
single OS-level `os-user-default` profile. Canonical files live under
`skills/aoa-evals/`; this repository does not duplicate the globally installed
bundle under `.agents/skills`.

## Verification posture

Manual tasks establish usefulness. Working validation guidance lives in
`skills/AGENTS.md`. The pinned `aoa-skills` source check validates identity,
admission, and package digest; the OS profile installer separately verifies
the managed user copy. Neither check proves routing, model portability,
safety, or outcome benefit.
