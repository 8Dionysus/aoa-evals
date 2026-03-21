# Example Report

Bundle: `aoa-bounded-change-quality`
Case family: bounded non-trivial change tasks
Bundle-level verdict: `supports bounded claim`

## Summary

- BCQ-01 stayed inside the requested file surface, ran the relevant validation step, and reported the touched scope plainly.
- BCQ-02 stayed bounded but the summary initially blurred skipped checks, so the readout was downgraded even though the change itself remained reviewable.
- BCQ-03 made a docs-only change, named the limited verification honestly, and avoided turning the task into a broader cleanup.

## Key signals

- approve signal: the workflow stayed scoped, named real verification, and kept the final report aligned with what was actually done.
- failure signal: a case that widens the task or invents verification would fail the bundle claim.
- readout distinction: a mixed case note is a case-level readout, not automatic proof that the whole bundle failed.

## Interpretation note

This summary supports only the bounded change-workflow claim.
It does not prove general engineering quality or any narrower diagnostic question by itself.
For root-cause reads on verification truthfulness or scope drift, use the narrower bundles.
