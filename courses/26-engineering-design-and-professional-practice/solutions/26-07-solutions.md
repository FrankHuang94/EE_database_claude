# Solutions 26-07 · Engineering Ethics and Professional Responsibility

Problems: [26-07 problems](../problems/26-07-problems.md) · Chapter: [26-07](../chapters/26-07-engineering-ethics.md). Every number is recomputed by [verify_26_07.py](../verify/verify_26_07.py).

---

## Solutions

### Solution 26-07.1

(a) Canon 2, competence ("Perform services only in areas of their competence"); she should decline or get the work reviewed by someone qualified.

(b) Canons 3 and 5: public statements must be objective and truthful, and the brochure deceives by omission.

(c) Canon 1, public safety, which outranks the duty to the employer (canon 4); an automotive erratum is a safety matter.

(d) Canon 4: a faithful agent keeps the employer's confidential information confidential.

(e) Canon 1 with rule II.1.a: if overruled where life or property is endangered, notify the employer and "such other authority as may be appropriate" [R-654].

### Solution 26-07.2

"A. Codes of ethics", "B. Intellectual property" and "C. Safety" [R-655]. Examples: (A) applying the NSPE canons to an erratum decision; (B) handling a former employer's trade secrets, or patenting a circuit; (C) electrostatic-discharge and laser safety in a lab, or the functional safety of an automotive part.

### Solution 26-07.3

(a) $2 \times 10^{-7} \times 3 \times 10^7 \times 4$ = **24** failures.

(b) $1 - e^{-24}$, which is **1.0** to any useful precision.

(c) One expected failure needs $p = 1/(1.2 \times 10^8)$ = **8.33e-9** per unit per year.

### Solution 26-07.4

(a) $2 \times 365 \times 10$ = **7300** hours.

(b) $100 \times 10^{-9} \times 2 \times 10^6 \times 7300$ = **1460** failures.

(c) $1 - e^{-100 \times 10^{-9} \times 7300}$ = **7.30e-4**, about one vehicle in 1,400.

### Solution 26-07.5

(a) Independent: $(10^{-4})^2$ = **1.0e-8**. With $\beta$ = 0.02: $0.02 \times 10^{-4} + (0.98 \times 10^{-4})^2$ = **2.01e-6**.

(b) **201** times.

(c) Solving $\beta \times 10^{-4} + [(1 - \beta) \times 10^{-4}]^2 = 10^{-7}$ gives $\beta$ = **9.00e-4**: fewer than one failure in a thousand may be shared. Only channels of genuinely different design reach that.

### Solution 26-07.6

$T = 500{,}000 \times 2{,}000$ = **1.0e9** device-hours.

(a) $2.996/10^9$ per hour = **3.00** FIT.

(b) $12.592/(2 \times 10^9)$ per hour = **6.30** FIT.

### Solution 26-07.7

$T = -\ln(0.1)/(100 \times 10^{-9})$ = **2.30e7** device-hours. With 1,000 units, **2.30e4** hours each, about **2.63** years; with an acceleration factor of 50, **461** hours each. This is why reliability claims rest on accelerated stress testing (25-09).

### Solution 26-07.8

(a) TPP = $400 \times 16$ = **6400**, density **8.0**: 3A090.a.1.

(b) TPP = $180 \times 16$ = **2880**, density **6.4**: 3A090.a.2 (TPP ≥ 1600, density ≥ 5.92).

(c) TPP = $300 \times 8$ = **2400**, density **1.6**: 3A090.b.1 (TPP of 2400 or more and less than 4800, density of 1.6 or more and less than 5.92), exactly at both lower bounds, which the rule's "or more" includes.

(d) $4800/8$ = **600** TOPS at 8 bits and $4800/16$ = **300** TFLOPS at 16 bits, the figures the rule itself gives [R-659].

### Solution 26-07.9

(a) **Patent** (a new and useful invention). (b) **Mask work** registration (layout). (c) **Trade secret** (kept confidential, valuable because not known; a patent would publish it). (d) **Copyright** (expression), possibly with trade-secret protection while unpublished. (e) **Trademark**.

### Solution 26-07.10

(a) 20 years from filing: **2 October 2045**.

(b) Protection starts at the earlier date, registration on 20 January 2026; ten years later is 20 January 2036, extended to the end of the calendar year: **31 December 2036**.

### Solution 26-07.11

In order: (1) document the finding precisely (conditions, affected parts, evidence) and report it in writing through the company's safety and quality process, not only verbally; (2) support a fast assessment of the hazard: which safety goals the missed fault can violate, the affected population and the field exposure; (3) if management decides not to notify customers or the risk remains unaddressed, canon 1 and rule II.1.a require notifying "such other authority as may be appropriate", inside the company first (the functional-safety manager, quality, legal) and beyond it if needed [R-654]. The company owes its customers a prompt erratum with the conditions, the risk and a workaround or fix, so that the vehicle makers can meet their own safety obligations. Useful calculations: the fleet probability and expected events (§3.3) for the affected population; a FIT-style estimate of the condition's rate; and, if the comparator is one of two protections, the beta-factor model to see what the remaining protection covers.

### Solution 26-07.12

A model set:

1. *IP provenance:* "What did the founders bring from their former employer, and how did you ensure it was nothing confidential?" Strong: signed attestations at hiring, a clean-room or independent-design record for the first designs, legal review, no disputes. Weak: "we started from scratch" with no evidence.
2. *Open source:* "Which open-source RTL, tools and firmware are in your products, under which licenses, and how do you track them?" Strong: a maintained inventory, license review, compliance with obligations. Weak: "it's all permissive".
3. *Export controls:* "How are your products classified under the EAR, who made the classification, and how do you screen customers and data-center end users?" Strong: a written classification with TPP and density calculations, a compliance owner, procedures updated for the 2026 rules [R-659]. Weak: "our chips are below the thresholds" without a calculation.
4. *Escalation:* "When an engineer disagreed with a release decision, what happened?" Strong: a concrete case, a written record and a decision that weighed the concern. Weak: no example, or "we have never had a disagreement".

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 26-07.3a | expected failures | 24 | |
| 26-07.3b | P(at least one) | 1.0 | |
| 26-07.3c | risk for one expected | 8.33e-9 | per unit-year |
| 26-07.4a | hours per vehicle | 7300 | h |
| 26-07.4b | fleet failures | 1460 | |
| 26-07.4c | per-vehicle probability | 7.30e-4 | |
| 26-07.4c1 | one vehicle in | 1.4e3 | |
| 26-07.5a | independent | 1.0e-8 | |
| 26-07.5a1 | with common cause | 2.01e-6 | |
| 26-07.5b | ratio | 201 | |
| 26-07.5c | required beta | 9.00e-4 | |
| 26-07.6 | device-hours | 1.0e9 | h |
| 26-07.6a | bound, no failures | 3.00 | FIT |
| 26-07.6b | bound, two failures | 6.30 | FIT |
| 26-07.7 | device-hours | 2.30e7 | h |
| 26-07.7a | hours per unit | 2.30e4 | h |
| 26-07.7a1 | years per unit | 2.63 | years |
| 26-07.7b | accelerated hours | 461 | h |
| 26-07.8a | TPP | 6400 | |
| 26-07.8a1 | density | 8.0 | |
| 26-07.8b | TPP | 2880 | |
| 26-07.8b1 | density | 6.4 | |
| 26-07.8c | TPP | 2400 | |
| 26-07.8c1 | density | 1.6 | |
| 26-07.8d | 8-bit rate | 600 | TOPS |
| 26-07.8d1 | 16-bit rate | 300 | TFLOPS |
