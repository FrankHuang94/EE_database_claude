"""Lab 18-11: small, self-contained models of hardware-security attacks and defences.

- brute force and rate limits;
- a timing side channel: an early-exit comparison leaks how many leading bytes match, and an attacker recovers a
  secret byte by byte from noisy timings; a constant-time comparison does not leak;
- correlation power analysis (CPA) on the first round of AES: leakage = Hamming weight of S-box(plaintext XOR key)
  plus Gaussian noise; the attacker ranks key guesses by correlation; a first-order Boolean mask defeats it;
- an SRAM-PUF key with repetition-code error correction: bit and key failure probabilities, exact and simulated;
- fault injection: attempts to success with and without redundant checks.
The AES S-box is generated from its definition (inverse in GF(2^8) followed by the affine map), not typed in.
"""
from __future__ import annotations

import math

import numpy as np


# ------------------------------------------------------------------ AES S-box from its definition
def _gmul(a: int, b: int) -> int:
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def _ginv(a: int) -> int:
    if a == 0:
        return 0
    r = 1
    for _ in range(254):          # a^254 = a^-1 in GF(2^8)
        r = _gmul(r, a)
    return r


def aes_sbox() -> np.ndarray:
    s = np.zeros(256, dtype=np.uint8)
    for x in range(256):
        b = _ginv(x)
        y = b
        for k in range(1, 5):
            y ^= ((b << k) | (b >> (8 - k))) & 0xFF
        s[x] = y ^ 0x63
    return s


SBOX = aes_sbox()
HW = np.array([bin(v).count("1") for v in range(256)], dtype=np.int64)


# ------------------------------------------------------------------ brute force
def expected_guesses(bits: float) -> float:
    """Average number of guesses to find a uniformly random secret of `bits` bits: (2^bits + 1)/2."""
    return (2.0 ** bits + 1) / 2


def years(seconds: float) -> float:
    return seconds / (365.25 * 86400)


# ------------------------------------------------------------------ timing side channel
def early_exit_time(secret: bytes, guess: bytes, t_byte: float = 1.0) -> float:
    """Time of a byte-wise comparison that stops at the first mismatch: (matching prefix + 1) byte times."""
    n = 0
    for a, b in zip(secret, guess):
        n += 1
        if a != b:
            break
    return n * t_byte


def constant_time(secret: bytes, guess: bytes, t_byte: float = 1.0) -> float:
    return len(secret) * t_byte


def timing_attack(secret: bytes, compare=early_exit_time, noise: float = 2.0, reps: int = 200, seed: int = 1811):
    """Recover the secret byte by byte: for each position try all 256 values, averaging `reps` noisy timings, and
    keep the slowest; the last byte, which does not change the timing, is found from the accept/reject answer.
    Returns (recovered bytes, number of queries)."""
    rng = np.random.default_rng(seed)
    known = bytearray()
    queries = 0
    for pos in range(len(secret)):
        if pos == len(secret) - 1:
            # the last byte takes the same time whether it matches or not; the accept/reject answer reveals it
            for v in range(256):
                queries += 1
                if bytes(known) + bytes([v]) == secret:
                    known.append(v)
                    break
            else:
                known.append(0)
            break
        best, best_t = 0, -math.inf
        for v in range(256):
            guess = bytes(known) + bytes([v]) + bytes(len(secret) - pos - 1)
            t = compare(secret, guess) + rng.normal(0, noise, reps).mean()
            queries += reps
            if t > best_t:
                best, best_t = v, t
        known.append(best)
    return bytes(known), queries


# ------------------------------------------------------------------ correlation power analysis
def simulate_traces(key_byte: int, n: int, noise_sigma: float, masked: bool = False, seed: int = 1811):
    """Return (plaintext bytes, leakage samples). Leakage is HW(S(p ^ k)) + noise; with masking, the device leaks
    HW(S(p ^ k) ^ m) for a fresh random mask m each trace, which is independent of the key."""
    rng = np.random.default_rng(seed)
    p = rng.integers(0, 256, n)
    v = SBOX[p ^ key_byte].astype(np.int64)
    if masked:
        v = v ^ rng.integers(0, 256, n)
    leak = HW[v] + rng.normal(0, noise_sigma, n)
    return p, leak


def cpa_rank(p: np.ndarray, leak: np.ndarray, true_key: int):
    """Correlate the leakage with HW(S(p ^ k)) for every key guess k. Returns (best guess, rank of the true key
    (0 = best), correlation of the true key)."""
    hyp = HW[SBOX[np.bitwise_xor.outer(np.arange(256), p)]].astype(float)   # 256 x n
    hyp -= hyp.mean(axis=1, keepdims=True)
    l = leak - leak.mean()
    rho = hyp @ l / (np.sqrt((hyp ** 2).sum(axis=1)) * math.sqrt((l ** 2).sum()))
    order = np.argsort(-np.abs(rho))
    return int(order[0]), int(np.where(order == true_key)[0][0]), float(rho[true_key])


def theoretical_rho(noise_sigma: float) -> float:
    """Correlation between HW of a uniform byte (variance 2) and that HW plus noise: sqrt(2 / (2 + sigma^2))."""
    return math.sqrt(2 / (2 + noise_sigma ** 2))


def traces_needed(rho: float, z: float = 4.5) -> float:
    """Rule of thumb: the sample correlation of unrelated data has standard deviation about 1/sqrt(N), so a true
    correlation rho stands z standard deviations clear when N is about (z / rho)^2."""
    return (z / rho) ** 2


# ------------------------------------------------------------------ PUF with a repetition code
def bit_failure(p: float, n: int) -> float:
    """Majority decoding of an n-fold repetition (n odd) fails when more than n/2 of the copies flip."""
    return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1))


def key_failure(p: float, n: int, key_bits: int = 128) -> float:
    return 1 - (1 - bit_failure(p, n)) ** key_bits


def smallest_repetition(p: float, target: float, key_bits: int = 128) -> int:
    n = 1
    while key_failure(p, n, key_bits) > target:
        n += 2
    return n


def simulate_puf(p: float, n: int, key_bits: int = 128, trials: int = 20000, seed: int = 1811) -> float:
    rng = np.random.default_rng(seed)
    flips = rng.random((trials, key_bits, n)) < p
    wrong_bits = flips.sum(axis=2) > n // 2
    return float(np.mean(wrong_bits.any(axis=1)))


# ------------------------------------------------------------------ fault injection
def expected_attempts(p_success: float) -> float:
    return 1 / p_success
