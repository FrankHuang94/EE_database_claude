# Problems 21-08 · Transceiver Architectures

Chapter: [21-08](../chapters/21-08-transceiver-architectures.md) · Worked solutions: [21-08 solutions](../solutions/21-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Preselectors and IF filters are Butterworth band-pass filters with the stated centre and 3 dB bandwidth (§3.1). Image rejection uses the IRR formula of 21-05. Noise floors use −174 dBm/Hz at 290 K. Problems marked *(lab)* can be checked with `labs/21-08-lab/trx.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-08.1 [A]

**Low-side LO.** A 1.9 GHz receiver uses a 200 MHz IF with a low-side LO. Find (a) the LO and (b) the image.

### Problem 21-08.2 [A]

**Preselector order.** *(lab)* The preselector of Problem 21-08.1 is centred at 1.9 GHz with 60 MHz bandwidth. Find its attenuation at the image for orders (a) 1, (b) 2 and (c) 3, and (d) the order needed for 50 dB.

### Problem 21-08.3 [B]

**A dual-conversion plan.** A 5.8 GHz receiver converts first to a 1.2 GHz IF with a high-side LO, then to 10 MHz with a low-side second LO. Find (a) LO1, (b) the first image, (c) LO2 and (d) the second image. (e) A second-order first-IF filter (20 MHz bandwidth at 1.2 GHz) attenuates the second image by how much, and (f) what order would give 60 dB?

### Problem 21-08.4 [B]

**More spurs.** *(lab)* For Problem 21-08.1's plan (LO 1.7 GHz, IF 200 MHz), find (a, b) the responses to the LO's third harmonic, (c, d) the half-IF spurs, and (e, f) the third-order preselector's attenuation at each half-IF spur.

### Problem 21-08.5 [B]

**What does 35 dB of image rejection allow?** A zero-IF receiver achieves 35 dB IRR. (a) What EVM floor does I/Q mismatch set? (b) What share of a 2.5% EVM budget (base-station 1024-QAM) does it use?

### Problem 21-08.6 [B]

**Flicker noise in zero-IF.** A baseband has white noise density $S_0$ plus flicker noise with a 200 kHz corner, $S(f) = S_0(1 + f_c/f)$; the DC notch removes everything below 10 kHz. How much does flicker raise the noise in (a) a 1 MHz channel and (b) a 100 MHz channel?

### Problem 21-08.7 [A]

**IIP2.** The transmit leakage reaching a receiver is −30 dBm; its in-channel noise floor is −100 dBm. What IIP2 keeps the second-order product 6 dB below the noise?

### Problem 21-08.8 [B]

**A low-IF Wi-Fi-class receiver.** A low-IF receiver uses a 2 MHz IF. The adjacent channel may be 25 dB stronger and the demodulator needs 12 dB SNR. Find (a) the required IRR and (b, c) equal-share gain and phase errors. (d) What image selectivity does a fourth-order complex Butterworth filter with $f_p$ = 1 MHz centred on +2 MHz give?

### Problem 21-08.9 [A]

**Nyquist zones.** *(lab)* An ADC samples at 3 GS/s. In which zone and at what frequency does (a, b) a 2.45 GHz and (c, d) a 5.8 GHz signal appear?

### Problem 21-08.10 [B]

**Jitter and noise density.** (a) What rms jitter allows 60 dB SNR at 6 GHz? (b) An ADC with 60 dB full-band SNR samples at 3 GS/s: what is its noise spectral density?

### Problem 21-08.11 [C]

**The RF-sampling front-end trade.** An ADC has a 25 dB noise figure and +2 dBm full scale; the LNA has a 1 dB noise figure. (a) What LNA gain gives a 2.5 dB cascaded noise figure? (b) With that gain, how large a blocker can the LNA input take while staying 6 dB below full scale? (c) To remove such blockers, a filter with 1.5 dB loss is placed before the LNA: what is the new cascaded noise figure with the same gain?

### Problem 21-08.12 [B]

**Transmit sideband budget.** A direct-conversion transmitter must achieve 40 dB sideband suppression. With a 0.5° phase error, (a) what gain error is allowed (small-error formula), and (b) what does the exact formula then give?

### Problem 21-08.13 [C]

**Transmit noise in FDD.** A PA delivers 26 dBm; the duplexer isolates the receiver by 45 dB; the receiver's noise figure is 4 dB, and the leaked transmit noise must be 6 dB below its noise floor. (a) What transmit noise density is allowed in the receive band, and (b) relative to the carrier? (c) If the PA alone produces −135 dBm/Hz in the receive band, what isolation is needed?

### Problem 21-08.14 [A]

**Counting chains.** A phone must receive four aggregated carriers on four antennas each, plus a dedicated GNSS receiver. How many receive chains does that require?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Superheterodyne frequency planning and spurs | 1, 2, 3, 4 |
| 2. Zero-IF impairments and requirements | 5, 6, 7 |
| 3. Low-IF and complex filtering | 8 |
| 4. Direct RF sampling | 9, 10, 11 |
| 5. Transmitter budgets | 12, 13 |
| 6. Architectures in products | 14, 11 |
