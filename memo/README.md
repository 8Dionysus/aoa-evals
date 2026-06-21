# aoa-evals Memo Port

This is the proof-layer local memory port for `aoa-evals`.

Use it for candidates, receipts, exports, and local notes that should be visible
to future agents without making `aoa-evals` the central memory authority.

| Path | Use |
|---|---|
| `PORT.yaml` | proof-layer local memory port contract |
| `INDEX.md` / `index.min.json` | generated local read model over packets |
| `candidates/` | proposed memory claims with source and evidence refs |
| `receipts/` | accept, reject, validate, or forward traces |
| `exports/` | reviewed-intake packets for `aoa-memo` |
| `local/` | proof-layer memory notes that should remain local |

Default write mode: `write_candidate_only`.

Proof claims, verdicts, baselines, scoring, reports, and source proof meaning
stay in their owning eval bundle, mechanic, report, generated reader, or
decision surface. Durable reviewed memory lands in `aoa-memo`.
