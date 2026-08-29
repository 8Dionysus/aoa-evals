# Eval integrity check

## Bundle boundary

- `EVAL.md` owns the bounded claim, exclusions, and interpretation.
- `eval.yaml` keeps the bundle draft and review-required.
- `fixtures/contract.json` names the shared public-safe family.
- `runners/run_scenarios.py` performs schema and semantic checks.
- `reports/summary.schema.json` constrains the candidate summary shape.

## Integrity questions

1. Does every manifest case appear exactly once in the raw report?
2. Does every observation match its declared operation and required planes?
3. Are lineage, freshness, invalidation, metrics, and provenance explicit?
4. Are ambiguity, delta/full parity, and reproducibility handled by their
   stronger local oracle, and do affected-test selections exactly match the
   checked-in fixture-local oracle reference?
5. Does the summary preserve the draft/review boundary and claim limits?
6. If an actual provider-execution envelope is supplied, does it bind the
   provider state to the reviewed machine contract snapshot (epoch, workspace
   manifest, and raw file digest), source epoch, invalidation universe,
   reproducibility digest, latency/resource measurements, and the fixture case
   IDs without claiming admission or proof? If it declares complete coverage,
   does it execute every fixture case exactly once and provide the required
   deletion, parity, reproducibility, and safe-path evidence?
7. If provider-observation evidence is supplied, does each available provider
   expose all twelve source-manifest cases while retaining `not_admitted` and
   the explicit source-snapshot claim limits?
8. Does the source-bound provider candidate execute every case from the
   provider-execution fixture and let the validator recompute source epochs,
   symbol snapshots, invalidation/deletion semantics, affected tests, stale
   freshness, and full/delta parity instead of accepting declarations alone?
9. When normalized TypeScript envelopes are supplied, do Tree-sitter, SCIP,
   and LSP bind the same repository, path, content digest, and source epoch,
   remain explicitly unadmitted, and expose every required shared fact?

## Review posture

A green local run is only a bounded contract check. It is not a promoted
aoa-evals verdict, a provider admission or acceptance, or a cross-owner
semantic result. Provider-execution validation is a source-bound evidence
check; it does not replace the machine owner admission gate or a normalized
observation/proof route.
