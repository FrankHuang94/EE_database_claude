#!/usr/bin/env python3
"""Verify every number in chapter 19-07 (sequential timing and clocking), its problems and its lab.

Independent routes:
- setup and hold by explicit arrival-time and required-time bookkeeping on a timeline (launch edge, capture edge,
  skew), not by the rearranged inequalities;
- skew windows by scanning skew on a fine grid;
- pipeline optima by direct numerical minimization;
- metastability by integrating the cross-coupled pair with a separately written square-law model (Radau), and tau
  by fitting resolution time against log offset over several offsets;
- MTBF by direct evaluation; the lab module is checked against these results; ngspice confirms the pair (meta.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import timing as tm  # noqa: E402

v = Verifier.from_files("19-07", ROOT / "chapters" / "19-07-sequential-timing-and-clocking.md",
                        ROOT / "solutions" / "19-07-solutions.md", LAB / "README.md")
P = 1e-12
YEAR = 365.25 * 86400


# ---------------------------------------------------------------- timeline bookkeeping (all times in ps)
def setup_slack(tc, tpcq, tpd, tsu, skew=0.0, jitter=0.0):
    launch = 0.0
    arrival = launch + tpcq + tpd
    capture = tc + skew - jitter          # next edge at the capture register, early by the jitter
    return capture - tsu - arrival


def hold_slack(tccq, tcd, th, skew=0.0):
    earliest_new = 0.0 + tccq + tcd       # new data from the same edge at the launch register
    must_hold_until = 0.0 + skew + th     # capture register's edge plus hold
    return earliest_new - must_hold_until


def min_tc(tpcq, tpd, tsu, skew=0.0, jitter=0.0):
    return minimize_scalar(lambda t: (setup_slack(t, tpcq, tpd, tsu, skew, jitter)) ** 2, bounds=(0, 1e5),
                           method="bounded", options={"xatol": 1e-9}).x


t1 = min_tc(30, 250, 20)
v.check("Ex 19-07.1a", t1)
v.check("Ex 19-07.1b", 1e3 / t1)
t1b = min_tc(30, 250, 20, skew=-15, jitter=10)
v.check("Ex 19-07.1c", t1b)
v.check("Ex 19-07.1d", 1e3 / t1b)
v.check("Ex 19-07.1e", 100 * (1 - t1 / t1b))
v.check("Ex 19-07.2a", hold_slack(15, 5, 25, 20))
v.check("Ex 19-07.2b", -hold_slack(15, 5, 25, 20))
v.check("Ex 19-07.2c", hold_slack(15, 5, 25, 0))


def window(tc, tpcq, tpd, tsu, tccq, tcd, th):
    sk = np.arange(-200, 200.0001, 0.001)
    ok = [s for s in sk if setup_slack(tc, tpcq, tpd, tsu, s) >= -1e-9 and hold_slack(tccq, tcd, th, s) >= -1e-9]
    return min(ok), max(ok)


lo, hi = window(500, 30, 400, 20, 20, 30, 15)
v.check("Ex 19-07.3a", lo)
v.check("Ex 19-07.3b", hi)
lo4, hi4 = window(700, 35, 600, 30, 25, 40, 20)
v.check("19-07.4a", lo4)
v.check("19-07.4b", hi4)

for n, keys in ((1, "abc"), (2, "def"), (4, "ghi"), (8, "jkl"), (16, "mno")):
    tc = 2000 / n + 60
    v.check(f"Ex 19-07.4{keys[0]}", tc)
    v.check(f"Ex 19-07.4{keys[1]}", 1e3 / tc)
    v.check(f"Ex 19-07.4{keys[2]}", 100 * 60 / tc)
v.check("Ex 19-07.4p", 16 * (2000 / 16 + 60))
v.check("Ex 19-07.4q", 100 * (16 * (2000 / 16 + 60) / 2000 - 1))
v.check("Ex 19-07.4r", (2000 / 8 + 60) / (2000 / 16 + 60))
v.assert_true("lab pipeline_period", abs(tm.pipeline_period(2000e-12, 8, 60e-12) - 310e-12) < 1e-18, "")

# latches: simulate the two-phase loop by tracking arrival times through transparent latches
def latch_loop_ok(tc, l1, l2, tdq, tsu, cycles=50):
    """Latch A opens at 0 (closes at tc/2), latch B opens at tc/2 (closes at tc). Data departs A at max(arrival, open)
    + tdq, crosses l1 to B, departs B, crosses l2 back to A in the next cycle. Fails if data arrives later than the
    latch's closing edge minus setup."""
    depart_a = tdq
    worst_borrow = 0.0
    for k in range(cycles):
        arr_b = depart_a + l1
        open_b, close_b = k * tc + tc / 2, k * tc + tc
        if arr_b > close_b - tsu:
            return False, worst_borrow
        worst_borrow = max(worst_borrow, arr_b - open_b)
        depart_b = max(arr_b, open_b) + tdq
        arr_a = depart_b + l2
        open_a, close_a = (k + 1) * tc, (k + 1) * tc + tc / 2
        if arr_a > close_a - tsu:
            return False, worst_borrow
        depart_a = max(arr_a, open_a) + tdq
    return True, worst_borrow


ok5, borrow5 = latch_loop_ok(500, 300, 120, 25, 20)
v.assert_true("Example 5 loop meets timing", ok5, "")
v.check("Ex 19-07.5a", 500 / 2 - 20)
v.check("Ex 19-07.5b", 300 + 120 + 2 * 25)
v.check("Ex 19-07.5c", 300 + 25 - 250)
ok8, borrow8 = latch_loop_ok(400, 260, 90, 20, 15)
v.assert_true("Problem 8 loop meets timing", ok8, "")
v.check("19-07.8a", 400 / 2 - 15)
v.check("19-07.8b", 260 + 90 + 2 * 20)
v.check("19-07.8c", 260 + 20 - 200)
v.assert_true("a 500 ps loop with 300 ps halves fails", not latch_loop_ok(500, 300, 200, 25, 20)[0], "")


# ---------------------------------------------------------------- metastability by an independent ODE
def ids(k, vgs, vds, vt=0.35):
    ov = vgs - vt
    if ov <= 0 or vds <= 0:
        return 0.0
    return k * (ov * vds - vds * vds / 2) if vds < ov else k * ov * ov / 2


def resolve(dv0, k=200e-6, c=10e-15, vdd=1.2, target=0.9):
    def f(_t, x):
        a, b = x
        return [(ids(k, vdd - b, vdd - a) - ids(k, b, a)) / c, (ids(k, vdd - a, vdd - b) - ids(k, a, b)) / c]
    ev = lambda _t, x: x[0] - target  # noqa: E731
    ev.terminal = True
    s = solve_ivp(f, (0, 2e-8), [vdd / 2 + dv0 / 2, vdd / 2 - dv0 / 2], method="Radau", events=ev, rtol=1e-12,
                  atol=1e-18)
    return float(s.t_events[0][0])


r1m, r1u = resolve(1e-3), resolve(1e-6)
v.check("Ex 19-07.6a", r1m / P)
v.check("Ex 19-07.6b", r1u / P)
offs = np.array([1e-9, 1e-8, 1e-7, 1e-6])
tfit = np.polyfit(np.log(1 / offs), [resolve(o) for o in offs], 1)[0]
v.check("Ex 19-07.6c", tfit / P)
v.check("Ex 19-07.6d", tfit * math.log(1000) / P)
v.assert_true("simulated difference equals tau ln 1000", abs((r1u - r1m) - 100e-12 * math.log(1000)) < 0.5e-12,
              f"{(r1u - r1m) / P:.2f} ps")
v.check("Lab 19-07.a", np.polyfit(np.log(1 / offs[:3]), [resolve(o, c=20e-15) for o in offs[:3]], 1)[0] / P)
v.check("Lab 19-07.b", np.polyfit(np.log(1 / offs[:3]), [resolve(o, k=400e-6) for o in offs[:3]], 1)[0] / P)
v.check("19-07.12a", np.polyfit(np.log(1 / offs[:3]), [resolve(o, k=400e-6) for o in offs[:3]], 1)[0] / P)
v.assert_true("lab resolve_time matches", abs(tm.resolve_time(1e-3) - r1m) < 1e-15, "")

m1 = math.exp(300 / 20) / (20e-12 * 1e9 * 100e6)
m2 = math.exp(950 / 20) / (20e-12 * 1e9 * 100e6)
v.check("Ex 19-07.6e", m1)
v.check("Ex 19-07.6f", m2)
v.check("Ex 19-07.6g", m2 / YEAR / 1e6)
v.check("Ex 19-07.6h", (950 - 300) / 20)
v.check("Ex 19-07.6i", math.exp((950 - 300) / 20))
rate = 10e-12 * 2e9 * 50e6
m10 = math.exp(450 / 15) / rate
v.check("19-07.10a", m10)
v.check("19-07.10b", m10 / 86400)
v.check("19-07.10e", 10 * YEAR * rate)
v.check("19-07.10c", 15 * math.log(10 * YEAR * rate))
v.check("19-07.10d", math.exp(950 / 15) / rate / YEAR)
v.check("19-07.9a", 5e-15 / 200e-6 / P)
v.check("19-07.9b", 5e-15 / 200e-6 * math.log(1000) / P)

# ---------------------------------------------------------------- problems 1-3, 5-7, 11
v.check("19-07.1a", min_tc(40, 500, 25))
v.check("19-07.1b", 1e3 / min_tc(40, 500, 25))
v.check("19-07.2a", hold_slack(30, 0, 10))
v.check("19-07.2b", hold_slack(30, 0, 10))
v.check("19-07.3a", 60 / 15)
v.check("19-07.3b", 100 * 4 / 20)
v.check("19-07.5a", 400 - 70 - 15 - 20)
v.check("19-07.5b", 100 * 295 / 400)
n6 = next(n for n in range(1, 50) if 1200 / n + 50 <= 250)
v.check("19-07.6a", n6)
v.check("19-07.6b", n6 * 250)
v.check("19-07.6c", 100 * (n6 * 250 / 1200 - 1))
v.check("19-07.7a", 100 * 50 / (1200 / 6 + 50))
v.check("19-07.7b", 1e3 / (1200 / 12 + 50))


def t_instr(n, tl=2000, to=60, b=0.1):
    return (tl / n + to) * (1 + b * n)


nopt = minimize_scalar(t_instr, bounds=(1, 100), method="bounded", options={"xatol": 1e-10}).x
v.check("19-07.11a", nopt)
v.check("19-07.11b", t_instr(18))
v.check("19-07.11c", t_instr(19))
v.check("19-07.11d", t_instr(1))
v.check("19-07.11e", t_instr(1) / t_instr(18))
v.check("19-07.11f", 2000 / 18 + 60)
v.check("19-07.11g", (2000 + 60) / (2000 / 18 + 60))
v.check("19-07.11h", 18)
v.assert_true("closed-form optimum", abs(nopt - math.sqrt(2000 / (0.1 * 60))) < 1e-6, "")

# ---------------------------------------------------------------- practitioner arithmetic [R-316]
v.check("Txt 19-07.a", 100 * 28 / 1250)
v.check("Txt 19-07.b", 100 * 4.5 / 25)
v.check("Txt 19-07.c", 0.2692208 + 0.1033184)
v.check("Txt 19-07.d", (0.2692208 + 0.1033184) / (0.5 * 130e-3))
v.check("Txt 19-07.i", (0.2692208 + 0.1033184) / (0.36 * 130e-3))
v.check("Txt 19-07.j", (0.2692208 + 0.1033184) / (3 * 31.8e-3))
v.check("Txt 19-07.e", resolve(1e-9) / P)
v.check("Txt 19-07.f", tfit * math.log(10) / P)
v.check("Txt 19-07.g", 1e3 / (2000 / 32 + 60))
v.check("Txt 19-07.h", 100 * 60 / (2000 / 32 + 60))

sys.exit(v.finish())
