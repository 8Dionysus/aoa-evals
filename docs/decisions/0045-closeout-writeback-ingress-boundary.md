# 0045 Closeout Writeback Ingress Boundary

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`

## Context

`docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` preserves a repeated
closeout survivor:
`candidate:proof:aoa-evals-runtime-candidate-template-index-min`.

The note already says it is an owner-local ingress anchor, not a second source
of truth. `quests/closeout/captured/AOA-EV-Q-0013.yaml` also keeps the cue as
captured proof pressure until another reviewed route supplies a concrete
claim, fixture, and verdict boundary.

Nearby active surfaces exist, but they are narrower:

- `evals/workflow/aoa-memo-writeback-act-integrity/` owns the confirmed base
  writeback-act proof bundle.
- `mechanics/proof-infra/parts/fixture-families/fixtures/memo-writeback-act-guardrail-v1/`
  owns the shared writeback-act fixture family.
- `mechanics/audit/parts/selected-evidence-packets/` owns the selected
  runtime evidence sidecar.
- `mechanics/distillation/parts/runtime-candidate-adoption/` owns reviewed
  runtime distillation candidate adoption, not confirmed writeback-act proof.
- `mechanics/growth-cycle/parts/diagnosis-gate/` owns diagnosis-cause
  discipline, not closeout-chain promotion.

## Options Considered

- Move the ingress note into `mechanics/growth-cycle/` as a
  `reviewed-closeout-chain` part.
- Move the ingress note into `mechanics/distillation/` because it names the
  next reviewed-candidate gap.
- Keep the note as root ingress and quest pressure until a separate active
  operation exists.

## Decision

Keep `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` in root `docs/` as an
ingress anchor.

Do not promote it into `growth-cycle`, `distillation`, or a new parent mechanic
in this slice.

Clarify the Distillation and Growth Cycle package cards so future agents read
the note as related ingress/deferred context, not as an active source surface
or part-local contract.

## Rationale

The evidence does not yet prove an active `reviewed-closeout-chain`,
`owner-followthrough`, or writeback-stage part. It proves a repeated cue and a
quest obligation.

Moving the file now would make topology look more complete than the proof
surface is. It would also invite the exact failure mode this refactor is trying
to eliminate: naming a parent or part from pressure vocabulary before the
cross-root operation has inputs, outputs, stop-lines, and validation.

## Consequences

- Positive: the root ingress role stays visible and honest.
- Positive: `distillation` no longer lists the ingress note as an active source
  surface.
- Positive: `growth-cycle` separates active diagnosis surfaces from deferred
  closeout/writeback context.
- Tradeoff: root `docs/` keeps one narrow ingress file for now.
- Follow-up: if another reviewed owner-followthrough route produces a concrete
  claim, fixture, verdict boundary, and validation path, reconsider a narrow
  part under the correct parent.

## Boundaries

This decision does not weaken the base writeback-act bundle.

It does not make reviewed-candidate adoption part of confirmed writeback-act
proof.

It does not authorize a `reviewed-closeout-chain`, `donor-harvest`,
`quest-promotion`, or `owner-followthrough` part without a later evidence pass.

It does not move sibling owner meaning into `aoa-evals`.

## Validation

- `mechanics/distillation/README.md` and
  `mechanics/distillation/parts/runtime-candidate-adoption/README.md` list the
  ingress note only as related ingress.
- `mechanics/growth-cycle/README.md` separates active diagnosis source
  surfaces from deferred closeout/writeback context.
- `docs/LEGACY_NAMING.md` maps the root ingress path as active ingress, not an
  active mechanic part.
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`

## Current Applicability

As of 2026-05-24:

- Still valid: `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md` remains the
  root owner-local ingress anchor for the closeout/writeback survivor.
- Changed: the active note now names its positive route as traceable proof ingress,
  owner-local re-read anchor, and source-bundle handoff.
- Source surfaces updated: `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation route: `python -m pytest -q tests/test_validate_repo.py -k closeout_writeback_ingress`
  and `python scripts/validate_repo.py`.

## Review Log

### 2026-05-24 - Ingress route language clarified

- Previous assumption: the note could describe its role by saying it was not a
  second source, not a shadow copy, and not a new bundle.
- New reality: low-context agents need the active route first: re-read anchor,
  bundle source surface, neighboring proof context, and deferred new-bundle
  authority.
- Reason: the file is still active root ingress, so its first read should route
  the agent to the source bundle and future evidence pass.
- Source surfaces updated: `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k closeout_writeback_ingress`
  and `python scripts/validate_repo.py`.
