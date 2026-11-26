"""Smartwatch energy models for Chapter 27-03 (Wearables I: The Smartwatch).

Each function is a first-order engineering model from the chapter. Units are
stated in every docstring; powers are in milliwatts unless the name says
otherwise. Parameter values used in the chapter are illustrative assumptions,
not measurements of any product.
"""
import math


# --- Battery and daily budget ------------------------------------------------

def battery_energy_mwh(capacity_mah, v_nom):
    """Stored energy in mWh of a cell with capacity (mAh) and nominal voltage (V)."""
    return capacity_mah * v_nom


def daily_energy_mwh(items):
    """Rail energy per day (mWh) from items [(name, power_mW, hours_per_day), ...]."""
    return sum(p * h for _, p, h in items)


def battery_life_h(e_batt_mwh, e_day_rail_mwh, eta=1.0, usable=1.0):
    """Hours of life when the rails draw e_day_rail_mwh per 24 h through a
    converter of efficiency eta and a fraction `usable` of the cell is available."""
    return 24.0 * usable * e_batt_mwh * eta / e_day_rail_mwh


# --- Display -----------------------------------------------------------------

def oled_emission_mw(lum_nits, area_m2, apl, efficacy_lm_per_w):
    """Electrical power (mW) to emit luminance lum_nits (cd/m^2) from a
    Lambertian panel of area area_m2 at average pixel level apl (0..1) with a
    panel luminous efficacy in lm/W. Luminous flux = pi * L * A * apl."""
    flux_lm = math.pi * lum_nits * area_m2 * apl
    return 1e3 * flux_lm / efficacy_lm_per_w


def display_power_mw(lum_nits, area_m2, apl, efficacy_lm_per_w,
                     p0_mw, e_frame_mj, refresh_hz):
    """Emission power plus driver power p0 + e_frame * refresh (mW)."""
    return (oled_emission_mw(lum_nits, area_m2, apl, efficacy_lm_per_w)
            + p0_mw + e_frame_mj * refresh_hz)


def pixel_hold_time_s(c_store_f, dv_allowed_v, i_leak_a):
    """Time (s) for a pixel storage capacitor to droop by dv_allowed through a
    constant leakage current: t = C * dV / I."""
    return c_store_f * dv_allowed_v / i_leak_a


# --- Sensor path: application processor versus always-on hub ----------------

def ap_batched_power_mw(fs_hz, e_sample_mj, e_wake_mj, n_batch):
    """Average power (mW) when the application processor wakes once per batch
    of n_batch samples and spends e_sample_mj per sample: fs*Es + fs*Ew/N."""
    return fs_hz * e_sample_mj + fs_hz * e_wake_mj / n_batch


def hub_power_mw(p_hub_mw, fs_hz, e_hub_sample_mj, event_rate_hz, e_wake_mj):
    """Average power (mW) of an always-on hub that processes every sample and
    wakes the application processor only for events: Ph + fs*Eh + r*Ew."""
    return p_hub_mw + fs_hz * e_hub_sample_mj + event_rate_hz * e_wake_mj


def batch_for_power(fs_hz, e_sample_mj, e_wake_mj, p_target_mw):
    """Smallest batch size N for which ap_batched_power_mw <= p_target_mw
    (math.inf if the per-sample floor fs*Es already exceeds the target)."""
    floor = fs_hz * e_sample_mj
    if p_target_mw <= floor:
        return math.inf
    return math.ceil(fs_hz * e_wake_mj / (p_target_mw - floor))


# --- Bluetooth LE link -------------------------------------------------------

def ble_airtime_us(payload_octets, phy_mbps=1, encrypted=False):
    """Air time (us) of an uncoded LE packet: preamble (1 octet on 1M, 2 on 2M),
    access address 4, header 2, payload, MIC 4 if encrypted and payload > 0, CRC 3."""
    pre = 1 if phy_mbps == 1 else 2
    mic = 4 if (encrypted and payload_octets > 0) else 0
    octets = pre + 4 + 2 + payload_octets + mic + 3
    return 8 * octets / phy_mbps


def ble_event_charge_uc(i_pre_ma, t_pre_us, i_rx_ma, t_rx_us, t_ifs_us,
                        i_tx_ma, t_tx_us):
    """Charge (uC) of one peripheral connection event with no data: wake-up
    overhead, receive the central's packet, turn around (counted at the
    receive current), transmit the reply. mA * us = nC, so divide by 1000."""
    return (i_pre_ma * t_pre_us + i_rx_ma * (t_rx_us + t_ifs_us)
            + i_tx_ma * t_tx_us) / 1000.0


def ble_avg_current_ua(q_event_uc, interval_s, i_sleep_ua, i_rx_ma=0.0,
                       sca_total_ppm=0.0, latency=0):
    """Average current (uA) of a peripheral that wakes every (1+latency)
    intervals. Window widening keeps the receiver on early for
    sca_total_ppm * 1e-6 * T_wake, which adds i_rx * sca * 1e-6 (a constant)."""
    t_wake = interval_s * (1 + latency)
    widening_ua = 1e3 * i_rx_ma * sca_total_ppm * 1e-6
    return i_sleep_ua + widening_ua + q_event_uc / t_wake


# --- Power conversion at light load and power gating ------------------------

def buck_input_uw(v_out, i_out_ua, eta_core, iq_ua, v_in):
    """Input power (uW) of a buck at light load: Po/eta_core + Iq*Vin."""
    return v_out * i_out_ua / eta_core + iq_ua * v_in


def ldo_input_uw(i_out_ua, iq_ua, v_in):
    """Input power (uW) of an LDO: Vin*(Io + Iq)."""
    return v_in * (i_out_ua + iq_ua)


def buck_ldo_crossover_ua(v_in, v_out, eta_core, iq_buck_ua, iq_ldo_ua):
    """Load current (uA) below which the LDO draws less input power than the buck."""
    return v_in * (iq_buck_ua - iq_ldo_ua) / (v_in - v_out / eta_core)


def gating_breakeven_s(e_overhead_uj, p_retain_uw, p_off_uw):
    """Idle time (s) beyond which switching a block off saves energy."""
    return e_overhead_uj / (p_retain_uw - p_off_uw)


# --- Battery cell geometry and terminal voltage ------------------------------

def active_fraction(dims_mm, overhead_mm):
    """Fraction of a box cell's volume that is active stack, given its outer
    dimensions and the total non-active thickness along each axis."""
    f = 1.0
    for a, t in zip(dims_mm, overhead_mm):
        f *= (a - t) / a
    return f


def terminal_voltage(v_oc, i_a, r_ohm):
    """Terminal voltage (V) of a cell with open-circuit voltage v_oc and
    internal resistance r_ohm delivering i_a."""
    return v_oc - i_a * r_ohm


def max_current_a(v_oc, v_min, r_ohm):
    """Largest current (A) that keeps the terminal voltage at or above v_min."""
    return (v_oc - v_min) / r_ohm


# --- Paging and harvesting ---------------------------------------------------

def paging_avg_current_ua(i_sleep_ua, q_page_uc, cycle_s):
    """Average current (uA) of a modem that wakes once per paging cycle."""
    return i_sleep_ua + q_page_uc / cycle_s


def harvest_mwh_per_day(irradiance_w_m2, area_cm2, efficiency, hours):
    """Energy (mWh) a photovoltaic area harvests in `hours` at a given irradiance."""
    return irradiance_w_m2 * area_cm2 * 1e-4 * efficiency * hours * 1e3
