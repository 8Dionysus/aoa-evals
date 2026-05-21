# Peer Compare Part

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

This part owns shared paired fixture/readout support. It does not choose a
winner, promote a bridge, establish a default truth source, or turn comparison
into baseline by association.

## Boundary

Peer-compare fixtures and dossiers support side-by-side bounded reading. They
do not turn one side into the default truth source, and they do not promote a
draft bridge by association.

## Stop-Lines

- Do not turn peer comparison into fixed-baseline by association.
- Do not make one side the default truth source without bundle-local review.
- Do not promote draft bridge surfaces through paired readout polish.
- Do not erase matched-condition limits or artifact/process separation.
- Do not use peer-compare blur as broad capability growth or repo-global score.

## Validation

Payload coverage anchor: `mechanics/comparison-spine/parts/peer-compare/`.

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
