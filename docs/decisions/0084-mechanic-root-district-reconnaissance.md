# Mechanic Root-district Reconnaissance

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/EVIDENCE_CLUSTERS.md`

## Context

The mechanics refactor depends on more than parent-name correctness. The root
districts of `aoa-evals` already contain the evidence that shows which
mechanics exist: `docs`, `bundles`, `fixtures`, `schemas`, `examples`,
`scripts`, `tests`, `config`, `manifests`, `generated`, `reports`, `quests`,
and `mechanics`. The later root route-card guard also made `runners`,
`scorers`, and `templates` explicit compatibility districts, so this
reconnaissance ledger must include them as first-class proof-infra root
districts instead of leaving them implicit.

Without an explicit reconnaissance pass, future agents can repeat the original
failure mode: creating a parent from an artifact form, moving one file because
its name looks related, or treating a former root payload path as active
topology after the payload has moved behind a mechanic-owned payload route.

## Options Considered

- Keep root-district knowledge only in `docs/PROOF_TOPOLOGY.md`.
- Rely on route-card-only guards for cleaned root districts.
- Add a Root District Reconnaissance Ledger to the mechanics evidence map and
  validate the required root-district rows.

## Decision

`mechanics/EVIDENCE_CLUSTERS.md` owns a Root District Reconnaissance Ledger.

The ledger must include one row for each required root district from the
mechanics refactor goal: `docs`, `bundles`, `fixtures`, `schemas`, `examples`,
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
  and current proof-infra route-card districts were inspected as a topology,
  not as isolated filenames.
- Positive: route-card-only districts cannot silently appear as active payload
  homes inside the mechanics evidence map.
- Positive: future parent growth has a local checklist for source, support,
  generated/readout, quest, and validation surfaces.
- Tradeoff: `mechanics/EVIDENCE_CLUSTERS.md` becomes longer, but it replaces
  ambiguous file-placement intuition with reviewable reconnaissance.

## Boundaries

The ledger does not move payloads by itself. It does not turn root docs into
mechanic-owned docs, does not move source bundles into mechanics, and does not
promote generated readers into proof authority.

It also does not weaken existing route-card-only guards for `config`,
`examples`, `fixtures`, `manifests`, `reports`, `runners`, `schemas`,
`scorers`, `templates`, or the other cleaned compatibility roots guarded by
`scripts/validate_repo.py`.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_root_district_recon
python scripts/validate_repo.py
```
