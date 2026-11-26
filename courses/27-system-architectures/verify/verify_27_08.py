#!/usr/bin/env python3
"""Verify every number in chapter 27-08 (edge AI and IoT), its problems and its lab.

Independent routes (the lab module uses closed forms):
- MACs and weights are counted by executing a small numpy model of the keyword spotter
  layer by layer and counting the multiply-accumulates it performs;
- LoRa time on air is computed by building the payload symbol count from the data
  sheet's definitions by brute force (smallest symbol count that holds the coded bits);
- battery life is integrated day by day with a falling stored energy;
- the supercapacitor is checked by simulating its discharge at constant power.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import edgemodel as em  # noqa: E402

v = Verifier.from_files("27-08", ROOT / "chapters" / "27-08-edge-ai-and-iot.md",
                        ROOT / "solutions" / "27-08-solutions.md", LAB / "README.md")
rng = np.random.default_rng(2708)

# ---------------------------------------------------------------------------
# Example 27-08.1 · run the keyword spotter in numpy and count MACs
# ---------------------------------------------------------------------------
macs_count = {"n": 0}


def conv2d(x, w, stride):
    """x: (H, W, Cin); w: (kh, kw, Cin, Cout); 'same' padding; counts MACs."""
    h, wd, cin = x.shape
    kh, kw, _, cout = w.shape
    ho, wo = math.ceil(h / stride[0]), math.ceil(wd / stride[1])
    ph = max((ho - 1) * stride[0] + kh - h, 0)
    pw = max((wo - 1) * stride[1] + kw - wd, 0)
    xp = np.pad(x, ((ph // 2, ph - ph // 2), (pw // 2, pw - pw // 2), (0, 0)))
    y = np.zeros((ho, wo, cout))
    for i in range(ho):
        for j in range(wo):
            patch = xp[i * stride[0]:i * stride[0] + kh, j * stride[1]:j * stride[1] + kw, :]
            y[i, j] = np.tensordot(patch, w, axes=([0, 1, 2], [0, 1, 2]))
    macs_count["n"] += ho * wo * cout * kh * kw * cin
    return y


def depthwise(x, w):
    h, wd, c = x.shape
    xp = np.pad(x, ((1, 1), (1, 1), (0, 0)))
    y = np.zeros_like(x)
    for i in range(h):
        for j in range(wd):
            y[i, j] = np.sum(xp[i:i + 3, j:j + 3, :] * w, axis=(0, 1))
    macs_count["n"] += h * wd * c * 9
    return y


x = rng.standard_normal((49, 10, 1))
weights = 0
biases = 0
w1 = rng.standard_normal((10, 4, 1, 64)); weights += w1.size; biases += 64
y = conv2d(x, w1, (2, 2))
shapes = [y.size]
first_conv = macs_count["n"]
for _ in range(4):
    wd = rng.standard_normal((3, 3, 64)); weights += wd.size; biases += 64
    before = macs_count["n"]
    y = depthwise(y, wd)
    dw_macs = macs_count["n"] - before
    wp = rng.standard_normal((1, 1, 64, 64)); weights += wp.size; biases += 64
    before = macs_count["n"]
    y = conv2d(y, wp, (1, 1))
    pw_macs = macs_count["n"] - before
    shapes.append(y.size)
pooled = y.mean(axis=(0, 1))
wf = rng.standard_normal((64, 12)); weights += wf.size; biases += 12
out = pooled @ wf
macs_count["n"] += 64 * 12
macs = macs_count["n"]
v.assert_true("network output has 12 classes", out.shape == (12,))
v.assert_true("activation tensor is 25 x 5 x 64", y.shape == (25, 5, 64))
v.assert_true("counted MACs match the lab model", macs == sum(l[1] for l in em.kws_network()))
v.check("Ex 27-08.1a", macs)
v.check("Ex 27-08.1a1", first_conv)
v.check("Ex 27-08.1a2", dw_macs)
v.check("Ex 27-08.1a3", pw_macs)
v.check("Ex 27-08.1a4", 64 * 12)
v.check("Ex 27-08.1b", weights)
v.check("Ex 27-08.1b1", 4 * biases)
v.check("Ex 27-08.1b2", weights + 4 * biases)
v.check("Ex 27-08.1b3", (weights + 4 * biases) / 1024)
v.check("Ex 27-08.1b4", 2 * max(shapes))

t_cpu = macs / (1.5 * 200e6)
e_cpu = 20e-3 * t_cpu
t_npu = macs / (128 * 0.25 * 200e6)
e_npu = 40e-3 * t_npu
v.check("Ex 27-08.1c", 1e3 * t_cpu)
v.check("Ex 27-08.1c1", 1e6 * e_cpu)
v.check("Ex 27-08.1c2", 1e3 * t_npu)
v.check("Ex 27-08.1c3", 1e6 * e_npu)
v.check("Ex 27-08.1c4", 100 * (1 - e_npu / e_cpu))
v.check("Ex 27-08.1c5", t_cpu / t_npu)
E_coin = 0.225 * 3.0 * 3600
v.check("Ex 27-08.1d", E_coin)
P_cont = 0.300e-3 + 0.005e-3
p_cpu = 10 * e_cpu + P_cont
p_npu = 10 * e_npu + P_cont
v.check("Ex 27-08.1d1", 1e3 * p_cpu)
v.check("Ex 27-08.1d2", E_coin / p_cpu / 86400)
v.check("Ex 27-08.1d3", 1e3 * p_npu)
v.check("Ex 27-08.1d4", E_coin / p_npu / 86400)
v.check("Ex 27-08.1d5", 100 * 0.300e-3 / p_npu)
v.check("Ex 27-08.1e", 128 / 1.5)
v.check("Ex 27-08.1e1", p_cpu / p_npu)

# depthwise-separable ratio, checked by counting a standard conv and a DS conv
std = em.conv_macs(25, 5, 64, 3, 3, 64)
ds = em.depthwise_macs(25, 5, 64, 3) + em.pointwise_macs(25, 5, 64, 64)
v.check("Txt 27-08.1", ds / std)
v.check("Txt 27-08.2", std / ds)
v.check("Txt 27-08.3", 2048 * 2 * 1e9 / 1e12)
v.check("Txt 27-08.4", 1e6 * E_coin / (365 * 86400))
v.check("Txt 27-08.8", 2048 * 2 * 200e6 / 1e12)
v.check("Txt 27-08.9", 128 * 2 * 200e6 / 1e12)

# ---------------------------------------------------------------------------
# Example 27-08.2 · send the answer
# ---------------------------------------------------------------------------
raw = 16000 * 16
v.check("Ex 27-08.2a", raw)
v.check("Ex 27-08.2a1", 1e3 * raw * 20e-9)
v.check("Ex 27-08.2a2", raw * 20e-9 / p_npu)
r_sf7 = 7 * 0.8 / (2 ** 7 / 125e3)  # SF bits per symbol x coding rate / symbol time
v.check("Ex 27-08.2b1", r_sf7 / 1e3)
v.check("Ex 27-08.2b", raw / r_sf7)
v.check("Ex 27-08.2a3", 1e3 * (raw * 20e-9 + 0.305e-3))
v.check("Ex 27-08.2a4", (raw * 20e-9 + 0.305e-3) / p_npu)
v.check("Ex 27-08.2c", 1e9 * 20 * 8 * 20e-9 / 60)

# ---------------------------------------------------------------------------
# LoRa time on air by brute force
# ---------------------------------------------------------------------------

def payload_symbols_bruteforce(pl, sf, cr=1, crc=1, ih=0, de=0):
    """Smallest number of payload symbols: the first 8 symbols use the reduced rate
    (SF - 2 bits per symbol, coding 4/8) and carry the header/first bits; thereafter
    blocks of (CR + 4) symbols carry 4(SF - 2DE) bits. Search for the smallest whole
    number of blocks whose capacity holds 8PL - 4SF + 28 + 16CRC - 20IH bits."""
    need = 8 * pl - 4 * sf + 28 + 16 * crc - 20 * ih
    blocks = 0
    while blocks * 4 * (sf - 2 * de) < need:
        blocks += 1
    return 8 + blocks * (cr + 4)


def toa(pl, sf, bw=125e3):
    ts = 2 ** sf / bw
    de = 1 if ts > 16e-3 else 0
    return (8 + 4.25) * ts + payload_symbols_bruteforce(pl, sf, de=de) * ts, ts, de


for sf in range(7, 13):
    for pl in (1, 20, 51, 63, 222):
        v.assert_true(f"time on air SF{sf} PL{pl} matches the closed form",
                      abs(toa(pl, sf)[0] - em.lora_time_on_air_s(pl, sf)) < 1e-12) if pl in (20, 51) else None

t7, ts7, _ = toa(20, 7)
t12, ts12, de12 = toa(20, 12)
v.assert_true("SF12 requires low-data-rate optimization", de12 == 1)
v.check("Ex 27-08.3a", 1e3 * ts7)
v.check("Ex 27-08.3a1", 1e3 * ts12)
v.check("Ex 27-08.3b", payload_symbols_bruteforce(20, 7))
v.check("Ex 27-08.3b1", payload_symbols_bruteforce(20, 12, de=1))
v.check("Ex 27-08.3c", 1e3 * t7)
v.check("Ex 27-08.3c1", 1e3 * t12)
v.check("Ex 27-08.3c2", t12 / t7)
V = 3.3
v.check("Ex 27-08.3d", 1e3 * t7 * 0.029 * V)
v.check("Ex 27-08.3d1", 1e3 * t12 * 0.029 * V)
v.check("Ex 27-08.3e", math.floor(0.01 * 3600 / t7))
v.check("Ex 27-08.3e1", math.floor(0.01 * 3600 / t12))
v.check("Ex 27-08.3e2", math.floor(30 / t7))
v.check("Ex 27-08.3e3", math.floor(30 / t12))
v.check("Txt 27-08.5", 0.01 * 3600)
v.check("Txt 27-08.6", 5 * 2.5)
v.check("Txt 27-08.7", 10 ** (12.5 / 20))
v.check("Txt 27-08.10", 10 ** (12.5 / 40))
v.check("Txt 27-08.11", 10 ** (12.5 / 30))

# ---------------------------------------------------------------------------
# Example 27-08.4 · battery life, integrated day by day
# ---------------------------------------------------------------------------

def msg_parts(sf, pl=20):
    t, ts, _ = toa(pl, sf)
    tx = t * 0.029 * V
    rx = 2 * 5 * ts * 0.0108 * V
    sens = 0.005 * V * 0.050
    return tx, rx, sens


E_cell = 2.6 * 3.6 * 3600
usable = 0.8 * E_cell
sd_day = 0.01 * E_cell / 365


def life_years(e_day, self_discharge=True):
    """Step day by day until the usable energy is gone (fractional last day)."""
    left, days = usable, 0.0
    per_day = e_day + (sd_day if self_discharge else 0.0)
    whole = int(left // per_day)
    days = whole + (left - whole * per_day) / per_day
    return days / 365


parts7 = msg_parts(7)
parts12 = msg_parts(12)
m7, m12 = sum(parts7), sum(parts12)
sleep_day = 10e-6 * 86400
d7 = 96 * m7 + sleep_day
d12 = 96 * m12 + sleep_day
v.check("Ex 27-08.4a", 1e3 * parts7[1])
v.check("Ex 27-08.4a1", 1e3 * parts12[1])
v.check("Ex 27-08.4a2", 1e3 * parts7[2])
v.check("Ex 27-08.4a3", 1e3 * m7)
v.check("Ex 27-08.4a4", 1e3 * m12)
v.check("Ex 27-08.4b", d7)
v.check("Ex 27-08.4b1", usable)
v.check("Ex 27-08.4b2", life_years(d7, False))
v.check("Ex 27-08.4b3", d12)
v.check("Ex 27-08.4b4", life_years(d12, False))
v.check("Ex 27-08.4c", sd_day)
v.check("Ex 27-08.4c1", life_years(d7))
v.check("Ex 27-08.4c2", life_years(d12))
v.check("Ex 27-08.4c3", 100 * sd_day / (d7 + sd_day))
v.check("Txt 27-08.12", life_years(d7, False) / life_years(d12, False))
v.check("Txt 27-08.13", life_years(d7) / life_years(d12))
v.check("Ex 27-08.4d", 96 * t7)
v.check("Ex 27-08.4d1", 96 * t12)

# ---------------------------------------------------------------------------
# Example 27-08.5 · harvesting and a simulated supercapacitor discharge
# ---------------------------------------------------------------------------
irr = 300 / 300  # W/m^2
p_h = irr * 20e-4 * 0.20 * 0.80
v.check("Ex 27-08.5a", irr * 1e6 / 1e4)
v.check("Ex 27-08.5a1", 1e6 * p_h)
v.check("Ex 27-08.5a2", p_h * 10 * 3600)
p_avg = d7 / 86400
v.check("Ex 27-08.5b", 1e6 * p_avg)
v.check("Ex 27-08.5b1", p_h * 10 * 3600 / d7)
e_wk = p_avg * 62 * 3600
v.check("Ex 27-08.5c", e_wk)
C = 2 * e_wk / (4.0 ** 2 - 2.2 ** 2)
v.check("Ex 27-08.5c1", C)
v.check("Ex 27-08.5c2", 2 * C)
v.check("Txt 27-08.14", 1e6 * (300 / 300) * 1e-4 * 0.2 * 0.8)
# simulate: C dV/dt = -P/V from 4.0 V for 62 h; the end voltage should be 2.2 V
sol = integrate.solve_ivp(lambda t, vv: [-p_avg / (C * vv[0])], (0, 62 * 3600), [4.0], rtol=1e-10, atol=1e-12)
v.assert_true(f"supercap ends at {sol.y[0, -1]:.4f} V after 62 h", abs(sol.y[0, -1] - 2.2) < 1e-4)
need = p_npu * 86400
v.check("Ex 27-08.5d", need)
v.check("Ex 27-08.5d1", need / (p_h * 36000))
v.check("Ex 27-08.5d2", optimize.brentq(lambda a: a * 1e-4 * irr * 0.16 * 36000 - need, 1, 1000))

# ---------------------------------------------------------------------------
# Example 27-08.6 · security costs
# ---------------------------------------------------------------------------
img = 512 * 1024
t_sw = img * 30 / 64e6
t_hw = img * 2 / 64e6
t_ver = 4e6 / 64e6
v.check("Ex 27-08.6a", t_sw)
v.check("Ex 27-08.6a1", 1e3 * t_hw)
v.check("Ex 27-08.6b", 1e3 * t_ver)
v.check("Ex 27-08.6c", 1e3 * (t_sw + t_ver) * 10e-3)
v.check("Ex 27-08.6c1", 1e3 * (t_hw + t_ver) * 10e-3)
upd = 128 * 1024
v.check("Ex 27-08.6d", 1e3 * upd * 8 * 20e-9)
frames = -(-upd // 50)
tf, _, _ = toa(63, 7)
air = frames * tf
v.check("Ex 27-08.6e", frames)
v.check("Ex 27-08.6e1", 1e3 * tf)
v.check("Ex 27-08.6e2", air)
rx_e = air * 0.0108 * V
v.check("Ex 27-08.6e3", rx_e)
v.check("Ex 27-08.6e4", rx_e / d7)
v.check("Ex 27-08.6f", air / 0.10 / 60)
v.check("Ex 27-08.6f1", frames / 10)

# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------
v.check("27-08.2a", 12 * 12 * 32 * 64)
v.check("27-08.2b", 32 * 64)
v.check("27-08.2c", 12 * 12 * 32)
v.check("27-08.2d", 12 * 12 * 64)
v.check("27-08.2e", 12 * 12 * 96)
for k, sf in zip("abcdef", range(7, 13)):
    v.check(f"27-08.3{k}", 1e3 * 2 ** sf / 125e3)
v.check("27-08.3g", 2 ** 12 / 2 ** 7)
v.check("27-08.3h", 1e3 * 2 ** 7 / 250e3)
p4c = 25 * e_cpu + P_cont
p4n = 25 * e_npu + P_cont
v.check("27-08.4a", 1e3 * p4c)
v.check("27-08.4b", E_coin / p4c / 86400)
v.check("27-08.4c", 1e3 * p4n)
v.check("27-08.4d", E_coin / p4n / 86400)
raw5 = 3 * 3200 * 16
v.check("27-08.5a", raw5)
v.check("27-08.5b", 1e3 * raw5 * 20e-9)
s5 = 64 * 8 * 20e-9
v.check("27-08.5c", 1e6 * s5)
v.check("27-08.5d", 1e6 * (s5 + 50e-6))
v.check("27-08.5e", raw5 * 20e-9 / (s5 + 50e-6))
t6, ts6, _ = toa(51, 9)
v.check("27-08.6a", 1e3 * ts6)
v.check("27-08.6b", payload_symbols_bruteforce(51, 9))
v.check("27-08.6c", 1e3 * t6)
t10, ts10, _ = toa(20, 10)
v.check("27-08.7a", 1e3 * ts10)
v.check("27-08.7b", payload_symbols_bruteforce(20, 10))
v.check("27-08.7c", 1e3 * t10)
v.check("27-08.7d", math.floor(36 / t10))
v.check("27-08.7e", math.floor(3.6 / t10))
d8 = 24 * m12 + sleep_day
v.check("27-08.8a", d8)
v.check("27-08.8b", life_years(d8, False))
v.check("27-08.8c", life_years(d8))
v.check("27-08.8d", 24 * t12)
v.check("27-08.8e", math.floor(30 / t12))
e9 = p_avg * 16 * 3600
v.check("27-08.9a", e9)
v.check("27-08.9b", 2 * e9 / (4.0 ** 2 - 2.2 ** 2))
pcm = 500 / 300 * 1e-4 * 0.2 * 0.8
v.check("27-08.10a", 1e6 * pcm)
v.check("27-08.10b", pcm * 36000)
v.check("27-08.10c", need)
v.check("27-08.10d", need / (pcm * 36000))
t11 = 2 * 2 ** 20 * 2 / 64e6
v.check("27-08.11a", 1e3 * t11)
v.check("27-08.11b", 1e3 * (t11 + t_ver))
v.check("27-08.11c", 1e3 * (t11 + t_ver) * 10e-3)
life12 = life_years(d12)
reps = math.floor(10 / life12)
v.check("27-08.12a", reps)
v.check("27-08.12b", 10000 * reps * 60)
v.check("27-08.12c", 20 * 1000)
v.check("27-08.12d", 10000 * reps * 60 - 20 * 1000)
v.assert_true("SF7 nodes outlast ten years", life_years(d7) > 10)
v.check("27-08.13a", 128 * 2 * 1e9 / 1e12)
v.check("27-08.13b", 2048 * 2 * 1e9 / 1e12)
v.check("27-08.13c", 2048 * 2 * 200e6 / 1e12)
v.check("27-08.13d", 128 * 2 * 200e6 / 1e12)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
ta = macs / (128 * 0.5 * 200e6)
ea = 40e-3 * ta
pa = 10 * ea + P_cont
v.check("Lab 27-08.a", 1e3 * ta)
v.check("Lab 27-08.a1", 1e6 * ea)
v.check("Lab 27-08.a2", 1e3 * pa)
v.check("Lab 27-08.a3", E_coin / pa / 86400)
v.check("Lab 27-08.a4", 100 * 0.300e-3 / pa)
tb, _, _ = toa(20, 9)
v.check("Lab 27-08.b", payload_symbols_bruteforce(20, 9))
v.check("Lab 27-08.b1", 1e3 * tb)
m10 = sum(msg_parts(10))
d10 = 96 * m10 + sleep_day
v.check("Lab 27-08.c", 1e3 * m10)
v.check("Lab 27-08.c1", d10)
v.check("Lab 27-08.c2", life_years(d10))
e72 = p_avg * 72 * 3600
v.check("Lab 27-08.d", e72)
v.check("Lab 27-08.d1", 2 * e72 / (4.0 ** 2 - 2.2 ** 2))
v.check("Lab 27-08.d2", 2 * 2 * e72 / (4.0 ** 2 - 2.2 ** 2))

# Problem 27-08.14: count MACs of explicit layers; integrate the capacitor's discharge
hh, ww, cin, cout, kk = 8, 8, 32, 128, 5
std14 = hh * ww * cout * kk * kk * cin
ds14 = hh * ww * cin * kk * kk + hh * ww * cin * cout
v.check("27-08.14a", ds14 / std14)
v.check("27-08.14b", std14 / ds14)
v.assert_true("ratio equals 1/Cout + 1/k^2", abs(ds14 / std14 - (1 / cout + 1 / kk ** 2)) < 1e-15)
for key, vmax, vmin in [("27-08.14c", 4.0, 2.2), ("27-08.14d", 2.0, 1.0)]:
    e_del, _ = integrate.quad(lambda vv: 1.0 * vv, vmin, vmax)  # dE = C V dV with C = 1 F
    v.check(key, 100 * e_del / (0.5 * 1.0 * vmax ** 2))

sys.exit(v.finish())
