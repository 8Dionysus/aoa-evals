# 0039 Recurrence Support Parts Expansion

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/recurrence/`

## Index Metadata

- Surface classes: mechanic part
- Mechanic parents: recurrence
- Guard families: part and payload
- Posture: active rationale

## Context

The first recurrence package slice made `control-plane-integrity` active and
left return-aware families bundle-local. A later root-district pass showed that
several recurrence support families already had more than one bundle-local
mention:

- `aoa-return-anchor-integrity` had a shared fixture family, bundle contracts,
  report contracts, generated catalog references, audit-selected runtime
  sidecar, and recurrence proof-program routing.
- `aoa-memo-recall-integrity` had a shared fixture family, bundle contracts,
  phase-alpha report, audit-selected runtime evidence, generated readers, and
  tests.
- Recursor readiness boundary had a bundle extension note, fixture cases,
  scorer, runner, and tests.
- `aoa-stats-regrounding-boundary-integrity` had a shared fixture family,
  bundle contracts, report schema/example, generated readers, and tests.

These are recurrence proof support operations. They are not new parent
mechanics, and they are not Distillation, audit, stats, or memo truth.

## Decision

Keep `mechanics/recurrence/` as the AoA-aligned parent and add active parts:

- `anchor-return`
- `memory-recall`
- `recursor-boundary`
- `stats-regrounding-boundary`

Move only support artifacts into those parts. Source proof bundles stay under
`evals/`, and selected runtime evidence stays under `mechanics/audit/`.

Continuity-anchor and self-reanchor remain bundle-local because they do not yet
have the same support-artifact depth.

## Rationale

The correct topological move is to make the existing recurrence mechanic more
convex, not to invent parents such as `memo-proof`, `recursor-readiness`, or
`stats-proof`.

These part names describe narrower support operations inside recurrence:
return to anchor, memory recall as recurrence recall proof, recursor boundary
as readiness-only no-spawn proof, and stats re-grounding as return-to-owner
truth boundary proof.

## Current Applicability

As of 2026-05-24:

- Still valid: `anchor-return`, `memory-recall`, `recursor-boundary`, and
  `stats-regrounding-boundary` remain recurrence support parts.
- Changed: active part contracts now expose pressure-to-owner route rows, and
  validator tokens guard those rows.
- Superseded by: none.

## Review Log

### 2026-05-24 - Support part boundary route wording

- Previous assumption: support part READMEs could keep boundaries as direct
  claim exclusions.
- New reality: the part contracts now route each boundary pressure to the
  owner that can act on it.
- Reason: a low-context agent should see where return quality, memory canon,
  recursor activation, stats truth, route approval, runtime behavior, and owner
  acceptance go next without parsing a prohibition list.
- Source surfaces updated:
  `mechanics/recurrence/parts/anchor-return/README.md`,
  `mechanics/recurrence/parts/memory-recall/README.md`,
  `mechanics/recurrence/parts/recursor-boundary/README.md`,
  `mechanics/recurrence/parts/stats-regrounding-boundary/README.md`, and
  `scripts/validate_repo.py`.
- Validation: recurrence validator focus, recurrence part runners and tests,
  catalog check, root validation, semantic AGENTS validation, diff whitespace
  check, and full pytest passed.

## Boundaries

This decision does not move source proof bundles into mechanics.

It does not claim memory canon, recursor activation, stats-as-proof, route
approval, runtime self-healing, global recurrence completeness, owner artifact
truth, or hidden continuity.

`aoa-memo`, `aoa-agents`, `aoa-sdk`, `aoa-stats`, `aoa-routing`, runtime
owners, and source owner repositories keep stronger local truth.

## Validation

- `mechanics/recurrence/README.md`, `PARTS.md`, and `PROVENANCE.md` route the
  new parts and bridge old placement questions into the owning legacy archive.
- `docs/architecture/PROOF_TOPOLOGY.md`, `docs/architecture/LEGACY_NAMING.md`, and
  `mechanics/EVIDENCE_CLUSTERS.md` name the updated topology.
- `scripts/validate_repo.py` checks the recurrence package and active support
  part route tokens.
- `python mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py --case mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/cases/RRB-001.no-spawn-readiness.json --check-expected --json`
- `python -m pytest -q mechanics/recurrence/parts/recursor-boundary/tests/test_recursor_readiness_boundary_eval_seed.py mechanics/recurrence/parts/memory-recall/tests/test_memo_recall_phase_alpha_report.py mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
