# AGENTS.md

## Applies to

This card applies to root `tests/` and repo-wide validator regression tests.

## Role

`tests/` protects repo-wide eval contracts, catalogs, generated readers,
validators, semantic route cards, and anti-overread posture.

Repo-wide tests live here; mechanic-owned tests live beside the owning part
under `mechanics/<mechanic>/parts/<part>/tests/` when the invariant belongs to
that part rather than the repository-wide mesh.

## Operating Card

| Field | Route |
| --- | --- |
| role | root validator regression and repo-wide contract test district |
| input | validator rules, generated reader contracts, source eval invariants, route-card posture, and anti-overread constraints |
| output | regression proof that root-wide contracts still hold |
| owner | root `tests/` for repo-wide invariants; mechanic part for part-local payload invariants |
| next route | protected source surface, `scripts/` validator, generated reader, or owning mechanic part |
| tools | pytest, root validator, semantic AGENTS validator |
| validation | this card's `Verify` section |

## Validator regression role

`tests/test_validate_repo.py` is the root validator regression mesh. It protects
cross-surface contracts in `scripts/validate_repo.py`; it is not generic unit
test overflow.

A test in this root district should name the repository-wide invariant it
protects. If a check only constrains one mechanic part payload, keep or move the
test beside that part instead.

Tests should prove bounded behavior, not freeze incidental prose. Prefer cases
around claim limits, fixture coverage, status drift, report validation, and
comparison-spine integrity.

Expected-output pressure routes first through the owning bundle, schema, runner,
or scorer.

Keep fixtures public-safe and reduced to the checked-in proof contract. Private
benchmarks, hidden telemetry, secrets, and unreduced operator traces route away
from this public regression mesh.

## Owner Routes

| Test pressure | Owner route |
| --- | --- |
| repo-wide validator invariant | root `tests/` with protected source surface named |
| mechanic payload invariant | `mechanics/<mechanic>/parts/<part>/tests/` |
| generated reader parity | builder, generated reader, source input, and regression test together |
| expected-output change | owning bundle, schema, runner, scorer, or route card first |
| new human-readable law | docs, mechanics, or root source surface before test-only enforcement |

## Verify

Run:

```bash
python -m pytest -q
python -m pytest -q tests
python scripts/validate_semantic_agents.py
```
