# Split-Model Boundary

The intended split is:

- `aoa-stats` exposes derived surface profiles and source-coverage thinness
- `aoa-sdk` applies the consumer-side re-grounding policy
- `aoa-routing` may publish advisory next-read hints
- `aoa-evals` checks the boundary without taking over owner truth
- owner repos remain stronger than every derived signal

The eval should fail any report that turns stats coverage into proof, routing
advice into route authority, or SDK policy into an eval verdict.
