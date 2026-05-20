# 0003 Sibling Proof Reference Compatibility

- Status: Accepted
- Date: 2026-05-19
- Owner surface: sibling reference checks and proof evidence references

## Context

The current repository validation fails because several `aoa-memo` evidence and
artifact references point at paths that moved in the sibling repository.

That failure is not merely a broken-link chore. It shows that `aoa-evals` needs
a local compatibility posture for proof references whose source owner is a
sibling repo.

## Options Considered

- Patch every failing path directly and treat the failure as a one-off.
- Edit sibling repositories so old `aoa-evals` references pass again.
- Add a local compatibility/provenance route that can distinguish current,
  intentionally legacy, rejected, and unresolved sibling references.

## Decision

Repair sibling reference drift from inside `aoa-evals` unless the user
explicitly routes work to the sibling owner.

For `aoa-evals`, a sibling proof reference is an input to bounded proof review,
not a transfer of sibling authority. Future repair should preserve enough
provenance to tell whether a reference is current, intentionally legacy,
accepted as a historical input, or invalid.

## Rationale

The proof layer must remain self-contained and reviewable while acknowledging
that some evidence points to neighboring owners. A compatibility bridge makes
future drift inspectable instead of hiding it behind ad hoc path edits.

## Consequences

- Positive: validation failures can become a designed proof-reference boundary.
- Tradeoff: local repair may need a small mapping or provenance surface before
  all references are updated.
- Follow-up: the next sibling-reference slice should fix the currently failing
  `aoa-memo` refs through current paths or an explicit compatibility bridge,
  then rerun `python scripts/validate_repo.py`.

## Boundaries

This decision does not authorize changing `aoa-memo`.

It does not make `aoa-evals` the owner of memory truth, runtime truth, or old
memo path aliases. It only defines how local proof references should remain
honest when sibling topology moves.

## Validation

- current baseline failure is visible through `python scripts/validate_repo.py`
- failing refs are limited to sibling path drift in `aoa-memo`
- future repair should leave `validate_repo.py` green without editing sibling
  repos unless separately authorized
