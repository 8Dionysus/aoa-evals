# Search Coverage Contract

The search obligation is conditional, but it must be explicit.

## Coverage Fields

For each case, classify these surfaces as `covered`, `not_applicable`,
`insufficient`, `missing`, or `blocked`:

- `.aoa` session evidence: search hits, segment refs, retrieve refs, raw refs,
  or a justified not-applicable note
- source refs: owner repo files, route cards, contracts, decisions, reports, or
  other authored surfaces that support the memory-worthy question
- landed-work lens: PR, diff, commit, release note, review thread, or final
  report when it reconciles what landed
- memo recall or pending exports: reviewed `aoa-memo` recall, pending export,
  generated readout, or a justified not-applicable note
- local memo port status: `memo/` port exists and was checked, is missing, is
  stale, or does not apply to the owner route
- privacy review: public packet safety, raw transcript exclusion, and
  secret/operator-sensitive material exclusion

## Missed-Evidence Risk

Missed-evidence risk must be one of:

- `none`
- `low`
- `medium`
- `high`
- `blocking`

Use `high` or `blocking` when a relevant `.aoa`, owner-source, memo recall,
pending-export, or local-port surface was not inspected and could change the
decision outcome.

## Evidence Discipline

`.aoa` refs are evidence handles. They do not become reviewed memory truth.

PRs, diffs, commits, releases, and review threads are reconciliation lenses.
They do not replace session evidence when the meaning lived in the session.

Memo recall and pending exports are context. They do not authorize durable
memory landing from this eval.
