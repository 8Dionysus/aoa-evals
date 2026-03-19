# Example Report

Bundle: `aoa-bounded-change-quality`
Case family: bounded non-trivial change tasks
Bundle-level verdict: `mixed support`

## Summary

- scope stayed mostly bounded across the reviewed cases
- verification naming was usually honest but one case relied on partial static reasoning
- final reports stayed reviewable, but one summary understated skipped checks

## Key signals

- strongest positive signal: one code-fix case stayed inside the requested surface, ran the relevant test, and reported touched files clearly
- main downgrade signal: one docs or config case stayed bounded, but verification language slightly outran the actual checks performed

## Interpretation note

This summary supports a bounded workflow-discipline claim only.
For a narrower read on verification truthfulness or scope alignment,
pair this bundle with the corresponding diagnostic starter.
