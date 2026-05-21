# Schemas Route

`schemas/` is a compatibility route card, not an active root schema payload
district.

No active root schema payload should live here. Current schema owners are
mechanic-local:

- bundle frontmatter and manifest schemas live under
  `mechanics/proof-object/parts/bundle-contracts/schemas/`;
- shared fixture, runner, and report-summary schemas live under
  `mechanics/proof-infra/parts/reportable-contracts/schemas/`;
- quest source and dispatch schemas live under `mechanics/questbook/parts/`;
- mechanic-specific schemas live under the owning mechanic part.

Schema edits are proof-contract edits. Do not recreate root schema aliases to
make old paths convenient; route old path lineage through the relevant
mechanic `PROVENANCE.md`. The owning legacy archive explains itself after that
bridge.
