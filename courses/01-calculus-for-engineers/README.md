<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 01 · Calculus for Engineers

Single- and multivariable calculus taught through electrical examples: charge and current, energy and power, RC decay, RMS values and fields. Starts at refresher level and ends at what circuits, devices and electromagnetics require.

| | |
|---|---|
| **Term** | 1 |
| **Study hours** | ≈ 116 |
| **University equivalents** | Calculus I–III (single variable + multivariable); MIT 18.01 / 18.02 |
| **Textbook alignment** | Stewart, *Calculus: Early Transcendentals*; Strang, *Calculus* (free, MIT OpenCourseWare); Kreyszig, *Advanced Engineering Mathematics* (multivariable / vector chapters) |
| **Free courses** | MIT OCW 18.01SC Single Variable Calculus; MIT OCW 18.02SC Multivariable Calculus |
| **Prerequisites** | [00 · Orientation](../00-orientation/README.md) |
| **FE areas** | Mathematics |

## Learning objectives

1. Differentiate and integrate the functions that appear in EE (polynomials, exponentials, logarithms, sinusoids, rational functions).
2. Use derivatives for rates of change, optimization and linearization (the idea behind small-signal models).
3. Use integrals for accumulation (charge from current, energy from power), averages and RMS values.
4. Build and use Taylor expansions, and bound their error.
5. Compute partial derivatives and gradients, and interpret line and surface integrals as work, flux and circulation.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [01-01 · Functions, Models and Units](chapters/01-01-functions-models-and-units.md) | 8 | ✅ verified | [problems](problems/01-01-problems.md) · [solutions](solutions/01-01-solutions.md) · [lab](labs/01-01-lab/README.md) · [verify](verify/verify_01_01.py) |
| [01-02 · Limits and Continuity](chapters/01-02-limits-and-continuity.md) | 8 | ✅ verified | [problems](problems/01-02-problems.md) · [solutions](solutions/01-02-solutions.md) · [lab](labs/01-02-lab/README.md) · [verify](verify/verify_01_02.py) |
| [01-03 · Derivatives: Rates of Change in Circuits](chapters/01-03-derivatives.md) | 12 | ✅ verified | [problems](problems/01-03-problems.md) · [solutions](solutions/01-03-solutions.md) · [lab](labs/01-03-lab/README.md) · [verify](verify/verify_01_03.py) |
| [01-04 · Applications of Derivatives](chapters/01-04-applications-of-derivatives.md) | 12 | ✅ verified | [problems](problems/01-04-problems.md) · [solutions](solutions/01-04-solutions.md) · [lab](labs/01-04-lab/README.md) · [verify](verify/verify_01_04.py) |
| [01-05 · Integrals: Accumulating Charge and Energy](chapters/01-05-integrals.md) | 12 | ✅ verified | [problems](problems/01-05-problems.md) · [solutions](solutions/01-05-solutions.md) · [lab](labs/01-05-lab/README.md) · [verify](verify/verify_01_05.py) |
| [01-06 · Techniques of Integration](chapters/01-06-techniques-of-integration.md) | 12 | ✅ verified | [problems](problems/01-06-problems.md) · [solutions](solutions/01-06-solutions.md) · [lab](labs/01-06-lab/README.md) · [verify](verify/verify_01_06.py) |
| [01-07 · Applications of Integration](chapters/01-07-applications-of-integration.md) | 10 | ✅ verified | [problems](problems/01-07-problems.md) · [solutions](solutions/01-07-solutions.md) · [lab](labs/01-07-lab/README.md) · [verify](verify/verify_01_07.py) |
| [01-08 · Sequences, Series and Taylor Expansions](chapters/01-08-sequences-series-and-taylor.md) | 12 | ✅ verified | [problems](problems/01-08-problems.md) · [solutions](solutions/01-08-solutions.md) · [lab](labs/01-08-lab/README.md) · [verify](verify/verify_01_08.py) |
| [01-09 · Multivariable Calculus I: Partial Derivatives and Gradients](chapters/01-09-multivariable-calculus-1.md) | 12 | ✅ verified | [problems](problems/01-09-problems.md) · [solutions](solutions/01-09-solutions.md) · [lab](labs/01-09-lab/README.md) · [verify](verify/verify_01_09.py) |
| [01-10 · Multivariable Calculus II: Multiple, Line and Surface Integrals](chapters/01-10-multivariable-calculus-2.md) | 12 | ✅ verified | [problems](problems/01-10-problems.md) · [solutions](solutions/01-10-solutions.md) · [lab](labs/01-10-lab/README.md) · [verify](verify/verify_01_10.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/01-calculus-for-engineers.csv) · [Equation sheet](../../reference/equation-sheets/01-calculus-for-engineers.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 01 is the longest of Term 1 (about 116 hours) and the mathematical foundation for everything after it. Chapters 01-01 to 01-08 are single-variable calculus (Calculus I–II), and 01-09 and 01-10 are multivariable calculus (Calculus III). Do them in order. If your algebra is rusty, the Math refresher callouts in 01-01 and 01-02 fill the gaps. Work at least the [A] and [B] problems of every chapter before moving on: the problem sets, not the reading, are where the skills form. Each lab pairs a notebook with ngspice netlists where a circuit can confirm the mathematics (01-10's lab is a notebook only, since its subject is fields and geometry).

**What to master cold.** Exponentials and decibels (01-01), the derivative rules and $i = C\,dv/dt$ (01-03), linearization and Newton's method (01-04), RMS and energy integrals (01-07), Taylor approximations with their error terms (01-08), sensitivity analysis and Lagrange multipliers (01-09), and the integral laws of 01-10. Course 02 (complex numbers, ODEs and linear algebra), Courses 06–07 (circuits) and Course 13 (electromagnetics) build directly on them. The [equation sheet](../../reference/equation-sheets/01-calculus-for-engineers.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions, takes 180 minutes, and allows a calculator and the equation sheet but not Python. Aim for at least 70%. One part of question 11 is a short-answer diligence question about die cost. The [flashcards](../../flashcards/01-calculus-for-engineers.csv) (101 cards) are for spaced review alongside the chapters.

**Perishable content.** Most of this course is timeless mathematics. The dated facts are in the practitioner sections: the 6 GHz Wi-Fi limits ([R-007](../../reference/research-log.md#r-007--us-6-ghz-unlicensed-band)), the reticle limit ([R-015](../../reference/research-log.md#r-015--lithography-exposure-field-the-reticle-limit)), op-amp slew rates ([R-025](../../reference/research-log.md#r-025--op-amp-slew-rate-and-bandwidth-ti-lm358)), accelerator power ratings ([R-026](../../reference/research-log.md#r-026--ai-accelerator-power-ratings)) and subthreshold operation ([R-027](../../reference/research-log.md#r-027--subthreshold-and-near-threshold-operation)). Check those entries once a year.
