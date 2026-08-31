# Comparison Spine / Peer Compare Part

## Role

This part owns the artifact/process peer-compare fixture families and readout
dossiers, including validation-routing method comparison support.

## Source Surfaces

- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/validation-routing-bounded-v1/README.md`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/validation-routing-bounded-v1/cases.json`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/validation-routing-comparison-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/peer-compare/examples/validation-routing-comparison.example.json`
- `mechanics/comparison-spine/parts/peer-compare/schemas/validation-routing-comparison-v1.contract.json`
- `mechanics/comparison-spine/parts/peer-compare/schemas/validation-routing-comparison-report-v1.schema.json`
- `mechanics/comparison-spine/parts/peer-compare/scripts/run_validation_routing_comparison.py`
- `mechanics/comparison-spine/parts/peer-compare/tests/test_validation_routing_comparison.py`

## Inputs

- bundle-local `baseline_mode` value `peer-compare`;
- `comparison_surface` fields such as `peer_surfaces`, `matched_surface`,
  `shared_family_path`, `additional_shared_family_paths`, `paired_readout_path`,
  and `additional_paired_readout_paths`;
- paired artifact/process fixture-family contracts;
- side-by-side readout evidence with matched conditions and interpretation
  limits;
- validation-routing scenarios whose peer methods share workload,
  candidate_set_id, environment_id, and source_ref identities;
- a full-owner-proof oracle/fallback plus explicit stale, unknown, malformed,
  wrong-identity, and unexplained-miss states;
- generated comparison-spine entries derived from source bundles.

## Outputs

- peer-compare fixture-family routes for bounded artifact/process readings;
- paired proof-flow dossiers for v1 and v2 comparison surfaces;
- a seeded measurement-only validation-routing comparison with misses, excess
  nodes, denominator-qualified precision/recall, synthetic fixture-proxy
  latency, retry amplification, node-bound explanations, and fail-closed
  escalation;
- guidance that keeps both sides comparable without making either side default
  truth;
- validation failures when peer comparison lacks matched conditions,
  side-by-side limits, fixture families, or paired readout refs.

## Stronger Owner Split

Source proof bundles own the peer-compare claim, compared surfaces, matched
conditions, verdict posture, and blind spots. Stronger owner repositories own
validator execution, external receipts, and acceptance. The validation-routing
support surface owns only the comparison contract, seeded runner, and bounded
readout.

This part owns shared paired fixture/readout support. Winner, bridge promotion,
default truth source, and baseline pressure route through bundle-local review.

## Boundary

Peer-compare fixtures and dossiers support side-by-side bounded reading. They
keep both sides inside matched-condition evidence until a source owner accepts a
stronger read. Validation-routing measurements are not a release verdict or a
routing-policy selection, and missing candidate families remain missing rather
than scoring as zero.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| peer comparison into fixed-baseline by association | source bundle `baseline_mode` and fixed-baseline part route |
| one side as default truth source | bundle-local review plus source owner acceptance |
| draft bridge promotion from paired readout polish | release/report owner route with bundle-local review |
| matched-condition limits or artifact/process separation drift | peer-compare support note and paired report route |
| peer-compare blur as broad capability growth or repo-global score | bounded comparison read plus growth/progression owner review |
| validation-routing measurement as a winning routing policy | keep `claim_posture=measurement_only`; route policy to the stronger routing owner after identity-bound evidence |
| local green proxy as complete owner proof | `full_owner_proof` oracle/fallback with stale, unknown, malformed, and wrong-identity state preserved |
| seeded cases or shadow report as real-session proof | public-safe fixture boundary and the external report's own claim limit |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable commands are owned by this part-local VALIDATION.md route.
