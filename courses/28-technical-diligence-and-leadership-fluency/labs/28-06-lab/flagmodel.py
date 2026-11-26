"""Models for red and green flags in technical diligence (chapter 28-06): flags as
diagnostic tests, checklist false alarms, count thresholds, key-person risk, customer
concentration and the design-win funnel.

All probabilities are fractions; money in $M; time in years.
"""
from __future__ import annotations

from scipy import stats

# --- Flags as tests ----------------------------------------------------------------------


def lr_pos(sens, fpr):
    """Likelihood ratio of a flag that is present: sensitivity / false-positive rate."""
    return sens / fpr


def lr_neg(sens, fpr):
    """Likelihood ratio of a flag that is absent: (1 - sensitivity) / (1 - fpr)."""
    return (1 - sens) / (1 - fpr)


def posterior(prior, *ratios):
    """Posterior (odds, probability) of trouble from a prior and likelihood ratios."""
    odds = prior / (1 - prior)
    for r in ratios:
        odds *= r
    return odds, odds / (1 + odds)


# --- Checklists --------------------------------------------------------------------------


def false_alarm(n, fpr):
    """Probability that a healthy company shows at least one of n independent flags."""
    return 1 - (1 - fpr) ** n


def tail(n, p, k):
    """P(K >= k) for K ~ Binomial(n, p)."""
    return stats.binom.sf(k - 1, n, p)


def threshold_table(n, fpr, sens, kmax=None):
    """Rows (k, sensitivity, false-positive rate, likelihood ratio) for 'K >= k'."""
    kmax = kmax or n
    rows = []
    for k in range(1, kmax + 1):
        se, fp = tail(n, sens, k), tail(n, fpr, k)
        rows.append((k, se, fp, se / fp))
    return rows


# --- Organization and commerce ---------------------------------------------------------


def key_person_loss(m, q, years):
    """Probability that at least one of m key people (annual departure rate q) leaves."""
    return 1 - (1 - q) ** (m * years)


def hhi(shares):
    """Herfindahl-Hirschman index of revenue shares (fractions summing to 1)."""
    return sum(s * s for s in shares)


def effective_customers(shares):
    """Number of equal customers with the same concentration: 1 / HHI."""
    return 1 / hhi(shares)


def funnel_value(n_wins, p_prod, life_rev, first_year, n_years, rate):
    """Risk-adjusted present value of a design-win funnel, revenue spread evenly over
    n_years starting in first_year."""
    factor = sum((1 + rate) ** -k for k in range(first_year, first_year + n_years)) / n_years
    return n_wins * p_prod * life_rev * factor
