"""Lab 20-03: bandgap and current references.

Device model (chapter 20-03, section 3.1). A diode-connected substrate PNP carries emitter current I (base current
neglected) with
    I_S(T) = A I_S0 (T/T0)^eta exp[(q V_g0 / k)(1/T0 - 1/T)],   V_BE = V_T ln(I / I_S(T)),
the same form as SPICE's Gummel-Poon model with EG = V_g0 and XTI = eta. The T130 substrate PNP is illustrative:
I_S0 = 2e-17 A for a unit device at T0 = 300 K, V_g0 = 1.2009 V (09-06's silicon value) and eta = 3.

Circuits:
* `opamp_bandgap`: Q1 (area 1) at node A and R1 + Q2 (area N) at node B, each fed from the output by R2; an op-amp
  forces V_A - V_B = V_os (its input offset). Output V_REF = V_BE1 + I1 R2.
* `current_mode_bandgap`: the sub-1 V reference of Banba et al.: as above but each node also has R2 to ground,
  the op-amp drives three equal current sources, and the third flows into R3.
* `beta_multiplier`: a self-biased NMOS current reference (M2 K times wider, resistor R in its source), solved with
  the long-channel charge-based model of 20-01.
All quantities SI.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

K_B, Q_E = 1.380649e-23, 1.602176634e-19
T0 = 300.0


def vt(temp: float) -> float:
    return K_B * temp / Q_E


@dataclass
class PNP:
    is0: float = 2e-17      # A, unit device at T0
    vg0: float = 1.2009     # V, extrapolated bandgap (09-06)
    eta: float = 3.0        # temperature exponent of I_S

    def i_s(self, temp: float, area: float = 1.0) -> float:
        return area * self.is0 * (temp / T0) ** self.eta * math.exp(Q_E * self.vg0 / K_B * (1 / T0 - 1 / temp))

    def vbe(self, i: float, temp: float, area: float = 1.0) -> float:
        return vt(temp) * math.log(i / self.i_s(temp, area))


def vbe_closed_form(vbe0: float, temp: float, vg0: float, eta: float, m: float) -> float:
    """Tsividis' form: V_BE(T) = V_g0 - (V_g0 - V_BE0) T/T0 - (eta - m) V_T ln(T/T0) for a bias current ~ T^m."""
    return vg0 - (vg0 - vbe0) * temp / T0 - (eta - m) * vt(temp) * math.log(temp / T0)


def k_zero_tc(vbe0: float, n: float, vg0: float, eta: float, m: float = 1.0, tc: float = T0) -> float:
    """PTAT gain K (= R2/R1) that zeroes dV_REF/dT at the temperature tc (V_BE0 given at T0)."""
    # d/dT [V_BE(T) + K V_T ln N] = 0 at tc, using the closed form
    dvbe = -(vg0 - vbe0) / T0 - (eta - m) * (K_B / Q_E) * (math.log(tc / T0) + 1)
    return -dvbe / ((K_B / Q_E) * math.log(n))


def vref_closed_form(temp: float, vg0: float, eta: float, m: float = 1.0, tc: float = T0) -> float:
    """First-order bandgap with zero TC at tc: V_REF(T) = V_g0 + (eta - m) V_T(T) [1 - ln(T/tc)]."""
    return vg0 + (eta - m) * vt(temp) * (1 - math.log(temp / tc))


def opamp_bandgap(temp: float, r1: float, r2: float, n: float = 8.0, pnp: PNP | None = None,
                  vos: float = 0.0, r2b: float | None = None) -> dict:
    """Solve the op-amp bandgap exactly. Returns V_REF, the two currents and the node voltages."""
    pnp = pnp or PNP()
    r2b = r2 if r2b is None else r2b

    def resid(i2: float) -> float:
        vb = pnp.vbe(i2, temp, n) + i2 * r1
        va = vb + vos
        vo = vb + i2 * r2b
        i1 = (vo - va) / r2
        return pnp.vbe(i1, temp) - va if i1 > 0 else 1.0

    i2 = brentq(resid, 1e-12, 1e-3, xtol=1e-22, rtol=1e-14)
    vb = pnp.vbe(i2, temp, n) + i2 * r1
    vo = vb + i2 * r2b
    va = vb + vos
    return {"vref": vo, "i1": (vo - va) / r2, "i2": i2, "va": va, "vb": vb}


def current_mode_bandgap(temp: float, r1: float, r2: float, r3: float, n: float = 8.0,
                         pnp: PNP | None = None) -> dict:
    """Banba-style sub-1 V reference with an ideal op-amp and ideal 1:1:1 current mirrors."""
    pnp = pnp or PNP()

    def resid(i_q: float) -> float:
        va = pnp.vbe(i_q, temp)                 # Q1 branch: BJT current i_q
        i_branch = i_q + va / r2
        i2 = i_branch - va / r2                 # node B = node A: same R2 current, so the BJT currents are equal
        return va - (pnp.vbe(i2, temp, n) + i2 * r1)

    iq = brentq(resid, 1e-12, 1e-3, xtol=1e-22, rtol=1e-14)
    va = pnp.vbe(iq, temp)
    i_tot = iq + va / r2
    return {"vref": i_tot * r3, "iq": iq, "i_branch": i_tot, "va": va}


def box_tc(temps, values, v_nom: float) -> float:
    """Box-method temperature coefficient in ppm/K: (max - min) / (V_nom (T_max - T_min))."""
    temps, values = np.asarray(temps), np.asarray(values)
    return (values.max() - values.min()) / (v_nom * (temps.max() - temps.min())) * 1e6


# ---------------------------------------------------------------- a beta-multiplier current reference
@dataclass
class NMOS:
    """Long-channel charge-based NMOS (20-01) with bulk at ground: (V_P - V_S)/V_T = 2 q + ln q."""
    mu: float = 350e-4
    cox: float = 8.6e-3
    n: float = 1.3
    vth: float = 0.45

    def ispec(self, w_over_l: float, temp: float = T0) -> float:
        return 2 * self.n * self.mu * self.cox * w_over_l * vt(temp) ** 2

    def q_of(self, vg: float, vs: float, temp: float = T0) -> float:
        vp = (vg - self.vth) / self.n
        return brentq(lambda q: 2 * q + math.log(q) - (vp - vs) / vt(temp), 1e-40, 1e6, xtol=1e-40, rtol=1e-15)

    def i_d(self, vg: float, vs: float, w_over_l: float, temp: float = T0) -> float:
        q = self.q_of(vg, vs, temp)
        return self.ispec(w_over_l, temp) * (q * q + q)


def beta_multiplier(r: float, k: float, w_over_l: float, nmos: NMOS | None = None, temp: float = T0) -> float:
    """Non-zero operating current of the beta multiplier: M1 (W/L) diode-connected, M2 (K W/L) with source
    resistor R, equal currents forced by a 1:1 PMOS mirror (bulk at ground, so M2 sees body effect)."""
    nmos = nmos or NMOS()

    def resid(vg: float) -> float:
        i = nmos.i_d(vg, 0.0, w_over_l, temp)
        vs = brentq(lambda x: nmos.i_d(vg, x, k * w_over_l, temp) - x / r, 0.0, vg, xtol=1e-16)
        return i - vs / r
    # the current at which M1 and M2 agree; start well above the off state
    vg = brentq(resid, nmos.vth - 0.25, nmos.vth + 1.0, xtol=1e-15)
    return nmos.i_d(vg, 0.0, w_over_l, temp)


if __name__ == "__main__":
    p = PNP()
    i0, n = 5e-6, 8.0
    vbe0 = p.vbe(i0, T0)
    k = k_zero_tc(vbe0, n, p.vg0, p.eta)
    r1 = vt(T0) * math.log(n) / i0
    print(f"V_BE0 = {vbe0:.4f} V, K = {k:.3f}, R1 = {r1 / 1e3:.3f} kohm, R2 = {k * r1 / 1e3:.2f} kohm")
    print(f"V_REF(T0) = {opamp_bandgap(T0, r1, k * r1, n)['vref']:.5f} V")
