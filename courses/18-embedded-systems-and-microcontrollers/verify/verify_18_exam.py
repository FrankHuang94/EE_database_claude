#!/usr/bin/env python3
"""Verify every number in the Course 18 final-exam solutions.

Independent routes:
- addresses, masks, linker symbols and the read-modify-write race by integer arithmetic on Python ints, with the
  race replayed as an explicit interleaving;
- wait states by searching for the smallest whole number of clock cycles that covers the flash access time; CPIs by
  the 18-01 lab's cycle-level fetch simulator on synthetic instruction streams, against the first-order model;
- interrupt response times by the 18-03 lab's discrete-event simulator at the critical instant, against the
  recurrence; timer and watchdog figures by searching over prescalers and reloads;
- ping-pong buffers by the 18-04 lab's block simulator (overruns just below and none at the chosen sizes);
- baud rates and I2C rise times from their definitions, the rise time by root finding on the RC step;
- ADC settling by root finding, averaging by Monte Carlo, the multiplexed-input error by the exact charge-sharing
  recursion, and the PWM ripple from the exact steady state of the RC filter;
- RTOS response times and the three priority-inversion timelines by the 18-07 lab's scheduler simulation, queue
  depth by its occupancy simulation;
- the outage probability by Monte Carlo over Poisson power cuts as well as the closed form;
- battery budgets from charge sums, the coin-cell droop by integrating the circuit ODE (ngspice confirms it in
  exam/coin_cell_exam.cir);
- sensor noise by simulated white noise through the complementary filter;
- CPA correlations by measuring them on simulated traces (18-11 lab), PUF repetition lengths by the binomial tail
  and a direct search, and the timing attack's query count by running the lab's attack.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, integrate, signal
from scipy.optimize import brentq
from scipy.stats import binom

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("18-01-lab", "18-03-lab", "18-04-lab", "18-07-lab", "18-11-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import dmasim as dm  # noqa: E402
import hwsec as hs  # noqa: E402
import irqtime as it  # noqa: E402
import mcuarch as ma  # noqa: E402
import rtsched as rs  # noqa: E402

v = Verifier.from_files("18-exam", ROOT / "exam" / "solutions.md")


def ws_search(f, t_acc):
    """Smallest number of wait states WS such that (1 + WS) clock periods cover the access time."""
    ws = 0
    while (1 + ws) / f < t_acc * (1 - 1e-12):
        ws += 1
    return ws


def align4(x):
    return (x + 3) & ~3


# ================================================================ Question 1 (architecture)
v.check("X18.1a", 0x40020C00 + 0x14)
v.assert_true("0x40020C14 is in the peripheral region", ma.region(0x40020C14).lower().startswith("periph"),
              ma.region(0x40020C14))
v.check("X18.1b", 0x20000000 + 192 * 1024 - 1)
t_acc = 40e-9
v.check("X18.1c", ws_search(48e6, t_acc))
v.check("X18.1d", ws_search(120e6, t_acc))
v.assert_true("lab wait_states agrees", ma.wait_states(48e6, t_acc) == 1 and ma.wait_states(120e6, t_acc) == 4)
f2 = brentq(lambda f: 3 / f - t_acc, 10e6, 500e6)          # 3 cycles exactly cover 40 ns
v.check("X18.1e", f2 / 1e6)
v.assert_true("2 wait states at 75 MHz, 3 just above", ws_search(75e6, t_acc) == 2 and ws_search(75.01e6, t_acc) == 3)
cpi64 = ma.cpi_analytic(4, 8, 2, 0.10)
cpi128 = ma.cpi_analytic(4, 16, 2, 0.10)
v.check("X18.1f", cpi64)
v.check("X18.1g", 120 / cpi64)
v.check("X18.1h", cpi128)
v.check("X18.1i", 120 / cpi128)
rng = np.random.default_rng(1801)
prog = ma.make_program(200000, 10, 1.0, 0.0, rng, aligned=True, line_bytes=16)
sim128 = ma.simulate_fetch(prog, 4, line_bytes=16).cpi
v.assert_true("cycle simulator: 128-bit lines at 4 WS give CPI 1.40 within 2%", abs(sim128 / 1.40 - 1) < 0.02, f"{sim128:.3f}")
rng = np.random.default_rng(1802)
prog8 = ma.make_program(200000, 10, 1.0, 0.0, rng, aligned=True, line_bytes=8)
sim64 = ma.simulate_fetch(prog8, 4, line_bytes=8).cpi
v.assert_true("cycle simulator: 64-bit lines at 4 WS are slower than 128-bit lines, near the model's 1.65",
              sim64 > sim128 and abs(sim64 / 1.65 - 1) < 0.08, f"{sim64:.3f}")
v.check("X18.1j", 400 / 4.10 / 0.96)

# ================================================================ Question 2 (toolchain)
text, data, bss = 41872, 2316, 14622
v.check("X18.2a", text + data)
v.check("X18.2b", 100 * (text + data) / (512 * 1024))
sram = data + bss + 6 * 1024 + 4 * 1024
v.check("X18.2c", sram)
v.check("X18.2d", 100 * sram / (96 * 1024))
v.assert_true("data and bss sizes in hex", data == 0x090C and bss == 0x391E)
edata = 0x20000000 + align4(data)
ebss = align4(edata + bss)
estack = 0x20000000 + 96 * 1024
stack_bottom = estack - 6 * 1024
heap_end = ebss + 4 * 1024
v.check("X18.2e", edata)
v.check("X18.2f", ebss)
v.check("X18.2g", stack_bottom)
v.check("X18.2h", stack_bottom - heap_end)
v.assert_true("free SRAM = total minus the size report minus 2 alignment bytes", stack_bottom - heap_end == 96 * 1024 - sram - 2)
reg0 = 0x000152C7
mask = ((1 << 3) - 1) << 4
v.check("X18.2i", mask)
v.check("X18.2j", reg0 & ~mask)
v.check("X18.2k", (reg0 & ~mask) | (5 << 4))
# replay the race: main reads, the handler clears bit 0 with its own read-modify-write, main writes its stale result
hw = reg0
main_snapshot = hw
hw = hw & ~0x1                                   # handler
hw = (main_snapshot & ~mask) | (5 << 4)          # main's write
v.check("X18.2l", hw)
v.check("X18.2m", ((reg0 & ~0x1) & ~mask) | (5 << 4))
v.assert_true("the interleaving loses the handler's change", hw & 1 == 1)
words_copy, words_zero = math.ceil(data / 4), math.ceil(bss / 4)
cycles = 7 * words_copy + 4 * words_zero
v.check("X18.2n", cycles)
v.check("X18.2o", cycles / 16e6 * 1e3)


# ================================================================ Question 3 (priorities, response times)
def decode(byte, impl_bits=3, group_bits=2):
    top = byte >> (8 - impl_bits)
    return top >> (impl_bits - group_bits), top & ((1 << (impl_bits - group_bits)) - 1)


v.check("X18.3a", 2 ** 2)
v.check("X18.3b", 2 ** 1)
byte = next(b for b in range(0, 256, 32) if decode(b) == (1, 1))
v.check("X18.3c", byte)
v.assert_true("0x40 is group 1 (no preemption of 0x60); 0x20 is group 0 (preempts)",
              decode(0x40)[0] == decode(0x60)[0] and decode(0x20)[0] < decode(0x60)[0])
irqs = [it.Irq("A", 4, 40, 0), it.Irq("B", 12, 100, 1), it.Irq("C", 25, 500, 2)]
v.check("X18.3d", it.utilization(irqs))


def rt_sim(blocking):
    """Critical instant: every IRQ requested at t = 0, just after a blocking section starts at t = 0."""
    return it.simulate(irqs, 2000, blocking_at=0.0, blocking_len=blocking)


for blk, ids in ((6, ("X18.3e", "X18.3f", "X18.3g")), (14, ("X18.3i", "X18.3j", "X18.3k"))):
    sim = rt_sim(blk)
    for name, ident in zip("ABC", ids):
        r = it.response_time(irqs, name, blocking=blk)
        v.assert_true(f"simulated worst response of {name} with {blk} us blocking equals the recurrence",
                      abs(sim[name] - r) < 1e-9, f"{sim[name]} vs {r}")
        v.check(ident, r)
v.check("X18.3h", 15 - 4)
v.assert_true("11 us of blocking meets A's 15 us deadline, 12 us does not",
              it.response_time(irqs, "A", 11) <= 15 < it.response_time(irqs, "A", 12))
v.check("X18.3l", it.response_time(irqs, "A", 0))

# ================================================================ Question 4 (timers, watchdog)
fclk = 72e6
best = max(((psc, arr) for psc in range(0, 8) for arr in range(0, 65536)
            if (psc + 1) * (arr + 1) == round(fclk / 25e3)), key=lambda x: x[1])
v.check("X18.4a", best[1])
v.assert_true("PSC = 0 gives the finest resolution", best[0] == 0)
v.check("X18.4b", math.log2(fclk / 25e3))
v.check("X18.4c", 0.625 * (best[1] + 1))
arr_c = fclk / 25e3 / 2
v.check("X18.4d", arr_c)
v.check("X18.4e", math.log2(arr_c))
v.assert_true("lab PWM resolution agrees", abs(it.pwm_resolution_bits(fclk, 25e3) - math.log2(2880)) < 1e-9
              and abs(it.pwm_resolution_bits(fclk, 25e3, center_aligned=True) - math.log2(1440)) < 1e-9)
psc = next(p for p in range(65536) if fclk / (p + 1) == 1e6)
v.check("X18.4f", psc)
d = it.capture_delta(0xFE70, 0x0A28)
v.check("X18.4g", d)
v.assert_true("capture difference by hand: 0x10A28 - 0xFE70", d == 0x10A28 - 0xFE70)
v.check("X18.4h", 1 / (d * 1e-6))
v.check("X18.4i", 100 / d)
v.check("X18.4j", it.watchdog_timeout(32, 2000, 32e3))
v.check("X18.4k", it.watchdog_timeout(32, 2000, 47e3))
v.check("X18.4l", it.watchdog_timeout(32, 2000, 17e3))
reload_min = next(r for r in range(1, 4096) if it.watchdog_timeout(32, r, 47e3) >= 1.5)
v.check("X18.4m", reload_min)
v.check("X18.4n", it.watchdog_timeout(32, reload_min, 17e3))
v.assert_true("1.5 s loop is unsafe at the original reload", it.watchdog_timeout(32, 2000, 47e3) < 1.5)

# ================================================================ Question 5 (DMA)
v.check("X18.5a", 100 * 16000 * 50 / 48e6)
v.check("X18.5b", 16000 / 160)
v.check("X18.5c", 100 * 100 * 300 / 48e6)
v.check("X18.5d", 160 / 16000 * 1e3)
fs, a, b, L = 500e3, 30e-6, 1.2e-6, 40e-6
n2 = (a + L) * fs / (1 - b * fs)
v.check("X18.5e", n2)
v.check("X18.5f", 128)
v.assert_true("128 is the next power of two above 87.5", 64 < n2 <= 128)
v.check("X18.5g", 2 * 128 * 2)
lat2 = (128 / fs + L + a + b * 128) * 1e6
v.check("X18.5h", lat2)
dead3 = (a + L) * fs / (2 - b * fs)
floor3 = a * fs / (1 - b * fs)
v.check("X18.5i", dead3)
v.check("X18.5j", floor3)
v.assert_true("lab bound for three buffers is the floor", abs(dm.pingpong_min_block(fs, a, b, L, 3) - floor3) < 1e-9)
v.check("X18.5k", 64)
v.check("X18.5l", 3 * 64 * 2)
lat3 = (64 / fs + L + a + b * 64) * 1e6
v.check("X18.5m", lat3)
v.check("X18.5n", (a + b * 32) * 1e6)
sim = {(n, k): dm.simulate_pingpong(fs, n, a, b, n_blocks=5000, n_buffers=k, service_latency=L)
       for n, k in ((64, 2), (128, 2), (32, 3), (64, 3))}
v.assert_true("simulation: overruns at 64 (two buffers) and 32 (three), none at 128 (two) or 64 (three)",
              sim[(64, 2)][0] > 0 and sim[(32, 3)][0] > 0 and sim[(128, 2)][0] == 0 and sim[(64, 3)][0] == 0)
v.assert_true("simulated worst latencies equal the formulas",
              abs(sim[(128, 2)][1] * 1e6 - lat2) < 1e-6 and abs(sim[(64, 3)][1] * 1e6 - lat3) < 1e-6)
rate = 460800 / 10
v.check("X18.5o", rate)
v.check("X18.5p", rate * 8e-3)
v.check("X18.5q", 2 ** math.ceil(math.log2(rate * 8e-3)))
head = dm.ring_head(512, 100)
v.check("X18.5r", head)
v.check("X18.5s", dm.ring_unread(head, 450, 512))
v.assert_true("unread by hand: 412 + 512 - 450", dm.ring_unread(head, 450, 512) == 412 + 512 - 450)

# ================================================================ Question 6 (serial buses)
fu = 48e6
v.check("X18.6a", fu / (16 * 230400))
v.check("X18.6b", fu / (16 * 13))
v.check("X18.6c", 100 * (fu / (16 * 13) / 230400 - 1))
v.check("X18.6d", fu / (16 * 921600))
v.check("X18.6e", 100 * (fu / (16 * 3) / 921600 - 1))
frac = round(fu / (16 * 921600) * 16) / 16
v.check("X18.6f", frac)
v.check("X18.6g", fu / (16 * frac))
v.assert_true("+8.51% is beyond the 16x receiver's +4.58% fast-sender limit; +0.16% is well inside",
              100 * (1 / ((9.5 + 1 / 16) / 10) - 1) < 8.51 and 0.16 < 2)
v.check("X18.6h", 1 / (2 * (3 + 1.5 + 12 + 1.5 + 4) * 1e-9) / 1e6)
v.check("X18.6i", 1 / (2 * (3 + 1.5 + 12 + 1.5 + 4 + 2 * 2.5) * 1e-9) / 1e6)
v.check("X18.6j", (2.5 - 0.4) / 3e-3)
k_rise = math.log(0.7 / 0.3)
v.check("X18.6k", 300e-9 / (k_rise * 250e-12))
tau = 1000 * 250e-12
t30 = brentq(lambda t: 1 - math.exp(-t / tau) - 0.3, 0, 10 * tau)
t70 = brentq(lambda t: 1 - math.exp(-t / tau) - 0.7, 0, 10 * tau)
v.check("X18.6l", (t70 - t30) * 1e9)
periods = (3 + 6) * 9 + 3
v.check("X18.6m", periods)
v.check("X18.6n", periods / 400e3 * 1e6)
v.check("X18.6o", 100 * 48 / periods)
v.check("X18.6p", 400e3 / periods)

# ================================================================ Question 7 (ADC, DAC, PWM)
lsb14 = 2.5 / 2 ** 14
v.check("X18.7a", lsb14 * 1e6)
v.check("X18.7b", round(1.0 / lsb14))
v.check("X18.7c", 6.02 * 14 + 1.76)
v.check("X18.7d", (78.0 - 1.76) / 6.02)
n_tau = brentq(lambda x: math.exp(-x) - 2.0 ** -15, 1, 30)
v.check("X18.7e", n_tau)
v.check("X18.7f", 3000 * 5e-12 * n_tau * 1e9)
v.check("X18.7g", 100e-9 / (5e-12 * n_tau) - 1000)
rng = np.random.default_rng(1807)
avg = rng.normal(0, 1.2, (40000, 64)).mean(axis=1)
v.assert_true("Monte Carlo: 64-sample averages of 1.2 LSB noise have 0.15 LSB rms", abs(avg.std() / 0.15 - 1) < 0.02,
              f"{avg.std():.4f}")
v.check("X18.7h", 1.2 / math.sqrt(64))
v.check("X18.7i", 0.5 * math.log2(64))
v.check("X18.7j", 1e6 / 64 / 1e3)
fpwm = 48e6 / 256
T = 1 / fpwm
tau_pwm = 256 * T / 4
v.check("X18.7k", fpwm / 1e3)
v.check("X18.7l", tau_pwm * 1e6)
v.check("X18.7m", 1 / (2 * math.pi * tau_pwm))
v.check("X18.7n", tau_pwm * math.log(2 ** 9) * 1e3)
# exact peak-to-peak ripple of an RC driven by a 50% square wave of 0 to 3.3 V: V tanh(T / (4 tau))
ripple = 3.3 * math.tanh(T / (4 * tau_pwm))
v.assert_true("exact 50%-duty ripple with tau = 341.3 us is within 0.01% of one LSB (12.89 mV)",
              abs(ripple / (3.3 / 256) - 1) < 1e-4, f"{ripple * 1e3:.4f} mV")

# ================================================================ Question 8 (RTOS)
v.check("X18.8a", 100 * (1000 * 2e-6 + 800 * 1.5e-6))
tasks = [rs.Task("A", 6, [(2, None)]), rs.Task("B", 10, [(3, None)]), rs.Task("C", 20, [(4, None)])]
tasks = rs.rm_priorities(tasks)
v.check("X18.8b", rs.utilization(tasks))
v.check("X18.8c", rs.ll_bound(3))
v.check("X18.8d", (1 + 2 / 6) * (1 + 3 / 10) * (1 + 4 / 20))
v.assert_true("hyperbolic bound inconclusive", not rs.hyperbolic_ok(tasks))
res = rs.simulate(tasks, 60 * 10, policy="fp")
for name, ident, val in (("A", "X18.8e", 2), ("B", "X18.8f", 5), ("C", "X18.8g", 16)):
    v.assert_true(f"simulated worst response of {name} over 10 hyperperiods is {val}", res.worst(name) == val, str(res.worst(name)))
    v.check(ident, res.worst(name))
v.assert_true("no deadline misses", sum(res.misses.values()) == 0)


def inversion():
    return [rs.Task("L", 100, [(1, None), (3, "S"), (1, None)], priority=1, offset=0, max_jobs=1),
            rs.Task("M", 100, [(6, None)], priority=2, offset=3, max_jobs=1),
            rs.Task("H", 100, [(1, None), (1, "S"), (1, None)], priority=3, offset=2, max_jobs=1)]


def trace(r):
    return "".join(x or "." for x in r.trace).rstrip(".")


none8, inh8, ceil8 = (rs.simulate(inversion(), 40, protocol=p) for p in ("none", "inherit", "ceiling"))
v.assert_true("no-protocol timeline", trace(none8) == "LLHMMMMMMLLHHL", trace(none8))
v.assert_true("inheritance timeline", trace(inh8) == "LLHLLHHMMMMMML", trace(inh8))
v.assert_true("ceiling timeline", trace(ceil8) == "LLLLHHHMMMMMML", trace(ceil8))
v.check("X18.8h", none8.worst("H"))
v.check("X18.8i", inh8.worst("H"))
v.check("X18.8j", ceil8.worst("H"))
v.check("X18.8k", rs.blocking_ceiling(inversion(), 2))
v.check("X18.8l", 3 + rs.blocking_ceiling(inversion(), 2))
slots30 = max(rs.queue_max_occupancy(4, 400, [(t0, 30)]) for t0 in range(100, 104))
slots32 = max(rs.queue_max_occupancy(4, 400, [(t0, 32)]) for t0 in range(100, 104))
v.check("X18.8m", math.floor(30 / 4) + 1)
v.assert_true("occupancy simulation: 8 records wait at worst with a 30 ms stall, 9 with 32 ms", slots30 == 8 and slots32 == 9,
              f"{slots30}, {slots32}")
v.check("X18.8n", 8 * 16)
v.check("X18.8o", math.floor(32 / 4) + 1)

# ================================================================ Question 9 (boot and update)
v.check("X18.9a", 512 - 48)
v.check("X18.9b", (512 - 48) / 2)
v.check("X18.9c", (512 - 48 - 16) / 2)
sectors = 200 // 8
v.check("X18.9d", sectors)
copy = 30e-3 + (8192 // 16) * 50e-6
v.check("X18.9e", copy * 1e3)
v.check("X18.9f", sectors * copy)
v.check("X18.9g", 3 * sectors * copy)
v.check("X18.9h", 10000 / sectors)
img = 200 * 1024
v.check("X18.9i", img * 20 / 96e6 * 1e3)
v.check("X18.9j", 3e6 / 96e6 * 1e3)
v.check("X18.9k", (img * 20 + 3e6) / 96e6 * 1e3)
v.check("X18.9l", (img + 3e6) / 96e6 * 1e3)
window = img / 40e3
v.check("X18.9m", window)
rate_cut = 3 / (30 * 86400)
p_hit = 1 - math.exp(-rate_cut * window)
v.check("X18.9n", p_hit)
v.check("X18.9o", 2e6 * p_hit)
# the first cut after the window opens is exponential with rate lambda: integrate its density over the window
p_quad = integrate.quad(lambda t: rate_cut * math.exp(-rate_cut * t), 0, window)[0]
v.assert_true("integrated exponential density over the window equals the closed form", abs(p_quad / p_hit - 1) < 1e-9)

# ================================================================ Question 10 (ultra-low power)
q = 1.5e-3 * 4e-3 + 5e-3 * 2.5e-3 + 2e-6 * (2 - 6.5e-3)
i_avg = q / 2
v.check("X18.10a", i_avg * 1e6)
v.check("X18.10b", 225e-3 / i_avg / 24)
v.check("X18.10c", 100 * 5e-3 * 2.5e-3 / q)
v.check("X18.10d", 150e-9 / (0.6e-3 - 4e-6) * 1e3)
v.check("X18.10e", 6e-6 / (4e-6 - 0.3e-6))


def charge(f_mhz):
    t = 2e6 / (f_mhz * 1e6)
    return (50e-6 * f_mhz + 300e-6) * t + 1.5e-6 * (1 - t)


v.check("X18.10f", charge(16) * 1e6)
v.check("X18.10g", charge(64) * 1e6)
v.check("X18.10h", 100 * (1 - charge(64) / charge(16)))
v.check("X18.10i", 10e-3 * 60)
c_min = 3e-3 / math.log(2) / 60
v.check("X18.10j", c_min * 1e6)


def droop(c):
    """Integrate C dv/dt = (3.0 - v)/R - I for 3 ms from v = 3.0 V; return the drop."""
    sol = integrate.solve_ivp(lambda t, y: [((3.0 - y[0]) / 60 - 10e-3) / c], (0, 3e-3), [3.0], rtol=1e-10, atol=1e-12)
    return 3.0 - sol.y[0, -1]


v.assert_true("ODE: 72.1 uF gives exactly 0.30 V of droop", abs(droop(c_min) - 0.3) < 1e-6)
v.check("X18.10k", droop(100e-6) * 1e3)

# ================================================================ Question 11 (sensors)
v.check("X18.11a", 90e-3 * math.sqrt(100))
tilt = math.degrees(math.asin(0.9e-3))
v.check("X18.11b", tilt)
v.check("X18.11c", tilt / math.sqrt(400))
# one-sided density rho: white rate samples at fs have variance rho^2 fs / 2; integrate 100 s of them
rho_g, fs_g = 0.005, 100.0
rng = np.random.default_rng(18011)
theta = (rng.normal(0, rho_g * math.sqrt(fs_g / 2), (4000, int(100 * fs_g))) / fs_g).sum(axis=1)
v.assert_true("Monte Carlo angle noise after 100 s is 0.0354 deg within 3%", abs(theta.std() / 0.03536 - 1) < 0.03, f"{theta.std():.5f}")
v.check("X18.11d", 60 * rho_g / math.sqrt(2))
v.check("X18.11e", rho_g * math.sqrt(100 / 2))
v.check("X18.11f", 0.2 * 100)
alpha, dt = 0.99, 1 / 200
tau_c = alpha * dt / (1 - alpha)
v.check("X18.11g", tau_c)
v.check("X18.11h", 0.2 * tau_c)
v.check("X18.11i", math.sqrt((1 - alpha) / (1 + alpha)))
rng = np.random.default_rng(1811)
w = rng.normal(0, 1, 400000)
y = signal.lfilter([1 - alpha], [1, -alpha], w)[2000:]
v.assert_true("simulated low-pass passes 0.0709 of white noise (within 2%)", abs(y.std() / 0.07089 - 1) < 0.02, f"{y.std():.4f}")
# constant gyroscope bias through the filter: the estimate settles at b * tau
est = 0.0
for _ in range(20000):
    est = alpha * (est + 0.2 * dt) + (1 - alpha) * 0.0
v.assert_true("simulated bias error settles at 0.099 deg", abs(est - 0.099) < 1e-6, f"{est:.6f}")
m_pi, i_dc, bw = 0.005, 2e-6, 8
snr = m_pi ** 2 * i_dc / (4 * constants.e * bw)
v.check("X18.11j", 10 * math.log10(snr))
v.assert_true("SNR from signal power (m I)^2/2 over shot noise 2 q I B", abs(((m_pi * i_dc) ** 2 / 2) / (2 * constants.e * i_dc * bw) / snr - 1) < 1e-12)
v.check("X18.11k", 15e-3 * 80e-6 * 50 * 1e6)

# ================================================================ Question 12 (security)
v.check("X18.12a", (2 ** 24 + 1) / 2 / 200 / 3600)
v.check("X18.12b", (2 ** 24 + 1) / 2 / 86400)
v.check("X18.12c", 5 * 256 * 100 + 256)
secret = bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0xFF])
got, qn = hs.timing_attack(secret, reps=100)
v.assert_true("lab timing attack recovers a 6-byte token whose last byte is 0xFF in exactly 128 256 queries",
              got == secret and qn == 128256, f"{got.hex()} {qn}")


def rho(s):
    return math.sqrt(2 / (2 + s ** 2))


v.check("X18.12d", rho(6))
v.check("X18.12e", (4 / rho(6)) ** 2)
v.check("X18.12f", (4 / rho(12)) ** 2)
p_, l_ = hs.simulate_traces(0x3C, 400000, 6.0, seed=18012)
meas = np.corrcoef(hs.HW[hs.SBOX[p_ ^ 0x3C]], l_)[0, 1]
v.assert_true("measured correlation at sigma = 6 matches 0.229", abs(meas - rho(6)) < 0.005, f"{meas:.4f}")


def key_fail(p, n, k=128):
    return 1 - (1 - binom.sf(n // 2, n, p)) ** k


def smallest_odd(p, target=1e-6, k=128):
    n = 1
    while key_fail(p, n, k) > target:
        n += 2
    return n


n12 = smallest_odd(0.08)
v.check("X18.12g", n12)
v.check("X18.12h", 128 * n12)
v.check("X18.12i", key_fail(0.08, n12))
v.assert_true("lab smallest_repetition agrees", hs.smallest_repetition(0.08, 1e-6) == n12)

# ================================================================ Question 13 (derivations)
for fq, ident in ((75e6, "X18.13a"), (80e6, "X18.13b")):
    ws = ws_search(fq, t_acc)
    v.check(ident, fq / 1e6 / ma.cpi_analytic(ws, 16, 2, 0.10))
v.check("X18.13c", 5e-12 * (2 ** 15 - 1) * 1e9)
r_eq = 1 / (50e3 * 5e-12)
err_est = 2.5 * 10e3 / (10e3 + r_eq)
v.check("X18.13d", err_est * 1e3)
v.check("X18.13e", err_est / lsb14)
# exact recursion: pin x, share with C_sh arriving from 0 V, recover through R_s for T = 1/f
cext, csh, rs_, vs, T13 = 220e-9, 5e-12, 10e3, 2.5, 1 / 50e3
aa = cext / (cext + csh)
eps = math.exp(-T13 / (rs_ * cext))
x = vs
for _ in range(200000):
    s_ = aa * x
    x = vs + (s_ - vs) * eps
sampled = aa * x
v.assert_true("exact recursion error within 1% of the average-current estimate (6.23 mV)",
              abs((vs - sampled) / err_est - 1) < 0.01, f"{(vs - sampled) * 1e3:.3f} mV")
v.assert_true("charge-sharing step with 220 nF is below half an LSB",
              2.5 * csh / (cext + csh) < lsb14 / 2)
v.check("X18.13f", rho(10))
v.check("X18.13g", (4 / rho(10)) ** 2)
v.check("X18.13h", 4 ** 2 * 10 ** 2 / 2)
vals = np.arange(256)
v.assert_true("HW of a uniform byte has mean 4 and variance 2", abs(hs.HW[vals].mean() - 4) < 1e-12 and abs(hs.HW[vals].var() - 2) < 1e-12)
pm, lm = hs.simulate_traces(0x3C, 200000, 1.0, masked=True, seed=18013)
rm = np.corrcoef(hs.HW[hs.SBOX[pm ^ 0x3C]], lm)[0, 1]
v.assert_true("masked leakage has no first-order correlation", abs(rm) < 4 / math.sqrt(200000), f"{rm:.4f}")

# ================================================================ Question 14 (diligence)
led = 12e-3 * 60e-6 * 25
v.check("X18.14a", led * 1e6)
total = led + 25e-6 + 35e-6 + 40e-6
v.check("X18.14b", total * 1e6)
v.check("X18.14c", 18e-3 * 0.85 / total / 24)
v.check("X18.14d", 18e-3 * 0.85 / (7 * 24) * 1e6)
image = 448 * 1024
v.check("X18.14e", image / 60e3)
v.check("X18.14f", 100 * 3 * 60e3 / image)
v.check("X18.14g", 0.97 ** 128)
n14 = smallest_odd(0.03)
v.check("X18.14h", n14)
v.check("X18.14i", 128 * n14)
v.assert_true("lab PUF Monte Carlo at the chosen length shows no failures in 20 000 keys",
              hs.simulate_puf(0.03, n14) == 0.0)

sys.exit(v.finish())
