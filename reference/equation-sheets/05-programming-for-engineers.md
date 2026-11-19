# Reference Sheet · 05 Programming for Engineers

The rules, formulas and numbers to know cold from Course 05, each with its conditions and the chapter that develops it. Unless stated otherwise, C rules assume a 32-bit `int`, and sizes assume a 64-bit desktop (8-byte pointers).

## Python and NumPy

| Rule or formula | Conditions / notes | Chapter |
|---|---|---|
| `b = a` names the same object; `a[:]`, `list(a)`, `copy.copy` make shallow copies | Mutable objects (lists, dicts, arrays) | [05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md) |
| `//` floors toward −∞ (`-7 // 2 == -4`); `%` takes the divisor's sign | Python integers never overflow | [05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md) |
| binary64: 53-bit significand, $\varepsilon = 2^{-52} \approx 2.22\times10^{-16}$; `0.1 + 0.2 != 0.3` | Compare floats with tolerances | [05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md) |
| binary32: $\varepsilon = 2^{-23} \approx 1.19\times10^{-7}$; float16: $2^{-10}$ | About 7 and 3 significant digits | [05-02](../../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md) |
| Broadcasting: align shapes from the right; each pair of dimensions must be equal or 1 | (3, 1) + (4,) → (3, 4) | [05-02](../../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md) |
| Fixed-width NumPy integers wrap modulo $2^n$; NumPy 2 (NEP 50): a Python scalar adopts the array's dtype | `uint8` 200 + 100 = 44; `int8` 100 + 50 = −106 | [05-02](../../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md) |
| Catastrophic cancellation: subtracting near-equal numbers loses the shared digits | Reformulate (e.g. $1 - \cos x = 2\sin^2(x/2)$) | [05-02](../../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md) |

## Numerical methods

| Rule or formula | Conditions / notes | Chapter |
|---|---|---|
| Bisection: bracket width $w_0/2^n$; steps $n = \lceil\log_2(w_0/\text{tol})\rceil$ | Needs a sign change; always converges | [05-01](../../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md), [05-03](../../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md) |
| Newton: $x_{k+1} = x_k - f(x_k)/f'(x_k)$; correct digits roughly double near the root | Needs a good start; can diverge or stall | [05-03](../../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md) |
| Least-squares line: $m = S_{xy}/S_{xx}$, $b = \bar y - m\bar x$ | Check residuals for patterns | [05-02](../../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md), [05-03](../../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md) |
| Trapezoid: $\int \approx h\,[\tfrac12 y_0 + y_1 + \cdots + y_{n-1} + \tfrac12 y_n]$ | Error $O(h^2)$ for smooth integrands | [05-03](../../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md) |
| Always substitute the answer back: the residual must be small relative to the problem's scale | Solvers can stop at non-roots | [05-03](../../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md) |

## Testing and reproducibility

| Rule or formula | Conditions / notes | Chapter |
|---|---|---|
| `math.isclose`: rel $10^{-9}$, abs 0; `pytest.approx`: rel $10^{-6}$, abs $10^{-12}$; `numpy.isclose`: rtol $10^{-5}$, atol $10^{-8}$ | A relative tolerance of 0 is useless for expected value 0 | [05-04](../../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md) |
| Half-unit check: tolerance $= \tfrac12 \times 10^{\text{(exponent of last digit)}}$ | 0.6925 → ±0.00005 | [05-04](../../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md) |
| Birthday bound: $P \approx n^2/(2N)$; 50% at $n \approx \sqrt{2N\ln 2}$ | 7-hex short hashes: ~19,300 commits | [05-04](../../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md) |
| False failures: one test $p$; suite of $k$: $1 - (1 - p)^k$; $P(|Z| > 3) = 0.0027$, $P(|Z| > 4) = 6.3\times10^{-5}$ | Fix seeds; widen limits for big suites | [05-04](../../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md) |
| Git blob hash = SHA-1(`"blob <size>\0"` + content) | Content-addressed versions | [05-04](../../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md) |

## C language rules

| Rule | Conditions / notes | Chapter |
|---|---|---|
| Build: preprocessor → compiler → assembler → linker; "undefined reference" is a linker error | Declarations in headers, one definition | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| `int` 32 bits: −2,147,483,648 to 2,147,483,647; `long` 64 bits on Linux/macOS, 32 on Windows and MCUs | Use `<stdint.h>` when width matters | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| `/` truncates toward 0; `%` has the dividend's sign; $(a/b)b + a\%b = a$ | `-7 / 2 == -3`, `-7 % 2 == -1` | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| Integer promotion: types narrower than `int` become `int` before arithmetic | `uint8_t` 250 + 10 is the `int` 260 | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| Mixed signed/unsigned of the same size: the signed operand converts to unsigned | `-1 < 1u` is false | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| Unsigned arithmetic wraps mod $2^n$; signed overflow, oversized shifts, uninitialized reads are undefined behavior | Catch with `-Wall -Wextra -Werror` and sanitizers | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| `(int64_t)a * b`, not `(int64_t)(a * b)` | Widen before multiplying | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| ADC to mV with rounding: `(k * Vref + 2^(N-1)) / 2^N` | Multiply first; check the intermediate fits | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |
| `static`: file scope → internal linkage; inside a function → persists | | [05-05](../../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md) |

## Pointers and memory

| Rule | Conditions / notes | Chapter |
|---|---|---|
| `a[i]` ≡ `*(a + i)`; `p + k` advances $k \times$ `sizeof *p` bytes; `q - p` counts elements | Same array only | [05-06](../../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |
| Arrays decay to pointers when passed: `sizeof` a parameter gives the pointer size | Pass lengths as `size_t` | [05-06](../../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |
| String of length $L$ needs $L + 1$ bytes; `snprintf` returns the length it needed (≥ size means truncated) | Avoid `strcpy`, `sprintf` | [05-06](../../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |
| Struct padding: each field aligned to its size; total rounded to the largest alignment; order fields largest first | uint8, uint32, uint16 → 12 bytes; reordered → 8 | [05-06](../../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |
| Stack (locals, freed on return), static (whole program), heap (`malloc`/`free`, one owner, free once) | `realloc` may move the block | [05-06](../../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |
| Doubling growth: total copies < final capacity; fixed step $s$: ~$n^2/(2s)$ | Amortized O(1) append | [05-06](../../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |

## Bits, bytes and fixed point

| Rule or formula | Conditions / notes | Chapter |
|---|---|---|
| Two's complement: $S = -b_{n-1}2^{n-1} + \sum_{i<n-1} b_i 2^i$; range $-2^{n-1}$ to $2^{n-1}-1$; $-x = \sim x + 1$ | Same adder for signed and unsigned | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| Sign-extend a $k$-bit field: $(x \oplus 2^{k-1}) - 2^{k-1}$ | 12-bit `0xFFF` → −1 | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| Set `r \|= m`; clear `r &= ~m`; toggle `r ^= m`; test `r & m`; field: `(r >> p) & (2^w − 1)`; insert: clear, then OR `(v & mask) << p` | Unsigned types; `1u << 31` | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| `volatile` for registers and ISR-shared variables; it does not make read-modify-write atomic | Beware write-1-to-clear bits | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| Little-endian: least significant byte at the lowest address (x86, most Arm MCUs); network order is big-endian | Serialize with shifts | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| Q15: $x = q/2^{15}$, range $[-1, 1 - 2^{-15}]$; product `(a*b + 2^14) >> 15`, saturate $(-1)(-1)$ | Q30 intermediate in 32 bits | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| Rounding error RMS $\Delta/\sqrt{12}$; truncation RMS $\Delta/\sqrt3$ (biased); ≈6.02 dB per bit; ideal SNR $6.02N + 1.76$ dB | Uniform-error model | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| Power of two: `x && !(x & (x-1))`; `x % 2^k == x & (2^k − 1)`; `x &= x − 1` clears the lowest set bit | Unsigned `x` | [05-07](../../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |

## Algorithms and data structures

| Rule or formula | Conditions / notes | Chapter |
|---|---|---|
| $f = O(g)$: $f(n) \le c\,g(n)$ for $n \ge n_0$; costs at $n = 10^6$ and $10^9$/s: $\log n$ 20 ns, $n$ 1 ms, $n\log n$ 20 ms, $n^2$ 17 min | Growth rate dominates constants at large $n$ | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| Binary search: at most $\lfloor\log_2 n\rfloor + 1$ comparisons | Sorted data | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| Insertion sort: inversions + ~$n$; $n(n-1)/4$ on random data; merge sort $T(n) = 2T(n/2) + n = n\log_2 n$, worst $n\lceil\log n\rceil - 2^{\lceil\log n\rceil} + 1$ | Merge sort is stable | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| Comparison-sort lower bound $\lceil\log_2 n!\rceil \approx n\log_2 n - 1.44n$; counting sort $O(n + k)$ | Keys in a range of $k$ | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| Ring buffer (size $N = 2^k$, free-running counters): slot `c & (N−1)`, count `head − tail`, full when $N$ | Wrap-safe unsigned arithmetic | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| Linear probing at load α: successful $\tfrac12(1 + \frac1{1-\alpha})$, miss $\tfrac12(1 + \frac1{(1-\alpha)^2})$; chaining $1 + \alpha/2$, $1 + \alpha$ | Resize before α ≈ 0.75; never fill | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| Binary heap (0-based): children $2i+1$, $2i+2$, parent $\lfloor(i-1)/2\rfloor$; push and pop $O(\log n)$ | Priority queue | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |
| FNV-1a (32-bit): $h_0$ = 2166136261; $h \leftarrow (h \oplus \text{byte}) \times 16777619 \bmod 2^{32}$ | Non-cryptographic | [05-08](../../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md) |

## Software engineering

| Rule or formula | Conditions / notes | Chapter |
|---|---|---|
| Cyclomatic complexity $M = E - N + 2P$ = decisions + 1 | Basis-path test count; flag $M$ > 10–15 | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
| MC/DC: each condition independently flips the decision; ≥ $N + 1$ tests (vs $2^N$) | Required for DO-178C Level A | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
| Boundary values: just below, at, just above each edge | Where `<` vs `<=` bugs live | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
| Escapes through filters: $D\prod(1 - p_i)$ | Independence is optimistic | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
| Capture–recapture: $\hat N = n_A n_B/m$ | Two independent reviews | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
| Canary detection: $1 - (1 - p)^n$; 95% needs $n \approx 3/p$ | Rule of three | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
| Semantic versioning MAJOR.MINOR.PATCH: breaking / compatible feature / fix | Compare as numeric tuples | [05-09](../../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md) |
