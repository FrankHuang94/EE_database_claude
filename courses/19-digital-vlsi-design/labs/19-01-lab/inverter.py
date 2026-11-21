"""CMOS inverter static models for Lab 19-01.

Square-law (long-channel) and alpha-power (velocity-saturated) transistors with channel-length modulation, the
voltage transfer characteristic by root finding, the switching threshold, the unity-gain points and noise margins,
the gain at the switching threshold, and a subthreshold inverter. Voltages in volts, k in A/V^2 (A/V^alpha for the
alpha-power law), lambda in 1/V.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

VT_300K = 1.380649e-23 * 300.0 / 1.602176634e-19        # thermal voltage at 300 K, 25.85 mV


@dataclass
class Inverter:
    vdd: float
    vtn: float
    vtp: float                 # magnitude of the PMOS threshold
    kn: float                  # mu_n Cox W_n / L_n (square law) or the alpha-power coefficient
    kp: float
    lam_n: float = 0.0
    lam_p: float = 0.0
    alpha: float = 2.0         # 2 = square law; 1 = fully velocity-saturated

    # ---------------------------------------------------------------- device currents
    def i_n(self, vin: float, vout: float) -> float:
        """NMOS drain current (source at ground, drain at vout)."""
        vov = vin - self.vtn
        if vov <= 0:
            return 0.0
        return _drain(self.kn, vov, vout, self.lam_n, self.alpha)

    def i_p(self, vin: float, vout: float) -> float:
        """PMOS drain current (source at VDD, drain at vout), as a positive number flowing into the output."""
        vov = self.vdd - vin - self.vtp
        if vov <= 0:
            return 0.0
        return _drain(self.kp, vov, self.vdd - vout, self.lam_p, self.alpha)

    # ---------------------------------------------------------------- transfer characteristic
    def vout(self, vin: float) -> float:
        """Output voltage for a given input: the voltage where the PMOS sources what the NMOS sinks."""
        f = lambda vo: self.i_p(vin, vo) - self.i_n(vin, vo)  # noqa: E731
        lo, hi = 0.0, self.vdd
        if f(lo) <= 0:
            return 0.0
        if f(hi) >= 0:
            return self.vdd
        return brentq(f, lo, hi, xtol=1e-14, rtol=1e-15, maxiter=500)

    def vtc(self, vin: np.ndarray) -> np.ndarray:
        return np.array([self.vout(x) for x in vin])

    def vm(self) -> float:
        """Switching threshold: the input at which Vout = Vin."""
        return brentq(lambda x: self.vout(x) - x, 1e-9, self.vdd - 1e-9, xtol=1e-14)

    def gain(self, vin: float, h: float = 1e-6) -> float:
        return (self.vout(vin + h) - self.vout(vin - h)) / (2 * h)

    def unity_gain_points(self) -> tuple[float, float]:
        """V_IL and V_IH: the inputs at which dVout/dVin = -1, below and above V_M."""
        m = self.vm()
        g = lambda x: self.gain(x) + 1.0  # noqa: E731
        vil = brentq(g, self.vtn + 1e-6, m - 1e-6, xtol=1e-12)
        vih = brentq(g, m + 1e-6, self.vdd - self.vtp - 1e-6, xtol=1e-12)
        return vil, vih

    def noise_margins(self) -> tuple[float, float]:
        """(NM_L, NM_H) with V_OL and V_OH taken at the unity-gain points' complementary inputs."""
        vil, vih = self.unity_gain_points()
        vol, voh = self.vout(self.vdd), self.vout(0.0)
        return vil - vol, voh - vih


def _drain(k: float, vov: float, vds: float, lam: float, alpha: float) -> float:
    """Drain current with channel-length modulation. For alpha = 2 this is the square law; otherwise the
    alpha-power law with V_Dsat = vov (a simplification adequate for the transfer curve's shape)."""
    if vds <= 0:
        return 0.0
    if alpha == 2.0:
        if vds < vov:
            return k * (vov * vds - 0.5 * vds * vds) * (1 + lam * vds)
        return 0.5 * k * vov * vov * (1 + lam * vds)
    isat = 0.5 * k * vov ** alpha
    vdsat = vov
    if vds < vdsat:
        return isat * (2 - vds / vdsat) * (vds / vdsat) * (1 + lam * vds)
    return isat * (1 + lam * vds)


def vm_closed_form(vdd: float, vtn: float, vtp: float, r: float, alpha: float = 2.0) -> float:
    """Switching threshold with both devices saturated and no channel-length modulation; r = kn / kp."""
    s = r ** (1.0 / alpha)
    return (vtn * s + vdd - vtp) / (1 + s)


def ratio_for_vm(vdd: float, vtn: float, vtp: float, vm: float, alpha: float = 2.0) -> float:
    """The kn/kp that places the switching threshold at vm (inverse of vm_closed_form)."""
    return ((vdd - vtp - vm) / (vm - vtn)) ** alpha


def vil_closed_form(vdd: float, vtn: float, vtp: float, r: float) -> float:
    """Square-law V_IL for any r = kn/kp (lambda = 0): V_IL = V_TN + t/(1 + t) (VDD - V_TN - |V_TP|)."""
    t = (2 * math.sqrt(r * r + 3 * r) - r) / (r * (r + 4))
    return vtn + t / (1 + t) * (vdd - vtn - vtp)


def vih_closed_form(vdd: float, vtn: float, vtp: float, r: float) -> float:
    """Square-law V_IH, by the mirror symmetry Vin -> VDD - Vin that swaps the two transistors."""
    return vdd - vil_closed_form(vdd, vtp, vtn, 1.0 / r)


def gain_at_vm(vdd: float, vtn: float, vtp: float, r: float, lam_n: float, lam_p: float) -> float:
    """Small-signal gain at V_M: -(g_mn + g_mp)/(g_dsn + g_dsp) with g_m = 2 I_D / V_ov and g_ds = lambda I_D."""
    vm = vm_closed_form(vdd, vtn, vtp, r)
    return -2 * (1 / (vm - vtn) + 1 / (vdd - vm - vtp)) / (lam_n + lam_p)


def subthreshold_gain(vdd: float, n: float, vt: float = VT_300K) -> float:
    """Magnitude of a symmetric subthreshold inverter's gain at V_M = VDD/2: (exp(VDD/(2 VT)) - 1)/n."""
    return (math.exp(vdd / (2 * vt)) - 1) / n


def subthreshold_vdd_min(n: float, vt: float = VT_300K) -> float:
    """Smallest supply for which the symmetric subthreshold inverter has a gain of magnitude 1: 2 VT ln(1 + n)."""
    return 2 * vt * math.log(1 + n)


def subthreshold_vtc(vdd: float, n: float, vin: np.ndarray, vt: float = VT_300K) -> np.ndarray:
    """Transfer curve of a symmetric subthreshold inverter, solved from I_n = I_p with
    I = I0 exp(Vov / (n VT)) (1 - exp(-VDS / VT)) and equal I0 and thresholds."""
    out = []
    for x in vin:
        f = lambda y: (math.exp((x - vdd / 2) / (n * vt)) * (1 - math.exp(-y / vt))  # noqa: E731
                       - math.exp((vdd / 2 - x) / (n * vt)) * (1 - math.exp(-(vdd - y) / vt)))
        out.append(brentq(f, 0.0, vdd, xtol=1e-15))
    return np.array(out)


def chain(vin: float, inv: Inverter, stages: int) -> list[float]:
    """Levels along a chain of identical inverters: each stage's output drives the next one's input."""
    levels = [vin]
    for _ in range(stages):
        levels.append(inv.vout(levels[-1]))
    return levels
