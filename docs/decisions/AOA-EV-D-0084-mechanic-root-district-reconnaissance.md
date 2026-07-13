# Mechanic Root-district Reconnaissance

- Decision ID: AOA-EV-D-0084
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/EVIDENCE_CLUSTERS.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: root/topology
- Mechanic parents: cross-parent
- Guard families: none
- Posture: active rationale; source tree routed by 0104

## Context

The mechanics refactor depends on more than parent-name correctness. The root
districts of `aoa-evals` already contain the evidence that shows which
mechanics exist: `docs`, `evals`, `fixtures`, `schemas`, `examples`,
`scripts`, `tests`, `config`, `manifests`, `generated`, `reports`, `quests`,
and `mechanics`. The later root route-card guard also made `runners`,
`scorers`, and `templates` explicit compatibility districts, so this
reconnaissance ledger must include them as first-class proof-infra root
districts instead of leaving them implicit.

The original reconnaissance pressure still used the old `bundles/` source
district name. Decision 0104 supersedes that placement language for current
work: source eval packages route through `evals/<claim-family>/<eval-name>/`.

Without an explicit reconnaissance pass, future agents can repeat the original
failure mode: creating a parent from an artifact form, moving one file because
its name looks related, or treating a former root payload path as active
topology after the payload has moved behind a mechanic-owned payload route.

## Options Considered

- Keep root-district knowledge only in `docs/architecture/PROOF_TOPOLOGY.md`.
- Rely on route-card-only guards for cleaned root districts.
- Add a Root District Reconnaissance Ledger to the mechanics evidence map and
  validate the required root-district rows.

## Decision

`mechanics/EVIDENCE_CLUSTERS.md` owns a Root District Reconnaissance Ledger.

The ledger must include one row for each required root district from the
mechanics refactor goal: `docs`, `evals`, `fixtures`, `schemas`, `examples`,
`scripts`, `tests`, `config`, `manifests`, `generated`, `reports`, `quests`,
and `mechanics`; it also includes the current route-card-only proof-infra
districts `runners`, `scorers`, and `templates`.

Each row names the district's authority class, current root posture, mechanics
relationship, and validation guard. Route-card-only districts must explicitly
keep `route-card-only` posture, and mechanic-owned payload placement must route
through the owning active part instead of old root payload paths.

## Rationale

This keeps mechanics discovery evidence-first. The root districts are not just
storage folders; together they show the living proof operation: source bundles,
guidance, contracts, examples, fixtures, builders, validators, generated
readers, reports, quest pressure, and the active mechanics atlas.

The reconnaissance ledger makes that relationship visible before another file
movement or parent package growth occurs.

## Consequences

- Positive: the mechanics map now proves that the goal-listed root districts
  and current proof-infra route-card districts were inspected as a connected
  topology.
- Positive: route-card-only districts remain visible as compatibility roots
  inside the mechanics evidence map.
- Positive: future parent growth has a local checklist for source, support,
  generated/readout, quest, and validation surfaces.
- Tradeoff: `mechanics/EVIDENCE_CLUSTERS.md` becomes longer, but it replaces
  ambiguous file-placement intuition with reviewable reconnaissance.

## Route Boundaries

The ledger is a read model for root-district posture. Payload movement still
routes through the owning source surface, route card, decision review, and
validator update.

Root docs stay guidance, source bundles stay under `evals/`, generated readers
stay derived, and mechanic-owned payloads stay under the owning active part.
Existing route-card-only guards for `config`, `examples`, `fixtures`,
`manifests`, `reports`, `runners`, `schemas`, `scorers`, `templates`, and the
other cleaned compatibility roots remain enforced by `scripts/validate_repo.py`.

## Current Applicability

As of 2026-05-24:

- Still valid: this decision owns the rationale for the root-district
  reconnaissance ledger in `mechanics/EVIDENCE_CLUSTERS.md`.
- Changed: active source eval package topology routes through
  [0104 Source Eval Tree Topology](AOA-EV-D-0104-source-eval-tree-topology.md) and
  `evals/<claim-family>/<eval-name>/`.
- Superseded by: 0104 only for active source eval tree placement. This decision
  still owns the mechanics root-district evidence ledger rationale.

## Review Log

### 2026-05-24 - Source eval tree route narrowed

- Previous assumption: root-district reconnaissance could carry the old
  `bundles/` source-district pressure inside its active status line.
- New reality: source eval package topology is owned by 0104, and the active
  source package route is `evals/<claim-family>/<eval-name>/`.
- Reason: decision status should stay atomic; dated applicability carries
  current route changes without rewriting the original context or rationale.
- Source surfaces updated:
  `docs/decisions/AOA-EV-D-0084-mechanic-root-district-reconnaissance.md`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md`; the local route for this decision is
[mechanics/AGENTS.md#validation](../../mechanics/AGENTS.md#validation).
