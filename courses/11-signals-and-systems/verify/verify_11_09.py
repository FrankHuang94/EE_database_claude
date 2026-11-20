#!/usr/bin/env python3
"""Verify every number in chapter 11-09 (the z-transform), its solutions and lab.

Independent routes:
- transforms by summing the defining series numerically (never from the table), and candidate inverse
  sequences checked by summing them back to X(z) at test points inside each ROC;
- residues as numerical limits; sequences by running the difference equations (lfilter and explicit loops);
- poles with numpy.roots; stability by root magnitudes; frequency responses by direct evaluation on the unit
  circle and by measuring filtered sinusoids; edges, peaks and bandwidths by root finding and optimization;
- the bilinear mapping with scipy.signal.bilinear_zpk applied to the CTLE of R-189;
- coefficient grids by brute-force enumeration.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-09", COURSE / "chapters" / "11-09-z-transform.md",
                        COURSE / "solutions" / "11-09-solutions.md",
                        COURSE / "labs" / "11-09-lab" / "README.md")
db = lambda r: 20 * math.log10(r)


def zsum(x, z, n0=0):
    """Sum x[n] z^{-n} for a finite array x starting at index n0."""
    n = n0 + np.arange(len(x))
    return complex(np.sum(np.asarray(x, dtype=complex) * z ** (-n.astype(float))))


def geo(a, N=4000):
    return a ** np.arange(N, dtype=float)


def resid(X, p, eps=1e-7):
    return ((1 - p / (p + eps)) * X(p + eps) + (1 - p / (p - eps)) * X(p - eps)) / 2


def H_on_circle(b, a, w):
    e = np.exp(-1j * w)
    return np.polyval(b[::-1], e) / np.polyval(a[::-1], e)


def impulse(b, a, N):
    x = np.zeros(N)
    x[0] = 1
    return signal.lfilter(b, a, x)


def sine_gain(b, a, w, N=20000):
    """Steady-state amplitude of the response to cos(w n), by a least-squares fit of A cos + B sin over the
    second half of the record (sampled peaks miss the true peak when the phase shift is not whole samples)."""
    n = np.arange(N)
    y = signal.lfilter(b, a, np.cos(w * n))[N // 2:]
    m = n[N // 2:]
    coef, *_ = np.linalg.lstsq(np.column_stack([np.cos(w * m), np.sin(w * m)]), y, rcond=None)
    return float(np.hypot(*coef))


# ============================================================ theory / practitioner
def thmin(B):
    q = 2.0 ** -B
    r = math.sqrt(1 - q)
    k = math.floor(2 * r / q)
    while k * q >= 2 * r:
        k -= 1
    return r, k * q, math.acos(k * q / (2 * r))


_, _, th15 = thmin(15)
v.check("T 11-09.a", th15)
v.check("T 11-09.b", th15 * 48000 / (2 * math.pi))
fsE = 500.0
w60 = 2 * math.pi * 60 / fsE
hfir = np.array([1, -2 * math.cos(w60), 1])
hfir = hfir / hfir.sum()
v.check("T 11-09.c", abs(H_on_circle(hfir, np.array([1.0]), 2 * math.pi * 50 / fsE)))
v.check("T 11-09.d", abs(H_on_circle(hfir, np.array([1.0]), 2 * math.pi * 120 / fsE)))
v.check("T 11-09.e", (512e3 / 4) / 500)
radii = sorted({round(abs(p), 12) for p in np.roots(np.polymul([1, -0.5], [1, -2]))})
v.check("T 11-09.f", len(radii) + 1)
v.check("T 11-09.g", 0.1 * math.pi * 10e3 / (2 * math.pi))
# resonator at r = 0.99, angle 0.1 pi: measure the -3 dB bandwidth numerically
a99 = np.array([1, -2 * 0.99 * math.cos(0.1 * math.pi), 0.99 ** 2])
mag99 = lambda w: abs(1 / np.polyval(a99[::-1], np.exp(-1j * w)))
pk99 = minimize_scalar(lambda w: -mag99(w), bounds=(0.25, 0.38), method="bounded", options={"xatol": 1e-12}).x
lo99 = brentq(lambda w: mag99(w) - mag99(pk99) / math.sqrt(2), 0.2, pk99)
hi99 = brentq(lambda w: mag99(w) - mag99(pk99) / math.sqrt(2), pk99, 0.45)
v.check("T 11-09.h", (hi99 - lo99) * 10e3 / (2 * math.pi), rtol=0.03)   # the 2(1 - r) estimate, within 3%
v.check("T 11-09.i", 1 / (1 - 0.99))
v.assert_true("exact time constant -1/ln(0.99) is within 1% of 100", abs(-1 / math.log(0.99) - 100) < 1)
v.check("T 11-09.j", 1 / (1 - 0.99) / 10e3 * 1e3)
n1 = lambda r: next(n for n in range(1, 100000) if r ** n <= 0.01)
v.check("T 11-09.k", n1(0.98))
v.check("T 11-09.l", n1(0.98) / fsE)
v.check("T 11-09.m", math.log(0.01) / math.log(0.995) / (math.log(0.01) / math.log(0.98)))

# ============================================================ Example 1
x1 = geo(0.5) + geo(0.25)
v.check("Ex 11-09.1a", np.roots(np.polyadd([1, -0.25], [1, -0.5]))[0].real)
v.check("Ex 11-09.1b", zsum(x1, 1.0).real)
v.check("Ex 11-09.1c", zsum(x1, -1.0).real)
v.check("Ex 11-09.1d", zsum(x1, 1e9).real)

# ============================================================ Example 2
X2 = lambda z: 1 / ((1 - 0.5 / z) * (1 - 2 / z))
A1, A2 = resid(X2, 0.5).real, resid(X2, 2.0).real
v.check("Ex 11-09.2a", A1)
v.check("Ex 11-09.2b", A2)
npos = np.arange(0, 200)
nneg = np.arange(-200, 0)
st_pos = -(1 / 3) * 0.5 ** npos
st_neg = -(4 / 3) * 2.0 ** nneg
z_test = 1.1 * np.exp(0.7j)
v.assert_true("stable sequence sums back to X inside the ring",
              abs(zsum(st_pos, z_test) + zsum(st_neg, z_test, n0=-200) - X2(z_test)) < 1e-10)
v.check("Ex 11-09.2c", st_pos[0])
v.check("Ex 11-09.2d", st_neg[-1])
v.check("Ex 11-09.2e", st_pos[2])
v.check("Ex 11-09.2f", st_pos.sum() + st_neg.sum())
xc = impulse(np.array([1.0]), np.array([1, -2.5, 1.0]), 10)
v.assert_true("causal sequence is the recursion's impulse response",
              abs(xc[3] - (-(1 / 3) * 0.125 + (4 / 3) * 8)) < 1e-12)
v.check("Ex 11-09.2g", xc[3])
xa = lambda n: (1 / 3) * 0.5 ** n - (4 / 3) * 2.0 ** n
an = np.arange(-300, 0)
v.assert_true("anticausal sequence sums back to X at |z| = 0.3",
              abs(zsum(xa(an), 0.3 * np.exp(0.4j), n0=-300) - X2(0.3 * np.exp(0.4j))) < 1e-9)
v.check("Ex 11-09.2h", xa(-2))

# ============================================================ Example 3: resonator
r, th = 0.9, math.pi / 4
aR = np.array([1, -2 * r * math.cos(th), r * r])
hR = impulse(np.array([1.0]), aR, 10)
v.check("Ex 11-09.3a", aR[1])
v.check("Ex 11-09.3b", hR[1])
v.check("Ex 11-09.3c", hR[2])
v.check("Ex 11-09.3d", hR[3])
v.check("Ex 11-09.3e", hR[4])
v.check("Ex 11-09.3f", hR.sum() + impulse(np.array([1.0]), aR, 400)[10:].sum())
v.check("Ex 11-09.3g", abs(np.exp(1j * th) - r * np.exp(-1j * th)))
v.check("Ex 11-09.3h", 1 / ((1 - r) * abs(np.exp(1j * th) - r * np.exp(-1j * th))))
v.check("Ex 11-09.3i", 2 * (1 - r))
v.assert_true("exact peak 7.443 is within 0.2% of the estimate",
              abs(-minimize_scalar(lambda w: -abs(1 / np.polyval(aR[::-1], np.exp(-1j * w))), bounds=(0.6, 0.9),
                                   method="bounded").fun / 7.433 - 1) < 0.002)

# ============================================================ Example 4: IIR notch
rr = 0.98
bN = np.array([1, -2 * math.cos(w60), 1])
aN = np.array([1, -2 * rr * math.cos(w60), rr * rr])
K = np.polyval(aN[::-1], 1) / np.polyval(bN[::-1], 1)
HN = lambda w: abs(K * H_on_circle(bN, aN, w))
v.check("Ex 11-09.4a", w60 / math.pi)
v.check("Ex 11-09.4b", math.cos(w60))
v.check("Ex 11-09.4c", aN[1])
v.check("Ex 11-09.4d", aN[2])
v.check("Ex 11-09.4e", K)
v.check("Ex 11-09.4f", HN(2 * math.pi * 50 / fsE))
v.check("Ex 11-09.4g", HN(2 * math.pi * 120 / fsE))
v.check("Ex 11-09.4h", HN(math.pi))
loN = brentq(lambda w: HN(w) - 1 / math.sqrt(2), w60 - 0.1, w60)
hiN = brentq(lambda w: HN(w) - 1 / math.sqrt(2), w60, w60 + 0.1)
v.check("Ex 11-09.4i", loN * fsE / (2 * math.pi))
v.check("Ex 11-09.4j", hiN * fsE / (2 * math.pi))
v.check("Ex 11-09.4k", (hiN - loN) * fsE / (2 * math.pi))
v.check("Ex 11-09.4l", 2 * (1 - rr) * fsE / (2 * math.pi))
v.check("Ex 11-09.4m", -bN[1])
v.check("Ex 11-09.4n", -1 / math.log(rr))
v.assert_true("notch nulls 60 Hz", HN(w60) < 1e-12)

# ============================================================ Example 5: stability triangle
def margin(a1, a2):
    return 1 + a2 - abs(a1)


v.check("Ex 11-09.5a", margin(-1.5, 0.56))
v.check("Ex 11-09.5b", 1 - 1.5 - 0.56)
rf = np.sort(np.roots([1, 1.5, -0.56]))
v.check("Ex 11-09.5c", rf[1])
v.check("Ex 11-09.5d", rf[0])
v.check("Ex 11-09.5e", margin(aR[1], aR[2]))
rng = np.random.default_rng(3)
pts = rng.uniform([-2.5, -1.5], [2.5, 1.5], size=(4000, 2))
agree = all((max(abs(np.roots([1, a1, a2]))) < 1) == (abs(a2) < 1 and abs(a1) < 1 + a2) for a1, a2 in pts)
v.assert_true("triangle test agrees with root magnitudes on 4000 random biquads", agree)

# ============================================================ Example 6: CTLE digitized (R-189)
fb = 53.125e9
fz = fp1 = 21.25e9
fp2 = 53.125e9
G12 = 10 ** (-12 / 20)


def ctle(f):
    return (G12 + 1j * f / fz) / ((1 + 1j * f / fp1) * (1 + 1j * f / fp2))


def digitize(M):
    fs = fb * M
    zs = [-2 * math.pi * fz * G12]
    ps = [-2 * math.pi * fp1, -2 * math.pi * fp2]
    # analog H(s) = (G + s/wz) / ((1 + s/wp1)(1 + s/wp2)) = (wp1*wp2/wz) (s + G wz) / ((s + wp1)(s + wp2))
    k = (2 * math.pi * fp1) * (2 * math.pi * fp2) / (2 * math.pi * fz)
    zd, pd, kd = signal.bilinear_zpk(zs, ps, k, fs)
    return fs, zd, pd, kd


for M, keys in ((32, ("6a", "6b", "6c", "6d", "6e", "6f", "6g")), (2, ("6h", "6i", "6j", "6k", None, "6l", "6m"))):
    fs, zd, pd, kd = digitize(M)
    T = 1 / fs
    v.assert_true(f"M = {M}: digital zeros include z = -1", np.any(np.abs(zd + 1) < 1e-9))
    zr = zd[np.abs(zd + 1) > 1e-9][0].real
    pr = np.sort(pd.real)[::-1]
    v.check(f"Ex 11-09.{keys[0]}", T * 1e12)
    v.check(f"Ex 11-09.{keys[1]}", pr[0])
    v.check(f"Ex 11-09.{keys[2]}", pr[1])
    v.check(f"Ex 11-09.{keys[3]}", zr)
    wN = 2 * math.pi * (fb / 2) * T
    if keys[4]:
        v.check(f"Ex 11-09.{keys[4]}", wN)
    # analog frequency whose digital image is wN: solve the bilinear relation numerically
    fwarp = brentq(lambda f: 2 * math.atan(2 * math.pi * f * T / 2) - wN, 1e9, 1e12, xtol=1)
    v.check(f"Ex 11-09.{keys[5]}", fwarp / 1e9)
    _, hd = signal.freqz_zpk(zd, pd, kd, worN=[wN])
    v.check(f"Ex 11-09.{keys[6]}", db(abs(hd[0])))
    v.assert_true(f"M = {M}: DC gain preserved", abs(abs(signal.freqz_zpk(zd, pd, kd, worN=[0.0])[1][0]) - G12) < 1e-9)
v.check("Ex 11-09.6n", db(abs(ctle(fb / 2))))

# ============================================================ Example 7
y = []
yp = 4.0
for n in range(8):
    yp = 0.5 * yp + 1
    y.append(yp)
v.check("Ex 11-09.7a", y[0])
v.check("Ex 11-09.7b", y[1])
v.check("Ex 11-09.7c", y[5])
v.check("Ex 11-09.7d", 1 / (1 - 0.5))
v.assert_true("closed form 2 + 0.5^n matches", all(abs(y[n] - (2 + 0.5 ** n)) < 1e-12 for n in range(8)))

# ============================================================ solutions
v.check("11-09.1a", zsum(geo(0.8), 2.0).real)
nn = np.arange(-400, 0)
v.check("11-09.1b", zsum(-(0.8 ** nn.astype(float)), 0.5, n0=-400).real)
x2 = [1, 2, 3]
v.check("11-09.2a", zsum(x2, 1.0).real)
v.check("11-09.2b", zsum(x2, -1.0).real)
v.check("11-09.2c", abs(np.roots([1, 2, 3])[0]))
b3, a3 = np.array([1.0, 1.0]), np.array([1, -0.9])
v.check("11-09.3a", abs(H_on_circle(b3, a3, 0.0)))
v.check("11-09.3b", abs(H_on_circle(b3, a3, math.pi / 2)))
v.check("11-09.3c", abs(H_on_circle(b3, a3, math.pi)))
X4 = lambda z: 1 / ((1 - 0.5 / z) * (1 - 1.5 / z))
v.check("11-09.4a", resid(X4, 0.5).real)
v.check("11-09.4b", resid(X4, 1.5).real)
h4 = lambda n: -0.5 * 0.5 ** n if n >= 0 else -1.5 * 1.5 ** n
z4 = 1.0 * np.exp(0.3j)
v.assert_true("stable h sums back to H on the unit circle",
              abs(sum(h4(n) * z4 ** (-n) for n in range(-300, 300)) - X4(z4)) < 1e-9)
v.check("11-09.4c", h4(0))
v.check("11-09.4d", h4(-1))
X5 = lambda z: (1 - 0.2 / z) / ((1 - 0.8 / z) * (1 + 0.4 / z))
x5 = impulse(np.array([1, -0.2]), np.polymul([1, -0.8], [1, 0.4]), 6)
v.check("11-09.5a", resid(X5, 0.8).real)
v.check("11-09.5b", resid(X5, -0.4).real)
v.check("11-09.5c", x5[0])
v.check("11-09.5d", x5[1])
v.check("11-09.5e", x5[2])
x6 = impulse(np.array([1.0]), np.array([1, -1, 0.5]), 6)
for i, k in enumerate("abcde"):
    v.check(f"11-09.6{k}", x6[i])
v.check("11-09.6f", abs(np.roots([1, -1, 0.5])[0]))
y7 = []
yp = -5.0
for n in range(40):
    yp = 0.8 * yp + 1
    y7.append(yp)
v.check("11-09.7a", y7[0])
v.check("11-09.7b", y7[1])
v.check("11-09.7c", 1 / (1 - 0.8))
v.check("11-09.7d", next(n for n in range(40) if abs(y7[n] - 5) < 0.05))
b8 = np.array([1, 0, 0, 0, -1.0])
nulls = [w for w in np.linspace(0, math.pi, 4001) if abs(H_on_circle(b8, np.array([1.0]), w)) < 1e-9]
v.check("11-09.8a", nulls[0] * 8 / (2 * math.pi))
v.check("11-09.8b", nulls[1] * 8 / (2 * math.pi))
v.check("11-09.8c", nulls[2] * 8 / (2 * math.pi))
pk8 = minimize_scalar(lambda w: -abs(H_on_circle(b8, np.array([1.0]), w)), bounds=(0.1, 1.4), method="bounded",
                      options={"xatol": 1e-12})
v.check("11-09.8d", -pk8.fun)
v.check("11-09.8e", pk8.x * 8 / (2 * math.pi))
fs9 = 16000.0
th9 = 2 * math.pi * 1000 / fs9
bw9 = 2 * math.pi * 50 / fs9
r9 = 1 - bw9 / 2
a9 = np.array([1, -2 * r9 * math.cos(th9), r9 * r9])
m9 = lambda w: abs(1 / np.polyval(a9[::-1], np.exp(-1j * w)))
pk9 = minimize_scalar(lambda w: -m9(w), bounds=(th9 - 0.05, th9 + 0.05), method="bounded", options={"xatol": 1e-13})
lo9 = brentq(lambda w: m9(w) - m9(pk9.x) / math.sqrt(2), th9 - 0.1, pk9.x)
hi9 = brentq(lambda w: m9(w) - m9(pk9.x) / math.sqrt(2), pk9.x, th9 + 0.1)
v.check("11-09.9a", th9)
v.check("11-09.9b", r9)
v.check("11-09.9c", a9[1])
v.check("11-09.9d", a9[2])
v.check("11-09.9e", pk9.x * fs9 / (2 * math.pi))
v.check("11-09.9f", m9(pk9.x))
v.check("11-09.9g", (hi9 - lo9) * fs9 / (2 * math.pi))
v.check("11-09.9h", bw9)
v.check("11-09.9i", 1 - r9)
stable = lambda a1, a2: max(abs(np.roots([1, a1, a2]))) < 1
v.assert_true("classification of the four biquads",
              stable(-1.9, 0.95) and not stable(0.5, -1.2) and not stable(-1.6, 0.55) and stable(1.0, 0.3))
v.check("11-09.10a", margin(-1.9, 0.95))
v.check("11-09.10b", 1 - 1.6 + 0.55)
v.check("11-09.10c", max(np.roots([1, -1.6, 0.55]).real))
v.check("11-09.10d", abs(np.roots([1, 1.0, 0.3])[0]))
T11 = 1e-4
h11 = T11 * np.exp(-1000 * T11 * np.arange(2000))
v.check("11-09.11a", h11[1] / h11[0])
v.check("11-09.11b", h11.sum() / 1e-3)
v.check("11-09.11c", 100 * (h11.sum() / 1e-3 - 1))
zb, pb, kb = signal.bilinear_zpk([], [-1000.0], 1.0, 1 / T11)
v.check("11-09.11d", pb[0].real)
v.assert_true("bilinear DC gain is exactly 1/1000",
              abs(abs(signal.freqz_zpk(zb, pb, kb, worN=[0.0])[1][0]) - 1e-3) < 1e-12)
_, hb = signal.freqz_zpk(zb, pb, kb, worN=np.linspace(0.01, 0.3, 30001))
wq = np.linspace(0.01, 0.3, 30001)
v.check("11-09.11e", wq[np.argmin(np.abs(np.abs(hb) - 1e-3 / math.sqrt(2)))])
bw12 = 2 * math.pi * 1 / fsE
r12 = 1 - bw12 / 2
b12 = np.array([1, -2 * math.cos(w60), 1])
a12 = np.array([1, -2 * r12 * math.cos(w60), r12 * r12])
K12 = np.polyval(a12[::-1], 1) / np.polyval(b12[::-1], 1)
H12 = lambda w: abs(K12 * H_on_circle(b12, a12, w))
lo12 = brentq(lambda w: H12(w) - 1 / math.sqrt(2), w60 - 0.05, w60)
hi12 = brentq(lambda w: H12(w) - 1 / math.sqrt(2), w60, w60 + 0.05)
v.check("11-09.12a", r12)
v.check("11-09.12b", (hi12 - lo12) * fsE / (2 * math.pi))
v.check("11-09.12c", -1 / math.log(r12))
v.check("11-09.12d", -1 / math.log(r12) / fsE)
v.check("11-09.12e", n1(r12))
v.check("11-09.12f", n1(r12) / fsE, rtol=1e-3)
v.check("11-09.12g", bw12)
v.check("11-09.12h", 1 - r12)
r13, a13, th13 = thmin(8)
v.check("11-09.13a", r13)
v.check("11-09.13b", a13)
v.check("11-09.13c", th13)
v.check("11-09.13d", th13 * 48000 / (2 * math.pi))
v.check("11-09.13e", th13 * 8000 / (2 * math.pi))
v.check("11-09.13f", 2 * r13)
h14 = np.ones(8) / 8
v.check("11-09.14a", abs(H_on_circle(h14, np.array([1.0]), 0.0)))
w14 = minimize_scalar(lambda w: abs(H_on_circle(h14, np.array([1.0]), w)), bounds=(0.6, 1.0), method="bounded",
                      options={"xatol": 1e-12}).x
v.check("11-09.14b", w14 / math.pi)
g14 = abs(H_on_circle(h14, np.array([1.0]), math.pi / 8))
v.check("11-09.14c", g14)
v.check("11-09.14d", db(g14))
h14c = np.convolve(np.convolve(h14, h14), h14)
g14c = abs(H_on_circle(h14c, np.array([1.0]), math.pi / 8))
v.check("11-09.14e", g14c)
v.check("11-09.14f", db(g14c))
# wraparound integrator + comb equals the boxcar sum exactly
rngx = np.random.default_rng(5).integers(-100, 100, 5000)
acc = np.cumsum(rngx).astype(np.int64)
wrapped = ((acc + 2 ** 15) % 2 ** 16) - 2 ** 15
comb = wrapped[8:] - wrapped[:-8]
comb = ((comb + 2 ** 15) % 2 ** 16) - 2 ** 15
true = np.convolve(rngx, np.ones(8, dtype=np.int64))[8:len(rngx)]
v.assert_true("16-bit wraparound integrator + comb reproduces the boxcar sum", np.array_equal(comb, true))

# ============================================================ lab
v.check("Lab 11-09.a", sine_gain(K * bN, aN, 2 * math.pi * 50 / fsE))
v.check("Lab 11-09.b", n1(0.98))
v.check("Lab 11-09.c", n1(0.995))
q = 1 / 16
cnt = sum(1 for i in range(-64, 64) for k in range(-32, 32)
          if (lambda a1, a2: abs(a2) < 1 and abs(a1) < 1 + a2 and a1 * a1 < 4 * a2)(i * q, k * q))
v.check("Lab 11-09.d", cnt)
for M, key in ((4, "e"), (8, "f"), (2, "g")):
    fs, zd, pd, kd = digitize(M)
    wN = math.pi / M
    _, hd = signal.freqz_zpk(zd, pd, kd, worN=[wN])
    v.check(f"Lab 11-09.{key}", db(abs(hd[0])) - db(abs(ctle(fb / 2))))

sys.exit(v.finish())
