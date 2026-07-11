# Eval Forge Operating Path

## Role

This is the short operating path for using OS Abyss Eval Forge in a live
agent session.

It turns eval pressure into one of these outcomes:

- apply an existing central or local surface;
- write or inspect repo-local intake, suite, or report pressure;
- route a candidate packet through Eval Forge;
- create an owner-review worksheet;
- reject or defer noisy evidence;
- stop before proof promotion.

This document is an operating path, not proof doctrine. Central proof doctrine,
verdicts, scoring, baselines, and regression meaning stay with `aoa-evals`
source proof bundles and their validators. Repo-local `evals/` ports own local
intake, suites, reports, and pressure evidence.

## Authority Boundary

Treat these as routing or access evidence only:

- `.aoa` raw sessions, segment indexes, and search/read-model output;
- `aoa-evals-mcp` packets, receipts, and selected roots;
- generated dashboards, readiness packets, support registries, and candidate
  queue summaries;
- runtime exports and candidate packets;
- repo-local `evals/` intake, suites, and reports before owner review.

None of them can accept proof, score evals, mint baselines, publish verdicts, or
promote a central bundle by themselves.

## Ten Minute Start

From `/srv/AbyssOS/aoa-evals`, run:

```bash
python scripts/aoa_eval_session_start.py --json
python scripts/check_eval_forge_readiness.py --json
python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json
python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets
```

Then read the result in this order:

1. Name freshness blockers first. If `.aoa` live catchup or dirty repos are
   reported, keep them visible and do not turn stale evidence into proof.
2. Check the candidate queue and packet count. Candidate packets are only
   admission evidence for review.
3. Check active repo-local ports. A suite note alone routes to design/review.
   Only a source-contract-`ready` suite execution sidecar can route to local
   apply/regression checks; the owner route JIT-revalidates and captures
   environment plus an execution receipt. `invalid` and `stale` route to repair. Active
   intake pressure routes to select/design review before central adoption.
4. Check the support registry. Apply directly only when the surface is
   classified as safe. Treat candidate-only, component-only, generated, or
   forbidden entries according to their route.
5. Check existing central eval surfaces before designing anything new.

## Forge Route Commands

For a session-mining candidate packet:

```bash
python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py \
  --candidate-packet mechanics/audit/parts/candidate-readers/packets/session-mining/<packet>.eval_candidate.json \
  --json
```

For a repo-local port pressure item after building the inventory:

```bash
python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py \
  --local-port-repo <repo-id> \
  --local-port-inventory /tmp/aoa_local_eval_ports.current.json \
  --workspace-root /srv/AbyssOS \
  --json
```

Write a worksheet only when owner review needs a concrete schema-valid artifact:

```bash
python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py \
  --candidate-packet <packet-path> \
  --write-worksheet <path>.eval_design_worksheet.example.json \
  --json
```

The worksheet is still non-proof. It must carry `proof_authority: false` and
`promotion_allowed: false`.

## Route Choice

Use the smallest route that can honestly handle the pressure:

| Pressure | Route |
| --- | --- |
| Existing central eval may fit | inspect `EVAL_INDEX.md`, `EVAL_SELECTION.md`, generated catalog, then source bundle |
| Existing local suite has a source-contract-ready sidecar | route typed `python_pytest` argv to the repo owner or `aoa-eval-apply`; Forge does not execute it; owner/apply JIT-revalidates and captures environment plus receipt |
| Only `.suite.md` exists | local design/review; do not call it runnable |
| Suite sidecar is invalid or stale | repair schema/path/hash state before owner-local apply |
| Active local intake exists | `aoa-eval-select`, then local design or apply after duplicate-fit review |
| Missed skill trigger or prompt-routing failure | `aoa-skills-trigger-eval` and `aoa-skills` owner review |
| Agent route/path failure across tools or steps | `trace-trajectory-eval` with `.aoa` refs candidate-only |
| Runtime, MCP, or mirror freshness behavior | runtime/MCP smoke under the runtime owner, not central proof |
| Criteria are missing before mining | `human-review-rubric` before automation |
| Keyword-only, emotion-only, transition-only, ownerless, or duplicate pressure | reject or defer; do not packetize as a new eval |

## External Pattern Grounding

Current external grounding is used as design input only:

- Anthropic agent eval guidance supports task/trial/grader/outcome thinking and
  warns that multi-turn tool-using agents can compound mistakes.
- Inspect AI keeps the runnable-eval shape close to dataset, solver or agent,
  scorer, tools, and logs.
- LangSmith and LangChain AgentEvals separate trajectory/tool-call evaluation
  from final-response evaluation and support strict or flexible trajectory
  comparison.
- Google ADK separates trajectory/tool-use evaluation from final-response
  evaluation.
- Langfuse emphasizes manual trace inspection before scaling to online or
  offline automated evaluation.
- OpenAI's hosted Evals platform is deprecated in 2026, so OS Abyss must not
  couple durable Eval Forge workflow to that product.

These sources inform archetype design. They do not own OS Abyss proof authority
or repo-local owner routing.

## Closeout Record

For any meaningful Eval Forge pass, record:

- readiness commands run and freshness blockers;
- candidate packet validator result;
- existing central/local/support surfaces checked;
- selected archetype and admission decision;
- owner route and stop-lines;
- worksheet path when written;
- validation commands run;
- remaining gaps separated as owner-review needed, automation later, proof
  promotion later, and rejected/noise.

Record the local suite execution state when suite pressure is involved. The
only states are `absent`, `invalid`, `stale`, and `ready`, aggregated in that
order of blocking priority: `invalid > stale > ready > absent`. Inventory,
Forge, readiness, dashboard, session-start, promotion review, and MCP never
invoke `runner.argv`.
`ready` does not claim interpreter/dependency reproducibility. PORT, Git
common-dir/origin, notes, and sidecar must resolve one canonical owner; a named
worktree basename is not that owner.
Before any archetype selection, Forge normalizes inventory v1 or unknown input:
even an injected `suite_execution.ready` and old runnable route become
`absent` plus sidecar design. Only inventory v2 can expose runnable routing.
