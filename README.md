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

```text
practice canon -> workflow canon -> proof canon
```

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
| Eval discovery | [Eval Bundle Selection Chooser](EVAL_SELECTION.md), [Eval Bundle Index](EVAL_INDEX.md) |
| Full documentation map | [docs/README.md](docs/README.md) |
| Durable rationale | [docs/decisions/README.md](docs/decisions/README.md) |
| Direction and obligations | [ROADMAP.md](ROADMAP.md), [QUESTBOOK.md](QUESTBOOK.md), [quests](quests/README.md) |
| Agent route law and local checks | [AGENTS.md](AGENTS.md), then the nearest nested `AGENTS.md` |

## Start Here

Read the surface that matches the job.

| Need | Route |
| --- | --- |
| Shortest honest overview | this README -> [DESIGN.md](DESIGN.md) -> [DESIGN.AGENTS.md](DESIGN.AGENTS.md) |
| Agent location in the tree | [docs/AGENT_INDEX.md](docs/AGENT_INDEX.md) |
| Artifact authority class | [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md) |
| Proof operation or mechanic parent | [mechanics/README.md](mechanics/README.md), then parent `README.md`, `DIRECTION.md`, `PARTS.md`, and part `README.md` |
| Eval bundle selection | [Eval Bundle Selection Chooser](EVAL_SELECTION.md) and [Eval Bundle Index](EVAL_INDEX.md) |
| First concrete proof object | [aoa-bounded-change-quality](evals/workflow/aoa-bounded-change-quality/EVAL.md) |
| Generated reader parity | [generated/README.md](generated/README.md) |
| Mechanics or payload movement | [mechanics/EVIDENCE_CLUSTERS.md](mechanics/EVIDENCE_CLUSTERS.md), then the owning mechanic |
| Legacy, provenance, or accepted-input vocabulary | [docs/LEGACY_NAMING.md](docs/LEGACY_NAMING.md) |
| Decision rationale | [docs/decisions/README.md](docs/decisions/README.md) |
| Executable validation route | [AGENTS.md#verify](AGENTS.md#verify), then the nearest nested route card |

Maintained agent lane routing is under `.agents/AGENTS.md` and
`.agents/spark/AGENTS.md`.

## Proof Check

Before trusting, publishing, or extending a proof claim, open the smallest owner
that can answer the question.

| Question | Owner route |
| --- | --- |
| What exactly is being claimed? | bundle-local `EVAL.md` and `eval.yaml` |
| What class of proof object is this? | [docs/PROOF_TOPOLOGY.md](docs/PROOF_TOPOLOGY.md) |
| Which repeatable operation owns the movement? | [mechanics/README.md](mechanics/README.md), then the parent mechanic |
| Which guide, report, receipt, or evidence anchor explains the route? | [docs/README.md](docs/README.md), its [mechanic and evidence anchors](docs/README.md#mechanic-and-evidence-anchors), and `generated/eval_report_index.min.json` |
| Is memory context involved? | reviewed `aoa-memo` object ids and provenance can support recall; verdict authority stays with the eval bundle or owning mechanic |
| How should the change close? | nearest `AGENTS.md` validation lane |

## Current Contour

`aoa-evals` currently carries the source eval bundle corpus, generated proof
readers, runtime-candidate templates, trace and receipt bridges, phase-alpha
matrices, Agon alignment surfaces, mechanics packages, and public-safe proof
references into sibling owners.

Current public discovery starts here:

- [Eval Bundle Selection Chooser](EVAL_SELECTION.md)
- [Eval Bundle Index](EVAL_INDEX.md)
- [generated/README.md](generated/README.md)
- [generated/eval_catalog.min.json](generated/eval_catalog.min.json)
- [generated/eval_capsules.json](generated/eval_capsules.json)
- [generated/eval_sections.full.json](generated/eval_sections.full.json)
- [generated/eval_report_index.min.json](generated/eval_report_index.min.json)
- [generated/comparison_spine.json](generated/comparison_spine.json)

Generated readers are compact companions. Source bundles, mechanics, decisions,
and route cards keep meaning.

## Technical Districts

| District | Use for |
| --- | --- |
| [evals](evals/README.md) | source proof bundles and bundle-local reports |
| [docs](docs/README.md) | proof guides, topology maps, decision records, and reading routes |
| [mechanics](mechanics/README.md) | repeatable proof-layer operations and mechanic-owned payloads |
| [generated](generated/README.md) | compact derived readers tied back to source inputs |
| [quests](quests/README.md) | durable proof obligations and source quest records |
| [reports](reports/README.md) | compatibility route for former root report placement |
| [fixtures](fixtures/README.md), [runners](runners/README.md), [scorers](scorers/README.md), [schemas](schemas/README.md), [templates](templates/README.md) | route-card-only compatibility districts for shared proof infrastructure whose active payloads live with owning bundles or mechanics |
| [config](config/README.md), [manifests](manifests/README.md), [examples](examples/README.md) | compatibility districts that route active payloads to the owning proof surface |
| [scripts](scripts/AGENTS.md) and [tests](tests/AGENTS.md) | root-wide validators, builders, and regression surfaces |

District gates narrow local handling. Source proof meaning stays with bundles;
mechanic payload meaning stays with the owning part; generated files stay
derived companions.

## Evidence And Handoff

Use [mechanics/README.md](mechanics/README.md) for operation-owned reports,
receipts, runtime candidates, sibling refs, and release support. Use
bundle-local `reports/` after the source eval claim is clear.

Use [docs/README.md#mechanic-and-evidence-anchors](docs/README.md#mechanic-and-evidence-anchors)
when the question is a reading route across guides, mechanics, generated
readers, and evidence anchors.

Use `aoa-memo` for reviewed memory objects and recall posture. `aoa-evals`
can cite reviewed recall as bounded context while proof authority stays with
the eval bundle or owning mechanic.

## Validation

Executable validation routes live in [AGENTS.md#verify](AGENTS.md#verify) and
the nearest nested `AGENTS.md`.

For bundle edits, start with [evals/AGENTS](evals/AGENTS.md). For generated
reader parity, start with [generated/AGENTS](generated/AGENTS.md). For proof
operation or mechanics movement, start with [mechanics/AGENTS](mechanics/AGENTS.md).

## Owner Boundary

| Pressure | Route |
| --- | --- |
| Portable eval bundle, bounded workflow evaluation, comparison or regression surface, verdict schema, fixture, runner, scorer, rubric, or report contract | keep in `aoa-evals` under the owning bundle, mechanic, generated reader, schema, test, or route card |
| Reusable practice meaning | route to `aoa-techniques` |
| Bounded execution workflow meaning | route to `aoa-skills` |
| Navigation and dispatch | route to `aoa-routing` |
| Role posture and handoff contracts | route to `aoa-agents` |
| Scenario composition | route to `aoa-playbooks` |
| Reviewed memory objects and recall posture | route to `aoa-memo` |
| Runtime, deployment, storage, and lifecycle state | route to `abyss-stack` |

## Working Rule

Grow the proof canon by making the next proof route clearer.

Add evals, mechanics, schemas, reports, generated readers, route cards, tests,
and decision records where they make a bounded proof claim more inspectable,
reviewable, and honest. Route detail to the owning bundle, mechanic, docs map,
decision record, quest, generated companion, changelog, roadmap, or sibling
owner.

## License

Apache-2.0
