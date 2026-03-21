# Comparison Contract

Use this bundle only when the baseline target is explicit:
- baseline target: `RS-v1 frozen bounded workflow reference`
- the baseline run family is frozen
- the candidate is judged on the same bounded task family
- comparison is read as regression detection, not as general capability ranking

Comparative readings should separate:
- material regression against the baseline
- improvement on the same bounded surface
- noisy variation that does not justify a stronger claim
- style-only change that does not move the bounded workflow evidence enough to count as improvement or regression

Public summary discipline:
- keep the baseline target visible in the report
- keep per-case baseline and candidate notes visible before the bundle-level verdict
- treat style-only or presentation-only changes as noisy variation unless the bounded workflow evidence also moved
- do not let a single improved case erase a material regression somewhere else in the frozen set
- do not overread one same-task comparison as proof of broad capability growth or decline
