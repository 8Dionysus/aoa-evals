# AGENTS.md

Local guidance for `templates/`.

## Purpose

The active eval bundle template now lives at
`mechanics/proof-object/parts/bundle-authoring/templates/EVAL.template.md`.

This root district is a compatibility route card, not the active template
source.

No active root template payload should live here.

## Rules

Preserve the required headings, frontmatter keys, and placeholders unless the repository-wide bundle contract changes.
Keep `comparison_surface`, `shared_family_path`, `paired_readout_path`, and `integrity_sidecar` explicit in the template where comparison applies.
Keep `comparison_mode` guidance aligned with the report-schema contract for comparative bundles.
Do not turn the template into a doctrine essay or a repo-specific example bundle.
Keep placeholders neutral, bounded, and public-safe.
Do not recreate root `templates/EVAL.template.md`; route authoring work through the proof-object part.

## Validation

After template edits, run `python scripts/validate_repo.py`.
