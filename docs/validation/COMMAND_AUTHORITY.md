# Validation Command Authority

`aoa-evals` uses a lane-owned command model.

- `docs/validation/validation_lanes.json` is the canonical storage surface for
  named lane definitions and command sequences in this repository.
- `scripts/validation_lanes.py` is the loader/API for Python callers.
- `scripts/ci_gate.py` executes named lanes for local and CI callers.
- `scripts/release_check.py` remains the local release entrypoint, but it reads
  the release command sequence from the lane manifest.
- `scripts/validate_repo.py` remains the compatibility CLI and root proof
  validator entrypoint while rules continue moving into `scripts/validators/`
  owner modules.
- `docs/validation/validator_inventory.json` and
  `docs/validation/script_inventory.json` are coverage inventories. They do
  not store blocking command sequences.
- Root and nested `AGENTS.md` cards may name focused validation routes and lane
  ids. Exact local commands live in the nearest on-demand `VALIDATION.md`; agent
  cards are not hidden release command stores.
- Decision records, changelogs, release notes, receipts, and review reports
  preserve outcomes and owner routes, not copied runnable command catalogs.
- The Eval Forge operating path, readiness guide, local-port standard, and
  release procedure may keep the narrow operator routes they own; they do not
  duplicate validation lane sequences.

The manifest lives under `docs/validation/` rather than root `config/` because
`config/` is currently a route-card-only compatibility district in this repo.
Changing that root district is a separate topology decision.

## Lane Entries

Use these active entrypoints:

| Lane | Entry |
| --- | --- |
| `source-fast` | `python scripts/ci_gate.py --mode source-fast` |
| `generated` | `python scripts/ci_gate.py --mode generated` |
| `mechanics/part-local` | `python scripts/ci_gate.py --mode mechanics-part-local` |
| `pinned-sibling` | `python scripts/ci_gate.py --mode pinned-sibling` |
| `latest-sibling` | `python scripts/ci_gate.py --mode latest-sibling` |
| `release` | `python scripts/release_check.py` |
| `nightly` | `python scripts/ci_gate.py --mode nightly` |
| `advisory` | `python scripts/ci_gate.py --mode advisory` |

## Full-suite execution cost

The existing release test step uses two pytest-xdist workers with file-based
scheduling. This preserves the complete collection and reuses module-scoped
fixtures within each file; it does not select fewer tests or add a new runner.
Focused commands remain serial unless their measured workload benefits from
parallel execution. The serial full-suite route remains available in
`tests/VALIDATION.md`.

The choice follows work reduction, not just extra CPU allocation. On the same
local source baseline and shared Python 3.14 host (2026-09-04), the complete
suite reported 1267 passed, 6 skipped and 1780 successful subtests in all three
runs:

| Execution | Process elapsed | User + system CPU |
| --- | ---: | ---: |
| Before source/fixture reuse, serial | 92.53 s | 85.02 s |
| After source/fixture reuse, serial | 49.37 s | 43.89 s |
| After reuse, two file-scheduled workers | 29.94 s | 51.02 s |

These are local observations, not a hosted-CI speed guarantee. Two workers
trade some duplicated imports and concurrent memory for shorter elapsed time;
the removed duplicate validation remains beneficial in serial mode. Revisit
the worker count when the workload or runner changes rather than treating it
as a permanent upper bound. Bundle proof meaning and negative cases are
unchanged.

## Promotion Rule

Advisory and compatibility boundaries become hard gates only when a current
source owner, runtime owner, sibling owner, or decision record proves that
`aoa-evals` owns the checked behavior or the PR explicitly makes a bounded
cross-organ compatibility claim.

Until then, runtime policy, trace grading, memory/RAG authority, inter-agent
execution, observability policy, security enforcement, and sibling path
existence stay as route-visible boundaries. `aoa-evals` can prove bounded eval
artifacts and evidence routes; it does not become the runtime policy engine or
a sibling topology owner by adding a validator.

## Failure Route

When a lane fails:

1. Fix the source owner named by the failing command.
2. Rebuild generated companions only from their source builders.
3. Keep `docs/validation/validation_lanes.json` as the command store if the
   command route itself moved.
4. Update `docs/validation/validator_inventory.json` when validator owner,
   lane, mode, or failure route changes.
5. Update `docs/validation/script_inventory.json` when a script is added,
   moved, removed, or changes owner, lane, side-effect posture, CI inclusion, or
   focused test target.
