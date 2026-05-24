# Checkpoint / Part Index

`mechanics/checkpoint/parts/` contains the active parts of the eval-side
checkpoint proof operation.

The mechanic owns the route:

`checkpoint pressure -> bounded checkpoint proof question -> selected support surface -> bundle-local review -> bounded report or owner handoff`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `a2a-summon-return` | Maintains the A2A summon child-return checkpoint fixture and hook route. | `mechanics/checkpoint/parts/a2a-summon-return/README.md` |
| `restartable-inquiry` | Maintains checkpoint-and-relaunch proof routing for long-horizon inquiry restart fidelity. | `mechanics/checkpoint/parts/restartable-inquiry/README.md` |
| `self-agent-posture` | Maintains the self-agent checkpoint eval posture and approval-boundary hook route while checkpoint-canon pressure stays with stronger owners. | `mechanics/checkpoint/parts/self-agent-posture/README.md` |

## Part Contract

Inputs are checkpoint bridge plans, inquiry checkpoints, reviewed child
results, return plans, approval records, rollback markers, health checks,
improvement logs, memo writeback candidates, dry-run runtime receipts, and
owner-source refs.

Outputs are bounded checkpoint proof readings, fixture family contracts,
artifact-to-verdict hook examples for candidate readers, route notes, and owner
handoffs.

Owner split stays explicit: `Agents-of-Abyss` owns checkpoint law; SDK, skills,
agents, memo, playbooks, routing, stats, runtime, and owner repositories keep
their local truth; `aoa-evals` owns bounded proof interpretation.

Stop-lines route stronger-owner pressure through the boundary routes below.

| Pressure | Owner route |
| --- | --- |
| checkpoint implementation authority | Agents-of-Abyss law route plus `aoa-sdk` checkpoint-control route |
| memory canon or recall sovereignty | `aoa-memo` memory route |
| live runtime activation | `abyss-stack` runtime route |
| owner acceptance or promotion | owner repository acceptance route |
| hidden scheduling behavior | `aoa-playbooks` choreography route plus `abyss-stack` runtime route |
| autonomous self-repair | `aoa-agents` role, approval, rollback, and health route |
| final child-output quality grading | owner repository child-output acceptance route |
| broad long-horizon competence | bundle-local proof object plus source-owner evidence review |

Validation routes through [AGENTS](AGENTS.md#validation), including the
part-local test, audit candidate-reader builders, generated catalog check, and
repo validation lanes.

## Deferred Part Families

Candidate-lineage and return-anchor checkpoint pressure remain bundle-local or
adjacent to `recurrence`, `growth-cycle`, `audit`, or `comparison-spine` until
their support artifacts have their own source surfaces, inputs, outputs, owner
split, stop-lines, and validation beyond bundle-local proof-object routing.
