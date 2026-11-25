"""Lab 22-11 helpers: DC motor, synchronous speed and slip, the induction-machine equivalent circuit and torque–slip
curve, synchronous-machine power angle, V/f operation, inverter voltage limits, affinity laws and EV envelopes.
SI units; speeds in rad/s unless a name says rpm."""
from __future__ import annotations

import cmath
import math

RPM = 2 * math.pi / 60


# ---------------------------------------------------------------- DC motor
def dc_motor(v, r_a, k, torque):
    """Returns (current, back EMF, speed rad/s, output power, efficiency) at a load torque."""
    i = torque / k
    e = v - i * r_a
    w = e / k
    return i, e, w, torque * w, (torque * w) / (v * i) if i else float("nan")


# ---------------------------------------------------------------- AC machines
def sync_speed_rpm(f, poles):
    return 120 * f / poles


def slip(n_sync, n):
    return (n_sync - n) / n_sync


class Induction:
    """Per-phase equivalent circuit (Y): R1 + jX1, magnetizing jXm, rotor R2/s + jX2, phase voltage v_ph."""

    def __init__(self, v_ph, f, poles, r1, x1, xm, r2, x2):
        self.v, self.r1, self.x1, self.xm, self.r2, self.x2 = v_ph, r1, x1, xm, r2, x2
        self.ws = 2 * math.pi * f * 2 / poles

    def thevenin(self):
        z1 = self.r1 + 1j * self.x1
        zm = 1j * self.xm
        vth = self.v * abs(zm / (z1 + zm))
        zth = zm * z1 / (zm + z1)
        return vth, zth.real, zth.imag

    def torque(self, s, r2=None):
        r2 = self.r2 if r2 is None else r2
        vth, rth, xth = self.thevenin()
        return 3 * vth ** 2 * (r2 / s) / (self.ws * ((rth + r2 / s) ** 2 + (xth + self.x2) ** 2))

    def s_max(self, r2=None):
        r2 = self.r2 if r2 is None else r2
        _, rth, xth = self.thevenin()
        return r2 / math.hypot(rth, xth + self.x2)

    def t_max(self):
        vth, rth, xth = self.thevenin()
        return 3 * vth ** 2 / (2 * self.ws * (rth + math.hypot(rth, xth + self.x2)))

    def stator_current(self, s):
        z2 = self.r2 / s + 1j * self.x2
        zp = 1j * self.xm * z2 / (1j * self.xm + z2)
        return self.v / (self.r1 + 1j * self.x1 + zp)


def power_flow(p_in, p_scl, p_core, s, p_fw):
    """Returns (P_ag, rotor copper loss, P_mech, P_out, efficiency)."""
    p_ag = p_in - p_scl - p_core
    p_rcl = s * p_ag
    p_mech = p_ag - p_rcl
    p_out = p_mech - p_fw
    return p_ag, p_rcl, p_mech, p_out, p_out / p_in


def sync_power(v_ph, e_f, x_s, delta_deg):
    return 3 * v_ph * e_f / x_s * math.sin(math.radians(delta_deg))


# ---------------------------------------------------------------- drives
def v_over_f(v_rated, f_rated, f):
    return v_rated * min(f, f_rated) / f_rated


def inverter_vll_rms(v_dc, m=1.0, svpwm=False):
    m_eff = m * (2 / math.sqrt(3) if svpwm else 1.0)
    return math.sqrt(3) / (2 * math.sqrt(2)) * m_eff * v_dc


def affinity(speed_ratio):
    """Returns (flow, head, power) ratios for a fan or centrifugal pump."""
    return speed_ratio, speed_ratio ** 2, speed_ratio ** 3


def ev_envelope(t_peak, n_base_rpm, n_rpm):
    """Torque available at n_rpm for constant torque to base speed and constant power above."""
    return t_peak if n_rpm <= n_base_rpm else t_peak * n_base_rpm / n_rpm
