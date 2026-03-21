# Shared Runners

This directory stores top-level runner contracts for portable proof execution.

Runner surfaces here are not hidden harness logic.
They document the minimum execution assumptions needed for:
- bounded inputs
- shared fixture replacement
- scorer helper use
- report schema validation

Bundle-local `runners/contract.json` files point back to these top-level runner surfaces.
