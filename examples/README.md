# Examples Route

`examples/` is a compatibility route card, not an active root examples payload
district.

No active root examples payload should live here. Examples should stay beside
the source that owns their interpretation:

- bundle-local examples stay under `evals/**/examples/`;
- audit candidate packets and artifact-to-verdict examples live under
  `mechanics/audit/parts/`;
- mechanic-owned examples live under the owning `mechanics/*/parts/*/examples/`;
- receipt examples live under `mechanics/publication-receipts/parts/`.

Examples illustrate a bounded contract. They do not become verdict authority,
bundle meaning, runtime acceptance, or sibling owner truth.
