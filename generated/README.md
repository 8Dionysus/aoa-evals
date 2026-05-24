# Generated Reader Index

`generated/` stores repo-wide derived reader surfaces.

These files help agents and tooling navigate source proof objects, quest
records, reports, capsules, sections, and comparison metadata while preserving
authored source ownership.

## Operating Card

| Field | Route |
| --- | --- |
| role | repo-wide generated reader index |
| input | source eval packages, quest records, reports, mechanic payloads, and builder outputs |
| output | reader family route, source owner route, builder route, or validation route |
| owner | source surfaces and builders own truth; `generated/AGENTS.md` owns edit law |
| next route | source bundle, quest record, report, mechanic part, builder, or route card |
| tools | catalog builder, report-index builder, quest readers, candidate-reader builders, and phase-alpha matrix builder |
| validation | [generated/AGENTS.md#validation](AGENTS.md#validation) and source-owner checks |

## Current Root Readers

| Reader | Source shape | Builder or guard |
| --- | --- | --- |
| `generated/eval_catalog.json` | full eval bundle catalog derived from `evals/**/EVAL.md` and `eval.yaml` | `scripts/build_catalog.py` |
| `generated/eval_catalog.min.json` | compact catalog projection | `scripts/build_catalog.py` |
| `generated/eval_capsules.json` | capsule-oriented projection of bundle source sections | `scripts/build_catalog.py` |
| `generated/eval_sections.full.json` | full section extraction for downstream readers | `scripts/build_catalog.py` |
| `generated/comparison_spine.json` | comparison-only projection from bundle manifests | `scripts/build_catalog.py` |
| `generated/eval_report_index.min.json` | compact index of bundle-local report artifacts | `scripts/generate_eval_report_index.py` |
| `generated/quest_catalog.min.json` | compact quest source-record catalog | `scripts/build_catalog.py` |
| `generated/quest_dispatch.min.json` | compact quest dispatch reader | `scripts/build_catalog.py` |
| `generated/quest_catalog.min.example.json` | public-safe example projection for quest catalog shape | `scripts/build_catalog.py` |
| `generated/quest_dispatch.min.example.json` | public-safe example projection for quest dispatch shape | `scripts/build_catalog.py` |

## Part-Local Generated Companions

Some generated companions live below the mechanic part that owns the operation:

- audit runtime candidate readers:
  `mechanics/audit/parts/candidate-readers/generated/`;
- Agon alignment registries:
  `mechanics/agon/parts/*/generated/`;
- boundary-bridge Phase Alpha matrix:
  `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/`;
- RPG unlock proof cards:
  `mechanics/rpg/parts/progression-unlocks/generated/`.

Part-local generated output stays weaker than the part-local source surfaces,
schemas, examples, and builders.

## Read Chain

Use generated readers in this order:

```text
question or tool route
-> generated reader
-> source bundle, quest record, report, or mechanic part
-> source owner surface
-> validator or builder check
```

Generated readers answer "where should I look next?" Source surfaces answer
"what is true?" after the reader returns the agent to the owner path.

## Validation

Executable generated-reader commands live in
[generated/AGENTS.md#validation](AGENTS.md#validation). This index names the
reader families, source chain, and owning builders; the route card owns the
operational command lane.

Use source-owner checks as well when generated drift comes from bundle, quest,
report, or mechanic payload changes.
