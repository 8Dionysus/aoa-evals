# Eval Result Receipt Guide

## Purpose

This guide defines the bounded machine-readable publication seam for
`aoa-evals`.

An `eval_result_receipt` records that one bounded eval publication happened.
It keeps the publication legible for later derived read models without moving
verdict meaning into telemetry.

## Core rule

An `eval_result_receipt` is a publication sidecar, not a second proof canon.

It is subordinate to:

- the owning bundle `EVAL.md`
- the bundle-local report schema
- the concrete report artifact being published
- the bundle-local interpretation boundary

It does not replace bundle-local verdict meaning.

## Shared receipt surfaces

The shared schema-backed surfaces for this seam are:

- canonical shared envelope:
  `repo:aoa-stats/schemas/stats-event-envelope.schema.json`
- `schemas/stats-event-envelope.schema.json`
- `schemas/eval-result-receipt.schema.json`
- `examples/eval_result_receipt.example.json`
- owner-local append-only log:
  `.aoa/live_receipts/eval-result-receipts.jsonl`

Use the shared `stats-event-envelope` for event facts.
Treat the local `aoa-evals` copy as a mirror of the canonical `aoa-stats`
schema rather than as a competing source of ownership.
Use `eval-result-receipt.schema.json` only for the bounded proof payload that
travels inside that envelope.
Use `scripts/publish_live_receipts.py` to append validated owner-local receipts
to the live JSONL log.

## What the receipt may say

An `eval_result_receipt` may name:

- which eval bundle published the result
- which report artifact carries the bounded readout
- the emitted verdict string
- the bounded claim scope used for this publication
- case count or score when the owning bundle already exposes them
- an explicit interpretation bound

It should stay evidence-linked and point back to the report artifact and bundle
contract instead of duplicating the whole proof surface.

## What the receipt must not do

Do not use this seam to:

- create a repo-global score
- replace bundle-local reports with one receipt payload
- hide blind spots or limitations behind counters
- convert comparative or repeated-window reads into universal rankings
- let derived summaries pretend to own verdict logic

## Correction posture

Receipts should stay append-only.

When a published receipt needs correction, emit a later receipt and link it
through `supersedes`.
Do not silently rewrite old publication facts.

## Boundary to preserve

- `aoa-stats` owns the shared cross-repo receipt envelope and active event-kind
  vocabulary used for downstream derivation
- `aoa-evals` owns verdict meaning, report interpretation, and claim limits
- bundle-local report schemas remain the stronger machine-readable proof
  contract
- shared receipts remain weaker than bundle-local interpretation guidance
- later derived stats or observatory layers may read receipts, but they do not
  become proof authorities
