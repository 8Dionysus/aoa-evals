# Session Survivor Placement

This note preserves the proof-shaped survivors from
`session:2026-04-13T23-45-25-274328Z-aoa-sdk-checkpoint-growth-8a1bacd7-bd9`.

It is a bounded owner-local hold note. It does not change the eval verdict
logic, does not make the SDK fixture proof by itself, and does not create a new
runtime runner.

## Surviving units

- `candidate:proof:aoa-evals-runtime-candidate-template-index-min`
- `candidate:growth:aoa-evals-commit-code`

## Landing judgment

- the proof survivor belongs beside this bundle because the bundle already owns
  the A2A summon return checkpoint proof contract
- the growth survivor is evidence that this bundle and its fixture contract
  moved during the session, not proof that the eval is mature
- the nearest wrong target is `aoa-skills`; a proof-shaped candidate should not
  become a skill just because the route involved `aoa-summon`

## Evidence refs

- `repo:aoa-sdk/.aoa/session-growth/current/8a1bacd7-bd9a-48bf-a197-3a04f25b86a5/aoa-sdk/reviewed-closeout-live.md`
- `repo:aoa-sdk/.aoa/closeout/handoffs/session-2026-04-13T23-45-25-274328Z-aoa-sdk-checkpoint-growth-8a1bacd7-bd9.owner-handoff.json`
- `repo:aoa-evals/commit:7e4bfb3a559aa67d3df2fcca92e1d7389961dfc8`
- `repo:aoa-evals/bundles/aoa-a2a-summon-return-checkpoint/EVAL.md`
- `repo:aoa-evals/bundles/aoa-a2a-summon-return-checkpoint/fixtures/contract.json`
- `repo:aoa-evals/fixtures/a2a-summon-return-checkpoint-v1/README.md`

## Next honest move

Keep the survivor as proof-surface carry until another reviewed A2A summon
return route either strengthens this bundle with an additional case or proves a
separate eval boundary. Do not promote it to a new eval, skill, or verdict
claim from this single session.
