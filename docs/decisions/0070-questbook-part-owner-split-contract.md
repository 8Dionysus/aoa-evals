# 0070 Questbook Part Owner-split Contract

## Status

Accepted.

## Context

`mechanics/questbook/` routes the quest obligation loop:

`source quest record -> human open-obligation index -> generated quest reader -> deferred return or reviewed promotion`

Its active parts are close but not interchangeable:

- `source-record-contract` owns source quest schema, lane/state consistency,
  lifecycle posture, and stable quest record shape.
- `dispatch-reader` owns generated quest catalog and dispatch projection shape
  and drift detection.

Without explicit stronger-owner split, a quest source record can be mistaken
for a proof verdict or roadmap command, and a generated dispatch reader can be
mistaken for live authority, owner acceptance, or proof-surface promotion.

## Decision

Require both questbook part README files to expose `## Stronger Owner Split`
and `## Stop-Lines`:

- `mechanics/questbook/parts/source-record-contract/README.md`
- `mechanics/questbook/parts/dispatch-reader/README.md`

Source quest records stay under `quests/<lane>/<state>/`. Human visibility stays
in `QUESTBOOK.md`. Generated quest readers stay under root `generated/` as
derived navigation. Eval bundles, proof mechanics, sibling repositories, and
owner-local surfaces keep stronger verdict, promotion, acceptance, and
implementation truth.

## Consequences

- Future questbook edits must preserve the split between source quest truth,
  human obligation visibility, generated navigation, and later proof or owner
  acceptance.
- `aoa-quest-harvest` may support triage, but it must not become source truth.
- Generated dispatch may route attention, but it must not become live task assignment,
  release readiness, portable verdict authority, or promotion proof.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k questbook_part_owner_split
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q
```
