# Spark Swarm Recipe — aoa-evals

Рекомендуемый путь назначения: `Spark/SWARM.md`

## Для чего этот рой
Используй Spark здесь для одного bounded eval bundle или одного eval seam за раз: fixtures, scorers, verdict/report contracts, regression/comparison surfaces. Рой должен строить форму доказательства, а не делать театр тотального IQ-скора.

## Читать перед стартом
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/EVAL_PHILOSOPHY.md`
- `EVAL_INDEX.md`
- `bundles/aoa-bounded-change-quality/EVAL.md`
- `templates/EVAL.template.md`

## Форма роя
- **Coordinator**: выбирает один bounded claim
- **Scout**: картографирует bundle, fixtures, scorers, runners, schemas и blind spots
- **Builder**: делает минимальный bundle-level diff
- **Verifier**: гоняет repo validation и build catalog
- **Boundary Keeper**: следит за bounded claims, named blind spots и anti-overclaim posture

## Параллельные дорожки
- Lane A: `EVAL.md` / `eval.yaml` / bundle contract
- Lane B: fixtures / scorers / report schema / runner contract
- Lane C: generated catalogs only if rebuild needed
- Не запускай больше одного пишущего агента на одну и ту же семью файлов.

## Allowed
- создать или починить один portable eval bundle
- добавить shared fixture family или scorer helper для выбранного claim
- усилить regression/comparison/readout surfaces
- прояснить blind spots и interpretation guidance

## Forbidden
- превращать один eval в total intelligence score
- скрывать blind spots
- таскать сюда project-local QA без portable contract
- подменять techniques/skills meaning
- добавлять undocumented verdict logic

## Launch packet для координатора
```text
We are working in aoa-evals with a one-repo one-swarm setup.
Pick exactly one bounded claim.
First return:
1. the claim
2. object under evaluation
3. in-scope / out-of-scope
4. files to touch
5. which lane each agent owns

The swarm must keep this repository as proof canon:
portable, bounded, reviewable, explicit about blind spots.
```

## Промпт для Scout
```text
Map only. Do not edit.
Return:
- nearest existing eval bundle(s)
- fixtures/scorers/runners/schemas likely affected
- current blind spots
- whether this is capability/workflow/boundary/artifact/regression/comparative/longitudinal/stress
- what would make this overclaim if done badly
```

## Промпт для Builder
```text
Make the smallest reviewable change.
Rules:
- keep the claim bounded
- make verdict logic explicit
- name blind spots
- prefer portable contracts over repo-local hacks
- keep human-readable meaning primary
```

## Промпт для Verifier
```text
Run the repo validation loop and report actual results.
Required:
- python -m pip install -r requirements-dev.txt
- python scripts/validate_repo.py
- python scripts/build_catalog.py
Return:
- commands run
- whether generated surfaces changed
- whether the bundle states what it can and cannot support
```

## Промпт для Boundary Keeper
```text
Review only for anti-overclaim and anti-scope.
Check:
- not a total score
- one claim only
- interpretation guidance is explicit
- blind spots named
- no secret-bearing fixtures or raw dumps
- no undocumented scoring logic
```

## Verify
```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python scripts/build_catalog.py
```

## Done when
- один bounded claim оформлен как portable proof surface
- what it can support / cannot support названо явно
- blind spots и interpretation guidance присутствуют
- repo validation and build catalog реально прогнаны

## Handoff
Если рой нашёл reusable execution pattern, follow-up идёт в `aoa-skills` или `aoa-techniques`, а не продолжает распухать здесь.
