"""Lab 21-04 helpers: low-noise amplifier topologies, input match, noise factor and linearity.

Small-signal model of the inductively degenerated common-source LNA: source v_s with resistance R_s, gate
inductor L_g (optional series loss r_g), gate-source capacitance C_gs, source inductor L_s, channel current
g_m v_gs and drain noise current with density 4 k T0 gamma g_d0 (written here as 4 k T0 x g_m with x = gamma/alpha).
Induced gate noise is not modelled; the chapter discusses it.
"""
from __future__ import annotations

import math

K_B = 1.380649e-23
T0 = 290.0


def db(x):
    return 10 * math.log10(x)


# ---------------------------------------------------------------- simple topologies
def nf_resistive_termination(f_amp=1.0):
    """Shunt R = R_s at the input, then an amplifier with noise factor f_amp referred to the divided source
    (R_s/2): the terminated source's noise is twice the source's own share, so F = 2 f_amp."""
    return 2 * f_amp


def nf_common_gate(x, gm, rs=50.0):
    """Common-gate stage, drain noise only: F = 1 + x / (g_m R_s); at match (g_m = 1/R_s) F = 1 + x."""
    return 1 + x / (gm * rs)


def nf_noise_cancelling(x, gm2, r2, rs=50.0):
    """CG-CS noise-cancelling LNA at the cancelling condition R1 = g_m2 R2 R_s (CG device noise removed):
    F = 1 + x/(g_m2 R_s) + 1/(g_m2 R2) + 1/(g_m2^2 R2 R_s)."""
    return 1 + x / (gm2 * rs) + 1 / (gm2 * r2) + 1 / (gm2 ** 2 * r2 * rs)


# ---------------------------------------------------------------- inductively degenerated CS
def design_ind_degen(f0, gm, ft, rs=50.0, rg=0.0):
    """Element values for a match to rs at f0: C_gs = g_m/w_T, L_s = (R_s - r_g)/w_T (so that r_g + w_T L_s = R_s),
    L_g = 1/(w0^2 C_gs) - L_s; returns a dict with Q_in = 1/(2 w0 R_s C_gs) and G_m = w_T/(2 w0 R_s)."""
    w0, wt = 2 * math.pi * f0, 2 * math.pi * ft
    cgs = gm / wt
    ls = (rs - rg) / wt
    lg = 1 / (w0 * w0 * cgs) - ls
    return {"gm": gm, "cgs": cgs, "ls": ls, "lg": lg, "q_in": 1 / (2 * w0 * rs * cgs), "gm_eff": wt / (2 * w0 * rs)}


def nf_ind_degen(x, gm, f0, ft, rs=50.0, rg=0.0):
    """Noise factor at resonance, input re-matched to R_s with a series gate loss r_g, drain noise only:
    F = 1 + r_g/R_s + x g_m (R_s + r_g)^2 (w0/w_T)^2 / R_s. With r_g = 0 the drain noise reaches the output
    halved and F = 1 + x g_m R_s (w0/w_T)^2."""
    return 1 + rg / rs + x * gm * (rs + rg) ** 2 * (f0 / ft) ** 2 / rs


def zin_ind_degen(f, gm, cgs, ls, lg, rg=0.0):
    """Input impedance s(L_g + L_s) + 1/(s C_gs) + g_m L_s / C_gs + r_g."""
    s = 2j * math.pi * f
    return rg + s * (lg + ls) + 1 / (s * cgs) + gm * ls / cgs


def solve_ind_degen(f, el, rs=50.0, x=1.0, rg=0.0):
    """Nodal solution of the small-signal model at frequency f. Returns (Z_in, output current per volt of v_s,
    output noise-current density from the drain noise, from the source and from r_g), all in A^2/Hz."""
    s = 2j * math.pi * f
    gm, cgs, ls, lg = el["gm"], el["cgs"], el["ls"], el["lg"]
    zg = rs + rg + s * lg
    zl = s * ls
    zc = 1 / (s * cgs)

    def out(vs, ind):
        # loop current i (through source, Lg, Cgs into the source node); KVL:
        # vs = i zg + i zc + zl (i + gm i zc + ind)  ->  i (zg + zc + zl + zl gm zc) = vs - zl ind
        i = (vs - zl * ind) / (zg + zc + zl + zl * gm * zc)
        return gm * i * zc + ind, i

    io_sig, i_sig = out(1.0, 0.0)
    io_nd, _ = out(0.0, 1.0)
    zin = 1.0 / i_sig - rs
    s_src = abs(io_sig) ** 2 * 4 * K_B * T0 * rs
    s_nd = abs(io_nd) ** 2 * 4 * K_B * T0 * x * gm
    s_rg = abs(io_sig) ** 2 * 4 * K_B * T0 * rg
    return zin, io_sig, s_nd, s_src, s_rg


def iip3_shift_db(q_in):
    """The gate-source voltage is Q_in times the source EMF at resonance, so a device's own V_gs intercept is
    reached at a source amplitude Q_in times smaller: the input-referred IIP3 falls by 20 log10(Q_in)."""
    return 20 * math.log10(q_in)


def design_with_gate_q(f0, gm, ft, q_l, rs=50.0):
    """Re-matched design when L_g has quality factor q_l (series loss r_g = w0 L_g / q_l): solves
    r_g = (w0/q_l)(L_tot - (R_s - r_g)/w_T) for r_g and returns (design dict, r_g)."""
    w0, wt = 2 * math.pi * f0, 2 * math.pi * ft
    l_tot = wt / (gm * w0 * w0)          # 1/(w0^2 C_gs) with C_gs = g_m/w_T
    rg = (w0 / q_l) * (l_tot - rs / wt) / (1 - w0 / (q_l * wt))
    return design_ind_degen(f0, gm, ft, rs, rg), rg
