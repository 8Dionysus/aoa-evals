# Release Support / Parts Route

`mechanics/release-support/parts/` is the lower index for release-support-owned
state artifacts. Use it after the parent Release Support route has selected a
release-support operation and the next agent needs the exact part, payload
home, owner route, tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for release-support readiness, closeout, and PR handoff artifacts |
| input | bounded release scope, changelog narrative, release procedure, repository validation posture, handoff evidence, audit evidence, or live landing pressure |
| output | readiness audit route, strategic closeout route, PR handoff route, release-route review artifact, or live owner-evidence handoff |
| owner | root release entrypoints stay in root/docs/scripts/GitHub lanes; release-support parts own state artifacts; bundle claims stay with source proof surfaces |
| next route | `mechanics/release-support/PARTS.md`, selected part README, root release entrypoint, GitHub evidence, source bundle, and parent validation lane |
| tools | release check, repo validator, semantic AGENTS validator, GitHub validation, and focused release-support checks through `mechanics/release-support/AGENTS.md#validation` |
| validation | `mechanics/release-support/parts/AGENTS.md#validation` and `mechanics/release-support/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `readiness-audit/` | Readiness Audit artifact for accumulated strategic refactor diff | `readiness-audit/README.md` |
| `strategic-closeout/` | Strategic Closeout artifact for requirement-by-requirement goal review | `strategic-closeout/README.md` |
| `pr-handoff/` | PR Handoff snapshot; current git and GitHub evidence own live branch, PR, CI, and merge status | `pr-handoff/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| public release narrative | `CHANGELOG.md` |
| release procedure | `docs/RELEASING.md` |
| local release gate | `scripts/release_check.py` |
| GitHub landing gate | `.github/workflows/repo-validation.yml` and observed GitHub check evidence |
| tag, GitHub Release, PR approval, merge, or goal completion | live git, GitHub, tag, release, and current-goal evidence |
| eval claim strength | bundle-local proof surfaces |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| release-prep readiness needs a local artifact | readiness audit has bounded scope and validation posture | `readiness-audit/README.md` |
| strategic goal closeout needs requirement-by-requirement audit | closeout artifact can name evidence and residual risk | `strategic-closeout/README.md` |
| PR landing needs a pre-PR handoff snapshot | handoff artifact can point to live git/GitHub evidence without replacing it | `pr-handoff/README.md` |
| live publication state changes | current git, GitHub, tag, or release evidence owns the fact | route outward before adding a Release Support part |
