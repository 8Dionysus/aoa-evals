# Audit / Part Index

## Part Topology

`audit` is one mechanic because all of its parts serve one operation:

`runtime or trace artifact -> selected evidence packet or hook -> generated candidate reader -> bundle-local review`

The parts are not independent mechanics. They are suboperations inside the same
candidate-evidence intake and proof-boundary review loop.

## Parts

### `selected-evidence-packets`

Owns the curation step that turns runtime-owner artifacts into public-safe,
bounded evidence packets.

It answers:

- which runtime artifacts may travel upward;
- which source owner and schema still own the evidence;
- what the packet may support;
- what the packet must not overread.

It does not accept the evidence as proof canon.

### `artifact-verdict-hooks`

Owns the bridge schema, generic bridge metadata, and candidate-reader intake
for playbook or trace artifacts that meet an eval anchor and expected review
shape.

It answers:

- which artifact inputs a route emits;
- which eval bundle can read them;
- which contract refs and report shape constrain the reading.

It does not become a runtime judge and does not move verdict logic out of
`aoa-evals`. Mechanic-specific hook examples may live under the mechanic part
that owns the proof route.

### `candidate-readers`

Owns generated navigation surfaces derived from selected evidence packets and
artifact hooks.

It answers:

- which candidate templates exist;
- which examples they came from;
- which review guide and owner-review refs future review must inspect.

It is weaker than source examples and must be regenerated, not hand-authored as
truth.

### `integrity-review`

Owns the owner-local W10-shaped review contract for runtime continuity evidence
that is meaningful enough to inspect but still weaker than proof canon and
activation authority.

It answers:

- which evidence refs are allowed into this review;
- what replay requirements remain mandatory;
- which authority jumps are forbidden.

It does not activate runtime continuity, write canon, or seal a verdict.

## Part Contract

Inputs are selected runtime, trace, machine, or artifact refs that have been
made public-safe enough to inspect.

Outputs are selected evidence packets, artifact-to-verdict hook payloads,
generated candidate readers, and bounded integrity-review artifacts.

Owner split stays explicit: runtime and sibling repositories keep stronger
truth; `aoa-evals` owns only the candidate-evidence route and the proof review
boundary.

Stop-lines keep every part candidate-only. No audit part accepts a verdict,
activates runtime state, rewrites sibling truth, or bypasses bundle-local
review.

Validation routes through [AGENTS](AGENTS.md#validation), candidate-reader
builders, schema checks, and example tests.

## Stop Lines

- Raw runtime logs stay out unless selected into public-safe packet shape.
- `abyss-stack` remains runtime authority.
- `aoa-playbooks`, `aoa-agents`, `aoa-memo`, and `aoa-stats` keep their owner
  truth.
- Bundle-local review is the first place candidate evidence can become accepted
  proof support.
