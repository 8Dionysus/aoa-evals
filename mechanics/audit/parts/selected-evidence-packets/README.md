# Selected Evidence Packets

## Role

This part owns the curation contract for runtime-owner artifacts that may travel
into `aoa-evals` as candidate evidence.

It keeps `abyss-stack` runtime truth outside eval ownership while allowing a
public-safe packet to name a bounded claim, source schema, selected artifacts,
environment invariants, and do-not-overread notes.

## Source Surfaces

- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- `mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json`
- `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json`

## Inputs

- public-safe runtime or machine artifact refs selected from stronger-owner
  systems;
- source schema refs that still belong to the runtime or sibling owner;
- candidate eval refs that remain below bundle-local review;
- do-not-overread notes, environment invariants, and reviewer evidence refs.

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

Selected evidence is not accepted proof. It becomes useful only after
bundle-local review confirms how the owning eval may read it.

## Stop-Lines

- Do not ingest raw logs, secrets, private host fingerprints, or unreduced
  operator traces.
- Do not treat selected evidence as runtime health, proof acceptance, or bundle
  promotion.
- Do not let a packet override the source bundle, runtime owner, or sibling
  owner.

## Validation

Payload coverage anchor: `mechanics/audit/parts/selected-evidence-packets/`.

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
```
