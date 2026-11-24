"""Lab 20-04: a low-dropout regulator in the illustrative T130 process.

Pass device (chapter 20-04, section 3.2): a PMOS described by 20-01's charge-based model with source at V_in and
bulk at V_in. In triode (dropout) the long-channel forward-reverse form I = I_spec[(q_s^2 + q_s) - (q_d^2 + q_d)] is
used and the width is then increased by 1 + V_DS/(E_sat L) for velocity saturation (E_sat = v_sat/mu). In
saturation the current is I_spec (q^2 + q)/(1 + lambda_c q) as in 20-01, and r_ds = V_A' L / I.

Loop (section 3.4): an error amplifier (transconductance g_ma, output resistance R_a, capacitance C_a) drives a
buffer of output conductance g_mb into the pass device's gate capacitance C_g; the divider feeds back beta of the
output; the output node has r_ds || R_L || R_div in parallel with C_L in series with its ESR:

    L(s) = A_EA beta g_mp Z_out(s) / [(1 + s/p_a)(1 + s/p_g)],  A_EA = g_ma R_a, p_a = 1/(R_a C_a), p_g = g_mb/C_g.

Supply rejection (section 3.5): if the gate carries a fraction k of the input ripple, the ripple injected at the
output is [g_mp (1 - k) + g_ds] v_in, so 1/PSRR(s) = [g_mp (1 - k) + g_ds] Z_out(s) / (1 + L(s)).
All quantities SI.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

K_B, Q_E = 1.380649e-23, 1.602176634e-19


def vt(temp: float = 300.0) -> float:
    return K_B * temp / Q_E


@dataclass
class PMOS:
    mu: float = 100e-4
    cox: float = 8.6e-3
    n: float = 1.3
    vth: float = 0.45
    vsat: float = 6e4
    va_per_l: float = 8e6
    length: float = 0.15e-6

    def ispec(self, w: float) -> float:
        return 2 * self.n * self.mu * self.cox * (w / self.length) * vt() ** 2

    @staticmethod
    def q_of(vp: float) -> float:
        return brentq(lambda q: 2 * q + math.log(q) - vp / vt(), 1e-40, 1e7, xtol=1e-40, rtol=1e-15)

    def i_triode_long(self, w: float, vsg: float, vsd: float) -> float:
        vp = (vsg - self.vth) / self.n
        qs, qd = self.q_of(vp), self.q_of(vp - vsd)
        return self.ispec(w) * ((qs * qs + qs) - (qd * qd + qd))

    def lam(self) -> float:
        return self.mu * vt() / (self.vsat * self.length)

    def i_sat(self, w: float, vsg: float) -> float:
        q = self.q_of((vsg - self.vth) / self.n)
        return self.ispec(w) * (q * q + q) / (1 + self.lam() * q)

    def e_sat(self) -> float:
        return self.vsat / self.mu


def size_pass_device(dev: PMOS, vin_min: float, v_dropout: float, i_max: float) -> dict:
    """Width for a dropout v_dropout at i_max with the gate pulled to ground (V_SG = vin_min)."""
    w_long = brentq(lambda w: dev.i_triode_long(w, vin_min, v_dropout) - i_max, 1e-7, 1.0, xtol=1e-13)
    corr = 1 + v_dropout / (dev.e_sat() * dev.length)
    w = w_long * corr
    return {"w_long": w_long, "vs_factor": corr, "w": w, "cgg": 2 / 3 * w * dev.length * dev.cox}


def operating_point(dev: PMOS, w: float, i_load: float) -> dict:
    """Saturated pass device at i_load: V_SG, g_m (finite difference), r_ds."""
    vsg = brentq(lambda v: dev.i_sat(w, v) - i_load, 0.0, 3.0, xtol=1e-14)
    h = 1e-6
    gm = (dev.i_sat(w, vsg + h) - dev.i_sat(w, vsg - h)) / (2 * h)
    return {"vsg": vsg, "gm": gm, "rds": dev.va_per_l * dev.length / i_load, "ic": i_load / dev.ispec(w)}


@dataclass
class LDO:
    vout: float = 1.2
    vref: float = 0.6
    gma: float = 1e-3        # error-amplifier transconductance, S
    ra: float = 100e3        # error-amplifier output resistance, ohm
    ca: float = 0.2e-12      # error-amplifier output capacitance, F
    gmb: float = 2e-3        # gate-driver (buffer) output conductance, S
    cl: float = 1e-6         # output capacitor, F
    esr: float = 5e-3        # its ESR, ohm
    rdiv: float = 1.2e6      # divider total, ohm
    k_gate: float = 1.0      # fraction of the supply ripple carried by the gate
    dev: PMOS = field(default_factory=PMOS)
    w: float = 0.0           # pass-device width (set by size_pass_device)
    cg: float = 0.0          # gate capacitance

    @property
    def beta(self) -> float:
        return self.vref / self.vout

    @property
    def a_ea(self) -> float:
        return self.gma * self.ra

    def small_signal(self, i_load: float) -> dict:
        op = operating_point(self.dev, self.w, i_load)
        rl = self.vout / i_load
        rout = 1 / (1 / op["rds"] + 1 / rl + 1 / self.rdiv)
        return {**op, "rl": rl, "rout": rout, "pa": 1 / (self.ra * self.ca), "pg": self.gmb / self.cg,
                "pout": 1 / (rout * self.cl), "zesr": 1 / (self.esr * self.cl)}

    def transfer(self, i_load: float):
        """Return functions of s: loop gain, open-loop output impedance, closed-loop output impedance, 1/PSRR."""
        ss = self.small_signal(i_load)

        def zout(s):
            zc = self.esr + 1 / (s * self.cl)
            return ss["rout"] * zc / (ss["rout"] + zc)

        def loop(s):
            return self.a_ea * self.beta * ss["gm"] * zout(s) / ((1 + s / ss["pa"]) * (1 + s / ss["pg"]))

        def zcl(s):
            return zout(s) / (1 + loop(s))

        def psrr_inv(s):
            inj = ss["gm"] * (1 - self.k_gate) + 1 / ss["rds"]
            return inj * zout(s) / (1 + loop(s))
        return loop, zout, zcl, psrr_inv, ss


def margins(loop, f_lo: float = 1.0, f_hi: float = 1e10, n: int = 40001) -> dict:
    f = np.logspace(math.log10(f_lo), math.log10(f_hi), n)
    hv = np.array([loop(2j * math.pi * x) for x in f])
    mag = np.abs(hv)
    ph = np.unwrap(np.angle(hv))
    i = int(np.where(mag < 1)[0][0])
    fc = brentq(lambda x: abs(loop(2j * math.pi * x)) - 1, f[i - 1], f[i])
    pm = 180 + math.degrees(np.interp(math.log10(fc), np.log10(f), ph))
    return {"fc": fc, "pm": pm, "l0": abs(loop(2j * math.pi * 1e-3))}


def load_step_droop(ldo: LDO, i_load: float, delta_i: float, t_end: float = 5e-6, npts: int = 50001) -> dict:
    """Linearized response of the output to a load-current step delta_i at the i_load operating point:
    v(t) = -delta_i * step response of Z_cl. Returns the peak droop and its time."""
    ss = ldo.small_signal(i_load)
    s = np.poly1d([1, 0])
    # rational forms: Z_out = R (1 + s ESR C) / (1 + s (R + ESR) C)
    zn = ss["rout"] * np.poly1d([ldo.esr * ldo.cl, 1])
    zd = np.poly1d([(ss["rout"] + ldo.esr) * ldo.cl, 1])
    den_ea = np.poly1d([1 / ss["pa"], 1]) * np.poly1d([1 / ss["pg"], 1])
    k = ldo.a_ea * ldo.beta * ss["gm"]
    # Z_cl = zn/zd / (1 + k zn/(zd den_ea)) = zn den_ea / (zd den_ea + k zn)
    num = zn * den_ea
    den = zd * den_ea + k * zn
    t = np.linspace(0, t_end, npts)
    _, y = signal.step((num.coeffs, den.coeffs), T=t)
    v = -delta_i * y
    i = int(np.argmin(v))
    del s
    return {"droop": -v[i], "t_peak": t[i], "final": -v[-1]}


def load_step_nonlinear(ldo: LDO, i0: float, i1: float, vin: float = 1.8, t_rise: float = 1e-9,
                        t_end: float = 40e-6, npts: int = 200001) -> dict:
    """Nonlinear load step from i0 to i1 (linear ramp over t_rise). States: output deviation x, error-amplifier
    output y, gate deviation z (z > 0 pulls the gate down, raising V_SG). The pass device follows the saturated
    charge-based law with r_ds = V_A' L / I; the error amplifier and buffer are linear (no slew limit)."""
    dev, w = ldo.dev, ldo.w
    va = dev.va_per_l * dev.length
    vsg0 = brentq(lambda v: dev.i_sat(w, v) - (i0 + ldo.vout / ldo.rdiv), 0.0, 3.0, xtol=1e-15)
    vsd0 = vin - ldo.vout

    def i_pass(z, x):
        return dev.i_sat(w, vsg0 + z) * (1 + ((vsd0 - x) - vsd0) / va)

    def i_load(t):
        return i0 + (i1 - i0) * min(max(t / t_rise, 0.0), 1.0)

    def rhs(t, st):
        x, y, z = st
        dx = (i_pass(z, x) - i_load(t) - (ldo.vout + x) / ldo.rdiv) / ldo.cl
        dy = (-ldo.gma * ldo.beta * x - y / ldo.ra) / ldo.ca
        dz = ldo.gmb * (y - z) / ldo.cg
        return [dx, dy, dz]
    sol = solve_ivp(rhs, (0.0, t_end), [0.0, 0.0, 0.0], method="Radau", max_step=2e-9, rtol=1e-8, atol=1e-12,
                    dense_output=True)
    t = np.linspace(0.0, t_end, npts)
    x = sol.sol(t)[0]
    i = int(np.argmin(x)) if i1 > i0 else int(np.argmax(x))
    return {"t": t, "v": x, "peak": x[i], "t_peak": t[i], "final": x[-1]}


def design(vin_min: float = 1.35, v_dropout: float = 0.15, i_max: float = 0.1) -> LDO:
    dev = PMOS()
    sz = size_pass_device(dev, vin_min, v_dropout, i_max)
    return LDO(dev=dev, w=sz["w"], cg=sz["cgg"])


if __name__ == "__main__":
    ldo = design()
    print(f"W = {ldo.w * 1e3:.3f} mm, C_g = {ldo.cg * 1e12:.3f} pF")
    for il in (100e-6, 1e-3, 10e-3, 100e-3):
        loop, *_ = ldo.transfer(il)
        m = margins(loop)
        print(f"I_L = {il * 1e3:7.3f} mA: L(0) = {m['l0']:7.1f}, f_c = {m['fc'] / 1e3:9.2f} kHz, PM = {m['pm']:.1f} deg")
