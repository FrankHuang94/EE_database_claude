# Course 00 · Final Exam (Orientation)

**Time limit:** 90 minutes. **Allowed:** a calculator (or Python) and [reference/notation.md](../../../reference/notation.md). No notes.
**Instructions:** answer all 13 questions and show your method. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (104 points in total; 73 or more, about 70%, is a strong pass). Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

---

**1 [A].** A phone battery is rated 5,000 mAh at 3.87 V. Find its energy in Wh, and the average power it can supply for a 30-hour battery life.

**2 [A].** A 224 Gb/s SerDes lane consumes 4 pJ/bit. What power does one lane use? What do 32 lanes use?

**3 [B].** A 30 cm circuit-board trace carries signals at $1.5\times10^8$ m/s. Is it lumped ($\ell < \lambda/10$) at (a) 1 GHz and (b) 10 MHz? Give its length in wavelengths for each.

**4 [A].** A logic family has $V_{OL} = 0.15$ V, $V_{OH} = 1.05$ V, $V_{IL} = 0.45$ V and $V_{IH} = 0.75$ V. Compute $NM_L$ and $NM_H$.

**5 [B].** A digital chain makes a decision at each stage with distance 0.45 V to the threshold and per-stage Gaussian noise σ = 0.1 V. Find the per-stage error probability and the probability of at least one error over 1,000 stages.

**6 [C].** A 1 V step from a source with $R_s = 30\ \Omega$ drives a 50 Ω transmission line, open at the far end. Find the source reflection coefficient, the launched wave, and the far-end voltage after the first and second arrivals.

**7 [A].** (a) What is the value of `C1 a b 10M` in SPICE? (b) A 3.3 V source drives 10 kΩ in series with 20 kΩ to ground. What voltage appears across the 20 kΩ resistor?

**8 [B].** For $x = 10^{16}$, `math.sqrt(x+1) - math.sqrt(x)` returns 0.0. Explain why, rewrite the expression in a stable form, and evaluate it.

**9 [B].** Check the units and say which are dimensionally valid: (a) $E = \tfrac{1}{2}CV^2$; (b) $f = R/(2\pi L)$; (c) $\tau = \sqrt{LC}$; (d) $P = I^2/R$.

**10 [B].** A processor has 30 billion transistors at 2.5 GHz, with 2% average activity and 0.4 fJ per switch (illustrative). Estimate its dynamic power, and say whether the answer is plausible.

**11 [B].** A chip integrates 40 independent blocks, each 99.5% likely to be bug-free. What is the probability of first-silicon success?

**12 [C].** Two sequential phases have triangular durations (min, most likely, max) of (8, 10, 15) and (12, 14, 22) weeks. Find the sum of the most-likely values and the expected total duration. Explain to a non-engineer why the "most likely" plan is likely to be late.

**13 [C].** A 40 MHz channel has SNR = 15 dB. Find its Shannon capacity. Would you rather double the bandwidth or double the SNR, and why?
