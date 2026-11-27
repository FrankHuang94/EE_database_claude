#!/usr/bin/env python3
"""Verify the full-length FE practice exam.

What is checked, and how:
- Every numerical answer is recomputed here, by a second route where one exists: finite differences, quadrature,
  numpy solvers, RK4 and scipy step/ramp simulations, sympy transforms and series, scipy distributions, explicit
  cash-flow sums, complex nodal analysis, a frequency sweep for Q, a simulated quantizer and rectifier, a
  closed-loop op-amp sweep, a Biot-Savart integral, a standing-wave sweep, ipaddress, cache, pipeline and
  finite-state-machine models, and the pseudocode loop run as written. Each value is compared with the answer key in
  solutions.md (v.check).
- Every wrong option of a numerical multiple-choice question is recomputed from the mistake that solutions.md names,
  and the options must be exactly {answer} plus those mistakes, each within its printed precision, with the lettered
  answer on the correct value.
- Conceptual answers are checked by the text of the lettered option. The Boolean ones are also checked by truth
  tables: the K-map options, and the state counts by minimizing Moore and Mealy machines.
- Structure: 110 questions; area headings against the NCEES ranges in tools/data/fe_spec.yml; every multiple-choice
  explanation names the three wrong letters; answer letters balanced, with no runs of four and no short periodic
  patterns; question types do not alternate for long stretches.
Questions are located by a fragment of their stem, so the checks follow a question if it is renumbered.
The circuit answers are also simulated in ngspice (fe_circuits.cir, run by tools/run_spice.py).
"""
from __future__ import annotations

import datetime
import ipaddress
import math
import re
import sys
from pathlib import Path

import numpy as np
import sympy as sp
import yaml
from scipy import integrate, optimize, signal, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("fe-practice", SOL)
readme = README.read_text(encoding="utf-8")
sol_text = SOL.read_text(encoding="utf-8")

# ------------------------------------------------------------------ parse questions, options, letters, solutions
QS: dict[int, tuple[str, dict[str, str]]] = {}
for block in re.split(r"^\*\*(?=\d+\.\*\*)", readme, flags=re.M)[1:]:
    n = int(block.split(".", 1)[0])
    body = block.split("**", 1)[1]
    body = re.split(r"^#", body, flags=re.M)[0]
    opt_line = next((ln for ln in body.splitlines() if ln.startswith("(A) ")), None)
    opts = {}
    if opt_line:
        for part in opt_line.split(" · "):
            m = re.match(r"\(([A-D])\) (.+)$", part.strip())
            opts[m.group(1)] = m.group(2)
    QS[n] = (body if not opt_line else body[: body.index(opt_line)], opts)
letters = {int(n_): l_ for n_, l_ in re.findall(r"^\*\*(\d+)\. Answer: \(([A-D])\)", sol_text, re.M)}
SOLS = {int(m.group(1)): m.group(0) for m in re.finditer(r"^\*\*(\d+)\. Answer:.*$", sol_text, re.M)}


def q(fragment):
    """The number of the one question whose stem contains this fragment."""
    hits = [n_ for n_, (stem, _) in QS.items() if fragment in stem]
    assert len(hits) == 1, f"stem fragment {fragment!r} matches {hits}"
    return hits[0]


def value_of(text):
    pub = parse_value(text.replace("−", "-"))
    part = pub.parts[0]
    return part.value, part.halfulp


def key(n_, value):
    v.check(f"FE.{n_:03d}", value)


def mcnum(n_, answer, mistakes, keyed=True):
    """Options must be {answer} + the named mistakes, within printed precision; the letter must mark the answer."""
    opts = QS[n_][1]
    vals = {L: value_of(t) for L, t in opts.items()}
    near = lambda x, L: abs(vals[L][0] - x) <= vals[L][1] * (1 + 1e-9)  # noqa: E731
    correct = [L for L in opts if near(answer, L)]
    v.assert_true(f"Q{n_}: exactly one option equals the computed answer, and it is the lettered one",
                  correct == [letters.get(n_)], f"answer {answer:.6g}, options {opts}, letter {letters.get(n_)}")
    wrong = [L for L in "ABCD" if L != letters.get(n_)]
    matched = sorted(next((i for i, m in enumerate(mistakes) if near(m, L)), -1) for L in wrong)
    v.assert_true(f"Q{n_}: each wrong option is one of the named mistakes, recomputed", matched == [0, 1, 2],
                  f"mistakes {[f'{m:.6g}' for m in mistakes]}, options {opts}")
    if keyed:
        key(n_, answer)


def concept(n_, text):
    opts = QS[n_][1]
    v.assert_true(f"Q{n_}: the lettered option is '{text}'", opts.get(letters.get(n_)) == text, f"options {opts}")


def rk4(f, y0, t_end, n=20000):
    h, t, y = t_end / n, 0.0, np.array(y0, dtype=float)
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
    return y


def pv(flows, i):
    return sum(cf / (1 + i) ** (t + 1) for t, cf in enumerate(flows))


# ================================================================= mathematics
n = q("For $f(x) = x^3e^{-x}$")
f = lambda x: x ** 3 * math.exp(-x)  # noqa: E731
d1 = (f(1 + 1e-5) - f(1 - 1e-5)) / 2e-5
mcnum(n, d1, [3 * math.exp(-1), -math.exp(-1), f(1)])
n = q(r"\int_0^{\pi} \sin^2 x")
xs = np.linspace(0, math.pi, 4001)
mcnum(n, integrate.simpson(np.sin(xs) ** 2, x=xs),
      [integrate.simpson(np.ones_like(xs), x=xs), math.pi / 4, integrate.simpson(np.sin(xs), x=xs)])
n = q("Solve $x + y + z = 6$")
A3, b3 = np.array([[1, 1, 1], [2, -1, 1], [1, 2, -1]], float), np.array([6, 3, 2], float)
sol3 = np.linalg.solve(A3, b3)
v.assert_true(f"Q{n}: the solution satisfies all three equations", np.allclose(A3 @ sol3, b3))
key(n, sol3[2])
n = q("The larger eigenvalue")
M2 = np.array([[4, 1], [2, 3]], float)
ev = sorted(np.linalg.eigvals(M2).real)
mcnum(n, ev[1], [np.trace(M2), np.linalg.det(M2), ev[0]])
key(q("magnitude of $(3 + j4)/(1 - j)$"), abs((3 + 4j) / (1 - 1j)))
n = q("The angle of $-1 + j\\sqrt3$")
z6 = complex(-1, math.sqrt(3))
mcnum(n, math.degrees(np.angle(z6)), [math.degrees(math.atan(z6.imag / z6.real)), math.degrees(math.atan(abs(z6.imag / z6.real))),
                                      math.degrees(np.angle(z6.conjugate())) % 360])
key(q("$dy/dt + 4y = 8$"), rk4(lambda t, y: np.array([8 - 4 * y[0]]), [0.0], 0.25)[0])
n = q("$y'' + 4y' + 13y = 0$")
r8 = np.roots([1, 4, 13])
mcnum(n, abs(r8[0].imag), [abs(r8[0].real), math.sqrt(13), 13])
n = q("second-order Taylor approximation")
xx = sp.symbols("xx")
ser = sp.series(sp.sqrt(1 + xx), xx, 0, 3).removeO()
f2 = sp.diff(sp.sqrt(1 + xx), xx, 2).subs(xx, 0)
mcnum(n, float(ser.subs(xx, 0.4)), [float(sp.series(sp.sqrt(1 + xx), xx, 0, 2).removeO().subs(xx, 0.4)), math.sqrt(1.4),
                                    float(1 + 0.4 / 2 + f2 * 0.4 ** 2)])
v.assert_true(f"Q{n}: the Taylor error is about the next term x^3/16",
              abs(math.sqrt(1.4) - float(ser.subs(xx, 0.4)) - 0.4 ** 3 / 16) < 1e-3)
n = q("magnitude of the gradient")
X_, Y_ = sp.symbols("X_ Y_")
F_ = X_ ** 2 * Y_ + 3 * Y_ ** 2
key(n, math.hypot(*[float(sp.diff(F_, var).subs({X_: 1, Y_: 2})) for var in (X_, Y_)]))
n = q("Newton–Raphson")
fx, dfx = (lambda x: x * x - 2), (lambda x: 2 * x)
mcnum(n, 1 - fx(1) / dfx(1), [1 + fx(1) / dfx(1), math.sqrt(2), 1 - fx(1) / 1])
n = q("angle, in degrees, between")
a_, b_ = np.array([1, 2, 2.0]), np.array([2, -1, 2.0])
key(n, math.degrees(math.acos(a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_)))))

# ================================================================= probability and statistics
n = q("A resistor value is normal")
N1 = stats.norm(1000, 10)
mcnum(n, N1.cdf(1020) - N1.cdf(980), [N1.cdf(1010) - N1.cdf(990), N1.cdf(1030) - N1.cdf(970), N1.cdf(1020) - 0.5])
n = q("at most one defective part")
B50 = stats.binom(50, 0.02)
mcnum(n, B50.cdf(1), [B50.pmf(0), B50.pmf(1), B50.sf(1)])
v.check(f"FE.{n:03d}.P0", B50.pmf(0))
v.check(f"FE.{n:03d}.P1", B50.pmf(1))
v.assert_true(f"Q{n}: the Poisson approximation gives the same 3-figure answer",
              round(stats.poisson(1).cdf(1), 3) == round(B50.cdf(1), 3))
n = q("A test flags 95%")
pop = 1_000_000                                       # count a population for Bayes
bad = pop * 0.02
fl_bad, fl_good = bad * 0.95, (pop - bad) * 0.05
mcnum(n, fl_bad / (fl_bad + fl_good), [fl_bad / bad, fl_bad / pop, (fl_bad + fl_good) / pop])
n = q("Twenty-five measurements")
t24 = stats.t.ppf(0.975, 24)
key(n, t24 * 0.05 / 5 * 1e3)
v.check(f"FE.{n:03d}.t", t24)
n = q("no failures in $10^8$ device-hours")
lam = stats.chi2.ppf(0.95, 2) / (2 * 1e8)              # chi-square bound with zero failures
v.assert_true(f"Q{n}: chi-square and Poisson zero-failure bounds agree", abs(lam - math.log(20) / 1e8) < 1e-15)
key(n, lam * 1e9)

# ================================================================= ethics and professional practice
concept(q("endangers the public"), "the public's safety, health and welfare")
concept(q("A vendor offers an engineer a gift"), "decline it")
concept(q("asked to seal drawings"), "refuse to seal them")
n = q("utility patent application")
filed = datetime.date(2021, 3, 1)
key(n, filed.replace(year=filed.year + 20).year)

# ================================================================= engineering economics
n = q("The present worth of \\$10,000")
mcnum(n, 10_000 * np.prod([1 / 1.08] * 5), [10_000 * 1.08 ** 5, 10_000 * (1 - 5 * 0.08), 10_000 / (1 + 5 * 0.08)])
n = q("A tester costs")
pv_cost = 50_000 - 5_000 / 1.08 ** 6                  # present worth of the cash flows, then annualize
ann = 1 / pv([1.0] * 6, 0.08)
key(n, pv_cost * ann / 1e3)
v.check(f"FE.{n:03d}.AP", ann)
v.check(f"FE.{n:03d}.AF", 1 / sum(1.08 ** k for k in range(6)))
n = q("break-even")
mcnum(n, next(u for u in range(1, 100_000) if 50 * u - 30 * u >= 200_000), [200_000 / 50, 200_000 / 30, 200_000 / 80])
n = q("straight-line book value")
book = 120.0
for _ in range(3):
    book -= (120 - 20) / 5
key(n, book)
n = q("compounded quarterly")
bal = 1.0
for _ in range(4):
    bal *= 1 + 0.06 / 4
mcnum(n, (bal - 1) * 100, [6.0, (math.exp(0.06) - 1) * 100, 6.0 / 4])

# ================================================================= properties of electrical materials
key(q("Copper ($\\rho"), 1.72e-8 * 100 / (math.pi * (1.0e-3 / 2) ** 2))
n = q("A copper winding measures")
mcnum(n, 10 * (1 + 0.00393 * (75 - 20)), [10 * (1 + 0.00393 * 75), 10 * 0.00393 * 55, 10 / (1 + 0.00393 * 55)])
n = q("Silicon at 300 K")
ni, ND = 1e10, 1e16
key(n, 2 * ni ** 2 / (ND + math.sqrt(ND ** 2 + 4 * ni ** 2)))   # exact neutrality solution, stable form
n = q("parallel-plate capacitor")
e0 = 8.854e-12
mcnum(n, 4 * e0 * 1e-4 / 10e-6 * 1e12, [e0 * 1e-4 / 10e-6 * 1e12, e0 / 4 * 1e-4 / 10e-6 * 1e12, 4 * e0 * 1e-4 / 1e-4 * 1e12])

# ================================================================= circuit analysis
n = q("divider of two 10 kΩ resistors")
G = np.array([[1 / 10e3 + 1 / 10e3 + 1 / 10e3]])
key(n, np.linalg.solve(G, [12 / 10e3])[0])
n = q("Thévenin resistance, in Ω")
Gt = np.array([[1 / 2, -1 / 2], [-1 / 2, 1 / 2 + 1 / 6 + 1 / 3]])  # 1 A test source into terminal a; node x behind 2 Ω
rth = np.linalg.solve(Gt, [1.0, 0.0])[0]
mcnum(n, rth, [6 + 3 + 2, 1 / (1 / 6 + 1 / 3), 1 / (1 / 6 + 1 / (3 + 2))])
n = q("A 2 A source feeds node 1")
Gn = np.array([[1 / 4 + 1 / 2, -1 / 2], [-1 / 2, 1 / 2 + 1 / 6]])
Vn = np.linalg.solve(Gn, [2.0, 0.0])
key(n, Vn[1])
v.check(f"FE.{n:03d}.V1", Vn[0])
n = q("The most power it can deliver")
rl = np.linspace(1, 500, 49_901)
mcnum(n, max(10 ** 2 * rl / (50 + rl) ** 2), [10 ** 2 / 50, 10 ** 2 / (50 + 50), (10 / 2) ** 2 / (2 * 50)])
n = q("+10 V for 25% of each period")
tt = np.arange(400_000) / 400_000
wave = np.where(tt < 0.25, 10.0, -2.0)
mcnum(n, math.sqrt(np.mean(wave ** 2)), [np.mean(wave), math.sqrt(np.mean(np.where(tt < 0.25, 10.0, 0.0) ** 2)),
                                         math.sqrt(0.25 * 100 - 0.75 * 4)])
n = q("voltage-controlled current source")


def node_a(g_dep, sign=1.0, extra_res=None):
    """KCL at node a: (12 - va)/2 = va/4 + sign*g_dep*va (+ va/extra_res)."""
    gsum = 1 / 2 + 1 / 4 + sign * g_dep + (1 / extra_res if extra_res else 0)
    return (12 / 2) / gsum


mcnum(n, node_a(0.25), [node_a(0.0), node_a(0.25, -1.0), node_a(0.0, extra_res=0.25)])
n = q("source of phasor $10\\angle 0°$")
w = 1000.0
ZL4, Zb = 1j * w * 4e-3, 2 + 1 / (1j * w * 500e-6)
Va = (10 / 4) / (1 / 4 + 1 / ZL4 + 1 / Zb)             # nodal at node a, independent of the mesh solution
key(n, abs(Va / Zb))
v.check(f"FE.{n:03d}.I1", abs((10 - Va) / 4))
n = q("impedance magnitude of 30 Ω")
Z = 30 + 1j * 2 * math.pi * 60 * 0.1
key(n, abs(Z))
v.check(f"FE.{n:03d}.XL", Z.imag)
n = q("phase of the current relative")
mcnum(n, math.degrees(np.angle(1 / Z)), [math.degrees(np.angle(Z)), -math.degrees(math.atan(Z.real / Z.imag)), np.angle(1 / Z)])
n = q("Find its reactive power")
I41 = 10 * np.exp(-1j * math.acos(0.8))                # current lags the voltage
S41 = 230 * np.conj(I41)
key(n, S41.imag / 1e3)
n = q("shunt capacitance that corrects")


def cap(f_hz, q_var, wfac=2 * math.pi):
    return q_var / (wfac * f_hz * 230 ** 2) * 1e6


c42 = cap(50, S41.imag)
S_after = S41 + 230 ** 2 * np.conj(1j * 2 * math.pi * 50 * c42 * 1e-6)
v.assert_true(f"Q{n}: with the capacitor the source sees unity power factor", abs(S_after.imag) < 1e-6 * abs(S41))
mcnum(n, c42, [cap(60, S41.imag), cap(50, S41.real), cap(50, S41.imag, math.pi)])

# ================================================================= linear systems
n = q("$F(s) = 6/[s(s + 3)]$")
s, t = sp.symbols("s t", positive=True)
key(n, float(sp.inverse_laplace_transform(6 / (s * (s + 3)), s, t).subs(t, sp.Rational(1, 2))))
n = q("$H(s) = (s + 1)/(s^2 + 2s - 3)$")
v.assert_true(f"Q{n}: a right-half-plane pole exists", max(np.roots([1, 2, -3]).real) > 0)
concept(n, "unstable")
n = q("2% settling time")
tt, yy = signal.step(signal.lti([1], [0.2, 1]), T=np.linspace(0, 2, 200_001))
ts = tt[np.where(np.abs(yy - 1) > 0.02)[0][-1] + 1]
mcnum(n, ts, [0.2, tt[np.argmax(yy >= 0.9)], 5 * 0.2])
key(q("$H(s) = 1000/(s + 10)$"), 20 * math.log10(abs(1000 / (100j + 10))))
key(q("A 5 V step is applied"), rk4(lambda t, y: np.array([(5 - y[0]) / (10e3 * 100e-9)]), [0.0], 2e-3)[0])
n = q("The current 0.2 ms later")
rl_ode = lambda t, y: np.array([(10 - 100 * y[0]) / 10e-3])  # noqa: E731
i02 = rk4(rl_ode, [0.0], 0.2e-3)[0] * 1e3
mcnum(n, i02, [100.0, rk4(rl_ode, [0.0], 0.1e-3)[0] * 1e3, 100 - i02])
n = q("quality factor of")
fr = np.linspace(14_000, 18_000, 400_001)
Ir = np.abs(1 / (10 + 1j * 2 * np.pi * fr * 2e-3 + 1 / (1j * 2 * np.pi * fr * 50e-9)))
f0 = fr[np.argmax(Ir)]
band = fr[Ir >= Ir.max() / math.sqrt(2)]
bw = band[-1] - band[0]
mcnum(n, f0 / bw, [math.sqrt(2e-3 / 50e-9), 10 * math.sqrt(50e-9 / 2e-3), f0 * 2e-3 / 10])
v.check(f"FE.{n:03d}.f0", f0 / 1e3)
v.check(f"FE.{n:03d}.BW", bw)

# ================================================================= signal processing
n = q("The Nyquist rate")
mcnum(n, 2 * 4, [4, 2 * 2 * math.pi * 4, 4 / 2])
key(q("A 7 kHz tone"), min(abs(7 - k * 10) for k in range(-3, 4)))
n = q("1024-point DFT")
mcnum(n, np.fft.rfftfreq(1024, 1 / 44_100)[1], [44_100 / 2048, 44_100 / 512, 44_100 / 1000])
n = q("$H(z) = 1/(1 - 0.5z^{-1})$")
hh, prev = [], 0.0
for k in range(4):                                     # run y[n] = x[n] + 0.5 y[n-1] with an impulse
    prev = (1.0 if k == 0 else 0.0) + 0.5 * prev
    hh.append(prev)
key(n, hh[3])
n = q("12-bit ADC")
nb, NS = 12, 1 << 16
xq = (2 ** (nb - 1) - 0.5) * np.sin(2 * math.pi * 1031 * np.arange(NS) / NS)
qe = np.round(xq + 0.5) - 0.5 - xq                     # mid-rise quantizer, full-scale sine
snr_sim = 10 * math.log10(np.mean(xq ** 2) / np.mean(qe ** 2))
v.assert_true(f"Q{n}: a simulated 12-bit quantizer is within 0.05 dB of 6.02N + 1.76",
              abs(snr_sim - (6.02 * nb + 1.76)) < 0.05, f"simulated {snr_sim:.3f} dB")
mcnum(n, 6.02 * nb + 1.76, [20 * math.log10(2 ** nb), 10 * math.log10(2 ** nb), 6.02 * nb - 1.76])
n = q("$h[n] = \\{1, -1, 2\\}$")
yconv = np.convolve([1, 2, 3], [1, -1, 2])
key(n, yconv[2])
v.assert_true(f"Q{n}: forgetting to reverse h gives 5", np.dot([1, 2, 3], [1, -1, 2]) == 5)
n = q("square wave with 50% duty cycle")
tt = np.linspace(0, 1, 200_001)
sq = np.where(tt < 0.5, 1.0, -1.0)
b1 = 2 * integrate.simpson(sq * np.sin(2 * math.pi * tt), x=tt)
uni = np.where(tt < 0.5, 1.0, 0.0)                      # a 0-to-1 V square wave
mcnum(n, b1, [1.0, 2 * integrate.simpson(uni * np.sin(2 * math.pi * tt), x=tt), b1 / math.sqrt(2)])

# ================================================================= electronics
key(q("A silicon diode in series"), (5 - 0.7) / 1e3 * 1e3)
n = q("A 5.1 V Zener")
i_r, i_l = (12 - 5.1) / 470, 5.1 / 1e3
mcnum(n, (i_r - i_l) * 1e3, [i_r * 1e3, i_l * 1e3, (i_r + i_l) * 1e3])
n = q("An npn transistor")
ib = (5 - 0.7) / 100e3
vce = 10 - 100 * ib * 1e3
v.assert_true(f"Q{n}: the transistor is active (V_CE > 0.2 V)", vce > 0.2)
key(n, vce)
n = q("An NMOS transistor in saturation has")
kp, vgs, vth = 2e-3, 1.3, 0.5
idq = lambda vg: 0.5 * kp * (vg - vth) ** 2  # noqa: E731
mcnum(n, idq(vgs) * 1e3, [kp * (vgs - vth) ** 2 * 1e3, 0.5 * kp * vgs ** 2 * 1e3, 0.5 * kp * (vgs - vth) * 1e3])
n = q("The NMOS transistor of the previous question")
gm = (idq(vgs + 1e-6) - idq(vgs - 1e-6)) / 2e-6
vds = 5 - idq(vgs) * 5e3
v.assert_true(f"Q{n}: V_DS exceeds the overdrive, so the transistor is saturated", vds > vgs - vth)
key(n, -gm * 5e3)
v.check(f"FE.{n:03d}.VDS", vds)
v.check(f"FE.{n:03d}.gm", gm * 1e3)
n = q("full-wave rectifier")
dt = 1e-6
tgrid = np.arange(0, 0.2, dt)
vin = 12 * np.abs(np.sin(2 * math.pi * 60 * tgrid))
trace = np.empty_like(tgrid)
vc = 12.0
for k, vi in enumerate(vin):                          # ideal diodes: the capacitor follows the input when it is higher
    vc = max(vi, vc - 0.1 / 1000e-6 * dt)
    trace[k] = vc
ripple_sim = trace[tgrid > 0.1].max() - trace[tgrid > 0.1].min()
est = 0.1 / (2 * 60 * 1000e-6)
v.assert_true(f"Q{n}: the simulated ripple is 10-15% below the I/(2fC) estimate", 0.85 * est < ripple_sim < 0.9 * est,
              f"simulated {ripple_sim:.4f} V")
v.check(f"FE.{n:03d}.sim", ripple_sim)
th_on = math.degrees(math.asin((12 - ripple_sim) / 12))
v.assert_true(f"Q{n}: the diodes start conducting about 20° before each peak", 18 < 90 - th_on < 23, f"{90 - th_on:.1f}°")
mcnum(n, est, [0.1 / (60 * 1000e-6), est / (2 * math.sqrt(3)), 0.1 / (2 * 2 * math.pi * 60 * 1000e-6)])
n = q("gain-bandwidth product")
A0, fa, beta = 1e5, 100.0, 1 / 20                      # single-pole op-amp with GBW = 10 MHz
fq = np.logspace(3, 8, 500_001)
Aol = A0 / (1 + 1j * fq / fa)
Acl = np.abs(Aol / (1 + beta * Aol))
key(n, fq[np.argmax(Acl < Acl[0] / math.sqrt(2))] / 1e3)
n = q("Its CMRR")
mcnum(n, 20 * math.log10(1000 / 0.1), [10 * math.log10(1000 / 0.1), 20 * math.log10(1000), 20 * math.log10(0.1 / 1000)])
n = q("strain gauge")
dR = 2.0 * 500e-6 * 120
vb = 5 * ((120 + dR) / (240 + dR) - 120 / 240) * 1e3
mcnum(n, vb, [5 * dR / 120 / 2 * 1e3, 5 * dR / 120 * 1e3, 5 * 500e-6 / 4 * 1e3])
v.check(f"FE.{n:03d}.dR", dR)

# ================================================================= power systems
vph = 480 / math.sqrt(3)
phasors = [vph * np.exp(1j * a) for a in (0, -2 * math.pi / 3, 2 * math.pi / 3)]
n = q("Find the total power, in kW")
key(n, sum((vv * np.conj(vv / 10)).real for vv in phasors) / 1e3)
v.check(f"FE.{n:03d}.Vph", abs(phasors[1]))
n = q("Its line current, in A")
mcnum(n, abs(phasors[0] / 10), [480 / 10, vph / 10 / math.sqrt(3), math.sqrt(3) * 480 / 10])
key(q("single-phase 50 kVA"), 50e3 / 240)
n = q("the base impedance")
mcnum(n, 138e3 ** 2 / 100e6, [138 / 100, 100e6 / 138e3 ** 2, (138e3 / math.sqrt(3)) ** 2 / 100e6])
n = q("4-pole, 60 Hz induction motor")
ns = 60 * 60 / (4 / 2)                                 # field rev/s times 60, with pole pairs
key(n, (ns - 1746) / ns * 100)
n = q("synchronous speed of a 6-pole")
mcnum(n, 60 * 50 / 3, [60 * 50 / 6, 120 * 50 / 3, 60 * 50 / 3 * (1 - 0.04)])
n = q("Capacitors supplying 18 kvar")
S0 = 40 + 1j * 40 * math.tan(math.acos(0.8))
S1 = S0 - 18j
mcnum(n, S1.real / abs(S1), [40 / abs(40 + 18j), 40 / abs(S0 + 18j), S0.real / abs(S0)])
v.check(f"FE.{n:03d}.Q", S0.imag)
n = q("The line loss, in kW")
Iph = [np.conj((10e6 / 3) * (1 + 1j * math.tan(math.acos(0.9))) / (33e3 / math.sqrt(3) * np.exp(1j * a)))
       for a in (0, -2 * math.pi / 3, 2 * math.pi / 3)]
loss = sum(abs(ii) ** 2 * 2 for ii in Iph) / 1e3      # phase by phase
mcnum(n, loss, [loss / 3, 3 * (10e6 / (33e3 * 0.9)) ** 2 * 2 / 1e3, 3 * (10e6 / (math.sqrt(3) * 33e3)) ** 2 * 2 / 1e3])
v.check(f"FE.{n:03d}.I", abs(Iph[0]))
n = q("ideal buck converter")


def pwm_avg(d, vin_=12.0, steps=1_000_000):
    k = np.arange(steps) / steps
    return np.mean(np.where(k < d, vin_, 0.0))


d_buck = optimize.brentq(lambda d: pwm_avg(d) - 3.3, 0.01, 0.99, xtol=1e-9)
mcnum(n, d_buck, [12 / 3.3, 1 - d_buck, optimize.brentq(lambda d: d / (1 - d) - 3.3 / 12, 0.01, 0.99)])

# ================================================================= electromagnetics
n = q("long straight wire")
mu0 = 4 * math.pi * 1e-7
bs, _ = integrate.quad(lambda z: 0.05 / (0.05 ** 2 + z ** 2) ** 1.5, -np.inf, np.inf)   # Biot-Savart along the wire
key(n, mu0 * 10 / (4 * math.pi) * bs * 1e6)
n = q("coaxial cable")
mcnum(n, 3.00e8 / math.sqrt(2.25) / 1e9, [3.00e8 / 1e9, 3.00e8 / 2.25 / 1e9, 3.00e8 * math.sqrt(2.25) / 1e9])
n = q("terminated in 25 Ω")
gam = (25 - 50) / (25 + 50)
bz = np.linspace(0, 2 * math.pi, 100_001)
vz = np.abs(np.exp(1j * bz) + gam * np.exp(-1j * bz))  # standing wave along one wavelength
key(n, vz.max() / vz.min())
v.check(f"FE.{n:03d}.G", abs(gam))


def zin(zl, z0, bl):
    tn = math.tan(bl)
    return z0 * (zl + 1j * z0 * tn) / (z0 + 1j * zl * tn)


n = q("quarter-wave section")
mcnum(n, abs(zin(100, 50, math.pi / 2 - 1e-9)), [abs(zin(100, 50, math.pi)), 50.0, 100 ** 2 / 50])

# ================================================================= control systems
n = q("$G(s) = 5/(s^2 + 3s + 10)$")
tt, yy = signal.step(signal.lti([5], [1, 3, 10]), T=np.linspace(0, 30, 30_001))
fv_imp = signal.impulse(signal.lti([5], [1, 3, 10]), T=np.linspace(0, 30, 30_001))[1][-1]
mcnum(n, yy[-1], [5.0, fv_imp, 5 / 3])
n = q("steady-state error to a unit ramp")
tt = np.linspace(0, 40, 400_001)
_, yr, _ = signal.lsim(signal.lti([20], [1, 4, 20]), tt, tt)
mcnum(n, tt[-1] - yr[-1], [0.0, 20 / 4, 1 / 20])
n = q("has all its roots in the left half-plane")


def routh_stable(K):
    a3, a2, a1, a0 = 1, 2, 3, K
    return a2 > 0 and (a2 * a1 - a3 * a0) / a2 > 0 and a0 > 0


ks = np.linspace(0.001, 20, 200_000)
v.assert_true(f"Q{n}: roots change half-plane at K = 6",
              max(np.roots([1, 2, 3, 5.99]).real) < 0 < max(np.roots([1, 2, 3, 6.01]).real))
key(n, max(k for k in ks if routh_stable(k)))
n = q("The phase margin, in degrees")
mcnum(n, 180 + (-135), [135, -180 - (-135), -135 + 360])
n = q("a sensor of gain 1.2")
ss_, R_ = sp.symbols("ss_ R_")
Yb, Eb = sp.symbols("Yb Eb")
solb = sp.solve([sp.Eq(Eb, R_ - sp.Rational(6, 5) * Yb), sp.Eq(Yb, 5 / (ss_ + 2) * Eb)], [Yb, Eb], dict=True)[0]
T0 = float((solb[Yb] / R_).subs(ss_, 0))
mcnum(n, T0, [2.5 / (1 + 2.5), 2.5, 3 / (1 + 3)])
n = q("percent overshoot")
tt, yy = signal.step(signal.lti([1], [1, 1, 1]), T=np.linspace(0, 20, 200_001))   # zeta = 0.5, wn = 1
key(n, (yy.max() - 1) * 100)
n = q("$s^2 + 4s + 25$")
tt, yy = signal.step(signal.lti([25], [1, 4, 25]), T=np.linspace(0, 3, 300_001))
key(n, tt[np.argmax(yy)])

# ================================================================= communications
key(q("received power, in dBm"), 10 * math.log10(1e-3 * 10 ** 2 * 10 * 10 ** 0.3 / 10 ** 11) + 30)
key(q("Carson's-rule"), 2 * (75 + 15))
key(q("Shannon capacity"), 1e6 * math.log2(1 + 15) / 1e6)
n = q("16-QAM")
mcnum(n, 10 * math.log2(16), [10 * 16, 10 * math.log2(math.sqrt(16)), 10 / math.log2(16)])
n = q("thermal noise power")
kTB = 10 * math.log10(1.380649e-23 * 290 * 1e6 / 1e-3)
v.assert_true(f"Q{n}: kTB agrees with -174 dBm/Hz + 60 dB to 0.05 dB", abs(kTB - (-174 + 60)) < 0.05)
mcnum(n, kTB, [-174.0, -174 + 10 * math.log10(1e3), -174 - 60])

# ================================================================= computer networks
concept(q("reliable, ordered delivery"), "TCP")
key(q("1500-byte frame"), 1500 * 8 / 100e6 * 1e6)
concept(q("message authentication code"), "integrity and authenticity of the data")
n = q("/26 subnet")
mcnum(n, len(list(ipaddress.ip_network("10.0.0.0/26").hosts())),
      [ipaddress.ip_network("10.0.0.0/26").num_addresses, len(list(ipaddress.ip_network("10.0.0.0/27").hosts())),
       len(list(ipaddress.ip_network("10.0.0.0/25").hosts()))])

# ================================================================= digital systems
n = q("4-bit binary counter")
msb = [(c >> 3) & 1 for c in range(64)]
key(n, 1e6 * sum(1 for i in range(1, 64) if msb[i] and not msb[i - 1]) / 64 / 1e3)
n = q("any Boolean function on its own")
nand = lambda a, b: 1 - (a & b)  # noqa: E731
v.assert_true(f"Q{n}: NAND builds NOT, AND and OR",
              all(nand(a, a) == 1 - a and nand(nand(a, b), nand(a, b)) == (a & b) and nand(nand(a, a), nand(b, b)) == (a | b)
                  for a in (0, 1) for b in (0, 1)))
concept(n, "NAND")
n = q("0.12 ns clock-to-Q")
mcnum(n, 1e3 / (0.12 + 3.1 + 0.18), [1e3 / 3.1, 1e3 / (0.12 + 3.1 - 0.18), 1e3 / (3.1 + 0.18)])
n = q("Gray code")
gray = ["0", "1"]
for _ in range(3):                                     # build the reflected Gray sequence
    gray = ["0" + g for g in gray] + ["1" + g for g in reversed(gray)]
key(n, int(gray[0b1011], 2))
n = q("11110110")
raw = 0b11110110
mcnum(n, int.from_bytes(bytes([raw]), "big", signed=True), [raw, -(raw & 0x7F), -((~raw) & 0xFF)])
n = q("Moore machine detects")


def minimize(states, inputs, delta, out):
    """Partition refinement; out(s) is a state's output (Moore) or a tuple of transition outputs (Mealy)."""
    part = {s_: out(s_) for s_ in states}
    while True:
        new = {s_: (part[s_],) + tuple(part[delta(s_, x)] for x in inputs) for s_ in states}
        if len(set(new.values())) == len(set(part.values())):
            return len(set(part.values()))
        part = new


def reach(start, inputs, delta):
    seen, todo = {start}, [start]
    while todo:
        s_ = todo.pop()
        for x in inputs:
            nx = delta(s_, x)
            if nx not in seen:
                seen.add(nx)
                todo.append(nx)
    return seen


hist3 = lambda s_, x: (s_ + x)[-3:]  # noqa: E731
moore = minimize(reach("", "01", hist3), "01", hist3, lambda s_: s_ == "101")
hist2 = lambda s_, x: (s_ + x)[-2:]  # noqa: E731
mealy = minimize(reach("", "01", hist2), "01", hist2, lambda s_: tuple((s_ + x)[-3:] == "101" for x in "01"))
mcnum(n, moore, [mealy, 2 ** 3, math.ceil(math.log2(moore))])
n = q("register-to-register path")
key(n, 2 - 0.2 - 1.4 - 0.15)
n = q("\\Sigma m(1, 3, 5, 7, 9, 11)")
ones, dc = {1, 3, 5, 7, 9, 11}, {13, 15}
bit = lambda m, k: (m >> (3 - k)) & 1  # noqa: E731  (k = 0 is A, the most significant bit)
EXPR = {r"$D$": lambda m: bit(m, 3),
        r"$\bar AD + \bar BD$": lambda m: (not bit(m, 0) and bit(m, 3)) or (not bit(m, 1) and bit(m, 3)),
        r"$\bar AD$": lambda m: not bit(m, 0) and bit(m, 3),
        r"$\bar BD$": lambda m: not bit(m, 1) and bit(m, 3)}
fails = {t_: {m for m in range(16) if m not in dc and bool(fn(m)) != (m in ones)} for t_, fn in EXPR.items()}
cares = [m for m in range(16) if m not in dc]
v.assert_true(f"Q{n}: D covers F, using both don't-cares", not fails["$D$"])
v.assert_true(f"Q{n}: F is not constant on its care set, so one literal is minimal",
              any(m in ones for m in cares) and any(m not in ones for m in cares))
v.assert_true(f"Q{n}: the two-term cover is valid (and has four literals)", not fails[r"$\bar AD + \bar BD$"])
v.assert_true(f"Q{n}: the other options miss the minterms the solution names",
              fails[r"$\bar AD$"] == {9, 11} and fails[r"$\bar BD$"] == {5, 7})
v.assert_true(f"Q{n}: the options are exactly these four expressions", set(QS[n][1].values()) == set(EXPR))
concept(n, "$D$")

# ================================================================= computer systems
n = q("80% of a program")
t_serial, t_par = 200, math.ceil(800 / 8)             # 1000 unit tasks, 200 of them serial, on 8 cores
key(n, 1000 / (t_serial + t_par))
n = q("average memory access time")
trace_t = [1 + (60 if k % 20 == 0 else 0) for k in range(10_000)]   # exactly 5% misses
mcnum(n, sum(trace_t) / len(trace_t), [1 + 60, 0.05 * 60, 1 + 0.05])
n = q("instructions at a CPI of 1.5")
mcnum(n, 2e9 * 1.5 / 3e9, [2e9 / 3e9, 2e9 / (1.5 * 3e9), 1.5 * 3e9 / 2e9])
n = q("32 KB direct-mapped")
index_of = lambda a: (a // 64) % 512  # noqa: E731
offset_of = lambda a: a % 64  # noqa: E731
base = 0x12345678
tag_bits = sum(1 for b in range(32)
               if index_of(base ^ (1 << b)) == index_of(base) and offset_of(base ^ (1 << b)) == offset_of(base))
key(n, tag_bits)
n = q("5-stage pipeline")
finish = [i + 5 for i in range(100)]                  # instruction i (from 0) leaves the last stage at cycle i + 5
mcnum(n, 5 * 100 / finish[-1], [5.0, finish[-1] / 100, 5 * 100 / (100 + 5)])

# ================================================================= software engineering
items = list(range(1_000_000))


def comparisons(target):
    lo, hi, c = 0, len(items) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if items[mid] == target:
            return c
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return c


key(q("binary search needs"), max(comparisons(x_) for x_ in (0, 999_999, -1, 1_000_000, 524_287, 1)))
concept(q("constant average-time lookup"), "hash table")
n = q("How many times does the loop body run")
i_, runs = 3, 0
while i_ < 30:
    runs += 1
    i_ += 4
key(n, runs)
concept(q("interaction between modules"), "integration testing")

# ================================================================= structure
numbers = sorted(QS)
v.assert_true("110 questions, numbered 1 to 110", numbers == list(range(1, 111)))
mcq = {n_ for n_, (_, o) in QS.items() if o}
v.assert_true("every multiple-choice question has four options and an answer letter",
              all(len(QS[n_][1]) == 4 for n_ in mcq) and mcq == set(letters))
v.assert_true("every question has a solution", set(SOLS) == set(range(1, 111)))
v.assert_true("more multiple-choice than numeric-entry questions", len(mcq) > 110 - len(mcq))
for n_ in sorted(mcq):
    wrong = [L for L in "ABCD" if L != letters[n_]]
    text = SOLS[n_]
    v.assert_true(f"Q{n_}: the solution names the mistake behind every wrong option",
                  "**Wrong options:**" in text and all(f"({L}) {QS[n_][1][L]} " in text for L in wrong)
                  and f"Answer: ({letters[n_]}) {QS[n_][1][letters[n_]]}." in text)
seq = [letters[n_] for n_ in sorted(mcq)]
cnt = {x: seq.count(x) for x in "ABCD"}
v.assert_true("answer letters are balanced (each within 3 of a quarter)",
              all(abs(c - len(seq) / 4) <= 3 for c in cnt.values()), str(cnt))
v.assert_true("no answer letter repeats four times in a row", all(len(set(seq[i:i + 4])) > 1 for i in range(len(seq) - 3)))
v.assert_true("no period-2, -3 or -4 letter pattern runs for 8 answers",
              not any(all(seq[j] == seq[j + p] for j in range(i, i + 8)) for p in (2, 3, 4) for i in range(len(seq) - 8 - p + 1)))
types = ["M" if n_ in mcq else "N" for n_ in numbers]
alt = best = 1
for i in range(1, len(types)):
    alt = alt + 1 if types[i] != types[i - 1] else 1
    best = max(best, alt)
v.assert_true("question types do not alternate for more than 5 questions in a row", best <= 5, f"longest alternation {best}")

spec = yaml.safe_load((ROOT / "tools" / "data" / "fe_spec.yml").read_text(encoding="utf-8"))["areas"]
heads = [(m.group(1), int(m.group(2)), int(m.group(3)))
         for m in re.finditer(r"^### (.+?) \(questions (\d+)–(\d+)\)$", readme, re.M)]
v.assert_true("one README heading per NCEES area, in order", len(heads) == len(spec))
v.assert_true("the area headings tile questions 1 to 110",
              heads[0][1] == 1 and heads[-1][2] == 110 and all(heads[i][2] + 1 == heads[i + 1][1] for i in range(len(heads) - 1)))
ok_names, ok_counts = True, True
for (name, a, b), area in zip(heads, spec.values()):
    lo, hi = (int(x) for x in area["questions"].replace("–", "-").split("-"))
    ok_names &= area["name"].lower().startswith(name.lower())
    ok_counts &= lo <= b - a + 1 <= hi
v.assert_true("README area names match tools/data/fe_spec.yml", ok_names)
v.assert_true("every area's question count lies inside its NCEES range (tools/data/fe_spec.yml)", ok_counts)
table = re.findall(r"^\| ([A-Z][^|]+?) \| (\d+)–(\d+) \| (\d+) \|$", sol_text, re.M)
v.assert_true("the solutions' scoring table matches the README headings",
              [(t_[0], int(t_[1]), int(t_[2])) for t_ in table] == heads
              and all(int(t_[3]) == int(t_[2]) - int(t_[1]) + 1 for t_ in table))

sys.exit(v.finish())
