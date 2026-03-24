# AGENTS.md

Local guidance for `templates/`.

## Purpose

`EVAL.template.md` is the starter authoring scaffold for new eval bundles.

## Rules

Preserve the required headings, frontmatter keys, and placeholders unless the repository-wide bundle contract changes.
Keep `comparison_surface`, `shared_family_path`, `paired_readout_path`, and `integrity_sidecar` explicit in the template where comparison applies.
Keep `comparison_mode` guidance aligned with the report-schema contract for comparative bundles.
Do not turn the template into a doctrine essay or a repo-specific example bundle.
Keep placeholders neutral, bounded, and public-safe.

## Validation

After template edits, run `python scripts/validate_repo.py`.
