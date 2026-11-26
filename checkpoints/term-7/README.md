# Term 7 Checkpoint · FE-Style Practice Exam

**Covers:** Courses 26–28: engineering design and professional practice (requirements, reviews, engineering economics, schedule and risk, teams, ethics); system architectures; and technical diligence. **Questions:** 50 (multiple choice and numeric entry). **Time:** 150 minutes, the FE pace of about 3 minutes per question.
**Materials:** an FE-approved calculator and the *NCEES FE Reference Handbook* only (free PDF from NCEES); no course notes or sheets. The handbook has the interest factors and the standard normal table. Relations it does not contain are given in the conventions below or in the question.
**Scoring:** one point per question. Score each block separately and aim for at least 70% in every block. Blocks 1 and 3 are the FE's Engineering Economics and Ethics and Professional Practice areas. Write every miss into your error log with its cause, and re-solve it a week later. Solutions with full explanations, each pointing to the chapter to revisit, are in [solutions.md](solutions.md); open them only after you finish.

**Conventions:**

- For numeric entry, give 3 significant figures unless the question says otherwise.
- Money: cash flows at the end of each period unless stated; $i$ is the interest rate per period; "\$k" and "\$M" are thousands and millions of dollars.
- Time: a year is 8,760 h; a FIT is one failure per $10^9$ device-hours.
- Probability: $\Phi$ is the standard normal CDF; odds $= p/(1 - p)$, and posterior odds = prior odds × the product of the likelihood ratios of conditionally independent answers.
- Relations not in the handbook:
  - PERT: mean $(a + 4m + b)/6$, standard deviation $(b - a)/6$.
  - Expected escapes after $k$ independent reviews, each catching a fraction $p$: $N(1 - p)^k$.
  - Flat-team output with coordination cost $c$: $O(n) = n[1 - c(n - 1)]$.
  - Worst-case classic CAN frame with $n$ data bytes: $34 + 8n + 13 + \lfloor(34 + 8n - 1)/4\rfloor$ bits.
  - Ring all-reduce time, ignoring latency: $2\frac{p - 1}{p}\frac{S}{B}$.
  - Export control: TPP $= 2 \times$ MacTOPS $\times$ bit length.

---

## Block 1 · Engineering economics (questions 1–12)

**1.** *Numeric entry.* \$10,000 is invested at 6% a year, compounded annually, for 8 years. Find its future value, in \$k.

**2.** At 8% a year, the present worth of \$50,000 received at the end of each of the next 10 years, in \$k, is:
(A) 232 · (B) 500 · (C) 336 · (D) 362

**3.** *Numeric entry.* A \$2M test cell lasts 5 years and has a \$200k salvage value. At a MARR of 10%, find its annual capital-recovery cost, $P(A/P) - S(A/F)$, in \$k.

**4.** A loan carries a nominal 12% a year, compounded monthly. Its effective annual rate is:
(A) 12.0% · (B) 12.6% · (C) 1.00% · (D) 12.7%

**5.** *Numeric entry.* A chip program costs \$40M now and returns \$15M at the end of each of the next 5 years. At 12%, find its net present value, in \$M.

**6.** An investment of \$100 now returns \$60 at the end of year 1 and \$60 at the end of year 2. Its internal rate of return is:
(A) 13.1% · (B) 20.0% · (C) 10.0% · (D) 6.54%

**7.** *Numeric entry.* A part needs \$60M of NRE, sells at \$25 and costs \$10 to build. Find its break-even volume, in millions of units.

**8.** Test equipment costs \$5M, lasts 8 years and has a \$1M salvage value. With straight-line depreciation and a 25% tax rate, the annual tax shield, in \$k, is:
(A) 156 · (B) 500 · (C) 375 · (D) 125

**9.** *Numeric entry.* A die costs \$20 and its package \$5; assembly yields 98%; final test costs \$2 and passes 95% of the assembled parts. The part sells for \$60. Find its gross margin, in percent, with yields dividing the accumulated cost.

**10.** A team can license an IP block for a \$3M fee plus a royalty of \$0.50 per unit, or build it for \$8M of NRE with a 20% chance of a \$5M respin. The discounted volume at which the two cost the same, in millions of units, is:
(A) 10.0 · (B) 18.0 · (C) 16.0 · (D) 12.0

**11.** *Numeric entry.* A cleanroom upgrade costs \$3M now and \$400k a year to maintain, forever. At 8%, find its capitalized cost, in \$M.

**12.** An accelerator draws 1 kW for 4 years in a facility with a PUE of 1.25, at \$0.10 per kWh. Its lifetime electricity cost, in \$k, is:
(A) 3.50 · (B) 4.38 · (C) 1.10 · (D) 5.48

## Block 2 · Requirements, reviews, schedule and teams (questions 13–20)

**13.** *Numeric entry.* A sensor node draws 5 µA asleep (99% of the time) and 2 mA awake (1%). It runs from a 220 mAh cell of which 80% is usable. Find its battery life, in days.

**14.** Three independent error sources have standard deviations of 3, 4 and 12 mV. The standard deviation of their sum is:
(A) 19.0 mV · (B) 13.0 mV · (C) 11.0 mV · (D) 169 mV

**15.** *Numeric entry.* A design has 50 defects. Four reviewers inspect it independently, and each catches 40% of the defects. Find the expected number of defects that escape all four.

**16.** A path has three independent tasks, each with PERT estimates of 4, 6 and 14 weeks (optimistic, most likely, pessimistic). With a normal approximation, the probability that the path finishes within 24 weeks is:
(A) 72.6% · (B) 96.4% · (C) 98.1% · (D) 85.1%

**17.** *Numeric entry.* A chip's first tape-out succeeds with probability 0.3; each respin after it succeeds with probability 0.8, and each respin adds 4 months. Find the expected delay from respins, in months.

**18.** A team of 20 engineers has how many pairwise communication channels?
(A) 190 · (B) 380 · (C) 20 · (D) 210

**19.** *Numeric entry.* In a flat team each engineer loses a fraction $c$ = 0.04 of their time for every other team member. Find the largest output the team can reach, in engineer-equivalents.

**20.** A risk has a 30% chance of costing \$10M. A \$1.2M mitigation cuts the chance to 15%. The mitigation's expected saving net of its cost, in \$M, is:
(A) 1.80 · (B) 1.20 · (C) 0.30 · (D) 1.50

## Block 3 · Ethics, safety and intellectual property (questions 21–26)

**21.** *Numeric entry.* A hazardous failure has a probability of $2 \times 10^{-7}$ per unit per year. Find the probability that at least one of 5 million units fails this way in a year, in percent.

**22.** An engineer warns that a firmware change could silence a medical device's alarm. Her manager overrules her and ships it. Under the NSPE Code of Ethics she should:
(A) comply, because she is the employer's faithful agent · (B) notify her employer and other appropriate authority, because public safety is paramount · (C) resign without saying why · (D) publish the firmware on the internet so users can judge

**23.** *Numeric entry.* A part has shown zero failures in $3 \times 10^8$ device-hours. Find the 95% upper confidence bound on its failure rate, $-\ln(1 - C)/T$, in FIT.

**24.** An engineer moving to a competitor wants to bring her former employer's production test limits, which it keeps confidential. Those limits are protected as:
(A) a trade secret · (B) a copyright · (C) a patent · (D) a mask work

**25.** *Numeric entry.* A chip's layout is first exploited commercially on 15 March 2021 and registered as a mask work on 1 February 2022. US mask-work protection starts on the earlier of the two dates, lasts ten years, and then runs to the end of the calendar year in which those ten years expire. In what year does it end?

**26.** An accelerator delivers 1,000 dense INT8 TOPS. Its total processing performance is:
(A) 4000 · (B) 16000 · (C) 8000 · (D) 1000

## Block 4 · System architectures (questions 27–38)

**27.** *Numeric entry.* A battery feeds three rails: 1.2 W through a buck at 90% efficiency, 0.5 W through a buck at 85%, and 0.3 W through an LDO from a 1.8 V bus down to 1.2 V (treat the bus as drawn from the battery without loss, and the LDO's efficiency as $V_{out}/V_{in}$). Find the battery power, in W.

**28.** A phone's skin may reach 43 °C in 25 °C air, and its skin-to-ambient thermal resistance is 6 K/W. Its sustained power is:
(A) 7.17 W · (B) 3.00 W · (C) 4.17 W · (D) 108 W

**29.** *Numeric entry.* A 64-bit LPDDR5X interface runs at 8533 MT/s. Find its peak bandwidth, in GB/s.

**30.** An 8-billion-parameter model stored at 4 bits per parameter decodes from a 68.3 GB/s memory. If every token reads all the weights once, its bandwidth-bound decode rate, in tokens/s, is:
(A) 8.54 · (B) 34.2 · (C) 2.13 · (D) 17.1

**31.** *Numeric entry.* A watch's battery stores 300 mAh at 3.85 V, of which 90% is usable, and its converters are 85% efficient. Per day its rails use 20 mW for 2 h (display), 2 mW for 24 h (sensors), 5 mW for 1 h (radio) and 0.6 mW for 24 h (sleep). Find its battery life, in days.

**32.** An earbud's ANC has perfect gain and a 50 µs delay. At 500 Hz the residual is $2\lvert\sin(\pi f\tau)\rvert$ of the noise, so the attenuation is:
(A) 8.04 dB · (B) 22.1 dB · (C) 16.1 dB · (D) 10.0 dB

**33.** *Numeric entry.* Find the worst-case transmission time of a classic CAN frame with 8 data bytes at 500 kb/s, in µs.

**34.** A car at 30 m/s brakes at 7 m/s² after a 0.1 s perception-to-actuation latency. Its stopping distance is:
(A) 64.3 m · (B) 67.3 m · (C) 132 m · (D) 70.3 m

**35.** *Numeric entry.* A rack holds 8 servers, each with 8 accelerators at 1.0 kW and 2 kW of CPUs, memory and NICs, plus 6 kW of fans. Its power conversion is 95% efficient and the facility's PUE is 1.2. Find the facility power the rack needs, in kW.

**36.** A 70-billion-parameter model trains on $2 \times 10^{12}$ tokens with about $6ND$ FLOPs, on 4,096 accelerators of $10^{15}$ FLOP/s each at 40% utilization. The training time is:
(A) 2.37 days · (B) 1.98 days · (C) 14.8 days · (D) 5.93 days

**37.** *Numeric entry.* Eight accelerators all-reduce 12 GB of gradients over a ring with 400 GB/s per direction per link. Ignoring latency, find the all-reduce time, in ms.

**38.** A 3 × 3 convolution with 64 output channels is replaced by a depthwise-separable one. The separable layer needs what fraction of the original multiply-accumulates?
(A) 11.1% · (B) 12.7% · (C) 1.56% · (D) 87.3%

## Block 5 · Technical diligence (questions 39–50)

**39.** *Numeric entry.* Your prior that a target's claim is true is 0.3. Three conditionally independent answers have likelihood ratios 3, 0.4 and 2. Find the posterior probability, in percent.

**40.** A red flag appears at 60% of troubled targets and 10% of healthy ones. When the flag is absent, its likelihood ratio is:
(A) 0.444 · (B) 6.00 · (C) 0.400 · (D) 0.111

**41.** *Numeric entry.* A Beta prior has mean 0.14 and weight 10 (prior successes 1.4 in 10 notional projects). A team has 4 first-silicon successes in 5 projects. Find its posterior mean success rate, in percent.

**42.** An accelerator has 2 PFLOP/s of dense FP8 compute and 4 TB/s of memory bandwidth. Decoding at batch 16 with one-byte weights does about 2 FLOP per sequence per weight byte. Its attainable share of peak is:
(A) 3.20% · (B) 6.40% · (C) 12.8% · (D) 1.60%

**43.** *Numeric entry.* A CPU vendor claims 25% more performance at the same power from 10% more IPC, with switched capacitance unchanged and power $\propto f^3$ along the voltage–frequency line. Find the required reduction in energy per operation at the new operating point, $1 - 1/(R/g_{\text{IPC}})^3$, in percent.

**44.** A 400 mm² die has Poisson yield with $D_0$ = 0.001 per mm². Ignoring the wafer-edge term, the elasticity of its cost to its area is:
(A) 0.400 · (B) 1.04 · (C) 1.40 · (D) 2.40

**45.** *Numeric entry.* A product earning \$200M a year at 50% gross margin, in a market window with a fixed end date, needs a respin that slips it 3 months and costs \$15M of masks. Find the profit impact, in \$M.

**46.** A part rated at 50 FIT ships in 2 million units, each operating all year. The expected field failures per year are:
(A) 0.100 · (B) 87.6 · (C) 8760 · (D) 876

**47.** *Numeric entry.* Two accelerators do the same work at 900 W and 750 W. At a PUE of 1.3 and \$0.09 per kWh, find the lower-power device's electricity saving over 5 years, in dollars.

**48.** A target's revenue comes from five customers with shares of 40%, 25%, 15%, 10% and 10%. The effective number of customers, $1/\text{HHI}$, is:
(A) 5.00 · (B) 2.50 · (C) 3.77 · (D) 0.265

**49.** *Numeric entry.* A synergy plan promises \$40M a year for 5 years, starting at the end of year 1. At 10%, find its present value if it arrives one year late and 80% realized, in \$M.

**50.** A forecaster said 0.9 on five claims; four turned out true and one false. Her Brier score is:
(A) 0.250 · (B) 0.0100 · (C) 0.170 · (D) 0.810
