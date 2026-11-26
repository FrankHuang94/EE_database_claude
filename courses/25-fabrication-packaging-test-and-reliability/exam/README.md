# Course 25 · Final Exam (Semiconductor Fabrication, Packaging, Test and Reliability)

**Time limit:** 240 minutes, best taken in two sittings of about 120 minutes: Questions 1–6, then Questions 7–12.
**Allowed:** a scientific calculator and the [Course 25 equation sheet](../../../reference/equation-sheets/25-fabrication-packaging-test-and-reliability.md) printed without its chapter links. No notes, no Python and no simulator.

**Instructions.**

- Answer all 12 questions and show every step.
- Questions 1–10 [B] are worth 8 points each (2 per part), and Questions 11 and 12 [C] 12 each (3 per part): 104 points in total. 73 or more (70%) is a strong pass.
- Give numerical answers to 3 significant figures, with units, unless a part asks otherwise.
- Question 11 asks for derivations: results quoted from the equation sheet earn no credit unless derived. Question 12 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- $k$ = 8.617 × 10⁻⁵ eV/K, $T$ = °C + 273.15; $h$ = 6.626 × 10⁻³⁴ J·s, $c$ = 2.998 × 10⁸ m/s; Faraday's constant 96,485 C/mol.
- Silicon 150, copper 400, aluminium 200 W/(m·K); water 1,000 kg/m³ and 4,180 J/(kg·K).
- The alpha-power delay law: delay ∝ $V/(V - V_{TH})^{\alpha}$.
- $\operatorname{erf}$ values: erf(2.525) = 0.99964.
- Chi-square values at 60% confidence: $\chi^2_{0.6,2}$ = 1.833, $\chi^2_{0.6,4}$ = 4.045.
- "Assumed" values are illustrative.

---

**1 [B] · Process flow.** (25-01)
(a) Dry oxidation at 1,000 °C has Deal–Grove constants $A$ = 0.165 µm and $B$ = 0.0117 µm²/h (assumed), starting from bare silicon. How long does it take to grow 0.10 µm and 0.50 µm of oxide?
(b) How much silicon does the 0.10 µm oxide consume?
(c) A fab starts 60,000 wafers a month with a 90-day cycle time. Using Little's law and 30-day months, how many wafers are in process?
(d) A global wire has 24 kΩ and 0.4 pF in total. Find its distributed 50% delay, and the delay if its length is halved.

**2 [B] · Lithography.** (25-02)
(a) Find the minimum pitch with off-axis illumination for 193 nm immersion at NA 1.35, EUV at NA 0.33 and High-NA EUV at NA 0.55.
(b) Using the small-NA approximation $n\lambda/(2\text{NA}^2)$ with $n$ = 1, find the depth of focus for the two EUV systems.
(c) A 20 nm × 20 nm contact is exposed at 30 mJ/cm² of 13.5 nm light. How many photons does it receive, and what is the relative shot noise?
(d) A scanner spends 10 s of overhead and 12 s of exposure per wafer. Find its throughput, and the throughput if the dose (and so the exposure time) doubles.

**3 [B] · Unit processes.** (25-03)
(a) An implant of 10¹⁵ cm⁻² has $R_p$ = 50 nm and $\Delta R_p$ = 20 nm. Find the peak concentration.
(b) Find the junction depth in a 10¹⁷ cm⁻³ background.
(c) An anneal with $Dt$ = 2 × 10⁻¹² cm² follows. Find the new straggle and the new peak.
(d) A CVD process has $h_g$ = 5 cm/s and $k_s$ = 1 cm/s (assumed). Find its effective rate constant and say which step limits it. Copper plates at 20 mA/cm² (M = 63.55 g/mol, $n$ = 2, ρ = 8.96 g/cm³): find the plating rate in µm/min.

**4 [B] · Yield and die cost.** (25-04)
(a) Estimate the dies per 300 mm wafer for a 150 mm² die with the formula $\pi d^2/4A - \pi d/\sqrt{2A}$ (round to a whole number).
(b) At $D_0$ = 0.15 cm⁻², find the Poisson, Murphy and negative-binomial (α = 2) yields.
(c) With an $18,000 wafer, find the cost per good die with the Poisson yield.
(d) Repeat (c) with the negative-binomial yield, and explain the difference.

**5 [B] · Foundries and process options.** (25-05)
(a) A path runs at 0.75 V with $V_{TH}$ = 0.30 V and α = 1.3. Find its delay at the slow corner ($V_{TH}$ + 40 mV) and fast corner ($V_{TH}$ − 40 mV) relative to typical, and the slow-to-fast spread.
(b) An FD-SOI device has an EOT of 1.0 nm, a 6 nm silicon body (ε_r = 11.7) and a 20 nm BOX (ε_r = 3.9). Find its back-gate coupling in mV/V.
(c) An MPW slot is priced at €15,000/mm² with a 4 mm² minimum (assumed). What does a 3 mm² design cost?
(d) Explain in one or two sentences why a mixed-signal die gains less from a node shrink than a digital one.

**6 [B] · Packaging.** (25-06)
(a) Find the die size at which an area array at 110 µm pitch overtakes a single row of perimeter pads at 45 µm pitch.
(b) A 130 µm bump pitch with 75 µm pads routes 10 µm lines and spaces. How many traces fit between pads, and how many layers escape 18 rows?
(c) With Δα = 13.4 ppm/K, a 120 K cycle, a 12 mm distance from the neutral point and 80 µm joints, find the shear strain, and the fatigue life relative to a joint at 100 K, 10 mm and 70 µm (Coffin–Manson exponent 2).
(d) A package has 500 identical joints with Weibull shape 5. By what factor is its characteristic life shorter than one joint's?

**7 [B] · Advanced packaging and chiplets.** (25-07)
(a) Find the hybrid-bond density at 5 µm pitch and the overlay budget $p/4$.
(b) A die-to-wafer bonder places dies with σ = 0.35 µm per axis. Find the die bond yield for pads half the pitch wide, using erf(2.525) = 0.99964.
(c) A compute die has 85% yield and a test catching 98% of bad dies. Find its escape rate, and the yield of a package with that die, six HBM stacks with 0.4% escapes each, and 99.8% attach yield for each of the seven parts.
(d) At $0.30/mm², $3 test per die and $D_0$ = 0.12 cm⁻² (Poisson), compare a 600 mm² monolithic die in a $50 package with three chiplets of 220 mm² in a $90 package, both with 99% attach yield per die. Find both costs per good package and their ratio.

**8 [B] · Thermal.** (25-08)
(a) Find the resistance of a 30 µm TIM with $k$ = 4 W/(m·K) over 600 mm², and its temperature drop at 1,000 W.
(b) A 3 W hotspot covers a disk 0.8 mm in diameter on silicon. Find its centre temperature rise and its average spreading resistance.
(c) An aluminium fin 30 mm tall and 0.8 mm thick sees $h$ = 60 W/(m²·K). Find $mL$ and the fin efficiency.
(d) A 1,200 W GPU on a cold plate has 0.030 K/W from junction to coolant and 1.5 L/min of water at 40 °C inlet. Find the coolant rise and the junction temperature.

**9 [B] · Reliability.** (25-09)
(a) An EM test runs at 280 °C and use is 110 °C with $E_a$ = 0.85 eV. Find the thermal acceleration factor, and the total factor if the test current density is 4 times use with $n$ = 1.5.
(b) Breakdown takes 30 s at 10 MV/cm and 300 s at 9.5 MV/cm. Fit the E model and extrapolate to 6 MV/cm. Then fit a power law in field and extrapolate it to 6 MV/cm.
(c) An HTOL runs 2,000 units for 1,000 h at AF = 50 with no failures. Find the 60% FIT bound, and the bound with one failure.
(d) Explain in two or three sentences why the E-model and power-law answers in (b) differ so much, and which is conservative.

**10 [B] · Qualification and safety.** (25-10)
(a) AEC-Q100 Grade 1 cycles from −55 to +150 °C for 1,000 cycles. With a Coffin–Manson exponent of 2 and two 40 K field cycles a day, find the acceleration and the equivalent field years.
(b) An element has 150 FIT, of which 50 FIT are safe; its safety mechanism covers 98% of dangerous faults. The mechanism has 15 FIT, of which a start-up test reveals 80%. Find SPFM and LFM.
(c) Which ASIL targets do (b)'s metrics meet?
(d) A vehicle has 12,000 semiconductor components at 0.5 ppm each. What fraction of vehicles has at least one defective component?

**11 [C] · Derivations.** (25-01, 25-06, 25-09, 25-10)
(a) Starting from the Deal–Grove flux balance, show that oxide growth is linear in time for thin films and parabolic for thick ones. At what thickness are the two terms equal, and how long does it take to grow that thickness from bare silicon with Question 1's constants?
(b) Derive the Weibull scale of a package whose joints fail independently with a common shape β. A package has 100 corner joints of scale 1 and 10,000 others of scale 4, all with β = 4. Find the package scale.
(c) Derive the dual-point violation rate $\lambda_L\lambda_D\tau$ for a latent fault exposed for a time τ. Evaluate it for λ_L = 3 FIT, λ_D = 100 FIT and a test interval of 2,000 h.
(d) Derive the local current exponent $n(x)$ of the two-phase electromigration model $MTTF = Bj^{-2} + Cj^{-1}$. At what $x = j/j^*$ does a test measure $n$ = 1.6?

**12 [C] · Diligence: an AI accelerator startup.** (25-07, 25-08, 25-11, 25-12)
A startup pitching a four-chiplet 3 nm AI accelerator claims: "Splitting our 800 mm² design into four chiplets cuts silicon-plus-package cost by 30%. The 1,500 W part is air-cooled. Test is 2% of our $20,000 selling price. And our first silicon will work."
(a) Using the four-chiplet cost model of 25-07 (Example 25-07.9's costs, $D_0$ = 0.1 cm⁻², Poisson), what saving does the model give?
(b) With a 35 °C air inlet, a 95 °C junction limit and 0.020 K/W from junction to heat-sink base, what heat-sink resistance does air cooling need, and how many times better is that than Example 25-08.4's 0.0627 K/W sink?
(c) At a $500/h test-cell rate, how many test hours do 2%, 5% and 7% of the selling price buy? What does the 5–7% range in R-618 imply about the startup's 2%?
(d) What is the upper 95% Wilson bound on first-silicon success from the 2026 survey's 16 of 320? Write two questions you would ask the CTO about first silicon, with strong and evasive answers.
