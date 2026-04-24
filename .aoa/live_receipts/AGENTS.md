# AGENTS.md

## Guidance for `.aoa/live_receipts/`

`.aoa/live_receipts/` holds owner-local live receipt publication surfaces for eval-side follow-through.

Receipts are evidence-adjacent records, not new verdict authority. They may show that an eval-related event happened, but bundle-local `EVAL.md`, `eval.yaml`, schemas, and reports still own interpretation.

Keep receipts append-safe, public-safe, and explicit about source refs, timestamps, object under evaluation, and bounded result posture.

Do not store secrets, private telemetry, hidden benchmark payloads, unreduced operator data, or local credentials.

If receipt shape changes, update the owning schema, examples, docs, and validator together.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
