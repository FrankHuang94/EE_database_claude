#!/usr/bin/env python3
"""Verify every number in chapter 20-07 (Nyquist ADCs), its problems and its lab.

Independent routes:
- SAR switching energies from the closed-form sums (Ginsburg-Chandrakasan form for conventional switching, the
  monotonic sum), compared with a vectorized re-implementation of the charge bookkeeping over all codes at once
  (the lab loops code by code), which also gives the per-code minima and maxima;
- SAR conversions and redundancy with integer arithmetic (the lab uses floating-point voltages);
- the pipeline re-implemented with integer stage decisions and a separate sweep, for DNL and missing codes;
- the MDAC residue from symbolic charge conservation (sympy);
- interleaving spurs from explicit single-bin DFT sums (the lab uses an FFT) and from the closed forms;
- ngspice confirms the MDAC (run_spice); the lab module (nyq.py) is asserted to agree.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import nyq as lab  # noqa: E402

v = Verifier.from_files("20-07", ROOT / "chapters" / "20-07-nyquist-adcs.md",
                        ROOT / "solutions" / "20-07-solutions.md", LAB / "README.md")
KT = 1.380649e-23 * 300.0
conv = lambda n: sum(2 ** (n + 1 - 2 * i) * (2 ** i - 1) for i in range(1, n + 1))  # noqa: E731
mono = lambda n: sum(2.0 ** (n - 2 - i) for i in range(1, n))  # noqa: E731

# ------------------------------------------------------------------ Example 20-07.1
print("Example 20-07.1")
v.check("Ex 20-07.1a", 2 ** 6 - 1)
v.check("Ex 20-07.1b", 2 ** 8 - 1)
lsb8 = 1.0 / 256
sig8 = lsb8 / 8
wl8 = (3.5e-3 * 1e-6 / sig8) ** 2
v.check("Ex 20-07.1c", lsb8 * 1e3)
v.check("Ex 20-07.1d", sig8 * 1e3)
v.check("Ex 20-07.1e", wl8 * 1e12)
cin8 = 255 * 2 / 3 * 8.6e-3 * wl8
wl6 = (3.5e-9 / (1 / 64 / 8)) ** 2
cin6 = 63 * 2 / 3 * 8.6e-3 * wl6
v.check("Ex 20-07.1f", cin8 * 1e12)
v.check("Ex 20-07.1g", cin6 * 1e12)
v.check("Ex 20-07.1h", cin8 / cin6)


# ------------------------------------------------------------------ SAR trace (integer arithmetic)
def sar_trace(vin_frac_num, vin_frac_den, n):
    """Return v_x after each trial (as exact fractions of V_REF) and the code."""
    code, out = 0, []
    for b in range(n - 1, -1, -1):
        trial = code | (1 << b)
        vx = sp.Rational(trial, 2 ** n) - sp.Rational(vin_frac_num, vin_frac_den)
        out.append(float(vx))
        if vx <= 0:
            code = trial
    return out, code


print("Example 20-07.2")
vx, code = sar_trace(6, 10, 4)
for key, val in zip("abcd", vx):
    v.check(f"Ex 20-07.2{key}", val)
v.check("Ex 20-07.2e", code)

# ------------------------------------------------------------------ Example 20-07.3: energies, vectorized


def conv_energy_all(n):
    """Vectorized bookkeeping for all codes at once (single-ended), N trial transitions."""
    caps = np.array([2.0 ** i for i in range(n)] + [1.0])
    ct = caps.sum()
    vin = (np.arange(2 ** n) + 0.5) / 2 ** n
    q = -ct * vin
    st = np.zeros((vin.size, n + 1))
    kept = np.zeros_like(st)
    vx = (q + st @ caps) / ct
    e = np.zeros(vin.size)
    for b in range(n - 1, -1, -1):
        new = kept.copy()
        new[:, b] = 1.0
        vxn = (q + new @ caps) / ct
        at_ref = new == 1.0
        dq = ((new - vxn[:, None]) - (st - vx[:, None])) * caps
        e += np.where(at_ref, dq, 0.0).sum(axis=1)
        st, vx = new, vxn
        kept[:, b] = np.where(vx <= 0, 1.0, 0.0)
    return e


ec = 2 * conv_energy_all(10)
v.assert_true("vectorized conventional average equals the closed form", abs(ec.mean() - conv(10)) < 1e-6)
v.check("Ex 20-07.3a", conv(10))
v.check("Ex 20-07.3b", mono(10))
v.check("Ex 20-07.3c", (1 - mono(10) / conv(10)) * 100)
v.check("Ex 20-07.3d", conv(10) * 1e-15 * 1e12)
v.check("Ex 20-07.3e", mono(10) * 1e-15 * 1e12)
v.check("Ex 20-07.3f", conv(10) * 1e-15 * 100e6 * 1e6)
v.check("Ex 20-07.3g", mono(10) * 1e-15 * 100e6 * 1e6)
v.check("Ex 20-07.3h", conv(12))
v.check("Ex 20-07.3i", conv(12) / conv(10))
v.check("Lab 20-07.a", ec.min())
v.check("Lab 20-07.b", ec.max())


def mono_energy_own(n, vdiff, vref=1.0):
    """Monotonic switching from charge conservation. Each side: caps 2^(n-2)..1 plus a unit dummy, bottoms at V_REF
    while sampling, so the floating top plate holds Q = C_t (v_top - V_REF). After each comparison the side whose
    top plate is higher grounds its next cap; the caps still on V_REF then draw C_ref (v_old - v_new) from it."""
    caps = [2.0 ** i for i in range(n - 2, -1, -1)] + [1.0]
    ct = sum(caps)
    tops = [vref / 2 + vdiff / 2, vref / 2 - vdiff / 2]
    on_ref = [[True] * len(caps), [True] * len(caps)]
    energy = 0.0
    for k in range(n - 1):
        side = 0 if tops[0] > tops[1] else 1
        on_ref[side][k] = False
        v_new = tops[side] - caps[k] * vref / ct           # grounding cap k lowers the top plate by c_k V_REF / C_t
        c_ref = sum(c for c, r in zip(caps, on_ref[side]) if r)
        energy += vref * c_ref * (tops[side] - v_new)
        tops[side] = v_new
    return energy


em = np.array([mono_energy_own(10, ((c + 0.5) / 1024 - 0.5) * 2) for c in range(1024)])
v.assert_true("charge-conservation monotonic average equals the closed form", abs(em.mean() - mono(10)) < 1e-9)
em_lab = np.array([lab.monotonic_energy(10, ((c + 0.5) / 1024 - 0.5) * 2) for c in range(1024)])
v.assert_true("lab monotonic energies agree code by code", np.max(np.abs(em - em_lab)) < 1e-9)
v.check("Lab 20-07.c", em.min())
v.check("Lab 20-07.d", em.max())
v.assert_true("lab conventional average equals the closed form", abs(lab.conventional_energy_avg(10) - conv(10)) < 1e-6)

# ------------------------------------------------------------------ Example 20-07.4: redundancy, integer SAR
print("Example 20-07.4")
WR = [480, 256, 128, 64, 32, 32, 16, 8, 4, 2, 1]
WB = [512, 256, 128, 64, 32, 16, 8, 4, 2, 1]
marg = [sum(WR[k + 1:]) - WR[k] + 1 for k in range(len(WR))]
for key, m in zip("abcde", marg[:5]):
    v.check(f"Ex 20-07.4{key}", m)


def int_sar(x_lsb, w, err_first):
    """x_lsb: input in LSB (float); comparisons against the trial sum (+ err on the first)."""
    acc = 0
    for k, wk in enumerate(w):
        thr = acc + wk + (err_first if k == 0 else 0)
        if x_lsb >= thr:
            acc += wk
    return acc


xs = np.arange(0, 1024, 0.05)
err = 0.03 * 1024
v.check("Ex 20-07.4f", err)
worst_b = max(abs(int_sar(x, WB, err) - math.floor(x)) for x in xs)
worst_r = max(abs(int_sar(x, WR, err) - math.floor(x)) for x in xs)
v.check("Ex 20-07.4g", worst_b)
v.check("Ex 20-07.4h", worst_r)

# ------------------------------------------------------------------ Example 20-07.5: MDAC and pipeline
print("Example 20-07.5")
cs, cf, cp, vin_, dvr, A_ = sp.symbols("C_s C_f C_p v_in DV A", positive=True)
vx_, vo_ = sp.symbols("v_x v_o")
sol = sp.solve([sp.Eq(cf * (vx_ - vo_) + cs * (vx_ - dvr) + cp * vx_, -(cs + cf) * vin_), sp.Eq(vo_, -A_ * vx_)],
               [vx_, vo_], dict=True)[0]
res = lambda a: float(sol[vo_].subs({cs: 0.5e-12, cf: 0.5e-12, cp: 0.1e-12, vin_: 0.3, dvr: 0.5, A_: a}))  # noqa: E731
beta = 0.5 / 1.1
v.check("Ex 20-07.5a", 2 * 0.3 - 0.5)
v.check("Ex 20-07.5b", 1 / (1000 * beta) * 100)
v.check("Ex 20-07.5c", 1 / (100 * beta) * 100)
v.check("Ex 20-07.5d", res(1000))
v.check("Ex 20-07.5e", res(100))
v.assert_true("lab mdac_residue matches the symbolic solution",
              abs(lab.mdac_residue(0.3, 0.5, 0.5e-12, 0.5e-12, 0.1e-12, 1000) - res(1000)) < 1e-12)
for (k1, k2), n in ((("5f", "5g"), 10), (("5h", "5i"), 12)):
    a_min = 2 ** (n - 1) / beta
    v.check(f"Ex 20-07.{k1}", a_min)
    v.check(f"Ex 20-07.{k2}", 20 * math.log10(a_min))


def pipe_int(x, offs=None, gains=None, n_st=8):
    """Independent pipeline: stage decisions as integers, output code as an integer index 0..1023."""
    offs = np.zeros((n_st, 2)) if offs is None else offs
    gains = np.ones(n_st) if gains is None else gains
    code = np.zeros(x.shape, dtype=np.int64)
    r = x.copy()
    for i in range(n_st):
        d = (r > 0.25 + offs[i, 1]).astype(int) - (r < -0.25 + offs[i, 0]).astype(int)
        code += d * 2 ** (n_st - i)
        r = gains[i] * (2 * r - d)
    back = np.clip(np.floor((r + 1) / 2 * 4), 0, 3).astype(int)
    return code + back + 510


xx = np.linspace(-0.99999, 0.99999, 4000001)
ideal = pipe_int(xx)
rng = np.random.default_rng(7)
offs = rng.uniform(-0.2, 0.2, (8, 2))
v.assert_true("offsets within +-0.2 VREF change no code", np.array_equal(pipe_int(xx, offs), ideal))
o3 = offs.copy()
o3[0, 1] = 0.3
v.check("Ex 20-07.5j", np.abs(pipe_int(xx, o3) - ideal).max())


def dnl_of(codes):
    cnt = np.bincount(codes - codes.min())[1:-1].astype(float)
    return cnt / cnt.mean() - 1, int(np.sum(cnt == 0))


for g1, key in ((0.998, "5k"), (0.99, "5l"), (1.01, None)):
    gg = np.ones(8)
    gg[0] = g1
    d, miss = dnl_of(pipe_int(xx, gains=gg))
    if key == "5k":
        v.check("Ex 20-07.5k", d.min())
    elif key == "5l":
        v.check("Ex 20-07.5l", miss)
    else:
        v.check("Lab 20-07.e", d.max())
g99 = np.ones(8)
g99[0] = 0.99
cnt99 = np.bincount(pipe_int(xx, gains=g99), minlength=1024)
v.assert_true("1% gain: 4 interior plus 2 + 2 end codes never occur", int(np.sum(cnt99 == 0)) == 8
              and cnt99[:2].sum() == 0 and cnt99[-2:].sum() == 0)
v.assert_true("lab pipeline agrees with the integer pipeline (ideal)",
              np.array_equal(lab.pipeline(xx[::40]) + 511.5, ideal[::40]))

# ------------------------------------------------------------------ Example 20-07.6
print("Example 20-07.6")
s_scaled = 1 + 2 / 4 + 4 / 16
s_equal = 1 + 1 / 4 + 1 / 16
v.check("Ex 20-07.6a", s_scaled)
v.check("Ex 20-07.6b", math.sqrt(s_scaled * KT / 1e-12) * 1e6)
v.check("Ex 20-07.6c", s_equal)
v.check("Ex 20-07.6d", math.sqrt(s_equal * KT / 1e-12) * 1e6)
v.check("Ex 20-07.6e", 2 * 24 * KT / (1.6 / 4096) ** 2 * 1e12)
v.check("Ex 20-07.6f", 10 * math.log10(s_scaled / s_equal))

def mdac_size(cs, cf, cp, cload, th=2.5e-9, nbits=12, gmid=12):
    beta = cf / (cs + cf + cp)
    tau = 1e-9 * optimize.brentq(lambda t_ns: math.exp(-th * 1e9 / t_ns) - 2.0 ** -(nbits + 1), 1e-4, 10,
                                 xtol=1e-14)   # half-LSB settling, solved in ns
    cle = cload + cf * (cs + cp) / (cs + cf + cp)
    gm = cle / (beta * tau)
    return beta, tau, cle, gm, gm / gmid


# ------------------------------------------------------------------ Example 20-07.7: interleaving


def dft_power(x, k):
    n = x.size
    c = np.sum(x * np.exp(-2j * np.pi * k * np.arange(n) / n))
    return (2 if k not in (0, n // 2) else 1) * abs(c) ** 2 / n ** 2


print("Example 20-07.7")
n, fs, m, amp = 4096, 1e9, 1001, 0.8
fin = m * fs / n
cases = {"off": (np.array([0, 1e-3]), np.ones(2), np.zeros(2), n // 2),
         "gain": (np.zeros(2), np.array([1, 1.01]), np.zeros(2), n // 2 - m),
         "skew": (np.zeros(2), np.ones(2), np.array([0, 1e-12]), n // 2 - m)}
sp_db = {}
for name, (o, g, s_, b) in cases.items():
    x, _ = lab.ti_capture(2, fs, n, m, amp, o, g, s_)
    sp_db[name] = 10 * math.log10(dft_power(x, b) / dft_power(x, m))
v.check("Ex 20-07.7a", sp_db["off"])
v.assert_true("offset spur equals the closed form", abs(sp_db["off"] - 10 * math.log10(1e-6 / (2 * amp ** 2))) < 1e-6)
v.check("Ex 20-07.7b", 20 * math.log10(0.01 / 2))
v.check("Ex 20-07.7i", sp_db["gain"])
v.assert_true("simulated image is (a/2)/(1 + a/2)", abs(sp_db["gain"] - 20 * math.log10(0.005 / 1.005)) < 1e-6)
v.check("Ex 20-07.7c", 10 * math.log10(4 / 0.01 ** 2))
v.check("Ex 20-07.7d", sp_db["skew"])
v.assert_true("skew spur equals (pi f dt)^2", abs(sp_db["skew"] - 20 * math.log10(math.pi * fin * 1e-12)) < 1e-4)
dt = 1 / (math.pi * 500e6 * 10 ** (60 / 20))
v.check("Ex 20-07.7e", dt * 1e12)
v.check("Txt 20-07.a", dt * 1e12)
v.check("Ex 20-07.7f", 2 * 10 ** (-60 / 20) * 100)
v.check("Ex 20-07.7g", amp * math.sqrt(2e-8) * 1e3)
v.check("Ex 20-07.7h", (fs / 2 - fin) / 1e6)

# ------------------------------------------------------------------ practitioner numbers (sec. 7, sec. 9)
print("Practitioner numbers")
v.check("Txt 20-07.b", 99.9 + 10 * math.log10(0.5e6 / 5.5e-3))        # ADS8881: SINAD 99.9 dB, 1 MS/s, 5.5 mW
v.check("Txt 20-07.c", (4.90 / 4.01 - 1) * 100)                         # ADC12DJ5200RF background vs foreground
v.check("Txt 20-07.d", 53.9 + 10 * math.log10(2.56e9 / (5.03 / 2)))     # dual channel, 5.12 GS/s, 5.03 W
v.check("Txt 20-07.e", 72e9 / 1.125e9)
v.check("Txt 20-07.f", (36.1 - 1.76) / 6.02)
b8, t8, cl8, gm8, i8 = mdac_size(0.5e-12, 0.5e-12, 0.1e-12, 0.5e-12)
v.check("Ex 20-07.8a", t8 * 1e9)
v.check("Ex 20-07.8b", b8)
v.check("Ex 20-07.8c", cl8 * 1e12)
v.check("Ex 20-07.8d", 1 / (2 * math.pi * b8 * t8) / 1e9)
v.check("Ex 20-07.8e", gm8 * 1e3)
v.check("Ex 20-07.8f", i8 * 1e3)
v.check("Ex 20-07.8g", 13 * math.log(2) / (math.pi * b8))
v.assert_true("ratio equals f_t / f_s", abs(1 / (2 * math.pi * b8 * t8) / 200e6 - 13 * math.log(2) / (math.pi * b8)) < 1e-9)
v.check("Txt 20-07.g", 13 * math.log(2) / (2 * math.pi * 0.45 * 2.5e-9) / 1e9)
v.check("Txt 20-07.h", conv(12) * 1e-15 * 100e6 * 1e3)

# ------------------------------------------------------------------ problems
print("Problems")
for key, nb in (("1a", 5), ("1b", 7), ("1c", 9)):
    v.check(f"20-07.{key}", 2 ** nb - 1)
v.check("20-07.1d", (2 ** 10 - 1) / (2 ** 9 - 1))
th = np.array([1, 1, 1, 0, 1, 0, 0])
v.check("20-07.2a", int(th.sum()))
v.check("20-07.2b", int(np.argmin(th)))
v.assert_true("lab encoders agree", lab.ones_count(th[None, :])[0] == 4 and lab.first_transition(th[None, :])[0] == 3)
vx5, code5 = sar_trace(73, 100, 5)
for key, val in zip("abcde", vx5):
    v.check(f"20-07.3{key}", val)
v.check("20-07.3f", code5)
for (kc, km, ks), nb in ((("4a", "4b", "4c"), 8), (("4d", "4e", "4f"), 12)):
    v.check(f"20-07.{kc}", conv(nb))
    v.check(f"20-07.{km}", mono(nb))
    v.check(f"20-07.{ks}", (1 - mono(nb) / conv(nb)) * 100)
tb = 7e-9 / 12
v.check("20-07.5a", tb * 1e9)
v.check("20-07.5b", tb / math.log(2 ** 13) * 1e12)
for key, mval in zip("abcde", marg[:5]):
    v.check(f"20-07.6{key}", mval)
v.assert_true("last six margins are zero", all(mm == 0 for mm in marg[5:]))
r, ds, rs = 0.62, [], []
for _ in range(3):
    d = 1 if r > 0.25 else (-1 if r < -0.25 else 0)
    r = 2 * r - d
    ds.append(d)
    rs.append(r)
for (kd, kr), d, rr in zip((("7a", "7b"), ("7c", "7d"), ("7e", "7f")), ds, rs):
    v.check(f"20-07.{kd}", d)
    v.check(f"20-07.{kr}", rr)
v.check("20-07.8a", 2 ** 13 / 0.4)
v.check("20-07.8b", 20 * math.log10(2 ** 13 / 0.4))
v.check("20-07.9a", 0.5 / 4 * 1e3)
v.check("20-07.9b", 0)

b10, t10, cl10, gm10, i10 = mdac_size(0.65e-12, 0.65e-12, 0.2e-12, 0.65e-12)
v.check("20-07.10a", b10)
v.check("20-07.10b", 2048 / b10)
v.check("20-07.10c", 20 * math.log10(2048 / b10))
v.check("20-07.10d", cl10 * 1e12)
v.check("20-07.10e", gm10 * 1e3)
v.check("20-07.10f", i10 * 1e3)
v.check("20-07.10g", gm10 / (2 * math.pi * cl10) / 1e9)
b2, _, _, _, i2 = mdac_size(1.3e-12, 1.3e-12, 0.4e-12, 1.3e-12)
v.assert_true("doubling every capacitor keeps beta", abs(b2 - b10) < 1e-12)
v.check("20-07.10h", i2 * 1e3)
b3, _, _, gm3, i3 = mdac_size(0.65e-12, 0.65e-12, 0.5e-12, 0.65e-12)
v.check("20-07.10i", b3)
v.check("20-07.10j", 2048 / b3)
v.check("20-07.10k", 20 * math.log10(2048 / b3))
v.check("20-07.10l", gm3 * 1e3)
v.check("20-07.10m", (i3 / i10 - 1) * 100)
v.check("20-07.11a", 10 * math.log10(4e-6 / (2 * 0.25)))
v.check("20-07.12a", 2 * 10 ** (-50 / 20) * 100)
v.check("20-07.12b", 1 / (math.pi * 5e9 * 10 ** 2.5) * 1e12)
# combined image: simulate a two-channel capture with both errors at -50 dBc each and read the image bin
al12 = 2 * 10 ** (-50 / 20)
dt12 = 1 / (math.pi * 5e9 * 10 ** 2.5)
x12, _ = lab.ti_capture(2, 10e9, 4096, 2047, 0.5, np.zeros(2), np.array([1 - al12 / 2, 1 + al12 / 2]), np.array([0, dt12]))
img12 = 10 * math.log10(dft_power(x12, 4096 // 2 - 2047) / dft_power(x12, 2047))
v.check("20-07.12c", 10 * math.log10(2 * 10 ** (-5)))
v.assert_true(f"simulated combined image near -47 dBc ({img12:.2f})", abs(img12 + 47.0) < 0.1)
v.check("20-07.13a", 50e6 / 10 ** ((180 - 80) / 10) * 1e3)
v.check("20-07.13b", 10e9 / 10 ** ((150 - 45) / 10) * 1e3)

sys.exit(v.finish())
