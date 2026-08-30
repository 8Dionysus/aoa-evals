# refactor-torture-v1

## Role

This public-safe fixture family supplies bounded source-change cases for a
provider-neutral code-observation report. It asks whether a report keeps
semantic identity, lineage, freshness, invalidation, provenance, metrics, and
affected-test selection inspectable while a controlled refactor changes the
source graph.

The family is reusable case pressure, not a provider or index implementation.
The bundle that names it owns the claim, verdict, and interpretation.

## Case contract

`cases.json` is the canonical manifest. Each case declares:

- one refactor operation and a stable `case_id`;
- the expected lineage posture and freshness state;
- the expected invalidation scope and required observation planes;
- the metrics that must be present in a report;
- any additional bounded oracle, such as delta/full parity or affected tests.

`oracles/affected-tests.json` is the checked-in affected-test oracle. For
cases that require `affected_tests`, the runner requires the report's selected
paths to equal the oracle's case entry and requires `oracle_ref` to be the
canonical repo-relative `mechanics/proof-infra/parts/fixture-families/fixtures/
refactor-torture-v1/oracles/affected-tests.json#<case_id>` reference. Non-empty
remote, URI-like, or otherwise unbound oracle references are rejected.

The cases intentionally span rename, move, signature, add, delete, import,
multi-file, split, merge, stale-index, delta/full parity, and affected-test
selection pressure. They do not assert a particular parser, index, LSP,
SCIP, KAG, runtime, or proof verdict.

## Public-safety and replacement boundary

Fixtures must use synthetic paths and semantic identifiers only. A local
provider may replace the concrete cases only if it preserves the same twelve
operation families, expected posture fields, and required metric IDs. Private
source, credentials, repository contents, provider-internal identifiers, and
owner acceptance must not be required to interpret the case manifest.

## Stronger owner split

- the capability bundle owns the bounded claim and report interpretation;
- a provider owner owns actual live/indexed observations and source epochs;
- `aoa-kag` owns normalized navigation truth when admitted;
- `abyss-stack` owns live LSP/runtime transport;
- this family owns only reusable synthetic case pressure.
