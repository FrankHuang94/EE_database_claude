"""Models for evaluating engineering teams (chapter 28-07): track-record shrinkage with a
Beta prior, lognormal schedule calibration, bench depth, scorecards, retention value and
regression capacity.

Probabilities are fractions; durations in months; money in $M.
"""
from __future__ import annotations

import math

from scipy import stats

# --- Track record --------------------------------------------------------------------------


def prior_params(mean, weight):
    """Beta(alpha0, beta0) with the given mean and weight alpha0 + beta0."""
    return mean * weight, (1 - mean) * weight


def posterior(alpha0, beta0, successes, n):
    """Posterior Beta parameters after s successes in n projects."""
    return alpha0 + successes, beta0 + n - successes


def posterior_mean(alpha0, beta0, successes, n):
    a, b = posterior(alpha0, beta0, successes, n)
    return a / (a + b)


def credible_interval(alpha0, beta0, successes, n, level=0.90):
    """Equal-tailed credible interval of the posterior."""
    a, b = posterior(alpha0, beta0, successes, n)
    tail = (1 - level) / 2
    return stats.beta.ppf(tail, a, b), stats.beta.ppf(1 - tail, a, b)


# --- Schedules -------------------------------------------------------------------------------


def schedule_fit(ratios):
    """Log-mean and sample standard deviation (n - 1) of actual/plan ratios."""
    logs = [math.log(x) for x in ratios]
    mu = sum(logs) / len(logs)
    sd = math.sqrt(sum((x - mu) ** 2 for x in logs) / (len(logs) - 1))
    return mu, sd


def on_time_probability(mu, sd):
    return stats.norm.cdf(-mu / sd)


def duration_quantile(plan, mu, sd, p):
    return plan * math.exp(mu + stats.norm.ppf(p) * sd)


# --- Bench depth -------------------------------------------------------------------------------


def horizon_rate(annual, years):
    """Probability that one person leaves within the horizon."""
    return 1 - (1 - annual) ** years


def capability_loss(q, owners, group_event=0.0):
    """Probability that all owners leave: c + (1 - c) q^k with a group-event probability c."""
    return group_event + (1 - group_event) * q ** owners


def any_single_owner_loss(q, m):
    """Probability of losing at least one of m single-owner capabilities."""
    return 1 - (1 - q) ** m


# --- Scorecards and value -------------------------------------------------------------------


def weighted_score(weights, scores):
    return sum(w * x for w, x in zip(weights, scores))


def geometric_score(weights, scores):
    return math.exp(sum(w * math.log(x) for w, x in zip(weights, scores)))


def gate_passes(scores, floor=2):
    return min(scores) >= floor


def retained_value(n, value_each, retention):
    return n * value_each * retention


def regression_hours(runs, cpu_hours_each, cores, utilization):
    return runs * cpu_hours_each / (cores * utilization)
