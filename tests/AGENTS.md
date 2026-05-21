# AGENTS.md

## Guidance for `tests/`

`tests/` protects repo-wide eval contracts, catalogs, generated readers,
validators, semantic route cards, and anti-overread posture.

Repo-wide tests live here; mechanic-owned tests live beside the owning part under
`mechanics/<mechanic>/parts/<part>/tests/`. Do not move a part-local test back
to root `tests/` just because pytest can collect it from either place.

## Validator regression role

`tests/test_validate_repo.py` is the root validator regression mesh. It protects
cross-surface contracts in `scripts/validate_repo.py`; it is not generic unit
test overflow.

A test in this root district should name the repository-wide invariant it
protects. If a check only constrains one mechanic part payload, keep or move the
test beside that part instead.

Tests should prove bounded behavior, not freeze incidental prose. Prefer cases around claim limits, fixture coverage, status drift, report validation, and comparison-spine integrity.

Do not update expected outputs without checking the owning bundle, schema, runner, or scorer.

Keep fixtures public-safe. No private benchmarks, hidden telemetry, secrets, or unreduced operator traces.

Verify with:

```bash
python -m pytest -q
python -m pytest -q tests
python scripts/validate_semantic_agents.py
```
