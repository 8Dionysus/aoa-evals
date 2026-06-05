"""Mechanic route-domain context construction."""

from __future__ import annotations

from typing import TypeVar

from validators import agon_routes, antifragility_routes, checkpoint_routes
from validators import distillation_routes, experience_routes, growth_cycle_routes
from validators import mechanic_provenance_bridge, method_growth_routes, questbook_routes
from validators import recurrence_routes, root_route_tokens, route_residue_common
from validators import rpg_routes, titan_routes


RouteContext = TypeVar("RouteContext")
PROVENANCE_TOKENS = (
    mechanic_provenance_bridge.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
)


def _context(context_type: type[RouteContext]) -> RouteContext:
    return context_type(require_tokens=root_route_tokens.context_require_tokens)


def _provenance_context(context_type: type[RouteContext]) -> RouteContext:
    return context_type(
        require_tokens=root_route_tokens.context_require_tokens,
        provenance_tokens=PROVENANCE_TOKENS,
    )


def route_residue_context() -> route_residue_common.RouteResidueContext:
    return _context(route_residue_common.RouteResidueContext)


def recurrence_route_context() -> recurrence_routes.RecurrenceRouteContext:
    return _provenance_context(recurrence_routes.RecurrenceRouteContext)


def checkpoint_route_context() -> checkpoint_routes.CheckpointRouteContext:
    return _provenance_context(checkpoint_routes.CheckpointRouteContext)


def experience_route_context() -> experience_routes.ExperienceRouteContext:
    return _provenance_context(experience_routes.ExperienceRouteContext)


def antifragility_route_context() -> antifragility_routes.AntifragilityRouteContext:
    return _provenance_context(antifragility_routes.AntifragilityRouteContext)


def method_growth_route_context() -> method_growth_routes.MethodGrowthRouteContext:
    return _provenance_context(method_growth_routes.MethodGrowthRouteContext)


def rpg_route_context() -> rpg_routes.RpgRouteContext:
    return _provenance_context(rpg_routes.RpgRouteContext)


def growth_cycle_route_context() -> growth_cycle_routes.GrowthCycleRouteContext:
    return _provenance_context(growth_cycle_routes.GrowthCycleRouteContext)


def distillation_route_context() -> distillation_routes.DistillationRouteContext:
    return _provenance_context(distillation_routes.DistillationRouteContext)


def titan_route_context() -> titan_routes.TitanRouteContext:
    return _context(titan_routes.TitanRouteContext)


def agon_route_context() -> agon_routes.AgonRouteContext:
    return _context(agon_routes.AgonRouteContext)


def questbook_route_context() -> questbook_routes.QuestbookRouteContext:
    return _provenance_context(questbook_routes.QuestbookRouteContext)
