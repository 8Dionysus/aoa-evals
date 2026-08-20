# External Luna landing L2 manual review

## Review identity

| Field | Value |
| --- | --- |
| packet ID | `runtime:external-luna-landing-l2-20260802` |
| packet path | `mechanics/audit/parts/candidate-readers/packets/external-luna-landing-l2-20260802.eval_candidate.json` |
| linked packet digest | `sha256:6dee214e95fa28171496ebf8e38380a0ba334fc9ac6b1c17f6524138ae2710d2` |
| design path | `mechanics/audit/parts/candidate-readers/reports/runtime/2026-08-02-external-luna-landing-l2.local-eval-design.md` |
| design digest | `sha256:49bf76093be0e2c090771d36378d7ba0914aff02060be430dc2bf669142e2839` |
| reviewer | `codex-root-sol-owner-review-preparation` |
| review method | manual rubric reading of digest-pinned artifacts; no model-authored aggregate score |
| reviewed at | `2026-08-02T05:00:59Z` |
| repository revision | `aoa-evals@1e228c1d5e0c2610b7e667513fbdbe068b49aef4` |
| human acceptance | absent; the user authorized creation of this report but has not accepted its decision |
| proof authority | false |

`manual` means that the cases were interpreted individually rather than by an
automatic scorer. It does not mean that a human authored this report. The sole
human authority must still accept, reject, or narrow the resulting decision.

The repository was already dirty. This review changes only the candidate-reader
README, the named packet, design, and report. Pre-existing `memo/` changes are
outside scope and were neither read as proof nor modified by this review.

## Bounded question

Does the current evidence justify admitting one exact Luna effort and landing
task boundary, after accounting for owner and effect boundaries, accepted
outcome, independent review, filtered parent re-entry, total system burden, and
false-confidence cost?

The nearest existing central bundles were reviewed during `aoa-eval select` and
returned `no_fit` for this combined question:

- `aoa-bounded-change-quality` observes bounded workflow discipline;
- `aoa-regression-same-task` observes frozen same-task regression;
- `aoa-runtime-latency-tradeoff` observes matched runtime metrics and excludes
  agent/model-quality ranking.

This report therefore remains owner-local candidate review. It does not create
or modify a source eval bundle.

## Evidence verification

| Evidence | Verified digest | Review role |
| --- | --- | --- |
| `artifact:external-codex-landing-track-20260801/l2-reentry-closeout-v2.json` | `sha256:8db2434e77dbee04e6088c0a89737761086cf1c54a2a4a75482b15216bb3ce37` | successful L2 cycle plus filtered counterexample |
| `artifact:external-codex-landing-track-20260801/state-l2-reentry-v1/reentries/b5beb318d2408c26af3ba03d35e1be83/state.json` | `sha256:2caea79a0afbee5d137c47fc7e092235ab23a6a41756558427d2e81a4ad23695` | invalid-report filtering and one-turn parent |
| `artifact:external-codex-landing-track-20260801/state-l2-reentry-v2/reentries/96afcd46364eb2ab7ce9e3b7c7e6e299/state.json` | `sha256:98c7205def19912c43e3f753c8ef1ff6f395f6b242cf053c486769ed41e498eb` | exact-thread authority re-entry |
| `artifact:external-codex-landing-track-20260801/comparison-closeout-pr342-canonical-summon-v4f/comparison-candidate.json` | `sha256:10e4a1116f829d2a5eddbf02c72d8f987cc3a8e15afd81f6c48fbba892186df0` | max/xhigh, reviewer disagreement, system and economic limits |
| `artifact:external-codex-landing-track-20260801/completion-audit-20260802.json` | `sha256:576d536cf61fb3c2c5e906d180ca28ee2d775e5c43955dabb1dd8c0ecd6a8646` | goal-wide deliverable and authority gap |

The current historical target remains identified as Git HEAD
`4a7d6212011a3a01c61ffdd6f91f38b8faa9cfea` and manifest
`sha256:8848ac970aab337f7ea11e9446111fdefff1e0ac78c07a588921c8eee1786cfb`.
No current-source repair or target-owner acceptance artifact is present.

## Manual case readings

| Case | Result | Evidence reading | Forbidden overread |
| --- | --- | --- | --- |
| P1 significant authority event | `supports` | Parent Sol completed its yield turn, the process ended, runtime waited 188.399973 seconds without model polling, and the same thread `019fc0a2-be54-7671-9f35-0951ce70d0d7` resumed once after the exact authority event. | L2 transport success is not model fit, accepted outcome, or economic benefit. |
| P2 independent xhigh review | `supports` | Distinct writer/reviewer sessions were preserved; xhigh returned repair and the projection-identity blocker was reproduced independently. | One safer fixture outcome is not a general Luna ranking. |
| N1 invalid report filtering | `counterevidence` | Safe escalation intent carried an invalid source anchor; runtime selected `result.failed/stop`, did not wake Sol, and retained one parent turn. | Semantic intent cannot substitute for admissible evidence or a significant wake. |
| N2 max false readiness | `counterevidence` | Nine fixed validations passed and max returned proceed, yet exact source reproduction confirmed the blocker it missed. | Green validation, fewer commands, or lower aggregate input cannot erase false-readiness cost. |
| C1 gross savings versus burden | `collision` | On the predecessor same-input writer packet, xhigh used 61.5397 percent of Sol input and 57.9989 percent of Sol wall time. The fresh xhigh writer/reviewer pair nevertheless used 5,406,372 input tokens, while outcome value and operator effort remain absent. | Gross savings cannot be labeled net benefit; missing cost terms are not zero. |
| C2 L2 versus comparison attribution | `not_comparable` | L2 is real but uses a separate ambiguity-stop packet whose max arm did not run. | L2 receipts cannot be pooled into the closeout effort comparison. |
| R1 repaired-target rerun | `missing` | No repaired current target, target-owner outcome, same-fixture Sol/max/xhigh rerun, operator-time record, or complete parent/review/rework attribution exists. | Missing R1 evidence forbids a shadow-admission proposal. |

## Separate dispositions

### Transport

Disposition: `supported_bounded`.

The evidence supports external L0-L2 mechanics: separate processes and threads,
durable session state, exact child resume, independent reviewer contexts,
filtered non-wake outcomes, inference-free parent wait, and exact-thread parent
re-entry. This is the strongest positive result.

### Model fit

Disposition: `insufficient_evidence` for admission; `mixed support` for continued
research.

Luna xhigh is the preferred next research/shadow candidate because it has the
lowest predecessor writer usage, one accepted generated-drift repair after
resume, and the only fresh closeout reviewer that detected the confirmed
blocker. The finding is bounded to these fixtures. Trial-order, cache, quota,
same-family reviewer bias, complementary finding coverage, and the unrun L2 max
arm remain confounds.

Luna max remains a research comparison arm. Its lower fresh-pair aggregate
input and command count did not compensate for false readiness.

### System fit

Disposition: `supported_bounded` for substrate mechanics and
`insufficient_evidence` for an accepted production route.

Sol-to-external-Luna, persistence, separated review, candidate A2A return, and
filtered re-entry are demonstrated. The current evidence does not show an
accepted repaired-target outcome or a natural admitted route under ordinary
owner traffic.

### Economics and net benefit

Disposition: `indeterminate`.

Observed token and wall-time reductions are real bounded measurements. They do
not supply realized USD cost under the ChatGPT quota regime. Parent Sol,
operator minutes, review, rework, latency, and false-confidence cost are not
attributed on one accepted fixed-input system comparison. Accepted outcome
value is null. A numerical net-benefit verdict would be fabricated.

### Admission

Disposition: `retain_unadmitted_shadow_candidate`.

Current admitted Luna scope remains `null`. Retain the following exact candidate
for the R1 study only:

- model: `gpt-5.6-luna`;
- effort: `xhigh`;
- task boundary: bounded read-only landing readiness, independent landing
  review, post-landing closeout reconstruction, and isolated generated-surface
  preparation;
- effects: disabled;
- acceptance: target owner plus sole human authority;
- proof posture: candidate-only until a source bundle or accepted local proof
  route reads complete R1 evidence.

This is not `propose_human_review_of_shadow_admission`: the design explicitly
forbids that decision while R1 is missing and false-readiness/attribution
residuals remain unresolved.

## Owner and effect boundaries

- `aoa-models` may record this bounded model-specific candidate lifecycle but
  cannot turn the report into proof or activation.
- `aoa-evals` may interpret the candidate only up to its report/source evidence
  ceiling; this report is not a source bundle or central verdict.
- `aoa-sdk` may carry a future accepted projection but cannot select or launch
  the model from this report.
- `abyss-stack` owns runtime facts and remains source-local/unregistered.
- the target owner owns repair and accepted repository outcome.
- the user remains the sole human authority for admission and every external
  effect.

No commit, push, PR, merge, tag, release, deployment, publication, center
integration, route activation, target repair, or global runtime mutation is
authorized by this review.

## Skipped checks and freshness limits

- no current remote/GitHub, CI, merged-main, release, deployed-runtime, or
  center-registry check;
- no KAG source repair or post-repair R1 rerun;
- no target-owner accepted outcome;
- no Luna max arm on the L2 ambiguity-stop v2 packet;
- no attributable operator minutes or realized USD cost;
- no general model, task-family, cross-host, or long-horizon benefit claim;
- repository-local unrelated `memo/` changes were not interpreted.

The report must be refreshed after any material model, Codex, quota, target,
runtime-controller, fixture, review, or owner-acceptance change.

## Terminal decision and next route

Terminal decision: `retain_unadmitted_shadow_candidate`.

Next route:

1. validate the linked packet and report path;
2. resolve them through `aoa-evals review-context` and preserve the resulting
   bounded proof ceiling;
3. present this exact non-admission decision to the sole human authority;
4. only after a later R1 result, run a fresh owner review before any admission,
   routing, center, or effect proposal.

Rollback removes only this report, its packet reference, and the runtime-report
README source-surface line through owner review. It never deletes runtime
evidence, counterevidence, or unrelated work.
