"""Lab 20-06: data-converter metrics on behavioral ADC models.

Conventions (chapter 20-06): an N-bit ADC has full-scale range V_FS and LSB Delta = V_FS/2^N; code k (0..2^N-1) is
output for T[k] <= v < T[k+1], where T[1..2^N-1] are the code transition levels (T[k] ideally (k - 1/2) Delta above
the bottom of the range for a mid-tread converter whose first transition is half an LSB up). DNL[k] = (T[k+1] - T[k])/
Delta_avg - 1 and INL[k] = (T[k] - T_line[k])/Delta_avg, with Delta_avg and the line taken from the end points
(endpoint INL) or a least-squares fit (best-fit INL).

The SAR model: a binary-weighted capacitive DAC whose bit capacitors are sums of unit capacitors with independent
relative errors (seeded), so the transition levels follow from the actual weights; optional input-referred Gaussian
noise and a static polynomial nonlinearity in front of the quantizer. All quantities SI.
"""
from __future__ import annotations

import math

import numpy as np

K_B = 1.380649e-23


def ideal_snr_db(n_bits: int) -> float:
    return 10 * math.log10(1.5 * 4 ** n_bits)


def enob(sinad_db: float) -> float:
    return (sinad_db - 1.76) / 6.02


def sar_weights(n_bits: int, sigma_unit: float, rng: np.random.Generator) -> np.ndarray:
    """Actual bit weights (in LSB) of a binary-weighted DAC built from unit capacitors with relative sigma."""
    w = []
    for b in range(n_bits):
        units = 2 ** b
        w.append(units + sigma_unit * math.sqrt(units) * rng.standard_normal())
    return np.array(w)


def sar_code(v: np.ndarray, w: np.ndarray, vfs: float) -> np.ndarray:
    """Output codes of a SAR (binary search) with bit weights w (in LSB) for inputs v (volts above the bottom of the
    range). Each trial code c is kept if v >= (DAC(c) * scale - 1/2) LSB, where scale normalizes the total weight to
    2^N - 1 so that an ideal converter has transitions at (k - 1/2) Delta."""
    n = len(w)
    lsb = vfs / 2 ** n
    scale = (2 ** n - 1) / w.sum()
    v = np.asarray(v, dtype=float)
    c = np.zeros(v.shape, dtype=np.int64)
    for b in range(n - 1, -1, -1):
        trial = c | (1 << b)
        bits = (trial[..., None] >> np.arange(n)) & 1
        thr = ((bits @ w) * scale - 0.5) * lsb
        c = np.where(v >= thr, trial, c)
    return c


def sar_transitions(w: np.ndarray, vfs: float, iters: int = 60) -> np.ndarray:
    """Transition levels T[1..2^N-1] of the SAR (its transfer is monotonic): T[k] = inf{v : code(v) >= k},
    found by vectorized bisection. Missing codes give coincident transitions (zero code width)."""
    n = len(w)
    lsb = vfs / 2 ** n
    k = np.arange(1, 2 ** n)
    lo = np.full(k.shape, -2 * lsb)
    hi = np.full(k.shape, vfs + 2 * lsb)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        up = sar_code(mid, w, vfs) >= k
        hi = np.where(up, mid, hi)
        lo = np.where(up, lo, mid)
    return hi


def dnl_inl(t: np.ndarray, method: str = "endpoint") -> tuple[np.ndarray, np.ndarray]:
    """DNL for codes 1..2^N-2 and INL for transitions 1..2^N-1, in LSB."""
    k = np.arange(1, len(t) + 1)
    if method == "endpoint":
        d_avg = (t[-1] - t[0]) / (len(t) - 1)
        line = t[0] + (k - 1) * d_avg
    else:
        a, b = np.polyfit(k, t, 1)
        d_avg, line = a, a * k + b
    dnl = np.diff(t) / d_avg - 1
    inl = (t - line) / d_avg
    return dnl, inl


def quantize(v: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Codes for inputs v (volts above the bottom of the range) given transition levels t."""
    return np.searchsorted(t, v, side="right")


def histogram_transitions(codes: np.ndarray, n_codes: int, amp: float, offset: float) -> np.ndarray:
    """Sine-wave code-density test: transition levels from the cumulative histogram,
    T[k] = offset - amp cos(pi C[k-1]/N_total), C the cumulative count of codes below k."""
    h = np.bincount(codes, minlength=n_codes).astype(float)
    c = np.cumsum(h)[:-1]
    return offset - amp * np.cos(math.pi * c / codes.size)


def coherent_frequency(fs: float, n_fft: int, f_target: float) -> tuple[float, int]:
    """Closest coherent input frequency f = M fs/N with M odd (hence co-prime with a power-of-two N)."""
    m = int(round(f_target * n_fft / fs))
    if m % 2 == 0:
        m += 1
    return m * fs / n_fft, m


def spectrum_metrics(x: np.ndarray, m: int, n_harm: int = 9, full_scale_amp: float | None = None) -> dict:
    """SNR, THD, SINAD, SFDR (dBc) and ENOB of a coherently sampled record (rectangular window).

    m is the input's FFT bin; harmonics are folded into the first Nyquist zone. If full_scale_amp is given,
    'enob_fs' corrects the SINAD to a full-scale input (adds 20 log10(full_scale_amp/amplitude))."""
    n = x.size
    s = np.abs(np.fft.rfft(x - x.mean())) ** 2 / n ** 2 * 2
    s[0] = 0.0
    if n % 2 == 0:
        s[-1] /= 2          # the Nyquist bin has no mirror image: count it once
    p_sig = s[m]
    harm_bins = []
    for h in range(2, n_harm + 1):
        b = (h * m) % n
        b = n - b if b > n // 2 else b
        if b not in harm_bins and b not in (0, m):
            harm_bins.append(b)
    p_harm = sum(s[b] for b in harm_bins)
    p_noise = s.sum() - p_sig - p_harm
    spur = max(np.delete(s, [0, m]))
    amp = math.sqrt(2 * p_sig)
    out = {"snr": 10 * math.log10(p_sig / p_noise), "thd": 10 * math.log10(p_harm / p_sig),
           "sinad": 10 * math.log10(p_sig / (p_noise + p_harm)), "sfdr": 10 * math.log10(p_sig / spur),
           "amp": amp}
    out["enob"] = enob(out["sinad"])
    if full_scale_amp:
        out["enob_fs"] = enob(out["sinad"] + 20 * math.log10(full_scale_amp / amp))
    return out


def fom_walden(power: float, fs: float, enob_bits: float) -> float:
    return power / (2 ** enob_bits * fs)


def fom_schreier(sndr_db: float, bw: float, power: float) -> float:
    return sndr_db + 10 * math.log10(bw / power)


def thermal_limit_fom_s(temp: float = 300.0) -> float:
    """Schreier FoM of a Nyquist sampler at the 8 kT SNR energy bound: 10 log10(1/(16 kT))."""
    return 10 * math.log10(1 / (16 * K_B * temp))
