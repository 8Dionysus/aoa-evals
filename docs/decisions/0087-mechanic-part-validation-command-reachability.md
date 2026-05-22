# Mechanic Part Validation Command Reachability

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Context

Concrete mechanic parts now expose inputs, outputs, owner split, stop-lines,
payload inventory, and `## Validation` sections. That still leaves one
practical failure mode: a part README can name a validation route whose script,
test, or helper path no longer exists after root-district movement.

That would satisfy the text shape while breaking the proof-side operation in
practice. For this repository, validation is part of the mechanic boundary, not
decoration.

There is a second failure mode: a payload-bearing part can list only naked
route-wide commands such as `python scripts/validate_repo.py` and
`python scripts/build_catalog.py --check` without saying which part-local
payload or source bundle the validation is meant to cover. That creates formal
safety without an operational return path.

## Options Considered

- Keep validation commands as unconstrained prose.
- Rely on occasional full release checks to notice stale commands.
- Add a validator-backed reachability check for python command paths in every
  concrete part README.
- Require a payload coverage anchor for any part with local payload
  subdirectories, while allowing bundle-backed thin routes to stay bundle-led.

## Decision

Every concrete `mechanics/<parent>/parts/<part>/README.md` `## Validation`
section must list at least one python command.

When the part has local payload subdirectories, the validation section must
also include a payload coverage anchor: either a command or validation-section
code ref under `mechanics/<parent>/parts/<part>/`, or a specific
`python scripts/validate_repo.py --eval ...` command for a source-bundle route.
Naked route-wide commands are not enough for payload-bearing parts.

`scripts/validate_repo.py` parses python commands from fenced, bullet, or
inline-code validation text and rejects:

- a stale validation path;
- an absolute validation path instead of a repo-relative reachable path;
- an unparsable python command;
- a validation section with no python command.
- a payload-bearing part whose validation section has no payload coverage
  anchor.

The check is intentionally reachability-oriented. It proves that the command
targets named by the part route still exist; it does not execute every part
command on every repository validation pass.

## Rationale

The mechanics refactor moved many scripts, tests, scorers, schemas, reports,
and generated outputs into part-local homes. A stale validation command would
turn that movement into ceremony: the part would look reviewable but would not
give the next worker a usable check.

Reachability plus a payload coverage anchor is the smallest durable guard that
keeps part validation concrete without making every `validate_repo.py` run
execute the entire release battery.

## Consequences

- Positive: part-local validation routes stay usable after future file moves.
- Positive: stale validation paths are caught by the standard repository
  validator.
- Positive: payload-bearing parts cannot hide behind naked route-wide command
  lists; their validation route must point back to part-local payload or a
  specific source bundle.
- Positive: validation commands remain repo-relative and portable.
- Tradeoff: renaming a part-local script, test, or helper must update the part
  README in the same slice.
- Tradeoff: generic root validator commands sometimes need one extra coverage
  anchor line so the operational payload route stays visible.

## Boundaries

This decision does not prove that every validation command was executed in a
given run.

It does not replace part-local tests, generated `--check` commands,
`release_check.py`, or GitHub `Repo Validation`.

It does not allow validation commands to strengthen bundle claims, sibling
truth, runtime authority, or generated reader authority.

## Current Applicability

As of 2026-05-22:

- Still valid: validation command routes must stay reachable, repo-relative,
  and anchored to payload coverage.
- Changed: executable validation commands route through
  [mechanics/AGENTS.md#validation](../../mechanics/AGENTS.md#validation) and
  parent `parts/AGENTS.md` lanes.
- Superseded by: active command ownership in nearest AGENTS route cards.

## Review Log

### 2026-05-22 - Validation command ownership aligned

- Previous assumption: this decision could carry the focused validation-command
  guard list directly.
- New reality: `mechanics/AGENTS.md` owns the focused mechanic part validation-command guard.
- Reason: accepted decisions preserve why; AGENTS route cards carry executable
  validation lanes for agents.
- Source surfaces updated: `mechanics/AGENTS.md`, `scripts/validate_repo.py`,
  and `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k
  mechanic_part_validation_command`; `python scripts/validate_repo.py`.

## Validation

Use [mechanics/AGENTS.md#validation](../../mechanics/AGENTS.md#validation) for
the current command lane.
