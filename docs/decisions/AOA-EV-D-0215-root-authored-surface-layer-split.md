# Root-authored Surface Layer Split

- Decision ID: AOA-EV-D-0215
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused `scripts/validators/root_authored_surface_*` validators

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0185 correctly split mechanics root-district reconnaissance from
residual root-authored surface classification. The residual classification
module then kept growing as a second broad bucket: it carried docs/scripts/tests
allowlists, filesystem drift checks, ledger row checks, and decision-route
checks in one file.

That shape makes every new root-authored validator touch the same historical
module, even when the real failure route is narrower.

## Decision

Remove `scripts/validators/root_authored_surface_classification.py`.

Residual root-authored surface validation now uses focused modules:

- `scripts/validators/root_authored_surface_common.py` owns only shared
  constants and ledger-derived classification parsing.
- `scripts/validators/root_authored_surface_inventory.py` owns docs/scripts/tests
  inventory drift against the ledger-derived residual classification map.
- `scripts/validators/root_authored_surface_ledger.py` owns
  `mechanics/EVIDENCE_CLUSTERS.md` section tokens and row completeness.
- `scripts/validators/root_authored_surface_decision.py` owns decision index,
  proof-topology, and roadmap route-token checks.

`scripts/validators/mechanics.py` keeps the public route operation
`validate_root_authored_surface_classification` by composing the focused
validators, but no standalone aggregate validator file remains.

## Rationale

Inventory drift, ledger wording, and decision-route evidence are different
failure routes. Keeping them in one validator makes the residual classification
layer behave like the old historical gates this refactor is removing.

The residual classification still exists, because this boundary intentionally
protects the remaining root-authored docs/scripts/tests surfaces. The
improvement is that the helper now derives its map from the ledger instead of
owning a second file list.

## Consequences

- Positive: new root-authored files fail through the inventory validator.
- Positive: stale or incomplete evidence-ledger rows fail through the ledger
  validator.
- Positive: decision/proof/roadmap routing fails through the decision validator.
- Positive: the former aggregate file is removed instead of kept as a
  compatibility facade.
- Tradeoff: `mechanics.py` keeps a compatibility composition function so tests
  and route callers do not need to learn three focused validators at once.

## Current Applicability

As of 2026-06-05:

- Still valid: root-authored surface validation remains split across common
  parsing helpers, inventory drift checks, ledger row checks, and decision-route
  checks.
- Changed: `scripts/validators/root_authored_surface_common.py` no longer owns
  a Python file allowlist. It parses the
  `mechanics/EVIDENCE_CLUSTERS.md` residual classification ledger and exposes a
  ledger-derived surface map for the focused validators.
- Superseded by: not superseded; this is a narrowed application of the same
  focused-layer route.

## Review Log

### 2026-06-05 - Ledger-derived classification map

- Previous assumption: the common helper should carry shared constants and the
  expanded file list.
- New reality: the residual ledger is the only active list of classified
  root-authored surfaces; the helper reads that source instead of defining a
  second allowlist.
- Reason: keeping the allowlist in Python preserved historical validator bulk
  and made generated checks depend on code-owned topology data.
- Source surfaces updated:
  `scripts/validators/root_authored_surface_common.py`,
  `scripts/validators/root_authored_surface_inventory.py`,
  `scripts/validators/root_authored_surface_ledger.py`,
  `mechanics/EVIDENCE_CLUSTERS.md`, and
  `docs/decisions/AOA-EV-D-0085-root-authored-surface-classification.md`.
- Validation: root-authored topology tests, decision indexes, source-fast gate,
  and release check.

## Boundaries

This split does not make the root-authored layer own mechanic payload meaning,
parent evidence semantics, part contracts, runtime evidence, generated
projection parity, release packaging, or proof verdict meaning.

Root-district posture remains owned by
`scripts/validators/mechanics_root_districts.py`.

## Validation

- `python -m py_compile scripts/validators/root_authored_surface_common.py scripts/validators/root_authored_surface_inventory.py scripts/validators/root_authored_surface_ledger.py scripts/validators/root_authored_surface_decision.py scripts/validators/mechanics.py`
- `python -m pytest -q tests/test_mechanics_topology.py`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
