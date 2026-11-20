#!/usr/bin/env python3
"""Verify chapter 16-07 (IIR filter design): examples, text, problems and lab answers.

Routes (independent of the lab where possible):
- warping by direct trigonometry; first-order designs against scipy.signal.bilinear and a direct impulse-response sum;
  -3 dB frequencies by root finding on freqz;
- the Butterworth biquad against scipy.signal.butter(..., fs=...), the cookbook formula and closed forms;
- order bounds re-derived here (Butterworth, Chebyshev, elliptic via scipy.special.ellipk) and their ceilings checked
  against scipy's buttord, cheb1ord and ellipord;
- the lab's pole formulas and bilinear transform against scipy's buttap/cheb1ap and butter/cheby1/ellip;
- group delay by numerically differentiating the unwrapped phase of sosfreqz on a fine grid;
- quantization by rounding the direct-form and section coefficients and finding the roots.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq
from scipy.special import ellipk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
sys.path.insert(0, str(ROOT / "labs" / "16-06-lab"))
from eeverify import Verifier  # noqa: E402
import iirdesign as iir  # noqa: E402

CH = ROOT / "chapters" / "16-07-iir-filter-design.md"
v = Verifier.from_files("16-07", CH, ROOT / "solutions" / "16-07-solutions.md", LAB / "README.md")
PI = math.pi


def fa(fd, fs):
    return fs / PI * math.tan(PI * fd / fs)


def fd_of(fa_, fs):
    return fs / PI * math.atan(PI * fa_ / fs)


def f3db(b, a, fs, lo, hi):
    g0 = abs(signal.freqz(b, a, worN=[0.0])[1][0])
    f = lambda x: abs(signal.freqz(b, a, worN=[2 * PI * x / fs])[1][0]) / g0 - 1 / math.sqrt(2)
    return brentq(f, lo, hi, xtol=1e-9)


def gd_numeric(sos, w):
    """Group delay from the unwrapped phase of sosfreqz, by central differences on a fine grid."""
    h = 1e-6
    _, Hp = signal.sosfreqz(sos, worN=w + h)
    _, Hm = signal.sosfreqz(sos, worN=w - h)
    return -np.angle(Hp / Hm) / (2 * h)


def D_of(Ap, As):
    return (10 ** (As / 10) - 1) / (10 ** (Ap / 10) - 1)


def nb(Ap, As, r):
    return math.log10(D_of(Ap, As)) / (2 * math.log10(r))


def nc(Ap, As, r):
    return math.acosh(math.sqrt(D_of(Ap, As))) / math.acosh(r)


def ne(Ap, As, r):
    k, k1 = 1 / r, 1 / math.sqrt(D_of(Ap, As))
    return ellipk(k * k) * ellipk(1 - k1 * k1) / (ellipk(k1 * k1) * ellipk(1 - k * k))


# ---------------------------------------------------------------------------------------- Example 1 and text
fs = 48000.0
v.check("Ex 16-07.1a", fa(4000, fs) / 1000)
v.check("Ex 16-07.1b", fa(5000, fs) / 1000)
v.check("Ex 16-07.1c", fa(20000, fs) / 1000)
v.check("Ex 16-07.1d", fd_of(20000, fs) / 1000)
v.check("Txt 16-07.c", 100 * (fa(4000, fs) / 4000 - 1))
v.check("Txt 16-07.d", 100 * (1 - fd_of(20000, fs) / 20000))
v.assert_true("lab prewarp/unwarp agree", abs(iir.prewarp(4000, fs) / (2 * PI) - fa(4000, fs)) < 1e-9
              and abs(iir.unwarp(2 * PI * 20000, fs) - fd_of(20000, fs)) < 1e-9)

# ---------------------------------------------------------------------------------------- Example 2
f8 = 8000.0
a_ii = math.exp(-PI / 4)
n = np.arange(400)
h_ii = (PI / 4) * a_ii ** n                      # T h_a(nT)
b_ii, aa_ii = iir.impulse_invariant_first_order(1000, f8)
v.assert_true("impulse-invariant design reproduces T h_a(nT)",
              np.allclose(signal.lfilter(b_ii, aa_ii, np.r_[1.0, np.zeros(399)]), h_ii))
v.check("Ex 16-07.2k", PI / 4)
v.check("Ex 16-07.2a", a_ii)
v.check("Ex 16-07.2b", float(np.sum(h_ii)))
v.check("Ex 16-07.2c", f3db(b_ii, aa_ii, f8, 500, 3000))
_, Hn = signal.freqz(b_ii, aa_ii, worN=[0.0, PI])
v.check("Ex 16-07.2d", abs(Hn[1]) / abs(Hn[0]))
v.check("Ex 16-07.2e", 1 / math.sqrt(1 + 16))
Wc = 2 * PI * 1000
bb, ab = signal.bilinear([Wc], [1, Wc], fs=f8)
v.check("Ex 16-07.2l", bb[0])
v.check("Ex 16-07.2m", -ab[1])
v.check("Ex 16-07.2f", f3db(bb, ab, f8, 500, 1500))
v.check("Ex 16-07.2i", 2 * math.atan(PI / 8))
v.check("Ex 16-07.2j", 100 * (1 - f3db(bb, ab, f8, 500, 1500) / 1000))
v.assert_true("bilinear design has zero gain at Nyquist", abs(signal.freqz(bb, ab, worN=[PI])[1][0]) < 1e-12)
Wpre = 2 * f8 * math.tan(PI / 8)
bp, ap = signal.bilinear([Wpre], [1, Wpre], fs=f8)
v.check("Ex 16-07.2g", math.tan(PI / 8))
v.check("Ex 16-07.2n", bp[0])
v.check("Ex 16-07.2h", f3db(bp, ap, f8, 500, 1500))
v.assert_true("lab first-order bilinear designs equal scipy's",
              np.allclose(iir.bilinear_first_order(1000, f8, False)[0], bb)
              and np.allclose(iir.bilinear_first_order(1000, f8, True)[1], ap))

# ---------------------------------------------------------------------------------------- Example 3
b2, a2 = signal.butter(2, 1000, fs=f8)
v.assert_true("lab biquad equals scipy butter(2)", np.allclose(iir.butter2_biquad(1000, f8)[0], b2)
              and np.allclose(iir.butter2_biquad(1000, f8)[1], a2))
v.check("Ex 16-07.3a", b2[0])
v.check("Ex 16-07.3b", a2[1])
v.check("Ex 16-07.3c", a2[2])
v.assert_true("closed forms: a1 = -2 sqrt2/3, a2 = 1/3, b0 = (2 - sqrt2)/6",
              abs(a2[1] + 2 * math.sqrt(2) / 3) < 1e-12 and abs(a2[2] - 1 / 3) < 1e-12
              and abs(b2[0] - (2 - math.sqrt(2)) / 6) < 1e-12)
p2 = np.roots(a2)
v.check("Ex 16-07.3d", float(np.max(np.abs(p2))))
v.check("Ex 16-07.3i", float(np.max(p2.real)))
v.check("Ex 16-07.3j", float(np.max(p2.imag)))
_, H2 = signal.freqz(b2, a2, worN=[2 * PI * 1000 / f8, 2 * PI * 2000 / f8])
v.check("Ex 16-07.3e", 20 * math.log10(abs(H2[0])))
v.check("Ex 16-07.3f", 20 * math.log10(abs(H2[1])))
v.check("Ex 16-07.3g", -10 * math.log10(1 + 2 ** 4))
v.check("Ex 16-07.3h", float(np.sum(b2)))
v.check("Ex 16-07.3h", float(np.sum(a2)))
w0 = PI / 4
alpha = math.sin(w0) / (2 / math.sqrt(2))
cook_b0 = (1 - math.cos(w0)) / 2 / (1 + alpha)
v.check("Txt 16-07.e", cook_b0)
v.assert_true("cookbook low-pass (Q = 1/sqrt2) equals the Butterworth biquad",
              np.allclose([cook_b0, -2 * math.cos(w0) / (1 + alpha), (1 - alpha) / (1 + alpha)], [b2[0], a2[1], a2[2]]))

# ---------------------------------------------------------------------------------------- Example 4
Wp, Ws = 2 * fs * math.tan(PI * 4000 / fs), 2 * fs * math.tan(PI * 5000 / fs)
r = Ws / Wp
v.check("Ex 16-07.4a", r)
v.check("Ex 16-07.4b", D_of(0.1, 60))
v.check("Ex 16-07.4i", math.sqrt(D_of(0.1, 60)))
v.check("Ex 16-07.4c", nb(0.1, 60, r))
v.check("Ex 16-07.4d", nc(0.1, 60, r))
v.check("Ex 16-07.4e", ne(0.1, 60, r))
v.check("Ex 16-07.4f", nb(0.1, 60, 1.25))
v.check("Ex 16-07.4g", nc(0.1, 60, 1.25))
v.check("Ex 16-07.4h", ne(0.1, 60, 1.25))
v.assert_true("scipy buttord/cheb1ord/ellipord give 38, 14, 8",
              (signal.buttord(4000, 5000, 0.1, 60, fs=fs)[0], signal.cheb1ord(4000, 5000, 0.1, 60, fs=fs)[0],
               signal.ellipord(4000, 5000, 0.1, 60, fs=fs)[0]) == (38, 14, 8))
v.assert_true("lab order bounds agree", abs(iir.order_ellip(0.1, 60, Wp, Ws) - ne(0.1, 60, r)) < 1e-12
              and abs(iir.order_butter(0.1, 60, Wp, Ws) - nb(0.1, 60, r)) < 1e-12)

# ---------------------------------------------------------------------------------------- Example 5
sos = signal.ellip(8, 0.1, 60, 4000, fs=fs, output="sos")
za, pa, ka = signal.ellipap(8, 0.1, 60)
zl, pl, kl = iir.bilinear(za * Wp, pa * Wp, ka * Wp ** (len(pa) - len(za)), fs)
wd = np.linspace(1e-5, PI, 20001)
_, He = signal.sosfreqz(sos, worN=wd)
v.assert_true("lab bilinear of the elliptic prototype equals scipy ellip", np.max(np.abs(iir.response(zl, pl, kl, wd) - He)) < 1e-10)
wp_, ws_ = 2 * PI * 4000 / fs, 2 * PI * 5000 / fs
m = np.abs(He)
v.check("Ex 16-07.5a", 20 * math.log10(m[wd <= wp_].max() / m[wd <= wp_].min()))
v.check("Ex 16-07.5b", -20 * math.log10(m[wd >= ws_].max()))
f60 = brentq(lambda f: 20 * math.log10(abs(signal.sosfreqz(sos, worN=[2 * PI * f / fs])[1][0])) + 60, 4300, 4720, xtol=1e-6)
v.check("Ex 16-07.5c", f60)
z, p, k = signal.sos2zpk(sos)
zf = np.sort(np.angle(z[z.imag > 0])) * fs / (2 * PI) / 1000
v.assert_true("all zeros on the unit circle", np.allclose(np.abs(z), 1, atol=1e-9))
for key, val in zip(("Ex 16-07.5d", "Ex 16-07.5e", "Ex 16-07.5f", "Ex 16-07.5g"), zf):
    v.check(key, val)
rmax = float(np.max(np.abs(p)))
v.check("Ex 16-07.5h", rmax)
v.check("Ex 16-07.5p", rmax / (1 - rmax))
mul = iir.mults_sos(sos)
v.check("Ex 16-07.5i", mul)
v.check("Ex 16-07.5j", mul * fs)
v.check("Ex 16-07.5k", 69 / mul)
v.check("Ex 16-07.5q", 69 * fs / 1e6)
gdn = gd_numeric(sos, np.array([1e-3, wp_]))
v.check("Ex 16-07.5l", gdn[0])
v.check("Ex 16-07.5r", gdn[0] / fs * 1e3)
v.check("Ex 16-07.5m", gdn[1])
wpb = np.linspace(1e-3, wp_, 4001)
g = gd_numeric(sos, wpb)
v.check("Ex 16-07.5n", g.max() - g.min())
v.assert_true("lab root-by-root group delay matches the numerical one", np.allclose(iir.group_delay(z, p, wpb), g, atol=1e-4))
_, aden = signal.sos2tf(sos)
v.check("Ex 16-07.5o", float(np.max(np.abs(aden))))

# endpoint term and aliased sum (16-07 §3.3, Example 2, Problem 7), the aliased sum summed directly
def aliased_sum(wcT, w, M=200000):
    m = np.arange(-M, M + 1)
    return np.sum(wcT / (wcT + 1j * (w + 2 * PI * m))).real + wcT / (2 * PI) * 0  # real part (symmetric sum)


for wcT, kt, kd, kn in ((PI / 4, "Ex 16-07.2o", "Ex 16-07.2p", "Ex 16-07.2q"), (PI / 2, "16-07.7e", "16-07.7f", "16-07.7g")):
    v.check(kt, wcT / 2)
    a0, api = aliased_sum(wcT, 0.0), aliased_sum(wcT, PI)
    v.check(kd, a0)
    v.check(kn, api)
    pz_ = math.exp(-wcT)
    v.assert_true(f"impulse-invariant response = aliased sum + endpoint term ({wcT:.3f})",
                  abs(wcT / (1 - pz_) - (a0 + wcT / 2)) < 1e-4 and abs(wcT / (1 + pz_) - (api + wcT / 2)) < 1e-4)
v.check("16-07.7h", aliased_sum(PI / 2, PI) / aliased_sum(PI / 2, 0.0))
# group delay peaks just beyond the 4 kHz edge (about 84 samples near 4.07 kHz), outermost pole at 4.068 kHz
wg = np.linspace(2 * PI * 3900 / fs, 2 * PI * 4300 / fs, 40001)
gg = gd_numeric(sos, wg)
v.assert_true("Ex 5: delay peak of about 84 samples just beyond the edge", 84 < gg.max() < 84.5 and 4000 < wg[np.argmax(gg)] * fs / (2 * PI) < 4100)
v.assert_true("Ex 5: outermost pole near 4.068 kHz", abs(abs(np.angle(p[np.argmax(np.abs(p))])) * fs / (2 * PI) - 4068) < 1)
# single-polynomial coefficient rounding: unstable at 13 bits or fewer
_, aden8 = signal.sos2tf(sos)
rad = {F: float(np.max(np.abs(np.roots(np.round(aden8 * 2**F) / 2**F)))) for F in range(8, 18)}
v.assert_true("direct form unstable for F <= 13, stable 14..17", all(rad[F] > 1 for F in range(8, 14)) and all(rad[F] < 1 for F in range(14, 18)))
v.check("Txt 16-07.l", rad[13])

# ---------------------------------------------------------------------------------------- Problem 13 (band-pass)
fs13 = 48000.0
W13 = lambda f: 2 * fs13 * math.tan(PI * f / fs13)  # noqa: E731
e13 = [W13(f_) for f_ in (1000, 2000, 500, 4000)]
for key, val in zip(("16-07.13a", "16-07.13b", "16-07.13c", "16-07.13d"), e13):
    v.check(key, val)
O0 = math.sqrt(e13[0] * e13[1])
B13 = e13[1] - e13[0]
v.check("16-07.13e", O0)
v.check("16-07.13f", B13)
v.check("16-07.13g", fs13 / PI * math.atan(O0 / (2 * fs13)))
lp = lambda O: abs(O * O - O0 * O0) / (B13 * O)  # noqa: E731
v.check("16-07.13h", lp(e13[2]))
v.check("16-07.13i", lp(e13[3]))
N13 = math.log10((10**4 - 1) / (10**0.1 - 1)) / (2 * math.log10(min(lp(e13[2]), lp(e13[3]))))
v.check("16-07.13j", N13)
Nn = math.ceil(N13)
v.check("16-07.13k", Nn)
v.assert_true("P13: scipy buttord agrees on the prototype order", signal.buttord([1000, 2000], [500, 4000], 1, 40, fs=fs13)[0] == Nn)
sos13 = signal.iirfilter(*signal.buttord([1000, 2000], [500, 4000], 1, 40, fs=fs13), btype="bandpass", ftype="butter",
                         fs=fs13, output="sos")
zz, pp, _ = signal.sos2zpk(sos13)
v.check("16-07.13l", len(pp))
v.check("16-07.13m", len(sos13))
_, h13 = signal.sosfreqz(sos13, worN=[500, 1000, 2000, 4000], fs=fs13)
v.check("16-07.13n", -20 * math.log10(abs(h13[0])))
v.check("16-07.13o", -20 * math.log10(abs(h13[3])))
v.assert_true("P13: 1 dB at both passband edges", np.allclose(20 * np.log10(np.abs(h13[1:3])), -1, atol=1e-6))

# ---------------------------------------------------------------------------------------- Text and §9
for rho, key in ((0.95, "Txt 16-07.a"), (0.99, "Txt 16-07.b")):
    v.check(key, float(iir.group_delay([], [rho], [0.0])[0]))
v.check("Txt 16-07.f", 1e6 * 17.1 / 48000)       # R-240: linear-phase decimation filter, 17.1/fS
v.check("Txt 16-07.g", 1e6 * 7.7 / 48000)        # R-240: low latency, 7.7/fS
v.check("Txt 16-07.h", 1e6 * 4.1 / 48000)        # R-240: ultra-low latency, 4.1/fS
v.check("Txt 16-07.i", math.tan(PI / 16))
v.check("Txt 16-07.j", 100 * (math.tan(PI / 16) / (PI / 16) - 1))
v.check("Txt 16-07.k", 100 * (math.tan(PI / 8) / (PI / 8) - 1))

# ---------------------------------------------------------------------------------------- Problems
for f_, key in ((1000, "16-07.1a"), (2000, "16-07.1b"), (3000, "16-07.1c")):
    v.check(key, fa(f_, 8000))
b4, a4 = signal.butter(4, 2 * PI * 10000, analog=True)
bd, ad = signal.bilinear(b4, a4, fs=fs)
f3 = f3db(bd, ad, fs, 5000, 12000)
v.check("16-07.1d", f3)
v.check("16-07.1e", 100 * (1 - f3 / 10000))

s = -1000 + 5000j
zz = (16000 + s) / (16000 - s)
v.check("16-07.2a", zz.real)
v.check("16-07.2b", zz.imag)
v.check("16-07.2c", abs(zz))
v.check("16-07.3a", D_of(1, 40))
v.check("16-07.3b", nb(1, 40, 2))
v.check("16-07.3c", nc(1, 40, 2))
v.check("16-07.3d", ne(1, 40, 2))
v.assert_true("analog ord functions give 8, 5, 4",
              (signal.buttord(1, 2, 1, 40, analog=True)[0], signal.cheb1ord(1, 2, 1, 40, analog=True)[0],
               signal.ellipord(1, 2, 1, 40, analog=True)[0]) == (8, 5, 4))

K = math.tan(PI * 100 / fs)
b4h, a4h = signal.butter(1, 100, btype="high", fs=fs)
v.check("16-07.4a", K)
v.check("16-07.4b", b4h[0])
v.check("16-07.4c", -a4h[1])
v.check("16-07.4d", -1 / math.log(-a4h[1]))
v.check("16-07.4e", -1000 / math.log(-a4h[1]) / fs)
v.assert_true("high-pass gain at Nyquist is 1", abs(abs(signal.freqz(b4h, a4h, worN=[PI])[1][0]) - 1) < 1e-12)

_, p3, _ = signal.buttap(3)
v.assert_true("third-order poles are -1 and -1/2 ± j sqrt3/2",
              np.allclose(np.sort_complex(p3), np.sort_complex([-1, -0.5 + 1j * math.sqrt(3) / 2, -0.5 - 1j * math.sqrt(3) / 2])))
_, p4, _ = signal.buttap(4)
ang = np.sort(np.degrees(np.angle(p4)) % 360)
v.check("16-07.5a", ang[0])
v.check("16-07.5b", ang[1])
v.check("16-07.5c", math.cos(math.radians(180 - ang[1])))
v.check("16-07.5d", math.cos(math.radians(180 - ang[0])))

eps = math.sqrt(10 ** 0.1 - 1)
a6 = math.asinh(1 / eps) / 3
_, p6, k6 = signal.cheb1ap(3, 1)
v.check("16-07.6a", eps)
v.check("16-07.6b", a6)
v.check("16-07.6c", math.sinh(a6))
v.check("16-07.6d", math.cosh(a6))
pc = p6[np.argmax(p6.imag)]
v.check("16-07.6e", pc.real)
v.check("16-07.6f", pc.imag)
v.check("16-07.6g", k6 / abs(np.prod(-p6)))
v.assert_true("lab Chebyshev poles equal cheb1ap", np.allclose(np.sort_complex(iir.cheb1_analog(3, 1, 1.0)[1]), np.sort_complex(p6)))

b7, a7 = iir.impulse_invariant_first_order(2000, 8000)
_, H7 = signal.freqz(b7, a7, worN=[0.0, PI])
v.check("16-07.7a", abs(H7[0]))
v.check("16-07.7b", abs(H7[1]))
v.check("16-07.7c", abs(H7[1]) / abs(H7[0]))
v.check("16-07.7d", 1 / math.sqrt(5))

rho = 0.95
v.check("16-07.8a", rho / (1 - rho))
den8 = np.poly([rho * np.exp(1j * PI / 4), rho * np.exp(-1j * PI / 4)]).real
v.check("16-07.8b", float(signal.group_delay(([1.0], den8), w=[PI / 4])[1][0]))

v.check("16-07.9f", fa(40, 1000))
v.check("16-07.9g", fa(50, 1000))
v.check("16-07.9a", ne(0.5, 60, fa(50, 1000) / fa(40, 1000)))
sos9 = signal.ellip(7, 0.5, 60, 40, fs=1000, output="sos")
_, H9 = signal.sosfreqz(sos9, worN=np.linspace(2 * PI * 50 / 1000, PI, 20000))
v.check("16-07.9h", -20 * math.log10(np.max(np.abs(H9))))
dp9 = (10 ** 0.025 - 1) / (10 ** 0.025 + 1)
M9 = (-10 * math.log10(dp9 * 1e-3) - 13) / (2.324 * 2 * PI * 10 / 1000)
v.check("16-07.9b", M9)
v.check("16-07.9c", math.ceil((math.ceil(M9) + 1) / 2))
v.check("16-07.9d", iir.mults_sos(sos9))
v.check("16-07.9e", math.ceil((math.ceil(M9) + 1) / 2) / iir.mults_sos(sos9))

b10 = np.array([1, 3, 3, 1]) / 6
a10 = np.array([1, 0, 1 / 3])
b3, a3 = signal.butter(3, 2000, fs=8000)
v.assert_true("closed form equals butter(3, 2 kHz, fs = 8 kHz)",
              np.allclose(b3, b10) and np.allclose(a3, np.r_[a10, 0.0]))
v.check("16-07.10a", float(np.max(np.abs(np.roots(a10)))))
_, H10 = signal.freqz(b10, a10, worN=[0.0, PI / 2])
v.check("16-07.10b", abs(H10[0]))
v.check("16-07.10c", 20 * math.log10(abs(H10[1])))

pk = float(gd_numeric(sos, np.array([wp_]))[0])
v.check("16-07.11a", pk)
v.check("16-07.11b", pk - float(gd_numeric(sos, np.array([1e-3]))[0]))
v.check("16-07.11c", 1000 * pk / fs)
v.check("16-07.11d", 1000 * 68 / fs)

v.check("16-07.12a", float(np.max(np.abs(aden))))
v.check("16-07.12b", math.ceil(math.log2(np.max(np.abs(aden)))))


def rq(x, f):
    return np.round(x * 2.0 ** f) / 2.0 ** f


for f_, key in ((16, "16-07.12c"), (14, "16-07.12d"), (12, "16-07.12e"), (10, "16-07.12f")):
    v.check(key, float(np.max(np.abs(np.roots(rq(aden, f_))))))
v.check("16-07.12g", max(float(np.max(np.abs(np.roots(rq(sec[3:], 8))))) for sec in sos))
v.assert_true("sections stay stable from 17 down to 8 fractional bits",
              all(max(np.max(np.abs(np.roots(rq(sec[3:], f_)))) for sec in sos) < 1 for f_ in range(8, 18)))
v.check("Ex 16-07.5o", float(np.max(np.abs(aden))))

# ---------------------------------------------------------------------------------------- Lab answers
designs = {}
for name, N, fn in (("cheb", 14, iir.cheb1_analog), ("butter", 38, iir.butter_analog)):
    zz_, pp_, kk_ = iir.bilinear(*fn(N, 0.1, Wp), fs)
    designs[name] = signal.zpk2sos(zz_, pp_, kk_)
sc = signal.cheby1(14, 0.1, 4000, fs=fs, output="sos")
v.assert_true("lab Chebyshev design equals scipy cheby1",
              np.max(np.abs(signal.sosfreqz(designs["cheb"], worN=wd)[1] - signal.sosfreqz(sc, worN=wd)[1])) < 1e-9)
Wc38 = Wp / (10 ** 0.01 - 1) ** (1 / 76)
sb = signal.butter(38, fd_of(Wc38 / (2 * PI), fs), fs=fs, output="sos")
v.assert_true("lab Butterworth design equals scipy butter at the same cutoff",
              np.max(np.abs(signal.sosfreqz(designs["butter"], worN=wd)[1] - signal.sosfreqz(sb, worN=wd)[1])) < 1e-9)
for name, ka_, kd_, km_ in (("cheb", "Lab 16-07.a", "Lab 16-07.c", "Lab 16-07.e"), ("butter", "Lab 16-07.b", "Lab 16-07.d", "Lab 16-07.f")):
    so = designs[name]
    v.check(ka_, -20 * math.log10(abs(signal.sosfreqz(so, worN=[ws_])[1][0])))
    gg = gd_numeric(so, wpb)
    v.check(kd_, gg.max() - gg.min())
    v.check(km_, iir.mults_sos(so))

sys.exit(v.finish())
