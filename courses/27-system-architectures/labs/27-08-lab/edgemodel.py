"""Models for Chapter 27-08 (Edge AI and IoT).

Each function is a first-order engineering model from the chapter. Units are in
every docstring. Parameter values used in the chapter are illustrative
assumptions unless a source is cited there.
"""
import math

SECONDS_PER_DAY = 86400.0


# --- A neural network on a microcontroller -------------------------------------------

def conv_macs(h_out, w_out, c_out, k_h, k_w, c_in):
    """Multiply-accumulates of a standard convolution layer."""
    return h_out * w_out * c_out * k_h * k_w * c_in


def depthwise_macs(h, w, c, k):
    """MACs of a k x k depthwise convolution on an h x w x c tensor (one filter per channel)."""
    return h * w * c * k * k


def pointwise_macs(h, w, c_in, c_out):
    """MACs of a 1 x 1 (pointwise) convolution."""
    return h * w * c_in * c_out


def kws_network(n_blocks=4, c=64, h=25, w=5, n_classes=12, k1=(10, 4)):
    """Layer list [(name, macs, weights, biases)] of the chapter's depthwise-separable
    keyword spotter: a 10x4 stride-2 convolution to h x w x c, n_blocks of (3x3
    depthwise + 1x1 pointwise), global average pooling and a fully connected layer."""
    layers = [("conv", conv_macs(h, w, c, k1[0], k1[1], 1), k1[0] * k1[1] * c, c)]
    for i in range(n_blocks):
        layers.append((f"dw{i + 1}", depthwise_macs(h, w, c, 3), 9 * c, c))
        layers.append((f"pw{i + 1}", pointwise_macs(h, w, c, c), c * c, c))
    layers.append(("fc", c * n_classes, c * n_classes, n_classes))
    return layers


def inference_time_s(macs, macs_per_cycle, f_hz, utilization=1.0):
    """Inference time (s) at a sustained rate of macs_per_cycle x utilization MACs per cycle."""
    return macs / (macs_per_cycle * utilization * f_hz)


def average_power_w(rate_hz, energy_per_event_j, p_continuous_w):
    """Average power (W) of a periodic event plus continuously drawn power."""
    return rate_hz * energy_per_event_j + p_continuous_w


def life_days(energy_j, p_avg_w):
    """Days a stored energy lasts at an average power."""
    return energy_j / p_avg_w / SECONDS_PER_DAY


# --- LoRa ------------------------------------------------------------------------------

def lora_symbol_s(sf, bw_hz):
    """LoRa symbol time 2^SF / BW (s)."""
    return 2 ** sf / bw_hz


def lora_payload_symbols(pl, sf, cr=1, crc=1, ih=0, de=0):
    """Payload symbols from the Semtech SX1276 data sheet: 8 + max(ceil((8PL - 4SF + 28 +
    16CRC - 20IH)/(4(SF - 2DE))) (CR + 4), 0); CR = 1 for coding rate 4/5."""
    n = math.ceil((8 * pl - 4 * sf + 28 + 16 * crc - 20 * ih) / (4 * (sf - 2 * de)))
    return 8 + max(n * (cr + 4), 0)


def lora_time_on_air_s(pl, sf, bw_hz=125e3, cr=1, n_preamble=8, crc=1, ih=0, de=None):
    """Packet time on air (s); low-data-rate optimization (DE = 1) is switched on
    automatically when the symbol time exceeds 16 ms, as the data sheet mandates."""
    ts = lora_symbol_s(sf, bw_hz)
    if de is None:
        de = 1 if ts > 16e-3 else 0
    return (n_preamble + 4.25) * ts + lora_payload_symbols(pl, sf, cr, crc, ih, de) * ts


def max_messages(airtime_budget_s, toa_s):
    """Whole messages that fit in an airtime budget (s)."""
    return math.floor(airtime_budget_s / toa_s)


# --- Energy harvesting -----------------------------------------------------------------

def pv_power_w(lux, area_m2, efficacy_lm_per_w, eta_pv, eta_conv):
    """Electrical power (W) from a photovoltaic cell under illuminance `lux` (lm/m^2),
    converting to irradiance with a luminous efficacy of radiation (lm/W)."""
    return lux / efficacy_lm_per_w * area_m2 * eta_pv * eta_conv


def capacitor_for_energy_f(energy_j, v_max, v_min):
    """Capacitance (F) that delivers energy_j between v_max and v_min: 2E/(Vmax^2 - Vmin^2)."""
    return 2.0 * energy_j / (v_max ** 2 - v_min ** 2)


# --- Security --------------------------------------------------------------------------

def hash_time_s(n_bytes, cycles_per_byte, f_hz):
    """Time (s) to hash an image at a cost in cycles per byte."""
    return n_bytes * cycles_per_byte / f_hz
