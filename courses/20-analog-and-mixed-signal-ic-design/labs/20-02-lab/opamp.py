"""Lab 20-02: design and analysis helpers for two-stage (and three-stage) CMOS op-amps.

The device model is the charge-based model of chapter 20-01 (imported from ../20-01-lab/gmid.py). The circuit models
are the small-signal node models derived in chapter 20-02, section 3:

* Miller compensation with a nulling resistor: two high-impedance nodes (first-stage output, R1 || C1; output,
  R2 || C_L) joined by C_c in series with R_z;
* indirect (cascode) compensation: C_c returns to the low-impedance source node x of a cascode device of
  transconductance g_mc, through which the first stage's signal current flows;
* nested Miller compensation of a three-stage amplifier, C_m1 around stages 2-3 and C_m2 around stage 3.

All quantities are SI (A, V, S, F, Hz, rad/s) unless a name says otherwise. The T130 process is an illustrative
teaching process, not a foundry's.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "20-01-lab"))
import gmid as g  # noqa: E402

K_B = 1.380649e-23
TN = g.Process()                          # T130 NMOS (chapter 20-01)
TP = g.Process(mu=100e-4, vsat=6e4)       # T130 PMOS: mu_p = 100 cm^2/V s, v_sat = 6e6 cm/s, |V_TH| = 0.45 V


# ---------------------------------------------------------------- small device helpers
def vdsat(q: float, vt: float, frac: float = 0.02) -> float:
    """Saturation voltage in the long-channel charge model: the V_DS at which the drain (reverse) component of the
    current, I_spec (q_d^2 + q_d), has fallen to `frac` of the source (forward) component I_spec (q_s^2 + q_s), so the
    current is within frac of its saturated value. V_DS = V_T [2 (q_s - q_d) + ln(q_s / q_d)].
    Weak inversion: ln(1/frac) V_T (3.9 V_T for 2 %); strong inversion: about 0.86 V_P + 2 V_T."""
    qd = (math.sqrt(1 + 4 * frac * (q * q + q)) - 1) / 2
    return vt * (2 * (q - qd) + math.log(q / qd))


def q_for_gmid(gmid: float, proc: g.Process, length: float) -> float:
    return g.q_of_ic(g.ic_for_gm_over_id(gmid, proc, length), proc.lam(length))


def ic_same_vgs(q: float, proc: g.Process, length: float) -> float:
    """Inversion coefficient of a device at another length biased at the same V_GS (same normalized charge q)."""
    return g.ic_of_q(q, proc.lam(length))


# ---------------------------------------------------------------- specification and design choices
@dataclass
class Spec:
    vdd: float = 1.2            # V
    cl: float = 2e-12           # F
    gbw: float = 50e6           # Hz, g_m1 / (2 pi C_c)
    pm: float = 60.0            # degrees, unity-gain follower
    sr: float = 30e6            # V/s
    a0_db: float = 60.0         # dB
    noise: float = 15e-9        # V/sqrt(Hz), white (thermal) input-referred
    swing: float = 0.7          # V peak-to-peak at the output
    vcm: float = 0.4            # V, input common mode
    temp: float = 300.0         # K
    gamma: float = 2 / 3        # channel-noise factor (12-10's convention)


@dataclass
class Choices:
    gmid1: float = 18.0         # S/A, PMOS input pair
    gmid6: float = 10.0         # S/A, NMOS second stage
    gmid7: float = 10.0         # S/A, PMOS current source of the second stage
    l1: float = 1e-6
    l3: float = 1e-6
    l5: float = 1e-6
    l6: float = 0.5e-6
    l7: float = 0.5e-6
    cc: float = 0.6e-12         # F
    cp: float = 30e-15          # F, node-1 capacitance besides M6's gate (junctions, wiring)
    k2: float = 2.0             # target p2 / omega_u
    nmos: g.Process = field(default_factory=lambda: TN)
    pmos: g.Process = field(default_factory=lambda: TP)


def gm6_for_p2(p2: float, cc: float, cl: float, cp: float, wt6: float) -> float:
    """g_m6 that puts p2 = g_m6 C_c / [C1 (C_L + C_c) + C_c C_L] at p2 when C1 = C_p + g_m6 / omega_T6."""
    den = cc - p2 * (cl + cc) / wt6
    if den <= 0:
        raise ValueError("p2 target exceeds the f_T bound omega_T6 C_c / (C_L + C_c)")
    return p2 * (cp * (cl + cc) + cc * cl) / den


def total_current(cc: float, spec: Spec, ch: Choices) -> float:
    """I_SS + I_6 as a function of C_c (Section 3.3's optimization)."""
    wu = 2 * math.pi * spec.gbw
    ic6 = g.ic_for_gm_over_id(ch.gmid6, ch.nmos, ch.l6)
    wt6 = 2 * math.pi * g.ft(ic6, ch.nmos, ch.l6)
    return 2 * wu * cc / ch.gmid1 + gm6_for_p2(ch.k2 * wu, cc, spec.cl, ch.cp, wt6) / ch.gmid6


def optimum_cc(spec: Spec, ch: Choices, lo: float = 0.3e-12, hi: float = 3e-12) -> float:
    r = minimize_scalar(lambda c: total_current(c, spec, ch), bounds=(lo, hi), method="bounded",
                        options={"xatol": 1e-17})
    return float(r.x)


def design_two_stage(spec: Spec | None = None, ch: Choices | None = None) -> dict:
    """The design procedure of Section 3.8, returning every intermediate quantity."""
    spec, ch = spec or Spec(), ch or Choices()
    tn, tp, vt = ch.nmos, ch.pmos, ch.nmos.vt
    d: dict = {}
    wu = 2 * math.pi * spec.gbw
    d["wu"] = wu
    # first stage
    d["gmid1_max"] = 2 * wu / spec.sr
    d["gm1"] = gm1 = wu * ch.cc
    d["id1"] = id1 = gm1 / ch.gmid1
    d["iss"] = iss = 2 * id1
    d["sr"] = iss / ch.cc
    d["ic1"] = ic1 = g.ic_for_gm_over_id(ch.gmid1, tp, ch.l1)
    d["w1"] = id1 / g.id_per_w(ic1, tp, ch.l1)
    d["vov1"] = g.vov_of_ic(ic1, tp.n, vt, tp.lam(ch.l1))
    # second stage
    d["ic6"] = ic6 = g.ic_for_gm_over_id(ch.gmid6, tn, ch.l6)
    d["ft6"] = ft6 = g.ft(ic6, tn, ch.l6)
    wt6 = 2 * math.pi * ft6
    d["p2max"] = wt6 * ch.cc / (spec.cl + ch.cc)
    d["gm6"] = gm6 = gm6_for_p2(ch.k2 * wu, ch.cc, spec.cl, ch.cp, wt6)
    d["gm6_naive"] = ch.k2 * wu * spec.cl
    d["i6"] = i6 = gm6 / ch.gmid6
    d["w6"] = i6 / g.id_per_w(ic6, tn, ch.l6)
    d["cgg6"] = cgg6 = gm6 / wt6
    d["c1"] = c1 = ch.cp + cgg6
    d["vov6"] = g.vov_of_ic(ic6, tn.n, vt, tn.lam(ch.l6))
    # mirror M3/M4: same V_GS as M6 (zero systematic offset)
    q6 = g.q_of_ic(ic6, tn.lam(ch.l6))
    d["ic3"] = ic3 = ic_same_vgs(q6, tn, ch.l3)
    d["gmid3"] = gmid3 = g.gm_over_id(ic3, tn.n, vt, tn.lam(ch.l3))
    d["w3"] = id1 / g.id_per_w(ic3, tn, ch.l3)
    # PMOS sources M7 and M5 share one bias (same V_SG)
    d["ic7"] = ic7 = g.ic_for_gm_over_id(ch.gmid7, tp, ch.l7)
    d["w7"] = i6 / g.id_per_w(ic7, tp, ch.l7)
    q7 = g.q_of_ic(ic7, tp.lam(ch.l7))
    d["ic5"] = ic5 = ic_same_vgs(q7, tp, ch.l5)
    d["w5"] = iss / g.id_per_w(ic5, tp, ch.l5)
    # gain
    va = lambda proc, length: proc.va_per_l * length  # noqa: E731
    d["r1"] = r1 = 1 / (id1 / va(tp, ch.l1) + id1 / va(tn, ch.l3))
    d["r2"] = r2 = 1 / (i6 / va(tn, ch.l6) + i6 / va(tp, ch.l7))
    d["a1"] = gm1 * r1
    d["a2"] = gm6 * r2
    d["a0"] = gm1 * r1 * gm6 * r2
    d["a0_db"] = 20 * math.log10(d["a0"])
    # swing and input common-mode range
    q1, q5 = g.q_of_ic(ic1, tp.lam(ch.l1)), g.q_of_ic(ic5, tp.lam(ch.l5))
    d["vdsat1"], d["vdsat5"] = vdsat(q1, vt), vdsat(q5, vt)
    d["vdsat6"], d["vdsat7"] = vdsat(q6, vt), vdsat(q7, vt)
    d["vout_min"] = d["vdsat6"]
    d["vout_max"] = spec.vdd - d["vdsat7"]
    d["swing"] = d["vout_max"] - d["vout_min"]
    vsg1 = tp.vth + d["vov1"]
    vgs3 = tn.vth + g.vov_of_ic(ic3, tn.n, vt, tn.lam(ch.l3))
    d["vcm_max"] = spec.vdd - d["vdsat5"] - vsg1
    d["vcm_min"] = vgs3 + d["vdsat1"] - vsg1
    # noise, power, figure of merit
    kt = K_B * spec.temp
    d["noise"] = math.sqrt(8 * kt * spec.gamma / gm1 * (1 + gmid3 / ch.gmid1))
    d["itot"] = iss + i6
    d["power"] = spec.vdd * d["itot"]
    d["fom_s"] = (spec.gbw / 1e6) * (spec.cl / 1e-12) / (d["itot"] / 1e-3)
    d["rz"] = 1 / gm6
    d["rz_cancel"] = (1 + spec.cl / ch.cc) / gm6
    return d


# ---------------------------------------------------------------- transfer functions and margins
def miller_tf(gm1, gm2, r1, r2, c1, cl, cc, rz=0.0):
    """(num, den) polynomials in s, highest power first, for the Miller-compensated two-stage amplifier."""
    a1 = gm2 * r1 * r2 * cc + r2 * (cl + cc) + r1 * (c1 + cc) + rz * cc
    a2 = r1 * r2 * (c1 * cl + cc * (c1 + cl)) + rz * cc * (c1 * r1 + cl * r2)
    a3 = r1 * r2 * rz * c1 * cl * cc
    a0 = gm1 * gm2 * r1 * r2
    num = a0 * np.array([-cc * (1 / gm2 - rz), 1.0])
    den = np.array([a3, a2, a1, 1.0]) if rz > 0 else np.array([a2, a1, 1.0])
    return num, den


def nodal_tf(ymat, bvec, out_index: int):
    """Return H(s) for a nodal model: Y(s) v = b, output node out_index."""
    def h(s: complex) -> complex:
        return np.linalg.solve(ymat(s), bvec)[out_index]
    return h


def indirect_tf(gm1, gm2, gmc, r1, r2, rx, c1, cl, cc, cx):
    """Indirect compensation: nodes (1, x, out); the first stage's current gm1 v_in leaves node x."""
    g1, g2, gx = 1 / r1, 1 / r2, 1 / rx

    def y(s):
        return np.array([[g1 + s * c1, -gmc, 0],
                         [0, gmc + gx + s * (cx + cc), -s * cc],
                         [gm2, -s * cc, g2 + s * (cl + cc)]], dtype=complex)
    return nodal_tf(y, np.array([0, -gm1, 0], dtype=complex), 2)


def nmc_tf(gm1, gm2, gm3, r1, r2, r3, cn1, cn2, cl, cm1, cm2):
    """Nested Miller: stage 1 and 2 non-inverting, stage 3 inverting; C_m1 node1-out, C_m2 node2-out."""
    g1, g2, g3 = 1 / r1, 1 / r2, 1 / r3

    def y(s):
        return np.array([[g1 + s * (cn1 + cm1), 0, -s * cm1],
                         [-gm2, g2 + s * (cn2 + cm2), -s * cm2],
                         [-s * cm1, gm3 - s * cm2, g3 + s * (cl + cm1 + cm2)]], dtype=complex)
    return nodal_tf(y, np.array([gm1, 0, 0], dtype=complex), 2)


def poly_tf(num, den):
    return lambda s: np.polyval(num, s) / np.polyval(den, s)


def margins(h, f_lo: float = 1e2, f_hi: float = 1e11, points: int = 40001) -> dict:
    """Crossover, phase margin and gain margin of a loop gain h(s) whose DC value is positive."""
    f = np.logspace(math.log10(f_lo), math.log10(f_hi), points)
    hv = np.array([h(2j * math.pi * x) for x in f])
    if hv[0].real < 0:                       # a loop gain is positive at DC; flip an inverting model's sign
        hv = -hv
    ph = np.unwrap(np.angle(hv))
    mag = np.abs(hv)
    i = int(np.where(mag < 1)[0][0])
    fc = brentq(lambda x: abs(h(2j * math.pi * x)) - 1, f[i - 1], f[i])
    pm = 180 + math.degrees(np.interp(math.log10(fc), np.log10(f), ph))
    out = {"fc": fc, "pm": pm, "f180": None, "gm_db": None}
    j = np.where(ph < -math.pi)[0]
    if len(j):
        j = int(j[0])
        f180 = 10 ** np.interp(-math.pi, [ph[j], ph[j - 1]], [math.log10(f[j]), math.log10(f[j - 1])])
        out["f180"] = f180
        out["gm_db"] = -20 * math.log10(abs(h(2j * math.pi * f180)))
    out["sign"] = 1 if hv[0].real > 0 else -1
    return out


# ---------------------------------------------------------------- settling, gain boosting, CMFB
def two_pole_pm(k: float) -> float:
    """Exact phase margin of omega_u / [s (1 + s / (k omega_u))]."""
    x2 = (math.sqrt(1 + 4 / k ** 2) - 1) * k ** 2 / 2      # (omega_c / omega_u)^2
    return 90 - math.degrees(math.atan(math.sqrt(x2) / k))


def settle_time(num, den, eps: float, t_end: float, n: int = 400001) -> float:
    """Time after which |step response - final value| stays below eps (final value 1)."""
    from scipy import signal
    t = np.linspace(0, t_end, n)
    _, y = signal.step((num, den), T=t)
    bad = np.where(np.abs(y - 1) > eps)[0]
    return 0.0 if len(bad) == 0 else float(t[bad[-1] + 1])


def slew_plus_linear(v_step: float, sr: float, tau: float, eps: float) -> tuple[float, float]:
    """Single-pole settling with slewing: (slewing time, linear settling time) to a final error eps * v_step."""
    if v_step / tau <= sr:
        return 0.0, tau * math.log(1 / eps)
    t_slew = (v_step - sr * tau) / sr
    t_lin = tau * math.log(sr * tau / (eps * v_step))
    return t_slew, t_lin


def cmfb_cycles(c1: float, c2: float, reduction: float) -> float:
    """Clock cycles for a switched-capacitor CMFB's DC error to shrink by `reduction` (ratio C1/(C1+C2) per cycle)."""
    return math.log(reduction) / math.log((c1 + c2) / c1)


if __name__ == "__main__":
    d = design_two_stage()
    for key in ("gm1", "iss", "sr", "w1", "gm6", "i6", "w6", "c1", "a0_db", "swing", "noise", "itot", "fom_s"):
        print(f"{key:8s} {d[key]:.4g}")
    num, den = miller_tf(d["gm1"], d["gm6"], d["r1"], d["r2"], d["c1"], Spec().cl, Choices().cc, d["rz"])
    print(margins(poly_tf(num, den)))
