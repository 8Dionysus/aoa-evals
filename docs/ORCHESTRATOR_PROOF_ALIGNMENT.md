# Orchestrator Proof Alignment

## Purpose

This note defines how orchestrator-facing quest families align with `aoa-evals` without turning proof surfaces into class identity.

Orchestrator class identity lives in `aoa-agents`.
`aoa-evals` only names the proof anchors, eval hooks, and closure standards that those classes should satisfy.

## Router

The `router` class should be judged on:

- boundary adherence
- honest source-of-truth selection
- clear naming of the next bounded read set

Router proof alignment stays routing-shaped.
It does not become a replacement for playbook or memo meaning.

## Review

The `review` class should be judged on:

- evidence completeness
- honest verification posture
- correct closure, re-entry, or stop choice

Review proof alignment stays closure-shaped.
It does not become an execution planner.

## Bounded execution

The `bounded_execution` class should be judged on:

- bounded-step quality
- scope discipline
- artifact completeness relative to the named route

Bounded execution proof alignment stays smallest-step-shaped.
It does not become a universal performance score.

## Boundary rule

Proof surfaces judge work.
Quests may point at proof surfaces, but they must not redefine orchestrator identity or replace owner meaning from `aoa-agents`, `aoa-playbooks`, or `aoa-memo`.
