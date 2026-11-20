#!/usr/bin/env python3
"""Verify every number in chapter 11-05 (Fourier series), its solutions and lab.

Independent routes (the chapter's closed forms are not used to produce checked values):
- coefficients by numerical integration of the analysis formula over one period (scipy quad, with the
  discontinuities passed as breakpoints), cross-checked by FFTs of one sampled period;
- the Gibbs peak by evaluating partial sums on a fine grid and by the sine integral Si(pi);
- powers and THD by integrating x^2 over a period and comparing with sums of squared coefficients;
- the PWM ripple by integrating the RC circuit's ODE to periodic steady state;
- filter outputs by applying H(jk w0) to numerically computed coefficients;
- the AM example by listing harmonics; data-sheet values (R-179, R-188) quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import sici

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-05", COURSE / "chapters" / "11-05-fourier-series.md",
                        COURSE / "solutions" / "11-05-solutions.md",
                        COURSE / "labs" / "11-05-lab" / "README.md")


def ck(x, k, T0=1.0, breaks=()):
    w0 = 2 * math.pi / T0
    br = [b for b in breaks if 0 < b < T0]
    re = quad(lambda t: x(t) * math.cos(k * w0 * t), 0, T0, points=br or None, limit=500)[0]
    im = quad(lambda t: -x(t) * math.sin(k * w0 * t), 0, T0, points=br or None, limit=500)[0]
    return complex(re, im) / T0


def power(x, T0=1.0, breaks=()):
    br = [b for b in breaks if 0 < b < T0]
    return quad(lambda t: x(t) ** 2, 0, T0, points=br or None, limit=500)[0] / T0


db = lambda r: 20 * math.log10(r)
square = lambda t: 1.0 if (t % 1.0) < 0.5 else -1.0
pwm = lambda t: 3.3 if (t % 1.0) < 0.25 else 0.0
triangle = lambda t: 1 - 4 * abs((t % 1.0) - 0.5) if True else 0.0          # -1 at t = 0, +1 at t = 0.5


def partial_peak(N, M=40001):
    th = np.linspace(1e-7, 3 * math.pi / (N + 1), M)
    y = sum(4 / (math.pi * k) * np.sin(k * th) for k in range(1, N + 1, 2))
    i = int(np.argmax(y))
    return y[i], th[i]


# ============================================================ theory and practitioner
pk99, loc99 = partial_peak(99)
v.check("T 11-05.a", pk99)
v.check("T 11-05.b", 100 * 2 * abs(ck(square, 1, breaks=(0.5,))) ** 2 / power(square, breaks=(0.5,)))
A1sq = 2 * abs(ck(square, 1, breaks=(0.5,)))
v.check("T 11-05.c", 100 * math.sqrt((power(square, breaks=(0.5,)) - A1sq ** 2 / 2) / (A1sq ** 2 / 2)))
v.check("T 11-05.e", 400)                                            # TPA3116D2 f_OSC options [R-188]
v.check("T 11-05.f", 1200)
fc, f0, A, D = 1e3, 100e3, 3.3, 0.25
c1pwm = abs(ck(pwm, 1, breaks=(0.25,)))
v.check("T 11-05.g", 2 * c1pwm / abs((1 + 1j * f0 / fc) ** 2) * 1e3)
v.assert_true("orthogonality of harmonics", abs(quad(lambda t: math.cos(2 * math.pi * 3 * t) * math.cos(
    2 * math.pi * 5 * t), 0, 1)[0]) < 1e-12)

# ============================================================ Example 1
for key, k in (("a", 1), ("b", 3), ("c", 5)):
    v.check(f"Ex 11-05.1{key}", 2 * abs(ck(square, k, breaks=(0.5,))))
v.assert_true("no even harmonics in the square wave", abs(ck(square, 2, breaks=(0.5,))) < 1e-10)

# ============================================================ Example 2
v.check("Ex 11-05.2a", ck(pwm, 0, breaks=(0.25,)).real)
v.check("Ex 11-05.2b", c1pwm / ck(pwm, 0, breaks=(0.25,)).real)
v.check("Ex 11-05.2c", c1pwm)
v.check("Ex 11-05.2d", 2 * c1pwm)
c2pwm = abs(ck(pwm, 2, breaks=(0.25,)))
v.check("Ex 11-05.2e", c2pwm)
v.check("Ex 11-05.2f", 2 * c2pwm)
v.check("Ex 11-05.2g", abs(ck(pwm, 4, breaks=(0.25,))))
# FFT cross-check of the PWM coefficients
M = 8192
tm = (np.arange(M) + 0.5) / M
X = np.fft.fft(np.where(tm < 0.25, 3.3, 0.0)) / M
v.assert_true("FFT agrees with integration for the PWM c_1", abs(abs(X[1]) - c1pwm) < 1e-6)

# ============================================================ Example 3
Psq = power(square, breaks=(0.5,))
sh = lambda K: sum(2 * abs(ck(square, k, breaks=(0.5,))) ** 2 for k in range(1, K + 1))
v.check("Ex 11-05.3a", 100 * sh(1) / Psq)
v.check("Ex 11-05.3b", 100 * sh(5) / Psq)
v.check("Ex 11-05.3c", 100 * math.sqrt((Psq - sh(1)) / sh(1)))

# ============================================================ Example 4
v.check("Ex 11-05.4a", pk99)
v.check("Ex 11-05.4b", loc99)
pk999, _ = partial_peak(999)
v.check("Ex 11-05.4c", pk999)
v.check("Ex 11-05.4d", 100 * (pk999 - 1) / 2)
v.check("Ex 11-05.4e", 2 / math.pi * sici(math.pi)[0])

# ============================================================ Example 5: triangle with peak +1 at t = 0
tri0 = lambda t: 1 - 4 * abs(((t + 0.5) % 1.0) - 0.5)                # +1 at t = 0, -1 at t = 0.5
A1t = 2 * abs(ck(tri0, 1, breaks=(0.5,)))
A3t = 2 * abs(ck(tri0, 3, breaks=(0.5,)))
v.check("Ex 11-05.5a", A1t)
v.check("Ex 11-05.5b", A3t)
v.check("Ex 11-05.5c", db(A3t / A1t))
v.check("Ex 11-05.5d", db(2 * abs(ck(square, 3, breaks=(0.5,))) / A1sq))
v.assert_true("triangle coefficients are real (even signal)", abs(ck(tri0, 1, breaks=(0.5,)).imag) < 1e-12)

# ============================================================ Example 6: full-wave rectified sine (period 1/120 s)
fw = lambda t: abs(math.sin(2 * math.pi * 60 * t))
Tfw = 1 / 120
v.check("Ex 11-05.6a", ck(fw, 0, T0=Tfw).real)
v.check("Ex 11-05.6b", 2 * abs(ck(fw, 1, T0=Tfw)))
v.check("Ex 11-05.6c", 2 * abs(ck(fw, 2, T0=Tfw)))

# ============================================================ Example 7: PWM DAC, ripple from the ODE
v.check("Ex 11-05.7a", ck(pwm, 0, breaks=(0.25,)).real * abs(1 / (1 + 0j)))
H = lambda f: 1 / (1 + 1j * f / fc)
v.check("Ex 11-05.7b", abs(H(f0)))
v.check("Ex 11-05.7c", 2 * c1pwm * abs(H(f0)) * 1e3)
v.check("Ex 11-05.7d", abs(H(2 * f0)))
v.check("Ex 11-05.7e", 2 * c2pwm * abs(H(2 * f0)) * 1e3)
T0 = 1 / f0
RC = 1 / (2 * math.pi * fc)
src = lambda t: A if (t % T0) < D * T0 else 0.0
ode = solve_ivp(lambda t, y: [(src(t) - y[0]) / RC], (0, 300 * T0), [A * D], max_step=T0 / 400,
                rtol=1e-10, atol=1e-13, dense_output=True)               # 300 periods = 19 RC: steady state
tt = np.linspace(299 * T0, 300 * T0, 20001)
vv = ode.sol(tt)[0]
pp = vv.max() - vv.min()
v.check("Ex 11-05.7f", pp * 1e3)
v.check("T 11-05.d", pp * 1e3)
v.check("Ex 11-05.7g", 2 * 2 * c1pwm * abs(H(f0)) * 1e3)
v.check("Ex 11-05.7h", (A - A * D) * D * T0 / RC * 1e3)
v.check("Lab 11-05.g", pp * 1e3)

# ============================================================ Example 8: harmonic placement
def nearest(fsw, station, fmax=2000):
    return min(abs(k * fsw - station) for k in range(1, fmax // fsw + 1))


v.check("Ex 11-05.8a", nearest(400, 1000))
v.check("Ex 11-05.8b", nearest(500, 1000))
v.check("Ex 11-05.8c", nearest(600, 1000))
band = (917, 1125)
straddle = lambda fsw: any(k * fsw < band[0] and (k + 1) * fsw > band[1] for k in range(1, 6))
v.assert_true("400 and 600 kHz straddle 917-1125 kHz; 500 kHz does not",
              straddle(400) and straddle(600) and not straddle(500))

# ============================================================ solutions
x1 = lambda t: 3 + 2 * math.cos(2 * math.pi * t) + math.sin(3 * 2 * math.pi * t - math.pi / 4)
v.check("11-05.1a", ck(x1, 0).real)
v.check("11-05.1b", ck(x1, 1).real)
c3 = ck(x1, 3)
v.check("11-05.1c", abs(c3))
v.check("11-05.1d", math.degrees(math.atan2(c3.imag, c3.real)))
x1b = lambda t: math.cos(2 * math.pi * t) ** 2
v.check("11-05.1e", ck(x1b, 0).real)
v.check("11-05.1f", ck(x1b, 2).real)
p3 = lambda t: 5.0 if (t % 1.0) < 1 / 3 else 0.0
v.check("11-05.3a", ck(p3, 0, breaks=(1 / 3,)).real)
v.check("11-05.3b", abs(ck(p3, 1, breaks=(1 / 3,))))
v.check("11-05.3c", 2 * abs(ck(p3, 1, breaks=(1 / 3,))))
v.check("11-05.3d", next(k for k in range(1, 20) if abs(ck(p3, k, breaks=(1 / 3,))) < 1e-9))
saw = lambda t: ((t + math.pi) % (2 * math.pi)) - math.pi
bk = lambda k: 2 / (2 * math.pi) * quad(lambda t: saw(t) * math.sin(k * t), -math.pi, math.pi, points=[0])[0]
v.check("11-05.4a", bk(1))
v.check("11-05.4b", bk(2))
v.check("11-05.4c", bk(3))
v.check("11-05.4d", sum(bk(k) * math.sin(k * math.pi) for k in range(1, 50)))
hw = lambda t: max(math.sin(2 * math.pi * t), 0.0)
v.check("11-05.5a", ck(hw, 0, breaks=(0.5,)).real)
for key, k in (("b", 1), ("c", 2), ("d", 4)):
    v.check(f"11-05.5{key}", 2 * abs(ck(hw, k, breaks=(0.5,))))
sq01 = lambda t: 1.0 if ((t + 0.25) % 1.0) < 0.5 else 0.0               # high on (-1/4, 1/4)
c1s = ck(sq01, 1, breaks=(0.25, 0.75))
v.check("11-05.6a", abs(c1s))
v.assert_true("shifted 0-to-1 square wave has real coefficients", abs(c1s.imag) < 1e-12)
v.check("11-05.7a", power(triangle, breaks=(0.5,)))
v.check("11-05.7b", sum(1 / k ** 4 for k in range(1, 200001, 2)))
A1tri = 2 * abs(ck(triangle, 1, breaks=(0.5,)))
Ptri = power(triangle, breaks=(0.5,))
v.check("11-05.7c", 100 * (A1tri ** 2 / 2) / Ptri)
v.check("11-05.7d", 100 * math.sqrt((Ptri - A1tri ** 2 / 2) / (A1tri ** 2 / 2)))
I = [10, 6, 3, 1.5]
v.check("11-05.8a", 100 * math.sqrt(sum(i * i for i in I[1:])) / I[0])
# RMS of the current waveform by integrating a synthesized waveform
iw = lambda t: sum(math.sqrt(2) * I[n] * math.sin(2 * math.pi * (2 * n + 1) * t) for n in range(4))
v.check("11-05.8b", math.sqrt(power(iw)))
v.check("11-05.8c", I[0] / math.sqrt(power(iw)))
Hs = lambda k: 1 / (1 + 1j * k)                                         # corner at the fundamental
o1 = 2 * ck(square, 1, breaks=(0.5,)) * Hs(1)
o3 = 2 * ck(square, 3, breaks=(0.5,)) * Hs(3)
v.check("11-05.9a", abs(o1))
v.check("11-05.9b", math.degrees(np.angle(o1 / (2 * ck(square, 1, breaks=(0.5,))))))
v.check("11-05.9c", abs(o3))
v.check("11-05.9d", math.degrees(np.angle(o3 / (2 * ck(square, 3, breaks=(0.5,))))))
v.check("11-05.9e", 100 * math.sqrt((Psq - sh(1)) / sh(1)))
# output THD: total output power from the RC ODE's periodic steady state, minus the fundamental
src9 = lambda t: 1.0 if (t % 1.0) < 0.5 else -1.0
o9 = solve_ivp(lambda t, y: [(src9(t) - y[0]) * 2 * math.pi], (0, 30), [0.0], max_step=1e-3, rtol=1e-10,
               atol=1e-12, dense_output=True)
tq = np.linspace(29, 30, 200001)
yq = o9.sol(tq)[0]
Pout = np.mean(yq[:-1] ** 2)
A1out = abs(o1)
v.check("11-05.9f", 100 * math.sqrt((Pout - A1out ** 2 / 2) / (A1out ** 2 / 2)))
Ac = 1.65
sqc = lambda t: Ac if (t % 1.0) < 0.5 else -Ac
v.check("11-05.10a", 2 * abs(ck(sqc, 3, breaks=(0.5,))))
v.check("11-05.10b", 2 * abs(ck(sqc, 1, breaks=(0.5,))) * 10 ** (-40 / 20) * 1e3)
v.check("11-05.10c", 2 * abs(ck(sqc, 5, breaks=(0.5,))) * 10 ** (-30 / 20) * 1e3)
v.check("11-05.11a", pk99)
th = np.linspace(1e-6, 0.5, 200001)
fej = sum((1 - k / 100) * 4 / (math.pi * k) * np.sin(k * th) for k in range(1, 100, 2))
v.check("11-05.11b", fej.max())
fpwm = 64e6 / 4096
lsb = 3.3 / 4096
v.check("11-05.12a", fpwm)
v.check("11-05.12b", lsb * 1e3)
v.check("11-05.12c", lsb / 2 * 1e3)
RC12 = 3.3 * (1 / fpwm) / (4 * lsb / 2)
v.check("11-05.12d", RC12)
v.check("11-05.12e", 1 / (2 * math.pi * RC12))
v.check("11-05.12f", RC12 * math.log(8192))
# check the ripple formula A T/(4RC) at 50% duty against the exact periodic RC solution
a = math.exp(-0.5 / fpwm / RC12)
v0 = 3.3 * (1 - a) * a / (1 - a * a)
v.assert_true("ripple at 50% duty within 1% of A T/(4RC)",
              abs((3.3 + (v0 - 3.3) * a - v0) / (3.3 / fpwm / (4 * RC12)) - 1) < 0.01)
v.check("11-05.13a", nearest(400, 1300))
v.check("11-05.13b", nearest(500, 1300))
v.check("11-05.13c", nearest(600, 1300))
p14 = lambda t: 3.3 if (t % 1.0) < 0.25 else 0.0
P14 = power(p14, breaks=(0.25,))
c014 = ck(p14, 0, breaks=(0.25,)).real
v.check("11-05.14a", P14)
v.check("11-05.14b", c014 ** 2)
v.check("11-05.14c", P14 - c014 ** 2)
v.check("11-05.14d", sum(np.sinc(k * 0.25) ** 2 for k in range(1, 400001)))
Dg = np.linspace(0.01, 0.99, 9801)
v.check("11-05.14e", Dg[np.argmax(Dg * (1 - Dg))])

# ============================================================ lab
v.check("Lab 11-05.a", abs(ck(pwm, 3, breaks=(0.25,))))
v.check("Lab 11-05.b", partial_peak(9)[0])
v.check("Lab 11-05.c", pk999)
v.check("Lab 11-05.d", abs(ck(square, 0, breaks=(0.5,))) ** 2 + sh(199))
v.check("Lab 11-05.e", 2 * c1pwm * abs((1 + 1j * f0 / fc) ** -2) * 1e3)
ts = np.linspace(0, T0, 4001)
y2 = np.full_like(ts, A * D)
for k in range(1, 3001):
    c = A * D * np.sinc(k * D) * np.exp(-1j * math.pi * k * D)
    y2 += 2 * np.real(c * (1 + 1j * k * f0 / fc) ** -2 * np.exp(1j * 2 * math.pi * k * f0 * ts))
v.check("Lab 11-05.f", (y2.max() - y2.min()) * 1e3)

sys.exit(v.finish())
