# Shared Runners

This directory is a compatibility route card for shared runner contracts.

The active shared reportable proof runner surface now lives at:

`mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`

Runner surfaces are not hidden harness logic. They document the minimum
execution assumptions needed for:
- bounded inputs
- shared fixture replacement
- scorer helper use
- report schema validation
- additional shared dossier linkage when one bundle participates in more than one paired proof flow

Bundle-local `bundles/<bundle>/runners/contract.json` files should point to the active
part-local runner surface through `runner_surface_path`.

When a bundle participates in more than one shared readout:
- keep the main dossier in `paired_readout_path`
- list the additional dossiers in `additional_paired_readout_paths`
- keep all dossier paths weaker than the bundle-local `EVAL.md` boundary

Do not recreate active root runner payloads here. Route old root path lineage
through `mechanics/proof-infra/PROVENANCE.md`; the owning legacy archive
explains itself after that bridge.
