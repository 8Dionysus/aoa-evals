from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Mapping

SUPPORTS = "supports"
MIXED = "mixed"
FAILS = "fails"
NOT_OBSERVED = "not_observed"
AXES = [
    "registry_robustness",
    "propagation_closure",
    "hook_no_mutation",
    "beacon_boundary",
    "review_decision_closure",
    "downstream_thinness",
    "agon_stop_lines",
    "anti_overclaim_report_posture",
]
OVERCLAIM_TERMS = (
    "proves recurrence is complete",
    "all canonical upgrades are safe",
    "global recurrence maturity",
    "full federation correctness",
    "beacon is a verdict",
    "routing graph authority",
    "stats verdict authority",
    "kag source truth",
)


@dataclass
class AxisResult:
    axis: str
    status: str
    evidence_note: str
    signals: list[str]


def L(x):
    return x if isinstance(x, list) else ([] if x is None else [x])


def G(d, *path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, Mapping) or k not in cur:
            return default
        cur = cur[k]
    return cur


def score_registry_robustness(e):
    s = e.get("manifest_scan")
    if not isinstance(s, Mapping):
        return AxisResult(
            "registry_robustness",
            NOT_OBSERVED,
            "No manifest scan evidence was present.",
            [],
        )
    if L(s.get("fatal_errors")):
        return AxisResult(
            "registry_robustness",
            FAILS,
            "Manifest scan reported fatal loader errors.",
            ["fatal_errors"],
        )
    sig = []
    if L(s.get("accepted")):
        sig.append("accepted_components")
    if L(s.get("adapter_required")):
        sig.append("adapter_required")
    if L(s.get("quarantined")):
        sig.append("quarantine_visible")
    return AxisResult(
        "registry_robustness",
        SUPPORTS if sig else MIXED,
        "Manifest shapes were accepted, adapted, or quarantined without fatal collapse."
        if sig
        else "Manifest scan existed, but no bounded diagnostic evidence was visible.",
        sig,
    )


def score_propagation_closure(e):
    c = e.get("graph_closure")
    if not isinstance(c, Mapping):
        return AxisResult(
            "propagation_closure",
            NOT_OBSERVED,
            "No graph closure evidence was present.",
            [],
        )
    edges = L(c.get("edges"))
    batches = L(c.get("propagation_batches"))
    cycles = L(c.get("cycles"))
    if any(isinstance(x, Mapping) and x.get("handled") is False for x in cycles):
        return AxisResult(
            "propagation_closure",
            FAILS,
            "Graph closure exposed an unhandled cycle.",
            ["unhandled_cycle"],
        )
    ok_edges = bool(edges) and all(
        isinstance(x, Mapping) and x.get("kind") and x.get("strength") for x in edges
    )
    ok_batches = bool(batches) and all(
        isinstance(x, Mapping) and "batch_order" in x for x in batches
    )
    sig = []
    if ok_edges:
        sig.append("typed_edges")
    if ok_batches:
        sig.append("batch_order")
    if cycles:
        sig.append("cycle_reported")
    if c.get("max_depth") is not None:
        sig.append("depth_bounded")
    return AxisResult(
        "propagation_closure",
        SUPPORTS if ok_edges and ok_batches else MIXED,
        "Graph closure was typed, ordered, and diagnostic."
        if ok_edges and ok_batches
        else "Graph closure existed, but ordering or typed edge evidence was incomplete.",
        sig,
    )


def score_hook_no_mutation(e):
    h = e.get("hook_run")
    if not isinstance(h, Mapping):
        return AxisResult(
            "hook_no_mutation", NOT_OBSERVED, "No hook run evidence was present.", []
        )
    if L(h.get("forbidden_writes")) or L(h.get("mutated_owner_surfaces")):
        return AxisResult(
            "hook_no_mutation",
            FAILS,
            "Hook run wrote forbidden or owner-canonical surfaces.",
            ["forbidden_write"],
        )
    written = L(h.get("written_paths"))
    ok = h.get("emitted_observation_count", 0) > 0 and all(
        ".aoa/recurrence" in str(p) for p in written
    )
    return AxisResult(
        "hook_no_mutation",
        SUPPORTS if ok else MIXED,
        "Hook run emitted recurrence observations/reports only."
        if ok
        else "Hook run did not show forbidden writes, but observation-only evidence was incomplete.",
        ["observations_only"] if ok else [],
    )


def score_beacon_boundary(e):
    b = e.get("beacons")
    if not isinstance(b, Mapping):
        return AxisResult(
            "beacon_boundary", NOT_OBSERVED, "No beacon evidence was present.", []
        )
    items = L(b.get("items"))
    allowed = {"hint", "watch", "candidate", "review_ready"}
    bad = [
        i
        for i in items
        if isinstance(i, Mapping)
        and (i.get("auto_promoted") or i.get("status") not in allowed)
    ]
    if bad or L(b.get("forbidden_statuses_present")):
        return AxisResult(
            "beacon_boundary",
            FAILS,
            "Beacon evidence included auto-promotion or verdict-like status.",
            ["auto_promotion_or_forbidden_status"],
        )
    return AxisResult(
        "beacon_boundary",
        SUPPORTS if items else MIXED,
        "Beacons stayed in hint/watch/candidate/review_ready posture."
        if items
        else "Beacon surface existed, but no item-level signal was visible.",
        ["no_auto_promotion"] if items else [],
    )


def score_review_decision_closure(e):
    d = e.get("review_decisions")
    if not isinstance(d, Mapping):
        return AxisResult(
            "review_decision_closure",
            NOT_OBSERVED,
            "No review decision evidence was present.",
            [],
        )
    if L(d.get("sdk_minted_owner_refs")):
        return AxisResult(
            "review_decision_closure",
            FAILS,
            "SDK-minted owner refs were present.",
            ["sdk_minted_owner_ref"],
        )
    ok = bool(d.get("owner_authored") and L(d.get("decisions")))
    return AxisResult(
        "review_decision_closure",
        SUPPORTS if ok else MIXED,
        "Owner-authored decision packet closed review evidence without SDK-minted owner objects."
        if ok
        else "Decision evidence was present, but owner-authored closure was incomplete.",
        ["owner_authored_decision"] if ok else [],
    )


def score_downstream_thinness(e):
    p = e.get("downstream_projection")
    if not isinstance(p, Mapping):
        return AxisResult(
            "downstream_thinness",
            NOT_OBSERVED,
            "No downstream projection evidence was present.",
            [],
        )
    bad = (
        L(G(p, "guard_report", "authority_transfer_violations", default=[]))
        or G(p, "routing", "contains_full_graph", default=False)
        or G(p, "stats", "contains_verdicts", default=False)
        or G(p, "kag", "claims_authored_truth", default=False)
    )
    if bad:
        return AxisResult(
            "downstream_thinness",
            FAILS,
            "Downstream projection transferred or implied authority beyond thin hints/summaries/regrounding.",
            ["authority_transfer"],
        )
    claims = [
        G(p, "routing", "authority_claim"),
        G(p, "stats", "authority_claim"),
        G(p, "kag", "authority_claim"),
    ]
    return AxisResult(
        "downstream_thinness",
        SUPPORTS if any(claims) else MIXED,
        "Downstream projections stayed advisory, derived, or regrounding-only."
        if any(claims)
        else "Projection evidence existed, but authority posture was not explicit.",
        ["thin_projection"] if any(claims) else [],
    )


def score_agon_stop_lines(e):
    g = e.get("agon_guard")
    if not isinstance(g, Mapping):
        return AxisResult(
            "agon_stop_lines", NOT_OBSERVED, "No Agon guard evidence was present.", []
        )
    if L(g.get("allowed_forbidden_actions")) or g.get("spawn_pressure"):
        return AxisResult(
            "agon_stop_lines",
            FAILS,
            "Agon evidence allowed forbidden actions or created spawn pressure.",
            ["forbidden_action_allowed"],
        )
    requested = set(map(str, L(g.get("requested_actions"))))
    blocked = set(map(str, L(g.get("blocked_actions"))))
    ok = bool(g.get("observation_only") and requested.issubset(blocked))
    return AxisResult(
        "agon_stop_lines",
        SUPPORTS if ok else MIXED,
        "Agon-shaped recurrence input stayed observation-only and forbidden requests were blocked."
        if ok
        else "Agon guard existed, but stop-line evidence was incomplete.",
        ["forbidden_actions_blocked"] if ok else [],
    )


def score_anti_overclaim_report_posture(e):
    claim = str(e.get("report_claim", "")).lower()
    if not claim:
        return AxisResult(
            "anti_overclaim_report_posture",
            NOT_OBSERVED,
            "No report claim wording was present.",
            [],
        )
    hits = [t for t in OVERCLAIM_TERMS if t in claim]
    if hits:
        return AxisResult(
            "anti_overclaim_report_posture",
            FAILS,
            "Report wording implied a stronger claim than this bundle can support.",
            hits,
        )
    bounded = (
        "bounded",
        "sample",
        "without claiming",
        "does not",
        "remained",
        "only",
        "diagnostic",
    )
    ok = any(t in claim for t in bounded)
    return AxisResult(
        "anti_overclaim_report_posture",
        SUPPORTS if ok else MIXED,
        "Report wording stayed bounded."
        if ok
        else "Report wording was present but did not clearly state limits.",
        ["bounded_claim"] if ok else [],
    )


SCORERS = {name: globals()["score_" + name] for name in AXES}


def evaluate_dossier(dossier: Mapping[str, Any]) -> dict[str, Any]:
    evidence = dossier.get("evidence", dossier)
    if not isinstance(evidence, Mapping):
        evidence = {}
    results = [SCORERS[a](evidence) for a in AXES]
    statuses = [r.status for r in results]
    observed = [s for s in statuses if s != NOT_OBSERVED]
    fails = statuses.count(FAILS)
    mixed = statuses.count(MIXED)
    supports = statuses.count(SUPPORTS)
    if not observed:
        verdict = "insufficient evidence"
    elif fails:
        verdict = "does not support bounded claim" if fails >= 2 else "mixed support"
    elif mixed or supports < 4:
        verdict = "mixed support"
    else:
        verdict = "supports bounded claim"
    limitations = [
        "This eval reads public-safe recurrence artifact summaries, not private raw logs.",
        "A supported result does not prove full federation-wide recurrence completeness.",
        "Beacons, projections, and Agon diagnostics remain weaker than owner-authored decisions.",
    ]
    missing = [r.axis for r in results if r.status == NOT_OBSERVED]
    if missing:
        limitations.append(
            "Missing axes were not counted as passes: " + ", ".join(missing) + "."
        )
    return {
        "eval_name": "aoa-recurrence-control-plane-integrity",
        "bundle_status": "draft",
        "object_under_evaluation": str(
            dossier.get("title") or "recurrence control-plane run dossier"
        ),
        "verdict": verdict,
        "claim_boundary": "This report evaluates bounded recurrence control-plane integrity on the supplied public-safe artifact summary; it does not promote candidates or prove total project maturity.",
        "limitations": limitations,
        "axis_results": [asdict(r) for r in results],
        "case_notes": [
            {
                "case_id": dossier.get("case_id", "unknown"),
                "readout": verdict,
                "observed_axes": [r.axis for r in results if r.status != NOT_OBSERVED],
            }
        ],
        "anti_overclaim_notes": [
            "Do not read this bundle as a global intelligence, safety, or project-completeness score.",
            "Do not treat recurrence beacons as owner decisions.",
        ],
        "followthrough": [
            "Pair with owner-specific evals when the question moves from recurrence boundary integrity to artifact quality.",
            "Add real workspace dossiers once CI emits stable recurrence artifact summaries.",
        ],
    }


def compare_expected(
    report: Mapping[str, Any], expected: Mapping[str, str]
) -> list[str]:
    by = {
        r.get("axis"): r.get("status")
        for r in report.get("axis_results", [])
        if isinstance(r, Mapping)
    }
    return [
        f"{a}: expected {e!r}, got {by.get(a)!r}"
        for a, e in expected.items()
        if by.get(a) != e
    ]
