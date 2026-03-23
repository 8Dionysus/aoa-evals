# Shared Fixtures

This directory stores public-safe shared fixture families for `aoa-evals`.

These fixture families are reusable proof artifacts, not hidden benchmark dumps.

A shared fixture family should:
- preserve the bounded claim surface it supports
- explain what another repo must keep when replacing cases locally
- stay reviewable without private context
- remain weaker than the bundle-local `EVAL.md` meaning it serves

Current shared families:
- `bounded-change-paired-v1` for artifact/process pairing on the bounded change corpus
- `frozen-same-task-v1` for frozen same-task regression against one named baseline target
- `repeated-window-bounded-v1` for ordered repeated-window movement on one named workflow surface
