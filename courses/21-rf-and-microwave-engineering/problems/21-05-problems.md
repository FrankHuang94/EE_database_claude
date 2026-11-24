# Problems 21-05 · Mixers

Chapter: [21-05](../chapters/21-05-mixers.md) · Worked solutions: [21-05 solutions](../solutions/21-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Mixers are ideal hard-switched commutators unless stated; conversion gains are voltage ratios ($20\log_{10}$); powers are in dBm referred to 50 Ω; a peak amplitude $A$ across 50 Ω carries $A^2/100$ W. Problems marked *(lab)* can be checked with `labs/21-05-lab/mixer.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-05.1 [A]

**High-side LO.** A 5.80 GHz Wi-Fi signal is converted to a 100 MHz IF with a high-side LO. Find the LO frequency and the image.

### Problem 21-05.2 [A]

**A single switch versus a balanced pair.** Find the conversion gain of an ideal single-switch (0/1, unbalanced) mixer in dB, and how much less it is than a balanced (±1) one.

### Problem 21-05.3 [A]

**Sizing a Gilbert cell.** What transconductance gives a Gilbert mixer 12 dB of conversion gain with 400 Ω loads?

### Problem 21-05.4 [B]

**An image-rejection budget.** (a) What IRR do a 3% gain error and a 0.5° phase error give? (b) With a 0.3° phase error, what gain error still gives 45 dB?

### Problem 21-05.5 [B]

**Phase error alone.** Show that with no gain error the exact IRR is $\cot^2(\theta/2)$, and evaluate it for θ = 2°, exactly and from $4/\theta^2$.

### Problem 21-05.6 [B]

**Which noise folds?** An otherwise noiseless switching mixer is preceded by a filter that removes everything above $2f_{LO}$ but passes the image. What is its SSB noise figure? What if the filter removes everything above $4f_{LO}$, so the bands around $3f_{LO}$ also pass?

### Problem 21-05.7 [B]

**An active-mixer receiver.** An LNA (18 dB, NF 1.2 dB) drives an active mixer (conversion gain 10 dB, SSB NF 12 dB) and a baseband stage (30 dB, NF 20 dB). Find the cascade noise figure.

### Problem 21-05.8 [B]

**IP3 and LO drive.** A mixer with IP3 = 15 dBm sees two −10 dBm tones. What is the IM3 level? What IP3 is needed to bring it to −70 dBc?

### Problem 21-05.9 [B] *(lab)*

**Harmonic-reject mismatch.** For the three-phase harmonic-reject LO, find the 3rd- and 5th-harmonic responses with a 2% error in the $\sqrt2$ weight, and with a 0.5° error in the +45° phase. Compare the weight-error result with the estimate $\delta/6$.

### Problem 21-05.10 [B]

**Designing an N-path filter.** Choose C for an 8-path filter with 50 Ω source resistance and a 20 MHz bandwidth. What is its centre loss?

### Problem 21-05.11 [C]

**Self-mixing.** In a zero-IF receiver the LO reaches the mixer with 0.3 V amplitude, and 60 dB of LO-to-RF isolation lets a 0.3 mV copy reach the RF input. (a) What DC offset can self-mixing produce at the IF output? (b) A −90 dBm wanted signal arrives at the RF input (50 Ω). Compare its IF amplitude with the offset. (c) What happens after 60 dB of baseband gain, and what do receivers do about it?

### Problem 21-05.12 [C]

**A wideband frequency plan.** A zero-IF receiver tunes from 50 to 800 MHz with a square-wave LO and no tracking filter. Over what LO range does the 3rd-harmonic response fall inside the tuning range, and the 5th? What does that imply for the mixer?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Frequency plans, images and harmonic responses | 1, 12 |
| 2. Conversion gain of switching and Gilbert mixers | 2, 3 |
| 3. Image rejection and its error budget | 4, 5 |
| 4. Mixer noise: SSB, DSB and folding | 6, 7 |
| 5. Harmonic-reject mixers | 9, 12 |
| 6. N-path filters, LO leakage, linearity | 8, 10, 11 |
