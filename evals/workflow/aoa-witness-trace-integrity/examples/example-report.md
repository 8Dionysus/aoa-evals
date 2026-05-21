# Example Report

## Bundle

- bundle: `aoa-witness-trace-integrity`
- bundle shape: `diagnostic`
- verdict: `mixed support`

## Witness Integrity Breakdown

| run id | step visibility | tool visibility | state delta visibility | failure-path preservation | redaction posture | summary alignment |
|---|---|---|---|---|---|---|
| `WIT-01` | strong | strong | strong | adequate | strong | adequate |

## Bundle-Level Reading

The witness stayed broadly reviewable,
but the markdown summary compressed one failure branch too aggressively.

The main reasons are:
- meaningful steps remained visible in order
- tool use and one external effect were named explicitly
- redaction stayed bounded and did not erase the route
- the summary softened one review flag that the trace still showed

## Interpretation Boundary

This report does **not** prove the run outcome was correct.
It says only that the public witness artifact was reviewable enough for bounded downstream use,
with one visible summary-alignment weakness that should be fixed before stronger reuse.
