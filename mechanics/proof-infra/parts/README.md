# Proof Infra Parts

This directory contains active parts owned by `mechanics/proof-infra/`.

Parts here are reusable proof support. They stay weaker than source proof
bundles and weaker than any narrower AoA-aligned mechanic that owns a domain
operation.

Current active parts:

- `fixture-families/` for generic shared fixture-family support that has no
  narrower active mechanic owner.
- `reportable-contracts/` for the shared runner surface, scorer helper, and
  schemas consumed by bundle-local runner/report contracts.
