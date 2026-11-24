"""Lab 21-01: S-parameters, conversions, calibration and stability.

- gamma, return_loss_db, vswr, mismatch_loss_db: one-port reflection quantities.
- s_series, s_shunt, s_line: two-port S-parameters of a series impedance, a shunt admittance and a transmission-line
  section, all in a real reference impedance z0.
- z_to_s, s_to_z, abcd_to_s, s_to_abcd, s_to_t, t_to_s: conversions (2x2 numpy arrays, complex).
- shift_planes: move the reference planes of a two-port by electrical lengths theta1, theta2 (radians).
- one_port_cal, one_port_correct: three-term error model from ideal short/open/load standards, and correction.
- stability: Rollett K, |Delta|, mu, MSG and G_max of a two-port; stability_circle: load-plane circle.
- gamma_in: input reflection with a load reflection gamma_l.
"""
from __future__ import annotations

import numpy as np


def gamma(z, z0=50.0):
    return (z - z0) / (z + z0)


def return_loss_db(g):
    return -20 * np.log10(np.abs(g))


def vswr(g):
    m = np.abs(g)
    return (1 + m) / (1 - m)


def mismatch_loss_db(g):
    return -10 * np.log10(1 - np.abs(g) ** 2)


def s_series(z, z0=50.0):
    d = z + 2 * z0
    return np.array([[z / d, 2 * z0 / d], [2 * z0 / d, z / d]], dtype=complex)


def s_shunt(y, z0=50.0):
    d = 2 + y * z0
    return np.array([[-y * z0 / d, 2 / d], [2 / d, -y * z0 / d]], dtype=complex)


def abcd_line(zc, theta):
    """ABCD matrix of a lossless line of characteristic impedance zc and electrical length theta (rad)."""
    return np.array([[np.cos(theta), 1j * zc * np.sin(theta)], [1j * np.sin(theta) / zc, np.cos(theta)]], dtype=complex)


def abcd_to_s(m, z0=50.0):
    a, b, c, d = m[0, 0], m[0, 1], m[1, 0], m[1, 1]
    den = a + b / z0 + c * z0 + d
    return np.array([[(a + b / z0 - c * z0 - d) / den, 2 * (a * d - b * c) / den],
                     [2 / den, (-a + b / z0 - c * z0 + d) / den]], dtype=complex)


def s_to_abcd(s, z0=50.0):
    s11, s12, s21, s22 = s[0, 0], s[0, 1], s[1, 0], s[1, 1]
    den = 2 * s21
    return np.array([[((1 + s11) * (1 - s22) + s12 * s21) / den, z0 * ((1 + s11) * (1 + s22) - s12 * s21) / den],
                     [((1 - s11) * (1 - s22) - s12 * s21) / (z0 * den), ((1 - s11) * (1 + s22) + s12 * s21) / den]],
                    dtype=complex)


def s_line(zc, theta, z0=50.0):
    return abcd_to_s(abcd_line(zc, theta), z0)


def z_to_s(z, z0=50.0):
    i = np.eye(z.shape[0])
    return (z - z0 * i) @ np.linalg.inv(z + z0 * i)


def s_to_z(s, z0=50.0):
    i = np.eye(s.shape[0])
    return z0 * (i + s) @ np.linalg.inv(i - s)


def s_to_t(s):
    """Transfer (T) matrix with [b1, a1] = T [a2, b2]: cascades multiply left to right."""
    s11, s12, s21, s22 = s[0, 0], s[0, 1], s[1, 0], s[1, 1]
    return np.array([[s12 - s11 * s22 / s21, s11 / s21], [-s22 / s21, 1 / s21]], dtype=complex)


def t_to_s(t):
    t11, t12, t21, t22 = t[0, 0], t[0, 1], t[1, 0], t[1, 1]
    return np.array([[t12 / t22, t11 - t12 * t21 / t22], [1 / t22, -t21 / t22]], dtype=complex)


def shift_planes(s, theta1, theta2):
    """S-parameters seen after adding matched lines of electrical length theta1 (port 1) and theta2 (port 2)."""
    p = np.diag([np.exp(-1j * theta1), np.exp(-1j * theta2)])
    return p @ s @ p


def one_port_cal(m_short, m_open, m_load):
    """Three-term error model from raw readings of ideal short (-1), open (+1) and load (0):
    G_m = e00 + e10e01 G / (1 - e11 G). Returns (e00, e11, e10e01)."""
    e00 = m_load
    # G = -1: m_s - e00 = -t/(1 + e11);  G = +1: m_o - e00 = t/(1 - e11)
    a, b = m_short - e00, m_open - e00
    e11 = (a + b) / (b - a)
    t = b * (1 - e11)
    return e00, e11, t


def one_port_correct(m, e00, e11, t):
    return (m - e00) / (t + e11 * (m - e00))


def gamma_in(s, gamma_l):
    return s[0, 0] + s[0, 1] * s[1, 0] * gamma_l / (1 - s[1, 1] * gamma_l)


def stability(s):
    s11, s12, s21, s22 = s[0, 0], s[0, 1], s[1, 0], s[1, 1]
    delta = s11 * s22 - s12 * s21
    k = (1 - abs(s11) ** 2 - abs(s22) ** 2 + abs(delta) ** 2) / (2 * abs(s12 * s21))
    mu = (1 - abs(s11) ** 2) / (abs(s22 - delta * np.conj(s11)) + abs(s12 * s21))
    msg = abs(s21 / s12)
    gmax = msg * (k - np.sqrt(k * k - 1)) if k > 1 else np.nan
    return {"K": k, "delta": abs(delta), "mu": mu, "MSG": msg, "Gmax": gmax}


def stability_circle(s):
    """Load-plane stability circle: centre and radius (|Gamma_in| = 1 boundary)."""
    s11, s12, s21, s22 = s[0, 0], s[0, 1], s[1, 0], s[1, 1]
    delta = s11 * s22 - s12 * s21
    den = abs(s22) ** 2 - abs(delta) ** 2
    return np.conj(s22 - delta * np.conj(s11)) / den, abs(s12 * s21) / abs(den)
