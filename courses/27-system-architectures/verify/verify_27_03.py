#!/usr/bin/env python3
"""Verify every number in chapter 27-03 (the smartwatch), its problems and its lab.

Independent routes (the lab module uses closed forms):
- daily energy from a one-second power timeline of the whole day, and battery life by stepping
  the cumulative battery drain until it reaches the cell's energy;
- the Lambertian flux by numerical integration of L cos(theta) over the hemisphere;
- pixel hold times by integrating the droop ODE C dV/dt = -I with an event;
- BLE averages by summing charge event by event over a simulated hour, and air times by
  building the packet's octets;
- batching and paging by counting wakes over a simulated hour;
- buck/LDO crossover and power-gating break-even by root finding;
- cell active volume by subtracting the overhead shell, and the safe current by root finding.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import watchmodel as wm  # noqa: E402

v = Verifier.from_files("27-03", ROOT / "chapters" / "27-03-wearables-smartwatch.md",
                        ROOT / "solutions" / "27-03-solutions.md", LAB / "README.md")

DAY = 86400


# ---------------------------------------------------------------------------
# Day timeline (one-second resolution)
# ---------------------------------------------------------------------------

def day_timeline(floor=6.0, aod=7.0, checks=(300, 4, 250.0), notif=(90, 6, 300.0),
                 app=(0.25, 500.0), workout=(1.0, 150.0), sleep=(6.0, 3.0), hr_awake=2.0,
                 aod_on=True):
    """Return an array of rail power (mW) for each second of the day, plus per-item energies.
    The order of activities within the day does not matter for the energy."""
    p = np.zeros(DAY)
    state = np.full(DAY, "aod", dtype=object)
    t = 0
    n_sleep = int(round(sleep[0] * 3600))
    state[t:t + n_sleep] = "sleep"
    t += n_sleep
    n_work = int(round(workout[0] * 3600))
    state[t:t + n_work] = "workout"
    t += n_work
    n_app = int(round(app[0] * 3600))
    state[t:t + n_app] = "app"
    t += n_app
    for _ in range(checks[0]):
        state[t:t + checks[1]] = "check"
        t += checks[1] + 10
    for _ in range(notif[0]):
        state[t:t + notif[1]] = "notif"
        t += notif[1] + 10
    assert t < DAY
    powers = {"sleep": sleep[1], "workout": workout[1], "app": app[1], "check": checks[2],
              "notif": notif[2], "aod": aod if aod_on else 0.0}
    energies = {}
    for name, pw in powers.items():
        mask = state == name
        p[mask] += pw
        energies[name] = pw * mask.sum() / 3600.0
    energies["aod_hours"] = (state == "aod").sum() / 3600.0
    p += floor
    energies["floor"] = floor * 24.0
    awake = state != "sleep"
    p[awake] += hr_awake
    energies["hr"] = hr_awake * awake.sum() / 3600.0
    return p, energies


def life_by_stepping(p_rail_mw, e_batt_mwh, eta=0.85, usable=1.0):
    """Hours until the battery is empty under the day's average drain (the chapter's model:
    activities spread over the day), by integrating dE/dt = -P_avg/eta with an event."""
    p_avg = p_rail_mw.mean()  # mW, averaged over the one-second timeline

    def empty(t, y):
        return y[0]
    empty.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [-p_avg / eta], [0, 1e4], [usable * e_batt_mwh],
                              events=empty, rtol=1e-12, atol=1e-9, max_step=10.0)
    return sol.t_events[0][0]


# ---------------------------------------------------------------------------
# Example 27-03.1
# ---------------------------------------------------------------------------
EB = 320 * 3.85
v.check("Ex 27-03.1a", EB)
p1, e1 = day_timeline()
v.check("Ex 27-03.1b", e1["aod_hours"])
v.check("Ex 27-03.1b1", 300 * 4 / 3600)
v.check("Ex 27-03.1b2", 90 * 6 / 3600)
items = {"Ex 27-03.1c1": e1["floor"], "Ex 27-03.1c2": e1["aod"], "Ex 27-03.1c3": e1["check"],
         "Ex 27-03.1c4": e1["notif"], "Ex 27-03.1c5": e1["app"], "Ex 27-03.1c6": e1["workout"],
         "Ex 27-03.1c7": e1["sleep"], "Ex 27-03.1c8": e1["hr"]}
for k, val in items.items():
    v.check(k, val)
EDAY = p1.sum() / 3600.0
v.check("Ex 27-03.1c", EDAY)
v.check("Ex 27-03.1c9", EDAY / 0.85)
v.check("Ex 27-03.1d", EDAY / 0.85 / 24)
L1 = life_by_stepping(p1, EB)
v.check("Ex 27-03.1e", L1)
v.check("Ex 27-03.1e1", life_by_stepping(p1, EB, usable=0.8))
for k, name in [("Ex 27-03.1f1", "workout"), ("Ex 27-03.1f2", "floor"), ("Ex 27-03.1f3", "app"),
                ("Ex 27-03.1f4", "aod"), ("Ex 27-03.1f5", "check"), ("Ex 27-03.1f6", "notif"),
                ("Ex 27-03.1f7", "hr"), ("Ex 27-03.1f8", "sleep")]:
    v.check(k, 100 * e1[name] / EDAY)
p_noaod, _ = day_timeline(aod_on=False)
v.check("Ex 27-03.1g2", p_noaod.sum() / 3600)
L_noaod = life_by_stepping(p_noaod, EB)
v.check("Ex 27-03.1g", L_noaod)
v.check("Ex 27-03.1g5", L_noaod - L1)
p_2h, _ = day_timeline(workout=(2.0, 150.0))
v.check("Ex 27-03.1g3", p_2h.sum() / 3600 - EDAY)
v.check("Ex 27-03.1g4", p_2h.sum() / 3600)
v.check("Ex 27-03.1g1", life_by_stepping(p_2h, EB))
# the lab's closed form agrees
v.assert_true("lab battery_life_h matches stepping",
              abs(wm.battery_life_h(EB, EDAY, 0.85) - L1) < 1e-3)

# ---------------------------------------------------------------------------
# Example 27-03.2: Lambertian flux by numerical integration
# ---------------------------------------------------------------------------
A = 1.4e-3
EFF = 10.0


def flux(lum, area, apl):
    val, _ = integrate.dblquad(lambda th, ph: lum * math.cos(th) * math.sin(th),
                               0, 2 * math.pi, 0, math.pi / 2)
    return val * area * apl


v.assert_true("hemisphere integral equals pi", abs(flux(1, 1, 1) - math.pi) < 1e-9)


def disp(lum, apl, f, p0=2.0, ef=0.3):
    emit = 1e3 * flux(lum, A, apl) / EFF
    return emit, emit + p0 + ef * f


phi_aod = flux(50, A, 0.15)
v.check("Ex 27-03.2a2", phi_aod)
e_aod, d_aod = disp(50, 0.15, 1)
v.check("Ex 27-03.2a", e_aod)
v.check("Ex 27-03.2a3", 2.0 + 0.3 * 1)
v.check("Ex 27-03.2a1", d_aod)
v.check("Ex 27-03.2a4", 7.0 - d_aod)
v.check("Ex 27-03.2b", 2.0 + 0.3 * 60)
_, d_aod60 = disp(50, 0.15, 60)
v.check("Ex 27-03.2b1", d_aod60)
v.check("Ex 27-03.2b2", d_aod60 / d_aod)
e_in, d_in = disp(600, 0.30, 60)
v.check("Ex 27-03.2c", e_in)
v.check("Ex 27-03.2c1", d_in)
e_out, d_out = disp(2000, 0.30, 60)
v.check("Ex 27-03.2d", e_out)
v.check("Ex 27-03.2d1", d_out)
e_w, d_w = disp(50, 1.0, 1)
v.check("Ex 27-03.2e1", e_w)
v.check("Ex 27-03.2e", d_w)
v.check("Txt 27-03.12", e_w / e_aod)
v.assert_true("lab display_power_mw agrees",
              abs(wm.display_power_mw(600, A, 0.3, 10, 2.0, 0.3, 60) - d_in) < 1e-6)

# ---------------------------------------------------------------------------
# Example 27-03.3: count wakes over a simulated hour
# ---------------------------------------------------------------------------
FS, ES, EW, EH, PH = 50, 0.020, 0.5, 0.001, 0.15


def ap_hour(n_batch, es=ES, ew=EW, fs=FS):
    samples = fs * 3600
    wakes = math.ceil(samples / n_batch)
    return (samples * es + wakes * ew) / 3600.0  # mJ/s = mW


def hub_hour(events_per_hour=60):
    samples = FS * 3600
    return (PH * 3600 + samples * EH + events_per_hour * EW) / 3600.0


v.check("Ex 27-03.3a", ap_hour(1))
nmax = max(n for n in range(1, 100) if n / FS <= 0.150 + 1e-12)
v.check("Ex 27-03.3b", nmax)
v.check("Ex 27-03.3b4", 1e3 * nmax / FS)
v.check("Ex 27-03.3b2", FS * ES)
v.check("Ex 27-03.3b3", FS * EW / nmax)
p_ap7 = FS * ES + FS * EW / 7  # exact per-second average (no rounding of the last batch)
v.assert_true("hour count matches average for N=7", abs(ap_hour(7) - p_ap7) < 1e-3)
v.check("Ex 27-03.3b1", p_ap7)
p_hub = hub_hour()
v.check("Ex 27-03.3c", p_hub)
v.check("Ex 27-03.3c2", EW / 60)
v.check("Ex 27-03.3c1", p_ap7 / p_hub)
v.check("Ex 27-03.3d", ap_hour(500))
v.check("Ex 27-03.3d1", ap_hour(1) / 6.0)
v.check("Ex 27-03.3d2", FS * ES / p_hub)

# ---------------------------------------------------------------------------
# Example 27-03.4: BLE event by event
# ---------------------------------------------------------------------------


def octets(payload, phy=1, enc=False):
    pkt = bytearray(b"\xaa" * (1 if phy == 1 else 2))  # preamble
    pkt += b"\x00" * 4  # access address
    pkt += b"\x00" * 2  # header
    pkt += b"\x55" * payload
    if enc and payload > 0:
        pkt += b"\x00" * 4  # MIC
    pkt += b"\x00" * 3  # CRC
    return len(pkt)


def airtime(payload, phy=1, enc=False):
    return 8 * octets(payload, phy, enc) / phy


I_PRE, T_PRE, I_RX, I_TX, T_IFS, I_SL, SCA = 1.2, 250, 3.6, 4.1, 150, 1.5, 100e-6
t_e = airtime(0)
v.check("Ex 27-03.4a1", t_e)
q_pre, q_rx, q_tx = I_PRE * T_PRE, I_RX * (t_e + T_IFS), I_TX * t_e
v.check("Ex 27-03.4a2", q_pre)
v.check("Ex 27-03.4a3", q_rx)
v.check("Ex 27-03.4a4", q_tx)
Q_EV = (q_pre + q_rx + q_tx) / 1000.0
v.check("Ex 27-03.4a", Q_EV)
v.check("Ex 27-03.4b", 1e3 * I_RX * SCA)


def ble_sim(interval_s, latency=0, seconds=3600.0):
    """Average current (uA) from summing each attended event's charge over `seconds`."""
    t_wake = interval_s * (1 + latency)
    n = int(round(seconds / t_wake))
    q = 0.0
    for _ in range(n):
        widen_us = SCA * t_wake * 1e6
        q += Q_EV + I_RX * widen_us / 1000.0  # uC
    return I_SL + q / (n * t_wake)


for k, (T, lat) in {"Ex 27-03.4b1": (0.03, 0), "Ex 27-03.4b2": (0.1, 0),
                    "Ex 27-03.4b3": (1.0, 0), "Ex 27-03.4b4": (0.03, 4)}.items():
    v.check(k, ble_sim(T, lat))
v.check("Ex 27-03.4b5", 1e3 * 0.03 * 5)
i30 = ble_sim(0.03)
v.check("Ex 27-03.4c", 3.0 * i30)
v.check("Ex 27-03.4c1", 3.0 * i30 * 24 / 1000)
v.check("Ex 27-03.4d12", 3.0 * ble_sim(1.0))
v.check("Ex 27-03.4d6", octets(251, 2, True))
t_data = airtime(251, 2, True)
t_ack = airtime(0, 2)
v.check("Ex 27-03.4d", t_data)
v.check("Ex 27-03.4d7", t_ack)
cycle = t_data + T_IFS + t_ack + T_IFS
v.check("Ex 27-03.4d1", cycle)
v.check("Ex 27-03.4d9", 251 * 8)
v.check("Ex 27-03.4d2", 251 * 8 / cycle)  # bits/us = Mb/s
q_pkt = (I_TX * t_data + I_RX * (t_ack + 2 * T_IFS)) / 1000.0
v.check("Ex 27-03.4d8", q_pkt)
v.check("Ex 27-03.4d3", 3.0 * q_pkt)
sent, npk = 0, 0
while sent < 100_000:
    sent += 251
    npk += 1
v.check("Ex 27-03.4d4", npk)
e_up = npk * 3.0 * q_pkt / 1000.0  # mJ
v.check("Ex 27-03.4d5", e_up)
v.check("Ex 27-03.4d10", e_up / 3600.0)
v.assert_true("link-day to upload ratio near two thousand",
              1900 < (3.0 * i30 * 24 / 1000 * 3600) / e_up < 2000)
v.assert_true("lab BLE average agrees",
              abs(wm.ble_avg_current_ua(Q_EV, 0.03, 1.5, 3.6, 100) - i30) < 1e-6)

# ---------------------------------------------------------------------------
# Example 27-03.5: the floor ledger
# ---------------------------------------------------------------------------
bg_rail = 60 * 0.5 * 120 / 3600
ledger = [(2.0, 0.80), (bg_rail, 0.88), (p_hub, 0.75), (0.010 * 1.8, 0.75),
          (3.0 * i30 / 1000, 0.85), (0.5, 0.85), (0.8, 0.85), (0.30, 1.0), (0.025 * 3.85, 1.0)]
batt = [p / e for p, e in ledger]
for k, val in zip(["Ex 27-03.5a1", "Ex 27-03.5a3", "Ex 27-03.5a4", "Ex 27-03.5a6", "Ex 27-03.5a7",
                   "Ex 27-03.5a8", "Ex 27-03.5a9"], [batt[0], batt[1], batt[2], batt[3], batt[4],
                                                     batt[5], batt[6]]):
    v.check(k, val)
v.check("Ex 27-03.5a2", bg_rail)
v.check("Ex 27-03.5a5", 0.010 * 1.8)
v.check("Ex 27-03.5a10", batt[8])
floor_b = math.fsum(batt)
v.check("Ex 27-03.5a", floor_b)
v.check("Ex 27-03.5a11", 6.0 / 0.85)
v.check("Ex 27-03.5b", 6.0 / 0.85 - floor_b)
v.check("Ex 27-03.5b1", 100 * (6.0 / 0.85 - floor_b) / (6.0 / 0.85))
ap_share = 100 * (batt[0] + batt[1]) / floor_b
uw_share = 100 * (batt[2] + batt[3] + batt[4]) / floor_b
v.check("Ex 27-03.5c", ap_share)
v.check("Ex 27-03.5c3", ap_share)
v.check("Ex 27-03.5c1", uw_share)
v.check("Ex 27-03.5c2", uw_share)
dur = 0.2 + 5 * 0.3
v.check("Ex 27-03.5d2", dur)
bg2 = 12 * dur * 120 / 3600
v.check("Ex 27-03.5d", bg2)
v.check("Ex 27-03.5d1", (bg_rail - bg2) / 0.88)
v.check("Ex 27-03.5d3", batt[2] + batt[3] + batt[4])

# ---------------------------------------------------------------------------
# Example 27-03.6: the cell
# ---------------------------------------------------------------------------


def active_by_shell(dims, over):
    total = dims[0] * dims[1] * dims[2]
    inner = [a - t for a, t in zip(dims, over)]
    shell = total - inner[0] * inner[1] * inner[2]
    return total - shell, total


act, tot = active_by_shell((28, 24, 3.6), (3.0, 3.0, 0.25))
v.check("Ex 27-03.6a7", act)
fw = act / tot
v.check("Ex 27-03.6a", fw)
E_cell = act * 1e-6 * 700
v.check("Ex 27-03.6a1", E_cell)
v.check("Ex 27-03.6a2", 1e3 * E_cell / 3.85)
v.check("Ex 27-03.6a3", 700 * fw)
actp, totp = active_by_shell((150, 70, 5.0), (3.0, 3.0, 0.25))
fp = actp / totp
v.check("Ex 27-03.6a4", fp)
v.check("Ex 27-03.6a5", 700 * fp)
v.check("Ex 27-03.6a6", fw / fp)
v.check("Ex 27-03.6a8", 100 * (1 - fw))
v.check("Ex 27-03.6a9", 100 * (1 - fp))
v.assert_true("lab active_fraction agrees",
              abs(wm.active_fraction((28, 24, 3.6), (3.0, 3.0, 0.25)) - fw) < 1e-12)
v.check("Ex 27-03.6b", 3.70 - 0.8 * 0.30)
v.check("Ex 27-03.6b1", 3.70 - 0.8 * 0.90)
imax = optimize.brentq(lambda i: 3.70 - i * 0.90 - 3.20, 0, 5)
v.check("Ex 27-03.6b2", imax)
v.check("Ex 27-03.6b4", 0.8 - imax)
# hold-up capacitor: integrate the excess charge over 1 ms and divide by the droop
q_exc, _ = integrate.quad(lambda t: 0.8 - imax, 0, 1e-3)
v.check("Ex 27-03.6b3", 1e3 * q_exc / 0.1)

# ---------------------------------------------------------------------------
# Text numbers
# ---------------------------------------------------------------------------
v.check("Txt 27-03.1", 8 / 40)
v.check("Txt 27-03.2", 1461 / 24)
v.check("Txt 27-03.3", 2444 / 50)
v.check("Txt 27-03.4", 325 / 30)
v.check("Txt 27-03.5", 455 / 40)
v.check("Txt 27-03.6", 16 / 7)
v.check("Txt 27-03.7", 100 * (1 - 21 / 28))
v.check("Txt 27-03.8", 0.250 * 148)
v.check("Txt 27-03.9", 100 * 23.90 / 150.38)
v.check("Txt 27-03.10", 1 / 0.8)
v.check("Txt 27-03.11", 100 * (1 / 0.8 - 1))
v.check("Txt 27-03.13", ble_sim(10.0))
v.check("Txt 27-03.14", 1.461 / 24 * 1e3)

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
e2 = 455 * 3.87
v.check("27-03.2a", e2)
v.check("27-03.2a1", e2 / 1000)
v.check("27-03.2b", e2 / 40)
v.check("27-03.2c", 0.8 * e2 / 36)

# 27-03.3 with its own timeline
p3, e3 = day_timeline(floor=4.0, aod=0.0, checks=(200, 5, 220.0), notif=(60, 5, 260.0),
                      app=(0.5, 450.0), workout=(0.5, 180.0), sleep=(0.0, 0.0), hr_awake=1.5,
                      aod_on=False)
ED3 = p3.sum() / 3600
v.check("27-03.3a1", e3["check"])
v.check("27-03.3a2", e3["notif"])
v.check("27-03.3a", ED3)
v.check("27-03.3b", ED3 / 0.85)
EB3 = 300 * 3.85
v.check("27-03.3c2", EB3)
L3 = life_by_stepping(p3, EB3)
v.check("27-03.3c", L3)
v.check("27-03.3c1", L3 / 24)
v.check("27-03.3d", 100 * e3["app"] / ED3)
v.check("27-03.3d1", e3["floor"] + e3["hr"])

# 27-03.4 air times
v.check("27-03.4a1", octets(20, 1, True))
v.check("27-03.4a", airtime(20, 1, True))
v.check("27-03.4b2", octets(20, 2, True))
v.check("27-03.4b", airtime(20, 2, True))
v.check("27-03.4c1", octets(251, 1, True))
v.check("27-03.4c", airtime(251, 1, True))
v.check("27-03.4d", 100 * 251 / octets(251, 1, True))
v.check("27-03.4d1", 100 * 20 / octets(20, 1, True))
v.assert_true("lab ble_airtime_us agrees",
              wm.ble_airtime_us(251, 1, True) == airtime(251, 1, True)
              and wm.ble_airtime_us(0, 2) == airtime(0, 2))

# 27-03.5 interval
base = I_SL + 1e3 * I_RX * SCA
v.check("27-03.5a1", base)
v.check("27-03.5a2", 10 - base)
T10 = optimize.brentq(lambda T: ble_sim(T, 0, 3600.0 if T < 10 else 36000.0) - 10, 0.05, 1.0,
                      xtol=1e-9)
v.check("27-03.5a3", T10)
v.check("27-03.5a", 1e3 * T10)
v.check("27-03.5b", ble_sim(0.03, 9))
v.check("27-03.5b1", 1e3 * 0.03 * 10)
v.check("27-03.5b2", 1e3 * 0.03)
v.check("27-03.5c", ble_sim(10.0, 0, 36000.0))

# 27-03.6 display budget
drv60 = 2.0 + 0.3 * 60
v.check("27-03.6a1", drv60)
v.check("27-03.6a2", 150 - drv60)
lmax = optimize.brentq(lambda L: disp(L, 0.40, 60)[1] - 150, 1, 5000)
v.check("27-03.6a", lmax)
sav = disp(600, 0.30, 60)[1] - disp(600, 0.30, 10)[1]
v.check("27-03.6b", sav)
v.check("27-03.6b1", 100 * sav / d_in)

# 27-03.7 pixel hold by integrating the droop ODE


def hold_time(c, dv, i):
    ev = lambda t, y: y[0] - (1.0 - dv)  # noqa: E731
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [-i / c], [0, 1e3], [1.0], events=ev,
                              rtol=1e-12, atol=1e-15, max_step=0.5)
    return sol.t_events[0][0]


th_ltps = hold_time(0.2e-12, 0.01, 0.1e-12)
th_ox = hold_time(0.2e-12, 0.01, 1e-15)
v.check("27-03.7a", th_ltps)
v.check("27-03.7a1", 1 / th_ltps)
v.check("27-03.7b", th_ox)
v.check("27-03.7b1", 1 / th_ox)
c_need = optimize.brentq(lambda c: hold_time(c, 0.01, 0.1e-12) - 1.0, 1e-12, 1e-10)
v.check("27-03.7c", 1e12 * c_need)
v.check("27-03.7c1", c_need / 0.2e-12)

# 27-03.8 batching ties the hub
v.check("27-03.8a2", FS * 0.002)
v.check("27-03.8a3", p_hub - FS * 0.002)
nb = optimize.brentq(lambda n: FS * 0.002 + FS * EW / n - p_hub, 1, 1e5)
v.check("27-03.8a4", nb)
n_int = next(n for n in range(1, 10_000) if FS * 0.002 + FS * EW / n <= p_hub)
v.check("27-03.8a", n_int)
v.check("27-03.8a1", n_int / FS)
p8 = FS * 0.002 + FS * EW / 7
v.check("27-03.8b", p8)
v.check("27-03.8b1", p8 / p_hub)

# 27-03.9 crossover by root finding


def buck_in(i):
    return 0.8 * i / 0.88 + 1.5 * 4.0


def ldo_in(i):
    return 4.0 * (i + 0.3)


icr = optimize.brentq(lambda i: buck_in(i) - ldo_in(i), 0.01, 100)
v.check("27-03.9a", icr)
v.check("27-03.9b2", 0.8 * 100)
v.check("27-03.9b3", 0.8 * 100 / 0.88)
v.check("27-03.9b4", 1.5 * 4.0)
v.check("27-03.9b5", buck_in(100))
v.check("27-03.9b6", ldo_in(100))
v.check("27-03.9b", 100 * 80 / buck_in(100))
v.check("27-03.9b1", 100 * 80 / ldo_in(100))
v.check("27-03.9b7", 100 * 0.8 / 4.0)
v.assert_true("lab crossover agrees",
              abs(wm.buck_ldo_crossover_ua(4.0, 0.8, 0.88, 1.5, 0.3) - icr) < 1e-9)

# 27-03.10 power gating by root finding
saved = lambda t: (20 - 0.5) * t - 60  # noqa: E731  uJ for an idle period t
v.check("27-03.10a1", 20 - 0.5)
v.check("27-03.10a", optimize.brentq(saved, 0, 100))
v.check("27-03.10b2", saved(20))
day_j = 2000 * saved(20) / 1e6
v.check("27-03.10b", day_j)
v.check("27-03.10b1", day_j / 3.6)
v.check("27-03.10b3", 100 * (day_j / 3.6) / EDAY)
v.check("27-03.10c", saved(2))

# 27-03.11 paging: count wakes over a simulated day


def paging_day(cycle):
    wakes = DAY / cycle
    q_uc = 20 * DAY + wakes * 480  # uA*s + uC
    i_avg = q_uc / DAY
    return i_avg, i_avg * 3.85 / 1000, i_avg * 3.85 * 24 / 1000


for c, ks in [(1.28, ("27-03.11a", "27-03.11a1", "27-03.11a2")),
              (20.48, ("27-03.11b", "27-03.11b1", "27-03.11b2"))]:
    vals = paging_day(c)
    for k, val in zip(ks, vals):
        v.check(k, val)
v.check("27-03.11c", 100 * paging_day(1.28)[2] / (EDAY / 0.85))
v.check("27-03.11c1", 100 * paging_day(20.48)[2] / (EDAY / 0.85))

# 27-03.12 solar: integrate the harvest over the sunny hours
p_h, _ = integrate.quad(lambda t: 500 * 3.0e-4 * 0.08 * 1e3, 0, 3)  # mW * h
v.check("27-03.12a", 500 * 3.0e-4 * 0.08 * 1e3)
v.check("27-03.12a1", p_h)
into = 0.8 * p_h
v.check("27-03.12a2", into)
drain12 = EDAY / 0.85 - into
v.check("27-03.12b1", drain12)
L12 = 24 * EB / drain12
v.check("27-03.12b", L12)
v.check("27-03.12b2", 100 * (L12 / L1 - 1))
v.check("27-03.12c", EB / 48)
v.check("27-03.12c1", EB / (48 - into))
v.check("27-03.12d", 48 / (500 * 3.0e-4 * 0.08 * 1e3 * 0.8))
v.check("27-03.12d1", 100 * into / (EDAY / 0.85))
v.check("27-03.12d2", 100 * into / 48)

# 27-03.13 two days
need = optimize.brentq(lambda e: 24 * 0.85 * EB / e - 48, 100, 2000)
v.check("27-03.13a", need)
v.check("27-03.13a1", EDAY - need)
v.check("27-03.13a2", 100 * (EDAY - need) / EDAY)
v.check("27-03.13b", L_noaod)
v.check("27-03.13b1", life_by_stepping(day_timeline(floor=4.0)[0], EB))
v.check("27-03.13b2", life_by_stepping(day_timeline(workout=(1.0, 100.0))[0], EB))
v.check("27-03.13b3", life_by_stepping(day_timeline(app=(0.25, 400.0))[0], EB))
p13c, _ = day_timeline(floor=4.0, workout=(1.0, 100.0), app=(0.25, 400.0))
v.check("27-03.13c3", p13c.sum() / 3600)
v.check("27-03.13c", life_by_stepping(p13c, EB))
eb_need = 2 * (p13c.sum() / 3600) / 0.85
v.check("27-03.13c1", eb_need)
v.check("27-03.13c2", 100 * (eb_need / EB - 1))
v.check("27-03.13c4", 100 * (eb_need / EB - 1))
p13d, _ = day_timeline(floor=4.0, workout=(1.0, 100.0), aod_on=False)
v.check("27-03.13d1", p13d.sum() / 3600)
v.check("27-03.13d", life_by_stepping(p13d, EB))

# 27-03.14 charging
i_ch = 0.8 * 0.320 / 0.75  # A
v.check("27-03.14b1", i_ch)
v.check("27-03.14a", 1e3 * i_ch)
v.check("27-03.14a1", i_ch / 0.320)
v.check("27-03.14b", 1e3 * i_ch ** 2 * 0.30)
p_cell = i_ch * 3.9
v.check("27-03.14c", p_cell)
v.check("27-03.14d", p_cell / 0.70)
v.check("27-03.14d1", p_cell / 0.70 - p_cell)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
L4 = life_by_stepping(day_timeline(floor=4.0)[0], EB)
v.check("Lab 27-03.a", L4)
v.check("Lab 27-03.a1", (L4 - L1) / 2.0)
tb = optimize.brentq(lambda T: (ble_sim(T, 0, 7200.0) - base) - base, 0.1, 5.0, xtol=1e-9)
v.check("Lab 27-03.b", tb)
v.check("Lab 27-03.c", disp(50, 0.15, 10)[1])
nd = next(n for n in range(1, 100_000) if FS * 0.003 + FS * EW / n <= p_hub)
v.check("Lab 27-03.d", nd)
v.check("Lab 27-03.d1", nd / FS)
v.assert_true("lab batch_for_power agrees", wm.batch_for_power(FS, 0.003, EW, p_hub) == nd)

sys.exit(v.finish())
