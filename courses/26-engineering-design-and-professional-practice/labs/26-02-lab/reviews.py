"""Review and standards arithmetic for Lab 26-02.

- detection by k independent reviewers, and by reviewers who share blind spots (a mix of easy and hard
  defects), with the expected-cost-optimal number of reviewers (Example 26-02.2);
- capture-recapture estimates of the defects a review left behind, and a Monte Carlo of their bias
  (Example 26-02.3);
- the IEEE SA ballot rules: return, approval and abstention thresholds (Example 26-02.4);
- royalty stacking and the royalty base (Example 26-02.5);
- the expected value of designing to a draft standard (Example 26-02.6).
"""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np


# ---------------------------------------------------------------- reviewers
def p_found(p: float, k: int) -> float:
    """Probability that at least one of k independent reviewers, each finding a defect with probability p,
    finds it."""
    return 1.0 - (1.0 - p) ** k


def p_found_mix(classes: Sequence[tuple[float, float]], k: int) -> float:
    """Detection probability when defects come in classes [(fraction, per-reviewer p), ...].

    Within a class the reviewers are independent; across classes the difficulty differs, so the reviewers
    share blind spots for the hard class.
    """
    return sum(f * p_found(p, k) for f, p in classes)


def review_cost(k: int, n_defects: float, p: float, cost_reviewer: float, cost_escape: float) -> float:
    """Expected cost of k reviewers plus the expected cost of defects that escape all of them."""
    return cost_reviewer * k + cost_escape * n_defects * (1.0 - p) ** k


def best_k(n_defects: float, p: float, cost_reviewer: float, cost_escape: float, k_max: int = 30) -> int:
    """Number of independent reviewers that minimizes review_cost (searching 1..k_max)."""
    costs = [review_cost(k, n_defects, p, cost_reviewer, cost_escape) for k in range(1, k_max + 1)]
    return int(np.argmin(costs)) + 1


# ---------------------------------------------------------------- capture-recapture
def lincoln_petersen(n1: int, n2: int, m: int) -> float:
    """Estimated total defects from two reviews finding n1 and n2 with m in common."""
    return n1 * n2 / m


def chapman(n1: int, n2: int, m: int) -> float:
    """Chapman's less-biased version of the two-review estimate (defined even when m = 0)."""
    return (n1 + 1) * (n2 + 1) / (m + 1) - 1


def simulate_two_reviews(n_true: int, p1: float, p2: float, trials: int = 20000, seed: int = 262,
                         hard_fraction: float = 0.0, hard_p: float = 0.0) -> np.ndarray:
    """Chapman estimates from simulated pairs of reviews of a document with n_true defects.

    With hard_fraction > 0, that fraction of defects is found by each reviewer with probability hard_p
    instead of p1 or p2, which correlates the two reviews and biases the estimate low.
    """
    rng = np.random.default_rng(seed)
    n_hard = int(round(hard_fraction * n_true))
    pa = np.r_[np.full(n_true - n_hard, p1), np.full(n_hard, hard_p)]
    pb = np.r_[np.full(n_true - n_hard, p2), np.full(n_hard, hard_p)]
    a = rng.random((trials, n_true)) < pa
    b = rng.random((trials, n_true)) < pb
    n1, n2, m = a.sum(1), b.sum(1), (a & b).sum(1)
    return (n1 + 1) * (n2 + 1) / (m + 1) - 1


# ---------------------------------------------------------------- ballots
def ieee_ballot(group: int, approve: int, disapprove: int, abstain: int) -> dict:
    """Check a ballot against the IEEE SA rules quoted in 26-02: at least 75% of the balloting group must
    return a ballot, at least 75% of Approve plus Do Not Approve votes must be Approve, and the ballot is
    invalid if 30% or more of the returned ballots are abstentions."""
    returned = approve + disapprove + abstain
    ret = returned / group
    appr = approve / (approve + disapprove)
    abst = abstain / returned
    return {"return": ret, "approval": appr, "abstention": abst,
            "passes": ret >= 0.75 and appr >= 0.75 and abst < 0.30}


def approvals_needed(approve: int, disapprove: int) -> int:
    """Smallest number of Approve votes (with approve + disapprove fixed) that reaches 75% approval."""
    return math.ceil(0.75 * (approve + disapprove) - 1e-12)


# ---------------------------------------------------------------- royalties
def royalty_stack(rates: Sequence[float], base: float) -> float:
    """Total royalty when every holder charges its rate on the same base."""
    return sum(rates) * base


def top_down_share(aggregate_rate: float, base: float, patent_share: float) -> float:
    """A holder's royalty under a top-down cap split in proportion to its share of essential patents."""
    return aggregate_rate * base * patent_share


# ---------------------------------------------------------------- draft standards
def early_start_value(months_gained: float, value_per_month: float, p_change: float,
                      fix_cost: float, fix_months: float) -> float:
    """Expected net value of starting design before a standard freezes: the schedule gain minus the
    expected cost of a late change (its direct cost plus the delay it adds)."""
    return months_gained * value_per_month - p_change * (fix_cost + fix_months * value_per_month)
