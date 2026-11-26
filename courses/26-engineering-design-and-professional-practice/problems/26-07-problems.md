# Problems 26-07 · Engineering Ethics and Professional Responsibility

Chapter: [26-07](../chapters/26-07-engineering-ethics.md) · Worked solutions: [26-07 solutions](../solutions/26-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- FIT = failures per 10⁹ device-hours. Zero-failure 95% bound $\lambda_U = -\ln(0.05)/T$; with $k$ failures, $\chi^2_{0.95,\,2k+2}/(2T)$, where $\chi^2_{0.95,6}$ = 12.592.
- Beta-factor model: $P_{both} = \beta p + [(1 - \beta)p]^2$ (the overlap term is negligible here).
- Export criteria are the 2023 ECCN 3A090 text [R-659]; answers are exercises in reading it, not compliance advice.
- Probabilities and chip parameters are assumed.

---

## Problems

### Problem 26-07.1 [A]

**Which canon?** Name the NSPE fundamental canon most directly at stake in each case [R-654]: (a) a manager asks an engineer to sign a reliability report on a process she has never worked with; (b) a product brochure quotes a power figure measured on a hand-picked sample, without saying so; (c) an engineer is asked to omit a known erratum from a customer notice for an automotive part; (d) an engineer shares his employer's unreleased roadmap with a friend at a competitor; (e) an engineer's warning about a thermal hazard is overruled.

### Problem 26-07.2 [A]

**The FE exam's ethics area.** List the three topic headings of the FE Electrical and Computer exam's Ethics and Professional Practice area and give one example of each from chip engineering [R-655].

### Problem 26-07.3 [B]

**A consumer fleet.** A defect causes a dangerous failure with probability $2 \times 10^{-7}$ per unit per year in 30 million units for 4 years. (a) How many failures are expected over the 4 years? (b) What is the probability of at least one? (c) What per-unit annual risk would make one failure expected over the fleet's 4-year life?

### Problem 26-07.4 [B]

**An ASIL B budget.** An ASIL B item meets the 100 FIT target for safety-goal violations [R-614] and goes into 2 million vehicles operating 2 hours a day for 10 years. Find (a) the hours per vehicle, (b) the expected fleet failures, and (c) the probability per vehicle over its life.

### Problem 26-07.5 [B]

**How much diversity is enough?** Two protection channels each fail on demand with probability $10^{-4}$. (a) Find the probability both fail if independent, and with $\beta$ = 0.02. (b) By what factor does the common cause raise the risk? (c) What $\beta$ keeps the probability that both fail at $10^{-7}$?

### Problem 26-07.6 [B]

**Field data.** A population of 500,000 units runs 2,000 hours each. Find the 95% upper bound on the failure rate in FIT if (a) no failures are seen, and (b) two failures are seen.

### Problem 26-07.7 [B]

**A demonstration test.** How many failure-free device-hours show a rate below 100 FIT with 90% confidence? With 1,000 units on test, how long would that take, and how long with an acceleration factor of 50 (25-09)?

### Problem 26-07.8 [B]

**Classify by the 2023 rule.** For datacenter chips (dense rates), find TPP and performance density and the 3A090 criterion met, if any [R-659]: (a) 400 TFLOPS at 16 bits on 800 mm²; (b) 180 TFLOPS at 16 bits on 450 mm²; (c) 300 TOPS at 8 bits on 1,500 mm². (d) What dense 8-bit and 16-bit rates reach a TPP of 4800?

### Problem 26-07.9 [A]

**Which protection?** Name the most suitable IP protection for each: (a) a new sense-amplifier circuit; (b) the layout of a production chip; (c) a calibration algorithm kept inside the company's test programs; (d) firmware source code; (e) a product brand name.

### Problem 26-07.10 [A]

**Dates.** (a) A US patent application is filed on 2 October 2025; when does the term end (fees paid, no adjustment)? (b) A mask work is registered on 20 January 2026 and first sold on 5 May 2026; when does protection end [R-658]?

### Problem 26-07.11 [C]

**An erratum in the field.** An engineer at an automotive chip supplier discovers that, under a rare combination of temperature and supply voltage, a lockstep comparator can miss a fault in one core. Production parts are in vehicles. Using the NSPE canons and rule II.1.a, describe what she should do, in order, and what the company owes its customers. Which of the chapter's calculations would help size the problem?

### Problem 26-07.12 [C]

**Diligence questions.** You are evaluating a startup that designs datacenter accelerators and hired its founding team from a large competitor. Write four questions, one each on IP provenance, open-source license compliance, export controls and the escalation of safety or quality concerns, and say what a strong answer would contain.

### Problem 26-07.13 [A]

**FE-style questions.** Choose one answer for each [R-654, R-655, R-658]. (a) Under the NSPE Code, an engineer's paramount obligation is to: (A) the employer; (B) the client; (C) the safety, health and welfare of the public; (D) the profession. (b) In most US states, the usual path to a PE licence is: (A) the FE exam alone; (B) a degree from an EAC/ABET-accredited program, the FE exam, about four years of progressive engineering experience, then the PE exam; (C) eight years of experience with no exams; (D) a master's degree in engineering. (c) A chip's layout is first sold on 1 March 2026 and never registered as a mask work. Protection: (A) lasts ten years from first sale; (B) ends if registration is not applied for within two years of first sale, by 1 March 2028; (C) never starts; (D) runs to 31 December 2036. (d) Which is not one of the three headings of the FE exam's Ethics and Professional Practice area? (A) Codes of ethics; (B) Intellectual property; (C) Safety; (D) Project finance.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Codes of ethics | 1, 11 |
| 2. Licensure and the FE exam | 2, 13 |
| 3. Quantified safety | 3, 4, 5, 6, 7 |
| 4. Intellectual property | 9, 10, 12, 13 |
| 5. Export controls | 8, 12 |
