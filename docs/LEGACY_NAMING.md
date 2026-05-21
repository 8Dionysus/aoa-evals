# Legacy Naming Posture

## Role

`docs/LEGACY_NAMING.md` is a thin posture guide for old and overloaded names
that may still appear in `aoa-evals`.

It is not an archive map, not a route index, not a distillation log, and not a
place to list legacy internals. Details of legacy live only inside the owning
`legacy/` archive.

It answers one question:

When an old name appears, should it be treated as active, historical,
accepted-input, generated-projection, candidate-only, or provenance-bridge
vocabulary?

## Active-first Route

Start from the active route.

The active-first route is mandatory.

If the active route cannot answer a historical, old-placement, or source-lineage
question, cross the package `PROVENANCE.md` bridge. The bridge opens the
owning `legacy/` archive. The archive explains itself.

`PROVENANCE.md` is a bridge, not an active route.

Use active surfaces first:

- parent `README.md`;
- parent `DIRECTION.md` for current operating direction;
- parent `PARTS.md`;
- part-local `parts/` contracts.

`PROVENANCE.md` is the single controlled bridge from active mechanic surfaces
into the legacy archive.

Do not put legacy archive details in this file.

## Name Postures

| Posture | Meaning | Use |
| --- | --- | --- |
| `active` | the current living topology or operation name | use in new route cards, package names, and current design wording |
| `historical` | a source lineage, release wave, or old route name | preserve as provenance and cite the current active route before new work |
| `accepted-input` | an old name or path still accepted by schemas, builders, examples, reports, tests, or sibling refs | keep compatibility visible until a validator-backed compatibility change exists |
| `generated-projection` | a name carried by generated readers or generated payload fields | rebuild from source; do not hand-edit as authority |
| `candidate-only` | runtime, machine, trace, or evidence-intake vocabulary below bundle-local review | route through candidate evidence and review boundaries |
| `provenance-bridge` | a package-local bridge from active surfaces to historical archive context | enter only after active route surfaces are insufficient |

## Active Owner Lookup

This guide intentionally does not list legacy names, old parent forms, old root
paths, archive files, or active mechanic parents.

When a concrete current owner is needed, use the active topology surfaces:

- `mechanics/README.md` for the active operation atlas;
- `mechanics/EVIDENCE_CLUSTERS.md` for parent-class proof and wrong-parent
  guardrails;
- `docs/PROOF_TOPOLOGY.md` for authority class routing;
- nearest parent `README.md`, `DIRECTION.md`, `PARTS.md`, and part contracts for
  the living operation.

When a concrete historical placement is needed, start from those active
surfaces and cross only through the owning package `PROVENANCE.md`.

## Boundary Rules

- Start from active package surfaces before reading legacy.
- Use package `PROVENANCE.md` as the single controlled bridge from active
  mechanic surfaces into historical archive questions.
- Do not begin new work in `legacy/`.
- Do not copy archive details into root guidance.
- Do not move generated projections by theme. Regenerate them from source or
  leave them in `generated/`.
- Do not let generated/readout JSON preserve former parent routes or root
  route-card paths as structured active references.
- Do not let authored mechanics route cards preserve root payload paths or a
  legacy parent route as active navigation.
- Do not let root-facing authored surfaces preserve root payload paths as
  active navigation.
- Do not let decision records present former root payload paths as current
  routes.
- Keep accepted aliases reviewable while schemas, examples, reports, builders,
  tests, or sibling refs still consume them.
- Record a decision before changing compatibility for a name that carries
  public history, accepted input, or sibling proof-reference context.
- Avoid broad negative fences. Name the current positive route first, then add
  the stop-line only where overclaiming is likely.

## Route Residue Vocabulary

These phrases name validation guard domains, not archive contents.

- `root-facing authored surfaces` may mention historical context, but should
  route current work to the active owner.
- `repo config surfaces` must not preserve a legacy mechanic parent as an
  active path.
- `source proof bundles` may cite a repo-qualified sibling when the sibling
  owner remains stronger.
- `active mechanics payload` should resolve under the same part, an active repo
  path, a repo-qualified sibling, or an explicit owner handoff.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k legacy_naming
python scripts/validate_repo.py
```
