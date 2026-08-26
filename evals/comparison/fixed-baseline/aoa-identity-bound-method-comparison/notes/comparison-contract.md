# Comparison contract

This bundle uses the fixed-baseline comparison part because the comparison has
one declared reference method: `legacy_serial_full_release`. The other method
IDs are peer method shapes inside the same comparison unit, not existing eval
surfaces. A peer-compare manifest would require named peer evals and would
misrepresent those method IDs as independent bundles.

The `anchor_surface` is `aoa-runtime-latency-tradeoff` only because it is the
nearest existing owner route for bounded runtime comparison. It is a routing
neighbor, not a source of evidence, baseline measurement, or winner logic.

The new paired readout documents the identity and parity ABI. It does not
change the existing runtime-latency bundle, create a central score, or turn a
future report into proof or acceptance.

The fixed baseline is a reference route, not a winner. Noisy variation and
style-only change must remain visible and must not be promoted to method
effect, even when a future packet contains clean-looking numbers.
