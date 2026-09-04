# AGENTS.md

## Applies to

This root card applies to the whole `aoa-evals` repository unless a nearer
`AGENTS.md` narrows the touched lane.

## Role

`aoa-evals` is the bounded proof canon of AoA. It owns eval bundle wording,
claim framing, verdict shape, categories, baselines, reports, comparisons,
caveats, generated proof readers, and doctrine about what an eval does and does
not prove.

Claim limit: an eval proves only the bounded claim supported by its source
bundle, evidence, verdict logic, and validation route.

This repository also owns eval-local statistical declarations under `stats/`,
the admitted `aoa-evals-skills` callable procedure under `skills/`, and the
owner-local semantic capability tree under `capabilities/`. Those ports do not
absorb runtime DAG state, shared skill or technique meaning, role policy,
routing, playbooks, durable memory, cross-owner statistics, dashboards, or
private benchmark truth.

## Routes

Follow only the route relevant to the touched source:

| Need | Owner route |
| --- | --- |
| source proof meaning | `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| human repository orientation | `README.md` |
| proof authority class | `docs/architecture/PROOF_TOPOLOGY.md` and `docs/architecture/AGENT_INDEX.md` |
| proof operation | `mechanics/README.md`, then the affected parent, part, and source bundle |
| generated reader change | authored source, owning builder, generated reader, and its validator |
| audit or review | `AUDIT.md`, then the affected proof surface |
| direction | `ROADMAP.md` |
| local memory candidate | `memo/AGENTS.md` and `memo/PORT.yaml`; durable reviewed memory returns to `aoa-memo` |
| local statistics | `stats/AGENTS.md` and `stats/port.manifest.json` |
| callable proof procedure | `skills/AGENTS.md`, `skills/port.manifest.json`, then `skills/aoa-evals-skills/SKILL.md` |
| capability discovery | `capabilities/AGENTS.md`, `capabilities/port.manifest.json`, then the affected family source |
| exact checks | nearest `VALIDATION.md`; named repository lanes remain in `docs/validation/validation_lanes.json` |

For architecture or topology work, consult `DESIGN.md`, `DESIGN.AGENTS.md`, and
`mechanics/EVIDENCE_CLUSTERS.md` only when they can change interpretation of the
touched surface. A nearby README is not mandatory by convention.

## Boundaries and stop-lines

- Keep authored source surfaces stronger than generated, exported, compact,
  runtime, receipt, adapter, and dashboard views.
- Keep self-agency, recurrence, quest, progression, checkpoint, growth,
  comparison, and readiness language bounded, reviewable, evidence-linked, and
  reversible.
- Route shared skill workflow meaning, technique practice meaning, role policy,
  routing, playbooks, memory objects, cross-owner statistics, dashboards, and
  private benchmark truth to their owners.
- Do not turn a bounded eval into a broad intelligence, trust, general safety,
  or autonomous-self claim.
- Do not let a score, report, comparison, trace, receipt, runtime candidate, or
  generated reader become stronger than the source evidence it carries.
- Do not conceal private data, missing evidence, blind spots, or skipped
  validation behind polished wording.

Get explicit human confirmation before changing category, status, baseline
mode, report format, claim type, object under evaluation, default public
baseline or comparison-ladder wording, shared fixture/scorer/runner/report
shape, a new eval bundle, starter-selection posture, or bundle-local support
artifact shape that affects public interpretation.

## Verify

Use the nearest on-demand `VALIDATION.md`; use root [`VALIDATION.md`](VALIDATION.md)
for repository-wide proof topology and generated parity. A green command proves
only its declared check and does not establish release, runtime, proof, or owner
acceptance beyond that scope.

Generated readers change through their owning builders. Do not hand-edit a
derived surface to hide source or freshness debt.

## Landing route

The complete branch, PR, CI, merge, post-landing sync, and release-publication
procedure lives in `docs/operations/RELEASING.md`. `.github/AGENTS.md` owns only
the GitHub-native support files.

If GitHub status or merge permissions cannot be observed, stop and report the
exact blocker. Do not infer a green check, successful merge, tag, release, or
synced canonical state.

## Decision review

Use `docs/decisions/` when a structural, topology, workflow, validation,
public-contract, legacy, runtime-candidate, sibling-reference, or agent-route
choice needs durable rationale. Decision records explain why; current owner
sources define what.

## Closeout

Report changed proof surfaces, whether bounded claim meaning or public posture
moved, exact checks run and skipped, generated/source parity, remaining proof
limits, residual risk, and the next owner route. A closeout that says only
`done` is insufficient.

The historical long-form root guidance remains in
`docs/operations/AGENTS_ROOT_REFERENCE.md`; it is a reference, not active route
law.
