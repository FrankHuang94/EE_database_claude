"""Small decision models for technical diligence (chapter 28-01).

Everything here is deliberately simple: weighted and geometric scorecards with
independent (or correlated) score uncertainty, Bayes' rule in odds form, a discrete
distribution of silicon spins, a binary earn-out, and the value of perfect and
imperfect information for a buy-or-pass decision. Units are whatever the caller uses
(scores on a 1-5 scale, money in consistent units).
"""
from __future__ import annotations

import math
import random

# --- Scorecards --------------------------------------------------------------------


def weighted_score(weights, scores):
    """Arithmetic weighted score sum(w_i s_i); weights must sum to 1."""
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1")
    return sum(w * s for w, s in zip(weights, scores))


def geometric_score(weights, scores):
    """Weighted geometric score prod(s_i ** w_i): a weak dimension drags the total down."""
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1")
    return math.exp(sum(w * math.log(s) for w, s in zip(weights, scores)))


def passes_gates(scores, thresholds):
    """True if every gated dimension meets its threshold (None means not gated)."""
    return all(t is None or s >= t for s, t in zip(scores, thresholds))


def score_variance(weights, sigmas, rho=0.0):
    """Variance of sum(w_i s_i) when each score has standard deviation sigma_i and every
    pair has correlation rho."""
    var = sum((w * s) ** 2 for w, s in zip(weights, sigmas))
    n = len(weights)
    for i in range(n):
        for j in range(i + 1, n):
            var += 2 * rho * weights[i] * weights[j] * sigmas[i] * sigmas[j]
    return var


def p_second_ahead(weights, scores_a, sig_a, scores_b, sig_b):
    """P(B's true weighted score exceeds A's), independent normal score errors."""
    mu = weighted_score(weights, scores_a) - weighted_score(weights, scores_b)
    sd = math.sqrt(score_variance(weights, sig_a) + score_variance(weights, sig_b))
    return 0.5 * math.erfc(mu / (sd * math.sqrt(2)))


def p_second_ahead_mc(weights, scores_a, sig_a, scores_b, sig_b, n=200_000, seed=1):
    """Monte Carlo version of p_second_ahead."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(n):
        a = sum(w * rng.gauss(m, s) for w, m, s in zip(weights, scores_a, sig_a))
        b = sum(w * rng.gauss(m, s) for w, m, s in zip(weights, scores_b, sig_b))
        hits += b > a
    return hits / n


# --- Evidence ----------------------------------------------------------------------


def posterior(prior, likelihood_ratios):
    """Posterior probability from a prior probability and independent likelihood ratios."""
    odds = prior / (1 - prior)
    for lr in likelihood_ratios:
        odds *= lr
    return odds / (1 + odds)


def required_lr(prior, target):
    """Combined likelihood ratio needed to move a prior probability to a target."""
    return (target / (1 - target)) / (prior / (1 - prior))


# --- Spins and milestones ----------------------------------------------------------


def spin_stats(dist, planned, months_per_spin, cost_per_spin):
    """dist: {spins: weight}. Returns (mean spins, P(spins <= planned),
    expected spins beyond plan, expected delay, expected extra cost)."""
    tot = sum(dist.values())
    mean = sum(k * v for k, v in dist.items()) / tot
    p_ok = sum(v for k, v in dist.items() if k <= planned) / tot
    extra = sum(max(0, k - planned) * v for k, v in dist.items()) / tot
    return mean, p_ok, extra, extra * months_per_spin, extra * cost_per_spin


def chain_probability(stage_probs):
    """Probability that every stage of a milestone chain succeeds (independent stages)."""
    p = 1.0
    for q in stage_probs:
        p *= q
    return p


def earnout_pv(probability, payment, years, rate):
    """Present value of a binary contingent payment."""
    return probability * payment / (1 + rate) ** years


# --- Value of information ----------------------------------------------------------


def buy_or_pass(p, gain, loss):
    """Expected value of buying (gain if the technology works, loss if not) against
    passing (0). Returns (E[buy], EVPI)."""
    e_buy = p * gain + (1 - p) * loss
    best = max(e_buy, 0.0)
    return e_buy, p * max(gain, 0.0) + (1 - p) * max(loss, 0.0) - best


def evsi(p, gain, loss, sensitivity, specificity):
    """Expected value of sample information for a test that passes a working technology
    with probability `sensitivity` and fails a broken one with probability `specificity`.
    Returns (EVSI, P(pass), P(works | pass), E[buy | pass], P(works | fail), E[buy | fail])."""
    e_buy, _ = buy_or_pass(p, gain, loss)
    p_pass = p * sensitivity + (1 - p) * (1 - specificity)
    q_pass = p * sensitivity / p_pass
    q_fail = p * (1 - sensitivity) / (1 - p_pass)
    e_pass = q_pass * gain + (1 - q_pass) * loss
    e_fail = q_fail * gain + (1 - q_fail) * loss
    value = p_pass * max(e_pass, 0.0) + (1 - p_pass) * max(e_fail, 0.0) - max(e_buy, 0.0)
    return value, p_pass, q_pass, e_pass, q_fail, e_fail


# --- The chapter's cases -----------------------------------------------------------

WEIGHTS = [0.20, 0.15, 0.15, 0.15, 0.10, 0.15, 0.10]
DIMENSIONS = ["architecture", "implementation", "IP position", "team", "roadmap",
              "ecosystem and software", "manufacturing and supply"]
TARGET_A = [4.5, 4.0, 3.0, 4.5, 4.0, 2.0, 3.5]
TARGET_B = [3.5, 3.5, 4.0, 3.5, 3.5, 4.0, 3.5]
SIGMA_A = [0.75, 0.5, 0.5, 0.75, 0.5, 0.5, 0.5]
SIGMA_B = [0.4] * 7
SPINS_2024 = {1: 14, 2: 25, 3: 28, 4: 16, 5: 10, 6: 4}  # chart readings, R-645
