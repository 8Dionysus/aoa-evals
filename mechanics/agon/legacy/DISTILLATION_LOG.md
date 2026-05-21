# Agon Legacy Distillation Log

## 2026-05-19 Mechanics Refactor

Agon moved from a proof-suffix parent into the active `mechanics/agon/` parent.

Distilled into active parts:

- seed configs, schemas, examples, generated registries, scripts, tests, and
  recurrence manifests moved into the owning `mechanics/agon/parts/<part>/`
  homes;
- package-level route cards now name `agon` as the parent mechanic;
- historical wave landing files remain under `legacy/raw/`;
- former Agon markdown quest notes moved out of active `quests/` lifecycle
  paths and into `legacy/raw/`;
- `legacy/INDEX.md` maps wave files to current active part routes.

Still historical:

- wave labels;
- `AOE-Q-AGON-*` markdown quest-note form;
- old docs-root landing files;
- old `agon-proof` parent wording;
- any path that uses a wave name as active topology.

Do not create new work in legacy. Distill into an active part first.
