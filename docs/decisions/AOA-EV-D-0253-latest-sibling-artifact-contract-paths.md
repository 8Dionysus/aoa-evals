# Latest-Sibling Artifact Contract Paths Follow Current Owner Sources

- Decision ID: AOA-EV-D-0253
- Status: Accepted
- Date: 2026-08-20
- Owner surface: `scripts/validators/artifact_hooks.py` and its source examples

## Index Metadata

- Original date: 2026-08-20
- Surface classes: sibling compatibility, validation contract, source examples
- Mechanic parents: boundary-bridge, audit
- Guard families: source freshness, owner boundary, fail-closed validation
- Posture: active compatibility rationale

## Context

The latest-sibling canary on current `main` reached the strict validator but
failed on historical artifact-contract paths. The referenced sibling owners
have reorganized playbooks, moved the summon skill under `aoa-agents`, renamed
two SDK handoff examples, and placed the KAG regrounding ticket under its
owning mechanic. The old paths were still authored in the local hook matrix
and its source examples, so current sibling checkout drift was reported as
missing evidence.

## Options Considered

- Disable strict sibling path checks or treat missing paths as success.
- Edit the sibling repositories from `aoa-evals`.
- Update the `aoa-evals` source-owned contract refs to the exact current
  sibling paths and retain strict existence checks.

## Decision

Choose the third option. `aoa-evals` now names the current owner paths in
`scripts/validators/artifact_hooks.py` and the corresponding authored example
payloads. The canary remains strict: a missing current sibling source is still
an honest compatibility failure. Generated readers are regenerated from these
source examples and remain non-authoritative.

No sibling repository, deployed runtime, or external acceptance state is
changed by this decision.

## Rationale

The local hook matrix owns the compatibility assertion, while each sibling
owns the meaning and location of its source. Updating only the local refs
preserves the owner boundary and lets a current checkout prove the contract
without laundering a missing path into a green result.

## Consequences

- Positive: current sibling checkouts can satisfy the strict artifact-hook
  contract after the source refs and derived readers converge.
- Tradeoff: a future sibling move requires another owner-local source update;
  strict canary evidence remains sensitive to that drift.
- Follow-up: re-run the scheduled latest-sibling canary after this branch is
  merged and record any remaining sibling-owned gaps separately.

## Current Applicability

As of 2026-08-20:

- Still valid: sibling source meaning and runtime/acceptance authority remain
  outside `aoa-evals`.
- Changed: artifact-hook refs use current playbook, summon, SDK, and KAG paths.
- Superseded by: none.

## Review Log

### 2026-08-20 - Reconcile current sibling paths

- Previous assumption: historical paths in the hook matrix remained current.
- New reality: live sibling `main` trees expose reorganized paths.
- Reason: the latest-sibling canary reported missing refs against current
  default branches.
- Source surfaces updated:
  - `scripts/validators/artifact_hooks.py`
  - five artifact-to-verdict hook examples
- Validation: live GitHub tree inspection, focused runtime-evidence tests,
  source repository validation, and latest-sibling canary rerun after merge.

## Boundaries

This decision does not accept sibling meaning, issue a proof verdict, promote a
candidate, authorize a runtime effect, or make a generated reader authoritative.
Historical reports may retain their original refs as evidence; active source
contracts must use current owner paths.

## Validation

Run `python scripts/validate_repo.py`, the focused runtime-evidence tests,
candidate/generated parity checks, and the latest-sibling canary against fresh
sibling checkouts. A red canary caused by a new sibling move remains an honest
compatibility residual rather than a reason to weaken strict validation.
