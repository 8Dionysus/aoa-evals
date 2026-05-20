# 0002 Proof Object Authority Contract

- Status: Accepted
- Date: 2026-05-19
- Owner surface: proof bundle and shared proof-contract surfaces

## Context

The repository contains generated catalogs, runtime-candidate readers, receipts,
reports, examples, schemas, quests, and sibling references. These surfaces are
useful, but the refactor plan needs a stable local rule for what owns a bounded
proof claim.

The existing architecture already says an eval bundle packages a bounded claim,
object under evaluation, fixture or case surface, scoring or verdict logic,
execution guidance, baseline or comparison mode, report expectations, and blind
spots. The root design spine turns that into the organizing authority contract.

## Options Considered

- Treat generated catalogs as the main proof map because they are compact.
- Treat reports or receipts as proof authority because they record outcomes.
- Treat the source proof object as the authority and keep derived or emitted
  surfaces subordinate.

## Decision

`aoa-evals` treats the proof object as the source authority for a bounded eval
claim.

For an existing bundle, that proof object is primarily `bundles/*/EVAL.md` plus
`bundles/*/eval.yaml`, supported by bundle-local notes, fixtures, runners,
schemas, reports, and examples when present.

Generated readers, runtime candidates, machine evidence, sibling references,
and receipts may route, summarize, or carry evidence. They do not accept a
verdict without bundle-local review.

## Rationale

This keeps the proof layer self-contained and honest. It lets generated and
runtime-facing surfaces become useful without becoming stronger than the
authored claim, evidence boundary, verdict logic, and blind spots they describe.

## Consequences

- Positive: future mechanics and validators can ask which proof object a
  candidate, report, receipt, or generated entry belongs to.
- Tradeoff: some convenience surfaces must remain visibly weaker even when they
  are easier for agents to consume.
- Follow-up: later validators should check candidate-only posture,
  generated-source derivation, receipt subordination, and proof-object
  completeness more directly.

## Boundaries

This decision does not freeze the current bundle schema forever.

It does not prevent future proof-object drafts outside `bundles/` during
mechanics work, but those drafts must name their authority and promotion route
before being read as accepted eval bundles.

## Validation

- `DESIGN.md` names the proof object as the authority center
- `docs/ARCHITECTURE.md` remains the technical model for eval bundle anatomy
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
