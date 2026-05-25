# Documentation Map

This file is the human and agent entrypoint for the `docs/` surface. It helps a
reader choose the next source without guessing from filenames.

Operational edit law belongs in the nearest `AGENTS.md`. This map explains
where meaning lives and which surface to open next.

## Operating Card

| Field | Route |
| --- | --- |
| role | docs entrypoint and source-of-truth chooser |
| entry | choose by question in `First Route` |
| input | proof questions, route questions, topology questions, guide lookup, or operational docs lookup |
| output | the next source surface, index, proof guide, operation guide, or owner route |
| owner | `docs/AGENTS.md` for docs edits; target source files own their meaning |
| next route | `docs/architecture/`, `docs/guides/`, `docs/operations/`, `docs/decisions/`, mechanics, or bundle-local proof |
| validation | [docs/AGENTS.md#validation](AGENTS.md#validation) and the nearest owner route card |

## First Route

| Question | Open |
| --- | --- |
| What is this repository? | [aoa-evals Bounded Proof Canon](../README.md) |
| Where am I in the agent index chain? | [Agent Index](architecture/AGENT_INDEX.md) |
| What is the proof-system shape? | [Design](../DESIGN.md), [Agent Surface Design](../DESIGN.AGENTS.md), [Architecture](architecture/ARCHITECTURE.md) |
| Which authority class owns this artifact? | [Proof Topology](architecture/PROOF_TOPOLOGY.md) |
| What may `aoa_evals` MCP expose without becoming proof authority? | [AoA Evals MCP Contract](architecture/AOA_EVALS_MCP_CONTRACT.md) |
| Is this route residue, stale path, or wrong owner pressure? | [Route Residue Guards](architecture/ROUTE_RESIDUE_GUARDS.md) |
| Is this name active, legacy, accepted input, generated projection, or candidate vocabulary? | [Legacy Naming](architecture/LEGACY_NAMING.md) |
| Which proof guide applies? | [Guides](#guides) |
| Which proof operation owns this route? | [Mechanics Operation Atlas](../mechanics/README.md) |
| Which generated report or comparison reader should I inspect? | [Generated Eval Report Index](../generated/eval_report_index.min.json), [Comparison Spine Reader](../generated/comparison_spine.json), then the source bundle or mechanic named inside the reader |
| Why was this route chosen? | [Decision Records Index](decisions/README.md) |
| What should happen next? | [Proof Direction Roadmap](../ROADMAP.md), [Questbook Obligation Index](../QUESTBOOK.md), [Quest Source Records](../quests/README.md), [Quest Lifecycle Contract](../quests/LIFECYCLE.md) |
| Which eval should I inspect? | [Eval Bundle Selection Chooser](../EVAL_SELECTION.md), [Eval Bundle Index](../EVAL_INDEX.md) |

The first concrete source-owned proof surface remains
[First starter bundle](../evals/workflow/aoa-bounded-change-quality/EVAL.md).

## Folder Map

| Folder | Role | Open first |
| --- | --- | --- |
| `architecture/` | authority, topology, route law, and legacy/provenance posture | [Proof Topology](architecture/PROOF_TOPOLOGY.md) |
| `guides/` | proof-reading guides for review, score, verdict, comparison, portability, fixtures, blind spots, and boundaries | [Eval Review Guide](guides/EVAL_REVIEW_GUIDE.md) |
| `operations/` | release, quest integration, closeout/writeback ingress, and preserved root reference material | [Releasing](operations/RELEASING.md) |
| `decisions/` | durable rationale and generated lookup indexes | [Decision Records Index](decisions/README.md) |

## Architecture

- [Agent Index](architecture/AGENT_INDEX.md)
- [Architecture](architecture/ARCHITECTURE.md)
- [Proof Topology](architecture/PROOF_TOPOLOGY.md)
- [AoA Evals MCP Contract](architecture/AOA_EVALS_MCP_CONTRACT.md)
- [Route Residue Guards](architecture/ROUTE_RESIDUE_GUARDS.md)
- [Legacy Naming](architecture/LEGACY_NAMING.md)

## Guides

- [Eval Philosophy](guides/EVAL_PHILOSOPHY.md)
- [Eval Rubric](guides/EVAL_RUBRIC.md)
- [Eval Review Guide](guides/EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](guides/SCORE_SEMANTICS_GUIDE.md)
- [Verdict Interpretation Guide](guides/VERDICT_INTERPRETATION_GUIDE.md)
- [Comparison Spine Guide](guides/COMPARISON_SPINE_GUIDE.md)
- [Repeated Window Discipline Guide](guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
- [Portable Eval Boundary Guide](guides/PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Fixture Surface Guide](guides/FIXTURE_SURFACE_GUIDE.md)
- [Blind Spot Disclosure Guide](guides/BLIND_SPOT_DISCLOSURE_GUIDE.md)
- [Shared Proof Infra Guide](guides/SHARED_PROOF_INFRA_GUIDE.md)
- [Artifact Process Separation Guide](guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
- [Baseline Comparison Guide](guides/BASELINE_COMPARISON_GUIDE.md)
- [Regression Proof Surfaces](guides/REGRESSION_PROOF_SURFACES.md)
- [Boundary Route Checklist](guides/BOUNDARY_ROUTE_CHECKLIST.md)

## Operations

- [Releasing `aoa-evals`](operations/RELEASING.md)
- [Questbook Eval Integration](operations/QUESTBOOK_EVAL_INTEGRATION.md)
- [Reviewed Closeout Writeback Proof Ingress](operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md)
- [AGENTS Root Reference](operations/AGENTS_ROOT_REFERENCE.md)

## Recommended Reading Paths

| Path | Route |
| --- | --- |
| New reader | [aoa-evals Bounded Proof Canon](../README.md) -> [Agent Index](architecture/AGENT_INDEX.md) -> [First starter bundle](../evals/workflow/aoa-bounded-change-quality/EVAL.md) -> [Eval Bundle Selection Chooser](../EVAL_SELECTION.md) -> [Eval Bundle Index](../EVAL_INDEX.md) |
| Reviewer | [Eval Rubric](guides/EVAL_RUBRIC.md) -> [Eval Review Guide](guides/EVAL_REVIEW_GUIDE.md) -> [Verdict Interpretation Guide](guides/VERDICT_INTERPRETATION_GUIDE.md) -> bundle notes -> [Blind Spot Disclosure Guide](guides/BLIND_SPOT_DISCLOSURE_GUIDE.md) |
| Mechanics Refactor Path | [Proof Topology](architecture/PROOF_TOPOLOGY.md) -> [Route Residue Guards](architecture/ROUTE_RESIDUE_GUARDS.md) -> [Mechanics Operation Atlas](../mechanics/README.md) -> parent `README.md`/`DIRECTION.md`/`PARTS.md` -> nearest `AGENTS.md` |
| Release and handoff | [Releasing](operations/RELEASING.md) -> [Release Support Mechanic](../mechanics/release-support/README.md) -> readiness, closeout, or PR-handoff report |

## Validation Route

Executable commands for docs-map or docs-owned proof-meaning changes live in
[docs/AGENTS.md#validation](AGENTS.md#validation) and the nearest owner route
card. Generated reader parity routes through
[generated/AGENTS](../generated/AGENTS.md), while mechanic-owned payload docs
route through [mechanics/AGENTS](../mechanics/AGENTS.md) and the package card.
