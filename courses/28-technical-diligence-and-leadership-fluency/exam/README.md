# Course 28 · Final Exam (Technical Diligence and Engineering Leadership Fluency)

**Time limit:** 210 minutes, best taken in two sittings: Questions 1–6 (about 100 minutes), then Questions 7–12 (about 110 minutes).
**Allowed:** a scientific calculator and the [Course 28 equation sheet](../../../reference/equation-sheets/28-technical-diligence-and-leadership-fluency.md) printed without its chapter links. No notes, no Python and no spreadsheet.

**Instructions.**

- Answer all 12 questions and show every step.
- Scoring:
  - Questions 1–10 are [B] and worth 8 points each, 2 per part.
  - Questions 11 and 12 are [C] and worth 12 points each, 3 per part.
  - The total is 104 points; 73 or more (70%) is a strong pass.
- Give numerical answers to 3 significant figures, with units, unless a part asks otherwise; exact values may be given in full. Carry intermediate values at full precision and round only final answers.
- Two parts need a short iteration on the calculator (bisection is fine): 3(d) only if you do not use the closed form, and 11(c). Say what you iterated on.
- Questions 11(b) and 12(a) ask for derivations: a result quoted from the equation sheet earns no credit unless derived. Question 12(d) is a short written answer; its rubric is at the end of the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- A year is 8,766 hours. Boltzmann's constant is $8.617 \times 10^{-5}$ eV/K; temperatures in kelvin are °C + 273.15.
- Dies per wafer use $\pi d^2/(4A) - \pi d/\sqrt{2A}$ for a 300 mm wafer, rounded down unless stated; yield is $e^{-AD_0}$.
- Decode intensity is $2B/b_w$ FLOP per byte; TPP is $2 \times \text{MacTOPS} \times$ bit length.
- Ideal class-B efficiency is $(\pi/4)10^{-\text{BO}/20}$; an ideal symmetric Doherty below half amplitude has twice that.
- "Assumed" values are illustrative; sourced values carry the research-log IDs used in the chapters.

---

**1 [B] · Scorecards, evidence and value.** (28-01)
Weights 0.3, 0.3, 0.2 and 0.2. Target A scores 4, 4, 2, 5; target B scores 3, 4, 4, 3.
(a) Find the weighted arithmetic and geometric scores of each target.
(b) The prior that A's key claim holds is 0.35. Two independent pieces of evidence have likelihood ratios 4 and 0.6. Find the posterior odds and probability.
(c) Buying A is worth +$300M if the claim holds and −$150M if not. At the posterior of (b), find the expected value of buying and the expected value of perfect information.
(d) A $120M earn-out is paid in 2 years if the claim holds. Find its expected present value at 12%, using the posterior of (b).

**2 [B] · An NPU brochure.** (28-02)
An NPU has 16,384 INT8 MAC units at 1.5 GHz; its brochure says "98 TOPS" and "24.5 TOPS/W" at 4 W.
(a) Find the dense INT8 peak and its ratio to the brochure figure. What could explain the ratio?
(b) Find the TPP.
(c) With 51.2 GB/s of memory bandwidth, a model with an intensity of 100 operations per byte is memory-bound. Find the attainable throughput and its share of the dense peak.
(d) At 4 W, find the delivered TOPS/W in (c) and compare it with the brochure.

**3 [B] · Maturity and qualification.** (28-03)
(a) A programme has completed engineering samples; qualification (0.85, 5 months) and release (0.95, 2 months) remain. Find the probability of production and the value multiplier at 15% a year.
(b) Find the Arrhenius acceleration factor between a 60 °C use junction and a 125 °C stress junction at 0.7 eV.
(c) 300 devices run 1000 hours at 125 °C with no failures. Find the FIT bound at 60% confidence ($\chi^2_{0.6;2} = 1.833$).
(d) How many devices would a zero-failure 1000-hour test need to bound the rate at 20 FIT with 90% confidence ($\chi^2_{0.9;2} = 4.605$)?

**4 [B] · Digital and AI claims.** (28-04)
(a) A CPU claims 18% more performance at the same power, with 8% more IPC and 4% more switched capacitance. Find the frequency ratio, the power factor and the required reduction in energy per operation.
(b) An accelerator has 4 PFLOP/s of dense FP8 and 8 TB/s. Find the ridge, the decode intensity at batch 24 with FP8 weights, the attainable throughput and share of peak, and the batch at the ridge.
(c) Find the bandwidth of one 2,048-bit HBM4 stack at 9.6 Gb/s, and of six stacks.
(d) Find the power of six such stacks at full read bandwidth at 6.5 pJ/bit.

**5 [B] · Interconnect and optics.** (28-04)
(a) A 102.4 Tb/s switch's SerDes draw 4.5 pJ/bit all-in. Find their power.
(b) Two chiplets exchange 3 TB/s over UCIe-A links at 0.25 pJ/bit [R-524]. Find the link power and the die edge needed at 1,317 GB/s per mm.
(c) A 1.6 Tb/s port draws 25 W with pluggable optics and 6 W with CPO. Find each energy per bit.
(d) An external laser delivers 23 dBm per fiber. Find its optical power in mW and its electrical power at 20% wall-plug efficiency.

**6 [B] · Analog and RF claims.** (28-05)
(a) A 2 GS/s ADC reports 58 dB SNDR near Nyquist at 80 mW. Find its Schreier figure and ENOB.
(b) What clock jitter alone would limit SNR to 58 dB for a 3 GHz input?
(c) Find the ideal class-B and symmetric-Doherty efficiencies at 9 dB back-off.
(d) Express a 2% EVM requirement in dB.

**7 [B] · Power, packaging and embedded.** (28-05)
(a) A 6 kW supply runs at 97% or 98% efficiency. Find each loss and the difference.
(b) A chain of 97.5%, 96% and 90% stages feeds an 800 W load. Find the chain efficiency, the input power and the total loss.
(c) A package holds one die (99.5% survival) and four stacks (99.7% each), with 99% assembly yield. Find the package yield.
(d) A node sleeps at 0.9 µA, runs at 2.5 mA for 6 ms every 4 s, and transmits at 5 mA for 1.5 ms every 20 s. Find its average current and its life on 220 mAh.

**8 [B] · Flags.** (28-06)
(a) A flag appears in 70% of troubled and 15% of healthy companies. Find its positive and negative likelihood ratios.
(b) With a base rate of 25%, find the posterior probability of trouble when the flag is present and when it is absent.
(c) A checklist has 30 independent flags, each with a 3% false-positive rate. Find the probability that a healthy company shows at least one and the expected number.
(d) Troubled companies show each flag with probability 25%. For the threshold "three or more flags", find the sensitivity, the false-positive rate and the likelihood ratio.

**9 [B] · Teams.** (28-07)
(a) With a Beta prior of mean 14% and weight 10, find the posterior mean first-silicon success rate for a team with 2 successes in 5 projects, and the weight on its record.
(b) Find the 90% credible interval of that posterior.
(c) A team's last three projects took 1.10, 1.30 and 1.45 times plan. Find the geometric-mean overrun, the forecast for a 20-month plan, the standard deviation of the log-ratios ($n - 1$) and the probability of meeting the plan.
(d) Engineers leave at 15% a year. Over two years, find the probability of losing a capability with one owner and with two.

**10 [B] · Integration.** (28-08)
(a) Synergies of $40M a year for 5 years at 10%: find the planned value, the value if integration slips a year with 75% realization, and the fractional loss.
(b) Migrating 30 engineers takes 5 months at $25k per engineer-month; done now it would delay a product earning $120M a year in a fixed window by 2 months. Find both costs.
(c) Two programs for a $180M socket succeed with probabilities 0.55 and 0.45 (independent); keeping the second costs $35M. Find the probability that at least one succeeds, the expected value with both and with the better alone, the gain, and the decision.
(d) A deal pays $500M upfront and $300M contingent (all-or-nothing) in 3 years with probability 0.45, at 10%. Find the contingent part's expected present value and the deal's.

**11 [C] · Translation.** (28-09)
(a) A 150 mm² die is built on a \$20,000 wafer with $D_0$ = 0.0008 per mm². Find the dies per wafer, the yield and the cost per good die.
(b) Derive the elasticity of die cost to area, ignoring the wafer edge, and evaluate it for this die. Then find the actual cost increase and average elasticity if the die grows 10% (dies per wafer rounded down).
(c) The part sells at $120 with $12 of package and test. Find its gross margin, and the largest die area (unrounded dies per wafer) that would give 65%.
(d) Devices draw 450 W and 400 W at equal performance; PUE 1.3, $0.09 per kWh, 4 years. Find each lifetime energy cost, the saving, and the capacity gain in a fixed power budget.

**12 [C] · Conversation and calibration.** (28-10)
(a) Derive the expected Brier score of reporting $p$ when the true probability is $q$, and show that it is minimized by $p = q$.
(b) After a meeting (prior 0.45), the answers' likelihood ratios are 3 (on fact A), 2 (fact B), 0.5 (fact C), 3 (fact A again) and 0.8 (fact D). Find the posterior odds and probability if all are counted, and if fact A is counted once.
(c) Five forecasts were 0.9, 0.7, 0.6, 0.3 and 0.8; the first two claims came true and the last three did not. Find the Brier score and compare it with always saying 0.5.
(d) A target claims the "best performance per watt of any edge NPU". Write three questions you would ask, each with what a strong answer must contain.
