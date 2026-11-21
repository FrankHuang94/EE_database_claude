#!/usr/bin/env python3
"""Verify every number in chapter 18-07 (RTOS concepts), its problems and its lab.

Independent routes:
- utilization bounds by direct arithmetic; the two-task bound by minimizing (1 + f^2)/(1 + f) numerically and by a
  brute-force search over integer task sets;
- response times by a separate implementation of the fixed-priority recurrence written here (not the lab's), and
  cross-checked against the lab's;
- every schedule (RM, EDF, the inversion timelines, blocking phasing) by the lab's discrete-time kernel simulator,
  with the expected timelines written out as strings;
- queues, stacks, overheads and latencies by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import rtsched as rs  # noqa: E402

v = Verifier.from_files("18-07", ROOT / "chapters" / "18-07-rtos-concepts.md",
                        ROOT / "solutions" / "18-07-solutions.md", LAB / "README.md")


def rta(tasks, i, blocking=0.0):
    """tasks: list of (C, T, prio) with higher prio = more urgent. Returns R_i or None if R_i > T_i."""
    c, t, p = tasks[i]
    hp = [(cj, tj) for cj, tj, pj in tasks if pj > p]
    r = c + blocking
    for _ in range(10000):
        nxt = c + blocking + sum(math.ceil(r / tj - 1e-12) * cj for cj, tj in hp)
        if abs(nxt - r) < 1e-12:
            return r
        if nxt > t + 1e-12:
            return None
        r = nxt
    raise RuntimeError("no convergence")


def rm(ct):
    order = sorted(range(len(ct)), key=lambda k: ct[k][1])
    prio = {k: len(ct) - rank for rank, k in enumerate(order)}
    return [(c, t, prio[k]) for k, (c, t) in enumerate(ct)]


def trace(res):
    return "".join((x or ".")[0] for x in res.trace).rstrip(".")


def ll(n):
    return n * (2 ** (1 / n) - 1)


# ---------------------------------------------------------------- text and the two-task derivation
v.check("Txt 18-07.a", ll(2))
v.check("Txt 18-07.b", ll(3))
v.check("Txt 18-07.c", math.log(2))
v.assert_true("bound tends to ln 2", abs(ll(10 ** 6) - math.log(2)) < 1e-6)
opt = minimize_scalar(lambda f: (1 + f * f) / (1 + f), bounds=(0, 1), method="bounded", options={"xatol": 1e-12})
v.assert_true("U(f) minimized at f = sqrt(2) - 1 with value 2(sqrt2 - 1)",
              abs(opt.x - (math.sqrt(2) - 1)) < 1e-6 and abs(opt.fun - ll(2)) < 1e-12)
v.assert_true("case formulas agree at C1 = T2 - T1", all(
    abs((1 + f - 2 * f / (1 + f)) - (1 / (1 + f) + f * (1 - 1 / (1 + f)))) < 1e-12 for f in (0.1, 0.4, 0.9)))

# ---------------------------------------------------------------- Example 1
v.check("Ex 18-07.1a", 100 * (1000 * 3e-6 + 400 * 2.5e-6))
v.check("Ex 18-07.1b", 100 * (10000 * 3e-6 + 400 * 2.5e-6))

# ---------------------------------------------------------------- Example 2
ex2 = rm([(1, 4), (2, 6), (3, 12)])
u2 = sum(c / t for c, t, _ in ex2)
v.check("Ex 18-07.2a", u2)
v.check("Ex 18-07.2b", ll(3))
v.check("Ex 18-07.2c", math.prod(c / t + 1 for c, t, _ in ex2))
r2 = [rta(ex2, i) for i in range(3)]
v.check("Ex 18-07.2d", r2[0])
v.check("Ex 18-07.2e", r2[1])
v.check("Ex 18-07.2f", r2[2])
T2 = rs.rm_priorities([rs.Task("A", 4, [(1, None)]), rs.Task("B", 6, [(2, None)]), rs.Task("C", 12, [(3, None)])])
sim2 = rs.simulate(T2, 240)
v.assert_true("simulation over 20 hyperperiods observes the same worst cases",
              [sim2.worst(n) for n in "ABC"] == r2 and not any(sim2.misses.values()))
v.assert_true("lab response_time agrees", [rs.response_time(T2, i) for i in range(3)] == r2)

# ---------------------------------------------------------------- Example 3
ex3 = rm([(2, 5), (4, 7)])
v.check("Ex 18-07.3a", 2 / 5 + 4 / 7)
v.assert_true("RM: B's response exceeds 7", rta(ex3, 1) is None)
T3 = rs.rm_priorities([rs.Task("A", 5, [(2, None)]), rs.Task("B", 7, [(4, None)])])
rm3 = rs.simulate(T3, 350)
v.check("Ex 18-07.3b", rm3.misses["B"])
v.assert_true("10 hyperperiods hold 50 of B's jobs; first finishes at 8", len(rm3.response["B"]) >= 49
              and rm3.response["B"][0] == 8 and 350 == 10 * 35)
edf3 = rs.simulate(T3, 350, policy="edf")
v.assert_true("EDF misses nothing", not any(edf3.misses.values()))
v.check("Ex 18-07.3c", edf3.worst("A"))
v.check("Ex 18-07.3d", edf3.worst("B"))
v.assert_true("RM worst response of A is 2", rm3.worst("A") == 2)


# ---------------------------------------------------------------- Example 4 (inversion)
def ex4(m=10):
    return [rs.Task("L", 100, [(1, None), (4, "S"), (1, None)], priority=1, offset=0, max_jobs=1),
            rs.Task("M", 100, [(m, None)], priority=2, offset=3, max_jobs=1),
            rs.Task("H", 100, [(1, None), (1, "S"), (1, None)], priority=3, offset=2, max_jobs=1)]


none4, inh4, ceil4 = (rs.simulate(ex4(), 40, protocol=p) for p in ("none", "inherit", "ceiling"))
v.assert_true("no-protocol timeline", trace(none4) == "LLHMMMMMMMMMMLLLHHL", trace(none4))
v.assert_true("inheritance timeline", trace(inh4) == "LLHLLLHHMMMMMMMMMML", trace(inh4))
v.assert_true("ceiling timeline", trace(ceil4) == "LLLLLHHHMMMMMMMMMML", trace(ceil4))
v.check("Ex 18-07.4a", none4.worst("H"))
v.check("Ex 18-07.4b", inh4.worst("H"))
v.check("Ex 18-07.4c", ceil4.worst("H"))
v.check("Ex 18-07.4d", 4)
v.assert_true("blocking bound from the lab agrees", rs.blocking_ceiling(ex4(), 2) == 4)
v.check("Ex 18-07.4e", 3 + 4)
v.assert_true("M of 100 ms makes H wait over 100 ms", rs.simulate(ex4(100), 200).worst("H") > 100)

# ---------------------------------------------------------------- Examples 5 and 6
v.check("Ex 18-07.5a", math.floor(45 / 10) + 1)
v.check("Ex 18-07.5b", 5 * 24)
v.check("Ex 18-07.5c", math.floor(50 / 10) + 1)
v.assert_true("queue simulation: 5 for 45 ms, 6 for 50 ms", rs.queue_max_occupancy(10, 200, [(30, 45)]) == 5
              and rs.queue_max_occupancy(10, 200, [(30, 50)]) == 6)
ram = sum([512, 512, 1024, 1024, 2048, 768, 256]) + 7 * 92
v.check("Ex 18-07.6a", ram)
v.check("Ex 18-07.6b", 100 * ram / 32768)
v.check("Ex 18-07.6c", ram - 2048)

# ---------------------------------------------------------------- Problem 1
p1 = rm([(2, 10), (3, 15), (5, 30), (4, 40)])
v.check("18-07.1a", sum(c / t for c, t, _ in p1))
v.check("18-07.1b", ll(4))
v.assert_true("U under the bound; exact analysis agrees", sum(c / t for c, t, _ in p1) <= ll(4)
              and all(rta(p1, i) is not None for i in range(4)))

# ---------------------------------------------------------------- Problem 2
v.check("18-07.2a", 100 * (1000 * 4e-6 + 1500 * 2e-6))
v.check("18-07.2b", 2e-6 * 64e6)
v.check("18-07.2c", 5 - 1)
v.check("18-07.2d", 5)

# ---------------------------------------------------------------- Problem 4
p4 = rm([(1, 5), (2, 8), (4, 20), (5, 40)])
v.check("18-07.4a", sum(c / t for c, t, _ in p4))
T4 = rs.rm_priorities([rs.Task("t1", 5, [(1, None)]), rs.Task("t2", 8, [(1, None), (1, "S")]),
                       rs.Task("t3", 20, [(4, None)]), rs.Task("t4", 40, [(3, None), (2, "S")])])
b4 = [rs.blocking_ceiling(T4, i) for i in range(4)]
v.assert_true("blocking terms 0, 2, 2, 0", b4 == [0, 2, 2, 0], str(b4))
v.check("18-07.4b", b4[1])
v.check("18-07.4c", b4[2])
r4 = [rta(p4, i, b4[i]) for i in range(4)]
for ident, val in zip(("18-07.4d", "18-07.4e", "18-07.4f", "18-07.4g"), r4):
    v.check(ident, val)
v.assert_true("lab response_time agrees", [rs.response_time(T4, i, b4[i]) for i in range(4)] == r4)
s4 = rs.simulate(T4, 400, protocol="ceiling")
v.check("18-07.4h", s4.worst("t2"))
v.check("18-07.4i", s4.worst("t3"))
# with a phasing that puts t4 inside its section when t2 and t1 release, the blocking appears
T4b = rs.rm_priorities([rs.Task("t1", 5, [(1, None)], offset=4), rs.Task("t2", 8, [(1, None), (1, "S")], offset=4),
                        rs.Task("t3", 20, [(4, None)], offset=40), rs.Task("t4", 40, [(3, None), (2, "S")])])
s4b = rs.simulate(T4b, 80, protocol="ceiling")
v.assert_true("an adversarial phasing shows blocking: t2 grows from 3 to 4, within R_2 = 5 (5 needs release an "
              "instant after t4 locks S, between integer steps)", s4b.worst("t2") == 4 and s4b.worst("t2") <= r4[1],
              str(s4b.worst("t2")))

# ---------------------------------------------------------------- Problem 5
c2 = max(10 - 4, 14 - 2 * 4)
v.check("18-07.5a", c2)
v.assert_true("R_2 = 10 at C_2 = 6", rta(rm([(4, 10), (c2, 14)]), 1) == 10 and rta(rm([(4, 10), (c2 + 1, 14)]), 1) is None)
v.check("18-07.5b", 4 / 10 + c2 / 14)
v.check("18-07.5c", ll(2))
v.assert_true("U(0.4) = 1.16/1.4", abs((1 + 0.16) / 1.4 - (0.4 + 6 / 14)) < 1e-12)

# ---------------------------------------------------------------- Problem 6
p6 = rm([(1, 3), (2, 5), (2, 8)])
v.check("18-07.6a", sum(c / t for c, t, _ in p6))
v.assert_true("RM fails for the third task", rta(p6, 2) is None and rta(p6, 1) == 3)
T6 = rs.rm_priorities([rs.Task("x", 3, [(1, None)]), rs.Task("y", 5, [(2, None)]), rs.Task("z", 8, [(2, None)])])
rm6 = rs.simulate(T6, 1200)
v.check("18-07.6b", sum(rm6.misses.values()))
v.assert_true("all RM misses are the third task's; 1200 = 10 hyperperiods",
              rm6.misses["z"] == sum(rm6.misses.values()) and 1200 == 10 * math.lcm(3, 5, 8))
edf6 = rs.simulate(T6, 1200, policy="edf")
v.assert_true("EDF misses nothing", not any(edf6.misses.values()))
v.check("18-07.6c", edf6.worst("x"))
v.check("18-07.6d", edf6.worst("y"))
v.check("18-07.6e", edf6.worst("z"))


# ---------------------------------------------------------------- Problem 7
def p7():
    return [rs.Task("L", 100, [(3, "S"), (1, None)], priority=1, offset=0, max_jobs=1),
            rs.Task("1", 100, [(5, None)], priority=2, offset=2, max_jobs=1),
            rs.Task("2", 100, [(4, None)], priority=3, offset=3, max_jobs=1),
            rs.Task("H", 100, [(1, "S"), (2, None)], priority=4, offset=1, max_jobs=1)]


n7, i7 = rs.simulate(p7(), 40), rs.simulate(p7(), 40, protocol="inherit")
v.assert_true("timeline without a protocol", trace(n7) == "LL122221111LHHHL", trace(n7))
v.check("18-07.7a", n7.worst("H"))
v.check("18-07.7b", i7.worst("H"))
v.check("18-07.7c", 3 + 3)

# ---------------------------------------------------------------- Problems 8 to 10
v.check("18-07.8a", 115200 / 10 * 0.012)
v.check("18-07.8b", math.floor(115200 / 10 * 0.012) + 1)
stack = 640 + 26 * 4 + 8 * 4 + 16 * 4
v.check("18-07.9a", stack)
alloc = math.ceil(stack * 1.25 / 8) * 8
v.check("18-07.9b", alloc)
v.check("18-07.9c", 5 * alloc)
v.check("18-07.10a", 0.5 + 8 + 25 + 2)
v.check("18-07.10b", 0.4 + 1.0 + 0.3)

# ---------------------------------------------------------------- Problem 11 (in units of 0.1 ms)
p11 = rm([(20, 75), (15, 100), (60, 400), (100, 1000)])
v.check("18-07.11a", sum(c / t for c, t, _ in p11))
v.check("18-07.11b", ll(4))
b11 = [0, 30, 0, 0]
r11 = [rta(p11, i, b11[i]) for i in range(4)]
for ident, val in zip(("18-07.11c", "18-07.11d", "18-07.11e", "18-07.11f"), r11):
    v.check(ident, val / 10)
T11 = rs.rm_priorities([rs.Task("BLE", 75, [(20, None)]), rs.Task("IMU", 100, [(3, None), (12, "I2C")]),
                        rs.Task("PPG", 400, [(30, "I2C"), (30, None)]), rs.Task("UI", 1000, [(100, None)])])
v.assert_true("lab blocking terms are 0, 30, 0, 0", [rs.blocking_ceiling(T11, i) for i in range(4)] == b11)
s11 = rs.simulate(T11, 6000, protocol="ceiling")
v.assert_true("simulated worst cases do not exceed the analysis; no misses",
              all(s11.worst(n) <= r / 1 for n, r in zip(("BLE", "IMU", "PPG", "UI"), r11)) and not any(s11.misses.values()))
v.check("18-07.11g", rta(rm([(20, 75)]), 0, 30) / 10)
v.assert_true("only the mutex design meets a 3 ms BLE deadline", r11[0] / 10 <= 3 < rta(rm([(20, 75)]), 0, 30) / 10)

# ---------------------------------------------------------------- lab
u_min, ratio = rs.two_task_min_utilization(1000)
v.check("Lab 18-07.a", u_min)
v.check("Lab 18-07.b", ratio)
brute = min(c1 / 100 + max(100 - c1, t2 - 2 * c1) / t2 for t2 in range(101, 200) for c1 in range(1, 100)
            if max(100 - c1, t2 - 2 * c1) > 0)
v.assert_true("brute force at T1 = 100 lands within 1e-4 of the bound", abs(brute - ll(2)) < 1e-4)
v.check("Lab 18-07.c", 7)
v.assert_true("B's first job finishes at 8, after its deadline at 7", rm3.response["B"][0] == 8)
v.check("Lab 18-07.d", rs.simulate(ex4(20), 80).worst("H"))
v.check("Lab 18-07.e", rs.simulate(ex4(20), 80, protocol="inherit").worst("H"))
v.assert_true("no-protocol response is 6 + m for m = 1, 5, 20",
              [rs.simulate(ex4(m), 80).worst("H") for m in (1, 5, 20)] == [7, 11, 26])
v.check("Lab 18-07.f", rs.queue_max_occupancy(10, 200, [(30, 45)]))
v.check("Lab 18-07.g", rs.queue_max_occupancy(10, 200, [(30, 50)]))
v.assert_true("stall starting one unit after an arrival: 4", rs.queue_max_occupancy(10, 200, [(31, 45)]) == 4)
a08, a09 = rs.acceptance(rs.random_task_sets(2000, 3, 0.80)), rs.acceptance(rs.random_task_sets(2000, 3, 0.90))
v.assert_true("U = 0.80: LL none, hyperbolic about 70%, exact all",
              a08[0] == 0 and 0.65 < a08[1] < 0.77 and a08[2] == 1.0, str(a08))
v.assert_true("U = 0.90: LL none, hyperbolic about 5%, exact about 75%",
              a09[0] == 0 and 0.03 < a09[1] < 0.08 and 0.70 < a09[2] < 0.80, str(a09))
over = rs.rm_priorities([rs.Task("A", 5, [(2, None)]), rs.Task("B", 7, [(5, None)])])
eo, ro = rs.simulate(over, 350, policy="edf"), rs.simulate(over, 350)
v.assert_true("overload: EDF misses both tasks, RM only B",
              eo.misses["A"] > 0 and eo.misses["B"] > 0 and ro.misses["A"] == 0 and ro.misses["B"] > 0)
v.assert_true("hyperbolic product at equal shares equals 2 at the LL bound",
              abs((ll(3) / 3 + 1) ** 3 - 2) < 1e-12)

v.assert_true("lab Part 3: B's WCET at 5 gives U = 1.11", round(2 / 5 + 5 / 7, 2) == 1.11)
ceil_m = [rs.simulate(ex4(m), 60, protocol="ceiling").worst("H") for m in (1, 5, 20)]
inh_m = [rs.simulate(ex4(m), 60, protocol="inherit").worst("H") for m in (1, 5, 20)]
v.assert_true("lab Part 4: with inheritance or ceiling H's response stays at 6 for m = 1, 5, 20", ceil_m == [6, 6, 6] and inh_m == [6, 6, 6], f"{ceil_m} {inh_m}")
v.assert_true("response_time returns None when C + B already exceeds the deadline",
              rs.response_time([rs.Task("X", 4, [(3, None)])], 0, blocking=2) is None)
sys.exit(v.finish())
