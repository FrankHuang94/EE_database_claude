"""Models for post-acquisition integration risk (chapter 28-08): synergy annuities with
delay and realization, migration and delay costs, parallel development paths, royalties,
export-control metrics, risk registers and earn-outs.

Money in $M unless noted; time in years; probabilities as fractions.
"""
from __future__ import annotations


def annuity(n, rate):
    """Present value of 1 a year for n years, first payment at the end of year 1."""
    return (1 - (1 + rate) ** -n) / rate


def synergy_value(per_year, years, rate, delay=0.0, realization=1.0, fixed_window=False):
    """PV of a synergy plan. With fixed_window, a delay of d whole years removes the first d
    years instead of shifting the plan."""
    if fixed_window:
        d = int(delay)
        return realization * per_year * annuity(years - d, rate) * (1 + rate) ** -d
    return realization * per_year * annuity(years, rate) * (1 + rate) ** -delay


def migration_cost(engineers, months, cost_per_engineer_month):
    return engineers * months * cost_per_engineer_month


def delay_cost(revenue_per_year, delay_months):
    """Revenue lost from a fixed market window."""
    return revenue_per_year * delay_months / 12


def parallel_gain(p1, p2, socket_value, p_both_fail=None):
    """Expected gain of keeping both programs over the better one alone."""
    both_fail = (1 - p1) * (1 - p2) if p_both_fail is None else p_both_fail
    return socket_value * (1 - both_fail - max(p1, p2))


def royalty(units, asp, rate):
    return units * asp * rate


def tpp(dense_tops, bits):
    """Total processing performance from dense TOPS (2 ops per MAC) and bit length."""
    return dense_tops * bits


def performance_density(tpp_value, die_mm2):
    return tpp_value / die_mm2


def expected_loss(risks):
    """risks: [(probability, impact), ...]."""
    return sum(p * i for p, i in risks)


def earnout_pv(upfront, contingent, probability, years, rate):
    """Expected present value of an all-or-nothing earn-out deal."""
    return upfront + probability * contingent * (1 + rate) ** -years
