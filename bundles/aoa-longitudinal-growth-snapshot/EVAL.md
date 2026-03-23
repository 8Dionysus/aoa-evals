---
name: aoa-longitudinal-growth-snapshot
category: longitudinal
status: draft
summary: Checks whether ordered, comparable windows on the same bounded workflow surface show modest directional movement without upgrading that movement into broad capability growth.
object_under_evaluation: ordered repeated-window movement on a bounded workflow surface
claim_type: longitudinal
baseline_mode: longitudinal-window
report_format: comparative-summary
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-longitudinal-growth-snapshot

## Intent

Use this eval to check whether ordered, comparable windows on the same bounded workflow surface show modest directional movement.

This starter bundle is a `diagnostic` longitudinal eval.
It is a report-led movement surface.
Its primary anchor is `aoa-bounded-change-quality`.
It is not meant to replace one-run workflow reading,
and it is not a frozen same-task comparator.

The goal is not to prove general capability growth.
The goal is to test one bounded claim:

across ordered, comparable evaluation windows on the same bounded workflow surface,
the repository can describe modest directional movement
without upgrading that movement into broad capability growth.

## Object under evaluation

This eval checks ordered repeated-window movement on a bounded workflow surface.

Primary surfaces under evaluation:
- directional movement on the `aoa-bounded-change-quality` workflow surface
- whether ordered windows are comparable enough for a bounded movement read
- whether style-only or report-only changes are kept separate from workflow growth
- whether the final longitudinal summary stays modest about what movement means

Nearby surfaces intentionally excluded:
- one-run workflow judgment by itself
- frozen same-task regression as a substitute for trend reading
- cross-surface artifact or process blending
- general capability growth across broader task families

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
ordered windows on the same bounded workflow surface
show a modest improvement signal,
regression signal,
flat reading,
or mixed movement
that remains bounded to this named workflow surface.

This eval does **not** support claims such as:
- the agent is getting better in general
- the workflow surface improved across all task families
- the movement is durable outside the named window sequence
- a longitudinal snapshot replaces same-task regression or one-run diagnostics

## Trigger boundary

Use this eval when:
- you have ordered windows on the same bounded workflow surface
- the main question is directional movement across windows rather than one-run quality
- you can name the window sequence and the comparability contract clearly
- style or report polish might otherwise masquerade as workflow growth

Do not use this eval when:
- you only need a one-run workflow judgment
- you need a frozen same-task baseline comparison rather than repeated-window movement
- the window sequence is too inconsistent to compare honestly
- the main question is cross-surface blending rather than bounded workflow movement

## Inputs

- ordered named windows
- one bounded workflow surface anchored in `aoa-bounded-change-quality`
- one public report or summary artifact per window
- context notes for environment, reviewer, or policy changes if they matter materially
- longitudinal comparison rubric

## Fixtures and case surface

This starter bundle should use ordered windows that stay on the same bounded workflow surface.

A strong v1 window sequence should include:
- a visible bounded improvement sequence
- a visible bounded regression sequence
- a mostly flat or noisy sequence
- a style-only or report-only shift that should not count as workflow growth
- a sequence where context drift is large enough to force a cautious or mixed reading

Window sequences should avoid:
- blending multiple unrelated workflow surfaces
- hidden local history that outside reviewers cannot inspect
- windows whose case family or review contract changes silently
- raw run histories that require new infra to interpret

The evidence surface is public-safe when:
- each window has a compact public report or summary artifact
- the named workflow surface stays the same across windows
- context changes are disclosed where they matter materially
- another repo could replace the reports with comparable bounded window artifacts and preserve the same movement question

The current materialized shared family is `fixtures/repeated-window-bounded-v1/README.md`.

## Scoring or verdict logic

This eval prefers per-window notes plus a comparative bundle-level verdict.

Canonical longitudinal readings for v1:
- `bounded improvement signal`
- `mixed or unstable movement`
- `no clear directional movement`
- `bounded regression signal`

Per-window-sequence review should ask:
- is the same bounded workflow surface being read in each window?
- does the next window show a reviewable strengthening, weakening, or flat reading on that surface?
- is the visible movement real, or mostly style or reporting drift?
- did context shift enough that a cautious or mixed read is more honest?
- does the bundle-level summary stay weaker than the strongest-looking local move?

Bundle-level reading should stay downstream of the named windows and their reports.
If the sequence contains materially different movement classes,
prefer `mixed or unstable movement` over a cleaner story.

### Approve signals

Signals toward `bounded improvement signal`:
- later windows show reviewable workflow strengthening on the same bounded surface
- the movement is not mostly style or summary polish
- context notes do not reveal hidden semantic drift
- the final summary remains bounded to the named workflow surface

Signals toward `no clear directional movement`:
- the windows remain broadly similar on the bounded workflow surface
- visible movement is too small, too style-shaped, or too noisy for a stronger claim

### Degrade signals

Signals toward `mixed or unstable movement` or `bounded regression signal`:
- later windows lose a bounded workflow strength that earlier windows had
- context drift weakens comparability enough to block a clean trend read
- style-only movement is upgraded into growth
- the summary narrates a clean improvement story that the windows do not support

## Baseline or comparison mode

This starter bundle uses `longitudinal-window`.

In this surface:
- the windows must be ordered and named
- the bounded workflow surface must stay the same
- context changes that affect comparability must be disclosed
- style-only or report-only movement should default to `no clear directional movement` or `mixed or unstable movement`

For a frozen same-task comparison against one fixed baseline,
use `aoa-regression-same-task` instead.

## Execution contract

A careful run should:
1. define the ordered window sequence and the bounded workflow surface
2. gather one public report or summary artifact per window
3. disclose context changes that matter to comparability
4. review directional movement between windows on the named surface
5. assign per-window or per-transition notes
6. publish one comparative-summary artifact with a bounded longitudinal verdict

Execution expectations:
- do not silently rewrite the workflow surface mid-sequence
- do not treat report polish as workflow growth by default
- do not let one vivid window erase mixed or flat evidence elsewhere
- keep enough evidence that a careful reviewer can see why the directional reading was assigned
- when shipping a machine-readable report, validate it against `reports/summary.schema.json`
- keep the repeated-window read compatible with `reports/repeated-window-proof-flow-v1.md`

## Outputs

The eval should produce:
- one bundle-level longitudinal verdict
- ordered window notes
- movement summary on the named workflow surface
- context-shift note where needed
- explicit interpretation boundary
- an optional schema-backed companion report artifact at `reports/example-report.json`

A compact public comparative-summary may include:
- window id
- anchor workflow note
- context note
- movement reading relative to the previous window
- bundle-level verdict
- caution about what the result still does not prove

## Failure modes

This eval can fail as an instrument when:
- windows are not actually comparable
- the workflow surface drifts across the sequence
- reviewers confuse cleaner reporting with stronger workflow behavior
- context changes are hidden
- the summary turns bounded movement into a growth myth
- one window dominates the story unfairly

## Blind spots

This eval does not prove:
- general capability growth
- movement outside the named workflow surface
- frozen same-task regression
- artifact or process movement across other surfaces
- durable long-term improvement beyond the named windows

Likely false-pass path:
- later windows look cleaner and more confident, but the bounded workflow evidence did not materially strengthen.

Likely misleading-result path:
- real movement can look mixed if the context changed enough that comparability weakened sharply.

Nearby claim classes that should use a different bundle instead:
- one-run workflow quality should use `aoa-bounded-change-quality`
- frozen same-task comparison should use `aoa-regression-same-task`
- artifact-versus-process divergence should use `aoa-output-vs-process-gap`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
across this named ordered window sequence,
the bounded workflow surface showed a modest directional movement signal.

Do not treat a positive result as:
- proof of general capability growth
- proof that all nearby workflow diagnostics improved
- proof that the movement is stable outside this window sequence
- proof that the same story would hold on a different task family

Use this bundle together with `aoa-regression-same-task`
when you need both:
- a repeated-window movement read
- and a tighter frozen-baseline comparison on one fixed task family

A negative, mixed, or flat result is valuable because it can reveal:
- bounded regression
- unstable movement
- flat performance hidden behind nicer reports
- context drift large enough to weaken comparison

## Verification

- confirm the bounded claim is explicit
- confirm windows are ordered, named, and comparable
- confirm the named workflow surface stays the same across windows
- confirm style-only movement is not upgraded into growth
- confirm the bundle-level verdict does not outrun the window evidence

## Technique traceability

Primary source techniques:
- AOA-T-0001 plan-diff-apply-verify-report

## Skill traceability

Primary checked skill surface:
- aoa-change-protocol

## Adaptation points

Project overlays may add:
- local window definitions
- local public report sinks
- local context notes for reviewer or policy changes
- local ordered release or evaluation milestones

