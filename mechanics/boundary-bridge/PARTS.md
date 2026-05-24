# Boundary Bridge / Part Index

`mechanics/boundary-bridge/parts/` contains the active parts of the
sibling-reference compatibility operation.

The mechanic owns the route:

`repo-qualified ref -> sibling owner route -> current/legacy/rejected/unresolved posture -> latest-sibling canary -> bundle-local review`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `compatibility-map` | Maintains the human-readable map for proof refs into sibling owners and the allowed posture vocabulary. | `docs/SIBLING_PROOF_REFS.md` |
| `latest-sibling-canary` | Maintains the current-sibling checkout matrix and runner that validates local compatibility while sibling edits stay in owner routes. | `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`, `mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py` |
| `orchestrator-proof-anchors` | Maintains the local proof-anchor map for orchestrator-facing quest obligations while leaving orchestrator identity in `aoa-agents`. | `docs/ORCHESTRATOR_PROOF_ALIGNMENT.md` |
| `phase-alpha-eval-matrix` | Maintains the bridge from `aoa-playbooks` Phase Alpha run truth to local eval anchors and support refs. | `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/examples/phase_alpha_eval_matrix.example.json`, `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/schemas/phase-alpha-eval-matrix.schema.json`, `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py`, `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json` |

## Boundary

Parts stay as limbs of `boundary-bridge` and route through the mechanic README,
local `AGENTS.md`, and the stronger owner truth of each referenced sibling
repository.

## Part Contract

Inputs are repo-qualified refs, sibling route hints, compatibility posture
entries, orchestrator class refs, quest owner-surface bindings, sibling
Phase Alpha run records, local eval-anchor mappings, and local checkout paths.

Outputs are the authored compatibility map, orchestrator proof-anchor map,
Phase Alpha eval matrix, quest reader projections, and latest-sibling canary
readout.

Owner split stays explicit: sibling repositories own their source truth;
`aoa-evals` owns only local reference compatibility, proof-anchor posture, and
proof-review routing.

Stop-lines route sibling edit pressure, sibling approval pressure,
orchestrator class-identity pressure, and canary proof-acceptance pressure back
to their stronger owners.

Validation routes through [AGENTS](AGENTS.md#validation), including the
latest-sibling canary, Phase Alpha matrix check, and repo validation lanes.
