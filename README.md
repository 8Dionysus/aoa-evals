# aoa-evals Bounded Proof Canon

`aoa-evals` is the AoA proof canon: the portable home for bounded eval
bundles, proof-support mechanics, generated readers, receipts, and routeable
evidence about agent-shaped work.

An eval here is a bounded proof surface. It carries a claim, fixtures or cases,
scoring or verdict logic, known limits, and a local validation route. Its proof
strength stays inside that local claim, evidence, and validation boundary.

Where `aoa-techniques` preserves reusable practice and `aoa-skills` preserves
bounded execution workflows, this repository preserves the proof surfaces that
make quality, boundary, regression, artifact, comparison, and repeated-window
claims reviewable outside the original project.

Current release: `v0.3.3`. See [CHANGELOG.md](CHANGELOG.md).

This README is the public proof-organ entry.

## What This Repository Does

| Function | Surface |
| --- | --- |
| Public proof-organ entry | this README |
| Agent pass-through chain from repo to authority class | [docs/AGENT_INDEX.md](docs/AGENT_INDEX.md) |
| Authority-class topology | [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md) |
| Proof operation atlas | [mechanics/README.md](mechanics/README.md) |
| Source proof objects | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| Full documentation map | [docs/README.md](docs/README.md) |
| Durable rationale | [docs/decisions/README.md](docs/decisions/README.md) |
| Current direction | [ROADMAP.md](ROADMAP.md) |
| Open obligations | [QUESTBOOK.md](QUESTBOOK.md) and [quests](quests/README.md) |
| Agent route law and local checks | [AGENTS.md](AGENTS.md), then the nearest nested `AGENTS.md` |

The repo shape is:

```text
practice canon -> workflow canon -> proof canon
```

## Start Here

Read only the surface that matches the job.

| Need | Route |
| --- | --- |
| Shortest honest overview | this README -> [DESIGN.md](DESIGN.md) -> [DESIGN.AGENTS.md](DESIGN.AGENTS.md) |
| Agent location in the tree | [docs/AGENT_INDEX.md](docs/AGENT_INDEX.md) |
| Artifact authority class | [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md) |
| Proof operation or mechanic parent | [mechanics/README.md](mechanics/README.md), then parent `README.md`, `DIRECTION.md`, `PARTS.md`, and part `README.md` |
| Eval discovery | [Eval Bundle Selection Chooser](EVAL_SELECTION.md) and [Eval Bundle Index](EVAL_INDEX.md) |
| First concrete proof object | [aoa-bounded-change-quality](evals/workflow/aoa-bounded-change-quality/EVAL.md) |
| Generated reader parity | [generated/README.md](generated/README.md) |
| Mechanics or payload movement | [mechanics/EVIDENCE_CLUSTERS.md](mechanics/EVIDENCE_CLUSTERS.md), then the owning mechanic |
| Legacy, provenance, or accepted-input vocabulary | [docs/LEGACY_NAMING.md](docs/LEGACY_NAMING.md) |
| Decision rationale | [docs/decisions/README.md](docs/decisions/README.md) |
| Executable validation route | [AGENTS.md#verify](AGENTS.md#verify), then the nearest nested route card |

Maintained agent lane routing is under `.agents/AGENTS.md` and
`.agents/spark/AGENTS.md`.

## Proof Check

Before trusting, publishing, or extending a proof claim, ask the narrowest owner.

| Claim question | Check |
| --- | --- |
| What bounded claim is being made? | bundle-local `EVAL.md` |
| What metadata, status, or baseline supports it? | bundle-local `eval.yaml` |
| Which authority class owns this artifact? | [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md) |
| Which proof operation routes the work? | [mechanics/README.md](mechanics/README.md) and the parent mechanic |
| Which comparison, artifact/process, repeated-window, or shared-infra guide applies? | [docs/COMPARISON_SPINE_GUIDE.md](docs/COMPARISON_SPINE_GUIDE.md), [docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md](docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md), [docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md](docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md), [docs/SHARED_PROOF_INFRA_GUIDE.md](docs/SHARED_PROOF_INFRA_GUIDE.md) |
| Which memory context may a proof cite? | Memory context is recall context, not proof authority; cite reviewed `aoa-memo` object ids, provenance, lifecycle, and generated read models, then keep the verdict in the eval bundle or owning mechanic. |
| Which report or receipt readout is available? | [docs/README.md#mechanic-and-evidence-anchors](docs/README.md#mechanic-and-evidence-anchors) and `generated/eval_report_index.min.json` |
| Which checks close the edit? | nearest `AGENTS.md` validation lane |

## Current Contour

`aoa-evals` currently carries the source eval bundle corpus, generated proof
readers, runtime-candidate templates, trace and receipt bridges, phase-alpha
matrices, Agon alignment surfaces, mechanics packages, and public-safe proof
references into sibling owners.

Current public eval discovery lives in:

- [Eval Bundle Selection Chooser](EVAL_SELECTION.md)
- [Eval Bundle Index](EVAL_INDEX.md)
- [generated/eval_catalog.min.json](generated/eval_catalog.min.json)
- [generated/eval_capsules.json](generated/eval_capsules.json)
- [generated/eval_sections.full.json](generated/eval_sections.full.json)
- [generated/eval_report_index.min.json](generated/eval_report_index.min.json)
- [generated/comparison_spine.json](generated/comparison_spine.json)

The active public runtime path remains:

```text
pick -> inspect -> expand -> object use
```

## Technical Districts

| District | Use for |
| --- | --- |
| [evals](evals/README.md) | source proof bundles and bundle-local reports |
| [docs](docs/README.md) | proof guides, topology maps, decision records, and reading routes |
| [mechanics](mechanics/README.md) | repeatable proof-layer operations and mechanic-owned payloads |
| [generated](generated/README.md) | compact derived readers tied back to source inputs |
| [quests](quests/README.md) | durable proof obligations and source quest records |
| [reports](reports/README.md) | compatibility route for former root report placement |
| [fixtures](fixtures/README.md), [runners](runners/README.md), [scorers](scorers/README.md), [schemas](schemas/README.md), [templates](templates/README.md) | route-card-only compatibility districts for shared proof infrastructure whose active payloads now live with owning bundles or mechanics |
| [config](config/README.md), [manifests](manifests/README.md), [examples](examples/README.md) | compatibility districts that route active payloads to the owning proof surface |
| [scripts](scripts/AGENTS.md) and [tests](tests/AGENTS.md) | root-wide validators, builders, and regression surfaces |

District gates narrow local handling. Source proof meaning stays with bundles;
mechanic payload meaning stays with the owning part; generated files stay
derived companions.

## Machine Companions

| Surface | Role |
| --- | --- |
| `generated/eval_catalog.min.json` | compact eval catalog |
| `generated/eval_capsules.json` | capsule hydration surface |
| `generated/eval_sections.full.json` | expanded eval section reader |
| `generated/eval_report_index.min.json` | compact report reader |
| `generated/comparison_spine.json` | comparison spine reader |
| generated quest readers | compact obligation and dispatch readers |

Generated surfaces route back to authored sources and builders.

## Evidence And Handoff

Detailed evidence anchors live in
[docs/README.md#mechanic-and-evidence-anchors](docs/README.md#mechanic-and-evidence-anchors)
and in the owning mechanic cards.

Use [mechanics/README.md](mechanics/README.md) for operation-owned reports,
receipts, runtime candidates, sibling refs, and release support. Use bundle-local
`reports/` only after the source eval claim is clear.

## Validation

Executable validation routes live in [AGENTS.md#verify](AGENTS.md#verify) and
the nearest nested `AGENTS.md`.

For bundle edits, start with [evals/AGENTS](evals/AGENTS.md). For generated
reader parity, start with [generated/AGENTS](generated/AGENTS.md). For proof
operation or mechanics movement, start with [mechanics/AGENTS](mechanics/AGENTS.md).

## Owner Boundary

Good candidates belong here when they are portable eval bundles, bounded
workflow evaluations, comparison or regression surfaces, verdict schemas,
fixtures, runners, scorers, rubrics, or report contracts.

Route away by owner:

- `aoa-techniques` for reusable practice meaning;
- `aoa-skills` for bounded workflow meaning;
- `aoa-routing` for navigation and dispatch;
- `aoa-agents` for role posture and handoff contracts;
- `aoa-playbooks` for scenario composition;
- `aoa-memo` for reviewed memory objects and recall posture;
- `abyss-stack` for runtime, deployment, storage, and lifecycle state.

`aoa-evals` currently has route_only memory posture: it can cite reviewed
`aoa-memo` recall and `.aoa` session evidence as bounded context, but it does
not write local memo candidates, export reviewed-intake packets, or land durable
memory unless a local memo port is explicitly added by a future owner decision.
`aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs may support
inspection, but they are access-plane evidence only, not proof authority or
durable memory write authority.

## Working Rule

Grow the proof canon by making the next proof route clearer.

Add evals, mechanics, schemas, reports, generated readers, route cards, tests,
and decision records only where they make a bounded proof claim more
inspectable, reviewable, and honest. When detail belongs to a bundle, mechanic,
docs map, decision record, quest, generated companion, changelog, roadmap, or
sibling owner, route it there.

## License

Apache-2.0
