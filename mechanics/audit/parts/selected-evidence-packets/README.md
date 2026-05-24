# Audit / Selected Evidence Packets Part

## Role

This part owns the curation contract for runtime-owner artifacts that may travel
into `aoa-evals` as candidate evidence.

It keeps `abyss-stack` runtime truth outside eval ownership while allowing a
public-safe packet to name a bounded claim, source schema, selected artifacts,
environment invariants, and overread-routing notes.

## Source Surfaces

- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- `mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json`
- `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json`

## Inputs

- public-safe runtime or machine artifact refs selected from stronger-owner
  systems;
- source schema refs that still belong to the runtime or sibling owner;
- candidate eval refs that remain below bundle-local review;
- overread-routing notes, environment invariants, and reviewer evidence refs.

## Outputs

- schema-backed `runtime_evidence_selection.*.example.json` packets;
- selected evidence routes for candidate readers;
- owner-review refs that a later bundle-local review must inspect;
- explicit rejection posture for raw, private, or overbroad runtime evidence.

## Stronger Owner Split

`aoa-evals` owns packet shape, candidate-only posture, public-safe selection,
and the proof-review boundary.

`abyss-stack`, machine operators, and sibling repositories keep runtime truth,
artifact provenance, live state, and implementation meaning.

## Boundary

Selected evidence starts as a candidate packet. Bundle-local review decides how
the owning eval may read it, while the runtime or sibling owner keeps source
truth.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| raw logs, secrets, private host fingerprints, or unreduced operator traces appear | keep them with the source owner or curate a public-safe packet first |
| a selected packet is read as runtime health, proof acceptance, or bundle promotion | send the read to runtime-owner review and bundle-local eval review |
| packet wording conflicts with a source bundle, runtime owner, or sibling owner | follow the stronger owner surface before using the packet as evidence |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
