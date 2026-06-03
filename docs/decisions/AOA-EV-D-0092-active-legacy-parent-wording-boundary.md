# Active Legacy Parent Wording Boundary

- Decision ID: AOA-EV-D-0092

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: legacy/provenance
- Mechanic parents: none
- Guard families: legacy and provenance, sibling and boundary
- Posture: legacy/provenance rationale

## Context

The mechanics refactor rejects parent names such as `runtime-evidence`,
`proof-release`, `titan-canaries`, `agon-proof`, and `sibling-proof-refs`.
Those strings can still appear as legacy vocabulary, schema filenames, accepted
inputs, or explicit provenance notes, but active route wording must not make
them sound like current package owners.

`runtime-evidence` is the sharp edge: the schema filename
`runtime-evidence-selection.schema.json` remains accepted, and `audit` can name
runtime evidence as an evidence class. Outside that boundary, phrases such as
runtime-evidence bridge or runtime-evidence schema refs make the old parent
form look active again.

## Decision

Active route wording must:

- route runtime evidence through the `audit` parent as evidence class and
  selected-packet vocabulary;
- preserve exact schema filename compatibility where needed;
- avoid using legacy parent form wording as an active owner label;
- keep `runtime-evidence` as not the parent mechanic.

Validator coverage:

```bash
python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording
```

## Consequences

Boundary-bridge, recurrence, release docs, and topology maps use "runtime
evidence" or "runtime candidate evidence" when speaking about live routing.
Exact schema filenames and provenance contexts may still carry the old
hyphenated form when compatibility requires it.
