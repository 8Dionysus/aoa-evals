# Source-bound provider execution fixture

`manifest.json` contains public-safe before/after Python trees for the twelve
`refactor-torture-v1` cases. The source-owned executor parses those trees and
recomputes symbol fingerprints, stable lineage candidates, changed/added/deleted
paths, reverse-import invalidation, affected-test selection, stale epochs, and
full/delta projection parity.

The output uses the reviewed provider-execution ABI but is explicitly
`source-bound-provider-candidate` and `admission_state=not_admitted`. It is a
replayable candidate evidence generator, not an installed provider, machine
health receipt, runtime deployment observation, KAG result, proof verdict, or
owner acceptance.
