# Local Eval Port Write-Side MCP

- Decision ID: AOA-EV-D-0241
- Status: Accepted
- Date: 2026-06-13
- Owner surface: `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`

## Index Metadata

- Original date: 2026-06-13
- Surface classes: MCP access plane, proof topology, sibling reference, validation guard
- Mechanic parents: proof-object
- Guard families: local eval port, sibling-reference, source/topology, validation
- Posture: active rationale

## Context

Local `evals/` ports now exist across OS Abyss sibling repositories. The
standard in `AOA-EV-D-0240` lets each repo preserve local eval pressure without
moving verdict, scoring, regression, or proof doctrine authority out of
`aoa-evals`.

The existing `aoa_evals` MCP contract exposes central proof readers and
candidate-only runtime evidence routes, but it does not yet expose local ports
as first-class workspace surfaces. Agents still need one route to discover
which repo-local ports exist, read their intake/suite/report pressure, and add
small local pressure files while working inside an owning repo.

## Options Considered

- Keep local ports file-only and require direct shell/file edits.
- Keep `aoa_evals` read-only and add only federation resources.
- Allow `aoa_evals` to perform narrow gated writes into sibling repo-local
  `evals/` ports.
- Allow `aoa_evals` to create central `aoa-evals` source bundles directly.

## Decision

Choose narrow gated local-port writes.

`aoa_evals` may list and inspect sibling repo-local eval ports. It may also
write only local pressure files under the selected sibling repo's `evals/`
port:

- `evals/intake/*.eval_need.json`;
- `evals/suites/*.suite.md`;
- `evals/reports/*.report.md`;
- `evals/PORT.yaml` status movement from `skeleton` to `active` when the same
  write adds the first valid local pressure file.

The runnable implementation remains in `abyss-stack`, but `aoa-evals` owns the
contract, validator semantics, and proof-authority boundary.

## Rationale

This route lets agents capture proof pressure where it is born without turning
MCP into the proof owner. Local port writes are authoring support. They preserve
cases, fixture pressure, suite notes, and local report shells for later review.

Central source bundle creation still requires the `aoa-evals` eval-authoring
route. Verdicts, scoring, regression truth, receipt publication, and proof
doctrine remain outside MCP writes.

## Consequences

- Positive: OS Abyss gets one stable MCP path for local eval-port discovery and
  authoring support.
- Positive: repo-local pressure can be captured without leaving the owning
  repository.
- Tradeoff: the MCP implementation now has a write surface and must reject path
  traversal, unknown repos, invalid schemas, silent overwrites, and central
  source bundle writes.
- Follow-up: `abyss-stack` must implement package-local tests and validation
  for the local-port write tools.

## Current Applicability

As of 2026-06-13:

- Still valid: `AOA-EV-D-0240` keeps central proof authority in `aoa-evals`.
- Changed: `aoa_evals` may perform narrow gated sibling-local port writes.
- Superseded by: none.

## Boundaries

Future agents must not infer that write-side MCP may create central
`aoa-evals/evals/**` source bundles, approve proposals, accept evidence,
compute verdicts, define scoring, mark regression truth, publish receipts, or
promote local bundles.

Future agents must not infer that a local suite or report note is central proof
because MCP wrote it.

Future agents must not infer that `abyss-stack` owns local eval-port meaning
because it owns the runnable MCP package.

## Validation

This decision is valid when:

- `docs/architecture/AOA_EVALS_MCP_CONTRACT.md` names local-port federation and
  write stop-lines;
- `docs/guides/LOCAL_EVAL_PORT_STANDARD.md` defines local suite/report note
  shape;
- `scripts/validate_local_eval_port.py` validates suite/report notes and
  active/skeleton status;
- generated decision indexes include this note;
- the stack-owned `aoa-evals-mcp` package validates its local-port tools.
