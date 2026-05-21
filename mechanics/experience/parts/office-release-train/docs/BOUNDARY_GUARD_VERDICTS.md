# Boundary Guard Verdicts

Version: 1.0.0

## Purpose

Defines verdicts for ToS, source ownership, assistant self-rewrite, and kind safety guards.

This document belongs to the v1.0 installation and first sovereign release wave. It turns the experience program from forged seed into installable order: landing, migration, smoke testing, operator review, first live assistant office, governed release, rollback drill, replay audit, and post-release watch.

## Owns

- boundary verdict
- ownership proof
- kind safety

## Must not do

- source theft
- ToS direct write
- assistant self-certification

## Flow

```text
owner-local artifact
  -> validation
  -> operator review
  -> activation or denial
```

## Authority Source

Release authority and cross-layer doctrine live in [Agents-of-Abyss](https://github.com/8Dionysus/Agents-of-Abyss/blob/main/docs/EXPERIENCE_WAVE5_SOVEREIGN_OFFICE.md). The no-direct-write boundary for Tree-of-Sophia lives in [Tree-of-Sophia](https://github.com/8Dionysus/Tree-of-Sophia/blob/main/docs/NO_DIRECT_EXPERIENCE_INSTALL_WRITE.md). This `aoa-evals` surface only defines owner-local contract behavior and consumes those upstream gates.

## Exit signal

This surface is ready when it can produce a typed artifact, route it to the true owner, survive replay, and fail closed when authority is missing.
