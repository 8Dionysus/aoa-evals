# ring-application-discipline-v1

This shared fixture family defines a bounded ring-application orchestration
surface.

The goal is not to test broad reasoning quality.
The goal is to keep five orchestration pressures reviewable on one compact
surface:

- named ring or skill-family request
- explicit applicability-map evidence
- honest apply-now versus defer-skip handling
- visible execution-versus-closeout distinction
- visible harvest check or explicit no-harvest decision

## Required pressures

Any local replacement must preserve all five pressures.

### 1. Named ring request

The case must include a visible ring or skill-family request.

### 2. Applicability map pressure

The case must make it possible to inspect whether the agent produced an explicit
`apply_now`, `defer`, and `skip` map.

### 3. Honest defer-skip pressure

The case must include at least one plausible `defer` or `skip` opportunity.

### 4. Plane split pressure

The case must make execution and closeout distinguishable.

### 5. Harvest pressure

The case must make it inspectable whether a harvest check happened or whether
the agent explicitly recorded that no harvest move was needed.

## Public-safe rule

The family must stay reviewable without private prompts, hidden repo context, or
secret-bearing transcripts.

## Bounded interpretation rule

This family may support:

- bounded ring-application discipline review
- cautious side-by-side reading of orchestration behavior

This family may not support:

- broad planning rankings
- general reasoning quality claims
- owner-layer governance decisions by itself
