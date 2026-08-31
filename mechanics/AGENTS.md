# AGENTS.md

## Applies to

`mechanics/` operation packages and package route cards.

## Role

Mechanics route repeatable proof-layer operations.

They receive recurring proof pressure and route it to the parent operation,
part contract, payload home, validation lane, or stronger-owner handoff that
can carry the work.

## Operating Card

| Field | Route |
| --- | --- |
| role | operation-package route law for repeatable proof-layer work |
| input | proof pressure, artifact movement, package boundary changes, parent evidence, part payload work, and validation route changes |
| output | parent route, part contract, payload owner, validation lane, or stronger-owner handoff |
| owner | mechanics root for operation topology; parent package for local operation law; part for payload contract |
| next route | `mechanics/EVIDENCE_CLUSTERS.md`, `mechanics/README.md`, target parent `README.md`, target `DIRECTION.md`, target `PARTS.md`, and nearest `AGENTS.md` |
| tools | root validator, semantic AGENTS validator, catalog/report builders when generated readers move |
| validation | this card's `Validation` section |

Each target package keeps current operating direction in `DIRECTION.md`; the target package `DIRECTION.md` is the current direction source. Use the active-to-archive bridge in its `PROVENANCE.md` when legacy names are involved.
The architecture proof route remains `docs/architecture/PROOF_TOPOLOGY.md`.

## Shared Parts Card

### Operating Card

| Field | Route |
| --- | --- |
| role | part-contract and payload route law for this mechanic parent |
| input | part boundary change, payload movement, source-surface pressure, validation route change, or legacy placement question |
| output | parent `PARTS.md` alignment, nearest part `README.md`, part `VALIDATION.md`, on-demand part validation route, or stronger-owner handoff |
| owner | parent `PARTS.md` owns the part map; nearest part `README.md` owns the part contract; the nearest part VALIDATION.md owns executable child validation commands |
| next route | parent `AGENTS.md`, parent `DIRECTION.md`, parent `PARTS.md`, nearest part `README.md`, nearest part `VALIDATION.md`, and affected payload home |
| tools | parent validation lane, on-demand part validation routes, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

### Route Rules

- Keep each part tied to one row in the parent `PARTS.md`.
- Keep source proof meaning in bundles or source docs; validation text carries check route and evidence coverage.
- Keep executable child validation commands in child VALIDATION.md files so README files stay route maps and contracts.
- Route legacy placement through parent `PROVENANCE.md` and `legacy/` rather than recreating old root payload paths.

## Owner Routes

| Need | Owner route |
| --- | --- |
| source proof object meaning | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| root design or roadmap direction | root design surfaces or `ROADMAP.md` |
| generated reader truth | source surface, builder, generated reader, and `generated/AGENTS.md` |
| runtime authority | runtime owner or audit intake route before proof adoption |
| sibling owner truth | owning sibling repository |
| package-local operation law | `mechanics/<parent>/AGENTS.md`, `README.md`, `DIRECTION.md`, and `PARTS.md` |
| part payload contract | `mechanics/<parent>/parts/<part>/README.md` and `VALIDATION.md` |

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally. Read the root and nearest owner routes conditionally for the touched source; do not preload unrelated README or sibling validation material.
## Route Rules

- Create packages for live operations with evidence cluster support and a
  validation route.
- Use `mechanics/EVIDENCE_CLUSTERS.md` before turning a form, report, canary,
  or old path family into a parent mechanic.
- Top-level parent directories are validator allowlisted. A new
  `mechanics/<new-parent>/` slice updates the evidence cluster, package route
  cards, topology docs, decision record, and validator together.
- Keep source proof objects in `evals/`.
- Keep quest source records in `quests/<lane>/<state>/` and keep generated
  readers aligned with current source paths.
- Keep generated readers weaker than their builders and source surfaces.
- Keep runtime candidates, receipts, and sibling refs below bundle-local review.
- Preserve legacy names as provenance or accepted inputs; active topology
  follows current parent and part names.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

After package route changes, run:

If the changed package touches generated quest readers, catalogs, report
indexes, runtime-candidate readers, or boundary-bridge matrices, add the owning
builder check named by the package card, commonly:

Run package-specific builders or checks named in the package card before the
broader mechanics lane.

Focused mechanic topology checks live in this lane when the changed source
surface names a narrower guard:

## Closeout

Report which package operation changed, which source surfaces it routes, which
validators ran, which file movement remains deferred, and which stronger-owner
boundary stayed intact.
