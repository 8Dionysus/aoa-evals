# Shared Runners

This directory stores top-level runner contracts for portable proof execution.

Runner surfaces here are not hidden harness logic.
They document the minimum execution assumptions needed for:
- bounded inputs
- shared fixture replacement
- scorer helper use
- report schema validation
- additional shared dossier linkage when one bundle participates in more than one paired proof flow

Bundle-local `runners/contract.json` files point back to these top-level runner surfaces.

When a bundle participates in more than one shared readout:
- keep the main dossier in `paired_readout_path`
- list the additional dossiers in `additional_paired_readout_paths`
- keep all dossier paths weaker than the bundle-local `EVAL.md` boundary
