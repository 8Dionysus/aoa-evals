# Legacy Naming Single-Bridge Language

## Status

Accepted.

## Index Metadata

- Surface classes: legacy/provenance, boundary/runtime/sibling
- Mechanic parents: none
- Guard families: legacy and provenance, sibling and boundary
- Posture: legacy/provenance rationale

## Context

`docs/architecture/LEGACY_NAMING.md` is the map future agents read when an old name appears.
After the mechanics legacy bridge work, this map must not sound as if archive
surfaces are active entrypoints beside `PROVENANCE.md`.

Legacy still needs detailed accounting, but that accounting belongs inside the
owning `legacy/` archive.

## Decision

`docs/architecture/LEGACY_NAMING.md` must describe:

- `PROVENANCE.md` as the single controlled bridge from active mechanic
  surfaces for old placement and source-lineage questions.
- archive details as belonging inside the owning `legacy/` archive.
- active route surfaces as the place where new work begins.

Validator coverage:

```bash
python -m pytest -q tests/test_validate_repo.py -k legacy_naming_single_bridge_language
```

## Consequences

Old names remain visible and searchable, but they cannot steer active topology.
New work starts from the active mechanic route and crosses into legacy only
through `PROVENANCE.md`.
