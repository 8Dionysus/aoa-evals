# PROVEN code-intelligence direction completion

Status: `review_required`
Decision: `submit_for_review`
Owner: `aoa-evals`
Goal: `01a02fec-b609-7120-b11c-fa80d34ee86a`

## Result

The reviewed twelve-case PROVEN code-observation refactor-integrity package is
reconciled onto the current `origin/main` source tree. The package includes
the public-safe fixture family, bounded eval source, provider-observation and
provider-execution contracts/runners, generated readers, topology ledgers,
and focused tests.

The continuation adds one source-side repair: complete provider-execution
validation now compares affected-test selections with the checked-in
digest-bound oracle. The new regression test proves that a drifted canonical
oracle is rejected. Bundle meaning remains `capability` / `draft` / `none` /
`summary-with-breakdown`; no independent verdict is issued.

## Validation

- Fixture validation: 12 cases; fixture digest
  `sha256:e756db54160b86aff25851b938f97cb7e02b97ac407a21e92bb3ee09100cc0db`;
  oracle digest
  `sha256:81add1064651e08a97e36824502ab7a14375832c436bc651a61550b21f6fdfe9`.
- Raw report and synthetic scenario validation: 12/12 passed; bounded-contract
  summary; bundle remains draft.
- Provider candidate: 12/12 complete cases, provider
  `python-ast-bootstrap/source-candidate-1.0.0`, machine binding
  `not_admitted`, snapshot currentness `unobserved`.
- Provider observation: Python AST and host Ctags each saw 12/12 synthetic
  cases; both remain `not_admitted`.
- Target validator and all generated/semantic parity checks passed.
- Full owner validator passed for 43 eval bundles.
- Full pytest under `ABYSS_MACHINE_TMP_ROOT=/tmp`: 1,083 passed, 5 skipped,
  1,777 subtests passed. The default sandbox run had one unrelated temporary
  path failure because `/srv/abyss-machine/tmp` is read-only; it is retained as
  an environment residual, not called green.

## Landing and claim boundaries

A local packaging commit was prepared as
`aaf411bd8010f2506b8ef4bf376cd73f7d2de11c` on base
`cb734788b8a6fff9869f63bdf890fc54dbaf6563`. Canonical landing is blocked:
the owner worktree cannot write its shared Git index, SSH is blocked by the
system proxy-config permissions, HTTPS cannot resolve `github.com`, and the
GitHub connector write route requires unavailable approval. Therefore no PR,
Repo Validation result, merge, registry promotion, admission, deployment, or
owner acceptance is claimed.

G42 INDEXED output was not used as accepted input. G59 external artifact
authority was not exercised. Proof verdict: `not_issued`.

## Runtime return ABI

```json
{
  "decision": "submit_for_review",
  "reentry_request": {"condition_id": "validated-return", "proposed_action": "wake_parent"},
  "status": "review_required",
  "transition": {
    "approval_posture": "master_review_required",
    "from_status": "active",
    "owner": "aoa-evals",
    "rollback_reentry_route": "master:01a02fec-b609-7120-b11c-fa80d34ee86a",
    "to_status": "review_required"
  }
}
```

Required fixed validation commands are recorded in the JSON output and must
run last after all source/report mutation.
