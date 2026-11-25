# Problems 24-04 · DSP-Based SerDes and FEC

Chapter: [24-04](../chapters/24-04-dsp-serdes-and-fec.md) · Worked solutions: [24-04 solutions](../solutions/24-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- PAM4 levels are ±1 and ±1/3. The PAM4 signal rms is $\sqrt{5/9}$.
- Quantization noise is $\Delta/\sqrt{12}$.
- Jitter-limited SNR is $-20\log_{10}(2\pi f\sigma_t)$. Random interleaving skew is treated like jitter.
- Independent noise powers add.
- NCG uses the BPSK-equivalent convention of §3.5.
- An RS(544,514) codeword is 5,440 bits.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-04-lab/dsp.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-04.1 [A]

**Less headroom, one more bit.** A 7-bit ADC has a full scale of ±1.25 times the outer PAM4 level. Find (a) the step, (b) the quantization noise, (c) the SQNR for a PAM4 signal and (d) the ratio of the ISI-free half-eye (1/3) to the quantization noise.

### Problem 24-04.2 [A]

**Jitter budgets.** What rms sampling jitter keeps the jitter-limited SNR at (a) 30 dB at 53.125 GHz and (b) 38 dB at 26.5625 GHz?

### Problem 24-04.3 [B]

**Which noise to fix?** A receiver's SNR terms are 30 dB from thermal noise and crosstalk, 34.8 dB from quantization and 35.6 dB from sampling jitter (assumed). (a) Find the total SNR. (b) Find the total if each term in turn were removed entirely. Which is worth improving first?

### Problem 24-04.4 [B]

**A 128-way ADC.** A 106.25 GS/s ADC has 128 slices. (a) At what rate does each slice sample? (b) At what frequencies do offset-mismatch spurs appear? (c) What rms skew keeps the skew-limited SNR at 32 dB for a 26.5625 GHz input?

### Problem 24-04.5 [B]

**DSP energy.** A 212.5 Gb/s PAM4 receiver runs a 40-tap FFE at 30 fJ per MAC and a 4-state MLSD whose 16 branch-metric updates per symbol cost 10 fJ each (all assumed). Find (a) the FFE's power, (b) the MLSD's power and (c) their combined energy per bit.

### Problem 24-04.6 [B]

**MLSD gains.** *(lab)* For NRZ on (a) $h = (1, 0.75)$ and (b) $h = (1, 0.5, 0.25)$, find MLSD's minimum squared distance and its gain over an ideal DFE. Check that no multi-symbol error event is closer than a single error.

### Problem 24-04.7 [A]

**Viterbi complexity.** (a) How many states and branches per symbol does a PAM4 detector for a four-tap response ($L$ = 3) need? (b) An NRZ detector for the same response? (c) How many branch-metric updates per second does a PAM4 detector with $L$ = 1 perform at 106.25 GBd?

### Problem 24-04.8 [B]

**Latency stacks up.** A 212.5 Gb/s lane interleaves 4 RS(544,514) codewords, takes 100 ns to decode (assumed) and adds an inner code whose interleaver adds 56 ns [R-513]. Find (a) the accumulation time, (b) the total without the inner code and (c) the total with it.

### Problem 24-04.9 [B]

**NCG of a hypothetical code.** A rate-0.9 code takes an input BER of 10⁻³ to 10⁻¹⁵ (assumed). Find its NCG and compare it with KP4's 6.83 dB at 10⁻¹⁵.

### Problem 24-04.10 [C]

**From 200 GbE to the line rate.** 200 Gb/s Ethernet transcodes its data 256b/257b and adds RS(544,514) parity. (a) Find the resulting bit rate and the PAM4 symbol rate. (b) Adding the (128,120) inner code and padding gives 113.4375 GBd; what is the total overhead relative to 200 Gb/s? (c) What is the overhead without the inner code?

### Problem 24-04.11 [B]

**How often does PCIe retry?** A x16 PCIe link at 64 GT/s carries 256-byte flits, with a first-bit error rate of 10⁻⁶ and a retry probability of 5 × 10⁻⁶ per flit [R-059]. Find (a) the flits per second, (b) the retries per second and (c) the probability that a flit contains at least one bit error before FEC.

### Problem 24-04.12 [C]

**Interleaving against bursts.** RS(544,514) has 10-bit symbols and corrects 15 symbols per codeword. (a) What is the longest burst of bit errors one codeword always corrects? (b) With symbols interleaved round-robin over 4 codewords, what is the longest burst always corrected?

### Problem 24-04.13 [A]

**A round trip.** A request and its response each cross two PHY links. What FEC latency does the round trip accumulate with (a) 151 ns per Ethernet PHY crossing and (b) 2 ns per PCIe-style flit FEC?

### Problem 24-04.14 [C]

**An MMSE equalizer by hand.** NRZ symbols ±1 (independent, equally likely) cross the channel $x_n = a_n + 0.5a_{n-1} + w_n$ with white noise of variance 0.01. A two-tap FFE forms $z_n = c_0x_n + c_1x_{n-1}$ to estimate $a_n$. (a) Write the normal equations $\mathbf R\mathbf c = \mathbf p$ and solve for the MMSE taps. (b) Find the minimum mean-square error. (c) Compare with the zero-forcing taps (1, −0.5): find their residual ISI and total mean-square error. Why does MMSE do better?

### Problem 24-04.15 [C]

**A Viterbi trace.** *(lab)* The channel is $y_n = a_n + 0.5a_{n-1}$ plus noise, with NRZ symbols and $a_{-1} = +1$ known. The receiver sees $y$ = (1.6, 0.4, −1.3, −0.7). (a) Run the two-state Viterbi algorithm by hand with squared-error branch metrics, giving both path metrics after each sample. (b) Trace back the most likely sequence and its metric. (c) Compare with a plain slicer and with a one-tap DFE ($z_n = y_n - 0.5\hat a_{n-1}$).

### Problem 24-04.16 [B]

**How often does KP4 fail?** *(lab)* RS(544,514) uses 10-bit symbols and corrects up to 15 symbol errors. With independent bit errors at 2.4 × 10⁻⁴, find (a) the symbol error probability, (b) the mean number of symbol errors per codeword and (c) the probability that a codeword has more than 15 (binomial).

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Why ADC and DSP | 3, 5 |
| 2. ADC resolution, jitter and skew | 1, 2, 3, 4 |
| 3. Digital FFE arithmetic, energy and MMSE design | 5, 14 |
| 4. MLSD distance gain, complexity and the Viterbi algorithm | 6, 7, 15 |
| 5. FEC gain, line rate, latency, retry | 8, 9, 10, 11, 12, 13, 16 |
