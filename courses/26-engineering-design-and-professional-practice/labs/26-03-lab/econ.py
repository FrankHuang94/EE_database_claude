"""Engineering-economics tools for Lab 26-03.

- FE interest factors (F/P, P/F, P/A, A/P, F/A, A/F), effective and continuous rates;
- NPV, IRR (bisection) and simple payback;
- the cascaded per-unit cost stack and gross margin (Example 26-03.2);
- NRE amortization and break-even volume (Example 26-03.3);
- a chip program's cash flows with a schedule slip in fractional years and a closing market window
  (Example 26-03.5), and a one-at-a-time tornado analysis.
"""
from __future__ import annotations

import math
from typing import Callable, Sequence


# ---------------------------------------------------------------- interest factors
def f_p(i: float, n: float) -> float:
    return (1 + i) ** n


def p_f(i: float, n: float) -> float:
    return (1 + i) ** -n


def p_a(i: float, n: int) -> float:
    return (1 - (1 + i) ** -n) / i


def a_p(i: float, n: int) -> float:
    return 1 / p_a(i, n)


def f_a(i: float, n: int) -> float:
    return ((1 + i) ** n - 1) / i


def a_f(i: float, n: int) -> float:
    return 1 / f_a(i, n)


def effective_rate(r_nominal: float, m: float | None) -> float:
    """Effective annual rate for nominal r compounded m times a year (m=None means continuously)."""
    return math.exp(r_nominal) - 1 if m is None else (1 + r_nominal / m) ** m - 1


# ---------------------------------------------------------------- cash-flow measures
def npv(rate: float, flows: Sequence[float], times: Sequence[float] | None = None) -> float:
    times = range(len(flows)) if times is None else times
    return sum(cf / (1 + rate) ** t for cf, t in zip(flows, times))


def irr(flows: Sequence[float], lo: float = -0.99, hi: float = 10.0, tol: float = 1e-12) -> float:
    """Internal rate of return by bisection (assumes one sign change of NPV between lo and hi)."""
    f_lo, f_hi = npv(lo, flows), npv(hi, flows)
    if f_lo * f_hi > 0:
        raise ValueError("NPV does not change sign on the bracket")
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = npv(mid, flows)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


def payback(flows: Sequence[float]) -> float:
    """Simple payback in periods, interpolating within the period in which cumulative cash turns positive."""
    cum = 0.0
    for t, cf in enumerate(flows):
        if cum + cf >= 0 and cum < 0:
            return t - 1 + (-cum) / cf
        cum += cf
    return math.inf


# ---------------------------------------------------------------- cost stack
def dies_per_wafer(diameter_mm: float, area_mm2: float) -> int:
    return math.floor(math.pi * diameter_mm**2 / (4 * area_mm2) - math.pi * diameter_mm / math.sqrt(2 * area_mm2))


def cost_stack(wafer: float, dpw: int, y_die: float, pkg: float, y_asm: float, test: float, y_test: float,
               royalty: float) -> dict:
    """Per-unit costs through the flow; yields divide the accumulated cost at each gate."""
    die = wafer / (dpw * y_die)
    after_asm = (die + pkg) / y_asm
    after_test = (after_asm + test) / y_test
    return {"die": die, "after_asm": after_asm, "after_test": after_test, "cogs": after_test + royalty}


def gross_margin(asp: float, cogs: float) -> float:
    return (asp - cogs) / asp


def breakeven_volume(nre: float, asp: float, cogs: float) -> float:
    return nre / (asp - cogs)


# ---------------------------------------------------------------- programs
def program_flows(nre_by_year: Sequence[float], units_by_year: Sequence[float], contribution: float,
                  slip: float = 0.0, window_end: float | None = None) -> tuple[list[float], list[float]]:
    """Cash flows and their times for a program: NRE at years 0, 1, ...; sales units starting the year after
    the last NRE year, shifted by `slip` years, each year's cash booked at its end. Each sales year spans the
    year before its cash date; the fraction of that span falling after `window_end` is lost."""
    flows, times = [], []
    for t, c in enumerate(nre_by_year):
        flows.append(-c)
        times.append(float(t))
    start = len(nre_by_year)
    for k, u in enumerate(units_by_year):
        t = start + k + slip
        keep = 1.0
        if window_end is not None:
            keep = min(max(window_end - (t - 1), 0.0), 1.0)
        if keep <= 0:
            continue
        flows.append(u * contribution * keep)
        times.append(t)
    return flows, times


def tornado(base: dict, model: Callable[[dict], float], swing: float = 0.10) -> list[tuple[str, float, float]]:
    """One-at-a-time sensitivity: (input, NPV at -swing, NPV at +swing), sorted by the size of the range."""
    out = []
    for k in base:
        lo = dict(base, **{k: base[k] * (1 - swing)})
        hi = dict(base, **{k: base[k] * (1 + swing)})
        out.append((k, model(lo), model(hi)))
    return sorted(out, key=lambda r: -abs(r[2] - r[1]))
