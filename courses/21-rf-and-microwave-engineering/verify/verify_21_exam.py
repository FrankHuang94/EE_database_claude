#!/usr/bin/env python3
"""Verify every number in the Course 21 final-exam solutions.

Answers with a non-trivial route are recomputed independently; closed-form arithmetic is re-evaluated directly:
- reflection, S-parameters and absorbed power by solving the driven circuit for its port voltages and currents;
  Delta as a matrix determinant; mu as the smallest unstable load magnitude found by search; G_max by numerically
  maximizing the transducer gain over all passive source and load terminations; Gamma_in through the Z-matrix;
- the L-network by solving for L and C that present 5 ohms, and its bandwidth by sweeping the exact network;
- the cascade IIP3 by an FFT two-tone simulation of cascaded cubic stages; noise figure through noise temperatures;
- the LNA's match, Q_in, G_m and noise figure from phasor solutions of its small-signal loop equations;
- mixer gains and harmonic responses from numerical Fourier coefficients of the LO waveforms; IRR from I/Q phasors;
- the tank in parallel-loss form; the oscillator amplitude by numerical Fourier integration; phase noise from the
  Leeson form 2kT/P_s (omega_0/2Q d omega)^2;
- PA efficiencies by numerical integration of the clipped-cosine current; the ACLR limit in linear units, with the
  cubic ACLR law itself confirmed by a Monte Carlo complex-Gaussian simulation; OFDM average efficiencies by
  integrating over a clipped Rayleigh envelope;
- the N-path filter's bandwidth and centre gain confirmed by a time-domain switched-RC simulation;
- the preselector from scipy's analog Butterworth band-pass design;
- the BAW coupling from the Butterworth-Van Dyke impedance's numerically located resonances;
- switch loss and isolation from the ABCD matrix of the series element;
- the array's beam direction by maximizing its array factor, the squint bandwidth from the exact array factor,
  and quantization loss by integrating over the phase-error distribution;
- range, margins, rates, ranging error and Doppler from their definitions (Doppler from orbit geometry);
- the derivations' results by root finding and numerical minimization.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, signal, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, polar  # noqa: E402

v = Verifier.from_files("21-exam", ROOT / "exam" / "solutions.md")
lg = math.log10
TWO_PI = 2 * math.pi
Z0 = 50.0
C0 = 299_792_458.0
rng = np.random.default_rng(21)


def db(x: float) -> float:
    return 10 * lg(x)


def idb(x: float) -> float:
    return 10 ** (x / 10)


def s21_series(z: complex) -> complex:
    """S21 of a series impedance between Z0 ports, from its ABCD matrix [[1, Z], [0, 1]]."""
    a, b, c, d = 1, z, 0, 1
    return 2 / (a + b / Z0 + c * Z0 + d)


# ---------------------------------------------------------------- Q1: S-parameters
# (a) Drive the load from a matched source and form the power waves from V and I.
vs = 1.0
zl = 25.0
i_l = vs / (Z0 + zl)
v_l = i_l * zl
a_w = (v_l + Z0 * i_l) / (2 * math.sqrt(Z0))
b_w = (v_l - Z0 * i_l) / (2 * math.sqrt(Z0))
gam = b_w / a_w
v.check("X21.1a", gam)
v.check("X21.1b", -20 * lg(abs(gam)))
z = np.linspace(0, 1, 2001)  # one wavelength of standing wave
vz = np.abs(np.exp(1j * TWO_PI * z) + gam * np.exp(-1j * TWO_PI * z))
v.check("X21.1c", vz.max() / vz.min())
p_load = 0.5 * abs(i_l) ** 2 * zl
p_avail = vs**2 / (8 * Z0)
v.check("X21.1d", -db(p_load / p_avail))

# (b) Series 20 ohm: solve the circuit with port 2 terminated.
r = 20.0
i1 = vs / (Z0 + r + Z0)
v1 = vs - Z0 * i1
v2 = i1 * Z0
s11 = (v1 - Z0 * i1) / (v1 + Z0 * i1)
s21 = 2 * v2 / vs
v.check("X21.1e", s11)
v.check("X21.1f", s21)
v.check("X21.1g", -20 * lg(abs(s21)))
v.check("X21.1h", 0.5 * i1**2 * r / p_avail)

# (c) The transistor.
S = np.array([[polar(0.5, -140), polar(0.04, 40)], [polar(4.0, 80), polar(0.45, -45)]])
S11, S12, S21, S22 = S[0, 0], S[0, 1], S[1, 0], S[1, 1]
delta = np.linalg.det(S)
v.check("X21.1i", abs(delta))
k_fac = (1 - abs(S11) ** 2 - abs(S22) ** 2 + abs(delta) ** 2) / (2 * abs(S12 * S21))
v.check("X21.1j", k_fac)


def gin(gl: complex) -> complex:
    return S11 + S12 * S21 * gl / (1 - S22 * gl)


# mu (load side) is the distance from the origin to the nearest load that makes |Gamma_in| >= 1.
def first_unstable_radius(phi: float) -> float:
    rr = np.linspace(0.0, 5.0, 5001)
    m = np.abs(gin(rr * np.exp(1j * phi))) >= 1
    if not m.any():
        return np.inf
    i = int(np.argmax(m))
    return optimize.brentq(lambda q: abs(gin(q * np.exp(1j * phi))) - 1, rr[i - 1], rr[i], xtol=1e-14)


phis = np.linspace(0, TWO_PI, 3601)
radii = np.array([first_unstable_radius(p) for p in phis])
best = radii.min()
p0 = phis[int(np.argmin(radii))]
mu_fine = optimize.minimize_scalar(first_unstable_radius, bounds=(p0 - 0.01, p0 + 0.01), method="bounded",
                                   options={"xatol": 1e-12}).fun
v.assert_true("mu search agrees with the grid", abs(mu_fine - best) < 2e-3, f"{mu_fine} vs {best}")
v.check("X21.1k", mu_fine)
v.check("X21.1p", abs(S22 - delta * np.conj(S11)))
# Unconditional stability: no passive load or source gives |Gamma| >= 1 at the other port.
disk = np.array([rr * np.exp(1j * p) for rr in np.linspace(0, 1, 101) for p in np.linspace(0, TWO_PI, 181)])
gout = S22 + S12 * S21 * disk / (1 - S11 * disk)
v.assert_true("unconditionally stable over the passive disk",
              np.all(np.abs(gin(disk)) < 1) and np.all(np.abs(gout) < 1))
v.check("X21.1l", db(abs(S21 / S12)))


def neg_gt(x):
    gs = x[0] * np.exp(1j * x[1])
    gl = x[2] * np.exp(1j * x[3])
    num = (1 - abs(gs) ** 2) * abs(S21) ** 2 * (1 - abs(gl) ** 2)
    den = abs((1 - S11 * gs) * (1 - S22 * gl) - S12 * S21 * gs * gl) ** 2
    return -num / den


best_gt = min((optimize.minimize(neg_gt, x0, bounds=[(0, 0.999), (-10, 10), (0, 0.999), (-10, 10)],
                                 method="L-BFGS-B") for x0 in
               ([0.5, 2.4, 0.5, 0.8], [0.7, 2.0, 0.6, 1.0], [0.3, -2.0, 0.3, 0.5])), key=lambda res: res.fun)
v.check("X21.1m", db(-best_gt.fun))
v.check("X21.1q", -best_gt.fun / abs(S21 / S12))  # G_max / MSG = K - sqrt(K^2 - 1)

# (d) Gamma_in through the Z-matrix: Z = Z0 (I + S)(I - S)^-1, terminate, convert back.
I2 = np.eye(2)
Zm = Z0 * (I2 + S) @ np.linalg.inv(I2 - S)
zload = Z0 * (1 + polar(0.5, 60)) / (1 - polar(0.5, 60))
zin = Zm[0, 0] - Zm[0, 1] * Zm[1, 0] / (Zm[1, 1] + zload)
g_in = (zin - Z0) / (zin + Z0)
v.check("X21.1n", abs(g_in))
v.check("X21.1o", math.degrees(np.angle(g_in)))

# ---------------------------------------------------------------- Q2: matching a PA
f0 = 2.4e9
w0 = TWO_PI * f0
R_PA = 4.0


def zin_l(lv: float, cv: float, w) -> complex:
    """Input impedance seen by the 4 ohm PA: series L, then shunt C across 50 ohms."""
    return 1j * w * lv + 1 / (1 / 50 + 1j * w * cv)


sol = optimize.fsolve(lambda p: [zin_l(p[0] * 1e-9, p[1] * 1e-12, w0).real - R_PA,
                                 zin_l(p[0] * 1e-9, p[1] * 1e-12, w0).imag], [1.0, 4.0], xtol=1e-13)
l_mat, c_mat = sol[0] * 1e-9, sol[1] * 1e-12
v.check("X21.2a", (w0 * l_mat) / R_PA)  # Q = X_series / R_low
v.check("X21.2b", l_mat * 1e9)
v.check("X21.2c", c_mat * 1e12)
qn = w0 * l_mat / R_PA
v.check("X21.2d", f0 * 2 * 0.1 * math.sqrt(1 + qn**2) / qn**2 / 1e6)
v.check("X21.2e", f0 * 2 * 0.1 / qn / 1e6)
fs_ = np.linspace(2.0e9, 2.8e9, 800_001)
zz = zin_l(l_mat, c_mat, TWO_PI * fs_)
good = fs_[np.abs((zz - R_PA) / (zz + R_PA)) <= 0.1]
v.check("X21.2k", (good.max() - good.min()) / 1e6)
rm = math.exp((math.log(R_PA) + math.log(50)) / 2)
v.check("X21.2f", rm)
v.check("X21.2g", math.sqrt(rm / R_PA - 1))
v.check("X21.2h", db(1 + qn / 20))
v.check("X21.2i", 2 * db(1 + math.sqrt(50 / rm - 1) / 20))
v.check("X21.2n", db(1 + math.sqrt(100 - 1) / 20))
v.check("X21.2o", 2 * db(1 + math.sqrt(math.sqrt(100) - 1) / 20))
# Binomial two-section transformer: log steps weighted by C(2, n)/2^2, then checked by an exact line cascade.
weights = [math.comb(2, i) / 4 for i in range(3)]
z_sec = [R_PA * math.exp(sum(weights[: i + 1]) * math.log(50 / R_PA)) for i in range(2)]
v.check("X21.2l", z_sec[0])
v.check("X21.2m", z_sec[1])


def zin_lines(f: float) -> complex:
    """Exact input impedance of the two quarter-wave lines (quarter-wave at f0) loaded by 50 ohms."""
    zl_ = 50.0
    th_ = (math.pi / 2) * f / f0
    for zc in reversed(z_sec):
        zl_ = zc * (zl_ + 1j * zc * math.tan(th_)) / (zc + 1j * zl_ * math.tan(th_))
    return zl_


v.assert_true("binomial transformer is matched at f0", abs(zin_lines(f0) - R_PA) < 1e-9)
g_lines = [abs((zin_lines(f) - R_PA) / (zin_lines(f) + R_PA)) for f in (0.95 * f0, 1.05 * f0)]
v.assert_true("binomial transformer is flat near f0 (|Gamma| < 0.02 at +-5%)", max(g_lines) < 0.02, str(g_lines))
v.check("X21.2j", 1 / (2 * R_PA * 40e-12 * math.log(1 / 0.1)) / 1e9)
v.assert_true("the L-network's band is inside the Bode-Fano limit", (good.max() - good.min()) < 1.357e9)

# ---------------------------------------------------------------- Q3: receiver cascade
T0 = 290.0
stages = [(idb(16), idb(1.8)), (1 / idb(2.5), idb(2.5)), (idb(10), idb(9))]
temps = [T0 * (f - 1) for _, f in stages]
te = temps[0] + temps[1] / stages[0][0] + temps[2] / (stages[0][0] * stages[1][0])
f_tot = 1 + te / T0
v.check("X21.3a", db(f_tot))


def cubic_stage(gain_db: float, iip3_dbm: float):
    """Voltage-mode cubic stage in 50 ohms: y = a1 x + a3 x^3 with A_IIP3^2 = (4/3)|a1/a3|."""
    a1 = 10 ** (gain_db / 20)
    a_iip3 = math.sqrt(2 * 50 * idb(iip3_dbm) / 1e3)
    a3 = -4 * a1 / (3 * a_iip3**2)
    return lambda x: a1 * x + a3 * x**3


lna = cubic_stage(16, -8)
mix = cubic_stage(10, 3)
nfft = 4096
n = np.arange(nfft)
k1, k2 = 200, 220
a_in = math.sqrt(2 * 50 * idb(-60) / 1e3)  # -60 dBm per tone
x = a_in * (np.cos(TWO_PI * k1 * n / nfft) + np.cos(TWO_PI * k2 * n / nfft))
y = mix(lna(x) * 10 ** (-2.5 / 20))
spec = np.abs(np.fft.rfft(y)) / (nfft / 2)
p_fund = 20 * lg(spec[k1])
p_im3 = 20 * lg(spec[2 * k1 - k2])
iip3_sim = -60 + (p_fund - p_im3) / 2
v.check("X21.3b", iip3_sim)
v.check("X21.3f", idb(iip3_sim))
nf = db(f_tot)
noise = -174 + db(20e6) + nf
v.check("X21.3c", noise + 5)
v.check("X21.3d", 2 / 3 * (iip3_sim - noise))
th = T0 * (idb(15) + 1)
v.check("X21.3e", db((th + te) / (T0 + te)))
v.check("X21.3g", db(th / T0))  # noiseless receiver: T_e = 0

# ---------------------------------------------------------------- Q4: the LNA
f0 = 5.5e9
w0 = TWO_PI * f0
wt = TWO_PI * 55e9
cgs = 150e-15
gm = wt * cgs
rs = 50.0


def lna_solve(ls: float, lg_: float, r_g: float):
    """Phasor solution of the gate loop. Returns (Z_in, i_out per v_s, i_out per i_n, |v_gs/v_s|)."""
    zloop = r_g + 1j * w0 * (lg_ + ls) + 1 / (1j * w0 * cgs) + gm * ls / cgs
    zin = zloop
    i_s = 1 / (rs + zloop)  # loop current per unit source EMF
    hs = gm * i_s / (1j * w0 * cgs)
    # drain noise current i_n: loop current i satisfies i (rs + zloop) = -j w ls i_n
    i_n = -1j * w0 * ls / (rs + zloop)
    hn = gm * i_n / (1j * w0 * cgs) + 1
    qin = abs(i_s / (1j * w0 * cgs))
    return zin, hs, hn, qin


def match(r_g: float):
    def eqs(p):
        zin = lna_solve(p[0] * 1e-12, p[1] * 1e-9, r_g)[0]
        return [zin.real - rs, zin.imag]
    p = optimize.fsolve(eqs, [140.0, 5.4], xtol=1e-13)
    return p[0] * 1e-12, p[1] * 1e-9


ls0, lg0 = match(0.0)
v.check("X21.4a", ls0 * 1e12)
v.check("X21.4b", lg0 * 1e9)
_, hs0, hn0, qin0 = lna_solve(ls0, lg0, 0.0)
v.check("X21.4c", qin0)
v.check("X21.4d", abs(hs0) * 1e3)
v.check("X21.4e", 5 - 20 * lg(qin0))
v.check("X21.4f", gm * 1e3)
kt0 = 1.380649e-23 * T0
f_ideal = 1 + abs(hn0) ** 2 * 4 * kt0 * gm / (abs(hs0) ** 2 * 4 * kt0 * rs)  # gamma*g_d0 = (gamma/alpha) g_m
v.check("X21.4g", db(f_ideal))
rg = w0 * lg0 / 20
v.check("X21.4h", rg)
# Re-match with the loss resistance fixed at the value from part (a)'s L_g.
ls1 = optimize.brentq(lambda q: lna_solve(q, lg0, rg)[0].real - rs, 1e-12, 1e-9)
v.check("X21.4i", ls1 * 1e12)
lg1 = 1 / (w0**2 * cgs) - ls1
_, hs1, hn1, _ = lna_solve(ls1, lg1, rg)
f_lossy = 1 + (abs(hs1) ** 2 * 4 * kt0 * rg + abs(hn1) ** 2 * 4 * kt0 * gm) / (abs(hs1) ** 2 * 4 * kt0 * rs)
v.check("X21.4j", db(f_lossy))
g_need = optimize.brentq(lambda g: f_lossy + (10 - 1) / g - f_lossy * 10**0.05, 1, 1e4)
v.check("X21.4k", db(g_need))
v.check("X21.4l", g_need)

# ---------------------------------------------------------------- Q5: mixers


def fourier(fn, harmonic: int) -> float:
    """Cosine Fourier coefficient of a 2*pi-periodic waveform."""
    return integrate.quad(lambda t: fn(t) * math.cos(harmonic * t), -math.pi, math.pi, limit=400,
                          points=[-3 * math.pi / 4, -math.pi / 2, -math.pi / 4, 0, math.pi / 4, math.pi / 2,
                                  3 * math.pi / 4])[0] / math.pi


def square(t: float) -> float:
    return 1.0 if math.cos(t) >= 0 else -1.0


b1 = fourier(square, 1)
gc = b1 / 2  # the product's difference term carries half the LO fundamental
v.check("X21.5a", 20 * lg(gc))
v.check("X21.5b", 20 * lg(gc * 25e-3 * 400))
v.check("X21.5c", db(1 / gc**2))
eps = 10 ** (0.3 / 20) - 1
v.check("X21.5d", eps)
phase = math.radians(3)
wanted = abs(1 + (1 + eps) * np.exp(1j * phase)) ** 2
image = abs(1 - (1 + eps) * np.exp(1j * phase)) ** 2
v.check("X21.5e", db(wanted / image))
v.check("X21.5k", wanted / image)
v.check("X21.5f", db(4 / (eps**2 + phase**2)))
v.check("X21.5g", 20 * lg(abs(fourier(square, 3)) / b1))


def hr_lo(t: float) -> float:
    s45 = math.pi / 4
    return square(t - s45) + math.sqrt(2) * square(t) + square(t + s45)


v.assert_true("HR LO cancels the 3rd and 5th", abs(fourier(hr_lo, 3)) < 1e-9 and abs(fourier(hr_lo, 5)) < 1e-9)
v.check("X21.5h", 20 * lg(abs(fourier(hr_lo, 7)) / abs(fourier(hr_lo, 1))))
npath, cpath = 6, 25e-12
tau = npath * rs * cpath  # each capacitor is connected for 1/N of the period
f3 = optimize.brentq(lambda f: abs(1 / (1 + 1j * TWO_PI * f * tau)) - 1 / math.sqrt(2), 1, 1e9)
v.check("X21.5i", 2 * f3 / 1e6)
held = integrate.quad(math.cos, -math.pi / npath, math.pi / npath)[0] / (TWO_PI / npath)
v.check("X21.5j", 20 * lg(held**2))


def npath_sim(df: float, f_lo: float = 1e9, steps: int = 240, periods: int = 400) -> float:
    """Time-domain N-path filter: source EMF cos(2 pi (f_lo + df) t) through R_s, capacitor k connected during
    phase k of N. Returns the node voltage's component at f_lo + df (amplitude per unit EMF) in steady state."""
    dt = 1 / (f_lo * steps)
    vc = np.zeros(npath)
    a_step = math.exp(-dt / (rs * cpath))
    t = np.arange(periods * steps) * dt
    src = np.cos(TWO_PI * (f_lo + df) * t)
    node = np.empty_like(t)
    for i in range(t.size):
        ph = (i % steps) * npath // steps
        vc[ph] = src[i] + (vc[ph] - src[i]) * a_step
        node[i] = vc[ph]
    tail = slice((periods // 2) * steps, periods * steps)
    ref = np.exp(-1j * TWO_PI * (f_lo + df) * t[tail])
    return abs(2 * np.mean(node[tail] * ref))


g_centre = npath_sim(0.0)
v.assert_true("time-domain N-path centre gain matches [(N/pi) sin(pi/N)]^2 within 2%",
              abs(g_centre / held**2 - 1) < 0.02, f"{g_centre:.4f} vs {held**2:.4f}")
g_edge = npath_sim(f3)
v.assert_true("time-domain N-path is about 3 dB down at the predicted band edge (within 0.5 dB)",
              abs(20 * lg(g_edge / g_centre) + 3.01) < 0.5, f"{20 * lg(g_edge / g_centre):.2f} dB")

# ---------------------------------------------------------------- Q6: the VCO
f0 = 6e9
w0 = TWO_PI * f0
lt = 0.6e-9
ct = 1 / (w0**2 * lt)
r_l = 12 * w0 * lt  # inductor loss as a parallel resistance
r_c = 30 / (w0 * ct)  # capacitor loss as a parallel resistance
rp = r_l * r_c / (r_l + r_c)
qt = rp / (w0 * lt)
v.check("X21.6a", qt)
v.check("X21.6b", ct * 1e12)
v.check("X21.6c", rp)
i_tail = 3e-3
i1 = fourier(lambda t: (i_tail / 2) * square(t), 1)  # differential current switches +-I_tail/2
amp = i1 * rp
v.check("X21.6d", amp)
p_s = amp**2 / (2 * rp)
v.check("X21.6e", 100 * p_s / (i_tail * 1.0))
v.check("X21.6f", p_s * 1e3)
kt = 1.380649e-23 * 300
dw = TWO_PI * 1e6
l_tank = 2 * kt / p_s * (w0 / (2 * qt * dw)) ** 2
v.check("X21.6g", db(l_tank))
v.check("X21.6k", l_tank)
v.check("X21.6h", db(3 * l_tank))
v.check("X21.6i", -db(3 * l_tank) + 20 * lg(f0 / 1e6) - db(3e-3 / 1e-3))
v.check("X21.6j", db(3 * l_tank / 4))

# ---------------------------------------------------------------- Q7: the PA
p_out = idb(28) / 1e3
r_opt = optimize.brentq(lambda rr: (3.4 - 0.4) ** 2 / (2 * rr) - p_out, 0.1, 100)
v.check("X21.7a", r_opt)
v.check("X21.7b", math.sqrt(50 / r_opt - 1))


def eta_numeric(alpha_deg: float) -> float:
    half = math.radians(alpha_deg) / 2
    c = math.cos(half) if alpha_deg < 360 else -1.0

    def i_d(t):
        return max(0.0, (math.cos(t) - c) / (1 - c))
    idc = integrate.quad(i_d, -math.pi, math.pi, points=[-half, half] if alpha_deg < 360 else None)[0] / TWO_PI
    i1_ = integrate.quad(lambda t: i_d(t) * math.cos(t), -math.pi, math.pi,
                         points=[-half, half] if alpha_deg < 360 else None)[0] / math.pi
    return 0.5 * i1_ / idc


for key, ang in (("X21.7c", 360), ("X21.7d", 240), ("X21.7e", 180), ("X21.7f", 120)):
    v.check(key, 100 * eta_numeric(ang))
v.check("X21.7g", 100 * (3.4 - 0.4) / 2 / 3.4)
iip3_mw = idb(6)
p_max = optimize.brentq(lambda pp: (pp / iip3_mw) ** 2 / 3 - 1e-4, 1e-6, iip3_mw)  # ACLR = (1/3)(P/P_IIP3)^2
v.check("X21.7h", db(p_max))
v.check("X21.7i", db(p_max) + 30)
v.check("X21.7m", 28 - (db(p_max) + 30))
papr = db(math.log(1e4))  # complex-Gaussian envelope: P(|x|^2 > s) = exp(-s/P), 10^-4 point
v.check("X21.7n", db(p_max) + 30 + papr)
# Monte Carlo check of the cubic ACLR law for a flat complex-Gaussian signal (no clipping).
nmc = 2**18
bw_bins = nmc // 16
spec_in = np.zeros(nmc, complex)
spec_in[:bw_bins // 2] = rng.normal(size=bw_bins // 2) + 1j * rng.normal(size=bw_bins // 2)
spec_in[-bw_bins // 2:] = rng.normal(size=bw_bins // 2) + 1j * rng.normal(size=bw_bins // 2)
xs = np.fft.ifft(spec_in)
xs /= math.sqrt(np.mean(abs(xs) ** 2))
a3_mc = -0.003  # small cubic term (0.6% gain compression), relative to a1 = 1, for unit average power
ys = xs + a3_mc * xs * abs(xs) ** 2
ps = abs(np.fft.fft(ys)) ** 2
fbin = np.fft.fftfreq(nmc) * nmc
main = ps[abs(fbin) < bw_bins / 2].sum()
adj = ps[(fbin >= bw_bins / 2) & (fbin < 3 * bw_bins / 2)].sum()
aclr_mc = db(adj / main)
p_iip3_mc = 1 / abs(a3_mc)  # A^2_IIP3 per the envelope model: |a1/a3| in power units of |x|^2
aclr_law = db((1 / p_iip3_mc) ** 2 / 3)
v.assert_true("Monte Carlo ACLR of a cubic PA matches (1/3)(P/P_IIP3)^2 within 0.1 dB",
              abs(aclr_mc - aclr_law) < 0.1, f"{aclr_mc:.2f} vs {aclr_law:.2f} dB")


def doherty(xx: float) -> float:
    """Ideal symmetric Doherty from its class-B device currents (V_DD = R_opt = 1)."""
    i_main = xx
    i_aux = max(0.0, 2 * xx - 1)
    p_dc = (2 / math.pi) * (i_main + i_aux)
    return xx**2 / p_dc


x8 = 10 ** (-8 / 20)
v.check("X21.7j", 100 * doherty(x8))
idc_b = integrate.quad(lambda t: max(0.0, x8 * math.cos(t)), -math.pi, math.pi)[0] / TWO_PI
v.check("X21.7k", 100 * (0.5 * x8 * (x8 / 2)) / idc_b)  # V = x V_DD, I_1 = x I_max/2, I_max = 1
v.check("X21.7l", 100 * doherty(10 ** (-3 / 20)))
v.check("X21.7o", 100 * 0.65 * 0.85)

# ---------------------------------------------------------------- Q8: architectures
f_rf, f_if = 5.8e9, 0.4e9
f_lo = f_rf - f_if
v.check("X21.8a", f_lo / 1e9)
v.check("X21.8b", (f_lo - f_if) / 1e9)
half_if = sorted(fr for fr in (f_lo + f_if / 2, f_lo - f_if / 2) if math.isclose(abs(2 * fr - 2 * f_lo), f_if))
v.assert_true("two half-IF spurs, one each side of the LO", len(half_if) == 2 and half_if[0] < f_lo < half_if[1])
v.check("X21.8c", half_if[1] / 1e9)  # between the LO and the wanted signal
v.check("X21.8k", half_if[0] / 1e9)  # between the image and the LO
# Band edges with f1*f2 = f0^2 and f2 - f1 = B.
bw = 0.2e9
f1 = (-bw + math.sqrt(bw**2 + 4 * f_rf**2)) / 2
f2 = f1 + bw
bb, aa = signal.butter(4, [TWO_PI * f1, TWO_PI * f2], btype="bandpass", analog=True)
_, h = signal.freqs(bb, aa, worN=[TWO_PI * 5.0e9, TWO_PI * half_if[1], TWO_PI * f_rf, TWO_PI * half_if[0]])
v.check("X21.8d", -20 * lg(abs(h[0])))
v.check("X21.8e", -20 * lg(abs(h[1])))
v.check("X21.8l", -20 * lg(abs(h[3])))
v.assert_true("preselector passes the wanted signal", abs(abs(h[2]) - 1) < 1e-6)
irr_need = 30 + 12
v.check("X21.8f", irr_need)
theta = optimize.brentq(lambda t: db(abs(1 + np.exp(1j * t)) ** 2 / abs(1 - np.exp(1j * t)) ** 2) - irr_need,
                        1e-4, 0.5)
v.check("X21.8g", math.degrees(theta))
n_adc = -153 + 2  # dBm/Hz
f_adc = idb(n_adc) / idb(-174)
v.check("X21.8h", db(f_adc))
g_adc = optimize.brentq(lambda g: idb(2) + (f_adc - 1) / g - idb(3), 1, 1e5)
v.check("X21.8i", db(g_adc))
v.check("X21.8m", g_adc)
sig_fs = optimize.brentq(lambda s_: -20 * lg(TWO_PI * 6e9 * s_ * 1e-15) - 55, 1, 1000, xtol=1e-12)
v.check("X21.8j", sig_fs)

# ---------------------------------------------------------------- Q9: front end
fs_res, fp_res = 3.55e9, 3.65e9


def bvd_fp(ratio: float) -> float:
    """Parallel resonance of a BVD resonator with Cm/C0 = ratio and series resonance at fs_res."""
    c_0 = 1e-12
    c_m = ratio * c_0
    l_m = 1 / ((TWO_PI * fs_res) ** 2 * c_m)

    def imag_y(f):
        w = TWO_PI * f
        return (1j * w * c_0 + 1 / (1j * w * l_m + 1 / (1j * w * c_m))).imag
    return optimize.brentq(imag_y, fs_res * 1.0001, fs_res * 1.5)


ratio = optimize.brentq(lambda q: bvd_fp(q) - fp_res, 0.01, 0.2)
v.check("X21.9c", ratio)
fp_found = bvd_fp(ratio)
xk = (math.pi / 2) * fs_res / fp_found
v.check("X21.9a", 100 * xk / math.tan(xk))
v.check("X21.9b", 100 * (math.pi**2 / 4) * (fp_found - fs_res) / fp_found)
p_pa = db(idb(26) * idb(2.5))
v.check("X21.9d", p_pa)
v.check("X21.9m", db(idb(p_pa) / idb(50)))
floor_ant = db(kt0 * 1e3) + 4  # receiver noise referred to the antenna, dBm/Hz (kT at 290 K)
iso = optimize.brentq(lambda ii: -138 - ii - (floor_ant - 6), 0, 100)
v.check("X21.9n", iso, tol=0.05)  # kT at 290 K is -173.98 dBm/Hz; the question uses -174
ron, coff = 2.4, 100e-15
v.check("X21.9e", ron * coff * 1e15)
v.check("X21.9f", 1 / (TWO_PI * ron * coff) / 1e9)
v.check("X21.9g", -20 * lg(abs(s21_series(ron))))
v.check("X21.9h", -20 * lg(abs(s21_series(1 / (1j * TWO_PI * 3.5e9 * coff)))))
v_pk = optimize.brentq(lambda vv: vv**2 / (2 * 50) - idb(33) / 1e3, 1, 100)
v.check("X21.9i", v_pk)
gmag = (4 - 1) / (4 + 1)
v.check("X21.9j", v_pk * (1 + gmag))
v.check("X21.9k", math.ceil(v_pk * (1 + gmag) / 3.0))
v.check("X21.9l", -db(1 - gmag**2))

# ---------------------------------------------------------------- Q10: the array
nx = ny = 8
pe_mw, ge = idb(8), idb(5)
k = np.arange(nx)


def af2(theta_deg: float, f: float, steer_deg: float = 0.0, f_set: float = 39e9) -> float:
    """|AF|^2 of one 8-element row, lambda/2 at f_set, phase shifters set at f_set (row is 1-D)."""
    d_lam = 0.5 * f / f_set
    beta = -TWO_PI * 0.5 * k * math.sin(math.radians(steer_deg))
    psi = TWO_PI * d_lam * k * math.sin(math.radians(theta_deg)) + beta
    return abs(np.sum(np.exp(1j * psi))) ** 2


g_arr = af2(0, 39e9) * af2(0, 39e9) / (nx * ny)  # the 2-D array factor gain for uniform power splitting
eirp0 = db(nx * ny * pe_mw * g_arr * ge)
v.check("X21.10a", eirp0)
v.check("X21.10b", eirp0 + db(math.cos(math.radians(50))))
peak = optimize.minimize_scalar(lambda t: -af2(t, 37e9, 50), bounds=(45, 65), method="bounded",
                                options={"xatol": 1e-9})
v.check("X21.10c", peak.x)
freqs = np.linspace(25e9, 55e9, 30001)
gain_50 = np.array([af2(50, f, 50) for f in freqs]) / nx**2
band = freqs[gain_50 >= 0.5]
v.check("X21.10d", 0.886 * 39 / (8 * 0.5 * math.sin(math.radians(50))))
v.check("X21.10j", (band.max() - band.min()) / 1e9)
def quant(bits: int):
    xq = math.pi / 2**bits
    mean_c = integrate.quad(lambda e: math.cos(e), -xq, xq)[0] / (2 * xq)  # E[e^{j eps}] for uniform errors
    rms = math.degrees(math.sqrt(integrate.quad(lambda e: e**2, -xq, xq)[0] / (2 * xq)))
    return mean_c**2, rms


s_loss, rms2 = quant(2)
v.check("X21.10e", -db(s_loss))
v.check("X21.10f", db((1 - s_loss) / (nx * ny)))
v.check("X21.10g", rms2)
v.check("X21.10k", db((1 - quant(4)[0]) / (nx * ny)))
v.check("X21.10l", db((1 - quant(5)[0]) / (nx * ny)))
bits_needed = next(b for b in range(1, 12) if db((1 - quant(b)[0]) / (nx * ny)) < -40)
v.check("X21.10m", bits_needed)
# Monte Carlo: random phase errors (uniform over one 2-bit step) on all 64 elements, sampled where the ideal
# pattern has nulls (u = m/4 for an 8-wide row at lambda/2), where only the scattered floor (1 - S)/N remains.
u_null = np.array([0.25, 0.5, 0.75])
idx = np.arange(nx * ny)
pos_x = idx % nx
acc = np.zeros(u_null.size)
trials = 2000
for _ in range(trials):
    w_el = np.exp(1j * rng.uniform(-math.pi / 4, math.pi / 4, nx * ny))
    acc += abs((w_el[None, :] * np.exp(1j * math.pi * pos_x[None, :] * u_null[:, None])).sum(axis=1) / (nx * ny)) ** 2
floor_mc = db(acc.mean() / trials)
v.assert_true("Monte Carlo floor at the ideal pattern's nulls within 0.5 dB of (1 - S)/N (2 bits)",
              abs(floor_mc - db((1 - s_loss) / (nx * ny))) < 0.5, f"{floor_mc:.2f} dB")
v.check("X21.10h", 0.5 * 42 / 39)
lim = optimize.brentq(lambda dl: math.sin(math.radians(50)) - 1 / dl + 1, 0.3, 1.0)
v.check("X21.10i", lim)

# ---------------------------------------------------------------- Q11: the wearable link
eirp = 0 - 1 - 6
v.check("X21.11a", eirp)
sens = db(kt0 * 1e3) + db(1e6) + 11 + 7  # thermal floor from kT at 290 K
v.check("X21.11b", sens, tol=0.03)  # kT at 290 K is -173.98 dBm/Hz; the question uses -174
sens = -174 + 60 + 11 + 7
marg = 6 * stats.norm.ppf(0.9)
v.check("X21.11c", marg)
mapl = eirp + (-1) - 1.5 - sens - marg - 10
v.check("X21.11d", mapl)
lam = C0 / 2.44e9
pl1 = 20 * lg(4 * math.pi * 1.0 / lam)
v.check("X21.11e", pl1)
d_max = optimize.brentq(lambda d: pl1 + 30 * lg(d) - mapl, 1, 1e4)
v.check("X21.11f", d_max)
sens2 = -174 + db(125e3) + 5 + 7
v.check("X21.11g", sens2)
d2 = optimize.brentq(lambda d: pl1 + 30 * lg(d) - (mapl + sens - sens2), 1, 1e5)
v.check("X21.11h", d2)

# ---------------------------------------------------------------- Q12: modems and positioning


def nr_rate(layers, bits, prb, mu, oh):
    symbols_per_s = 14 * 2**mu * 1000
    return layers * bits * (948 / 1024) * prb * 12 * symbols_per_s * (1 - oh) / 1e6


r80 = nr_rate(4, 8, 217, 1, 0.14)
r60 = nr_rate(4, 8, 162, 1, 0.14)
v.check("X21.12a", r80)
v.check("X21.12b", r60)
v.check("X21.12c", r80 + r60)
bits_per_symbol = 2 * 1960 * 10 * 5 / 6
v.check("X21.12d", bits_per_symbol / (12.8e-6 + 1.6e-6) / 1e6)
tau_true = 10.0 / C0  # any distance: the error does not depend on it to first order
e_a, e_b = 5e-6, -15e-6
t_reply = 300e-6
t_round_meas = (2 * tau_true + t_reply) * (1 + e_a)
t_reply_meas = t_reply * (1 + e_b)
err = ((t_round_meas - t_reply_meas) / 2 - tau_true) * C0
v.check("X21.12e", err)
t_max = optimize.brentq(lambda tr: (e_a - e_b) * tr / 2 * C0 - 0.10, 1e-6, 1e-3)
v.check("X21.12f", t_max * 1e6)
GM, RE, H = 3.986e14, 6371e3, 1200e3
rad = RE + H
v_orb = math.sqrt(GM / rad)
v.check("X21.12g", v_orb)
# Range rate over a pass for a user in the orbital plane: the maximum is at the horizon.
user = np.array([0.0, RE])
ang = np.linspace(-math.acos(RE / rad), math.acos(RE / rad), 200_001)
pos = np.stack([rad * np.sin(ang), rad * np.cos(ang)], axis=1)
vel = v_orb * np.stack([np.cos(ang), -np.sin(ang)], axis=1)
rel = pos - user
range_rate = np.sum(rel * vel, axis=1) / np.linalg.norm(rel, axis=1)
v_los = np.abs(range_rate).max()
v.check("X21.12h", v_los)
v.check("X21.12i", v_los * 2e9 / C0 / 1e3)
v.check("X21.12j", v_los * 2e9 / C0 / 15e3)

# ---------------------------------------------------------------- Q13: derivations
a1, a3 = 1.0, -1.0
a_1db = optimize.brentq(lambda aa: 20 * lg(abs(a1 + 0.75 * a3 * aa**2) / a1) + 1, 1e-3, 1.0)
a_ip3 = optimize.brentq(lambda aa: a1 * aa - 0.75 * abs(a3) * aa**3, 0.5, 5.0)
gap = 20 * lg(a_ip3 / a_1db)
v.check("X21.13a", gap)
v.check("X21.13b", -10 - gap)
f_chain = stages[0][1] + (stages[1][1] - 1) / stages[0][0] + (stages[2][1] - 1) / (stages[0][0] * stages[1][0])
v.check("X21.13c", T0 * (f_chain - 1))
e_w, g_e, eta_pa, p_oh = idb(65) / 1e3, idb(5), 0.2, 0.05


def p_dc(nn: float) -> float:
    return nn * (e_w / (nn**2 * g_e) / eta_pa + p_oh)


opt = optimize.minimize_scalar(p_dc, bounds=(10, 5000), method="bounded", options={"xatol": 1e-8})
v.check("X21.13d", opt.x)
v.check("X21.13e", opt.fun)
v.check("X21.13f", p_dc(2 * opt.x) / opt.fun)
v.assert_true("the penalty is the same at half the count", abs(p_dc(opt.x / 2) / opt.fun - 1.25) < 1e-6)


def ebn0_min(eta: float) -> float:
    return optimize.brentq(lambda e: math.log2(1 + eta * e) - eta, 1e-6, 1e6)


v.check("X21.13g", db(ebn0_min(1e-7)))
v.check("X21.13h", db(ebn0_min(2)))
v.check("X21.13i", db(ebn0_min(6)))

# ---------------------------------------------------------------- Q14: diligence
ron_max = optimize.brentq(lambda rr: -20 * lg(abs(s21_series(rr))) - 0.2, 0.01, 50)
v.check("X21.14a", ron_max)
coff_fF = optimize.brentq(lambda cc: -20 * lg(abs(s21_series(1 / (1j * TWO_PI * 3.5e9 * cc * 1e-15)))) - 40,
                          0.1, 100, xtol=1e-12)
coff_max = coff_fF * 1e-15
v.check("X21.14b", coff_fF)
v.check("X21.14c", ron_max * coff_max * 1e15)
v.check("X21.14d", 100e-15 / (ron_max * coff_max))
v.check("X21.14e", 26 + 9.64)
v.check("X21.14l", idb(26 + 9.64) / 1e3)
p_avg = idb(26)
v.check("X21.14f", p_avg / 0.45)
v.check("X21.14g", p_avg / 0.45 / 3.8)
# The 29.2% and 54.9% given in the question: average efficiency E[x^2]/E[x^2/eta(x)] over a complex-Gaussian
# envelope clipped at its 10^-4 point (PAPR 9.64 dB), x = min(r/r_sat, 1) with r Rayleigh.
r_sat2 = math.log(1e4)  # |x|^2 at the 10^-4 point for unit average power


def avg_eff(eta_fn) -> float:
    def pdf(s_):  # |x|^2 is exponential with unit mean
        return math.exp(-s_)
    num = integrate.quad(lambda s_: min(s_ / r_sat2, 1.0) * pdf(s_), 0, 60, points=[r_sat2], limit=200)[0]
    den = integrate.quad(lambda s_: min(s_ / r_sat2, 1.0) / eta_fn(math.sqrt(min(s_ / r_sat2, 1.0))) * pdf(s_),
                         1e-12, 60, points=[r_sat2], limit=200)[0]
    return num / den


v.assert_true("ideal class-B OFDM average efficiency is 29.2%", round(100 * avg_eff(lambda xx: math.pi / 4 * xx), 1) == 29.2)
v.assert_true("ideal Doherty OFDM average efficiency is 54.9%", round(100 * avg_eff(doherty), 1) == 54.9)
v.check("X21.14h", p_avg / 0.292)
v.check("X21.14i", p_avg / 0.549)


def system_nf(switch_db: float) -> float:
    chain = [(1 / idb(switch_db), idb(switch_db)), (1 / idb(1.5), idb(1.5)), (idb(18), idb(1.0)),
             (1.0, idb(6))]
    t_sum, g_run = 0.0, 1.0
    for g_i, f_i in chain:
        t_sum += T0 * (f_i - 1) / g_run
        g_run *= g_i
    return db(1 + t_sum / T0)


v.check("X21.14j", system_nf(0.2))
v.check("X21.14k", system_nf(0.5))
v.check("X21.14m", system_nf(0.2) - 1.0)

v.finish()
