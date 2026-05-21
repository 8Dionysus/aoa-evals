# Schemas Route

`schemas/` is the root compatibility route card for historical schema paths.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root schema path routing |
| entry | open when an old root schema path appears or a proof contract schema needs an owner |
| input | schema payload, manifest/frontmatter contract, quest contract, shared report contract, or old root schema reference |
| output | proof-object schema route, proof-infra schema route, questbook schema route, or owning mechanic part |
| owner | `schemas/AGENTS.md` for route law; owning mechanic part for active schema meaning |
| next route | proof-object eval contracts, proof-infra reportable contracts, questbook parts, or domain mechanic part |
| validation | `schemas/AGENTS.md` and the owning route card |

Active root schema payloads route to mechanic-local owners:

- eval frontmatter and manifest schemas live under
  `mechanics/proof-object/parts/eval-contracts/schemas/`;
- shared fixture, runner, and report-summary schemas live under
  `mechanics/proof-infra/parts/reportable-contracts/schemas/`;
- quest source and dispatch schemas live under `mechanics/questbook/parts/`;
- mechanic-specific schemas live under the owning mechanic part.

Schema edits are proof-contract edits. Historical root schema aliases route
through the relevant mechanic `PROVENANCE.md`; the owning legacy archive
explains itself after that bridge.
