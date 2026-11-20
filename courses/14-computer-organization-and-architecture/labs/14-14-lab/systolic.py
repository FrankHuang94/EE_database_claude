"""A cycle-accurate output-stationary systolic array for Lab 14-14.

`run(A, B, P)` multiplies an M x K matrix A by a K x N matrix B on a P x P array (M, N <= P). Row i of A enters
the left edge delayed by i cycles and column j of B enters the top edge delayed by j cycles (the skew). Each cycle
every processing element (PE) multiplies the two operands it holds, adds the product to its own accumulator, and
passes A to the right and B downward. PE (i, j) therefore sees a[i][k] and b[k][j] together at cycle k + i + j.
The function returns the product, the cycles until the last multiply-accumulate, and the MACs performed.
`tiled_cycles` estimates a large GEMM tiled onto the array without overlap between tiles.
"""
from __future__ import annotations

import math


def run(A, B, P: int):
    M, K, N = len(A), len(A[0]), len(B[0])
    assert len(B) == K and M <= P and N <= P
    a_reg = [[None] * P for _ in range(P)]      # operand held by each PE this cycle
    b_reg = [[None] * P for _ in range(P)]
    acc = [[0] * N for _ in range(M)]
    macs = cycle = last = 0
    while cycle < K + M + N:                     # enough cycles for every operand to cross the array
        # shift: A moves right, B moves down (from the far edge inward so values are not overwritten)
        for i in range(P):
            for j in range(P - 1, 0, -1):
                a_reg[i][j] = a_reg[i][j - 1]
        for j in range(P):
            for i in range(P - 1, 0, -1):
                b_reg[i][j] = b_reg[i - 1][j]
        # inject skewed inputs at the edges
        for i in range(P):
            k = cycle - i
            a_reg[i][0] = A[i][k] if i < M and 0 <= k < K else None
        for j in range(P):
            k = cycle - j
            b_reg[0][j] = B[k][j] if j < N and 0 <= k < K else None
        # multiply-accumulate where both operands are present
        for i in range(M):
            for j in range(N):
                if a_reg[i][j] is not None and b_reg[i][j] is not None:
                    acc[i][j] += a_reg[i][j] * b_reg[i][j]
                    macs += 1
                    last = cycle
        cycle += 1
    return acc, last + 1, macs


def utilization(M: int, K: int, N: int, P: int, cycles: int) -> float:
    return M * K * N / (P * P * cycles)


def tiled_cycles(M: int, K: int, N: int, P: int) -> int:
    """Cycles to compute an M x K x N product as ceil(M/P) x ceil(N/P) output tiles of K + 2(P - 1) cycles each,
    one after another (no overlap of one tile's drain with the next tile's fill)."""
    return math.ceil(M / P) * math.ceil(N / P) * (K + 2 * (P - 1))


def quantize(xs, bits: int = 8):
    """Symmetric per-tensor quantization: scale = max|x| / (2^(bits-1) - 1); returns (ints, scale, dequantized)."""
    qmax = 2 ** (bits - 1) - 1
    scale = max(abs(x) for x in xs) / qmax
    q = [max(-qmax, min(qmax, round(x / scale))) for x in xs]
    return q, scale, [v * scale for v in q]
