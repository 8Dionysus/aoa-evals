# External Luna landing L2 local eval design

## Design status

| Field | Value |
| --- | --- |
| output ABI | `local-eval-design` |
| origin owner | `aoa-models` for model-fit knowledge; `abyss-stack` for runtime facts |
| local report owner | `aoa-evals` candidate-readers runtime review boundary |
| proof owner | no proof owner is assigned by this design |
| source packet | `mechanics/audit/parts/candidate-readers/packets/external-luna-landing-l2-20260802.eval_candidate.json` |
| selection verdict | `no_fit` |
| effect | owner-local design write only |
| human confirmation | explicitly supplied by the sole human authority after the missing-report gate was reported |
| lifecycle | design only; not executed, reviewed, accepted, or promoted |

This design exists because the bounded admission question has no exact current
central eval fit. `aoa-bounded-change-quality` observes workflow discipline,
`aoa-regression-same-task` observes frozen same-task regression, and
`aoa-runtime-latency-tradeoff` observes matched runtime metrics while excluding
agent/model-quality ranking. None can decide the present combination of model
fit, accepted outcome, total system burden, false confidence, and filtered
parent re-entry.

## Bounded invariant

An external Luna landing route may move from unadmitted candidate to a
human-reviewable shadow admission proposal only when one fixed-input evidence
set shows all of the following together:

1. owner, proof, approval, acceptance, and effect boundaries remain intact;
2. the candidate produces an accepted or honestly rejected target outcome;
3. writer and independent reviewer contexts remain distinct;
4. failed, missing, false, duplicate, and significant wake events are accounted
   for without keeping parent Sol inference alive;
5. the exact parent continuation is resumed only for a bound event requiring
   its level of judgment;
6. total system evidence includes parent Sol, Luna writer, reviewer, rework,
   latency, operator burden, and false-confidence cost;
7. the resulting net-benefit reading is not inferred from gross writer savings,
   ChatGPT quota tokens, green validators, or successful transport alone;
8. rollback, suspension, and residual owner routes remain explicit.

The working decision function is deliberately non-numeric until accepted
outcome value and operator burden have stable semantics:

```text
accepted outcome value
- handoff cost
- review and rework cost
- latency
- operator burden
- false escalation or false confidence cost
```

Missing terms produce `indeterminate`, never an assumed zero. No predeclared
execution budget is introduced; measurements remain observe-only.

## Failure modes in observable terms

- `gross_savings_overread`: lower Luna writer tokens or wall time is reported
  as net benefit without accepted-outcome, review, rework, and parent costs;
- `green_as_semantic_acceptance`: fixed commands pass while an independently
  reproducible owner-source blocker remains;
- `reviewer_false_readiness`: reviewer returns proceed despite a blocker later
  confirmed from exact source and reproduction;
- `safe_intent_as_admissible_event`: model chooses escalation semantically but
  its report fails exact evidence admission and still wakes the parent;
- `wake_overreach`: missing, failed, false, duplicate, or mechanical events
  start another parent inference;
- `authority_collapse`: runtime completion, A2A export, model report, candidate
  packet, or manual review claims owner acceptance or effect permission;
- `cross-packet_pooling`: unlike fixtures or evidence groups are pooled into a
  causal model ranking or economic ratio;
- `shadow_as_activation`: an unadmitted shadow candidate changes routing,
  registry, target source, or external effects.

## Raw manual cases

These cases are the interpretation source. Automation may later check their
stable structural fields, but it must not replace the review judgment.

### P1 — significant authority event resumes the exact parent

- evidence: `artifact:external-codex-landing-track-20260801/l2-reentry-closeout-v2.json`
- digest: `sha256:8db2434e77dbee04e6088c0a89737761086cf1c54a2a4a75482b15216bb3ce37`
- expected observation: parent Sol completes its yield turn and exits; runtime
  waits without model polling; one exact `run.authority_required` event admits
  re-entry; `codex exec resume` continues thread
  `019fc0a2-be54-7671-9f35-0951ce70d0d7`; the second turn requests human
  authority and claims no acceptance or effect.
- design reading: supports L2 transport and authority-bound wake mechanics;
  does not support model admission or net benefit.

### P2 — independent xhigh review detects a real blocker

- evidence: `artifact:external-codex-landing-track-20260801/comparison-closeout-pr342-canonical-summon-v4f/comparison-candidate.json`
- digest: `sha256:10e4a1116f829d2a5eddbf02c72d8f987cc3a8e15afd81f6c48fbba892186df0`
- expected observation: writer and reviewer have distinct sessions and threads;
  the xhigh reviewer returns repair; parent-level source inspection reproduces
  the stale owner-slice projection-identity blocker.
- design reading: supports the value of separated review and xhigh as the next
  research candidate on this fixture only.

### N1 — invalid report is filtered despite safe semantic intent

- evidence: `artifact:external-codex-landing-track-20260801/state-l2-reentry-v1/reentries/b5beb318d2408c26af3ba03d35e1be83/state.json`
- digest: `sha256:2caea79a0afbee5d137c47fc7e092235ab23a6a41756558427d2e81a4ad23695`
- expected observation: Luna's intended direction is escalation, but the bare
  numeric source anchor fails runtime admission; wake evaluation selects
  `result.failed/stop`; the parent remains at one turn.
- false-green sentinel: any review that calls this a successful authority wake
  fails the design.

### N2 — max reviewer false readiness outruns green validation

- evidence: the same comparison candidate as P2.
- expected observation: all nine fixed commands pass; the max reviewer returns
  proceed; the source blocker is nevertheless reproducible and the xhigh repair
  decision is safer on this fixture.
- false-green sentinel: green commands and lower aggregate input usage cannot
  erase false-readiness cost.

### C1 — usage reduction collides with total-system burden

- evidence: the same comparison candidate as P2.
- expected observation: predecessor Luna xhigh writer input is 61.5397 percent
  of Sol max and wall time is 57.9989 percent, but finding coverage is
  complementary, the fresh xhigh writer/reviewer pair consumes 5,406,372 input
  tokens, and accepted outcome value plus operator cost are absent.
- required reading: gross savings are supported; net benefit remains
  `indeterminate`.

### C2 — L2 success collides with different-packet attribution

- evidence: L2 closeout plus comparison candidate.
- expected observation: L2 is demonstrated on an ambiguity-stop packet that
  did not run its max arm; it cannot be pooled into the closeout comparison.
- required reading: transport support increases, causal model-fit confidence
  does not.

### R1 — future repaired-target rerun

- required future inputs: exact repaired target HEAD and manifest, frozen task
  packet, Sol baseline, Luna max, Luna xhigh, separated reviewers, parent
  yield/re-entry receipts, target-owner outcome, operator-time record, and
  identical metric semantics.
- regression check: the proposed xhigh route must not increase false closure,
  owner-boundary violations, missing/false wake events, or required rework
  relative to the accepted comparison baseline.
- absence posture: until these inputs exist, the manual report must not emit an
  admission verdict.

## Evidence levels

### Deterministic checks

The first review should run only read-only, low-level checks:

- recompute SHA-256 for every exact evidence file and compare it with the
  packet/design digest;
- validate the candidate packet schema and candidate-only lifecycle;
- verify exact thread equality across parent yield/re-entry and inequality
  across writer/reviewer contexts;
- verify target HEAD, final manifest, and changed-path posture from runtime
  receipts;
- verify every current admission/effect field remains null, false, disabled, or
  candidate-only as contracted.

These checks constrain identity and structure. They cannot decide accepted
outcome value, false-confidence cost, model fit, or net benefit.

### Rubric judgment

One manual reviewer must answer every case above and record:

- observed evidence and digest;
- case result: `supports`, `counterevidence`, `collision`, `missing`, or
  `not_comparable`;
- strongest supported claim;
- strongest forbidden overread;
- unresolved owner/human decision.

No aggregate score is permitted in the first report. Divergent evidence must
remain visible rather than being hidden inside a weighted total.

## Report contract

The future report path is exactly:

`mechanics/audit/parts/candidate-readers/reports/runtime/2026-08-02-external-luna-landing-l2.manual-review.md`

It must contain:

1. packet identity and digest;
2. reviewer identity and review timestamp;
3. repository/source revision and dirty-state boundary;
4. evidence table with exact refs and verified digests;
5. P1, P2, N1, N2, C1, C2, and R1 case readings;
6. separate transport, model-fit, system-fit, and economic dispositions;
7. explicit owner, proof, human-acceptance, and effect limits;
8. skipped checks and freshness limits;
9. one terminal decision from:
   - `retain_unadmitted_shadow_candidate`;
   - `propose_human_review_of_shadow_admission`;
   - `reject_or_suspend_candidate`;
10. the exact next owner route.

`propose_human_review_of_shadow_admission` is allowed only if R1 evidence is
complete, target-owner outcome is accepted or honestly rejected under an
approved contract, total-system attribution is reviewable, and no unresolved
false-readiness or authority blocker remains. The report itself never activates
the route.

## Runner and artifacts

There is no admitted permanent runner in this first design. The manual review
uses exact read-only commands selected by the reviewer from the evidence table.
Any later automation must trace to a manual case above and demonstrate that it
catches at least N1, N2, C1, and C2 before a validator is admitted.

Inputs:

- the exact candidate packet;
- the five digest-pinned evidence artifacts named here and by that packet;
- current target and owner-source revisions;
- the sole human authority's confirmation that the review artifact may be
  created.

Outputs:

- the exact manual-review report path above;
- one packet update adding that owner-relative report path to `evidence_refs`;
- validation output for packet schema and review-context resolution.

Accepted implementation outcomes:

- report and packet validate, and review-context resolves exactly one report;
- or implementation stops with a typed missing/drift/authority result and
  leaves the packet candidate-only.

## Proof limit, rollback, and next route

This design and its future report are local candidate-review evidence. They do
not become a source eval bundle, central verdict, model-fit admission, target
acceptance, routing activation, or permission for repository/external effects.

Rollback is an owner-local revert/removal of the exact design/report reference
and README source-surface line. Runtime evidence and failed/counterevidence
receipts are never deleted with that rollback. Existing unrelated `memo/`
changes remain untouched.

Next route after owner review of this design: separately implement the exact
manual report, add one report ref to the packet, validate it, then rerun
`aoa-evals review-context`. Selection must inspect that exact implemented
surface before any future `apply`; `apply` must not create it.
