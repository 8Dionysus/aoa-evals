# Route Residue Guards

## Role

`docs/architecture/ROUTE_RESIDUE_GUARDS.md` owns the detailed route-residue
guard contracts for `aoa-evals`.

Use `docs/architecture/PROOF_TOPOLOGY.md` for the authority-class map first.
Use this file when a validator, route card, generated reader, mechanic part, or
bundle still carries old root paths, wrong parent routes, or unresolved
payload residue.

## Operating Card

| Field | Route |
| --- | --- |
| role | route-residue guard contract map |
| entry | use when a path still points at an old root payload, wrong mechanic parent, stale generated route, or unclear current owner |
| input | stale path, generated ref, part payload, route-card text, decision note, repo config, source bundle ref, or sibling evidence ref |
| output | current owner route, allowed residue posture, and validation guard |
| owner | this file for guard contracts; `docs/architecture/PROOF_TOPOLOGY.md` for authority class; `mechanics/EVIDENCE_CLUSTERS.md` for mechanic evidence ledgers |
| next route | source eval package, active mechanic parent or part, generated builder, route card, decision note, or repo config owner |
| validation | `docs/AGENTS.md#validation`, root `AGENTS.md#verify`, and the focused validator that names the guard |

## Guard Contracts

Generated route residue is part of this topology contract. Root generated
readers must not carry structured links to route-card-only root districts or
former wrong mechanic parents; part-local generated readers may keep local
`config/`, `schemas/`, `reports/`, or similar sibling routes only when those
paths resolve under the same part root.

Active mechanic route residue is the authored companion guard. Mechanics route
cards and part READMEs may cite root route cards such as `fixtures/README.md`
and may cite `examples/`, `schemas/`, `reports/`, or similar paths only when
they resolve under the same part root. Bundle-local contracts should be written
as `evals/<family>/<eval>/...`, and active route cards must not link through
former legacy parent route paths.

Mechanic payload route residue is the active-payload companion guard. Fixtures,
schemas, manifests, examples, scripts, tests, and other authored mechanics
payload may keep part-local paths only when they resolve under the same
mechanic or part root; sibling-owned evidence uses a repo-qualified sibling ref
such as `repo:aoa-agents/...`, and old root payload globs such as root
runtime-example globs route through active selected-evidence packets or
explicit sibling refs.

Mechanic part payload inventory is the part-local companion guard: every actual
payload subdirectory under `mechanics/<parent>/parts/<part>/` must be named by
the part README, while an unexpected payload class, an empty payload
subdirectory, or an unexpected part-root file is rejected before it can become
hidden mechanics residue.

A part with no payload subdirectories must declare itself as an eval-backed
thin support route and state that the source eval package stays under
`evals/`; otherwise it is indistinguishable from empty topology.

Mechanic part Source Surfaces section shape is the source-entry companion
guard: every concrete part README must expose a plural section named
`## Source Surfaces` with at least one path-like source ref, so source refs
cannot hide in `## Role`, singular `## Source Surface`, or
`## Active Surfaces` headings.

Mechanic part Source Surfaces reference reachability is the active-reference
companion guard: every path-like `## Source Surfaces` reference must resolve as
an existing repo-relative path, a matching repo-relative glob, a repo-qualified
sibling ref, or an explicit placeholder route, so old root payload names cannot
remain as active part guidance.

Mechanic part validation route reachability is the child-validation companion
guard: every concrete part validation route flows from part README to
`VALIDATION.md` to the parent `parts/AGENTS.md` centralized child validation
block. The parent AGENTS child block keeps executable checks reachable and
repo-relative, so moved scripts, tests, scorers, or reports update through one
owner lane. A payload-bearing part also carries a payload coverage anchor in
its validation route: either a part-local path or a bundle-specific eval
validation route named through the nearest route card.

Mechanic PARTS index synchronization is the parent-map companion guard:
`mechanics/<parent>/PARTS.md` must match each actual part directory it owns and
must not preserve a stale local part route. A cross-parent reference remains
valid when it points to a different owner as a stop-line, handoff, or
owner-split route rather than declaring a local part.

Mechanic parent direction is the active parent contour guard. Every active
parent mechanic owns a `DIRECTION.md` that states the current operating
direction between `README.md`, `PARTS.md`, `PROVENANCE.md`, and part-local
contracts, and each parent `README.md` plus parent `AGENTS.md` routes that
direction from its Entry Route. Use `DIRECTION.md` for the parent contour,
`PARTS.md` for the part map, `PROVENANCE.md` for the active-to-archive bridge,
generated readers for derived views, and `mechanics/EVIDENCE_CLUSTERS.md` plus
the decision and validator route before proposing a new parent name.

Root authored route residue is the entry-guidance companion guard. Root-facing
authored surfaces such as `AUDIT.md`, `EVAL_INDEX.md`, `docs/README.md`,
`docs/architecture/*.md`, `docs/guides/*.md`, `docs/operations/*.md`,
`.agents/spark/SWARM.md`, root route cards, and `evals/AGENTS.md` should use
`evals/<family>/<eval>/...`, active `mechanics/...` routes, or root route cards
instead of bare root payload paths from route-card-only districts.

Decision route residue is the historical-memory companion guard. Decision
records may name former root paths only as explicit historical context; current
navigation in `docs/decisions/` should use `evals/<family>/<eval>/...`, active
`mechanics/...` routes, or root route cards instead of bare root payload paths.

Repo config route residue is the executable-routing companion guard.
`.gitignore`, `pytest.ini`, and `.github/workflows/` are executable routes; they
point at active owners rather than former mechanic parents or route-card-only
root payload paths.

Source bundle route residue is the proof-object companion guard. Source bundles
may use bundle-local paths only when they resolve under the owning bundle, and
repo-qualified sibling evidence, such as `repo:aoa-sdk/...`, stays distinct from
local route-card-only root payload paths.
