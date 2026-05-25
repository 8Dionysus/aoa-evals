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

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
5. `mechanics/EVIDENCE_CLUSTERS.md`
6. `mechanics/README.md`
7. the target package `README.md`
8. the target package `DIRECTION.md` for current operating direction
9. the target package `AGENTS.md`
10. `docs/decisions/` for package-creation or package-boundary changes

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

After package route changes, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If the changed package touches generated quest readers, catalogs, report
indexes, runtime-candidate readers, or boundary-bridge matrices, add the owning
builder check named by the package card, commonly:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
```

Run package-specific builders or checks named in the package card before the
broader mechanics lane.

Focused mechanic topology checks live in this lane when the changed source
surface names a narrower guard:

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_root_district_recon
python -m pytest -q tests/test_validate_repo.py -k mechanic_part_payload_inventory
python -m pytest -q tests/test_validate_repo.py -k mechanic_part_validation_command
```

## Closeout

Report which package operation changed, which source surfaces it routes, which
validators ran, which file movement remains deferred, and which stronger-owner
boundary stayed intact.
