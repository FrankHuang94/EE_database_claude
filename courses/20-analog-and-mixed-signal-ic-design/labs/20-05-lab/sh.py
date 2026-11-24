"""Lab 20-05: sample-and-hold and comparator models for the illustrative T130 process.

Running design (chapter 20-05): the front end of a 12-bit, 100 MS/s differential SAR ADC with V_DD = 1.2 V. Each input
swings 0.2 to 1.0 V around a 0.6 V common mode, so the differential full scale is 1.6 V peak to peak.

Sampling switch (section 3.2): a T130 NMOS in triode, I = K (V_G - V_TH(v_m) - v_m)(v_a - v_b) with K = mu C_ox W/L,
v_m = (v_a + v_b)/2 the channel's mean voltage and the body effect V_TH = V_TH0 + gamma_b (sqrt(2 phi_F + v_m) -
sqrt(2 phi_F)) with the body at ground. A plain switch has V_G = V_DD; a bootstrapped switch has V_G = v_in + V_DD
(ideal bootstrap capacitor); with the body tied to the source the body term is zero.

StrongARM comparator (section 3.6): integration gain A_int = (g_m/I_D) V_TH; input-referred integration noise
sigma^2 = 4 gamma kT/(A_int C); regeneration time constant tau = C/g_m,latch. All quantities SI.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import solve_ivp

K_B = 1.380649e-23
T0 = 300.0
KT = K_B * T0

# T130 NMOS (20-01) and illustrative body-effect and overlap values
MU_N, COX, VTH0, GAMMA_B, PHI2 = 350e-4, 8.6e-3, 0.45, 0.4, 0.8
L_MIN = 0.13e-6
VDD = 1.2


def vth(vsb: float) -> float:
    """Threshold with the body effect (body at ground, source/channel at vsb)."""
    return VTH0 + GAMMA_B * (math.sqrt(PHI2 + max(vsb, -0.5 * PHI2)) - math.sqrt(PHI2))


def ron(w: float, vg: float, vin: float, length: float = L_MIN, body_effect: bool = True) -> float:
    """Small-signal on-resistance of an NMOS switch at input vin (V_DS -> 0)."""
    vt = vth(vin) if body_effect else VTH0
    vov = vg - vin - vt
    return math.inf if vov <= 0 else 1.0 / (MU_N * COX * (w / length) * vov)


def ktc_cap(n_bits: int, vfs_pp_diff: float, differential: bool = True) -> float:
    """Capacitance per side that makes the sampled kT/C noise equal to the quantization noise."""
    lsb = vfs_pp_diff / 2 ** n_bits
    q2 = lsb ** 2 / 12
    return (2 if differential else 1) * KT / q2


def snr_db(n_bits: int, vfs_pp_diff: float, c: float, sigma_t: float = 0.0, f_in: float = 0.0) -> float:
    """SNR of a full-scale sine with quantization, differential kT/C and jitter noise."""
    a = vfs_pp_diff / 2
    sig = a ** 2 / 2
    lsb = vfs_pp_diff / 2 ** n_bits
    noise = lsb ** 2 / 12 + 2 * KT / c + sig * (2 * math.pi * f_in * sigma_t) ** 2
    return 10 * math.log10(sig / noise)


def jitter_snr_db(f_in: float, sigma_t: float) -> float:
    return -20 * math.log10(2 * math.pi * f_in * sigma_t)


def track(w: float, c: float, f_in: float, amp: float, vcm: float = 0.6, mode: str = "boot",
          periods: int = 12, keep: int = 4, pts_per_period: int = 512) -> dict:
    """Track-mode response of a switch driving C from a sine source; returns harmonic amplitudes (V) and dBc.

    mode: 'boot' (gate = v_in + V_DD, body at ground), 'boot_nobody' (body tied to source), 'plain' (gate = V_DD)."""
    k = MU_N * COX * w / L_MIN
    om = 2 * math.pi * f_in

    def current(t, vo):
        vi = vcm + amp * math.sin(om * t)
        vg = vi + VDD if mode.startswith("boot") else VDD
        vm = 0.5 * (vi + vo)
        vt = VTH0 if mode == "boot_nobody" else vth(vm)
        return k * max(vg - vt - vm, 0.0) * (vi - vo)

    sol = solve_ivp(lambda t, y: [current(t, y[0]) / c], (0, periods / f_in), [vcm], method="DOP853",
                    rtol=1e-11, atol=1e-14, dense_output=True)
    n = keep * pts_per_period
    t = (periods - keep) / f_in + np.arange(n) / (pts_per_period * f_in)
    v = sol.sol(t)[0]
    spec = np.fft.rfft(v) / n * 2
    h = [abs(spec[keep * m]) for m in range(1, 6)]
    return {"h1": h[0], "h2": h[1], "h3": h[2], "hd2_db": 20 * math.log10(h[1] / h[0]),
            "hd3_db": 20 * math.log10(h[2] / h[0]), "gain": h[0] / amp}


def strongarm(gm_id: float, c: float, vth_latch: float = VTH0, gamma: float = 2 / 3) -> dict:
    """Integration gain, input-referred integration noise (rms) and reset energy 2 C V_DD^2."""
    a = gm_id * vth_latch
    sigma = math.sqrt(4 * gamma * KT / (a * c))
    return {"a_int": a, "sigma": sigma, "energy": 2 * c * VDD ** 2}


def decision_time(v_in: float, a_int: float, tau: float, v_logic: float = VDD / 2) -> float:
    return tau * math.log(v_logic / (a_int * abs(v_in)))


def meta_vmin(t_avail: float, a_int: float, tau: float, v_logic: float = VDD / 2) -> float:
    """Smallest input that still resolves to v_logic within t_avail."""
    return v_logic / a_int * math.exp(-t_avail / tau)


def sar_meta_probability(t_avail: float, a_int: float, tau: float, n_bits: int, vfs: float,
                         v_logic: float = VDD / 2) -> float:
    """Probability per conversion that some decision of an N-bit SAR fails to resolve, for an input uniform over
    the full scale: decision k sees a residue uniform over vfs/2^(k-1)."""
    vmin = meta_vmin(t_avail, a_int, tau, v_logic)
    return sum(2 * vmin * 2 ** (k - 1) / vfs for k in range(1, n_bits + 1))


def regen(v0: float, gm: float, c: float, imax: float, v_target: float, t_end: float = 2e-9) -> float:
    """Time for a cross-coupled pair of tanh-limited transconductors (each i = imax tanh(gm v / imax)) loaded by C to
    grow a differential v0 to v_target; v = v1 - v2 with v1 = -v2."""
    def rhs(t, y):
        v1 = y[0]
        return [imax * math.tanh(gm * v1 / imax) / c]

    def hit(t, y):
        return 2 * y[0] - v_target
    hit.terminal = True
    sol = solve_ivp(rhs, (0, t_end), [v0 / 2], events=hit, rtol=1e-10, atol=1e-15, max_step=1e-12)
    return float(sol.t_events[0][0])


if __name__ == "__main__":
    c = ktc_cap(12, 1.6)
    print(f"C per side = {c * 1e12:.4f} pF, sqrt(kT/C) = {math.sqrt(KT / c) * 1e6:.2f} uV")
    for vin in (0.2, 0.6, 1.0):
        print(vin, "plain R_on", ron(0.888e-6, VDD, vin), "boot R_on", ron(0.888e-6, vin + VDD, vin))
