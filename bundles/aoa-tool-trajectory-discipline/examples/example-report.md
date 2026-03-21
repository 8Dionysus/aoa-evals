# Example Report

## Bundle

- bundle: `aoa-tool-trajectory-discipline`
- bundle shape: `diagnostic`
- verdict: `mixed support`

## Bounded Promotion Readout

- approve when the report keeps why-path-matters, trajectory note, and bundle-level verdict distinct
- defer when avoidable churn or skipped checks are laundered into a clean workflow story
- failure is the path-evidence mismatch
- readout is the public description of that mismatch

## Per-Case Breakdown

| case id | why path matters here | trajectory note | failure vs readout | outcome |
|---|---|---|---|---|
| TT-01 | the task requires a bounded file search before editing and one visible verification command after the change | tool sequence stayed narrow and reviewable without extra churn | aligned; the readout shows why the path was disciplined | approve |
| TT-02 | missing the obvious verification command would leave the change hard to review | the agent edited first, skipped the visible check, and used extra exploratory commands that did not add evidence | the failure is an avoidable omission plus churn, and the readout keeps both visible | approve |
| TT-03 | the same outcome can be reached by either a disciplined or noisy path, so proportionality is the real question | the outcome was acceptable, but the summary tried to reframe extra tool churn as helpful thoroughness | the failure is decorative path theater hidden by the readout | defer |

## Bundle-Level Reading

The surface shows that disciplined tool-use trajectory is possible,
but not consistently enough for `supports bounded claim`.

The main downgrade came from:
- one case with an avoidable missed check
- one case where extra tool churn was almost laundered into a cleaner-looking workflow story

## Failure vs Readout

- failure means the case evidence did not support the trajectory claim
- readout means the public summary of that case
- a disciplined final outcome does not repair weak tool-path evidence
- a bounded readout can still approve a case when the weakness is named honestly

## Interpretation Boundary

This report does **not** say that the overall workflows were strong or weak in every respect.
It says only that tool-use trajectory on this bounded path-sensitive surface was mixed.

For a broader outcome-vs-path split,
use this report together with `aoa-trace-outcome-separation`.
