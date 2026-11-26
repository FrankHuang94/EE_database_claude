#!/usr/bin/env python3
"""Verify every number in chapter 27-01 (system analysis method), its problems and its lab.

Independent routes:
- converter trees by energy accounting over a simulated hour (load energy plus each converter's loss);
- thermal limits by time-stepping C dT/dt = P - (T - T_a)/theta until the limit is crossed
  (the lab uses the closed-form logarithm);
- pipelines by simulating items through a chain of fixed-time stages and measuring the output rate;
- Little's law by counting items in flight in a simulated stream;
- the shadow price by a numerical derivative of performance with respect to power;
- Amdahl's law by adding up the sped-up times directly.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sysbudget as sb  # noqa: E402

v = Verifier.from_files("27-01", ROOT / "chapters" / "27-01-system-analysis-method.md",
                        ROOT / "solutions" / "27-01-solutions.md", LAB / "README.md")


def tree_by_energy(loads, hours=1.0):
    """Battery energy over `hours`: each converter delivers its load and burns P(1/eta - 1) as heat."""
    e_load = sum(p * hours for _, p, _ in loads)
    e_loss = {name: p * (1 / eta - 1) * hours for name, p, eta in loads}
    return e_load, e_loss, e_load + sum(e_loss.values())


def burst_by_stepping(t0, t_limit, t_amb, p, theta, c_th, dt=0.001, t_max=1e5):
    """Euler-integrate the thermal RC until the node reaches t_limit; returns the crossing time."""
    temp, t = t0, 0.0
    while t < t_max:
        nxt = temp + dt * (p - (temp - t_amb) / theta) / c_th
        if nxt >= t_limit:
            return t + dt * (t_limit - temp) / (nxt - temp)
        temp, t = nxt, t + dt
    return math.inf


def pipeline_by_simulation(rates, n_items=4000):
    """Push items through stages with service time 1/rate each; return the steady output rate."""
    free_at = [0.0] * len(rates)
    done = []
    for _ in range(n_items):
        t = 0.0
        for k, r in enumerate(rates):
            start = max(t, free_at[k])
            free_at[k] = start + 1 / r
            t = free_at[k]
        done.append(t)
    half = n_items // 2
    return (n_items - half - 1) / (done[-1] - done[half])


def in_flight_by_counting(rate, latency, start=2.0, stop=8.0, samples=60000):
    """Items enter every 1/rate s and leave `latency` later; time-average the count inside."""
    entries = [k / rate for k in range(int(10.0 * rate))]
    total = 0
    for j in range(samples):
        t = start + (stop - start) * (j + 0.5) / samples
        total += sum(1 for e in entries if e <= t < e + latency)
    return total / samples


# ---------------------------------------------------------------- Example 1 (power tree)
ldo = 1.8 / 3.7
loads1 = [("SoC", 1.8, 0.88), ("DRAM", 0.4, 0.90), ("display", 1.2, 0.85), ("radio", 0.6, 0.90),
          ("sensors", 0.2, ldo)]
e_load, e_loss, e_batt = tree_by_energy(loads1)
t1 = sb.power_tree(loads1)
v.assert_true("Ex 1 lab tree equals energy accounting", abs(t1["p_batt"] - e_batt) < 1e-12)
v.check("Ex 27-01.1a", 100 * ldo)
for k, (name, p, eta) in enumerate(loads1, start=1):
    v.check(f"Ex 27-01.1a{k}", p + e_loss[name])
v.check("Ex 27-01.1a6", e_batt)
v.check("Ex 27-01.1a7", e_load)
v.check("Ex 27-01.1a8", 100 * e_load / e_batt)
v.check("Ex 27-01.1a9", sum(e_loss.values()))
v.check("Ex 27-01.1b", e_loss["SoC"])
v.check("Ex 27-01.1b1", e_loss["display"])
v.check("Ex 27-01.1b2", e_loss["sensors"])
v.check("Ex 27-01.1b3", e_loss["radio"])
v.check("Ex 27-01.1b4", e_loss["DRAM"])
energy = 5000e-3 * 3.85
usable = 0.9 * energy
v.check("Ex 27-01.1c", energy)
v.check("Ex 27-01.1c1", usable)
v.check("Ex 27-01.1c2", usable / e_batt)
buck_in = 0.2 / 0.90
v.check("Ex 27-01.1d0", buck_in)
v.check("Ex 27-01.1d", 0.2 / ldo - buck_in)
_, _, e_batt_buck = tree_by_energy(loads1[:-1] + [("sensors", 0.2, 0.90)])
v.check("Ex 27-01.1d1", usable / e_batt_buck)
v.check("Ex 27-01.1d2", 60 * (usable / e_batt_buck - usable / e_batt))
v.check("Txt 27-01.9", 100 * (e_batt / e_load - 1))

# ---------------------------------------------------------------- Example 2 (thermal)
p_sus = (43 - 25) / 4.0
v.check("Ex 27-01.2a", p_sus)
v.check("Ex 27-01.2a1", p_sus - 1.0)
v.check("Ex 27-01.2a2", 43 + (p_sus - 1.0) * 6.0)
v.check("Ex 27-01.2b", 25 + 2.0 * 4.0)
v.check("Ex 27-01.2b1", 4.0 * 60)
v.check("Ex 27-01.2b2", 25 + 9 * 4.0)
tb = burst_by_stepping(33.0, 43.0, 25.0, 9.0, 4.0, 60.0)
v.assert_true("Ex 2 stepped burst equals the lab's closed form",
              abs(tb - sb.time_to_limit(33.0, 43.0, 25.0, 9.0, 4.0, 60.0)) < 0.01)
v.check("Ex 27-01.2b3", tb)
v.check("Ex 27-01.2c", (95 - 43) / 6.0)
d = (p_sus - 2.0) / (9 - 2.0)
v.assert_true("Ex 2 the duty-weighted average equals the sustained power", abs(9 * d + 2 * (1 - d) - p_sus) < 1e-12)
v.check("Ex 27-01.2d", d)

# ---------------------------------------------------------------- Example 3 (roofline)
peak, bw = 400e12, 3.2e12
v.check("Ex 27-01.3a", peak / bw)
v.check("Ex 27-01.3b", min(peak, 300 * bw) / 1e12)
v.check("Ex 27-01.3c", min(peak, 1 * bw) / 1e12)
v.check("Ex 27-01.3c1", 100 * min(peak, bw) / peak)
bytes_tok = 7e9 * 2
v.check("Ex 27-01.3c3", bytes_tok / 1e9)
v.check("Ex 27-01.3c4", bw / bytes_tok)
v.check("Ex 27-01.3c2", bw / bytes_tok)
v.check("Ex 27-01.3d", min(peak, 32 * bw) / 1e12)
v.check("Ex 27-01.3d1", 32 * bw / bytes_tok)

# ---------------------------------------------------------------- Example 4 (pipeline, Little)
stages = [120, 90, 72, 60, 40 / 0.5]
v.check("Ex 27-01.4a", 40 / 0.5)
v.check("Ex 27-01.4a1", pipeline_by_simulation(stages))
v.check("Ex 27-01.4b", pipeline_by_simulation([120, 90, 72, 120, 80]))
v.check("Ex 27-01.4c", in_flight_by_counting(60, 0.080))
v.assert_true("Ex 4 Little's law gives 4.8 frames", abs(sb.littles_law(60, 0.080) - 4.8) < 1e-12)
v.check("Ex 27-01.4c1", math.ceil(60 * 0.080) * 12)
v.check("Ex 27-01.4d", 3 * 2 * 12e6 * 60 / 1e9)
v.check("Ex 27-01.4d1", 100 * (3 * 2 * 12e6 * 60) / (9600e6 * 64 / 8))

# ---------------------------------------------------------------- Example 5 (BOM)
parts5 = {"SoC": 130, "memory": 95, "display": 85, "cameras": 65, "rf": 40, "power": 25, "mech": 55, "other": 60}
bom5 = sum(parts5.values())
cogs5 = bom5 + 45
v.check("Ex 27-01.5a", bom5)
v.check("Ex 27-01.5a1", cogs5)
v.check("Ex 27-01.5a2", 100 * (950 - cogs5) / 950)
v.check("Ex 27-01.5b", 100 * 130 / bom5)
v.check("Ex 27-01.5b1", 100 * 95 / bom5)
v.check("Ex 27-01.5c", cogs5 + 0.3 * 95)
v.check("Ex 27-01.5c1", 100 * (950 - cogs5 - 0.3 * 95) / 950)
v.check("Ex 27-01.5c2", 100 * 0.3 * 95 / 950)
v.check("Ex 27-01.5d", cogs5 - 13)
v.check("Ex 27-01.5d1", 100 * (950 - cogs5 + 13) / 950)
v.check("Ex 27-01.5d2", 100 * 13 / 950)

# ---------------------------------------------------------------- Example 6 (shadow price)
perf = lambda p_dyn: p_dyn ** (1 / 3)  # noqa: E731
v.check("Ex 27-01.6a", 100 * (perf(3.3) / perf(3.0) - 1))
h = 1e-6
dlog = (math.log(perf(3.0 + h)) - math.log(perf(3.0 - h))) / (2 * h)
v.check("Ex 27-01.6a1", dlog)
v.check("Ex 27-01.6a2", 100 * dlog)
v.check("Ex 27-01.6a3", 100 * 0.3 * dlog)
v.check("Ex 27-01.6b", (1 / 1.2) ** (1 / 3))
v.check("Ex 27-01.6b1", sb.perf_under_cap(3.0, 3.0, 1.15, 1.2))
v.check("Ex 27-01.6b2", 100 * (1.15 * (1 / 1.2) ** (1 / 3) - 1))
v.check("Ex 27-01.6c", 1.15 ** 3)

# ---------------------------------------------------------------- Txt
v.check("Txt 27-01.1", 1.2 ** (1 / 3))
v.check("Txt 27-01.2", 1.4 ** (1 / 3))
v.check("Txt 27-01.3", 1 / (0.6 + 0.4 / 20))
v.check("Txt 27-01.4", 1 / 0.6)
v.check("Txt 27-01.5", 0.9 * 0.9)
v.check("Txt 27-01.6", 0.92 * 0.88)
v.check("Txt 27-01.7", pipeline_by_simulation([100, 30, 40]))
v.check("Txt 27-01.8", 200 * 0.015)

# ---------------------------------------------------------------- Problems
ldo1 = 1.8 / 3.85
_, l1, b1 = tree_by_energy([("core", 2.0, 0.90), ("io", 0.3, ldo1)])
v.check("27-01.1a", 100 * ldo1)
v.check("27-01.1b", 2.0 + l1["core"])
v.check("27-01.1b1", 0.3 + l1["io"])
v.check("27-01.1b2", b1)
v.check("27-01.1c", 100 * 2.3 / b1)
v.check("27-01.1c1", b1 - 2.3)
v.check("27-01.1c2", l1["io"])

avg = lambda a, s_: 0.1 * a + 0.9 * s_  # noqa: E731
v.check("27-01.3a", avg(3.0, 0.25))
v.check("27-01.3a1", 13.5 / avg(3.0, 0.25))
v.check("27-01.3b", avg(3.0, 0.125))
v.check("27-01.3b1", 13.5 / avg(3.0, 0.125))
v.check("27-01.3b2", avg(1.5, 0.25))
v.check("27-01.3b3", 13.5 / avg(1.5, 0.25))
v.check("27-01.3c", 0.1 * 3.0)
v.check("27-01.3c1", 0.9 * 0.25)

v.check("27-01.4", (100 - 35) / 2.6)
v.check("27-01.4a", (100 - 35) / 6.5)
v.check("27-01.4b", 6.5 / 2.6)

v.check("27-01.5a", 5.0 * 45)
v.check("27-01.5a1", 25 + 1.0 * 5.0)
v.check("27-01.5b", 25 + 6.0 * 5.0)
v.check("27-01.5b1", burst_by_stepping(30.0, 42.0, 25.0, 6.0, 5.0, 45.0))
v.check("27-01.5c", (42 - 25) / 5.0)

v.check("27-01.6a", 40e12 / 64e9)
v.check("27-01.6b", min(40e12, 900 * 64e9) / 1e12)
v.check("27-01.6c", min(40e12, 2 * 64e9) / 1e9)
v.check("27-01.6c1", 100 * 2 * 64e9 / 40e12)
v.check("27-01.6d0", 3e9 * 0.5 / 1e9)
v.check("27-01.6d", 64e9 / (3e9 * 0.5))

v.check("27-01.7a0", 70e9 * 1 / 1e9)
v.check("27-01.7a", 3.2e12 / 70e9)
v.check("27-01.7b", (400e12 / 3.2e12) / 2)
v.check("27-01.7b1", next(b for b in range(1, 1000) if 2 * b >= 125))

pkt_rate = 8e9 / (1500 * 8)
v.check("27-01.8a", pipeline_by_simulation([10, 8, 12, 9]))
v.check("27-01.8b", pkt_rate)
v.check("27-01.8c", pkt_rate * 0.002)
v.check("27-01.8c1", 8e9 * 0.002 / 8 / 1e6)

parts9 = [18, 6, 22, 12, 4, 9, 15, 10]
bom9 = sum(parts9)
v.check("27-01.9a", bom9)
v.check("27-01.9a1", bom9 + 14)
v.check("27-01.9a2", 100 * (249 - bom9 - 14) / 249)
v.check("27-01.9b", 100 * 22 / bom9)
v.check("27-01.9c", 0.40 * 249)
v.check("27-01.9c1", bom9 + 14 - 0.40 * 249)

time10 = lambda parts: sum(f / s_ for f, s_ in parts)  # noqa: E731
v.check("27-01.10a", 1 / time10([(0.6, 1), (0.4, 20)]))
v.check("27-01.10b", 1 / time10([(0.6, 1), (0.4, 1e12)]))
v.check("27-01.10c", 1 / time10([(0.6, 1.25), (0.4, 20)]))

v.check("27-01.11b", 1.4 ** (1 / 3))
v.check("27-01.11b1", 1.10 / 1.4 ** (1 / 3))
v.check("27-01.11b2", 100 * (1 - 1.10 / 1.4 ** (1 / 3)))
v.check("27-01.11c", 1.2 ** (1 / 3))
v.check("27-01.11c1", 1.08 / 1.2 ** (1 / 3))
v.check("27-01.11c2", 100 * (1.08 / 1.2 ** (1 / 3) - 1))

e_op = 1 / 50e12
v.check("27-01.12a", e_op * 1e15)
v.check("27-01.12b", 8 * 3.9)
v.check("27-01.12b1", 8 * 3.9e-12 / e_op)

# ---------------------------------------------------------------- Lab
better = [row if row[0] != "display" else ("display", 1.2, 0.92) for row in loads1]
_, _, e_better = tree_by_energy(better)
v.check("Lab 27-01.a", e_better)
v.check("Lab 27-01.a1", usable / e_better)
v.check("Lab 27-01.a2", 60 * (usable / e_better - usable / e_batt))
v.check("Lab 27-01.a3", e_batt - e_better)
v.check("Lab 27-01.b", burst_by_stepping(33.0, 43.0, 25.0, 12.0, 4.0, 60.0))
v.check("Lab 27-01.b1", (43 - 25) / 4.0)
v.check("Lab 27-01.c", 400e12 / 3.2e12)
v.check("Lab 27-01.d", 100 * ((4.0 / 3.0) ** (1 / 3) - 1))
v.check("Lab 27-01.d1", 100 * dlog)

# Problem 27-01.13: budget tree arithmetic and the shadow price by numerical differentiation
pb13 = 0.9 * 20 / 4
pl13 = pb13 * 0.88
soc13 = pl13 * 0.9 - (1.2 + 0.4 + 0.2 + 0.15 + 0.25)
pd13 = soc13 - 0.3
v.check("27-01.13a", pb13)
v.check("27-01.13b", pl13)
v.check("27-01.13c", 0.1 * pl13)
v.check("27-01.13d", soc13)
v.check("27-01.13e", pd13)
hh = 1e-6
price = (math.log((pd13 + hh) ** (1 / 3)) - math.log((pd13 - hh) ** (1 / 3))) / (2 * hh)
v.check("27-01.13f", 100 * price)
v.check("27-01.13g", 100 * price * 0.1)
v.check("27-01.13h", 100 * (((pd13 + 0.1) / pd13) ** (1 / 3) - 1))

# Problem 27-01.14: integrate the thermal ODE to the surface limit
from scipy.integrate import solve_ivp  # noqa: E402

hit = lambda t, y: y[0] - 43.0  # noqa: E731
hit.terminal = True
s14 = solve_ivp(lambda t, y: [(30.0 - (y[0] - 25.0) / 4.0) / 60.0], (0, 1000), [33.0], events=hit,
                rtol=1e-11, atol=1e-11)
tb14 = s14.t_events[0][0]
v.check("27-01.14a", 25 + 30 * 4.0)
v.check("27-01.14b", 4.0 * 60)
v.check("27-01.14c", tb14)
v.check("27-01.14d", 60 * 10 / 30)
v.check("27-01.14e", 100 * (1 - 20.0 / tb14))

sys.exit(v.finish())
