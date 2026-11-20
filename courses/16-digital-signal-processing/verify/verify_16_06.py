#!/usr/bin/env python3
"""Verify chapter 16-06 (FIR filter design): examples, text, problems and lab answers.

Routes (independent of the lab's own response evaluation where possible):
- window and Kaiser designs rebuilt with scipy.signal.firwin (scale=False) and checked equal to the lab's;
- every magnitude response evaluated with scipy.signal.freqz on dense band grids;
- the amplitude response A(w) recovered from freqz by removing the linear phase e^{-jwM/2};
- frequency-sampling designs rebuilt by an inverse FFT of linear-phase DFT samples;
- equiripple designs from scipy.signal.remez, minimum lengths found by searching a window of shorter lengths, and
  optimality confirmed by an independent alternation count;
- the Gibbs constant from scipy.special.sici; the Remez-by-hand problem by solving its linear system.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import minimize_scalar
from scipy.special import sici

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import firdesign as fd  # noqa: E402

CH = ROOT / "chapters" / "16-06-fir-filter-design.md"
v = Verifier.from_files("16-06", CH, ROOT / "solutions" / "16-06-solutions.md", LAB / "README.md")

PI = math.pi
NG = 20000


def amp(h, w):
    """Real amplitude response from freqz: H e^{jwM/2} (real part for symmetric, imaginary for antisymmetric)."""
    h = np.asarray(h, dtype=float)
    M = len(h) - 1
    _, H = signal.freqz(h, 1, worN=np.atleast_1d(w))
    r = H * np.exp(1j * np.atleast_1d(w) * M / 2)
    return r.imag if np.allclose(h, -h[::-1]) else r.real


def bands(h, wp, ws, ng=NG):
    """(max passband deviation from 1, max stopband magnitude) by freqz."""
    _, Hp = signal.freqz(h, 1, worN=np.linspace(0, wp, ng))
    _, Hs = signal.freqz(h, 1, worN=np.linspace(ws, PI, ng))
    return float(np.max(np.abs(np.abs(Hp) - 1))), float(np.max(np.abs(Hs)))


def ripple_pp_db(h, wp, ng=NG):
    _, Hp = signal.freqz(h, 1, worN=np.linspace(0, wp, ng))
    return 20 * math.log10(np.max(np.abs(Hp)) / np.min(np.abs(Hp)))


def firwin_lp(M, wc, window):
    return signal.firwin(M + 1, wc / PI, window=window, scale=False)


def delta_from_pp(Ap):
    g = 10 ** (Ap / 20)
    return (g - 1) / (g + 1)


def meets(h, wp, ws, dp, ds):
    a, b = bands(h, wp, ws)
    return a <= dp and b <= ds


def remez(n, wp, ws, dp, ds):
    return signal.remez(n, [0, wp, ws, PI], [1, 0], weight=[1, dp / ds], fs=2 * PI, grid_density=64)


def count_alternations(h, wp, ws, dp, ds, ng=NG):
    pts = []
    for lo, hi, D, W in ((0, wp, 1.0, 1.0), (ws, PI, 0.0, dp / ds)):
        w = np.linspace(lo, hi, ng)
        E = W * (amp(h, w) - D)
        a = np.abs(E)
        inner = np.where((a[1:-1] >= a[:-2]) & (a[1:-1] >= a[2:]))[0] + 1
        pts += [E[0]] + [E[i] for i in inner] + [E[-1]]
    d = max(abs(e) for e in pts)
    sg = [np.sign(e) for e in pts if abs(e) >= 0.99 * d]
    return 1 + sum(1 for i in range(1, len(sg)) if sg[i] != sg[i - 1]), sum(1 for e in pts if abs(e) >= 0.99 * d)


# ------------------------------------------------------------------------------------------------- §3.1
fs = 48000.0
wp, ws = 2 * PI * 4000 / fs, 2 * PI * 5000 / fs
dp, ds = delta_from_pp(0.1), 10 ** (-60 / 20)
v.assert_true("0.1 dB peak-to-peak tolerance round-trips", abs(20 * math.log10((1 + dp) / (1 - dp)) - 0.1) < 1e-12)
v.check("Txt 16-06.a", dp)
v.check("Txt 16-06.b", ds)
v.check("Txt 16-06.c", ws - wp)
v.assert_true("lab deltas() agrees", np.allclose(fd.deltas(0.1, 60), (dp, ds)))

# ------------------------------------------------------------------------------------------------- §3.3 Gibbs
si_pi = sici(PI)[0]
v.check("Txt 16-06.d", si_pi)
v.check("Txt 16-06.e", 0.5 + si_pi / PI - 1)
v.check("Txt 16-06.f", -20 * math.log10(si_pi / PI - 0.5))

# ------------------------------------------------------------------------------------------------- §3.4 window table


def window_stats(win, M, wc, ng=100001):
    h = firwin_lp(M, wc, win)
    w = np.linspace(0, PI, ng)
    A = amp(h, w)
    ic = np.searchsorted(w, wc)
    z = ic + int(np.argmax(A[ic:] <= 0))
    o = ic - int(np.argmax((A[:ic] >= 1)[::-1]))
    d = max(np.max(np.abs(A[z:])), np.max(np.abs(A[:o] - 1)))
    bad_p = np.where(np.abs(A[:ic] - 1) > d * (1 + 1e-6))[0]
    bad_s = np.where(np.abs(A[ic:]) > d * (1 + 1e-6))[0]
    D = (w[ic + bad_s[-1] + 1] - w[bad_p[0] - 1]) * M / (2 * PI)
    return 20 * math.log10(d), D


tab = {"boxcar": ("g", "k"), "hann": ("h", "l"), "hamming": ("i", "m"), "blackman": ("j", "n")}
for win, (ke, kd) in tab.items():
    e, D = window_stats(win, 100, PI / 2)
    v.check(f"Txt 16-06.{ke}", e)
    v.check(f"Txt 16-06.{kd}", D)
    e50, _ = window_stats(win, 50, PI / 2)
    if win != "hamming":
        v.assert_true(f"{win}: error changes < 0.6 dB from M = 100 to 50", abs(e50 - e) < 0.6)
v.check("Txt 16-06.w", window_stats("hamming", 50, PI / 2)[0])
ham = [window_stats("hamming", 100, f * PI)[0] for f in np.linspace(0.15, 0.85, 15)]
v.check("Txt 16-06.o", max(ham))
v.assert_true("Hamming's deepest error over cutoffs is the pi/2 value -54.2", abs(min(ham) + 54.2) < 0.05)
v.check("Txt 16-06.p", (54.2 - 8) / (2.285 * 2 * PI))
v.check("Txt 16-06.q", (75.3 - 8) / (2.285 * 2 * PI))
for name, sw in (("hann", "hann"), ("hamming", "hamming"), ("blackman", "blackman")):
    v.assert_true(f"lab {name} window is scipy's symmetric window",
                  np.allclose(fd.window(name, 40), signal.windows.get_window(sw, 41, fftbins=False)))
v.assert_true("lab Kaiser window (I0 series) equals scipy's",
              np.allclose(fd.window("kaiser", 174, 5.653), signal.windows.kaiser(175, 5.653)))

# ------------------------------------------------------------------------------------------------- Example 1
h1 = np.array([1, 2, 3, 2, 1]) / 9
_, H = signal.freqz(h1, 1, worN=np.linspace(0, PI, 500))
gd = signal.group_delay((h1, 1), w=np.linspace(0.1, 1.5, 20))[1]
v.check("Ex 16-06.1a", float(np.mean(gd)))
v.assert_true("group delay is constant", np.ptp(gd) < 1e-9)
v.check("Ex 16-06.1b", abs(np.sum(h1 * (-1.0) ** np.arange(5))))
v.check("Ex 16-06.1c", 20 * math.log10(abs(np.sum(h1 * (-1.0) ** np.arange(5)))))
z = np.roots(h1 * 9)
v.check("Ex 16-06.1d", float(np.max(np.abs(np.angle(z)))) / PI)
v.assert_true("zeros are double, on the unit circle", np.allclose(np.abs(z), 1, atol=1e-6) and len(z) == 4)
w = np.linspace(0, PI, 400)
v.assert_true("A(w) = (1 + 2 cos w)^2 / 9", np.allclose(amp(h1, w), (1 + 2 * np.cos(w)) ** 2 / 9))
v.check("Ex 16-06.1e", float(np.mean(signal.group_delay(([0.5, 0.5], 1), w=np.linspace(0.1, 2, 10))[1])))
v.assert_true("type II (1,1)/2 has A(pi) = 0", abs(amp([0.5, 0.5], [PI])[0]) < 1e-12)

# ------------------------------------------------------------------------------------------------- Example 2
h2 = firwin_lp(20, PI / 2, "boxcar")
v.assert_true("half-band: even offsets are zero", np.allclose(h2[10 + np.array([2, 4, 6, 8, 10])], 0, atol=1e-15))
v.check("Ex 16-06.2a", h2[11])
v.check("Ex 16-06.2b", h2[13])
w = np.linspace(0, PI, 400001)
A2 = amp(h2, w)
v.check("Ex 16-06.2c", A2.max())
v.check("Ex 16-06.2d", w[np.argmax(A2)] / PI)
v.check("Ex 16-06.2e", 100 * (A2.max() - 1))
v.check("Ex 16-06.2f", -20 * math.log10(abs(A2[w > PI / 2].min())))
v.check("Ex 16-06.2o", np.sum(h2))
v.check("Ex 16-06.2o", 0.5 + 2 / PI * (1 - 1 / 3 + 1 / 5 - 1 / 7 + 1 / 9))
A100 = amp(firwin_lp(100, PI / 2, "boxcar"), w)
v.check("Ex 16-06.2g", 100 * (A100.max() - 1))
hh = firwin_lp(20, PI / 2, "hamming")
v.check("Ex 16-06.2h", hh[11])
v.check("Ex 16-06.2l", hh[13])
hw = signal.windows.hamming(21)
v.check("Ex 16-06.2j", hw[11])
v.check("Ex 16-06.2k", hw[13])
Ah = amp(hh, w)
dh = max(Ah.max() - 1, -Ah.min())     # the worst error in either band (the overshoot and the deepest dip)
v.check("Ex 16-06.2m", dh)
v.check("Ex 16-06.2i", 20 * math.log10(dh))
v.check("Ex 16-06.2n", 3.3 / 0.9)

# ------------------------------------------------------------------------------------------------- Example 3
A = -20 * math.log10(min(dp, ds))
beta = 0.1102 * (A - 8.7)
Mest = (A - 8) / (2.285 * (ws - wp))
v.check("Ex 16-06.3a", A)
v.check("Ex 16-06.3b", beta)
v.check("Ex 16-06.3c", Mest)
kn, kb = signal.kaiserord(A, (ws - wp) / PI)
v.check("Ex 16-06.3k", kn)                      # scipy's kaiserord uses A - 7.95 in place of A - 8
v.assert_true("scipy kaiserord gives the same beta", abs(kb - beta) < 1e-9)
hk = firwin_lp(174, (wp + ws) / 2, ("kaiser", beta))
v.assert_true("lab Kaiser design equals firwin's", np.allclose(hk, fd.window_lowpass(174, wp, ws, "kaiser", beta)))
v.check("Ex 16-06.3d", ripple_pp_db(hk, wp))
a3, b3 = bands(hk, wp, ws)
v.check("Ex 16-06.3e", -20 * math.log10(b3))
v.assert_true("Kaiser M = 174 meets both bands", a3 <= dp and b3 <= ds)
v.check("Ex 16-06.3f", -20 * math.log10(bands(firwin_lp(173, (wp + ws) / 2, ("kaiser", beta)), wp, ws)[1]))
v.check("Ex 16-06.3g", 1000 * (174 / 2) / fs)
v.check("Ex 16-06.3h", (wp + ws) / 2)
v.check("Ex 16-06.3i", 174 / 2)
v.check("Ex 16-06.3j", 20 * math.log10(1.001 / 0.999))

# ------------------------------------------------------------------------------------------------- Example 4


def fs_design(N, kp, T):
    Ak = np.zeros(N)
    Ak[: kp + 1] = 1
    Ak[kp + 1] = T
    Ak[N - kp - 1:] = 1
    Ak[0] = 1
    Ak[N - kp - 1] = T
    k = np.arange(N)
    Hk = Ak * np.exp(-1j * 2 * PI * k * (N - 1) / 2 / N)
    return np.real(np.fft.ifft(Hk))


N4, kp4 = 33, 4
v.assert_true("ifft frequency-sampling design equals the lab formula",
              np.allclose(fs_design(N4, kp4, 0.3), fd.freq_sampling_lowpass(N4, kp4, 0.3)))
w_stop = np.linspace(2 * PI * 6 / 33, PI, 40000)


def stop_peak(T):
    _, H = signal.freqz(fs_design(N4, kp4, T), 1, worN=w_stop)
    return float(np.max(np.abs(H)))


v.check("Ex 16-06.4a", 20 * math.log10(stop_peak(0.0)))
opt = minimize_scalar(stop_peak, bounds=(0, 1), method="bounded", options={"xatol": 1e-9})
v.check("Ex 16-06.4b", opt.x)
v.check("Ex 16-06.4c", 20 * math.log10(opt.fun))
v.check("Ex 16-06.4h", 20 * math.log10(opt.fun / stop_peak(0.0)) * -1)
_, Hp4 = signal.freqz(fs_design(N4, kp4, opt.x), 1, worN=np.linspace(0, 2 * PI * 4 / 33, 40000))
v.check("Ex 16-06.4d", float(np.max(np.abs(np.abs(Hp4) - 1))))
v.check("Ex 16-06.4f", 8 / 33)
v.check("Ex 16-06.4g", 12 / 33)
k = np.arange(17)
v.assert_true("frequency-sampling design passes through its samples",
              np.allclose(amp(fs_design(N4, kp4, 0.393), 2 * PI * k / 33), [1] * 5 + [0.393] + [0] * 11, atol=1e-12))
he = signal.remez(33, [0, 4 / 33, 6 / 33, 0.5], [1, 0], grid_density=64)
e4p, e4s = bands(he, 2 * PI * 4 / 33, 2 * PI * 6 / 33)
v.check("Ex 16-06.4e", max(e4p, e4s))
v.assert_true("equal-weight equiripple: equal errors in both bands", abs(e4p - e4s) / e4s < 0.01)
v.check("Ex 16-06.4i", -20 * math.log10(e4s))

# ------------------------------------------------------------------------------------------------- Example 5
prod = dp * ds
v.check("Ex 16-06.5l", -10 * math.log10(prod))
Mpm = (-10 * math.log10(prod) - 13) / (2.324 * (ws - wp))
v.check("Ex 16-06.5a", Mpm)
v.check("Ex 16-06.5b", (2 / 3) * math.log10(1 / (10 * prod)) * fs / 1000)
lengths = {n: remez(n, wp, ws, dp, ds) for n in range(128, 139)}
ok = {n: meets(h, wp, ws, dp, ds) for n, h in lengths.items()}
nmin = min(n for n in ok if ok[n])
v.check("Ex 16-06.5d", nmin)
v.assert_true("no length from 128 to 136 meets the mask", not any(ok[n] for n in range(128, 137)))
v.check("Ex 16-06.5c", -20 * math.log10(bands(lengths[nmin - 1], wp, ws)[1]))
h136_128 = signal.remez(nmin - 1, [0, wp, ws, PI], [1, 0], weight=[1, dp / ds], fs=2 * PI, grid_density=128)
v.check("Ex 16-06.5s", -20 * math.log10(bands(h136_128, wp, ws)[1]))
v.assert_true("136 taps sits on the mask (passband error within 1e-6 of dp)", abs(bands(h136_128, wp, ws)[0] - dp) < 1e-6)
hp = lengths[137]
v.check("Ex 16-06.5e", ripple_pp_db(hp, wp))
v.check("Ex 16-06.5f", -20 * math.log10(bands(hp, wp, ws)[1]))
alt, _ = count_alternations(hp, wp, ws, dp, ds)
v.check("Ex 16-06.5g", alt)
v.assert_true("alternations = L + 2 with L = 68", alt == 68 + 2)
v.assert_true("lab alternation count agrees", fd.alternations(hp, wp, ws, dp, ds) == alt)
ext_p, ext_s = 0, 0
for lo, hi, D, W in ((0, wp, 1.0, 1.0), (ws, PI, 0.0, dp / ds)):
    ww = np.linspace(lo, hi, NG)
    E = W * (amp(hp, ww) - D)
    a = np.abs(E)
    inner = np.where((a[1:-1] >= a[:-2]) & (a[1:-1] >= a[2:]))[0] + 1
    cnt = 2 + int(np.sum(a[inner] >= 0.99 * a.max()))
    if D == 1.0:
        ext_p = cnt
    else:
        ext_s = cnt
v.check("Ex 16-06.5n", ext_p)
v.check("Ex 16-06.5o", ext_s)
v.check("Ex 16-06.5m", (nmin - 1) - Mpm)
Lk = 174 + 1  # Kaiser taps (Example 3)
v.check("Ex 16-06.5h", math.ceil(nmin / 2))
v.check("Ex 16-06.5p", math.ceil(Lk / 2))
v.check("Ex 16-06.5i", math.ceil(nmin / 2) * fs / 1e6)
v.check("Ex 16-06.5q", math.ceil(Lk / 2) * fs / 1e6)
v.check("Ex 16-06.5j", 1000 * ((nmin - 1) / 2) / fs)
v.check("Ex 16-06.5k", 100 * (1 - nmin / Lk))
v.check("Ex 16-06.5r", math.ceil(nmin / 2) * 100e6 / 1e9)

# ------------------------------------------------------------------------------------------------- §9 and concept checks
v.check("Txt 16-06.r", 68 / 34)                 # R-238: settling 68/fDATA, group delay 34/fDATA
v.check("Txt 16-06.s", 1e6 * 34 / 400e3)
v.check("Txt 16-06.t", 1e6 * 20 / 48000)        # R-238: PCM5122 normal filter, 20 tS
v.check("Txt 16-06.v", 1e6 * 1.2 / 48000)       # R-238: asymmetric FIR, 1.2 tS
v.check("Txt 16-06.u", (80 - 8) / (60 - 8))

# ------------------------------------------------------------------------------------------------- Problem 1
seqs = {"a": [1, -2, 1], "b": [1, 3, 3, 1], "c": [1, 0, -1], "d": [1, -3, 3, -1], "e": [1, 2, 3]}
g0 = {k: abs(np.sum(s)) for k, s in seqs.items()}
gpi = {k: abs(np.sum(np.array(s) * (-1.0) ** np.arange(len(s)))) for k, s in seqs.items()}
v.check("16-06.1a", fd.fir_type(seqs["a"]))
v.check("16-06.1b", gpi["a"])
v.check("16-06.1c", fd.fir_type(seqs["b"]))
v.check("16-06.1d", float(np.mean(signal.group_delay((seqs["b"], 1), w=np.linspace(0.1, 2.5, 10))[1])))
v.check("16-06.1e", g0["b"])
v.check("16-06.1f", fd.fir_type(seqs["c"]))
v.check("16-06.1g", fd.fir_type(seqs["d"]))
v.check("16-06.1h", gpi["d"])
v.check("16-06.1i", g0["e"])
v.check("16-06.1j", gpi["e"])
v.assert_true("(e) is not linear phase", fd.fir_type(seqs["e"]) == 0)
v.assert_true("(a), (c), (d) block DC; (b), (c) block pi",
              g0["a"] == 0 and g0["c"] == 0 and g0["d"] == 0 and gpi["b"] == 0 and gpi["c"] < 1e-12)

# ------------------------------------------------------------------------------------------------- Problem 2
v.check("16-06.2a", delta_from_pp(0.5))
v.check("16-06.2b", -20 * math.log10(min(delta_from_pp(0.5), 0.01)))
v.check("16-06.2c", delta_from_pp(0.01))
v.check("16-06.2d", -20 * math.log10(min(delta_from_pp(0.01), 1e-4)))

# ------------------------------------------------------------------------------------------------- Problem 3
h3 = firwin_lp(6, PI / 3, "boxcar")
v.check("16-06.3a", h3[3])
v.check("16-06.3b", h3[2])
v.check("16-06.3c", h3[1])
v.check("16-06.3d", np.sum(h3))
v.assert_true("h[0] = h[6] = 0", abs(h3[0]) < 1e-15 and abs(h3[6]) < 1e-15)

# ------------------------------------------------------------------------------------------------- Problem 4
for M, ko, kp_ in ((30, "16-06.4a", "16-06.4b"), (300, "16-06.4c", "16-06.4d")):
    ww = np.linspace(0.2 * PI, 0.3 * PI, 400001)
    AA = amp(firwin_lp(M, 0.3 * PI, "boxcar"), ww)
    v.check(ko, 100 * (AA.max() - 1))
    v.check(kp_, 0.3 * PI - ww[np.argmax(AA)])

# ------------------------------------------------------------------------------------------------- Problem 5
wp5, ws5 = 0.4 * PI, 0.45 * PI
dp5, ds5 = 10 ** (0.05 / 20) - 1, 10 ** (-50 / 20)
v.check("16-06.5a", dp5)
v.check("16-06.5b", ds5)
v.check("16-06.5c", -20 * math.log10(min(dp5, ds5)))
v.check("16-06.5d", 2 * PI * 3.3 / (0.05 * PI))
v.check("16-06.5e", 2 * PI * 5.6 / (0.05 * PI))
v.check("16-06.5m", 100 * (224 / 132 - 1))
b5 = 0.5842 * 29 ** 0.4 + 0.07886 * 29
v.check("16-06.5f", b5)
M5 = 42 / (2.285 * 0.05 * PI)
v.check("16-06.5g", M5)
v.check("16-06.5h", math.ceil(M5))
v.check("16-06.5n", 132 - math.ceil(M5))
hham = firwin_lp(132, (wp5 + ws5) / 2, "hamming")
a, b = bands(hham, wp5, ws5)
v.check("16-06.5i", -20 * math.log10(b))
v.check("16-06.5l", 20 * math.log10(1 + a))
v.assert_true("Hamming 132 meets the spec", a <= dp5 and b <= ds5)
hk5 = firwin_lp(118, (wp5 + ws5) / 2, ("kaiser", b5))
a, b = bands(hk5, wp5, ws5)
v.check("16-06.5j", -20 * math.log10(b))
v.check("16-06.5k", 20 * math.log10(1 + a))
v.assert_true("Kaiser 118 meets the spec", a <= dp5 and b <= ds5)
v.assert_true("Hann (M = 124) fails 50 dB", bands(firwin_lp(124, (wp5 + ws5) / 2, "hann"), wp5, ws5)[1] > ds5)

# ------------------------------------------------------------------------------------------------- Problem 6
wp6, ws6, d6 = 0.3 * PI, 0.35 * PI, 10 ** (-3.5)
b6 = 0.1102 * (70 - 8.7)
M6 = 62 / (2.285 * 0.05 * PI)
v.check("16-06.6a", b6)
v.check("16-06.6h", 0.05 * PI)
v.check("16-06.6b", M6)
a, b = bands(firwin_lp(173, (wp6 + ws6) / 2, ("kaiser", b6)), wp6, ws6)
v.check("16-06.6c", -20 * math.log10(b))
v.check("16-06.6i", a)
v.assert_true("M = 173 fails both bands", a > d6 and b > d6)
first = next(M for M in range(173, 200) if meets(firwin_lp(M, (wp6 + ws6) / 2, ("kaiser", b6)), wp6, ws6, d6, d6))
v.check("16-06.6d", first)
b71 = 0.1102 * (71 - 8.7)
M71 = 63 / (2.285 * 0.05 * PI)
v.check("16-06.6e", b71)
v.check("16-06.6f", M71)
h71 = firwin_lp(math.ceil(M71), (wp6 + ws6) / 2, ("kaiser", b71))
a, b = bands(h71, wp6, ws6)
v.check("16-06.6g", -20 * math.log10(b))
v.assert_true("redesign at M = 176 meets both bands", a <= d6 and b <= d6)

# ------------------------------------------------------------------------------------------------- Problem 7
h7 = fs_design(15, 2, 0.0)
v.check("16-06.7a", h7[7])
v.check("16-06.7b", h7[6])
v.check("16-06.7c", h7[0])
kk = np.arange(8)
v.assert_true("A(w_k) equals the samples", np.allclose(amp(h7, 2 * PI * kk / 15), [1, 1, 1, 0, 0, 0, 0, 0], atol=1e-13))
v.check("16-06.7d", amp(h7, [2 * PI * 2.5 / 15])[0])

# ------------------------------------------------------------------------------------------------- Problem 8
dp8, ds8, df8 = 0.01, 0.001, 0.02
v.check("16-06.8a", dp8 / ds8)
v.check("16-06.8b", (-10 * math.log10(dp8 * ds8) - 13) / (2.324 * 2 * PI * df8))
v.check("16-06.8c", (2 / 3) * math.log10(1 / (10 * dp8 * ds8)) / df8)
wp8, ws8 = 0.5 * PI, (0.5 + 2 * df8) * PI
ok8 = {n: meets(remez(n, wp8, ws8, dp8, ds8), wp8, ws8, dp8, ds8) for n in range(124, 134)}
n8 = min(n for n in ok8 if ok8[n])
v.check("16-06.8d", n8)
v.assert_true("lengths 124 to 129 fail", not any(ok8[n] for n in range(124, 130)))

# ------------------------------------------------------------------------------------------------- Problem 9
v.check("16-06.9a", math.ceil(255 / 2))
v.check("16-06.9b", 128 * 100e6 / 1e9)
v.check("16-06.9c", 128 * 100e6 / 400e6)
v.check("16-06.9d", math.ceil(255 * 100e6 / 400e6))

# ------------------------------------------------------------------------------------------------- Problem 10
Mat = np.array([[1, math.cos(PI / 3), 1], [1, math.cos(PI / 2), -1], [1, math.cos(PI), 1]])
rhs = np.array([1, 0, 0])
a0, a1, dlt = np.linalg.solve(Mat, rhs)       # a0 + a1 cos(w_i) + s_i*delta = D_i with E alternating -, +, -
v.check("16-06.10a", dlt)
v.check("16-06.10b", a0)
v.check("16-06.10c", a1)
v.check("16-06.10d", -20 * math.log10(dlt))
h10 = signal.remez(3, [0, 1 / 6, 1 / 4, 0.5], [1, 0], grid_density=256)
v.assert_true("scipy remez returns (1, 1, 1)/3", np.allclose(h10, [1 / 3] * 3, atol=1e-6))
ww = np.concatenate([np.linspace(0, PI / 3, 2000), np.linspace(PI / 2, PI, 2000)])
E10 = a0 + a1 * np.cos(ww) - (ww <= PI / 3)
v.assert_true("error never exceeds 1/3", np.max(np.abs(E10)) <= 1 / 3 + 1e-12)

# ------------------------------------------------------------------------------------------------- Problem 11
dp11, ds11 = delta_from_pp(0.1), 1e-4
v.check("16-06.11a", -10 * math.log10(dp11 * ds11))
res = {}
for fsx, kM, kmul, krate, kdw in ((122.88e6, "16-06.11b", "16-06.11c", "16-06.11d", "16-06.11k"),
                                  (30.72e6, "16-06.11e", "16-06.11f", "16-06.11g", "16-06.11l")):
    dw = 2 * PI * 1e6 / fsx
    Mx = (-10 * math.log10(dp11 * ds11) - 13) / (2.324 * dw)
    mult = math.ceil((math.ceil(Mx) + 1) / 2)
    v.check(kdw, dw)
    v.check(kM, Mx)
    v.check(kmul, mult)
    v.check(krate, mult * fsx / 1e9)
    res[fsx] = mult * fsx
v.check("16-06.11h", res[122.88e6] / res[30.72e6])
for fsx, key, lo in ((122.88e6, "16-06.11i", 410), (30.72e6, "16-06.11j", 98)):
    wpx, wsx = 2 * PI * 9e6 / fsx, 2 * PI * 10e6 / fsx
    okx = {n: meets(remez(n, wpx, wsx, dp11, ds11), wpx, wsx, dp11, ds11) for n in range(lo, lo + 9)}
    nx = min(n for n in okx if okx[n])
    v.check(key, nx)
    v.assert_true(f"{key}: the five lengths below the minimum fail", not any(okx[n] for n in range(nx - 5, nx)))

# ------------------------------------------------------------------------------------------------- Problem 12
h12 = firwin_lp(46, PI / 2, "hamming")
nz = int(np.sum(np.abs(h12) > 1e-12))
v.check("16-06.12a", nz)
v.check("16-06.12b", (nz - 1) // 2)
v.check("16-06.12c", math.ceil(47 / 2))
ww = np.linspace(0, PI, 1001)
v.assert_true("A(w) + A(pi - w) = 1", np.allclose(amp(h12, ww) + amp(h12, PI - ww), 1, atol=1e-12))

# ------------------------------------------------------------------------------------------------- Lab answers
for M, key in ((400, "Lab 16-06.a"), (50, "Lab 16-06.b")):
    ww = np.linspace(0.4 * PI, 0.5 * PI, 400001)
    v.check(key, 100 * (amp(firwin_lp(M, PI / 2, "boxcar"), ww).max() - 1))
_, Ht = signal.freqz(hp, 1, worN=[2 * PI * 3000 / fs, 2 * PI * 6000 / fs])
v.check("Lab 16-06.c", 20 * math.log10(abs(Ht[0])))
v.check("Lab 16-06.d", -20 * math.log10(abs(Ht[1])))
nb = np.arange(6000)
burst = np.exp(-0.5 * ((nb - 2000) / 200) ** 2) * np.cos(2 * PI * 2000 * nb / fs)
out = signal.lfilter(hp, 1, burst)
v.check("Lab 16-06.e", int(np.argmax(np.abs(signal.hilbert(out))) - np.argmax(np.abs(signal.hilbert(burst)))))

sys.exit(v.finish())
