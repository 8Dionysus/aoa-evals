# Agent Index

This is the pass-through index for agents entering `aoa-evals`.

It tells an agent where it is in the repository shape, which authority class
the current file belongs to, and which stronger surface to open next. Source
truth, route law, generated readers, decisions, and validators keep their own
authority; this index connects them.

Use this index when a path needs an explicit owner route.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-facing pass-through index for agents |
| entry | start from the current path or from `README.md` |
| output | next owner surface and validation route |
| owner | `docs/` source guidance; executable commands stay in the nearest `AGENTS.md` |
| next route | `docs/architecture/PROOF_TOPOLOGY.md`, `mechanics/README.md`, or a bundle-local source file |
| validation | `docs/AGENTS.md#validation` and root `AGENTS.md#verify` |

## Canonical Chain

The repo should stay navigable in both directions:

```text
repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation
```

Top down, start from repository identity and narrow to the source or route that
owns the edit. Bottom up, start from the changed file and climb until the
owning authority class is explicit.

## First Orientation

| Agent question | Open next | Role |
| --- | --- | --- |
| What is this repository? | `README.md` | public proof-organ entry |
| What is the system form? | `DESIGN.md` and `DESIGN.AGENTS.md` | source design and agent-facing shape |
| Which class owns this artifact? | `docs/architecture/PROOF_TOPOLOGY.md` | authority-class topology |
| Which operation owns this proof support? | `mechanics/README.md` | operation atlas |
| Why does this route exist? | `docs/decisions/README.md` | durable rationale index |
| What is the current direction? | `ROADMAP.md` | direction and horizon order |
| What is executable route law here? | nearest `AGENTS.md` | local edit, validation, and closeout route |

## Authority Classes By Name

| Path shape | Authority class | Stronger surface |
| --- | --- | --- |
| `evals/<family>/<eval>/EVAL.md` and `eval.yaml` | source proof object | bundle-local files own the bounded claim |
| `docs/*.md` | root-owned guidance or topology | `docs/AGENTS.md` for edit route, target doc for meaning |
| `docs/decisions/*.md` | decision rationale | `docs/decisions/AGENTS.md` and the source surface being explained |
| `generated/*` | derived reader | `generated/AGENTS.md` plus the builder and source inputs |
| `quests/<lane>/<state>/*.yaml` | source quest record | `quests/AGENTS.md`, `QUESTBOOK.md`, and quest schemas |
| `mechanics/<parent>/` | mechanic parent operation | parent `AGENTS.md`, `README.md`, `DIRECTION.md`, `PARTS.md`, `PROVENANCE.md` |
| `mechanics/<parent>/parts/<part>/` | mechanic part operation | part `README.md`, `VALIDATION.md`, and parent `parts/AGENTS.md` |
| `.agents/` | maintained agent lane support | `.agents/AGENTS.md` and lane-local cards |
| `.aoa/live_receipts/` | receipt sidecar | `.aoa/live_receipts/AGENTS.md`; receipts stay below reports and bundles |

## Route-Card-Only Root Districts

These root directories are compatibility districts. Their names are short
because old root paths existed, but their current role is route-card-only:

- `config/`
- `examples/`
- `fixtures/`
- `manifests/`
- `reports/`
- `runners/`
- `schemas/`
- `scorers/`
- `templates/`

Agent expectation: those directories carry only `AGENTS.md` and `README.md`.
Active payloads belong under the owning bundle or mechanic part. The root
district README tells where that payload moved; the nearest `AGENTS.md` owns
the executable route.

## Mechanics Descent

Use this descent for mechanic-owned work:

```text
mechanics/README.md
-> mechanics/<parent>/README.md
-> mechanics/<parent>/DIRECTION.md
-> mechanics/<parent>/PARTS.md
-> mechanics/<parent>/parts/<part>/README.md
-> mechanics/<parent>/parts/<part>/VALIDATION.md
-> mechanics/<parent>/parts/AGENTS.md
```

`README.md` and `PARTS.md` explain role and map. `DIRECTION.md` names current
contour. `PROVENANCE.md` is the bridge for old names. `VALIDATION.md` names the
part-local route, while executable child validation commands live in the parent
`parts/AGENTS.md` lane.

## Bottom-Up Checks

When starting from a payload, ask these in order:

| If the file is under | Check |
| --- | --- |
| `evals/` | Does the bundle `EVAL.md` still own the claim? |
| `mechanics/<parent>/parts/<part>/` | Is the payload named by the part `README.md` and covered by `VALIDATION.md`? |
| `generated/` or part-local `generated/` | Which builder and source inputs produced it? |
| route-card-only root districts | Is this only `AGENTS.md` or `README.md`? Any other payload is drift. |
| `docs/` | Is this source guidance, topology, decision rationale, or a docs map? |
| `scripts/` or `tests/` | Which owner carries it: root-wide infrastructure or part-local route? |

## Validation Route

Executable validation commands belong in the nearest `AGENTS.md`.

For this index, use `docs/AGENTS.md#validation` and root `AGENTS.md#verify`.
For mechanic parts, follow the part `VALIDATION.md` to the parent
`parts/AGENTS.md` centralized child validation lane.
