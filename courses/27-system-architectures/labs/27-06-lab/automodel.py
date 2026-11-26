"""Models for Chapter 27-06 (Automotive E/E architecture and ADAS compute).

Each function is a first-order engineering model from the chapter. Units are in
every docstring. Parameter values used in the chapter are illustrative
assumptions unless a source is cited there.
"""
import math


# --- CAN ------------------------------------------------------------------------

def can_frame_bits(n_bytes, worst_case_stuffing=True):
    """Bits on the wire for a classic CAN data frame with an 11-bit identifier and
    n_bytes of data, including the 3-bit interframe space. The 34 + 8n bits from
    start-of-frame to the end of the CRC are subject to bit stuffing (worst case one
    stuff bit per 4 bits after the first); 13 bits (CRC delimiter, ACK, EOF, IFS) are not."""
    g = 34
    stuffed_region = g + 8 * n_bytes
    stuff = (stuffed_region - 1) // 4 if worst_case_stuffing else 0
    return stuffed_region + 13 + stuff


def can_frame_time_us(n_bytes, bitrate_kbps, worst_case_stuffing=True):
    """Transmission time (us) of one classic CAN frame."""
    return can_frame_bits(n_bytes, worst_case_stuffing) / (bitrate_kbps * 1e3) * 1e6


def bus_load(messages, bitrate_kbps):
    """Fraction of bus time used by [(n_bytes, period_ms), ...]."""
    return sum(can_frame_time_us(n, bitrate_kbps) / (p * 1e3) for n, p in messages)


def can_response_time_ms(index, messages, bitrate_kbps, max_iter=1000):
    """Worst-case response time (ms) of message `index` in a priority-ordered list
    [(n_bytes, period_ms), ...] (index 0 = highest priority), by the classic
    fixed-point iteration R = B + C + sum_{j<i} ceil((R - C + tau_bit)/T_j) C_j,
    with blocking B = longest lower-priority frame."""
    c = [can_frame_time_us(n, bitrate_kbps) / 1e3 for n, _ in messages]
    t = [p for _, p in messages]
    tau = 1.0 / (bitrate_kbps * 1e3) * 1e3  # ms per bit
    lower = c[index + 1:]
    b = max(lower) if lower else 0.0
    w = b
    for _ in range(max_iter):
        w_new = b + sum(math.ceil((w + tau) / t[j]) * c[j] for j in range(index))
        if abs(w_new - w) < 1e-12:
            break
        w = w_new
    return w + c[index]


# --- Sensors, compute and power -----------------------------------------------------

def camera_gbps(megapixels, fps, bits_per_pixel):
    """Raw camera data rate (Gb/s)."""
    return megapixels * 1e6 * fps * bits_per_pixel / 1e9


def tops_needed(cameras, fps, gops_per_frame, utilization):
    """Peak TOPS needed to run a network of gops_per_frame on every camera frame."""
    return cameras * fps * gops_per_frame * 1e9 / utilization / 1e12


def range_loss_fraction(p_compute_w, wh_per_km, speed_kmh):
    """Fraction of driving range lost to a constant compute load: Pc/(Pc + Pdrive),
    with Pdrive = consumption (Wh/km) * speed (km/h)."""
    p_drive = wh_per_km * speed_kmh
    return p_compute_w / (p_compute_w + p_drive)


def reaction_distance_m(speed_kmh, latency_s):
    """Distance (m) travelled during a latency at constant speed."""
    return speed_kmh / 3.6 * latency_s


def stopping_distance_m(speed_kmh, latency_s, decel_ms2):
    """Reaction distance plus braking distance v^2/(2a)."""
    v = speed_kmh / 3.6
    return v * latency_s + v * v / (2.0 * decel_ms2)


# --- Wiring ------------------------------------------------------------------------

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def star_length(endpoints, hub):
    """Total wire length (m) when every endpoint is wired to one hub."""
    return sum(manhattan(e, hub) for e in endpoints)


def zonal_length(endpoints, zones, central):
    """Total length (m) when each endpoint is wired to its nearest zone controller and
    each zone has one backbone link to the central computer.
    Returns (endpoint wiring, backbone, total)."""
    local = sum(min(manhattan(e, z) for z in zones) for e in endpoints)
    backbone = sum(manhattan(z, central) for z in zones)
    return local, backbone, local + backbone


# --- Safety and fleet -------------------------------------------------------------

def residual_fit(lambda_fit, diagnostic_coverage):
    """Residual (undetected) failure rate in FIT: lambda * (1 - DC)."""
    return lambda_fit * (1.0 - diagnostic_coverage)


def fleet_events_per_year(vehicles, hours_per_day, fit):
    """Expected events per year across a fleet at a failure rate in FIT (per 1e9 h)."""
    return vehicles * hours_per_day * 365.0 * fit * 1e-9


def ota_seconds(size_gb, mbps):
    """Download time (s) of an update of size_gb at an effective rate in Mb/s."""
    return size_gb * 8e3 / mbps
