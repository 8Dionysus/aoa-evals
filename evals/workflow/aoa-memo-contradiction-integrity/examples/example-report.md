# Example Report

## Bundle

- bundle: `aoa-memo-contradiction-integrity`
- bundle shape: `diagnostic`
- verdict: `mixed support`

This example answers the contradiction-visibility question first:
did the memo consumer keep superseded, retracted, and still-open tension
explicit enough for review without smoothing them into one clean active claim?
Its machine-readable companion lives at `reports/example-report.json`.

## Breakdown

- lifecycle visibility: `strong`
- current recall honesty: `mixed`
- contradiction linkage: `strong`
- replacement vs withdrawal clarity: `mixed`
- audit trace visibility: `strong`

## Strongest Signals

- strongest support: the consumer preserved the preferred claim, the withdrawn
  rival, and the audit walkback on the same object-facing read path
- strongest risk: the summary almost treated one unresolved tension as settled
  because the newer claim looked fresher and cleaner than the contradictory
  history

## Case Notes

| case id | contradiction reading | lifecycle note | audit or replacement note | current recall note |
|---|---|---|---|---|
| MCI-01 | mixed support | the preferred claim stayed preferred while the retracted rival remained visibly withdrawn | audit walkback remained reachable, but the replacement and withdrawal story was summarized too smoothly | the reader could still recover the right statuses, though the compact summary leaned toward one clean current story |

## Interpretation Boundary

This read supports only bounded contradiction visibility on the inspected memo
consumer path.
It does not prove contradiction resolution, permission safety, promotion
discipline, or broad memory quality.
