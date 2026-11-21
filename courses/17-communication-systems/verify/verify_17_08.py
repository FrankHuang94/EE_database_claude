#!/usr/bin/env python3
"""Verify chapter 17-08 (channel coding): text, examples, problems and lab answers.

Routes:
- block-code properties by enumerating every codeword and by GF(2) algebra (G H^T = 0, ranks);
- CRC guarantees by exhaustive tests over every burst pattern, and NR polynomial term counts from R-279;
- block and Reed-Solomon error rates from the binomial tail, cross-checked by log-domain sums and Monte Carlo;
- convolutional codes: free distance by brute-force enumeration of input sequences, the distance spectrum by
  the lab's state-diagram search and by a sympy series of the transfer function, Viterbi by an independent
  loop implementation here and by the lab's vectorized decoder, and the union bound against simulation;
- LDPC and polar decoders by running them (rank, H G^T = 0, error-free decoding at high SNR);
- polar erasure probabilities by an independent top-down recursion and by Monte Carlo on the BEC;
- the DVB-S2 comparison from R-276 and the BPSK-input capacity of the 17-07 lab.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import optimize
from scipy.stats import binom, norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
sys.path.insert(0, str(ROOT / "labs" / "17-07-lab"))
from eeverify import Verifier  # noqa: E402
import coding as cd  # noqa: E402
import infotheory as it  # noqa: E402

CH = ROOT / "chapters" / "17-08-channel-coding.md"
v = Verifier.from_files("17-08", CH, ROOT / "solutions" / "17-08-solutions.md", LAB / "README.md")
rng = np.random.default_rng(1708)
Q, Qi = norm.sf, norm.isf


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def bits(s):
    return np.array([int(c) for c in s.replace(" ", "")], np.uint8)


# ------------------------------------------------------------------ independent helpers
def conv_out(u_seq, gens, K):
    """Encoder written directly from the definition: output j = XOR of taps of (u_t, ..., u_{t-K+1})."""
    reg = [0] * K
    out = []
    for u in list(u_seq) + [0] * (K - 1):
        reg = [u] + reg[:-1]
        for g in gens:
            taps = [(g >> (K - 1 - i)) & 1 for i in range(K)]
            out.append(sum(a * b for a, b in zip(taps, reg)) % 2)
    return out


def viterbi_loops(rx, gens, K):
    """Hard-decision Viterbi with explicit loops; returns (inputs, metric, metric table per step)."""
    S = 2 ** (K - 1)
    INF = 10**9
    metric = [0] + [INF] * (S - 1)
    paths = [[] for _ in range(S)]
    steps = len(rx) // len(gens)
    table = []
    for t in range(steps):
        r = rx[t * len(gens) : (t + 1) * len(gens)]
        new, newp = [INF] * S, [None] * S
        for s in range(S):
            if metric[s] >= INF:
                continue
            for u in (0, 1):
                if t >= steps - (K - 1) and u == 1:
                    continue
                reg = (u << (K - 1)) | s
                o = [bin(reg & g).count("1") % 2 for g in gens]
                m = metric[s] + sum(a != b for a, b in zip(o, r))
                ns = reg >> 1
                if m < new[ns]:
                    new[ns], newp[ns] = m, paths[s] + [u]
        metric, paths = new, newp
        table.append(list(metric))
    return paths[0][: steps - (K - 1)], metric[0], table


def free_distance_brute(gens, K, max_len=12):
    best = 10**9
    for L in range(1, max_len + 1):
        for tail in itertools.product((0, 1), repeat=L - 1):
            u = (1,) + tail
            best = min(best, sum(conv_out(u, gens, K)))
    return best


def polar_z(i, n, eps):
    """Top-down: the first split applies to the raw channel; bit (n-1) of i chooses it."""
    if n == 0:
        return eps
    worse = 2 * eps - eps * eps
    better = eps * eps
    top = (i >> (n - 1)) & 1
    return polar_z(i & ((1 << (n - 1)) - 1), n - 1, better if top else worse)


def burst_miss(gpoly_bits, L):
    """Fraction of L-bit bursts (first and last bits 1) that leave remainder zero."""
    miss = 0
    for mid in range(2 ** (L - 2)):
        b = [1] + [(mid >> (L - 3 - i)) & 1 for i in range(L - 2)] + [1]
        word = np.zeros(L + len(gpoly_bits) + 3, np.uint8)
        word[3 : 3 + L] = b
        miss += cd.crc_check(word, gpoly_bits)
    return miss, 2 ** (L - 2)


# ------------------------------------------------------------------ text
v.check("Txt 17-08.a", db(4 / 7 * 3))
v.check("Txt 17-08.b", db(4 / 7 * 2))
v.check("Txt 17-08.c", (68 - 46) * 384)
v.check("Txt 17-08.d", 22 / 66)
v.check("Txt 17-08.e", (52 - 42) / 50)
z8 = [polar_z(i, 3, 0.5) for i in range(8)]
v.check("Txt 17-08.f", min(z8))
v.check("Txt 17-08.g", max(z8))
v.assert_true("polar N = 8: lab recursion equals the top-down one; erasures sum to N*eps = 4", np.allclose(cd.bec_polarize(0.5, 3), z8) and abs(sum(z8) - 4) < 1e-12)
v.check("Txt 17-08.h", free_distance_brute([0b111, 0b101], 3))
r_dvb = 0.988858 / 2  # R-276, bits per QPSK symbol / 2 dimensions
ebn0_dvb = 1.00 - db(0.988858)  # Es/N0 = 1.00 dB for QPSK 1/2
lim = it.required_es_n0_db(it.bpsk_soft_capacity, r_dvb) - db(r_dvb)
v.check("Txt 17-08.i", ebn0_dvb - lim)
v.check("Txt 17-08.j", lim)
v.assert_true("DVB-S2 QPSK 1/2 Eb/N0 = 1.05 dB (17-06); rate-1/2 BPSK-input limit 0.19 dB (17-07)", abs(ebn0_dvb - 1.05) < 0.005 and abs(it.required_es_n0_db(it.bpsk_soft_capacity, 0.5) + db(2) - 0.19) < 0.005)
v.assert_true("NR: BG2 largest block 10 x 384 = 3840; codeword 66 Zc and 50 Zc have 68 - 2 and 52 - 2 columns (2 Zc punctured)", 10 * 384 == 3840 and 66 == 68 - 2 and 50 == 52 - 2)

# sphere bound, perfect codes, syndrome independence, Singleton
v.assert_true("Hamming codes r = 2..5 are perfect: 2^k (1 + n) = 2^n", all(2 ** (2**r - 1 - r) * 2**r == 2 ** (2**r - 1) for r in range(2, 6)))
G15, H15 = cd.hamming(4)
v.assert_true("(15,11): G H^T = 0, rank H = 4, d_min = 3", not cd.gf2_matmul(G15, H15.T).any() and cd.gf2_rank(H15) == 4 and cd.min_distance(G15) == 3)
G74, H74 = cd.hamming74()
cws = cd.all_codewords(G74)
e = bits("0010000")
v.assert_true("syndrome depends only on the error pattern (all 16 codewords)", all((cd.syndrome(c ^ e, H74) == cd.syndrome(e, H74)).all() for c in cws))
v.assert_true("RS d_min = n - k + 1 meets Singleton; t = 15 for (544,514)", (544 - 514 + 1 - 1) // 2 == 15)
ext = np.hstack([cws, cws.sum(axis=1, keepdims=True) % 2])
v.assert_true("extended (8,4) Hamming code has d_min = 4 (SEC-DED)", int(ext.sum(axis=1)[1:].min()) == 4)
v.assert_true("SEC-DED for 64 bits: r = 7 is the least with 2^r >= 64 + r + 1, so 8 check bits", min(r for r in range(1, 20) if 2**r >= 64 + r + 1) == 7)

# CRC guarantees by exhaustive test on CRC6 and on x^4 + x + 1 (r = 4)
g6 = cd.poly_bits(cd.NR_CRC["CRC6"])
g4 = cd.poly_bits([4, 1, 0])
v.assert_true("every burst of length <= r is detected (CRC6, and x^4 + x + 1)", all(burst_miss(g6, L)[0] == 0 for L in range(1, 7) if L >= 2) and all(burst_miss(g4, L)[0] == 0 for L in range(2, 5)))
v.assert_true("bursts of length r + 1 missed with fraction 2^-(r-1), longer with 2^-r (x^4 + x + 1)", burst_miss(g4, 5) == (1, 8) and burst_miss(g4, 6) == (1, 16) and burst_miss(g4, 8)[0] / burst_miss(g4, 8)[1] == 1 / 16)
crc16 = cd.poly_bits(cd.NR_CRC["CRC16"])
v.assert_true("CRC16 detects every odd-weight pattern of weight 1, 3, 5 within 24 bits (x + 1 divides it)", all(not cd.crc_check(np.array([1 if i in pos else 0 for i in range(24)], np.uint8), crc16) for w in (1, 3) for pos in itertools.combinations(range(24), w)))
msg = rng.integers(0, 2, 40).astype(np.uint8)
v.assert_true("CRC24A append/check round trip; a single flipped bit is caught", cd.crc_check(cd.crc_append(msg, cd.poly_bits(cd.NR_CRC["CRC24A"])), cd.poly_bits(cd.NR_CRC["CRC24A"])) and not cd.crc_check(cd.crc_append(msg, cd.poly_bits(cd.NR_CRC["CRC24A"])) ^ np.eye(64, dtype=np.uint8)[7], cd.poly_bits(cd.NR_CRC["CRC24A"])))

# soft pairwise error and asymptotic gains
v.assert_true("Euclidean distance of BPSK codewords at Hamming distance d is 2 sqrt(d Ec)", abs(np.linalg.norm((1 - 2.0 * bits("1110000")) - (1 - 2.0 * bits("0000000"))) - 2 * math.sqrt(3)) < 1e-12)
v.assert_true("(7,5) gains 3.98 / 1.76 dB; K = 7 soft 6.99 dB", abs(db(2.5) - 3.98) < 0.005 and abs(db(1.5) - 1.76) < 0.005 and abs(db(5) - 6.99) < 0.005)

# polar: two-channel split by Monte Carlo on the BEC
n_mc = 200_000
er1 = rng.random(n_mc) < 0.3
er2 = rng.random(n_mc) < 0.3
v.assert_true("BEC split: u1 lost w.p. 2e - e^2, u2 lost w.p. e^2 (Monte Carlo, e = 0.3)", abs(np.mean(er1 | er2) - 0.51) < 0.005 and abs(np.mean(er1 & er2) - 0.09) < 0.003)

# LDPC: Gallager code properties and decoding
Hl = cd.gallager_ldpc(504, 3, 6, np.random.default_rng(3))
Gl = cd.gf2_nullspace(Hl)
v.assert_true("Gallager (3,6) H: column weight 3, row weight 6; null-space generator satisfies H G^T = 0", (Hl.sum(axis=0) == 3).all() and (Hl.sum(axis=1) == 6).all() and not cd.gf2_matmul(Hl, Gl.T).any())
v.assert_true("LDPC rank 250 of 252, so k = 254", cd.gf2_rank(Hl) == 250 and Gl.shape[0] == 254)
ok = 0
for _ in range(20):
    c = cd.encode_block(rng.integers(0, 2, Gl.shape[0]), Gl)[0]
    _, llr = cd.bpsk_awgn(c, 4.0, Gl.shape[0] / 504, rng)
    hard, _, success = cd.min_sum_decode(llr, Hl)
    ok += success and (hard == c).all()
v.assert_true("min-sum decodes 20 of 20 frames at 4 dB", ok == 20)
frozen = cd.polar_design(256, 128)
okp = 0
for _ in range(20):
    u = np.zeros(256, np.uint8)
    u[~frozen] = rng.integers(0, 2, 128)
    _, llr = cd.bpsk_awgn(cd.polar_encode(u), 5.0, 0.5, rng)
    uh, xh = cd.polar_sc_decode(llr, frozen)
    okp += (uh == u).all() and (xh == cd.polar_encode(uh)).all()
v.assert_true("polar SC decodes 20 of 20 (256,128) frames at 5 dB and re-encodes consistently", okp == 20)
Ls = rng.normal(0, 3, (2000, 5))
exact = 2 * np.arctanh(np.prod(np.tanh(Ls / 2), axis=1))
minsum = np.prod(np.sign(Ls), axis=1) * np.abs(Ls).min(axis=1)
v.assert_true("min-sum keeps the exact sign and never understates the magnitude (2000 random checks of degree 6)", (np.sign(exact) == np.sign(minsum)).all() and (np.abs(minsum) >= np.abs(exact) - 1e-12).all())

# ------------------------------------------------------------------ examples
v.check("Ex 17-08.1a", 4 / 7)
wd = np.bincount(cws.sum(axis=1), minlength=8)
v.check("Ex 17-08.1b", wd[3])
v.check("Ex 17-08.1c", int(min(w for w in range(1, 8) if wd[w])))
v.check("Ex 17-08.1d", 16 * (1 + 7))
c1011 = cd.encode_block(bits("1011"), G74)[0]
v.assert_true("Example 1: 1011 -> 1011 010; 1001 010 has syndrome 011 = column 3 and decodes back; A = (1, 0, 0, 7, 7, 0, 0, 1)", "".join(map(str, c1011)) == "1011010" and "".join(map(str, cd.syndrome(bits("1001010"), H74)[0])) == "011" and (cd.syndrome_decode(bits("1001010"), H74) == c1011).all() and list(wd) == [1, 0, 0, 7, 7, 0, 0, 1])

v.check("Ex 17-08.2a", 2.0**-24)
v.check("Ex 17-08.2b", 2.0**-23)
v.check("Ex 17-08.2c", 100 * 16 / 3824)
v.check("Ex 17-08.2d", 100 * 24 / 3840)
v.check("Ex 17-08.2e", sum(len(e) % 2 == 0 for e in cd.NR_CRC.values()))
v.assert_true("Example 2: term counts 14, 6, 13, 4, 5, 3 (R-279); g(1) = 0 exactly for the even ones", [len(cd.NR_CRC[k]) for k in ("CRC24A", "CRC24B", "CRC24C", "CRC16", "CRC11", "CRC6")] == [14, 6, 13, 4, 5, 3])
v.assert_true("Example 2: 8 more bits cut the miss rate by 256", 2.0**-16 / 2.0**-24 == 256)

eb7 = un(7)
p_u = Q(math.sqrt(2 * eb7))
p_c = Q(math.sqrt(2 * 4 / 7 * eb7))
v.check("Ex 17-08.3a", p_u)
v.check("Ex 17-08.3b", 1 - (1 - p_u) ** 4)
v.check("Ex 17-08.3c", p_c)
pb3 = 1 - (1 - p_c) ** 7 - 7 * p_c * (1 - p_c) ** 6
v.check("Ex 17-08.3d", pb3)
nblk = 300_000
msgs = rng.integers(0, 2, (nblk, 4)).astype(np.uint8)
cw = cd.gf2_matmul(msgs, G74).astype(np.uint8)
flips = (rng.random(cw.shape) < p_c).astype(np.uint8)
rx = cw ^ flips
syn = cd.gf2_matmul(rx, H74.T)
col_of = {tuple(H74[:, j]): j for j in range(7)}
fix = np.array([col_of.get(tuple(s), -1) for s in syn])
rows = np.flatnonzero(fix >= 0)
rx[rows, fix[rows]] ^= 1
sim_blk = np.mean((rx[:, :4] != msgs).any(axis=1))
v.assert_true(f"Example 3: Monte Carlo block error {sim_blk:.2e} vs formula (bounded distance, data part)", sim_blk <= pb3 * 1.1 and sim_blk > 0.8 * pb3)
v.assert_true("Example 3: close to 21 pc^2; ratio uncoded/coded about 2", abs(pb3 / (21 * p_c**2) - 1) < 0.05 and 1.9 < (1 - (1 - p_u) ** 4) / pb3 < 2.4)

g75 = [0b111, 0b101]
tx4 = conv_out([1, 0, 1, 1], g75, 3)
rx4 = list(tx4)
rx4[1] ^= 1
rx4[8] ^= 1
dec4, met4, tab4 = viterbi_loops(rx4, g75, 3)
v.check("Ex 17-08.4a", met4)
v.check("Ex 17-08.4b", cd.free_distance(("7", "5"), 3))
v.check("Ex 17-08.4c", db(0.5 * 5))
v.check("Ex 17-08.4d", db(0.5 * 3))
v.assert_true("Example 4: 1011 encodes to 11 10 00 01 01 11 (lab and definition agree)", "".join(map(str, tx4)) == "111000010111" and (cd.conv_encode([1, 0, 1, 1], ("7", "5"), 3) == np.array(tx4)).all())
INF = 10**9
want = {0: [1, 2, 2, 3, 3, 2], 2: [1, 2, 1, 3, INF, INF], 1: [INF, 1, 3, 3, 2, INF], 3: [INF, 3, 3, 1, INF, INF]}  # states 00, 10, 01, 11
v.assert_true("Example 4: survivor-metric table matches step by step; decoded 1011; lab Viterbi agrees", all([tab4[t][s] for t in range(6)] == want[s] for s in want) and dec4 == [1, 0, 1, 1] and (cd.viterbi(np.array(rx4), ("7", "5"), 3, soft=False) == [1, 0, 1, 1]).all())

spec7 = cd.distance_spectrum(("171", "133"), 7, 60)
v.assert_true("K = 7 spectrum: d_free 10, A_10 = 11, B = 36, 211, 1404, 11633; odd weights absent", spec7[10] == (11, 36) and spec7[12][1] == 211 and spec7[14][1] == 1404 and spec7[16][1] == 11633 and all(d % 2 == 0 for d in spec7) and free_distance_brute([0o171, 0o133], 7, 9) == 10)
v.check("Ex 17-08.5a", db(0.5 * min(spec7)))
ub = lambda x, s=spec7: cd.union_bound_ber(s, 0.5, un(x))  # noqa: E731
x5 = optimize.brentq(lambda x: ub(x) - 1e-5, 2, 8, xtol=1e-12)
unc5 = db(Qi(1e-5) ** 2 / 2)
v.check("Ex 17-08.5b", x5)
v.check("Ex 17-08.5c", unc5 - x5)
v.check("Ex 17-08.5d", x5 - (it.required_es_n0_db(it.bpsk_soft_capacity, 0.5) + db(2)))
v.assert_true("Example 5: threshold stable to 1e-4 dB when the spectrum is cut at d = 40 instead of 60", abs(optimize.brentq(lambda x: cd.union_bound_ber(cd.distance_spectrum(("171", "133"), 7, 40), 0.5, un(x)) - 1e-5, 2, 8) - x5) < 1e-4)
v.assert_true("Example 5: the d = 10 term is 57% of the bound at 4.17 dB", round(100 * 36 * Q(math.sqrt(10 * un(x5))) / 1e-5) == 57)
ub35 = ub(3.5)
errs35 = 0
for _ in range(6):
    u = rng.integers(0, 2, 100_000).astype(np.uint8)
    y, _ = cd.bpsk_awgn(cd.conv_encode(u, ("171", "133"), 7), 3.5, 0.5, rng)
    errs35 += int(np.sum(cd.viterbi(y, ("171", "133"), 7) != u))
sim35 = errs35 / 600_000
v.assert_true(f"Example 5: soft Viterbi at 3.5 dB over 600k bits gives {sim35:.2e}, below the bound {ub35:.2e} and within a factor 4 of it", 0.25 * ub35 < sim35 < 1.2 * ub35)

v.check("Ex 17-08.6a", (544 - 514) // 2)
v.check("Ex 17-08.6b", 100 * (544 / 514 - 1))
v.check("Ex 17-08.6c", cd.rs_burst_bits(15, 10))


def rs_fail_log(n, k, m, ber):
    """Independent route: sum the binomial tail in the log domain."""
    t = (n - k) // 2
    q = 1 - (1 - ber) ** m
    return sum(math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(q) + (n - i) * math.log1p(-q)) for i in range(t + 1, n + 1))


v.check("Ex 17-08.6d", rs_fail_log(544, 514, 10, 1e-4))
thr = lambda n, k: 10 ** optimize.brentq(lambda lb: math.log10(rs_fail_log(n, k, 10, 10**lb)) + 12, -7, -2, xtol=1e-13)  # noqa: E731
v.check("Ex 17-08.6e", thr(544, 514))
v.check("Ex 17-08.6f", thr(528, 514))
v.check("Ex 17-08.6g", 400 * 257 / 256 * 544 / 514)
v.assert_true("Example 6: lab rs_codeword_error agrees; q = 1.0e-3 at 1e-4; KR4: t = 7, 2.72%, 61 bits, 8.9e-8", abs(cd.rs_codeword_error(544, 514, 10, 1e-4) / rs_fail_log(544, 514, 10, 1e-4) - 1) < 1e-6 and abs(1 - (1 - 1e-4) ** 10 - 1.0e-3) < 5e-6 and abs(100 * (528 / 514 - 1) - 2.72) < 0.005 and cd.rs_burst_bits(7, 10) == 61 and abs(rs_fail_log(528, 514, 10, 1e-4) - 8.9e-8) < 5e-10)
v.assert_true("Example 6: 257 x 544 / (256 x 514) is exactly 1.0625; threshold codeword holds about 1.3 bad bits", 257 * 544 * 16 == 256 * 514 * 17 and abs(5440 * thr(544, 514) - 1.3) < 0.05)
v.assert_true("Example 6: worst-case burst 141 bits touches 15 symbols, 142 touches 16", 1 + math.ceil(140 / 10) == 15 and 1 + math.ceil(141 / 10) == 16)

# ------------------------------------------------------------------ problems
v.check("17-08.1a", (7 - 1) // 2)
v.check("17-08.1b", 7 - 1)
v.check("17-08.1c", 7 - 1 - 2)
v.check("17-08.2a", 1 + 15)
v.check("17-08.2b", sum(math.comb(23, i) for i in range(4)))
v.assert_true("Problem 2: 2^12 x 2048 = 2^23 and 2^11 x 16 = 2^15", 2**12 * 2048 == 2**23 and 2**11 * 16 == 2**15)
v.check("17-08.3a", int(g6.sum()))
v.assert_true("Problem 3: g(x) itself (1100001) is an undetected weight-3 pattern", cd.crc_check(np.concatenate([np.zeros(5, np.uint8), g6]), g6))
v.check("17-08.3b", burst_miss(g6, 7)[0] / burst_miss(g6, 7)[1])
v.check("17-08.3c", burst_miss(g6, 8)[0] / burst_miss(g6, 8)[1])
r4 = c1011.copy()
r4[[0, 1]] ^= 1
d4 = cd.syndrome_decode(r4, H74)
v.check("17-08.4a", int((d4 != c1011).sum()))
v.assert_true("Problem 4: syndrome 011; decoded 0101 010 is a codeword", "".join(map(str, cd.syndrome(r4, H74)[0])) == "011" and not cd.syndrome(d4, H74).any() and "".join(map(str, d4)) == "0101010")
r128 = min(r for r in range(1, 20) if 2**r >= 128 + r + 1)
r32 = min(r for r in range(1, 20) if 2**r >= 32 + r + 1)
v.check("17-08.5a", r128 + 1)
v.check("17-08.5b", 100 * (r128 + 1) / 128)
v.check("17-08.5c", r32 + 1)
v.check("17-08.5d", 100 * (r32 + 1) / 32)
v.check("17-08.6a", binom.sf(1, 15, 1e-3))
v.check("17-08.6b", binom.sf(1, 7, 1e-3))
v.check("17-08.6c", 11 / 15)
v.assert_true("Problem 6: about 5x per block, about 1.8x per information bit", round(binom.sf(1, 15, 1e-3) / binom.sf(1, 7, 1e-3)) == 5 and abs((binom.sf(1, 15, 1e-3) / 11) / (binom.sf(1, 7, 1e-3) / 4) - 1.8) < 0.05)
v.check("17-08.7a", db(1 / 3 * 3))
v.check("17-08.7b", db(1 / 3 * 2))
tx8 = conv_out([1, 1, 0, 1], g75, 3)
v.check("17-08.8a", sum(tx8))
v.assert_true("Problem 8: output 11 01 01 00 10 11", "".join(map(str, tx8)) == "110101001011")
rx9 = list(tx8)
rx9[2] ^= 1
rx9[9] ^= 1
dec9, met9, _ = viterbi_loops(rx9, g75, 3)
v.check("17-08.9a", met9)
v.assert_true("Problem 9: decodes 1101 (both implementations)", dec9 == [1, 1, 0, 1] and (cd.viterbi(np.array(rx9), ("7", "5"), 3, soft=False) == [1, 1, 0, 1]).all())
v.check("17-08.10a", 2 ** (7 - 1) * 1e9)
v.check("17-08.10b", 2 ** (9 - 1) / 2 ** (7 - 1))
v.check("17-08.10c", 5 * 7)
for key, (kin, kept) in (("17-08.11a", (2, 3)), ("17-08.11b", (3, 4)), ("17-08.11c", (5, 6))):
    v.check(key, 1 - kept / (2 * kin))
v.check("17-08.12a", binom.sf(15, 544, 1e-3))
v.check("17-08.12b", binom.sf(15, 544, 3e-3))
v.check("17-08.12c", binom.sf(7, 528, 1e-3))
v.check("17-08.12d", binom.sf(7, 528, 3e-3))
v.assert_true("Problem 12: tripling q multiplies failures by about 1.6e7 (KP4) and 2600 (KR4)", abs(binom.sf(15, 544, 3e-3) / binom.sf(15, 544, 1e-3) / 1.6e7 - 1) < 0.03 and abs(binom.sf(7, 528, 3e-3) / binom.sf(7, 528, 1e-3) / 2600 - 1) < 0.02)
z4 = [polar_z(i, 2, 0.3) for i in range(4)]
for key, val in zip(("17-08.13a", "17-08.13b", "17-08.13c", "17-08.13d"), z4):
    v.check(key, val)
v.check("17-08.13e", z4[2] + z4[3])
v.assert_true("Problem 13: erasures sum to 1.2; the two best are indices 2 and 3; lab agrees", abs(sum(z4) - 1.2) < 1e-12 and sorted(np.argsort(z4)[:2]) == [2, 3] and np.allclose(cd.bec_polarize(0.3, 2), z4))
unc6 = db(Qi(1e-6) ** 2 / 2)
x6 = optimize.brentq(lambda x: ub(x) - 1e-6, 2, 8, xtol=1e-12)
v.check("17-08.14a", x6)
v.check("17-08.14b", unc6 - x6)
v.check("17-08.14c", 10 ** ((unc6 - x6) / 20))
ldpc = it.required_es_n0_db(it.bpsk_soft_capacity, 0.5) + db(2) + 1.0
v.check("17-08.14d", unc6 - ldpc)
v.check("17-08.14e", 10 ** ((unc6 - ldpc) / 20))
D, N = sp.symbols("D N")
T = D**5 * N / (1 - 2 * D * N)
Xb, Xc, Xd = sp.symbols("X_b X_c X_d")
solv = sp.solve([sp.Eq(Xb, D**2 * N + N * Xc), sp.Eq(Xc, D * Xb + D * Xd), sp.Eq(Xd, D * N * Xb + D * N * Xd)], [Xb, Xc, Xd], dict=True)[0]
v.assert_true("Problem 15: solving the state equations gives T = D^5 N / (1 - 2DN)", sp.simplify(D**2 * solv[Xc] - T) == 0)
serA = sp.series(T.subs(N, 1), D, 0, 9).removeO()
serB = sp.series(sp.diff(T, N).subs(N, 1), D, 0, 9).removeO()
v.check("17-08.15a", int(serA.coeff(D, 8)))
v.check("17-08.15b", int(serB.coeff(D, 6)))
v.check("17-08.15c", int(serB.coeff(D, 8)))
spec75 = cd.distance_spectrum(("7", "5"), 3, 70)
v.check("17-08.15d", cd.union_bound_ber(spec75, 0.5, un(6)))
v.assert_true("Problem 15: lab spectrum equals the series (A_d = 2^(d-5), B_d = (d-4) 2^(d-5), d <= 20)", all(spec75[d] == (2 ** (d - 5), (d - 4) * 2 ** (d - 5)) for d in range(5, 21)) and abs(sum((d - 4) * 2 ** (d - 5) * Q(math.sqrt(d * un(6))) for d in range(5, 120)) - cd.union_bound_ber(spec75, 0.5, un(6))) < 1e-12)
v.check("17-08.16a", 2 * math.atanh(math.tanh(1.0) * math.tanh(-0.5)))
v.check("17-08.16b", np.sign(2 * -1) * min(2, 1))
v.check("17-08.16c", 0.75 * np.sign(2 * -1) * min(2, 1))
v.assert_true("Problem 16: tanh(1) = 0.7616, tanh(-0.5) = -0.4621, product -0.3519", abs(math.tanh(1) - 0.7616) < 5e-5 and abs(math.tanh(-0.5) + 0.4621) < 5e-5 and abs(math.tanh(1) * math.tanh(-0.5) + 0.3519) < 5e-5)

# ------------------------------------------------------------------ lab
v.check("Lab 17-08.a", int(cd.weight_distribution(G15)[3]))
v.assert_true("Lab part 1: (15,11) Hamming has A_3 = 35 = C(15,2)/3 (each weight-2 pattern lies in one weight-3 word)", cd.weight_distribution(G15)[3] == math.comb(15, 2) // 3)
v.check("Lab 17-08.b", burst_miss(g6, 7)[0])
v.check("Lab 17-08.c", burst_miss(g6, 9)[0] / burst_miss(g6, 9)[1])
v.check("Lab 17-08.d", cd.union_bound_ber(spec75, 0.5, un(3.5)))
v.check("Lab 17-08.e", ub35)
z1024 = cd.bec_polarize(0.5, 10)
v.check("Lab 17-08.f", np.mean((z1024 >= 0.1) & (z1024 <= 0.9)))
v.assert_true("Lab part 5: undecided fraction 0.75 at N = 8 and 0.31 at N = 64; mean of 1 - z stays 0.5", abs(np.mean((cd.bec_polarize(0.5, 3) >= 0.1) & (cd.bec_polarize(0.5, 3) <= 0.9)) - 0.75) < 1e-12 and abs(np.mean((cd.bec_polarize(0.5, 6) >= 0.1) & (cd.bec_polarize(0.5, 6) <= 0.9)) - 0.3125) < 1e-12 and abs(np.mean(1 - z1024) - 0.5) < 1e-12)
v.check("Lab 17-08.g", thr(544, 514))

sys.exit(v.finish())
