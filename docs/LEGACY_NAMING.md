# Legacy Naming

## Role

`docs/LEGACY_NAMING.md` maps legacy, historical, accepted-input, and generated
names that still matter inside `aoa-evals`.

It is not the roadmap, changelog, decision log, generated catalog, or proof
bundle source. It answers a narrower question:

When an old or overloaded name appears, what posture does that name have now,
and where should a future agent route the work?

## Core Rule

Legacy names preserve lineage and compatibility. They do not steer active
topology by habit.

Active names should describe the living proof operation. Historical names,
old wave vocabulary, old public paths, generated projections, and accepted
external inputs should stay visible when they still carry proof context.

The route is:

`legacy or overloaded name -> naming posture -> current owner route -> validation or containment`

## Name Postures

| Posture | Meaning | Use |
| --- | --- | --- |
| `active` | the current living topology or operation name | use in new route cards, package names, and current design wording |
| `historical` | a source lineage, release wave, or old route name | preserve as provenance and cite the current route before new work |
| `accepted-input` | an old name or path still accepted by schemas, builders, examples, or sibling refs | keep compatibility visible until a validator-backed retirement exists |
| `generated-projection` | a name carried by generated readers or generated payload fields | rebuild from source; do not hand-edit as authority |
| `candidate-only` | runtime, machine, trace, or evidence-intake vocabulary below bundle-local review | route through candidate evidence and review boundaries |
| `retire-after` | a name with a current replacement and a known removal condition | keep alias and removal condition together |

## Current Naming Map

| Name | Current posture | Current route | Boundary |
| --- | --- | --- | --- |
| `Agon` | `historical`, `accepted-input`, and active proof family context where source docs/configs still use it | current proof alignment work routes through `mechanics/agon-proof/` | Agon wording does not become repo-wide proof doctrine or live verdict authority |
| `wave`, `Wave XV`, `wave16`, and similar wave labels | `historical` | keep in release lineage, Agon seeds, generated alignment registries, and tests that prove old contracts | wave vocabulary should not become the active topology for new proof operations |
| `phase-alpha` | `accepted-input` and `historical` | route runtime and memo pilot evidence through `mechanics/runtime-evidence/` and sibling refs through `mechanics/sibling-proof-refs/` | Phase Alpha evidence is not proof acceptance without bundle-local review |
| `runtime-candidate` | `candidate-only` and `generated-projection` | current active route is `mechanics/runtime-evidence/` | generated runtime candidate readers are navigation and intake surfaces, not verdict authority |
| `artifact-to-verdict` | `accepted-input` bridge vocabulary | current active route is `mechanics/runtime-evidence/` and `docs/TRACE_EVAL_BRIDGE.md` | hooks do not become a runtime judge implementation |
| `bundle-family` | `historical` grouping vocabulary | keep as bundle-local or catalog lineage through `mechanics/proof-object/` lifecycle routing | do not promote family labels into top-level proof taxonomy by habit |
| `Titan canary` | `historical` and canary seed vocabulary | current active route is `mechanics/titan-canaries/`, `docs/TITAN_INCARNATION_CANARIES.md`, and `evals/titan_*_canary.yaml` | canaries seed boundary checks; they are not full incarnation proof by themselves |
| `Spark` | `active` lane name with `historical` root-path vocabulary | current active route is `.agents/spark/`; old `Spark/` references are legacy path vocabulary | do not use Spark lane guidance as proof authority or broad architecture permission |
| top-level `quests/AOA-EV-Q-*.yaml` | `historical` and `accepted-input` path vocabulary | current active source route is `quests/<lane>/<state>/AOA-EV-Q-*.yaml`; questbook routing lives in `quests/README.md` and `mechanics/questbook/` | keep IDs stable; do not reintroduce duplicate top-level source files |
| `latest-sibling canary` | `active` compatibility check name | current active route is `docs/SIBLING_PROOF_REFS.md` and `mechanics/sibling-proof-refs/` | path compatibility is not sibling owner acceptance |

## Active Route Replacements

Use these current routes when creating new guidance:

| Old or overloaded wording | Current active route |
| --- | --- |
| runtime candidate guide, runtime candidate intake | `mechanics/runtime-evidence/` |
| artifact-to-verdict hook work | `mechanics/runtime-evidence/` and `docs/TRACE_EVAL_BRIDGE.md` |
| sibling path drift | `docs/SIBLING_PROOF_REFS.md` and `mechanics/sibling-proof-refs/` |
| quest source movement, quest lifecycle, quest projection parity | `mechanics/questbook/` |
| old Agon or wave proof family work | `mechanics/agon-proof/` for proof alignment work; `docs/PROOF_TOPOLOGY.md` for authority-class questions |
| Titan canary shape work | `mechanics/titan-canaries/` |
| Spark lane work | `.agents/spark/` and `.agents/AGENTS.md` |
| proof bundle lifecycle and maturity wording | `mechanics/proof-object/` |

## Movement Rules

- Do not rename a legacy surface without a current route, source/read-model map,
  and provenance note.
- Do not move generated projections by theme. Regenerate them from source or
  leave them in `generated/`.
- Keep accepted aliases reviewable while schemas, examples, reports, builders,
  tests, or sibling refs still consume them.
- Prefer package-local `legacy/` only after the package owns a real operation.
- Record a decision before retiring a name that carries public history,
  accepted input, or sibling proof-reference context.
- Avoid broad negative fences. Name the current positive route first, then add
  the stop-line only where overclaiming is likely.

## Relationship to Current Packages

`mechanics/questbook/` owns quest obligation routing, including the current
top-level source quest path compatibility posture.

`mechanics/runtime-evidence/` owns runtime candidate, phase-alpha, and
artifact-to-verdict bridge names as candidate evidence vocabulary.

`mechanics/sibling-proof-refs/` owns sibling reference compatibility posture,
including current, legacy, rejected, and unresolved refs.

`mechanics/titan-canaries/` owns Titan canary seed shape routing while keeping
the YAML files in `evals/`.

`mechanics/agon-proof/` owns Agon pre-protocol proof alignment routing while
keeping Agon docs, seed configs, generated registries, recurrence manifests,
observe-only hooks, quest notes, and recurrence-control-plane bundle files in
their current source districts.

`.agents/spark/` owns the maintained Spark fast-loop lane. `.agents/AGENTS.md`
owns the agent district route. Old `Spark/` path wording is legacy path
vocabulary only.

`quests/<lane>/<state>/` owns active quest source paths. Old top-level quest
paths are legacy path vocabulary and accepted-input lineage, while generated
quest readers emit the current source path.

No active package owns all legacy naming. This file is the repo-level map that
keeps legacy vocabulary from scattering across packages before each package is
ready.

## Validation

Run the root validation after editing this map:

```bash
python scripts/validate_repo.py
```

When edits affect generated runtime candidate readers, quest readers, sibling
canaries, or reports, also run the owning builder or validator in `--check`
mode.
