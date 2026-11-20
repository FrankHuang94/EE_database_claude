# Solutions 16-09 · Multirate DSP: Decimation, Interpolation and Polyphase

Problems: [16-09 problems](../problems/16-09-problems.md) · Chapter: [16-09](../chapters/16-09-multirate-dsp.md). Every number below is recomputed by [verify_16_09.py](../verify/verify_16_09.py): aliases and images from FFTs of simulated tones, polyphase results against direct filtering, designs with SciPy's `remez`, and CIC responses against a direct cascade of moving sums.

---

## Solutions

### Solution 16-09.1

The new rate is 16 kHz (Nyquist 8 kHz). Each component lands at its distance from the nearest multiple of 16 kHz: 7 kHz stays at **7** kHz; 9 kHz lands at $16 - 9$ = **7** kHz, on top of the first; 13 kHz lands at $16 - 13$ = **3** kHz.

### Solution 16-09.2

The spectrum repeats every 8 kHz: $1$, $8 \pm 1$, $16 - 1$ kHz, so **1**, **7**, **9** and **15** kHz, each with a quarter of the tone's amplitude.

### Solution 16-09.3

(a) $H(z^2) = 1 + z^{-2}$: $v[n] = x[n] + x[n - 2] = (1, 2, 4, 6, 8, 10)$; keeping samples 0, 2, 4 gives **(1, 4, 8)**. (b) $\downarrow 2$ gives $(1, 3, 5)$; $1 + z^{-1}$ gives $(1, 1 + 3, 3 + 5) = $ **(1, 4, 8)**. Identical, as the first noble identity requires.

### Solution 16-09.4

$E_0 = (h[0], h[3], h[6]) = (1, 4, 7)$, $E_1 = (h[1], h[4]) = (2, 5)$, $E_2 = (h[2], h[5]) = (3, 6)$. Polyphase: the 7 taps are each used once per 10 kHz output, **70,000** multiplications per second; filtering at the input rate costs $7 \times 30{,}000$ = **210,000**.

### Solution 16-09.5

(a) $\gcd(44{,}100, 48{,}000) = 300$, so $L$ = **160** and $M$ = **147**; the intermediate rate is $44.1 \times 160$ = **7.056** MHz.

(b) Naive: $3200 \times 7.056 \times 10^6$ = **22.58** × 10⁹ per second. Polyphase: each output uses one phase of $3200/160$ = **20** taps, so $20 \times 48{,}000$ = **960,000** per second, about 23,500 times less.

### Solution 16-09.6

With the middle tap at index 29 (odd), $E_1[n] = h[2n + 1]$ contains $h[29] = 1/2$ and the taps at the other odd indices, which are at even offsets from the middle and therefore zero: $E_1(z) = \tfrac12z^{-14}$, a pure delay. $E_0[n] = h[2n]$ holds the 30 taps at even indices, all at odd offsets from the middle, all nonzero. Nonzero taps: **31**; folded (15 symmetric pairs in $E_0$, the middle tap a shift): **15** multipliers at the 48 kHz output rate, **720,000** per second.

### Solution 16-09.7

DC gain $16^3$ = **4096**; register growth $3\log_216$ = **12** bits. With $\lvert H(f)\rvert = \lvert\sin(16\pi f/f_s)/(16\sin(\pi f/f_s))\rvert^3$ and $f_s = 1.6$ MHz: droop at 10 kHz **−0.428** dB; attenuation at 90 kHz **57.5** dB. 90 kHz is 100 − 10 kHz: it is the alias that lands on the 10 kHz edge of a 0–10 kHz passband after decimation, so 57.5 dB is the worst-case protection of that passband from the first alias band.

### Solution 16-09.8

$16 + 5\log_264 = 16 + 30$ = **46** bits, in every register. The integrators must wrap around in two's complement (no saturation); the output is still exact because it fits in 46 bits and modular arithmetic is exact.

### Solution 16-09.9

At 192 kHz, $\Delta f/f_s = 8/192$; $-10\log_{10}(10^{-3} \times 10^{-4}) = 70$, so $M \approx (70 - 13)/(2.324 \times 2\pi \times 8/192)$ = **93.7**, about 95 taps. Naive (filtering the zero-stuffed signal at 192 kHz): $95 \times 192{,}000$ = **18.24** million per second. Polyphase (four branches of about 24 taps running at 48 kHz, so each tap once per input sample): $95 \times 48{,}000$ = **4.56** million per second, four times less.

### Solution 16-09.10

Single stage at 192 kHz, stopband from 28 kHz: the shortest equiripple filter has **98** taps; folded, 49 multiplications per 48 kHz output, **2.352** million per second. Two half-bands: 192 → 96 kHz (stopband from 76 kHz) needs **15** taps, 4 folded multipliers at 96 kHz (384,000 per second); 96 → 48 kHz (stopband from 28 kHz) needs **59** taps, 15 at 48 kHz (720,000 per second). Total **1.104** million per second, **2.13** times less.

### Solution 16-09.11

$R = 64$, $N = 4$: output rate $12.8\text{ MHz}/64$ = 200 kSPS. Solving $\lvert\sin(64\pi f/f_{MOD})/(64\sin(\pi f/f_{MOD}))\rvert^4 = 1/\sqrt2$ gives **45.51** kHz (data sheet: 45.5 kHz). The impulse response spans $NR = 256$ modulator samples, $256/12.8\text{ MHz}$ = **20.0** µs; the data sheet's 20.63 µs is that span plus the same 0.63 µs overhead seen at OSR 32. Theory and data sheet agree.

### Solution 16-09.12

$E_0 = (h[0], h[2]) = (0.5, 0.5)$ and $E_1 = (h[1]) = (1)$. Phase 0: $E_0 * x = (0.5 \times 2,\ 0.5 \times 4 + 0.5 \times 2,\ 0.5 \times 6 + 0.5 \times 4) = (1, 3, 5)$. Phase 1: $E_1 * x = (2, 4, 6)$. Interleaving phase 0 then phase 1: **(1, 2, 3, 4, 5, 6)**. This is linear interpolation: the inserted samples are the averages of their neighbours, and the whole output is delayed by half an input sample (16-06's linear-phase delay $M/2 = 1$ output sample).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-09.1a | 7 kHz lands at | 7 | kHz |
| 16-09.1b | 9 kHz lands at | 7 | kHz |
| 16-09.1c | 13 kHz lands at | 3 | kHz |
| 16-09.2a | image 1 | 7 | kHz |
| 16-09.2b | image 2 | 9 | kHz |
| 16-09.2c | image 3 | 15 | kHz |
| 16-09.3a | second output | 4 | — |
| 16-09.3b | third output | 8 | — |
| 16-09.4a | polyphase multiplications per second | 70000 | 1/s |
| 16-09.4b | input-rate multiplications per second | 210000 | 1/s |
| 16-09.5a | L | 160 | — |
| 16-09.5b | M | 147 | — |
| 16-09.5c | intermediate rate | 7.056 | MHz |
| 16-09.5d | naive multiplications per second | 22.58 | G/s |
| 16-09.5e | taps per phase | 20 | — |
| 16-09.5f | polyphase multiplications per second | 960000 | 1/s |
| 16-09.6a | nonzero taps | 31 | — |
| 16-09.6b | folded multipliers | 15 | — |
| 16-09.6c | multiplications per second | 720000 | 1/s |
| 16-09.7a | DC gain | 4096 | — |
| 16-09.7b | register growth | 12 | bits |
| 16-09.7c | droop at 10 kHz | −0.428 | dB |
| 16-09.7d | attenuation at 90 kHz | 57.5 | dB |
| 16-09.8a | register width | 46 | bits |
| 16-09.9a | order estimate | 93.7 | — |
| 16-09.9b | naive multiplications per second | 18.24 | M/s |
| 16-09.9c | polyphase multiplications per second | 4.56 | M/s |
| 16-09.10a | single-stage taps | 98 | — |
| 16-09.10b | single-stage folded rate | 2.352 | M/s |
| 16-09.10c | first half-band taps | 15 | — |
| 16-09.10d | second half-band taps | 59 | — |
| 16-09.10e | two-stage rate | 1.104 | M/s |
| 16-09.10f | saving | 2.13 | — |
| 16-09.11a | −3 dB frequency | 45.51 | kHz |
| 16-09.11b | impulse-response span | 20.0 | µs |
| 16-09.12a | y[0] | 1 | — |
| 16-09.12b | y[1] | 2 | — |
| 16-09.12c | y[5] | 6 | — |
