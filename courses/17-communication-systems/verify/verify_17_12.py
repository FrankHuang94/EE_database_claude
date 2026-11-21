#!/usr/bin/env python3
"""Verify chapter 17-12 (multiple access, cellular and Wi-Fi): text, examples, problems and lab answers.

Routes:
- channel counts and CDMA capacity from the formulas; Walsh orthogonality by direct products;
- reuse geometry from hexagonal-lattice coordinates (co-channel cell positions computed, distances measured),
  cluster sizes enumerated;
- ALOHA maxima by numerical maximization and by Poisson simulation; CSMA slot outcomes in closed form and by
  simulated binomial slots;
- Erlang B by the factorial formula, by the recursion, and by an event-driven loss-system simulation;
- multi-user diversity by integrating against the density of the maximum and by simulating schedulers;
- HARQ by simulating independent and combined retransmissions.
"""
from __future__ import annotations

import heapq
import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-12-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import access as ac  # noqa: E402

CH = ROOT / "chapters" / "17-12-multiple-access-and-cellular-wifi.md"
v = Verifier.from_files("17-12", CH, ROOT / "solutions" / "17-12-solutions.md", LAB / "README.md")
rng = np.random.default_rng(17120)


def db(x):
    return 10 * math.log10(x)


def erlang_fact(c, a):
    return (a**c / math.factorial(c)) / sum(a**k / math.factorial(k) for k in range(c + 1))


def loss_sim(c, a, ncalls, rng):
    """Event-driven M/M/c/c: Poisson arrivals (rate a), unit-mean exponential holding."""
    t = 0.0
    busy = []
    blocked = 0
    for _ in range(ncalls):
        t += rng.exponential(1 / a)
        while busy and busy[0] <= t:
            heapq.heappop(busy)
        if len(busy) >= c:
            blocked += 1
        else:
            heapq.heappush(busy, t + rng.exponential(1.0))
    return blocked / ncalls


def cochannel_distance(i, j):
    """Hexagonal lattice with unit cell-centre spacing sqrt(3) R (R = 1): co-channel offset (i, j)."""
    a1 = np.array([math.sqrt(3), 0.0])
    a2 = np.array([math.sqrt(3) / 2, 1.5])
    return float(np.linalg.norm(i * a1 + j * a2))


def max_exp_mean(k):
    val, _ = integrate.quad(lambda x: x * k * math.exp(-x) * (1 - math.exp(-x)) ** (k - 1), 0, np.inf)
    return val


def harq_sim(fail_probs, ntrials, rng):
    """Simulate HARQ with conditional failure probabilities per attempt; returns (transmissions per success, residual)."""
    tx = 0
    ok = 0
    for _ in range(ntrials):
        for k, p in enumerate(fail_probs):
            tx += 1
            if rng.random() >= p:
                ok += 1
                break
    return ok / tx, 1 - ok / ntrials


# ------------------------------------------------------------------ text
v.check("Txt 17-12.a", optimize.minimize_scalar(lambda g: -g * math.exp(-2 * g), bounds=(0.01, 3), method="bounded").fun * -1)
v.check("Txt 17-12.b", -optimize.minimize_scalar(lambda g: -g * math.exp(-g), bounds=(0.01, 5), method="bounded").fun)
v.check("Txt 17-12.c", (1 - 0.1**4) / sum(0.1**k for k in range(4)))
v.check("Txt 17-12.d", 0.1**4)
v.assert_true("HARQ with independent attempts: throughput is exactly 1 - p for M = 1..6", all(abs((1 - p**m) / sum(p**k for k in range(m)) - (1 - p)) < 1e-12 for p in (0.1, 0.3, 0.5) for m in range(1, 7)))
walsh = np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]])
v.assert_true("length-4 Walsh codes are mutually orthogonal", np.array_equal(walsh @ walsh.T, 4 * np.eye(4)))
v.assert_true("hexagonal co-channel distance sqrt(3N) from lattice coordinates (N = 1, 3, 4, 7, 12)", all(abs(cochannel_distance(i, j) - math.sqrt(3 * (i * i + i * j + j * j))) < 1e-12 for i, j in ((1, 0), (1, 1), (2, 0), (2, 1), (2, 2))))
v.assert_true("valid cluster sizes start 1, 3, 4, 7, 9, 12, 13", ac.valid_cluster_sizes()[:7] == [1, 3, 4, 7, 9, 12, 13])
v.assert_true("slot model: success maximized at tau = 1/n (n = 10) and tends to 1/e", abs(optimize.minimize_scalar(lambda t: -10 * t * (1 - t) ** 9, bounds=(0.001, 0.5), method="bounded").x - 0.1) < 1e-4 and abs(1000 * 0.001 * 0.999**999 - 1 / math.e) < 2e-4)
v.assert_true("CSMA with W = 16: 10 stations succeed 38% and collide 33%; 50 collide 98.5%", abs(ac.slot_outcomes(10, 2 / 17)[1] - 0.38) < 0.005 and abs(ac.slot_outcomes(10, 2 / 17)[2] - 0.33) < 0.005 and abs(ac.slot_outcomes(50, 2 / 17)[2] - 0.985) < 0.0005)
v.assert_true("Erlang B: trunking occupancy 70% (28 ch, 20 Erl) vs 49% (10 ch, 5 Erl)", abs(20 * (1 - erlang_fact(28, 20)) / 28 - 0.70) < 0.005 and abs(5 * (1 - erlang_fact(10, 5)) / 10 - 0.49) < 0.005)
v.assert_true("mean of the best of K exponentials is the harmonic number (K = 2, 10)", all(abs(max_exp_mean(k) - sum(1 / i for i in range(1, k + 1))) < 1e-9 for k in (2, 10)))

# ------------------------------------------------------------------ examples
v.check("Ex 17-12.1a", (20e6 // 200e3) * 8)
G = 5e6 / 12.2e3
v.check("Ex 17-12.1b", db(G))
v.check("Ex 17-12.1c", 1 + G / 10**0.7)
v.check("Ex 17-12.1d", 1 + G / (10**0.7 * 0.5 * 1.6))
sirs = {N: (cochannel_distance(*ij) ** 4) / 6 for N, ij in ((1, (1, 0)), (3, (1, 1)), (4, (2, 0)), (7, (2, 1)))}
v.check("Ex 17-12.2a", db(sirs[1]))
v.check("Ex 17-12.2b", db(sirs[3]))
v.check("Ex 17-12.2c", db(sirs[7]))
v.check("Ex 17-12.2d", db(cochannel_distance(2, 1) ** 3.5 / 6))
v.check("Ex 17-12.2e", min(N for N in sirs if db(sirs[N]) >= 15))
v.assert_true("Example 2: N = 4 gives 13.80 dB; D/R = 1.732, 3.000, 4.583", abs(db(sirs[4]) - 13.80) < 0.005 and abs(cochannel_distance(1, 0) - 1.732) < 5e-4 and abs(cochannel_distance(1, 1) - 3.0) < 1e-12 and abs(cochannel_distance(2, 1) - 4.583) < 5e-4)
v.check("Ex 17-12.3a", 1 / (2 * math.e))
v.check("Ex 17-12.3b", 1000 / (2 * math.e))
v.check("Ex 17-12.3c", 1 / math.e)
v.check("Ex 17-12.3d", 1000 / math.e)
v.check("Ex 17-12.3e", math.exp(-2))
v.assert_true("Example 3: simulated slotted ALOHA at G = 1 and pure ALOHA at G = 0.5 match", abs(ac.simulate_slotted_aloha(1.0, 400_000, rng) - 1 / math.e) < 0.003 and abs(ac.simulate_pure_aloha(0.5, 400_000, rng) - 1 / (2 * math.e)) < 0.003)
tau = 2 / 17
v.check("Ex 17-12.4a", tau)
v.check("Ex 17-12.4b", (1 - tau) ** 10)
v.check("Ex 17-12.4c", 10 * tau * (1 - tau) ** 9)
v.check("Ex 17-12.4d", 1 - (1 - tau) ** 10 - 10 * tau * (1 - tau) ** 9)
v.check("Ex 17-12.4e", 50 * tau * (1 - tau) ** 49)
v.check("Ex 17-12.4f", 1 - (1 - tau) ** 50 - 50 * tau * (1 - tau) ** 49)
v.check("Ex 17-12.4g", 10 * 0.1 * 0.9**9)
sim = ac.simulate_slots(10, tau, 400_000, rng)
v.assert_true(f"Example 4: simulated slots {np.round(sim, 3)} match the closed form", all(abs(a - b) < 0.004 for a, b in zip(sim, ac.slot_outcomes(10, tau))))
v.check("Ex 17-12.5a", 100 * erlang_fact(10, 5))
v.check("Ex 17-12.5b", min(c for c in range(1, 60) if erlang_fact(c, 20) <= 0.02))
v.assert_true("Example 5: recursion equals the factorial formula; B(27, 20) = 2.68%, B(28, 20) = 1.88%", abs(ac.erlang_b(10, 5) - erlang_fact(10, 5)) < 1e-14 and abs(100 * erlang_fact(27, 20) - 2.68) < 0.005 and abs(100 * erlang_fact(28, 20) - 1.88) < 0.005)
bsim = loss_sim(10, 5.0, 400_000, rng)
v.assert_true(f"Example 5: loss-system simulation blocks {100 * bsim:.2f}% vs 1.84%", abs(bsim - erlang_fact(10, 5)) < 0.001)
rr = math.log2(math.e) * math.exp(0.1) * special.exp1(0.1)
mx = integrate.quad(lambda x: math.log2(1 + 10 * x) * 10 * math.exp(-x) * (1 - math.exp(-x)) ** 9, 0, np.inf, limit=200)[0]
v.check("Ex 17-12.6a", rr)
v.check("Ex 17-12.6b", mx)
v.check("Ex 17-12.6c", mx / rr)
v.check("Ex 17-12.6d", 10 * sum(1 / k for k in range(1, 11)))
v.check("Ex 17-12.6e", integrate.quad(lambda x: math.log2(1 + 10 * x) * 2 * math.exp(-x) * (1 - math.exp(-x)), 0, np.inf, limit=200)[0])
sched = ac.simulate_schedulers([10] * 10, 20_000, rng)
v.assert_true(f"Example 6: simulated round robin {sched['rr'].sum():.2f} and max-SNR {sched['max'].sum():.2f} b/s/Hz", abs(sched["rr"].sum() - rr) < 0.05 and abs(sched["max"].sum() - mx) < 0.05)
v.assert_true("Example 6: 29.3 is 14.7 dB", abs(db(10 * sum(1 / k for k in range(1, 11))) - 14.7) < 0.05)

# ------------------------------------------------------------------ problems
v.check("17-12.1a", 0.9 * 0.7)
v.check("17-12.1b", 0.9 * 0.3)
v.check("17-12.2a", float(np.dot(walsh[1], np.roll(walsh[1], 1))) / 4)
v.check("17-12.3a", db(1e7 / 1e5))
v.check("17-12.3b", 1 + 100 / 10**0.5)
v.check("17-12.3c", 1 + 100 / (10**0.5 * 0.4 * 1.5))
v.check("17-12.4a", db(128 * 10**-2))
for key, n in (("17-12.5a", 3), ("17-12.5b", 3.5), ("17-12.5c", 4)):
    v.check(key, min(N for N in ac.valid_cluster_sizes() if db(math.sqrt(3 * N) ** n / 6) >= 12))
v.check("17-12.6a", (1 / 0.3) ** 2)
v.check("17-12.7a", 20 * 0.05 * 0.95**19)
v.check("17-12.7b", 20 * 0.1 * 0.9**19)
v.check("17-12.8a", 2 / 0.05 - 1)
v.check("17-12.8b", 20 * 0.05 * 0.95**19)
v.check("17-12.9a", 100 * erlang_fact(5, 2))
c50 = min(c for c in range(1, 120) if ac.erlang_b(c, 50) <= 0.01)
v.check("17-12.9b", 100 * ac.erlang_b(c50, 50))
v.check("17-12.9c", c50)
v.assert_true("Problem 9: B(63, 50) = 1.09%; occupancy 77%", abs(100 * ac.erlang_b(63, 50) - 1.09) < 0.005 and abs(50 * (1 - ac.erlang_b(64, 50)) / 64 - 0.77) < 0.005)
v.check("17-12.10a", db(max_exp_mean(4)))
v.check("17-12.10b", db(sum(1 / k for k in range(1, 51))))
xw = rng.exponential(1.0, 1_000_000)
xs = rng.exponential(100.0, 1_000_000)
v.check("17-12.11a", 1 / (1 + 100))
v.assert_true("Problem 11: Monte Carlo share of the weak user matches 1/101", abs(np.mean(xw > xs) - 1 / 101) < 0.0005)
v.check("17-12.12a", 1 - 0.3)
v.check("17-12.12b", 0.3**4)
fails = np.cumprod([0.3, 0.05, 0.01, 0.002])
v.check("17-12.12c", 1 + fails[0] + fails[1] + fails[2])
v.check("17-12.12d", (1 - fails[3]) / (1 + fails[0] + fails[1] + fails[2]))
thr_sim, res_sim = harq_sim([0.3] * 4, 300_000, rng)
thr_c, _ = harq_sim([0.3, 0.05, 0.01, 0.002], 300_000, rng)
v.assert_true(f"Problem 12: simulated HARQ throughput {thr_sim:.3f} (independent) and {thr_c:.3f} (combining)", abs(thr_sim - 0.7) < 0.005 and abs(res_sim - 0.0081) < 0.001 and abs(thr_c - 0.760) < 0.005)

# ------------------------------------------------------------------ lab
v.check("Lab 17-12.a", db(math.sqrt(27) ** 3.5 / 6))
v.check("Lab 17-12.b", 0.25 * math.exp(-0.5))
t64 = 2 / 65
v.check("Lab 17-12.c", 50 * t64 * (1 - t64) ** 49)
v.check("Lab 17-12.d", 100 * erlang_fact(10, 7))
v.check("Lab 17-12.e", math.log2(math.e) * math.exp(0.01) * special.exp1(0.01) / 5)
v.assert_true("Lab part 3: W = 16 beats W = 64 for 5 stations; W = 64 beats W = 16 for 50", ac.slot_outcomes(5, 2 / 17)[1] > ac.slot_outcomes(5, t64)[1] and ac.slot_outcomes(50, t64)[1] > ac.slot_outcomes(50, 2 / 17)[1])
s5 = ac.simulate_schedulers([20, 15, 10, 5, 0], 40_000, rng)
v.assert_true(f"Lab part 5: Jain index max-SNR {ac.jain(s5['max']):.2f} (about 0.3), PF {ac.jain(s5['pf']):.2f} (about 0.8); PF sum between RR and max", abs(ac.jain(s5["max"]) - 0.31) < 0.05 and abs(ac.jain(s5["pf"]) - 0.80) < 0.05 and s5["rr"].sum() < s5["pf"].sum() < s5["max"].sum())

# reuse-1 corner SIR by a full hexagonal lattice sum; scheduler figures quoted in §3.6 from the lab simulation
_a1, _a2 = np.array([math.sqrt(3), 0.0]), np.array([math.sqrt(3) / 2, 1.5])
_pts = np.array([i * _a1 + j * _a2 for i in range(-60, 61) for j in range(-60, 61)])
_d = np.linalg.norm(_pts - np.array([0.0, 1.0]), axis=1)
_own = int(np.argmin(np.linalg.norm(_pts, axis=1)))
_pr = _d ** -4.0
v.check("Txt 17-12.e", 10 * math.log10(_pr[_own] / (_pr.sum() - _pr[_own])))
v.assert_true("corner is equidistant from three base stations", np.sum(np.isclose(_d, 1.0)) == 3)
_sch = ac.simulate_schedulers([20, 15, 10, 5, 0], 1_000_000, np.random.default_rng(1712))
v.check("Txt 17-12.f", float(np.sum(_sch["pf"])))
v.check("Txt 17-12.g", float(np.sum(_sch["max"])))
v.check("Txt 17-12.h", ac.jain(_sch["pf"]))
v.check("Txt 17-12.i", ac.jain(_sch["max"]))
v.assert_true("PF loses about a quarter of max-SNR's sum rate and beats round robin by about 45%",
              0.2 < 1 - np.sum(_sch["pf"]) / np.sum(_sch["max"]) < 0.3 and 1.4 < np.sum(_sch["pf"]) / np.sum(_sch["rr"]) < 1.5)

# Erlang C (from the birth-death chain continued past c, computed directly), sectorization, WCDMA gain
_A, _c = 10.0, 12
_terms = [_A**k / math.factorial(k) for k in range(_c)]
_tail = _A**_c / math.factorial(_c) * _c / (_c - _A)
_pw = _tail / (sum(_terms) + _tail)
v.check("Txt 17-12.j", 100 * _pw)
v.check("Txt 17-12.k", _pw / (_c - _A))
_b = ac.erlang_b(_c, _A)
v.assert_true("Erlang C from Erlang B: cB/(c - A(1 - B))", abs(_c * _b / (_c - _A * (1 - _b)) - _pw) < 1e-12)
v.check("Txt 17-12.l", 10 * math.log10(6 / 2))
v.check("Txt 17-12.m", 10 * math.log10(3.84e6 / 12200))

# Problems 17-12.13 (reuse + trunking) and 17-12.14 (normalized-SNR scheduler)
for tag, n_cl in (("a", 7), ("c", 4)):
    cpc = 125 // n_cl
    v.check(f"17-12.13{tag}", cpc)
    v.check(f"17-12.13{chr(ord(tag) + 1)}", 10 * math.log10(math.sqrt(3 * n_cl) ** 4 / 6))
_A7 = optimize.brentq(lambda a: ac.erlang_b(17, a) - 0.02, 1, 50)
_A4 = optimize.brentq(lambda a: ac.erlang_b(31, a) - 0.02, 1, 80)
v.check("17-12.13e", _A7)
v.check("17-12.13f", _A4)
v.check("17-12.13g", math.floor(_A7 / 0.05))
v.check("17-12.13h", math.floor(_A4 / 0.05))
for tag, g in (("a", 100.0), ("b", 1.0)):
    v.check(f"17-12.14{tag}", integrate.quad(lambda x: math.log2(1 + g * x) * math.exp(-x), 0, np.inf)[0] / 2)
for tag, g in (("c", 100.0), ("d", 1.0)):
    v.check(f"17-12.14{tag}", integrate.quad(lambda x: math.log2(1 + g * x) * 2 * math.exp(-x) * (1 - math.exp(-x)), 0, np.inf)[0] / 2)
_rng14 = np.random.default_rng(171214)
_g = _rng14.exponential(1.0, (400_000, 2)) * np.array([100.0, 1.0])
_win = np.argmax(_g / np.array([100.0, 1.0]), axis=1)
_thr = [np.sum(np.log2(1 + _g[_win == k, k])) / len(_g) for k in (0, 1)]
v.assert_true("normalized-SNR scheduler simulated: equal time shares and the integral throughputs", abs(np.mean(_win == 0) - 0.5) < 0.005 and abs(_thr[0] - 3.415) < 0.03 and abs(_thr[1] - 0.600) < 0.01, f"{_thr}")
_pf = ac.simulate_schedulers([20, 0], 300_000, np.random.default_rng(1715))
v.assert_true("rate-based PF gives about 3.69 and 0.58", abs(_pf["pf"][0] - 3.69) < 0.05 and abs(_pf["pf"][1] - 0.58) < 0.02, f"{_pf['pf']}")

# derived figures quoted in Solutions 17-12.4 and 17-12.7
v.check("17-12.4x", 10 * math.log10(128))
_s = lambda p: 20 * p * (1 - p) ** 19  # noqa: E731
v.check("17-12.7x", 100 * (1 - _s(0.1) / _s(0.05)))

sys.exit(v.finish())
