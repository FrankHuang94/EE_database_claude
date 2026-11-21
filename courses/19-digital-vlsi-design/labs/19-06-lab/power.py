"""Power models for Lab 19-06.

Dynamic (switching) power, short-circuit power of a ramp-driven inverter (Veendrick's model and a numerical
integration), subthreshold leakage with DIBL and the stack effect, voltage scaling for a fixed throughput and with
parallelism (alpha-power delay), the minimum-energy supply of subthreshold logic, and power-gating break-even.
Units: SI.
"""
from __future__ import annotations

import math

from scipy.integrate import quad
from scipy.optimize import brentq

VT_300K = 1.380649e-23 * 300 / 1.602176634e-19


# ---------------------------------------------------------------- dynamic and short-circuit power
def dynamic_power(alpha: float, c: float, vdd: float, f: float) -> float:
    """P = alpha C VDD^2 f, alpha = probability of a 0 -> 1 output transition per cycle."""
    return alpha * c * vdd * vdd * f


def short_circuit_power_veendrick(beta: float, vdd: float, vt: float, t_ramp: float, period: float) -> float:
    """Unloaded symmetric inverter, linear input ramps of duration t_ramp (0 to VDD), two transitions per period:
    P = (beta/12) (VDD - 2 VT)^3 t_ramp / period."""
    return beta / 12 * (vdd - 2 * vt) ** 3 * t_ramp / period


def short_circuit_charge_numeric(beta: float, vdd: float, vt: float, t_ramp: float) -> float:
    """Charge drawn from the supply during one input ramp of an unloaded symmetric square-law inverter: the current
    is the saturation current of whichever transistor is turning off... limited by the weaker of the two."""
    def i(t):
        vin = vdd * t / t_ramp
        i_n = 0.5 * beta * max(vin - vt, 0.0) ** 2
        i_p = 0.5 * beta * max(vdd - vin - vt, 0.0) ** 2
        return min(i_n, i_p)
    return quad(i, 0, t_ramp, points=[t_ramp / 2], epsabs=0, epsrel=1e-12)[0]


# ---------------------------------------------------------------- leakage
def subthreshold_current(i0: float, vgs: float, vds: float, vt: float, n: float, eta: float,
                         vth: float = VT_300K) -> float:
    """I = I0 exp((VGS - VT + eta VDS) / (n vth)) (1 - exp(-VDS / vth)): subthreshold with DIBL coefficient eta."""
    return i0 * math.exp((vgs - vt + eta * vds) / (n * vth)) * (1 - math.exp(-vds / vth))


def stack_leakage_ratio(vdd: float, vt: float, n: float, eta: float, vth: float = VT_300K) -> tuple[float, float]:
    """Two series off NMOS (gates at 0) against one: solve for the intermediate node vx where the currents balance;
    returns (vx, I_single / I_stack)."""
    def i_top(vx):
        return subthreshold_current(1.0, -vx, vdd - vx, vt, n, eta, vth)

    def i_bot(vx):
        return subthreshold_current(1.0, 0.0, vx, vt, n, eta, vth)
    vx = brentq(lambda x: i_top(x) - i_bot(x), 1e-9, vdd / 2, xtol=1e-15)
    single = subthreshold_current(1.0, 0.0, vdd, vt, n, eta, vth)
    return vx, single / i_bot(vx)


def leakage_factor_for_vt_shift(dvt: float, slope_mv_per_dec: float) -> float:
    """Leakage multiplies by 10^(dVT / S) when the threshold is lowered by dVT."""
    return 10 ** (dvt * 1e3 / slope_mv_per_dec)


# ---------------------------------------------------------------- voltage scaling
def alpha_delay(v: float, vt: float, alpha: float) -> float:
    return v / (v - vt) ** alpha


def supply_for_slowdown(factor: float, v0: float, vt: float, alpha: float) -> float:
    """Supply at which the delay is `factor` times the delay at v0."""
    target = factor * alpha_delay(v0, vt, alpha)
    return brentq(lambda v: alpha_delay(v, vt, alpha) - target, vt + 1e-6, v0, xtol=1e-14)


# ---------------------------------------------------------------- minimum-energy point (subthreshold)
def energy_per_op(v: float, alpha: float, depth: float, n: float, vth: float = VT_300K) -> float:
    """Energy per operation, normalized to N C: V^2 [alpha + depth exp(-V/(n vth))] (dynamic plus leakage over the
    cycle time, with I_on/I_off = exp(V/(n vth)) in subthreshold)."""
    return v * v * (alpha + depth * math.exp(-v / (n * vth)))


def minimum_energy_supply(alpha: float, depth: float, n: float, vth: float = VT_300K) -> float | None:
    """Local minimum of energy_per_op: dE/dV = 0 gives depth exp(-x) (x - 2) = 2 alpha with x = V/(n vth). The
    left-hand side peaks at x = 3; the larger root (x > 3) is the minimum, the smaller one a local maximum below which
    the model (and robust logic) no longer applies. Returns None if depth exp(-3) <= 2 alpha (no interior minimum)."""
    if depth * math.exp(-3) <= 2 * alpha:
        return None
    x = brentq(lambda x: depth * math.exp(-x) * (x - 2) - 2 * alpha, 3.0, 200.0, xtol=1e-14)
    return x * n * vth


# ---------------------------------------------------------------- power gating
def break_even_time(e_overhead: float, p_leak_saved: float) -> float:
    """Sleep longer than E_overhead / P_saved for power gating to save energy."""
    return e_overhead / p_leak_saved
