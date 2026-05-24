# Sibling Proof References

## Role

`mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md` is the compatibility map for proof references that
point from `aoa-evals` into sibling repositories.

This map owns local compatibility posture. Generated catalogs, release notes,
sibling repo contracts, runtime mirrors, and proof bundles keep their own owner
routes while this map names how local proof references stay honest when their
stronger owner lives outside this repository.

## Core Rule

A sibling proof reference is a cited input to bounded proof review.

Authority-transfer pressure routes to the sibling owner.

`aoa-evals` may cite sibling surfaces, validate that current paths still exist,
and preserve compatibility or legacy posture. The sibling repository keeps the
meaning of the referenced object.

## Compatibility Operation

The owned operation is:

`repo-qualified ref -> sibling owner route -> current/legacy/rejected/unresolved posture -> latest-sibling canary -> bundle-local review`

This keeps local proof references inspectable without editing sibling repos to
make `aoa-evals` pass.

## Current Compatibility Map

| Sibling owner | Local proof use | Root variable | Resolver | Stronger owner truth | Current gate |
| --- | --- | --- | --- | --- | --- |
| `aoa-techniques` | technique dependency refs and practice-source refs | `AOA_TECHNIQUES_ROOT` | `direct` | technique meaning and reusable practice contracts | latest-sibling canary plus `validate_repo.py` dependency checks |
| `aoa-skills` | skill dependency refs and workflow-source refs | `AOA_SKILLS_ROOT` | `direct` | skill workflow meaning and portable skill contracts | latest-sibling canary plus `validate_repo.py` dependency checks |
| `aoa-agents` | orchestrator, role-facing, and artifact-contract refs | `AOA_AGENTS_ROOT` | `direct` | role policy, orchestrator posture, and agent artifact contracts | latest-sibling canary |
| `aoa-playbooks` | eval-anchor, phase-alpha, reviewed-run, and scenario refs | `AOA_PLAYBOOKS_ROOT` | `direct` | scenario composition and playbook route truth | latest-sibling canary |
| `aoa-memo` | recall, checkpoint, writeback, memory object, and provenance refs | `AOA_MEMO_ROOT` | `direct` | memory object truth, recall/writeback posture, and memo provenance | latest-sibling canary plus repaired path refs plus pinned `Repo Validation` ref |
| `aoa-routing` | runtime integrity route evidence refs | `AOA_ROUTING_ROOT` | `direct` | route review and dispatch posture | latest-sibling canary |
| `aoa-kag` | runtime chaos regrounding refs | `AOA_KAG_ROOT` | `direct` | derived KAG substrate and regrounding truth | latest-sibling canary |
| `aoa-sdk` | A2A checkpoint bridge and local target refs | `AOA_SDK_ROOT` | `direct` | SDK control-plane assembly and A2A helper contracts | latest-sibling canary |
| `aoa-stats` | stats event envelope mirror refs | `AOA_STATS_ROOT` | `direct` | shared event envelope vocabulary and downstream stats derivation | latest-sibling canary plus receipt-envelope checks |
| `abyss-stack` | runtime evidence schema and selected runtime candidate refs | `ABYSS_STACK_ROOT` | `abyss-stack-source` | runtime source contracts and implementation truth | latest-sibling canary resolves the source checkout, not the deployed mirror |

The canary matrix source is `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`.

The runner source is
`mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py`.
Use `mechanics/boundary-bridge/parts/AGENTS.md#validation` for the executable
canary command.

GitHub `Repo Validation` is the stricter pinned public lane. For `aoa-memo`,
that lane currently checks out `97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f` in
`.github/workflows/repo-validation.yml`; see
`docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md`.

## Posture Vocabulary

Use these terms when a sibling reference changes:

- `current`: the referenced sibling path exists in the current sibling checkout
  and remains appropriate for the local proof claim.
- `legacy`: the reference preserves old source lineage or accepted input, but a
  current path or replacement route should be named nearby.
- `rejected`: the reference is excluded from local proof review.
- `unresolved`: the owner route or current path needs owner-route review before
  the reference can carry proof authority.

## Repair Route

When a sibling proof reference fails:

1. Identify the local source surface that cites the sibling ref.
2. Identify the sibling owner and stronger owner truth.
3. Check whether the sibling path is current, legacy, rejected, or unresolved.
4. Repair the local `aoa-evals` reference or add a local compatibility note.
5. Route sibling edits through explicit sibling-owner work.
6. Use `mechanics/boundary-bridge/parts/AGENTS.md#validation` for local
   validation.
7. Add the latest-sibling canary from that route when current sibling checkout
   truth matters.
8. If GitHub `Repo Validation` fails because a pinned sibling checkout is stale,
   refresh the pin only after comparing it to current sibling truth and record
   the decision.

## Boundary

The latest-sibling canary proves that the current local checkout can resolve the
referenced sibling surfaces under the configured roots.

| Pressure | Route |
| --- | --- |
| sibling acceptance | sibling owner route |
| local proof bundle promotion | bundle-local review |
| old path names read as active topology | current/legacy/rejected/unresolved posture plus current owner route |
| runtime or machine evidence read as verdict meaning | runtime owner plus bundle-local review |
| generated reader read as source authority | authored sibling source and local source surface |

## Validation

Use `mechanics/boundary-bridge/parts/AGENTS.md#validation` for executable
compatibility checks.

Use the full repo battery when sibling references affect generated readers,
runtime candidate surfaces, quest projections, or bundle-local reports.
