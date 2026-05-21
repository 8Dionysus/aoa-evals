# AGENTS.md

## Applies to

`mechanics/growth-cycle/legacy/`.

## Role

This directory preserves Growth Cycle provenance. It is not an active work
surface.

## Rules

- Start from `../README.md`, `../PARTS.md`, and `../PROVENANCE.md`.
- Do not begin new Growth Cycle work here.
- Do not treat deferred closeout, harvest, repair, progression, or quest
  pressure as active just because it is listed in legacy.
- Do not move raw files here without updating `../PROVENANCE.md`, `INDEX.md`,
  and validation.

## Validation

Run root validation after editing:

```bash
python scripts/validate_repo.py
```
