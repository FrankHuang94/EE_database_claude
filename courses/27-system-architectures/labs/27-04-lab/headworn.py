"""Models for Chapter 27-04 (Wearables II: earbuds and smart glasses / XR).

Each function is a first-order engineering model from the chapter. Units are in
every docstring. Parameter values used in the chapter are illustrative
assumptions, not measurements of any product.
"""
import math


# --- Earbud audio chain -----------------------------------------------------

def speaker_power_mw(spl_db, sensitivity_db_per_mw):
    """Electrical power (mW) a driver of the given sensitivity (dB SPL at 1 mW)
    needs to reach spl_db: P = 10**((SPL - S)/10) mW."""
    return 10.0 ** ((spl_db - sensitivity_db_per_mw) / 10.0)


def amp_efficiency(p_out_mw, p_quiescent_mw, eta_switching):
    """Efficiency of a class-D stage: P_out / (P_out/eta + P_quiescent)."""
    return p_out_mw / (p_out_mw / eta_switching + p_quiescent_mw)


def anc_residual(f_hz, delay_s, gain_error=0.0):
    """Magnitude of the residual |1 - (1+e) exp(-j 2 pi f tau)| after cancelling a
    tone with an anti-noise copy delayed by tau and with fractional gain error e."""
    phi = 2.0 * math.pi * f_hz * delay_s
    g = 1.0 + gain_error
    return math.sqrt((1.0 - g * math.cos(phi)) ** 2 + (g * math.sin(phi)) ** 2)


def anc_attenuation_db(f_hz, delay_s, gain_error=0.0):
    """Noise reduction in dB (positive = quieter): -20 log10(residual)."""
    return -20.0 * math.log10(anc_residual(f_hz, delay_s, gain_error))


def anc_max_delay_s(f_hz, attenuation_db):
    """Largest delay (s) that still gives attenuation_db at f_hz with perfect gain:
    2 sin(pi f tau) = 10**(-A/20)."""
    r = 10.0 ** (-attenuation_db / 20.0)
    return math.asin(r / 2.0) / (math.pi * f_hz)


# --- LE Audio stream ----------------------------------------------------------

def lc3_frame_octets(bitrate_kbps, frame_ms):
    """Octets per LC3 frame: bitrate * frame duration / 8."""
    return bitrate_kbps * 1e3 * frame_ms * 1e-3 / 8.0


def le_airtime_us(payload_octets, phy_mbps=2, encrypted=True):
    """Air time (us) of an uncoded LE packet (preamble 1 or 2 octets, access
    address 4, header 2, payload, MIC 4 if encrypted and payload > 0, CRC 3)."""
    pre = 1 if phy_mbps == 1 else 2
    mic = 4 if (encrypted and payload_octets > 0) else 0
    return 8.0 * (pre + 4 + 2 + payload_octets + mic + 3) / phy_mbps


def stream_current_ua(t_rx_us, t_ack_us, t_ifs_us, t_pre_us, i_rx_ma, i_tx_ma, i_pre_ma,
                      interval_ms, i_sleep_ua=0.0):
    """Average radio current (uA) of a receiver that, every interval, wakes, receives
    one packet, turns around (at the receive current) and acknowledges."""
    q_nc = i_pre_ma * t_pre_us + i_rx_ma * (t_rx_us + t_ifs_us) + i_tx_ma * t_ack_us
    return i_sleep_ua + q_nc / (interval_ms * 1e3) * 1e3


# --- Batteries ----------------------------------------------------------------

def life_h(e_batt_mwh, p_rail_mw, eta=1.0):
    """Hours a cell of e_batt_mwh lasts at a rail power p_rail_mw through efficiency eta."""
    return e_batt_mwh * eta / p_rail_mw


def case_recharges(e_case_mwh, eta_transfer, e_bud_mwh, n_buds=2):
    """Full recharges of n_buds earbuds a charging case can deliver."""
    return e_case_mwh * eta_transfer / (n_buds * e_bud_mwh)


# --- Head-worn thermal and display --------------------------------------------

def surface_power_w(h_w_m2k, area_m2, delta_t_k):
    """Heat (W) a surface sheds at heat-transfer coefficient h over area A at rise dT."""
    return h_w_m2k * area_m2 * delta_t_k


def waveguide_display_mw(lum_nits, nits_per_lumen, apl, efficacy_lm_per_w):
    """Electrical power (mW) of a projector feeding a waveguide that delivers
    nits_per_lumen of eye-side luminance per lumen injected, at average pixel level apl."""
    flux_lm = lum_nits / nits_per_lumen * apl
    return 1e3 * flux_lm / efficacy_lm_per_w


# --- XR latency, rendering and offload -----------------------------------------

def angular_error_deg(omega_deg_s, latency_ms):
    """Angular registration error (deg) of a head turning at omega for latency_ms."""
    return omega_deg_s * latency_ms * 1e-3


def pixel_rate(width, height, eyes, refresh_hz):
    """Pixels per second the displays must be fed."""
    return width * height * eyes * refresh_hz


def foveated_fraction(fovea_deg, fov_deg, periphery_scale):
    """Fraction of full-resolution shading work with a square fovea at full
    resolution and the periphery at a linear scale factor (0.5 = half resolution)."""
    f = (fovea_deg / fov_deg) ** 2
    return f + (1.0 - f) * periphery_scale ** 2


def stream_power_w(bitrate_mbps, energy_nj_per_bit, p_decode_w):
    """Power (W) to receive a video stream and decode it: bitrate * E/bit + decoder."""
    return bitrate_mbps * 1e6 * energy_nj_per_bit * 1e-9 + p_decode_w
