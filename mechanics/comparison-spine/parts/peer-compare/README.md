# Comparison Spine / Peer Compare Part

## Role

This part owns the artifact/process peer-compare fixture families and readout
dossiers.

## Source Surfaces

- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md`

## Inputs

- bundle-local `baseline_mode` value `peer-compare`;
- `comparison_surface` fields such as `peer_surfaces`, `matched_surface`,
  `shared_family_path`, `additional_shared_family_paths`, `paired_readout_path`,
  and `additional_paired_readout_paths`;
- paired artifact/process fixture-family contracts;
- side-by-side readout evidence with matched conditions and interpretation
  limits;
- generated comparison-spine entries derived from source bundles.

## Outputs

- peer-compare fixture-family routes for bounded artifact/process readings;
- paired proof-flow dossiers for v1 and v2 comparison surfaces;
- guidance that keeps both sides comparable without making either side default
  truth;
- validation failures when peer comparison lacks matched conditions,
  side-by-side limits, fixture families, or paired readout refs.

## Stronger Owner Split

Source proof bundles own the peer-compare claim, compared surfaces, matched
conditions, verdict posture, and blind spots.

This part owns shared paired fixture/readout support. Winner, bridge promotion,
default truth source, and baseline pressure route through bundle-local review.

## Boundary

Peer-compare fixtures and dossiers support side-by-side bounded reading. They
keep both sides inside matched-condition evidence until a source owner accepts a
stronger read.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| peer comparison into fixed-baseline by association | source bundle `baseline_mode` and fixed-baseline part route |
| one side as default truth source | bundle-local review plus source owner acceptance |
| draft bridge promotion from paired readout polish | release/report owner route with bundle-local review |
| matched-condition limits or artifact/process separation drift | peer-compare support note and paired report route |
| peer-compare blur as broad capability growth or repo-global score | bounded comparison read plus growth/progression owner review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
