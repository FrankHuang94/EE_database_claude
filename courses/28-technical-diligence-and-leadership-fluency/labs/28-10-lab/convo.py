"""Live checks and debrief tools for technical conversations (chapter 28-10).

The pocket-card functions reproduce the identities of chapters 28-02 to 28-09 so they can
be used quickly in drills; the debrief functions score answers as evidence.
"""
from __future__ import annotations

import math
import random

HOURS_PER_YEAR = 8766.0

# --- Pocket card ---------------------------------------------------------------------------


def roofline(peak_flops, mem_bw, batch, bytes_per_weight=1.0):
    """(ridge, decode intensity, attainable FLOP/s, share of peak)."""
    ridge = peak_flops / mem_bw
    intensity = 2 * batch / bytes_per_weight
    att = min(peak_flops, intensity * mem_bw)
    return ridge, intensity, att, att / peak_flops


def iso_power_reduction(perf, ipc, cap=1.0):
    return 1 - 1 / (cap * (perf / ipc) ** 3)


def link_power(bits_per_s, pj_per_bit):
    return bits_per_s * pj_per_bit * 1e-12


def zero_failure_bound(exposure, confidence=0.95):
    """Upper bound on a rate after zero events in the given exposure."""
    return -math.log(1 - confidence) / exposure


def schreier(sndr_db, fs, power_w):
    return sndr_db + 10 * math.log10(fs / 2 / power_w)


def loss(p_out, eta):
    return p_out * (1 / eta - 1)


def avg_current_ua(sleep_ua, events):
    """events: [(current µA, duration s, period s), ...]."""
    return sleep_ua + sum(i * t / p for i, t, p in events)


def battery_years(mah, ua):
    return mah / (ua / 1000) / HOURS_PER_YEAR


def beta_mean(successes, n, prior_mean=0.14, weight=10):
    return (prior_mean * weight + successes) / (weight + n)


def energy_cost(watts, pue, years, price):
    return watts / 1000 * pue * years * HOURS_PER_YEAR * price


def field_failures(fit, units, hours):
    return fit * 1e-9 * units * hours


# --- Debrief ------------------------------------------------------------------------------------


def debrief(prior, answers):
    """answers: [(likelihood ratio, cause label), ...]. Answers sharing a cause count once,
    at the ratio furthest from 1 (in log terms). Returns (odds, probability, ratios used)."""
    by_cause = {}
    for lr, cause in answers:
        if cause not in by_cause or abs(math.log(lr)) > abs(math.log(by_cause[cause])):
            by_cause[cause] = lr
    odds = prior / (1 - prior)
    for lr in by_cause.values():
        odds *= lr
    return odds, odds / (1 + odds), list(by_cause.values())


def trajectory(prior, ratios):
    out = [prior]
    odds = prior / (1 - prior)
    for lr in ratios:
        odds *= lr
        out.append(odds / (1 + odds))
    return out


def brier(forecasts, outcomes):
    return sum((p - o) ** 2 for p, o in zip(forecasts, outcomes)) / len(forecasts)


# --- Drills --------------------------------------------------------------------------------------


def drill(seed=None):
    """Draw a random live-check question; returns (prompt, answer, unit)."""
    rng = random.Random(seed)
    kind = rng.choice(["roofline", "link", "loss", "battery", "fit"])
    if kind == "roofline":
        f, b, n = rng.choice([1, 2, 4]) * 1e15, rng.choice([2, 4, 8]) * 1e12, rng.choice([4, 8, 16, 32])
        share = roofline(f, b, n)[3]
        return (f"{f/1e15:g} PFLOP/s, {b/1e12:g} TB/s, batch {n}, FP8: decode share of peak?", 100 * share, "%")
    if kind == "link":
        r, e = rng.choice([12.8, 25.6, 51.2]), rng.choice([2, 3, 4, 5])
        return (f"{r} Tb/s at {e} pJ/bit: power?", link_power(r * 1e12, e), "W")
    if kind == "loss":
        p, eta = rng.choice([1000, 3000, 5000]), rng.choice([0.94, 0.96, 0.975])
        return (f"{p} W out at {eta:.1%} efficiency: loss?", loss(p, eta), "W")
    if kind == "battery":
        s, i, t, per = rng.choice([1, 2]), rng.choice([2000, 3000]), rng.choice([0.002, 0.005]), rng.choice([1, 2, 5])
        ua = avg_current_ua(s, [(i, t, per)])
        return (f"sleep {s} µA, {i/1000:g} mA for {t*1000:g} ms every {per} s: average current?", ua, "µA")
    fit, u, h = rng.choice([10, 50, 100]), rng.choice([1e5, 1e6]), rng.choice([2000, 8766])
    return (f"{fit} FIT, {u:.0f} units, {h} h/year: failures a year?", field_failures(fit, u, h), "failures")
