# Example Report

## Bundle verdict

`supports bounded claim`

## Interpretation

The lane stayed on contract across all four compact case families.
Observed latency remained bounded and reviewable, but the verdict stayed tied to
contract-fit rather than speed alone.

## Per-case breakdown

| case_id | contract surface | observed shape | latency note | failure vs readout | outcome |
|---|---|---|---|---|---|
| `LTC-01` | exact literal reply | exact literal string with no wrapper text | exact reply remained comfortably below the local timeout budget | the readout stayed honest because no extra chatter was required to explain the pass | approve |
| `LTC-02` | bounded repo routing | one valid target from the named repo set | routing stayed comfortably inside the bounded review window | the readout names route correctness first and latency second | approve |
| `LTC-03` | bounded repo choice | one valid option from the allowed set | latency stayed moderate and did not affect the contract readout | the readout stayed narrow and did not upgrade the case into broad repo understanding | approve |
| `LTC-04` | constrained JSON decision | valid compact JSON with the required keys and bounded values | JSON stayed inside the bounded case window | the readout kept structural validity separate from any richer-answer claim | approve |
