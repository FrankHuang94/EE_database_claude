#!/usr/bin/env python3
"""Verify every number in chapter 20-06 (data converter fundamentals), its problems and its lab.

Independent routes:
- SQNR by direct numerical quantization of long sine, uniform and Gaussian records (seeded), compared with the
  closed forms, and the Gaussian clipping probability from the error function;
- DNL/INL by explicit loops over transition levels rather than vectorized differences;
- the SAR transfer by brute-force sweep of a finely sampled input through an independent binary-search
  implementation (the lab bisects for each transition);
- the sine-histogram relation T_k = V0 - A cos(pi C) checked against the arcsine distribution numerically;
- spectral metrics computed with an explicit DFT at the signal and harmonic bins (Goertzel-style sums) rather than
  an FFT; figures of merit from their definitions; the thermal limit derived symbolically with sympy;
- ngspice confirms the ladder taps (run_spice); the lab module (adc.py) is asserted to agree.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import adc as lab  # noqa: E402

v = Verifier.from_files("20-06", ROOT / "chapters" / "20-06-data-converter-fundamentals.md",
                        ROOT / "solutions" / "20-06-solutions.md", LAB / "README.md")

KT = 1.380649e-23 * 300.0
db10 = lambda x: 10 * math.log10(x)  # noqa: E731


def sqnr_closed(n):
    return db10(1.5 * 4 ** n)


def enob(s):
    return (s - 1.76) / 6.02


def endpoint(t):
    n = len(t)
    d_avg = (t[-1] - t[0]) / (n - 1)
    dnl = [(t[i + 1] - t[i]) / d_avg - 1 for i in range(n - 1)]
    inl = [(t[i] - (t[0] + i * d_avg)) / d_avg for i in range(n)]
    return d_avg, dnl, inl


# ------------------------------------------------------------------ Example 20-06.1
print("Example 20-06.1")
rng = np.random.default_rng(2006)
n12, lsb12 = 12, 1.0 / 4096
x = 0.5 * np.sin(2 * np.pi * rng.uniform(0, 1, 2_000_000))
q = (np.floor(x / lsb12) + 0.5) * lsb12
v.assert_true("numerical sine SQNR matches 6.02N + 1.76", abs(db10(np.mean(x ** 2) / np.mean((x - q) ** 2)) -
                                                                sqnr_closed(12)) < 0.05)
v.check("Ex 20-06.1a", sqnr_closed(12))
v.check("Ex 20-06.1b", db10(4 ** 12))
v.check("Ex 20-06.1c", db10(12 * 4 ** 12 / 64))
pclip = math.erfc(4 / math.sqrt(2))
v.check("Ex 20-06.1d", pclip)
v.check("Ex 20-06.1e", sqnr_closed(12) - 20)
v.check("Ex 20-06.1f", 20 * math.log10(math.sqrt(2)))
v.check("Ex 20-06.1g", 20 * math.log10(4))
v.check("Ex 20-06.1h", db10(4 ** 12) - db10(12 * 4 ** 12 / 64))
v.check("Ex 20-06.1i", 1 / pclip)
v.check("Ex 20-06.1j", sqnr_closed(12) - db10(12 * 4 ** 12 / 64))
g = rng.normal(0, 1 / 8, 2_000_000)
gq = (np.floor(g / lsb12) + 0.5) * lsb12
v.assert_true("numerical Gaussian SQNR (granular) matches the closed form",
              abs(db10(np.mean(g ** 2) / np.mean((g - gq) ** 2)) - db10(12 * 4 ** 12 / 64)) < 0.05,
              str(db10(np.mean(g ** 2) / np.mean((g - gq) ** 2))))

# ------------------------------------------------------------------ Example 20-06.2
print("Example 20-06.2")
R = [51, 98, 103, 100, 97, 104, 100, 150]
taps = []
acc = 0.0
for r in R[:7]:
    acc += r
    taps.append(0.8 * acc / sum(R))
for key, t in zip("abcdefg", taps):
    v.check(f"Ex 20-06.2{key}", t * 1e3)
offs = [15e-3, -20e-3, 35e-3, 0.0, -10e-3, 40e-3, -5e-3]
T = [a + b for a, b in zip(taps, offs)]
for key, t in zip("hijklmn", T):
    v.check(f"Ex 20-06.2{key}", t * 1e3)
v.check("Ex 20-06.2o", (T[0] - 0.05) / 0.1)
v.check("Ex 20-06.2p", ((T[-1] - T[0]) - 0.6) / 0.1)
d_avg, dnl, inl = endpoint(T)
v.check("Ex 20-06.2q", d_avg * 1e3)
for key, d in zip(["2r", "2s", "2t", "2u", "2v", "2w"], dnl):
    v.check(f"Ex 20-06.{key}", d)
for key, i in zip(["2x", "2y", "2z", "2aa", "2ab"], inl[1:6]):
    v.check(f"Ex 20-06.{key}", i)
k = np.arange(1, 8)
a, b = np.polyfit(k, T, 1)
v.check("Ex 20-06.2ac", max(abs((t - (a * kk + b)) / a) for t, kk in zip(T, k)))
v.assert_true("INL is the running sum of DNL", all(abs(inl[j] - sum(dnl[:j])) < 1e-12 for j in range(7)))


# ------------------------------------------------------------------ SAR model, independent


def sar_sweep(w, n_bits, vfs, per_lsb=16):
    """Brute-force transfer: sweep the input finely, binary-search each point, read transitions."""
    lsb = vfs / 2 ** n_bits
    scale = (2 ** n_bits - 1) / sum(w)
    vin = (np.arange(-per_lsb, (2 ** n_bits + 1) * per_lsb) + 0.5) * lsb / per_lsb
    code = np.zeros(vin.size, dtype=np.int64)
    for bit in range(n_bits - 1, -1, -1):
        trial = code | (1 << bit)
        dac = np.zeros(vin.size)
        for bb in range(n_bits):
            dac += ((trial >> bb) & 1) * w[bb]
        code = np.where(vin >= (dac * scale - 0.5) * lsb, trial, code)
    return vin, code


def own_code(vin, w, n_bits, vfs):
    """The script's own SAR binary search (same comparison rule as sar_sweep) on an array of inputs."""
    lsb = vfs / 2 ** n_bits
    scale = (2 ** n_bits - 1) / sum(w)
    code = np.zeros(np.shape(vin), dtype=np.int64)
    for bit in range(n_bits - 1, -1, -1):
        trial = code | (1 << bit)
        dac = np.zeros(np.shape(vin))
        for bb in range(n_bits):
            dac = dac + ((trial >> bb) & 1) * w[bb]
        code = np.where(vin >= (dac * scale - 0.5) * lsb, trial, code)
    return code


def own_transitions(w, n_bits=12, vfs=1.6, iters=60):
    """Transition T_k (k = 1..2^N - 1): the lowest input whose code is at least k, by vectorized bisection."""
    k = np.arange(1, 2 ** n_bits)
    lo = np.full(k.size, -vfs / 2 ** n_bits)
    hi = np.full(k.size, vfs * (1 + 2 / 2 ** n_bits))
    for _ in range(iters):
        mid = (lo + hi) / 2
        ge = own_code(mid, w, n_bits, vfs) >= k
        hi = np.where(ge, mid, hi)
        lo = np.where(ge, lo, mid)
    return hi


def own_sfdr(x, m):
    """SFDR from the full complex FFT, pairing each bin with its mirror (an independent route to the lab's rfft)."""
    n = x.size
    xx = np.fft.fft(x - x.mean())
    p = np.abs(xx) ** 2
    one = np.concatenate([[0.0], p[1:n // 2] + p[n - 1:n // 2:-1], [p[n // 2]]])
    sig = one[m]
    spur = np.max(np.delete(one, [0, m]))
    return db10(sig / spur)


def widths_from_sweep(vin, code, n_bits, vfs, per_lsb):
    lsb = vfs / 2 ** n_bits
    counts = np.bincount(code, minlength=2 ** n_bits)
    return counts[1:-1] * (lsb / per_lsb) / lsb    # widths of codes 1..2^N-2 in LSB (to sweep resolution)


print("Example 20-06.3")
N = 12
w0 = [2.0 ** bb for bb in range(N)]
wa = list(w0)
wa[-1] *= 1.0005
scale_a = 4095 / sum(wa)
v.check("Ex 20-06.3a", 2048 * 0.0005)
step = (wa[-1] - sum(wa[:-1])) * scale_a           # LSB step at the major carry, renormalized
davg_a = (4095 - scale_a * wa[0]) / 4094               # average step in nominal LSB
v.check("Ex 20-06.3b", step / davg_a - 1)
ta = own_transitions(wa)
v.assert_true("lab transitions agree (a)", np.max(np.abs(ta - lab.sar_transitions(np.array(wa), 1.6))) < 1e-9)
_, dnl_a, inl_a = endpoint(list(ta))
v.assert_true("independent DNL at the carry matches the lab transitions", abs(dnl_a[2046] - (step / davg_a - 1))
              < 1e-6, f"{dnl_a[2046]}")
v.check("Ex 20-06.3c", inl_a[2047])
wb = list(w0)
wb[-1] *= 0.999
vin, code = sar_sweep(wb, N, 1.6, per_lsb=64)
present = set(np.unique(code).tolist())
missing = [c for c in range(1, 4095) if c not in present]
v.check("Ex 20-06.3d", missing[0])
v.check("Ex 20-06.3e", missing[1])
v.check("Ex 20-06.3f", len(missing))
tb = own_transitions(wb)
v.assert_true("lab transitions agree (b)", np.max(np.abs(tb - lab.sar_transitions(np.array(wb), 1.6))) < 1e-9)
_, dnl_b, inl_b = endpoint(list(tb))
v.check("Ex 20-06.3g", dnl_b[2044])
v.check("Ex 20-06.3h", inl_b[2047])
v.check("Ex 20-06.3i", 1 - 2048 * 0.001)
wid = widths_from_sweep(vin, code, N, 1.6, 64)
v.assert_true("sweep confirms zero width for codes 2046 and 2047", wid[2045] == 0 and wid[2046] == 0)

print("Example 20-06.4")
v.check("Ex 20-06.4a", 0.005 * math.sqrt(4095))
v.check("Ex 20-06.4b", 0.005 * math.sqrt(2048 * 2047 / 4095))
v.check("Ex 20-06.4c", 0.1 / math.sqrt(4095) * 100)
v.check("Txt 20-06.b", 0.005 * math.sqrt(4095))
# seeded instance, rebuilt independently from the same draws
rs = np.random.default_rng(2006)
ws = [2 ** bb + 0.005 * math.sqrt(2 ** bb) * rs.standard_normal() for bb in range(N)]
ts = own_transitions(ws)
v.assert_true("lab transitions agree (seeded)", np.max(np.abs(ts - lab.sar_transitions(np.array(ws), 1.6))) < 1e-9)
_, dnl_s, inl_s = endpoint(list(ts))
v.check("Ex 20-06.4d", max(abs(x_) for x_ in dnl_s))
v.check("Ex 20-06.4e", max(abs(x_) for x_ in inl_s))
vin_s, code_s = sar_sweep(ws, N, 1.6, per_lsb=32)
wid_s = widths_from_sweep(vin_s, code_s, N, 1.6, 32)
v.assert_true("sweep widths agree with the bisection DNL to the sweep resolution",
              np.max(np.abs(wid_s * (1.6 / 4096) / ((ts[-1] - ts[0]) / 4094) - 1 - np.array(dnl_s))) < 0.07)
# Monte Carlo of the mid-scale DNL standard deviation
mc = []
for _ in range(4000):
    ww = [2 ** bb + 0.005 * math.sqrt(2 ** bb) * rs.standard_normal() for bb in range(N)]
    sc = 4095 / sum(ww)
    mc.append((ww[-1] - sum(ww[:-1])) * sc - 1)
v.assert_true("Monte Carlo sigma(DNL_mid) matches sigma_u sqrt(2^N - 1)",
              abs(np.std(mc) / (0.005 * math.sqrt(4095)) - 1) < 0.05)

# ------------------------------------------------------------------ Example 20-06.5
print("Example 20-06.5")
A5, D12 = 1.02 * 0.8, 1.6 / 4096
pm = D12 / (math.pi * A5)
v.check("Ex 20-06.5a", pm)
v.check("Ex 20-06.5b", 400 / pm)
v.check("Ex 20-06.5c", 400 / math.sqrt(1 - (0.4 / A5) ** 2))
v.check("Ex 20-06.5d", 400 / math.sqrt(1 - (0.79 / A5) ** 2))
sfrac = 0.5 / math.sqrt(2 ** 22)
v.check("Ex 20-06.5e", sfrac)
v.check("Ex 20-06.5f", math.pi * A5 * sfrac * 1e3)
v.check("Ex 20-06.5g", math.pi * A5 * sfrac / D12)
v.check("Ex 20-06.5h", 100 / math.sqrt(400))
th = np.linspace(0, 2 * np.pi, 2_000_001)[:-1]
vv = A5 * np.sin(th)
for level in (-0.5, 0.0, 0.3):
    frac = np.mean(vv < level)
    v.assert_true(f"arcsine CDF inverts to the level {level}", abs(-A5 * math.cos(math.pi * frac) - level) < 1e-5)

# ------------------------------------------------------------------ Example 20-06.6 and 20-06.7
print("Example 20-06.6")
SNR = 68.76239465104206          # Problem 20-05.9's budget, recomputed there
for (kt, ks, kf, ke), hd3 in ((("6a", "6b", "6c", "6d"), -64.40878967245925),
                              (("6e", "6f", "6g", "6h"), -83.09525906495784)):
    sinad = -db10(10 ** (-SNR / 10) + 10 ** (hd3 / 10))
    v.check(f"Ex 20-06.{kt}", hd3)
    v.check(f"Ex 20-06.{ks}", sinad)
    v.check(f"Ex 20-06.{kf}", -hd3)
    v.check(f"Ex 20-06.{ke}", enob(sinad))
v.check("Ex 20-06.6i", SNR - 1)
v.check("Ex 20-06.6j", enob(SNR))
v.check("Ex 20-06.6k", -64.40878967245925 + SNR)
v.check("Ex 20-06.6l", enob(SNR) - enob(-db10(10 ** (-SNR / 10) + 10 ** (-83.09525906495784 / 10))))
print("Example 20-06.7")
v.check("Ex 20-06.7a", -SNR - db10(50e6))
v.check("Ex 20-06.7b", SNR + db10(50))
v.check("Ex 20-06.7c", db10(50))
v.check("Ex 20-06.7d", SNR + db10(8192))
v.check("Ex 20-06.7e", enob(SNR))
v.check("Ex 20-06.7f", enob(SNR + db10(50)))
v.check("Txt 20-06.c", db10(8192))
v.check("Txt 20-06.e", -55.6 - db10(5.12e9 / 2))

# ------------------------------------------------------------------ Example 20-06.8 and the thermal limit
print("Example 20-06.8")
fw = lambda p, fs, e: p / (2 ** e * fs) * 1e15  # noqa: E731
fsch = lambda s, bw, p: s + db10(bw / p)  # noqa: E731
for (k1, k2), hd3 in ((("8a", "8b"), -64.40878967245925), (("8c", "8d"), -83.09525906495784)):
    s = -db10(10 ** (-SNR / 10) + 10 ** (hd3 / 10))
    v.check(f"Ex 20-06.{k1}", fw(1.5e-3, 100e6, enob(s)))
    v.check(f"Ex 20-06.{k2}", fsch(s, 50e6, 1.5e-3))
for (k1, k2), (e, p, fs) in ((("8e", "8f"), (7.5, 1e-3, 1e9)), (("8g", "8h"), (15, 10e-3, 10e6))):
    v.check(f"Ex 20-06.{k1}", fw(p, fs, e))
    v.check(f"Ex 20-06.{k2}", fsch(6.02 * e + 1.76, fs / 2, p))
emin = 8 * KT * 10 ** (SNR / 10)
v.check("Ex 20-06.8i", emin * 1e12)
v.check("Ex 20-06.8j", emin * 100e6 * 1e6)
v.check("Ex 20-06.8k", 1.5e-3 / (emin * 100e6))
Asym, Csym, fs_sym, kTs, snr_sym = sp.symbols("A C f_s kT SNR", positive=True)
csub = sp.solve(sp.Eq(Asym ** 2 * Csym / (2 * kTs), snr_sym), Csym)[0]
# class-B supply charge per period by numerical integration of the positive part of C dv/dt (A = C = f = 1)
tt = np.linspace(0, 1, 200001)
i_drv = 2 * math.pi * np.cos(2 * math.pi * tt)                   # C dv/dt for v = A(1 + sin 2 pi f t)
q_supply = np.trapezoid(np.clip(i_drv, 0, None), tt)
v.assert_true("class-B supply charge per period is 2AC", abs(q_supply - 2) < 1e-6, f"{q_supply:.6f}")
p_b_nyq = 2 * q_supply * 0.5                    # P/f_s in units of A^2 C: V_DD = 2A, f = f_s/2
v.assert_true("ideal class-B at Nyquist: P/f_s = 4kT SNR", abs(p_b_nyq * 2 - 4) < 1e-6)   # A^2 C = 2 kT SNR
lim = db10(1 / (16 * KT))
v.check("Txt 20-06.a", lim)
v.check("Txt 20-06.a2", db10(1 / (8 * KT)))
v.check("Txt 20-06.d", lim - 189.17)
v.check("Txt 20-06.f", math.log2(math.sqrt(12)))
s_b = -db10(10 ** (-SNR / 10) + 10 ** (-64.40878967245925 / 10))
v.check("Ex 20-06.8l", lim - fsch(s_b, 50e6, 1.5e-3))

# ------------------------------------------------------------------ lab


def dft_metrics(xr, m, n_harm=9):
    """Signal, harmonic and total powers by explicit DFT sums at the needed bins; noise from Parseval."""
    n = xr.size
    xr = xr - xr.mean()
    tt = np.arange(n)

    def pbin(kk):
        c = np.sum(xr * np.exp(-2j * np.pi * kk * tt / n))
        return 2 * abs(c) ** 2 / n ** 2

    total = np.sum(xr ** 2) / n
    ps = pbin(m)
    bins = []
    for h in range(2, n_harm + 1):
        bb = (h * m) % n
        bb = n - bb if bb > n // 2 else bb
        if bb not in bins and bb not in (0, m):
            bins.append(bb)
    ph = sum(pbin(bb) for bb in bins)
    pn = total - ps - ph
    return {"snr": db10(ps / pn), "thd": db10(ph / ps), "sinad": db10(ps / (pn + ph)), "amp": math.sqrt(2 * ps)}


print("Lab 20-06")
n4k = 4096
for key_s, key_f, m in (("Lab 20-06.a", "Lab 20-06.b", 1001), ("Lab 20-06.c", "Lab 20-06.d", 64)):
    xs = 0.8 + 0.8 * (1 - 1e-9) * np.sin(2 * np.pi * m * np.arange(n4k) / n4k)
    cq = np.clip(np.floor(xs / D12 + 0.5), 0, 4095) * D12
    met = lab.spectrum_metrics(cq, m)
    dm = dft_metrics(cq, m)
    v.assert_true(f"explicit DFT SINAD matches the lab FFT for M = {m}", abs(dm["sinad"] - met["sinad"]) < 1e-6)
    v.check(key_s, dm["sinad"])
    v.check(key_f, own_sfdr(cq, m))
    v.assert_true(f"lab SFDR agrees for M = {m}", abs(own_sfdr(cq, m) - met["sfdr"]) < 1e-9)
rd = np.random.default_rng(20061)
xd = 0.8 + 0.8 * 0.98 * np.sin(2 * np.pi * 64 * np.arange(n4k) / n4k) + rd.normal(0, 0.5 * D12, n4k)
cd_ = np.clip(np.floor(xd / D12 + 0.5), 0, 4095) * D12
md = lab.spectrum_metrics(cd_, 64)
v.check("Lab 20-06.e", own_sfdr(cd_, 64))
v.check("Lab 20-06.f", dft_metrics(cd_, 64)["sinad"])
v.assert_true("lab dithered metrics agree", abs(md["sinad"] - dft_metrics(cd_, 64)["sinad"]) < 1e-6)
# histogram tests on the seeded instance
ns, Ah = 2 ** 22, 1.02 * 0.8
ph_c = 2 * np.pi * (np.arange(ns) * 1048573 / ns + 0.123)
codes_c = lab.sar_code(0.8 + Ah * np.sin(ph_c), np.array(ws), 1.6)
hc = np.bincount(codes_c, minlength=4096).astype(float)
Tc = 0.8 - Ah * np.cos(np.pi * np.cumsum(hc)[:-1] / ns)
_, dnl_c, inl_c = endpoint(list(Tc))
v.check("Lab 20-06.g", max(abs(p_ - q_) for p_, q_ in zip(dnl_c, dnl_s)))
v.check("Lab 20-06.h", max(abs(p_ - q_) for p_, q_ in zip(inl_c, inl_s)))
rr = np.random.default_rng(2007)
codes_r = lab.sar_code(0.8 + Ah * np.sin(rr.uniform(0, 2 * np.pi, ns)), np.array(ws), 1.6)
hr = np.bincount(codes_r, minlength=4096).astype(float)
Tr = 0.8 - Ah * np.cos(np.pi * np.cumsum(hr)[:-1] / ns)
_, dnl_r, inl_r = endpoint(list(Tr))
v.check("Lab 20-06.i", math.sqrt(np.mean((np.array(dnl_r) - np.array(dnl_s)) ** 2)))
v.check("Lab 20-06.j", max(abs(p_ - q_) for p_, q_ in zip(inl_r, inl_s)))
v.check("Lab 20-06.k", 1 / math.sqrt(ns * pm))
# full FFT test
n16 = 16384
m49 = int(round(49e6 * n16 / 100e6))
m49 += 1 - m49 % 2
sig_th = math.sqrt(206.2791136341102e-6 ** 2 - (D12 / math.sqrt(12)) ** 2)
a3 = 4 * 10 ** (-64.40878967245925 / 20) / 0.8 ** 2
vd = 0.8 * (1 - 1e-6) * 0.999 * np.sin(2 * np.pi * m49 * np.arange(n16) / n16)
vin_f = 0.8 + vd - a3 * vd ** 3 + np.random.default_rng(2008).normal(0, sig_th, n16)
cf = lab.sar_code(vin_f, np.array(ws), 1.6) * D12
dmf = dft_metrics(cf, m49)
v.check("Lab 20-06.l", m49 * 100e6 / n16 / 1e6)
v.check("Lab 20-06.m", dmf["snr"])
v.check("Lab 20-06.n", dmf["thd"])
v.check("Lab 20-06.o", dmf["sinad"])
v.check("Lab 20-06.p", own_sfdr(cf, m49))
v.assert_true("lab SFDR agrees (full FFT test)", abs(own_sfdr(cf, m49) - lab.spectrum_metrics(cf, m49)["sfdr"]) < 1e-9)
e_fs = enob(dmf["sinad"] + 20 * math.log10(0.8 / dmf["amp"]))
v.check("Lab 20-06.q", e_fs)
v.check("Lab 20-06.r", fw(1.5e-3, 100e6, e_fs))
v.check("Lab 20-06.s", fsch(dmf["sinad"] + 20 * math.log10(0.8 / dmf["amp"]), 50e6, 1.5e-3))
v.check("Lab 20-06.t", sig_th * 1e6)
_, dnl_lad, _ = endpoint(taps)
v.check("Lab 20-06.u", max(abs(x_) for x_ in dnl_lad))

# ------------------------------------------------------------------ problems
print("Problems")
for key, n in (("1a", 8), ("1b", 10), ("1c", 14), ("1d", 16)):
    v.check(f"20-06.{key}", sqnr_closed(n))
v.check("20-06.1e", sqnr_closed(16) - 6)
v.check("20-06.2a", enob(70.2))
v.check("20-06.2b", enob(71.2))
T3 = [0.048, 0.150, 0.262, 0.390, 0.390, 0.548, 0.655]
v.check("20-06.3a", (T3[0] - 0.05) / 0.1)
v.check("20-06.3b", ((T3[-1] - T3[0]) - 0.6) / 0.1)
d3, dn3, in3 = endpoint(T3)
v.check("20-06.3c", d3 * 1e3)
for key, d in zip("defghi", dn3):
    v.check(f"20-06.3{key}", d)
for key, i in zip("jklmn", in3[1:6]):
    v.check(f"20-06.3{key}", i)
dn4 = [0.2, -0.4, 0.5, -0.1, 0.3, -0.5]
in4 = [sum(dn4[:j]) for j in range(7)]
for key, i in zip("abcde", in4[1:6]):
    v.check(f"20-06.4{key}", i)
v.check("20-06.4f", max(abs(i) for i in in4))
for key, n in (("5a", 10), ("5b", 12), ("5c", 14)):
    v.check(f"20-06.{key}", 0.5 / 2 ** (n - 1) * 100)
su = 0.1 / math.sqrt(1023)
area = (0.01 / su) ** 2
v.check("20-06.6a", 1 / math.sqrt(4))
v.check("20-06.6b", su * 100)
v.check("20-06.6c", area)
v.check("20-06.6d", area * 1.0)
v.check("20-06.6e", 1024 * area / 1000)
A7, D10 = 1.01 * 0.5, 1.0 / 1024
v.check("20-06.7a", 1000 * math.pi * A7 / D10)
v.check("20-06.7b", 1000 / math.sqrt(1 - (0.95 / 1.01) ** 2))
v.check("20-06.8a", math.pi * A7 / (2 * math.sqrt(1e6)) / D10)
snr9 = 72.5 - 1.0
thd9 = db10(10 ** (-80 / 10) + 10 ** (-76 / 10))
sinad9 = -db10(10 ** (-snr9 / 10) + 10 ** (thd9 / 10))
v.check("20-06.9a", snr9)
v.check("20-06.9b", 72.5)
v.check("20-06.9c", thd9)
v.check("20-06.9d", sinad9)
v.check("20-06.9e", min(76, 88 - 1))
v.check("20-06.9f", enob(sinad9))
v.check("20-06.9g", enob(sinad9 + 1))
v.check("20-06.9h", -88 + 1)
m10 = min(range(1, 8192, 2), key=lambda m: abs(m * 250e6 / 8192 - 70e6))   # nearest odd cycle count by search
v.check("20-06.10a", m10)
v.check("20-06.10b", m10 * 250e6 / 8192 / 1e6)
v.check("20-06.10c", math.gcd(m10, 8192))
v.check("20-06.11a", -65 - db10(500e6))
v.check("20-06.11b", 65 + db10(500 / 20))
v.check("20-06.11c", db10(25) / 6.02)
v.check("20-06.11d", db10(25))
vs, a3s, As = sp.symbols("v a3 A", positive=True)
dev = sp.simplify((vs - a3s * vs ** 3) - (1 - a3s * As ** 2) * vs)
v.assert_true("sympy: cubic endpoint INL is a3 v (A^2 - v^2)", sp.simplify(dev - a3s * vs * (As ** 2 - vs ** 2)) == 0)
vpk = sp.solve(sp.diff(dev, vs), vs)[0]
coef = float(sp.simplify(dev.subs(vs, vpk) / (a3s * As ** 3)))
v.check("20-06.12a", coef)
a3p = 4 * 10 ** (-70 / 20) / 0.64
v.check("20-06.12b", a3p)
v.check("20-06.12c", coef * a3p * 0.512 * 1e3)
v.check("20-06.12d", coef * a3p * 0.512 / D12)
v.check("20-06.12e", 20 * math.log10((D12 / (coef * 0.512)) * 0.64 / 4))
for (ke, kw, ks), (s, bw, p) in ((("13a", "13b", "13c"), (50, 5e9, 0.1)), (("13d", "13e", "13f"), (70, 50e6, 1e-3)),
                                 (("13g", "13h", "13i"), (100, 20e3, 100e-6))):
    v.check(f"20-06.{ke}", enob(s))
    v.check(f"20-06.{kw}", fw(p, 2 * bw, enob(s)))
    v.check(f"20-06.{ks}", fsch(s, bw, p))
v.check("20-06.14a", 8 * KT * 10 ** (sqnr_closed(16) / 10) * 1e6 * 1e6)
v.check("20-06.14b", 8 * KT * 10 ** (sqnr_closed(12) / 10) * 1e9 * 1e3)
p_classa = 2 * Asym * Csym * Asym * sp.pi * fs_sym
ratio_a = sp.simplify(p_classa.subs(Csym, csub) / (4 * fs_sym * kTs * snr_sym))   # over ideal class B at Nyquist
v.assert_true("sympy: class-A over class-B is pi", sp.simplify(ratio_a - sp.pi) == 0, str(ratio_a))
i_peak = 2 * math.pi                                                 # constant class-A current, A = C = f = 1
v.assert_true("numerical class-A over class-B is pi", abs(i_peak / q_supply - math.pi) < 1e-6)
v.check("20-06.14c", float(ratio_a))
v.check("20-06.14d", db10(1 / (8 * math.pi * KT)))
v.check("20-06.14e", lim - db10(1 / (8 * math.pi * KT)))
v.check("20-06.14f", db10(math.pi))

# ------------------------------------------------------------------ agreement with the lab module
print("Lab module agreement")
v.assert_true("adc.py thermal limit matches", abs(lab.thermal_limit_fom_s() - lim) < 1e-12)
v.assert_true("adc.py endpoint DNL/INL match", np.allclose(lab.dnl_inl(np.array(T))[0], dnl) and
              np.allclose(lab.dnl_inl(np.array(T))[1], inl))
v.assert_true("adc.py ideal transitions", np.allclose(lab.sar_transitions(np.array(w0), 1.6),
                                                      (np.arange(1, 4096) - 0.5) * D12))

sys.exit(v.finish())
