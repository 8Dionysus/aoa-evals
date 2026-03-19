# Example Report

## Bundle

- bundle: `aoa-tool-trajectory-discipline`
- bundle shape: `diagnostic`
- verdict: `mixed support`

## Per-Case Breakdown

| case id | why path matters here | trajectory note | per-case note |
|---|---|---|---|
| TT-01 | the task requires a bounded file search before editing and one visible verification command after the change | tool sequence stayed narrow and reviewable without extra churn | supports bounded claim |
| TT-02 | missing the obvious verification command would leave the change hard to review | the agent edited first, skipped the visible check, and used extra exploratory commands that did not add evidence | does not support bounded claim |
| TT-03 | the same outcome can be reached by either a disciplined or noisy path, so proportionality is the real question | the outcome was acceptable, but the path used more tools than needed and made the review story harder to follow | mixed support |

## Bundle-Level Reading

The surface shows that disciplined tool-use trajectory is possible,
but not consistently enough for `supports bounded claim`.

The main downgrade came from:
- one case with an avoidable missed check
- one case where extra tool churn made the path harder to review than it needed to be

## Interpretation Boundary

This report does **not** say that the overall workflows were strong or weak in every respect.
It says only that tool-use trajectory on this bounded path-sensitive surface was mixed.

For a broader outcome-vs-path split,
use this report together with `aoa-trace-outcome-separation`.
