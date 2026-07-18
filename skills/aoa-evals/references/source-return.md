# Owner source return

Use the bundled read-only resource as the only ordinary source-return path.
Choose the command by task; `<mode>` is not a literal or universal placeholder.

- For `select`, run `catalog`; it returns `owner_source`. Then run `contracts`
  for one or two exact candidates. Do not run `source` separately.
- For `review` of a named candidate packet, resolve the owner, packet, and its
  single packet-declared manual-review report in one call:

  ```text
  python <bundle_dir>/scripts/eval_contract_packet.py review-context \
    --packet-id <exact-packet-id>
  ```

  When the request also supplies an exact owner-relative report path, add
  `--report <exact-owner-relative-report-path>` and require that report instead
  of deriving it from the packet's own refs.

  Read only the returned material paths. Do not run `source` separately, probe
  guessed `EVAL.md` paths, enumerate route cards, or search for the packet.
- For `review` or `evolve` when no catalog packet is needed, resolve the owner
  exactly once:

  ```text
  python <bundle_dir>/scripts/eval_contract_packet.py source
  ```

`<bundle_dir>` is the absolute directory containing the loaded `SKILL.md`.
Do not probe `--help` when one of these declared command shapes applies.
Do not inspect the task workspace or supplied owner-relative paths before the
declared command resolves the owner.

The resource resolves and validates exactly one source route:

- an installed copy uses its same-bundle `.aoa-skill-source.json`;
- the canonical owner home uses its own `skills/port.manifest.json`;
- direct maintenance may pass an explicit absolute `--owner-root`.

Every command verifies owner `aoa-evals`, bundle `skills/aoa-evals`, the owner
manifest, safe paths, and required owner files before returning data. Its
`owner_source` object reports the route, owner root, source path, and available
ref, version, digest, and dirty posture. `source` returns no selection,
evidence acceptance, verdict, or change authority.

`review-context` additionally resolves one exact packet ID and exactly one
manual-review report. Without `--report`, that report must be a safe,
owner-relative `*.manual-review.md` ref declared by the packet itself; zero or
multiple matching refs are terminal and require an exact report path. The
command returns their exact owner-relative paths and direct candidate route
fields, and reports whether the packet itself carries an explicit source-bundle
link. It remains a navigation packet; the returned owner files retain meaning.

If source resolution fails, stop as `blocked_missing_owner_source`. Do not
search parents, siblings, workspaces, `.system`, another skill copy, or a
conventional checkout. Do not retry through another source route.

Treat the source receipt, ref, digest, dirty posture, catalog score, and
neighbor hints as provenance or navigation only. They do not prove installed
parity, semantic fit, eval execution, report validity, maturity, or a verdict.

Report the returned source route and strongest owner files used. Resolve every
owner-relative path beneath the returned owner root.
