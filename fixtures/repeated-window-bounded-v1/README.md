# repeated-window-bounded-v1

Shared fixture family for the first materialized repeated-window proof flow.

This family is meant to be reusable across:
- `aoa-longitudinal-growth-snapshot`

## Shared case surface

Each window sequence should remain a bounded workflow read with:
- one named anchor workflow surface that stays constant across the sequence
- ordered named windows with one public report or summary artifact per window
- enough evidence to read directional movement without collapsing into a growth myth
- enough context notes to disclose reviewer, policy, environment, or case drift when it matters materially

## Required movement shapes

The family should preserve all four public repeated-window readings:
- `bounded improvement signal`
- `no clear directional movement`
- `mixed or unstable movement`
- `bounded regression signal`

## Replacement rule

Another repo may replace the concrete window sequence locally, but only if the replacement:
- preserves the same bounded workflow surface across the ordered windows
- keeps the windows named and comparable before the longitudinal read begins
- preserves the possibility of all four public movement readings
- discloses context drift that materially changes comparability
- does not silently turn report polish into a stronger movement claim

## Public safety

This family should stay public-safe:
- no secret-bearing run histories
- no hidden local chronology required to understand the window sequence
- no undeclared case-family drift across windows
- no growth claims that outrun the named bounded workflow surface
