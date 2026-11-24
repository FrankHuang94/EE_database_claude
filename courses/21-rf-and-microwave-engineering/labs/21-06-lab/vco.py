"""Lab 21-06 helpers: LC oscillators, phase noise, tuning, quadrature generation and injection locking.

The oscillator model is a parallel RLC tank (inductance L, capacitance C, loss resistance R_p) driven by a
memoryless negative-resistance device whose current into the tank is i = I0 tanh(v / V0). A bipolar
cross-coupled pair with tail current I_tail has I0 = I_tail / 2 and V0 = 2 V_T (differential quantities).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

K_B = 1.380649e-23  # J/K


# ---------------------------------------------------------------- tank, startup, amplitude
def tank(f0, L, QL, QC=math.inf):
    """Tank capacitance, combined Q and parallel loss resistance for an inductor of quality QL and a capacitor
    (varactor) of quality QC at f0: 1/Q = 1/QL + 1/QC, R_p = Q w0 L, C = 1/(w0^2 L)."""
    w0 = 2 * math.pi * f0
    Q = 1 / (1 / QL + (0 if math.isinf(QC) else 1 / QC))
    return {"C": 1 / (w0 * w0 * L), "Q": Q, "Rp": Q * w0 * L}


def describing_function(V, I0, V0):
    """Fundamental of i = I0 tanh(V cos x / V0), divided by V: the large-signal transconductance G(V)."""
    I1 = (2 / math.pi) * quad(lambda x: I0 * math.tanh(V * math.cos(x) / V0) * math.cos(x), 0, math.pi,
                              limit=200, epsabs=1e-14, epsrel=1e-12)[0]
    return I1 / V


def amplitude_df(Rp, I0, V0):
    """Steady-state amplitude where the describing function balances the tank loss, G(V) = 1/R_p."""
    if I0 / V0 <= 1 / Rp:
        return 0.0
    return brentq(lambda V: describing_function(V, I0, V0) - 1 / Rp, 1e-9 * V0, 10 * I0 * Rp, xtol=1e-15)


def amplitude_hard(Rp, I0):
    """Hard-switching limit: square-wave current of amplitude I0 has fundamental 4 I0 / pi."""
    return 4 * I0 * Rp / math.pi


# ---------------------------------------------------------------- phase noise
def isf_phase_noise(df, S_i, q_max, gamma_rms=1 / math.sqrt(2)):
    """Hajimiri-Lee: L(df) = Gamma_rms^2 S_i / (2 q_max^2 dw^2) for white current noise of one-sided density S_i."""
    dw = 2 * math.pi * df
    return gamma_rms ** 2 * S_i / (2 * q_max ** 2 * dw ** 2)


def leeson(df, f0, Q, Ps, F=1.0, T=300.0, f_corner=0.0):
    """Leeson's form (as in 20-10): (2FkT/Ps)[1 + (f0/(2Q df))^2](1 + f_corner/df)."""
    return (2 * F * K_B * T / Ps) * (1 + (f0 / (2 * Q * df)) ** 2) * (1 + f_corner / df)


def fom(L_dbc, f0, df, P_watt):
    """Oscillator figure of merit, dB: -L + 20 log(f0/df) - 10 log(P / 1 mW)."""
    return -L_dbc + 20 * math.log10(f0 / df) - 10 * math.log10(P_watt / 1e-3)


def control_noise_pn(K_hz_per_v, S_v, df):
    """Phase noise from white voltage noise S_v (V^2/Hz) on the tuning line: L = K^2 S_v / (2 df^2)."""
    return K_hz_per_v ** 2 * S_v / (2 * df ** 2)


def fm_spur_dbc(K_hz_per_v, Vm, fm):
    """Each sideband of a small sinusoidal tone Vm (peak) at fm on the tuning line: 20 log(beta/2), beta = K Vm/fm."""
    return 20 * math.log10(K_hz_per_v * Vm / fm / 2)


def rms_phase_one_pole(L0, fc):
    """rms phase (rad) of L(f) = L0 / (1 + (f/fc)^2) over 0..inf: phi^2 = 2 int L df = pi L0 fc."""
    return math.sqrt(math.pi * L0 * fc)


# ---------------------------------------------------------------- tuning
def freq(L, C):
    return 1 / (2 * math.pi * math.sqrt(L * C))


# ---------------------------------------------------------------- quadrature and image rejection
def irr_db(eps, theta_deg):
    """Image-rejection ratio (21-05) for relative gain error eps and phase error theta."""
    a = 1 + eps
    th = math.radians(theta_deg)
    return 10 * math.log10((1 + 2 * a * math.cos(th) + a * a) / (1 - 2 * a * math.cos(th) + a * a))


def rc_cr(f, R, C):
    """Outputs of an RC-CR pair driven by 1 V: low-pass 1/(1+jwRC) and high-pass jwRC/(1+jwRC)."""
    x = 2j * math.pi * f * R * C
    return 1 / (1 + x), x / (1 + x)


def div2_phase_error_deg(duty):
    """Quadrature phase error of a master-slave divide-by-2 clocked by a 2f clock of duty cycle D: (D - 1/2) 180."""
    return (duty - 0.5) * 180.0


# ---------------------------------------------------------------- injection locking
def lock_range(f0, Q, ratio):
    """One-sided lock range (Hz) for injected/oscillator current ratio: (f0/2Q) r / sqrt(1 - r^2)."""
    return f0 / (2 * Q) * ratio / math.sqrt(1 - ratio * ratio)


def beat(df, fL):
    """Adler: outside the lock range the phase slips at sqrt(df^2 - fL^2)."""
    return math.sqrt(df * df - fL * fL)


# ---------------------------------------------------------------- normalized time-domain oscillator (w0 = 1)
def _rhs(Q, I0, V0, Iinj=0.0, winj=1.0):
    def f(t, y):
        v, iL = y
        return [-v / Q - iL + I0 * math.tanh(v / V0) + Iinj * math.cos(winj * t), v]
    return f


def settle(Q, I0, V0, cycles=200):
    """Run the normalized oscillator (L = C = 1, R_p = Q) to steady state; return the final state."""
    sol = solve_ivp(_rhs(Q, I0, V0), (0, 2 * math.pi * cycles), [1e-3, 0.0], method="DOP853", rtol=1e-10,
                    atol=1e-12)
    return sol.y[:, -1]


def _phase(y):
    # state (v, iL) with v = A cos(t + p), iL = A sin(t + p) for the ideal tank: phase = atan2(iL, v)
    return math.atan2(y[1], y[0])


def isf(Q, I0, V0, thetas, dq=1e-3, cycles=40):
    """Numerical impulse sensitivity function. For each oscillation phase theta (radians, with v = A cos theta at
    the moment of injection), inject a charge dq q_max (q_max = C A), let the amplitude settle for `cycles`
    periods, and return the resulting phase shift divided by dq: Gamma(theta)."""
    f = _rhs(Q, I0, V0)
    opts = dict(method="DOP853", rtol=1e-11, atol=1e-13)
    y = settle(Q, I0, V0)
    A = math.hypot(*y)
    p0 = _phase(y)
    T = 2 * math.pi * cycles
    out = []
    for theta in np.atleast_1d(thetas):
        adv = (theta - p0) % (2 * math.pi)
        y1 = solve_ivp(f, (0, adv), y, **opts).y[:, -1] if adv > 0 else y.copy()
        ref = solve_ivp(f, (0, T), y1, **opts).y[:, -1]
        kick = y1.copy()
        kick[0] += dq * A  # C = 1, so a charge dq * q_max raises v by dq * A
        per = solve_ivp(f, (0, T), kick, **opts).y[:, -1]
        dphi = (_phase(per) - _phase(ref) + math.pi) % (2 * math.pi) - math.pi
        out.append(dphi / dq)
    return np.array(out)


def free_running_shift(Q, I0, V0, cycles=400, skip=200):
    """Fractional frequency offset of the free-running oscillator from 1/sqrt(LC) (Groszkowski shift)."""
    return injection_beat(Q, I0, V0, 0.0, 0.0, cycles=cycles, skip=skip)[0]


def groszkowski_shift(Rp, C, w0, I0, V0, V, nmax=41):
    """Predicted fractional frequency shift -1/2 sum (n^2 - 1) h_n^2, with h_n the n-th harmonic of the tank
    voltage relative to the fundamental: h_n = I_n |Z(n w0)| / V for the tanh current at amplitude V."""
    s = 0.0
    for n in range(3, nmax + 1, 2):
        In = (2 / math.pi) * quad(lambda x: I0 * math.tanh(V * math.cos(x) / V0) * math.cos(n * x), 0, math.pi,
                                  limit=400)[0]
        Zn = 1 / abs(1 / Rp + 1j * w0 * C * (n - 1 / n))
        s += (n * n - 1) * (In * Zn / V) ** 2
    return -s / 2


def injection_beat(Q, I0, V0, Iinj, dw, cycles=900, skip=150):
    """Mean phase-slip rate (rad per unit time) of the oscillator relative to an injection at 1 + dw."""
    winj = 1 + dw
    t_end = 2 * math.pi * cycles
    ts = np.linspace(2 * math.pi * skip, t_end, 40 * (cycles - skip))
    sol = solve_ivp(_rhs(Q, I0, V0, Iinj, winj), (0, t_end), [1e-2, 0.0], method="DOP853", rtol=1e-10,
                    atol=1e-12, t_eval=ts)
    ph = np.unwrap(np.arctan2(sol.y[1], sol.y[0]))
    psi = ph - winj * ts
    return (psi[-1] - psi[0]) / (ts[-1] - ts[0]), ts, psi
