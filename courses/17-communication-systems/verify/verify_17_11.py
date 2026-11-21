#!/usr/bin/env python3
"""Verify chapter 17-11 (MIMO and beamforming): text, examples, problems and lab answers.

Routes:
- combining statistics in closed form (Erlang, products of exponential CDFs, harmonic sums) and by Monte Carlo;
- Alamouti by encoding and decoding exact symbols, and its BER by simulation against the MRC formula at half SNR;
- array factors by direct summation of element phasors, beamwidths by root finding, grating lobes by search;
- capacities by SVD and by log-determinant, water-filling by a general optimizer, ergodic capacity by the
  closed form (SISO), by integrating the 2 x 2 Wishart eigenvalue density, and by Monte Carlo;
- ZF/MMSE SINRs by matrix algebra and by simulation;
- the TS 38.306 rate formula written out here (R-289).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import mimo as mm  # noqa: E402

CH = ROOT / "chapters" / "17-11-mimo-and-beamforming.md"
v = Verifier.from_files("17-11", CH, ROOT / "solutions" / "17-11-solutions.md", LAB / "README.md")
rng = np.random.default_rng(17110)


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def cr(*shape):
    return (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / math.sqrt(2)


def af_direct(n, dl, theta, steer=0.0):
    """|sum_k w_k a_k(theta)| with w = a(steer)/n, summed element by element."""
    k = np.arange(n)
    ph = 2 * np.pi * dl * k * (math.sin(math.radians(theta)) - math.sin(math.radians(steer)))
    return abs(np.sum(np.exp(1j * ph))) / n


def af_signed(n, dl, theta):
    """Real-valued (signed) broadside array factor, so its nulls are sign changes."""
    psi = 2 * np.pi * dl * math.sin(math.radians(theta))
    return math.sin(n * psi / 2) / (n * math.sin(psi / 2))


def hpbw(n, dl, steer=0.0):
    up = optimize.brentq(lambda t: af_direct(n, dl, steer + t, steer) ** 2 - 0.5, 1e-6, 60)
    dn = optimize.brentq(lambda t: af_direct(n, dl, steer - t, steer) ** 2 - 0.5, 1e-6, 60)
    return up + dn


def ber_mrc(g, L):
    """Closed form, written out independently of the lab (Proakis)."""
    mu = math.sqrt(g / (1 + g))
    return ((1 - mu) / 2) ** L * sum(math.comb(L - 1 + k, k) * ((1 + mu) / 2) ** k for k in range(L))


def rate(layers, qm, nrb, mu, oh):
    """TS 38.306 clause 4.1.2 (R-289), f = 1."""
    return 1e-6 * layers * qm * (948 / 1024) * (nrb * 12 / (1e-3 / (14 * 2**mu))) * (1 - oh)


# ------------------------------------------------------------------ text
v.check("Txt 17-11.a", 1 + 1 / 2)
v.check("Txt 17-11.b", db(2))
v.check("Txt 17-11.c", 948 / 1024)
h = cr(2, 400_000)
v.assert_true("Monte Carlo: SC mean gain 1.5 and MRC mean gain 2 for two branches", abs(np.mean(np.max(abs(h) ** 2, axis=0)) - 1.5) < 0.01 and abs(np.mean(np.sum(abs(h) ** 2, axis=0)) - 2) < 0.01)
w = cr(4)
hh = cr(4)
v.assert_true("Cauchy-Schwarz: any weight vector gives SNR <= ||h||^2, with equality for w = h", abs(np.vdot(w, hh)) ** 2 / np.vdot(w, w).real <= np.vdot(hh, hh).real + 1e-12 and abs(abs(np.vdot(hh, hh)) ** 2 / np.vdot(hh, hh).real - np.vdot(hh, hh).real) < 1e-12)
v.assert_true("array factor: lab closed form equals direct element sum (N = 8, several angles)", all(abs(mm.array_factor(8, 0.5, t, 20)[0] - af_direct(8, 0.5, t, 20)) < 1e-12 for t in (-50, -10, 5, 20, 33, 70)))
v.assert_true("HPBW ~ 101.5 deg / N: 0.886 * 2 rad", abs(math.degrees(0.886 * 2) - 101.5) < 0.05)
v.assert_true("half-wavelength spacing: 4.28 cm at 3.5 GHz, 5.35 mm at 28 GHz", abs(299792458 / 3.5e9 / 2 - 0.0428) < 5e-5 and abs(299792458 / 28e9 / 2 - 0.00535) < 5e-6)
Hr = cr(3, 2)
v.assert_true("capacity: log det form equals the SVD sum (random 3 x 2)", abs(mm.capacity_equal_power(Hr, 30) - mm.capacity_svd(Hr, 30)) < 1e-10)
U, S, Vh = np.linalg.svd(Hr)
v.assert_true("SVD precoding diagonalizes the channel: U^H H V = Sigma", np.allclose(U.conj().T @ Hr @ Vh.conj().T, np.vstack([np.diag(S), np.zeros((1, 2))]), atol=1e-12))
zf22 = [mm.zf_sinr(cr(2, 2), 2.0)[0] for _ in range(40_000)]
zf32 = [mm.zf_sinr(cr(3, 2), 2.0)[0] for _ in range(40_000)]
v.assert_true("Monte Carlo ZF SNR means: 1.0 (2 x 2) and 2.0 (3 x 2) times rho/Nt", abs(np.mean(zf22) - 1.0) < 0.03 and abs(np.mean(zf32) - 2.0) < 0.05)
M = np.array([1, 4, 64, 256])
spreads = [np.std(np.sum(abs(cr(m, 20_000)) ** 2, axis=0) / m) for m in M]
v.assert_true("channel hardening: spread of ||h||^2/M is 1/sqrt(M) within 5%", all(abs(s * math.sqrt(m) - 1) < 0.05 for s, m in zip(spreads, M)))

# ------------------------------------------------------------------ examples
v.check("Ex 17-11.1a", db(10 * 2))
v.check("Ex 17-11.1b", db(10 * 4))
v.check("Ex 17-11.1c", db(10 * 1.5))
v.check("Ex 17-11.1d", db(10 * (1 + 1 / 2 + 1 / 3 + 1 / 4)))
x = 10**-0.5
v.check("Ex 17-11.1e", 1 - math.exp(-x))
v.check("Ex 17-11.1f", (1 - math.exp(-x)) ** 2)
v.check("Ex 17-11.1g", 1 - math.exp(-x) * (1 + x))
erlang4, _ = integrate.quad(lambda t: t**3 * math.exp(-t) / 6, 0, x)
v.check("Ex 17-11.1h", erlang4)
e4 = rng.exponential(1.0, (4, 400_000))
v.assert_true("Example 1: Monte Carlo SC4 outage 0.0054 and MRC2 0.0406", abs(np.mean(e4.max(axis=0) < x) / 0.00540 - 1) < 0.05 and abs(np.mean(e4[:2].sum(axis=0) < x) / 0.0406 - 1) < 0.03)
h1, h2, s1, s2 = 0.8 + 0.6j, -0.3 + 0.4j, 1 + 1j, 1 - 1j
r1 = (h1 * s1 + h2 * s2) / math.sqrt(2)
r2 = (-h1 * np.conj(s2) + h2 * np.conj(s1)) / math.sqrt(2)
t1 = np.conj(h1) * r1 + h2 * np.conj(r2)
t2 = np.conj(h2) * r1 - h1 * np.conj(r2)
g = abs(h1) ** 2 + abs(h2) ** 2
v.check("Ex 17-11.2a", g)
v.assert_true("Example 2: Alamouti recovers s1 and s2 exactly (written out here and by the lab)", abs(t1 / (g / math.sqrt(2)) - s1) < 1e-12 and abs(t2 / (g / math.sqrt(2)) - s2) < 1e-12 and np.allclose(mm.alamouti_decode(*(np.einsum("sa,a->s", mm.alamouti_encode(np.array([s1, s2]))[0], np.array([h1, h2]))), h1, h2), [g / math.sqrt(2) * s1, g / math.sqrt(2) * s2]))
v.check("Ex 17-11.2b", ber_mrc(un(15), 2))
v.check("Ex 17-11.2c", ber_mrc(un(15) / 2, 2))
sim_ala = mm.simulate_alamouti(15, 600_000, rng)
v.assert_true(f"Example 2: Alamouti simulated {sim_ala:.2e} at 15 dB vs {ber_mrc(un(15) / 2, 2):.2e}", abs(sim_ala / ber_mrc(un(15) / 2, 2) - 1) < 0.15)
v.check("Ex 17-11.3a", db(8))
v.check("Ex 17-11.3b", hpbw(8, 0.5))
v.check("Ex 17-11.3c", hpbw(8, 0.5, 30))
null = optimize.brentq(lambda t: af_signed(8, 0.5, t), 5, 20)
v.check("Ex 17-11.3d", null)
v.check("Ex 17-11.3e", 1 / (1 + math.sin(math.radians(60))))
v.assert_true("Example 3: rule-of-thumb beamwidths 12.69 and 14.65 deg; lab agrees with the direct sum", abs(math.degrees(0.886 * 2 / 8) - 12.69) < 0.005 and abs(math.degrees(0.886 * 2 / 8 / math.cos(math.radians(30))) - 14.65) < 0.005 and abs(mm.hpbw_deg(8, 0.5) - hpbw(8, 0.5)) < 1e-6)
H4 = np.array([[1, 0.5], [0.2j, 0.8]])
s4 = np.linalg.svd(H4, compute_uv=False)
v.check("Ex 17-11.4a", s4[0])
v.check("Ex 17-11.4b", s4[1])
c_eq = float(np.real(np.log2(np.linalg.det(np.eye(2) + 50 * H4 @ H4.conj().T))))
v.check("Ex 17-11.4c", c_eq)
Ginv = np.linalg.inv(H4.conj().T @ H4)
zf = 50 / np.real(np.diag(Ginv))
v.check("Ex 17-11.4d", db(zf[0]))
v.check("Ex 17-11.4e", db(zf[1]))
v.check("Ex 17-11.4f", np.sum(np.log2(1 + zf)))
v.check("Ex 17-11.4g", math.log2(101))
res = optimize.minimize(lambda p: -np.sum(np.log2(1 + s4**2 * p)), [50, 50], bounds=[(0, 100)] * 2, constraints=[{"type": "eq", "fun": lambda p: p.sum() - 100}], method="SLSQP", options={"ftol": 1e-14})
v.assert_true("Example 4: water-filling (SLSQP) adds 0.0004 b/s/Hz; condition number 1.85; diag of inverse 1.369 and 1.600", abs(-res.fun - c_eq - 0.0004) < 0.00005 and abs(s4[0] / s4[1] - 1.85) < 0.005 and abs(Ginv[0, 0].real - 1.369) < 5e-4 and abs(Ginv[1, 1].real - 1.6) < 1e-9)
v.assert_true("Example 4: MMSE SINRs slightly exceed ZF's", np.all(mm.mmse_sinr(H4, 100) > mm.zf_sinr(H4, 100)))
v.check("Ex 17-11.5a", math.log2(math.e) * math.exp(1 / 100) * special.exp1(1 / 100))
v.check("Ex 17-11.5b", 2 * integrate.quad(lambda lam: math.log2(1 + 50 * lam) * 0.5 * (1 + (1 - lam) ** 2) * math.exp(-lam), 0, np.inf, limit=200)[0])
Hm = cr(400_000, 4, 4)
c44 = np.mean(np.linalg.slogdet(np.eye(4) + 25 * Hm @ np.conj(np.transpose(Hm, (0, 2, 1))))[1]) / math.log(2)
v.check("Ex 17-11.5c", c44)
H2m = cr(400_000, 2, 2)
c22mc = np.mean(np.linalg.slogdet(np.eye(2) + 50 * H2m @ np.conj(np.transpose(H2m, (0, 2, 1))))[1]) / math.log(2)
v.assert_true("Example 5: Monte Carlo 2 x 2 matches the eigenvalue integral; SISO closed form matches Monte Carlo", abs(c22mc - mm.ergodic_2x2(100)) < 0.01 and abs(np.mean(np.log2(1 + 100 * rng.exponential(1.0, 400_000))) - mm.ergodic_siso(100)) < 0.01)
v.assert_true("Example 5: Wishart marginal integrates to 1 and has mean 2 (= Nt for unit-variance entries)", abs(integrate.quad(lambda l: 0.5 * (1 + (1 - l) ** 2) * math.exp(-l), 0, np.inf)[0] - 1) < 1e-12 and abs(integrate.quad(lambda l: l * 0.5 * (1 + (1 - l) ** 2) * math.exp(-l), 0, np.inf)[0] - 2) < 1e-12)
v.check("Ex 17-11.6a", rate(4, 8, 273, 1, 0.14))
v.check("Ex 17-11.6b", rate(2, 8, 273, 1, 0.14))
v.check("Ex 17-11.6c", rate(4, 8, 273, 1, 0.14) / 100)
v.assert_true("Example 6: lab formula agrees; 5.84 b/s/Hz per layer", abs(mm.nr_max_rate_mbps(4, 8, 273, 1, 0.14) - rate(4, 8, 273, 1, 0.14)) < 1e-9 and abs(rate(4, 8, 273, 1, 0.14) / 400 - 5.84) < 0.005)

# ------------------------------------------------------------------ problems
v.check("17-11.2a", (1 + 0.5) ** 2 / 2)
v.check("17-11.2b", 1 + 0.25)
v.check("17-11.3a", sum(1 / k for k in range(1, 4)))
v.check("17-11.3b", sum(1 / k for k in range(1, 9)))
v.check("17-11.3c", db(8 / sum(1 / k for k in range(1, 9))))
v.check("17-11.4a", 1 - math.exp(-0.1) * (1 + 0.1 + 0.005))
v.check("17-11.4b", 0.1**3 / 6)
v.check("17-11.4c", (1 - math.exp(-0.1)) ** 3)
for key, L in (("17-11.5a", 1), ("17-11.5b", 2), ("17-11.5c", 4)):
    v.check(key, optimize.brentq(lambda d: ber_mrc(un(d), L) - 1e-6, -10, 80, xtol=1e-12))
v.check("17-11.6a", db(16))
v.check("17-11.6b", hpbw(16, 0.5))
v.check("17-11.6c", optimize.brentq(lambda t: af_signed(16, 0.5, t), 3, 10))
v.check("17-11.6d", 1 / (1 + math.sin(math.radians(45))))
v.check("17-11.7a", 10 ** ((db(64) + db(64)) / 20))
H8 = np.ones((2, 2))
s8 = np.linalg.svd(H8, compute_uv=False)
v.check("17-11.8a", s8[0])
v.check("17-11.8b", s8[1])
v.check("17-11.8c", math.log2(1 + 50 * s8[0] ** 2))
v.check("17-11.8d", 2 * math.log2(1 + 50))
v.check("17-11.9a", math.log2(1.5) + math.log2(1 + 0.5 * 0.09))
res9 = optimize.minimize(lambda p: -(math.log2(1 + p[0]) + math.log2(1 + 0.09 * p[1])), [0.5, 0.5], bounds=[(0, 1)] * 2, constraints=[{"type": "eq", "fun": lambda p: p.sum() - 1}], method="SLSQP", options={"ftol": 1e-14})
v.check("17-11.9b", -res9.fun)
H10 = np.array([[1, 0.9], [0.9, 1.0]])
s10 = np.linalg.svd(H10, compute_uv=False)
z10 = 50 / np.real(np.diag(np.linalg.inv(H10.T @ H10)))
v.check("17-11.10a", s10[0])
v.check("17-11.10b", s10[1])
v.check("17-11.10c", s10[0] / s10[1])
v.check("17-11.10d", db(z10[0]))
v.check("17-11.10e", np.sum(np.log2(1 + z10)))
v.check("17-11.10f", math.log2(1 + 50 * s10[0] ** 2) + math.log2(1 + 50 * s10[1] ** 2))
v.check("17-11.10g", db(50 * np.sum(H10[:, 0] ** 2)))
v.assert_true("Problem 10: diagonal of (H^T H)^-1 is 1.81/0.19^2 = 50.1", abs(np.linalg.inv(H10.T @ H10)[0, 0] - 1.81 / 0.19**2) < 1e-9)
e2x2 = lambda rho: 2 * integrate.quad(lambda lam: math.log2(1 + rho * lam / 2) * 0.5 * (1 + (1 - lam) ** 2) * math.exp(-lam), 0, np.inf, limit=200)[0]  # noqa: E731
siso = lambda rho: math.log2(math.e) * math.exp(1 / rho) * special.exp1(1 / rho)  # noqa: E731
v.check("17-11.11a", e2x2(10))
v.check("17-11.11b", e2x2(1000))
v.check("17-11.11c", e2x2(1000) - e2x2(100))
v.check("17-11.11d", siso(1000) - siso(100))
v.check("17-11.12a", rate(2, 8, 273, 1, 0.08))
v.check("17-11.12b", rate(2, 6, 264, 3, 0.18))
v.check("17-11.13a", 1 / math.sqrt(100))
v.check("17-11.14a", ber_mrc(100, 2))
v.check("17-11.14b", ber_mrc(50, 2))
v.check("17-11.14c", 20 + db(2))

# ------------------------------------------------------------------ lab
v.check("Lab 17-11.a", ber_mrc(10, 2))
v.check("Lab 17-11.b", ber_mrc(5, 2))
gl = [t for t in np.arange(-89.95, 90, 0.05) if t < 0 and af_direct(8, 1.0, t, 30) > 0.99]
v.check("Lab 17-11.c", float(np.mean(gl)))
H88 = cr(100_000, 8, 8)
v.check("Lab 17-11.d", np.mean(np.linalg.slogdet(np.eye(8) + 12.5 * H88 @ np.conj(np.transpose(H88, (0, 2, 1))))[1]) / math.log(2))
v.check("Lab 17-11.e", 1 / math.sqrt(256))
sims = {k: mm.simulate_combining(2, 10, k, 400_000, rng) for k in ("sc", "egc", "mrc")}
v.assert_true(f"Lab part 1: simulated SC > EGC > MRC at 10 dB ({sims}); MRC on its formula; SC about 2x MRC", sims["sc"] > sims["egc"] > sims["mrc"] and abs(sims["mrc"] / ber_mrc(10, 2) - 1) < 0.1 and 1.6 < sims["sc"] / sims["mrc"] < 2.2)

# MMSE SINRs (independent: explicit error covariance), half-power point of sinc
def _mmse(H, rho):
    E = np.linalg.inv(np.eye(H.shape[1]) + rho / H.shape[1] * H.conj().T @ H)
    return 1 / np.real(np.diag(E)) - 1


_H4 = np.array([[1, 0.5], [0.2j, 0.8]])
_m4 = _mmse(_H4, 100)
v.check("Ex 17-11.4h", db(_m4[0]))
v.check("Ex 17-11.4i", db(_m4[1]))
v.check("Ex 17-11.4j", float(np.sum(np.log2(1 + _m4))))
v.assert_true("lab mmse_sinr agrees", np.allclose(mm.mmse_sinr(_H4, 100), _m4))
_m10 = _mmse(np.array([[1, 0.9], [0.9, 1]]), 100)
v.check("17-11.10h", db(_m10[0]))
v.check("17-11.10i", float(np.sum(np.log2(1 + _m10))))
v.check("Txt 17-11.hp", optimize.brentq(lambda x: math.sin(x) / x - 1 / math.sqrt(2), 0.5, 2.5))

# derived figures quoted in Solutions 17-11.5, 17-11.2 and 17-11.9
from scipy.stats import norm as _nrm  # noqa: E402


def _req_db(L):
    return optimize.brentq(lambda d: mm.ber_bpsk_mrc(10 ** (d / 10), L) - 1e-6, 0, 80)


v.check("17-11.5x", _req_db(1) - _req_db(2))
v.check("17-11.5y", _req_db(2) - _req_db(4))
v.check("17-11.5z", db(_nrm.isf(1e-6) ** 2 / 2))
v.check("17-11.2x", db(1.25 / ((1 + 0.5) ** 2 / 2)))
v.check("17-11.9x", 100 * (math.log2(2) / (math.log2(1.5) + math.log2(1.045)) - 1))

sys.exit(v.finish())
