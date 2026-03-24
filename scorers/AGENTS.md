# AGENTS.md

Local guidance for `scorers/`.

## Purpose

`scorers/` stores shared bounded helpers for reportable proof artifacts.

## Current surface

- `bounded_rubric_breakdown.py`

## Rules

Shared helpers may format or normalize bounded breakdowns, but they must remain reviewable enough for outside inspection.
Never let a scorer outrank the bundle-local meaning in EVAL.md.
Do not flatten a bounded proof surface into one generic score without explicit bundle-level interpretation.
Preserve helper support for transition-note and integrity-risk payloads when editing repeated-window or sidecar-related logic.
