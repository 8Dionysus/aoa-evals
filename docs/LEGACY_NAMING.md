# Legacy Naming Posture

## Role

`docs/LEGACY_NAMING.md` is a thin posture guide for old and overloaded names
that may still appear in `aoa-evals`.

Use this guide to classify old vocabulary, then route through the active owner.
Archive maps, route indexes, distillation logs, and legacy internals stay with
the owning active surface, `PROVENANCE.md`, and the package-local `legacy/`
archive.

It answers one question:

When an old name appears, should it be treated as active, historical,
accepted-input, generated-projection, candidate-only, or provenance-bridge
vocabulary?

## Operating Card

| Field | Route |
| --- | --- |
| role | legacy-name posture guide and active-owner lookup route |
| input | old path, overloaded name, former parent form, generated projection, candidate evidence name, or accepted compatibility vocabulary |
| output | name posture, active owner route, provenance bridge route, rename gate, and validation guard |
| owner | this guide owns posture vocabulary; active mechanic surfaces own concrete legacy archive details through `PROVENANCE.md` |
| next route | `mechanics/EVIDENCE_CLUSTERS.md`, `docs/PROOF_TOPOLOGY.md`, nearest parent `README.md`/`DIRECTION.md`/`PARTS.md`, package `PROVENANCE.md`, then archive-local legacy surfaces |
| tools | root validator, semantic AGENTS validator, and focused legacy naming tests in `tests/test_validate_repo.py` |
| validation | [docs/AGENTS.md#validation](AGENTS.md#validation) and root [AGENTS.md#verify](../AGENTS.md#verify) |

## Active-first Route

Start from the active route.

The active-first route starts with the current owner before archive context.

For historical, old-placement, or source-lineage questions, cross the package
`PROVENANCE.md` bridge after the active route identifies the owner. The bridge
opens the owning `legacy/` archive. The archive explains itself.

`PROVENANCE.md` is the active-to-archive bridge for the mechanic. It opens
historical archive context after active surfaces identify the owner.

Use active surfaces first:

- parent `README.md`;
- parent `DIRECTION.md` for current operating direction;
- parent `PARTS.md`;
- part-local `parts/` contracts.

`PROVENANCE.md` is the single controlled bridge from active mechanic surfaces
into the legacy archive.

Legacy archive details stay inside the owning archive after the active
`PROVENANCE.md` bridge.

## Name Postures

| Posture | Meaning | Use |
| --- | --- | --- |
| `active` | the current living topology or operation name | use in new route cards, package names, and current design wording |
| `historical` | a source lineage, release wave, or old route name | preserve as provenance and cite the current active route before new work |
| `accepted-input` | an old name or path still accepted by schemas, builders, examples, reports, tests, or sibling refs | keep compatibility visible until a validator-backed compatibility change exists |
| `generated-projection` | a name carried by generated readers or generated payload fields | rebuild from source and keep the projection weaker than authority |
| `candidate-only` | runtime, machine, trace, or evidence-intake vocabulary below bundle-local review | route through candidate evidence and review boundaries |
| `provenance-bridge` | a package-local bridge from active surfaces to historical archive context | enter only after active route surfaces are insufficient |

## Naming Depth

Directory names should reveal topology at first glance:

| Layer | Name should describe | Example shape |
| --- | --- | --- |
| mechanic parent | repeatable proof operation | `mechanics/<operation>/` |
| mechanic part | bounded sub-operation or support contract | `mechanics/<operation>/parts/<part>/` |
| payload directory | artifact class owned by that part | `docs/`, `examples/`, `fixtures/`, `schemas/`, `scripts/`, `tests`, `reports/`, `generated/` |
| payload file | concrete proof-support object, report, schema, fixture, or generated readout | part-local, bundle-local, or repo-qualified by owner |

When a name looks like an artifact form, evidence class, release stage, old root
placement, or stronger-owner doctrine, first ask whether it belongs below an
existing parent as a part or payload. Promote it to a parent name only through
the evidence-backed mechanics route.

## Rename Gate

A rename is a topology change with compatibility impact.

Before changing a public path, parent name, part name, payload directory, schema
field, generated file name, or accepted input vocabulary, gather the owning
chain:

1. active route and nearest `AGENTS.md`;
2. source surface that owns the meaning;
3. `PROVENANCE.md` or legacy archive bridge when old placement matters;
4. generated reader or builder impact;
5. validator constant and regression test impact;
6. decision record when future agents need the rationale.

When that chain is incomplete, keep the active name and document the ambiguity
in the owning roadmap, quest, or decision queue before renaming.

## Active Owner Lookup

This guide classifies naming posture. Concrete legacy names, old parent forms,
old root paths, archive files, and active mechanic parents are resolved through
the active owner lookup below.

When a concrete current owner is needed, use the active topology surfaces:

- `mechanics/README.md` for the active operation atlas;
- `mechanics/EVIDENCE_CLUSTERS.md` for parent-class proof and wrong-parent
  guardrails;
- `docs/PROOF_TOPOLOGY.md` for authority class routing;
- nearest parent `README.md`, `DIRECTION.md`, `PARTS.md`, and part contracts for
  the living operation.

When a concrete historical placement is needed, start from those active
surfaces and cross only through the owning package `PROVENANCE.md`.

## Route Rules

- Start from active package surfaces before reading legacy.
- Use package `PROVENANCE.md` as the single controlled bridge from active
  mechanic surfaces into historical archive questions.
- Start current work in the active package or owning part.
- Keep archive details inside the owning package legacy archive.
- Regenerate generated projections from source; keep remaining projections in
  `generated/` until their builder moves.
- Resolve generated/readout structured active references to current parent,
  part, bundle-local, or explicit provenance routes.
- Resolve generated/readout JSON to current active references or explicit
  historical context.
- Use authored mechanics route cards for current parent and part navigation;
  keep former root payload paths and legacy parent forms as provenance context.
- Keep legacy parent route vocabulary mapped to the current parent or part.
- Route root-facing authored surfaces to the active owner when current work is
  involved.
- Use decision records for rationale and current route choice; keep former root
  payload paths as historical context.
- Keep accepted aliases reviewable while schemas, examples, reports, builders,
  tests, or sibling refs still consume them.
- Record a decision before changing compatibility for a name that carries
  public history, accepted input, or sibling proof-reference context.
- Name the current positive route first, then add a stop-line only where
  overclaiming is likely.

## Route Residue Vocabulary

These phrases name validation guard domains for active route residue.

- `root-facing authored surfaces` may mention historical context, but should
  route current work to the active owner.
- `repo config surfaces` resolve legacy mechanic parents to active paths.
- `source proof bundles` may cite a repo-qualified sibling when the sibling
  owner remains stronger.
- `active mechanics payload` should resolve under the same part, an active repo
  path, a repo-qualified sibling, or an explicit owner handoff.

## Validation

Executable checks for legacy naming posture live in
[docs/AGENTS.md#validation](AGENTS.md#validation) and root
[AGENTS.md#verify](../AGENTS.md#verify).
