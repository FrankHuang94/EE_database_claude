#!/usr/bin/env python3
"""Verify every number in chapter 27-06 (automotive E/E architecture and ADAS compute),
its problems and its lab.

Independent routes (the lab module uses closed forms):
- CAN frame lengths by building the worst-case bit pattern and stuffing it bit by bit;
- response times by simulating the bus event by event (critical instant, non-preemptive
  fixed priority) rather than by the analytic iteration;
- wiring lengths by explicit enumeration of endpoints; stopping distance by integrating motion;
- range loss, TOPS and FIT by direct arithmetic on the definitions.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy import integrate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import automodel as am  # noqa: E402

v = Verifier.from_files("27-06", ROOT / "chapters" / "27-06-automotive-ee-architecture.md",
                        ROOT / "solutions" / "27-06-solutions.md", LAB / "README.md")


def stuffed_length(n_bytes, worst=True):
    """Stuff a worst-case bit pattern bit by bit: each data bit repeats the last bit on
    the wire (including stuff bits), which forces a stuff bit after the first five and
    after every four thereafter. Stuffing covers the 34 + 8n bits from start-of-frame
    to the end of the CRC; 13 trailing bits are not stuffed."""
    n_region = 34 + 8 * n_bytes
    if not worst:
        return n_region + 13
    wire, last, run = 0, 0, 0
    for k in range(n_region):
        bit = last if k > 0 else 0
        wire += 1
        run = run + 1 if (k > 0 and bit == last) else 1
        last = bit
        if run == 5:
            wire += 1
            last = 1 - bit
            run = 1
    return wire + 13


def frame_ms(n, kbps):
    return stuffed_length(n) / (kbps * 1e3) * 1e3


def simulate_response(index, msgs, kbps, horizon_factor=3):
    """Event simulation of a non-preemptive fixed-priority bus from a critical instant:
    the message under test and all higher-priority messages are queued at t = 0, just
    after the longest lower-priority frame has started (blocking); return when the
    message under test finishes. Arbitration happens only when the bus is idle."""
    c = [frame_ms(n, kbps) for n, _ in msgs]
    t_per = [p for _, p in msgs]
    tau = 1.0 / (kbps * 1e3) * 1e3
    lower = c[index + 1:]
    bus_free = max(lower) if lower else 0.0
    # pending releases for higher-priority messages and the message itself
    next_release = {j: 0.0 for j in range(index + 1)}
    queue = set(range(index + 1))
    t = bus_free
    while True:
        # release any jobs whose time has come (a message released within one bit time of
        # the bus going idle still competes in that arbitration)
        for j in range(index + 1):
            while next_release[j] + t_per[j] <= t + tau and j != index:
                next_release[j] += t_per[j]
                queue.add(j)
        if not queue:
            t = min(next_release[j] + t_per[j] for j in range(index)) - tau
            continue
        winner = min(queue)
        queue.discard(winner)
        t += c[winner]
        if winner == index:
            return t


# ---------------------------------------------------------------------------
# Example 27-06.1
# ---------------------------------------------------------------------------
v.check("Ex 27-06.1a", stuffed_length(8))
v.check("Ex 27-06.1a0", stuffed_length(8, worst=False))
v.check("Ex 27-06.1a2", stuffed_length(8) - stuffed_length(8, worst=False))
v.check("Ex 27-06.1a1", 1e3 * frame_ms(8, 500))
v.check("Ex 27-06.1a3", 100 * 64 / stuffed_length(8))
MSGS = [(8, 5), (8, 5), (8, 10), (8, 10), (8, 10), (4, 20), (8, 20), (8, 20), (2, 50), (8, 50),
        (8, 100), (8, 100)]
for k, br in [("b", 500), ("b1", 250), ("b2", 125)]:
    v.check(f"Ex 27-06.1{k}", 100 * sum(frame_ms(n, br) / p for n, p in MSGS))
v.check("Ex 27-06.1c", simulate_response(0, MSGS, 500))
r500 = simulate_response(11, MSGS, 500)
r125 = simulate_response(11, MSGS, 125)
v.check("Ex 27-06.1c1", r500)
v.check("Ex 27-06.1c2", simulate_response(11, MSGS, 250))
v.check("Ex 27-06.1c3", r125)
v.check("Ex 27-06.1c4", r125 / r500)
def rta_chain(index, msgs, kbps, extra_ms=0.0):
    """Our own response-time iteration, returning every queuing-time pass; extra_ms adds
    a fixed error-recovery overhead inside the queuing time."""
    c = [frame_ms(n, kbps) for n, _ in msgs]
    t_per = [p for _, p in msgs]
    tau = 1.0 / kbps
    b = max(c[index + 1:]) if c[index + 1:] else 0.0
    w, chain = b, [b]
    while True:
        wn = b + extra_ms + sum(math.ceil((w + tau) / t_per[j] - 1e-12) * c[j] for j in range(index))
        chain.append(wn)
        if abs(wn - w) < 1e-12 or wn > 1e4:
            return chain, wn + c[index]
        w = wn


def busy_period(index, msgs, kbps):
    c = [frame_ms(n, kbps) for n, _ in msgs]
    t_per = [p for _, p in msgs]
    b = max(c[index + 1:]) if c[index + 1:] else 0.0
    t, chain = c[index], []
    while True:
        tn = b + sum(math.ceil(t / t_per[j] - 1e-12) * c[j] for j in range(index + 1))
        chain.append(tn)
        if abs(tn - t) < 1e-12:
            return chain, tn
        t = tn


per_group = {}
for n, p in MSGS:
    per_group[p] = per_group.get(p, 0.0) + frame_ms(n, 500) / p
for k, p in [("b3", 5), ("b4", 10), ("b5", 20), ("b6", 50), ("b7", 100)]:
    v.check(f"Ex 27-06.1{k}", 100 * per_group[p])
v.check("Ex 27-06.1t", 1e3 / 125)
for k, n in [("t1", 8), ("t2", 4), ("t3", 2)]:
    v.check(f"Ex 27-06.1{k}", frame_ms(n, 125))
chain125, rr125 = rta_chain(11, MSGS, 125)
for k in range(1, 7):
    v.check(f"Ex 27-06.1w{k}", chain125[k])
v.check("Ex 27-06.1w7", chain125[-1])
v.assert_true("hand iteration matches the simulated 125 kb/s response", abs(rr125 - r125) < 1e-9)
err = 31 / 125 + frame_ms(8, 125)  # 31 bit times of error signalling plus one 8-byte retransmission
for k, ne in [("e1", 1), ("e3", 3), ("e4", 4)]:
    v.check(f"Ex 27-06.1{k}", rta_chain(11, MSGS, 125, ne * err)[1])
mm2 = MSGS + [(8, 100)] * 2
v.check("Ex 27-06.1m2", rta_chain(13, mm2, 125)[1])
v.assert_true("four more 100 ms messages push the 125 kb/s load past 100%",
              sum(frame_ms(n, 125) / p for n, p in MSGS + [(8, 100)] * 4) > 1)
_, bp125 = busy_period(11, MSGS, 125)
v.check("Txt 27-06.5", bp125)
v.assert_true("busy period at 125 kb/s is within the 100 ms period", bp125 <= 100)
v.assert_true("analytic response iteration agrees with simulation",
              all(abs(am.can_response_time_ms(i, MSGS, br) - simulate_response(i, MSGS, br)) < 1e-9
                  for i in range(len(MSGS)) for br in (500, 250, 125)))

# ---------------------------------------------------------------------------
# Example 27-06.2 to 27-06.4
# ---------------------------------------------------------------------------
cam = 8e6 * 30 * 12 / 1e9
v.check("Ex 27-06.2a", cam)
v.check("Ex 27-06.2a1", 8 * cam)
v.check("Ex 27-06.2b", 5 * 20e6 / 1e9)
lid = 2.0e6 * 16 * 8 / 1e9
v.check("Ex 27-06.2b1", lid)
tot = 8 * cam + 0.1 + lid
v.check("Ex 27-06.2c", tot)
v.check("Ex 27-06.2c1", 100 * 8 * cam / tot)
v.check("Ex 27-06.2d", 8 * cam / (0.1 + lid))
v.check("Ex 27-06.2d1", cam / 0.020)
v.check("Ex 27-06.2d2", cam / lid)
sus = 8 * 30 * 80e9 / 1e12
v.check("Ex 27-06.3a", sus)
v.check("Ex 27-06.3b", sus / 0.30)
v.check("Ex 27-06.3c", 2 * sus / 0.30)
v.check("Ex 27-06.3d", 2 * sus / 0.30 / 2.5)
pu, ph = 150 * 50, 180 * 110
v.check("Ex 27-06.4a", pu / 1e3)
v.check("Ex 27-06.4a1", ph / 1e3)
for k, pc, pd in [("b", 500, pu), ("b1", 500, ph), ("c", 100, pu), ("c1", 100, ph)]:
    # range with and without the load: R = E/(Pd + Pc) * v, so the loss is 1 - Pd/(Pd + Pc)
    v.check(f"Ex 27-06.4{k}", 100 * (1 - pd / (pd + pc)))

# ---------------------------------------------------------------------------
# Example 27-06.5: enumerate the layout
# ---------------------------------------------------------------------------
off = [(dx, dy) for dx in (-0.2, 0.0, 0.2) for dy in (-0.15, 0.15)]
offs = off + [(dx * 0.5, dy * 2) for dx, dy in off]
clusters = [(0.5, 0.3), (0.5, 1.5), (4.0, 0.3), (4.0, 1.5)]
eps = [(cx + dx, cy + dy) for cx, cy in clusters for dx, dy in offs]
ecus = [(1.5, 0.9), (2.0, 0.9), (2.5, 0.9)]
dom = 0.0
for i, (x, y) in enumerate(eps):
    ex, ey = ecus[i % 3]
    dom += abs(x - ex) + abs(y - ey)
v.check("Ex 27-06.5a", dom)
loc = 0.0
for k, (cx, cy) in enumerate(clusters):
    for x, y in eps[12 * k:12 * (k + 1)]:
        loc += abs(x - cx) + abs(y - cy)
bb = sum(abs(cx - 2.25) + abs(cy - 0.9) for cx, cy in clusters)
v.check("Ex 27-06.5b", loc)
v.check("Ex 27-06.5b1", bb)
v.check("Ex 27-06.5b2", loc + bb)
v.check("Ex 27-06.5c", 100 * (1 - (loc + bb) / dom))
front = eps[:12]
rear = eps[24:36]
v.check("Ex 27-06.5d", sum(abs(x - ecus[i % 3][0]) for i, (x, _) in enumerate(front)))
v.check("Ex 27-06.5d1", sum(abs(x - ecus[i % 3][0]) for i, (x, _) in enumerate(rear)))
v.check("Ex 27-06.5d2", sum(abs(y - 0.9) for _, y in front))
v.check("Ex 27-06.5d3", sum(abs(x - 0.5) + abs(y - 0.3) for x, y in front))
v.check("Ex 27-06.5d4", abs(0.5 - 2.25) + abs(0.3 - 0.9))
v.assert_true("domain wiring does not depend on which controller each endpoint gets",
              all(abs(sum(abs(x - ecus[(i + s) % 3][0]) + abs(y - 0.9) for i, (x, y) in enumerate(eps)) - dom)
                  < 1e-9 for s in range(3)))

# ---------------------------------------------------------------------------
# Example 27-06.6: integrate the motion
# ---------------------------------------------------------------------------


def stop_dist(kmh, latency, decel):
    v0 = kmh / 3.6
    t_brake = v0 / decel
    d1, _ = integrate.quad(lambda t: v0, 0, latency)
    d2, _ = integrate.quad(lambda t: v0 - decel * t, 0, t_brake)
    return d1 + d2, d1, d2


d100, r100, brk = stop_dist(130, 0.1, 8)
d300, _, _ = stop_dist(130, 0.3, 8)
v.check("Ex 27-06.6v", 130 / 3.6)
v.check("Ex 27-06.6a", r100)
v.check("Ex 27-06.6b0", brk)
v.check("Ex 27-06.6b", d100)
v.check("Ex 27-06.6b1", d300)
v.check("Ex 27-06.6b2", d300 - d100)
v.check("Ex 27-06.6c", 100 * (1 - 5 / 600))
v.check("Ex 27-06.6c1", 600 * (1 - 0.99))
v.check("Ex 27-06.6d", 5e6 * 1.5 * 365 * 5 * 1e-9)

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
for k, n in [("a", 0), ("b", 2), ("c", 4), ("d", 8)]:
    v.check(f"27-06.2{k}", stuffed_length(n))
    v.check(f"27-06.2{k}1", stuffed_length(n, worst=False))
    v.check(f"27-06.2{k}2", 1e3 * frame_ms(n, 500))
base = [(8, 10), (8, 20), (4, 20), (8, 50), (8, 100)]
load = sum(frame_ms(n, 500) / p for n, p in base)
v.check("27-06.3a", 100 * load)
per = frame_ms(8, 500) / 10
v.check("27-06.3a1", 100 * per)
v.check("27-06.3a2", (0.5 - load) / per)
k3 = 0
while load + (k3 + 1) * per <= 0.5:
    k3 += 1
v.check("27-06.3b", k3)
v.check("27-06.3c", 100 * (load + k3 * per))
s3 = [(8, 5), (8, 10), (8, 20)]
for k, i in [("a", 0), ("b", 1), ("c", 2)]:
    v.check(f"27-06.4{k}", simulate_response(i, s3, 500))
v.check("27-06.5a", 3e6 * 60 * 12 / 1e9)
v.check("27-06.5b", 3e6 * 60 * 8 / 1e9)
v.check("27-06.6a", 11 * 30 * 50e9 / 1e12)
v.check("27-06.6b", 11 * 30 * 50e9 / 1e12 / 0.25)
v.check("27-06.7", 0.02 * 7500 / 0.98)
d8, _, _ = stop_dist(100, 0.15, 7)
v.check("27-06.8v", 100 / 3.6)
v.check("27-06.8a", 1e3 / (100 / 3.6))
v.check("27-06.8b", d8)
v.check("27-06.9a", 100 * (1 - 3 / 400))
v.check("27-06.9b", 100 * (1 - 2 / 250))
v.check("27-06.9c", 400 * 0.005)
v.check("27-06.9d", 250 * 0.01)
v.check("27-06.9e", 400 * 0.005 + 250 * 0.01)
sec = 3 * 8000 / 20
v.check("27-06.10a", sec)
v.check("27-06.10b", sec / 60)
v.check("27-06.10c", 2e6 * 3 / 1e6)
v.check("27-06.10d", 2e6 * 3 * 0.5 / 1e6)
z3 = [(0.5, 0.9), (4.0, 0.3), (4.0, 1.5)]
loc3 = sum(min(abs(x - zx) + abs(y - zy) for zx, zy in z3) for x, y in eps)
bb3 = sum(abs(zx - 2.25) + abs(zy - 0.9) for zx, zy in z3)
v.check("27-06.11a", loc3)
v.check("27-06.11b", bb3)
v.check("27-06.11c", loc3 + bb3)
arb = 30 / 500e3 * 1e6
dat = (8 * 64 + 30) / 2e6 * 1e6
v.check("27-06.12a1", arb)
v.check("27-06.12a2", dat)
v.check("27-06.12a", arb + dat)
cl = 8 * 1e3 * frame_ms(8, 500)
v.check("27-06.12b", cl)
v.check("27-06.12c", cl / (arb + dat))
cl0 = 8 * stuffed_length(8, worst=False) / 500e3 * 1e6
v.check("27-06.12d", cl0)
v.check("27-06.12e", cl0 / (arb + dat))
v.check("27-06.11d", sum(abs(x - 0.5) for x, _ in eps[:12]))
v.check("27-06.11e", sum(abs(y - 0.9) for _, y in eps[:12]))
v.check("27-06.11f", sum(abs(x - 0.5) + abs(y - 0.9) for x, y in eps[:12]))
for k, n in [("a", 0), ("b", 4), ("c", 8)]:
    stuff = stuffed_length(n) - stuffed_length(n, worst=False)
    v.assert_true(f"stuffing bound floor((N-1)/4) holds for {n} bytes", stuff == (34 + 8 * n - 1) // 4)
    v.check(f"27-06.13{k}", stuff)
v.check("27-06.13d", 100 * 24 / 98)
v.check("27-06.13e", 100 * 24 / stuffed_length(8))
v.check("27-06.14a", 1e3 / 250)
for k, n in [("b", 8), ("c", 4), ("d", 2)]:
    v.check(f"27-06.14{k}", frame_ms(n, 250))
ch250, r250 = rta_chain(11, MSGS, 250)
v.check("27-06.14e", ch250[1])
v.check("27-06.14f", ch250[-1])
v.check("27-06.14g", simulate_response(11, MSGS, 250))
bch, bp250 = busy_period(11, MSGS, 250)
v.check("27-06.14h", bch[0])
v.check("27-06.14i", bp250)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
m2 = MSGS + [(8, 100)]
v.check("Lab 27-06.a", 100 * sum(frame_ms(n, 125) / p for n, p in m2))
v.check("Lab 27-06.a1", simulate_response(12, m2, 125))
nc = 40 / cam
v.check("Lab 27-06.b", nc)
v.check("Lab 27-06.b1", math.floor(nc))
v.check("Lab 27-06.c", 100 * 500 / (500 + 140 * 30))
d5, _, _ = stop_dist(130, 0.5, 8)
v.check("Lab 27-06.d", d5)
v.check("Lab 27-06.d1", d5 - d100)

v.check("Txt 27-06.1", 50 / 3.6 * 0.1)
v.check("Txt 27-06.2", 130 / 3.6 * 0.1)
v.check("Txt 27-06.3", 1e3 * frame_ms(8, 500))
v.check("Txt 27-06.4", cam)

sys.exit(v.finish())
