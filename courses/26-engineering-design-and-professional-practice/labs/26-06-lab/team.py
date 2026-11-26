"""Team-sizing models for Lab 26-06.

- communication channels n(n - 1)/2, flat and in sub-teams (Example 26-06.1);
- output with a per-colleague coordination cost, the best flat team size, and a hierarchy of sub-teams
  with a cross-team interface cost (Example 26-06.2);
- Brooks's law: adding people who need ramp-up and mentoring (Example 26-06.3);
- management layers for a span of control (Example 26-06.4);
- base staff plus contractors for a varying load, and the newsvendor rule for the base (Example 26-06.5);
- converting a design-cost estimate into engineer-years and average headcount (Example 26-06.6).
Effort in person-months of effective work; money in dollars unless stated.
"""
from __future__ import annotations

import math
from typing import Sequence


# ---------------------------------------------------------------- communication
def channels(n: int) -> int:
    return n * (n - 1) // 2


def channels_hierarchy(teams: int, size: int) -> int:
    """Channels inside each team (members plus its lead) plus channels among the leads."""
    return teams * channels(size + 1) + channels(teams)


# ---------------------------------------------------------------- output and team size
def flat_output(n: float, c: float) -> float:
    """Effective full-time equivalents: each person loses a fraction c of time per colleague."""
    return n * (1 - c * (n - 1))


def best_flat_size(c: float) -> float:
    """d/dn [n(1 - c(n - 1))] = 0 gives n* = (1 + 1/c)/2."""
    return (1 + 1 / c) / 2


def hierarchy_output(teams: int, size: int, c: float, c_x: float) -> float:
    """Teams of `size` engineers (plus a lead who only coordinates); each member loses c per teammate, and
    every team loses a fraction c_x of its output per other team to interfaces."""
    return teams * size * (1 - c * (size - 1)) * (1 - c_x * (teams - 1))


# ---------------------------------------------------------------- Brooks's law
def finish_time(work: float, n: int, c: float, add: int = 0, ramp: float = 0.0, mentor: float = 0.0) -> float:
    """Months to finish `work` person-months with n people, adding `add` at t = 0 who are unproductive for
    `ramp` months and each take `mentor` of an existing engineer's time meanwhile."""
    total = n + add
    eff = 1 - c * (total - 1)
    if add == 0 or ramp == 0:
        return work / (total * eff)
    rate_ramp = (n - mentor * add) * eff
    done = rate_ramp * ramp
    if done >= work:
        return work / rate_ramp
    return ramp + (work - done) / (total * eff)


# ---------------------------------------------------------------- hierarchy
def management_layers(n: int, span: int) -> list[int]:
    """Managers needed at each level, bottom up, until one person leads."""
    levels, people = [], n
    while people > 1:
        people = math.ceil(people / span)
        levels.append(people)
    return levels


# ---------------------------------------------------------------- staffing
def staffing_cost(load: Sequence[float], base: float, cost_emp: float, cost_con: float) -> float:
    """Base employees all periods; contractors cover any load above the base."""
    return sum(base * cost_emp + max(0.0, l - base) * cost_con for l in load)


def newsvendor_base(load: Sequence[float], cost_emp: float, cost_con: float) -> float:
    """Raise the base while the share of periods whose load exceeds it is above cost_emp/cost_con."""
    ratio = cost_emp / cost_con
    best = 0.0
    for level in sorted(set(load)):
        share_above = sum(1 for l in load if l >= level) / len(load)
        if share_above > ratio:
            best = level
    return best


# ---------------------------------------------------------------- design cost to headcount
def engineer_years(design_cost: float, labor_share: float, loaded_cost: float) -> float:
    return design_cost * labor_share / loaded_cost
