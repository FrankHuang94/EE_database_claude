"""Lab 20-01: a charge-based MOSFET model for gm/ID design.

The model (derived in chapter 20-01, section 3) describes a saturated MOSFET by its normalized inversion charge q
at the source end. With the pinch-off voltage V_P = (V_GS - V_TH)/n and the source at 0 V,

    V_P / V_T = 2 q + ln q                                  (charge-potential relation)
    I_D = I_spec (q^2 + q) / (1 + lam q)                    (drift + diffusion, with a velocity-saturation divisor)
    I_spec = 2 n mu C_ox (W/L) V_T^2,   lam = L_sat / L,   L_sat = mu V_T / v_sat

so that the inversion coefficient IC = I_D / I_spec = (q^2 + q)/(1 + lam q). With lam = 0 the model is the long-channel
charge-based (EKV-style) model, exact in weak and strong inversion; lam > 0 makes the current tend to
W C_ox v_sat V_ov in deep strong inversion. All quantities SI unless stated. The gate capacitance used for f_T is the
strong-inversion value (2/3) W L C_ox throughout (an assumption: it overestimates C_gg, and so underestimates f_T,
in weak inversion).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.optimize import brentq

K_B, Q_E = 1.380649e-23, 1.602176634e-19


def thermal_voltage(temp_k: float = 300.0) -> float:
    return K_B * temp_k / Q_E


@dataclass
class Process:
    """An illustrative 130 nm-class process ("T130"); the numbers are teaching values, not a foundry's."""
    mu: float = 350e-4          # effective electron mobility, m^2/(V s)
    cox: float = 8.6e-3         # gate capacitance per area, F/m^2 (8.6 fF/um^2)
    n: float = 1.3              # slope factor
    vth: float = 0.45           # threshold voltage, V
    vsat: float = 8e4           # saturation velocity, m/s (8e6 cm/s, as 09-10)
    va_per_l: float = 8e6       # Early voltage per unit length, V/m (8 V/um)
    temp: float = 300.0         # K

    @property
    def vt(self) -> float:
        return thermal_voltage(self.temp)

    def lam(self, length: float) -> float:
        return self.mu * self.vt / (self.vsat * length)

    def ispec(self, w: float, length: float) -> float:
        return 2 * self.n * self.mu * self.cox * (w / length) * self.vt ** 2

    def ispec_square(self, length: float) -> float:
        """I_spec for W = L (the 'square' specific current), A."""
        return 2 * self.n * self.mu * self.cox * self.vt ** 2


# ---------------------------------------------------------------- the normalized model
def ic_of_q(q: float, lam: float = 0.0) -> float:
    return (q * q + q) / (1 + lam * q)


def q_of_ic(ic: float, lam: float = 0.0) -> float:
    if lam == 0.0:
        return (math.sqrt(1 + 4 * ic) - 1) / 2
    return brentq(lambda q: ic_of_q(q, lam) - ic, 1e-15, 1e9, xtol=1e-15, rtol=1e-14)


def di_dv(q: float, lam: float = 0.0) -> float:
    """Derivative of the normalized current with respect to V_P / V_T (equals g_m n V_T / I_spec)."""
    di_dq = (lam * q * q + 2 * q + 1) / (1 + lam * q) ** 2
    return di_dq * q / (2 * q + 1)


def gm_over_id(ic: float, n: float, vt: float, lam: float = 0.0) -> float:
    """Transconductance efficiency g_m / I_D in 1/V (S/A)."""
    q = q_of_ic(ic, lam)
    return di_dv(q, lam) / (n * vt * ic_of_q(q, lam))


def vov_of_ic(ic: float, n: float, vt: float, lam: float = 0.0) -> float:
    """Gate overdrive V_GS - V_TH that gives inversion coefficient IC (source at 0 V)."""
    q = q_of_ic(ic, lam)
    return n * vt * (2 * q + math.log(q))


def ft(ic: float, proc: Process, length: float) -> float:
    """Transit frequency with C_gg = (2/3) W L C_ox, Hz."""
    lam = proc.lam(length)
    q = q_of_ic(ic, lam)
    return 3 * proc.mu * proc.vt * di_dv(q, lam) / (2 * math.pi * length ** 2)


def id_per_w(ic: float, proc: Process, length: float) -> float:
    """Current density I_D / W at inversion coefficient IC, A/m."""
    return ic * proc.ispec_square(length) / length


def intrinsic_gain(ic: float, proc: Process, length: float) -> float:
    """g_m r_o = (g_m/I_D) V_A with V_A = V_A' L."""
    return gm_over_id(ic, proc.n, proc.vt, proc.lam(length)) * proc.va_per_l * length


def ic_for_gm_over_id(target: float, proc: Process, length: float) -> float:
    """Inversion coefficient at which g_m/I_D equals target (1/V)."""
    lam = proc.lam(length)
    return brentq(lambda ic: gm_over_id(ic, proc.n, proc.vt, lam) - target, 1e-6, 1e5, xtol=1e-14, rtol=1e-13)


def size_for_gm(gm: float, gmid: float, proc: Process, length: float) -> tuple[float, float, float]:
    """gm/ID design step: returns (I_D, W, IC) for a target g_m at a chosen g_m/I_D and L."""
    i_d = gm / gmid
    ic = ic_for_gm_over_id(gmid, proc, length)
    w = i_d / id_per_w(ic, proc, length)
    return i_d, w, ic


def drain_current(vgs: float, proc: Process, w: float, length: float) -> float:
    """Saturation current for a given V_GS (source at 0 V)."""
    vp = (vgs - proc.vth) / proc.n
    q = brentq(lambda q: 2 * q + math.log(q) - vp / proc.vt, 1e-30, 1e6, xtol=1e-30, rtol=1e-14)
    return proc.ispec(w, length) * ic_of_q(q, proc.lam(length))
