# Course 26 · Final Exam (Engineering Design and Professional Practice)

**Time limit:** 180 minutes, best taken in two sittings of about 90 minutes: Questions 1–6, then Questions 7–12.
**Allowed:** a scientific calculator, the FE Reference Handbook's unit normal table (or the calculator's normal-distribution function), and the [Course 26 equation sheet](../../../reference/equation-sheets/26-engineering-design-and-professional-practice.md) printed without its chapter links. No notes, no Python and no spreadsheet.

**Instructions.**

- Answer all 12 questions and show every step.
- Questions 1–10 [B] are worth 8 points each (2 per part), and Questions 11 and 12 [C] 12 each (3 per part): 104 points in total. 73 or more (70%) is a strong pass.
- Give numerical answers to 3 significant figures, with units, unless a part asks otherwise (interest factors and dollar amounts may carry more). Money is in dollars unless stated.
- Carry intermediate values at full calculator precision and round only final answers.
- A few parts need a short iteration on the calculator (bisection is fine); say what you iterated on.
- Question 11(a) asks for a derivation: a result quoted from the equation sheet earns no credit unless derived. Question 12(d) has a short written part; its rubric is at the end of the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- Dies per wafer use $\pi d^2/(4A) - \pi d/\sqrt{2A}$ on 300 mm wafers, rounded down; die yield is Poisson, $e^{-AD_0}$ with $A$ in cm².
- Cash flows occur at the ends of years; NRE and upfront fees at year 0 unless stated.
- PERT: $\mu = (a + 4m + b)/6$, $\sigma = (b - a)/6$; path durations are approximately normal.
- FIT = failures per 10⁹ device-hours; the zero-failure 95% upper bound on a rate is $-\ln(0.05)/T$.
- Normal values: $\Phi(-2.828)$ = 0.002342; $\Phi^{-1}(0.90)$ = 1.2816; $\Phi^{-1}(0.95)$ = 1.645. Other values of $\Phi$ may be read from the FE Reference Handbook's table or a calculator's normal-distribution function.
- "Assumed" values are illustrative.

---

**1 [B] · Requirements and budgets.** (26-01)
(a) A wearable spends 2% of the time active at 12 mA, 5% in radio bursts at 4 mA and the rest asleep at 15 µA. Find its average current, and its life on a 200 mAh battery of which 80% is usable.
(b) Three independent error sources have standard deviations of 0.5%, 0.3% and 0.4%. Find the worst-case sum of their ±3σ bounds and the RSS 3σ total.
(c) If the first two sources are correlated with $\rho$ = 0.6, find the new 3σ total.
(d) With the independent sources of (b), zero mean, a Gaussian total and a specification of ±2%, what fraction of units falls outside the specification, in ppm?

**2 [B] · When errors are found, and choosing.** (26-01)
(a) A program has 50 specification defects. The specification review finds each with probability 0.4 at a cost of $1k per defect. Defects it misses are found at the next stage with probability 0.5 ($10k each), then at the next with probability 0.6 ($100k each), and any left are found in the field ($1,000k each). Find the expected downstream cost per missed defect and the total expected cost.
(b) With $C$ the total expected cost and $p_1$ the specification review's detection probability, find $\partial C/\partial p_1$, and the saving from raising the review's detection probability by 0.01.
(c) Option $a$ scores 9 and option $b$ 5 on criterion $c$; their weighted averages over the other criteria are 6.0 and 7.5. Above what weight on $c$ does option $a$ win?
(d) Of 200 requirements, 8% have no test traced to them; each untraced requirement has a 25% chance of hiding a defect that costs $150k. Find the expected cost of the gaps.

**3 [B] · Reviews and standards.** (26-02)
(a) Each reviewer independently finds a given defect with probability 0.4. What fraction of defects do three reviewers find?
(b) A reviewer costs $6,000; an escaped defect costs $20,000; the document holds 25 defects. Find the cost-optimal number of reviewers, and confirm it by comparing costs at the neighbouring team sizes.
(c) Two reviewers find 18 and 15 defects, 10 in common. Estimate the total by Lincoln–Petersen and by Chapman, and the number still undetected (Lincoln–Petersen).
(d) An IEEE ballot has 180 eligible voters; 140 return ballots: 98 approve, 22 disapprove and 20 abstain. Check the return, approval and abstention rules (75%, 75%, under 30%). Does it pass?

**4 [B] · Cost stack and margin.** (26-03)
(a) A 120 mm² die is made on $15,000 wafers at $D_0$ = 0.12 cm⁻². Find the dies per wafer, die yield and cost per good die.
(b) The package costs $5.00 and assembly yields 98.5%; final test costs $1.50 per unit tested and yields 97%. Find the cost after assembly and after test.
(c) The chip sells for $75 (no royalties). Find the gross margin and markup.
(d) The program's NRE is $90 M. Find the break-even volume.

**5 [B] · Time value and a program's NPV.** (26-03)
(a) Find $(P/A, 8\%, 6)$ and $(A/P, 8\%, 6)$, and the annual payment that repays a $250,000 tester over 6 years at 8%.
(b) A program spends $40 M of NRE in each of years 0 and 1 and earns $35 M a year in years 2 to 5 (assumed). Find its NPV at 12% and its IRR.
(c) Find its simple payback, interpolating within the year in which cumulative cash turns positive.
(d) A one-year slip delays every sales year, and the market window closes after year 5 so the last year is lost. Find the new NPV and the value lost.

**6 [B] · License or build.** (26-04)
(a) A chip ships 4, 6, 6 and 4 million units in years 1 to 4; the MARR is 10%. Find the discounted unit stream.
(b) A PHY licence costs $8 M up front and $1.00 a unit; building it costs $30 M with a 20% chance of a slip worth $20 M. Find each present cost and the better option.
(c) Find the discounted break-even volume and its multiple of the plan.
(d) The licensor offers instead 2.5% of the chip's ASP, which starts at $40 and falls 10% a year. Find the percentage form's present value and the equivalent per-unit royalty.

**7 [B] · Node choice.** (26-04)
(a) A 150 mm² die is 60% logic, 25% SRAM and 15% analog. The new node improves their density by 1.6×, 1.15× and 1.05×. Find the effective density gain and the new die area.
(b) Old-node wafers cost $15,000 with $D_0$ = 0.10 cm⁻²; new-node wafers $19,000 with $D_0$ = 0.12 cm⁻². Find the cost per good die at each node.
(c) The new node costs $40 M more NRE. Find the break-even lifetime volume.
(d) Before yield and edge effects, by what factor does cost per function change? Explain in one sentence why it is not $1/1.6$.

**8 [B] · Custom or merchant.** (26-04)
(a) A merchant accelerator costs $25,000 and draws 0.9 kW; a custom one costs $8,000, draws 0.6 kW and has 0.75 of the merchant's throughput. Each slot carries $10,000 of other infrastructure; life 4 years, PUE 1.25, electricity $0.07/kWh. Find each slot's energy cost and TCO.
(b) Find the cost per merchant-equivalent of each and the saving.
(c) The custom program's NRE is $500 M. Find the break-even fleet in merchant-equivalents and in custom chips.
(d) What merchant price makes a fleet of 150,000 custom chips exactly break even?

**9 [B] · Schedules and tape-outs.** (26-05)
(a) Path A is verification closure (6, 8, 14 weeks) then regression (2, 3, 5); path B is place and route (5, 7, 11) then signoff (3, 4, 7). Find each path's mean and standard deviation.
(b) Taking the paths as independent, find the chance that each path, and both, finish within 14 weeks, and the date by which both finish with a 90% chance (iterate).
(c) Spins succeed with probabilities 0.3, 0.8 and then 1. Find the expected number of tape-outs, the distribution, and the expected delay at 16 weeks per respin.
(d) A process has 85 mask layers, the last 28 of them metal and via, at 1.3 days per layer. Find the fab time of a full respin and of a metal-only ECO restarted from wafers held at the contact layer (before the first metal layer), in weeks.

**10 [B] · Risk register and when to tape out.** (26-05)
(a) Risks (probability, impact $ M): R1 (0.2, 25), R2 (0.3, 10), R3 (0.1, 40). Mitigations (cost $ M, probability after): R1 (2.0, 0.05), R2 (1.0, 0.15), R3 (1.5, 0.03). Find the EMV, each mitigation's net benefit, and the best set with a $3 M budget.
(b) Final verification starts with $N_0$ = 30 bugs, mean discovery time $\tau$ = 3 weeks, and a fraction $\phi$ = 0.3 respin-class; a respin costs $30 M and a week $1.2 M. Find $k = c_w\tau/C_r$, the optimal $\lambda^*$ (the smaller root of $\lambda e^{-\lambda} = k$; iterate), the optimal verification time and the respin probability there.
(c) Find the expected cost at the optimum and at $t$ = 0.
(d) Emulation costing $2 M shortens $\tau$ to 2 weeks. Find the new optimum time, respin probability and expected cost including the emulation. Is it worth buying?

**11 [C] · Teams.** (26-06)
(a) Derive the flat team size that maximizes $O(n) = n[1 - c(n - 1)]$, show it is a maximum, and evaluate the best integer size and its output for $c$ = 0.035.
(b) 64 people are organized as 8 teams of 7 engineers plus a lead; $c$ = 0.035 within teams and $c_x$ = 0.02 per other team. Find the output and the output per head.
(c) A team of 12 ($c$ = 0.02) can add 6 engineers who need 2.5 months of ramp, each taking half an experienced engineer's time meanwhile. Find the remaining work, in person-months, below which adding them lengthens the project, and the time it represents at the current rate.
(d) Verification needs 12, 18, 30, 45, 45, 30, 18 and 12 engineers in eight quarters; employees cost $80,000 a quarter and contractors $120,000. Find the newsvendor base and its total cost, and compare with a base of 12 and of 30.

**12 [C] · Safety, evidence and export rules.** (26-07)
(a) An ASIL B part at its 100 FIT target goes into 5 million vehicles that run 1.5 hours a day for 15 years. Find the hours per vehicle, the expected fleet failures and the probability per vehicle.
(b) Two protection channels each fail on demand with probability $5 \times 10^{-4}$, with a common-cause fraction $\beta$ = 0.03. Find the probability that both fail and the factor by which the common cause raises it over independence. What design choice lowers $\beta$?
(c) A part has $2 \times 10^8$ failure-free device-hours. Find the 95% upper bound on its rate in FIT, and the total failure-free hours needed to support 10 FIT, as a multiple of the hours so far. What does this say about a clean field record as evidence?
(d) A datacenter accelerator delivers 220 TFLOPS dense at 16 bits on a 520 mm² die. Find its TPP and performance density, and which 2023 ECCN 3A090 criterion it meets. Marketing wants to describe it to an overseas prospect as "below US export thresholds". Which NSPE canons apply, and what should the engineer do?
