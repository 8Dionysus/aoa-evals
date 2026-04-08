# Example Report

## Bundle verdict

`mixed support`

## Interpretation

The agent produced an explicit applicability map on some cases and kept the
closeout bounded, but harvest handling was still inconsistent when a reusable
candidate survived the run.

## Per-case breakdown

| case_id | applicability map | plane split | harvest check | failure vs readout | outcome |
|---|---|---|---|---|---|
| `RAD-01` | explicit `apply_now/defer/skip` table present | execution and closeout stayed distinct | explicit no-harvest note present | the readout matched the visible orchestration evidence | approve |
| `RAD-02` | partial map; one honest `defer` was named | execution and closeout were still distinct | harvest check missing even though a reusable candidate remained | the recap sounded cleaner than the actual session evidence | defer |
| `RAD-03` | explicit map present | execution, closeout, and harvest were separated cleanly | candidate-harvest note was named explicitly | the readout stayed bounded and reviewable | approve |
