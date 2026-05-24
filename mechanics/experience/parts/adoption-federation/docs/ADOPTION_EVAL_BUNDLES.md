# ADOPTION EVAL BUNDLES

Version: v0.7
Owner surface: `aoa-evals`
Seed family: Experience Adoption Forge

## Purpose

Eval bundles for adoption readiness and safety.

## Core law

- Adoption must be explicit.
- Local owner consent is required.
- Durable behavior change needs evidence, rollback and retention.

## Lifecycle hooks

- request
- readiness
- shadow
- decision
- activation
- retention

## Outputs

- adoption_eval_bundles

## Boundary Routes

| Pressure | Route |
| --- | --- |
| hidden assistant self-adoption | release/version review and owner-local adoption decision |
| adoption without local owner consent | owner consent refs and local owner route before activation |
| Tree-of-Sophia runtime write or runtime adoption | ToS dossier boundary plus runtime owner route |
| KAG forced adoption into source repos | KAG promotion gates and source-repo consent |
| routing layer authorship of meaning | `aoa-routing` for routing behavior; source owner for meaning |
| persistent change | rollback path, retention watch, or explicit quarantine fallback |

## Notes

This document belongs to the v0.7 downstream adoption wave. It assumes the v0.6 federation harvest has already approved a shared pattern, then routes adoption as a second sovereign act: local owner consent, compatibility, shadow proof, rollback path, retention watch, and kind-safe projection are required before activation.
