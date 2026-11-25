# Problems 24-03 · SerDes Architecture and Equalization

Chapter: [24-03](../chapters/24-03-serdes-architecture.md) · Worked solutions: [24-03 solutions](../solutions/24-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Cursors and eyes are fractions of the full swing, as in 24-02.
- Transmitter FFE taps satisfy $\sum\lvert c_j\rvert = 1$.
- The CTLE is the source-degenerated pair of §3.4, with its output pole at $1/(2\pi R_DC_L)$.
- Drivers see a 100 Ω differential termination.
- For NRZ, BER = $Q(V_{eye}/2\sigma)$. For PAM4, SER = $1.5\,Q(V_{eye}/2\sigma)$ and BER = SER/2.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-03-lab/serdes.py` or `ctle.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-03.1 [A]

**Clocking a 128 Gb/s lane.** A 128 Gb/s PAM4 lane uses a quarter-rate clock and a 64-way time-interleaved ADC. Find (a) the symbol rate and UI, (b) the clock frequency, (c) the timing error per degree of quadrature error and (d) each sub-ADC's sample rate.

### Problem 24-03.2 [A]

**Driver power.** A transmitter must deliver 1.0 V peak-to-peak differential from a 1.2 V supply. Find the power of (a) a CML driver, (b) a voltage-mode driver fed through a linear regulator and (c) a voltage-mode driver with an ideal 1.0 V supply.

### Problem 24-03.3 [B]

**One tap for a one-pole channel.** *(lab)* The first-order channel of Problem 24-02.3 has cursors $h_k = h_0e^{-2k}$ for $k \ge 0$, with $h_0 = 1 - e^{-2}$.

- (a) Show that a two-tap transmitter FFE ($c_0$, $c_1$) with $c_1/c_0 = -e^{-2}$ cancels *every* post-cursor, not just the first.
- (b) Find the taps under the peak constraint.
- (c) Find the equalized main cursor and show that it equals $\tanh 1$.
- (d) Find the de-emphasis in dB.
- (e) Find the NRZ and PAM4 eyes, and compare them with the unequalized 0.7293 and 0.1529.

### Problem 24-03.4 [B]

**Pre-cursors: FFE or FFE plus DFE?** *(lab)* A channel has $h_{-1}$ = 0.10, $h_0$ = 0.60, $h_1$ = 0.25 and $h_2$ = 0.05 (assumed).

- (a) Design the three-tap zero-forcing transmitter FFE and find the equalized cursors and NRZ eye. Compare it with the unequalized eye.
- (b) Instead, use a two-tap FFE ($c_{-1}$, $c_0$) that cancels only $h_{-1}$, followed by a DFE that cancels all post-cursors. Find the taps, the main cursor and the NRZ eye.

### Problem 24-03.5 [B]

**Designing a CTLE.** *(lab)* A degenerated pair has $g_m$ = 25 mS, $R_D$ = 160 Ω and $C_L$ = 30 fF (assumed). The design needs 12 dB of ideal peaking with its zero at 1.5 GHz.

- (a) Find $R_S$ and $C_S$.
- (b) Find both poles.
- (c) Find the DC gain.
- (d) Find the gain and the boost over DC at 13.28 GHz, the Nyquist frequency of 53.125 GBd.

### Problem 24-03.6 [B]

**Pole–zero cancellation.** A channel behaves as a single pole at 5 GHz. A CTLE places its zero at 5 GHz, its poles at 25 and 40 GHz, and its high-frequency gain at 1.

- (a) Write the combined transfer function.
- (b) Find its DC gain in dB.
- (c) Find its −3 dB bandwidth, against the channel's 5 GHz.
- (d) What has been traded for the bandwidth?

### Problem 24-03.7 [B]

**DFE timing at 64 GBd.** A DFE slice at 64 GBd has a clock-to-q of 7 ps, a summer settling time of 6 ps, a setup time of 4 ps and a multiplexer delay of 3 ps (all assumed).

- (a) Does the direct first-tap loop close?
- (b) Does the unrolled loop close, and with what slack?
- (c) How many comparators would unrolling the first *two* taps of a PAM4 DFE take?

### Problem 24-03.8 [B]

**How bursty?** An NRZ receiver with a one-tap DFE has $h_1 = 0.4h_0$. Its noise sets the error rate without propagation at 10⁻⁵. Find:

- (a) σ, with $h_0$ = 1;
- (b) the probability that an error is followed by another;
- (c) the mean burst length;
- (d) the error rate including propagation, assuming each burst starts at the 10⁻⁵ rate.

### Problem 24-03.9 [B]

**Adaptation time.** A sign-sign LMS DFE tap starts at zero and moves by $2^{-8}$ per update. Its target is 24-02's $h_1$ = 0.21088. Updates occur once every 64 UI at 53.125 GBd.

- (a) What is the fewest number of updates needed to reach the target?
- (b) How long does that take?
- (c) How large is the dither around the target, as a percentage of $h_0$ = 0.73402?

### Problem 24-03.10 [B]

**A bang-bang CDR and its jitter.** A bang-bang CDR at 64 GBd moves by $2^{-13}$ UI per vote, with transition density 0.5. Find its linearized detector gain and its loop bandwidth for input jitter of (a) 0.01 UI and (b) 0.04 UI rms. (c) Find the largest frequency offset its proportional path alone can track.

### Problem 24-03.11 [C]

**A second-order CDR against a frequency step.** A linear type-2 CDR has $\omega_n = 2\pi \times 2$ MHz and ζ = 0.707. At $t$ = 0 the incoming data's frequency jumps by 100 ppm at 53.125 GBd.

- (a) Show that the phase error is $E(s) = \Delta\omega/(s^2 + 2\zeta\omega_ns + \omega_n^2)$, where Δω is the drift rate in UI/s, and find the steady-state error.
- (b) Find the time and size of the peak phase error.
- (c) Compare with a first-order loop whose $f_c$ equals 2 MHz.

### Problem 24-03.12 [B]

**Long reach or short reach?** An accelerator has 72 lanes at 224 Gb/s. Find:

- (a) the SerDes power at 3 pJ/b;
- (b) the power at the 1.11 pJ/b of a published 224 Gb/s extra-short-reach receiver [R-509];
- (c) the saving, ignoring that the second figure covers only a receiver.

### Problem 24-03.13 [B]

**Break-even for a mixed channel.** A channel's loss at the PAM4 Nyquist frequency is half conductor loss and half dielectric loss.

- (a) Above what loss does PAM4 beat NRZ before equalization?
- (b) With 18 dB at the PAM4 Nyquist frequency, how much extra loss does NRZ suffer?
- (c) By how much does PAM4 win?

### Problem 24-03.14 [C]

**From equalized eye to BER.** Use the equalized eyes of Example 24-03.3: NRZ 0.520 with FFE and 0.709 with DFE, PAM4 0.155 with FFE and 0.219 with DFE, all at 32 GBd. The swing is 400 mV and the noise 8 mV rms.

- (a) Find the NRZ BER with each equalizer.
- (b) Find the PAM4 SER and BER with each.
- (c) Which PAM4 option would meet an FEC input target of 10⁻⁴? Which would meet 10⁻⁶?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Rates, clocks, interleaving and driver power | 1, 2 |
| 2. Transmitter FFE design | 3, 4, 14 |
| 3. CTLE zeros, poles and peaking | 5, 6 |
| 4. DFE timing, error propagation and adaptation | 4, 7, 8, 9 |
| 5. CDR loops, bang-bang gain and frequency offset | 10, 11 |
| 6. Energy per bit and modulation choice | 12, 13 |
