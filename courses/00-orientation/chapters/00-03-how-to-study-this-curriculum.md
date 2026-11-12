<!-- status: reviewed -->
# 00-03 · How to Study This Curriculum

| | |
|---|---|
| **Course** | [00 · Orientation](../README.md) |
| **University equivalent** | The "how to learn engineering" component of a first-year engineering seminar, informed by cognitive-science research on learning |
| **Prerequisites** | [00-01](00-01-map-of-electrical-engineering.md), [00-02](00-02-the-abstraction-stack.md). No mathematics beyond algebra. |
| **Estimated study hours** | 2 |
| **Last verified** | 2026-11-12 |

**Learning objectives.** After this chapter you can:

1. Follow the chapter study loop and explain the evidence behind each step (retrieval practice, spacing, interleaving).
2. Apply a five-step problem-solving protocol that ends with units, limit and magnitude checks.
3. Use dimensional analysis to check a formula and catch algebra errors.
4. Make an order-of-magnitude (Fermi) estimate and use it to sanity-check a claim.
5. Plan spaced reviews and decide, with stated criteria, when a chapter is mastered.

## 1. Big picture

You are learning a four-year technical degree part-time and without an instructor. What determines success is not raw ability. You plainly have that. It is whether your study habits produce *durable, usable* knowledge rather than the comfortable feeling of familiarity. Cognitive science has studied this for over a century, and its findings are consistent: the techniques that feel most productive (rereading, highlighting) produce the least lasting learning, and the techniques that feel effortful (self-testing, spacing, mixing problem types) produce the most. This chapter turns that evidence into a concrete routine for this curriculum, and teaches the three checking habits engineers use on every answer.

- **Problems are the curriculum.** Every chapter's problem set is retrieval practice in disguise.
- **The repository checks your numbers.** Answer keys and verify scripts give you the feedback an instructor would.
- **Spaced flashcards** (Anki) keep 29 courses' worth of vocabulary and formulas available years later.
- **Units, limits and magnitude checks** catch most errors before anyone else sees them. They are also the core of skeptical technical diligence.

## 2. Intuition first

### The illusion of competence

Reading a worked solution, you nod along: every step makes sense. That is *recognition*, and it is cheap. The exam (or the VP of Engineering across the table) asks for *recall and application*: produce the step yourself, from a blank page. The gap between the two is the illusion of competence, and the only reliable way to close it is to practice what you will be asked to do, which is retrieving and applying, not re-reading.

### An analogy from finance: compounding and depreciation

Knowledge depreciates. Without use, recall decays roughly exponentially, like an asset written down over time. Each successful retrieval does not just top the asset back up; it lowers the depreciation rate, so the next decay is slower. Spaced review is therefore like reinvesting at increasing intervals: early on you review often, later rarely, and the asset holds its value at very low maintenance cost (§3.6).

*Where the analogy breaks:* memory is not a single account. Retrieval strength (how easily you recall something now) and storage strength (how well it is learned) behave differently. That is why a fact that feels fluent today can still be forgotten next month, and why a *difficult* successful retrieval does more good than an easy one. Unlike money, the act of withdrawing (recalling) is what makes the investment grow.

## 3. Theory

### 3.1 What the evidence says

Four findings matter most ([R-021](../../../reference/research-log.md#r-021--learning-science-evidence)):

| Finding | Key study | Result |
|---|---|---|
| **Retrieval practice (the testing effect)** | Roediger & Karpicke (2006), *Psychological Science* | Restudying won on a test 5 minutes later, but testing won at 2 days and 1 week. One week out, students who mostly self-tested recalled 61% vs 40% for students who only reread |
| **Spacing** | Cepeda et al. (2006), *Psychological Bulletin*, a synthesis of 839 assessments | Spaced practice beats massed practice. The best gap between sessions grows with how long you need to remember |
| **Interleaving** | Rohrer & Taylor (2007), *Instructional Science* | Students who practiced mixed problem types scored 63% on a test a week later, versus 20% for blocked practice, despite *worse* performance during practice (60% vs 89%) |
| **What works overall** | Dunlosky et al. (2013), *Psychological Science in the Public Interest* | Only practice testing and distributed practice were rated "high utility". Rereading, highlighting and summarizing were rated low |

The interleaving result shows the illusion of competence in its purest form. The group that felt it was doing better during practice (89% vs 60%) learned far less.

### 3.2 The chapter study loop

Each chapter is designed to be worked through in this order:

1. **Preview (5 minutes).** Read the learning objectives, the section headings and the concept-check questions. Questions you can't yet answer prime your attention.
2. **Active reading.** Read the theory with paper beside you. For each derivation, cover the next line and try to produce it before you read it. Getting it wrong first and then seeing the right step helps learning, so do not skip this.
3. **Worked examples, attempted first.** Cover the solution, attempt the example, then compare.
4. **Lab.** Run it, and make every **predict, then run** prediction in writing *before* running.
5. **Concept check.** Answer from memory, then open the answers.
6. **Problem set.** Do all [A] and [B] problems unaided; then [C] as time allows. Check your answers against the answer key, then read the worked solution for any you missed.
7. **Error log.** Record every miss (§3.7).
8. **Flashcards.** Add the chapter's cards to Anki; review daily.

Steps 3, 5 and 6 are retrieval practice. Steps 6–8 use interleaving and spacing: problem sets mix problem types within a chapter, the term checkpoints mix chapters and courses, and the flashcards spread practice over months.

### 3.3 A five-step problem-solving protocol

1. **Understand.** Draw the circuit or system, label every quantity with a symbol and a unit, and write down what is known and what is asked.
2. **Plan.** Name the principle that connects them (KVL, conservation of energy, a transfer function) *before* computing anything.
3. **Execute symbolically, then numerically.** Solve with symbols; substitute numbers only at the end. A symbolic answer can be checked for units and limits; a number cannot.
4. **Check.** At minimum, three checks:
   - **Units:** does the answer have the right dimensions (§3.4)?
   - **Limits and special cases:** what happens as a resistance goes to 0 or ∞, as frequency goes to 0 or ∞, or if two components are equal? Does the formula give the obvious answer there?
   - **Magnitude:** is the number plausible (§3.5)? Is its sign right?
5. **Reflect.** If the answer was wrong, *why*? Log it.

### 3.4 Dimensional analysis

Every physical equation must balance in its units: you cannot add volts to amperes. Checking units catches a large share of algebra errors. Express quantities in the SI base units (kilogram, meter, second, ampere, kelvin) or in a few derived units that you know well:

| Unit | Symbol | In base units | Handy identities |
|---|---|---|---|
| volt | V | kg·m²·s⁻³·A⁻¹ | V = W/A = J/C |
| ohm | Ω | kg·m²·s⁻³·A⁻² | Ω = V/A |
| farad | F | kg⁻¹·m⁻²·s⁴·A² | F = C/V = A·s/V |
| henry | H | kg·m²·s⁻²·A⁻² | H = V·s/A = Ω·s |
| watt | W | kg·m²·s⁻³ | W = V·A = J/s |

From these, Ω·F = (V/A)(A·s/V) = s, so $RC$ is a time. And H/Ω = (Ω·s)/Ω = s, so $L/R$ is a time. If a derivation produces $\tau = R/C$, its units are Ω/F = V²/(A²·s), not seconds, so there is an error somewhere. Arguments of exponentials, logarithms and trig functions must be **dimensionless**: $e^{-t/RC}$ is fine, but $e^{-t}$ with $t$ in seconds is not, unless a "per second" is hidden somewhere.

### 3.5 Order-of-magnitude (Fermi) estimation

Before trusting any calculation, simulation or marketing claim, estimate it to within a factor of a few, using rounded numbers and multiplication. If the careful result and the estimate disagree by more than about 3×, one of them is wrong. Fermi estimation is also the fastest way to test a claim in a diligence meeting (Example 00-03.3).

### 3.6 Spacing, made concrete

A simple model captures the main idea. After you learn an item, your probability of recalling it after time $t$ decays like $R(t) = e^{-t/S}$, where $S$ is the item's *stability* (in days). (In this section $R$ is recall and $S$ stability, not resistance or siemens.) This forgetting model is a simplification used here only for intuition. Each successful review increases $S$. If you review when $R$ has fallen to a target such as 90%, the interval is $t = S\ln(1/0.9) \approx 0.105S$, and since $S$ grows with every review, the intervals expand.

Spaced-repetition software implements this idea. Schedulers in the SM-2 family (the basis of Anki's default) grow each successful interval by an "ease" factor that starts at 2.5; SM-2 itself begins with fixed intervals of 1 and 6 days and multiplies after that. Example 00-03.4 uses a simplified version that multiplies from the first interval: 1, 2.5, 6, 16, 39, 98 and 244 days. Six successful reviews fall within the first year, and the seventh, at day 406, carries the card past it. With about 3 new cards a day (roughly this curriculum's pace), the review load stays at a few minutes a day, which is why the study plan budgets 10–15 minutes of daily Anki.

### 3.7 The error log and mastery criteria

Keep one running document, the **error log**, with a line per mistake:

| Date | Problem | What I did | What was wrong | Category | Fix / rule |
|---|---|---|---|---|---|

Useful categories are concept, algebra, units, sign convention, misread question, and calculator or code. Patterns appear within weeks (for example, "I keep dropping the 2π between f and ω"), and each one becomes a personal rule. Before every checkpoint, re-solve every problem in the log.

**When to move on from a chapter:**

- you can answer every concept-check question from memory;
- you solved at least 80% of the [A] and [B] problems unaided;
- you can reproduce the chapter's key derivation on a blank page;
- you can explain the main idea aloud in two minutes to a non-engineer.

If not, revisit the sections behind your misses. Don't re-read everything.

### 3.8 Using this repository as your instructor

- **Answer keys:** every chapter, solution set and lab handout ends with a table of every published number. Check your answers there before reading the worked solution.
- **Verify scripts** (`python tools/run_verify.py NN`): these confirm that the published numbers themselves are right, so you can trust the key.
- **Labs:** simulation is your laboratory. A surprise in a "predict, then run" exercise is the most efficient learning moment the curriculum offers.
- **Glossary and notation:** [reference/glossary.md](../../../reference/glossary.md) and [reference/notation.md](../../../reference/notation.md). When a symbol confuses you, check notation first.
- **Checkpoints:** the end-of-term exams are timed, mixed and closed-book, practice for the FE exam and the strongest retrieval practice in the program.

## 4. Worked examples

### Example 00-03.1 — Dimensional analysis catches an error (tier A)

**Setup.** Check the units of: (a) $\tau = RC$; (b) a claimed $\tau = R/C$; (c) $f_0 = \frac{1}{2\pi\sqrt{LC}}$; (d) $P = V^2/R$; (e) a claimed "wave speed" $v = \sqrt{L/C}$.

**Solution.**

(a) Ω·F = (V/A)(A·s/V) = **s** ✓.
(b) Ω/F = (V/A)/(A·s/V) = V²/(A²·s), which is **not a time** ✗. The derivation has an error.
(c) H·F = (Ω·s)(s/Ω) = s², so $1/\sqrt{\text{s}^2}$ = **1/s** = Hz ✓ (the 2π is dimensionless).
(d) V²/Ω = V²/(V/A) = V·A = **W** ✓.
(e) $\sqrt{\text{H/F}} = \sqrt{(\Omega\cdot\text{s})/(\text{s}/\Omega)} = \Omega$: an **impedance**, not a speed ✗. (It is in fact the characteristic impedance of a transmission line, $Z_0 = \sqrt{L'/C'}$; the speed is $1/\sqrt{L'C'}$, [13-07](../../13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md).)

The lab shows how to automate these checks with SymPy's units module.

### Example 00-03.2 — The protocol on a small circuit (tier A)

**Setup.** A 9 V battery with internal resistance 1.5 Ω powers a 45 Ω load. Find the current and the load power, and check the answer.

**Solution.**

1. **Understand.** Draw a single loop: an ideal 9 V source, 1.5 Ω and 45 Ω in series. Unknowns: $I$ (A) and $P_L$ (W).
2. **Plan.** KVL: $V = I(R_{int} + R_L)$, and $P_L = I^2R_L$.
3. **Execute.** $I = \frac{V}{R_{int} + R_L} = \frac{9}{46.5} = 0.1935$ A, and $P_L = I^2R_L = 0.1935^2 \times 45 = 1.686$ W.
4. **Check.**
   - *Units:* V/Ω = A and A²·Ω = W ✓.
   - *Limit:* as $R_{int} \to 0$, $I \to 9/45 = 0.2$ A. Our 0.1935 A is slightly lower, as it should be ✓.
   - *Magnitude:* about 2 W from a 9 V battery is plausible for a short time ✓.
5. **Reflect.** The internal resistance cost $1 - 45/46.5 = 3.2\%$ of the voltage, a useful habit of mind for power-delivery problems later.

### Example 00-03.3 — A Fermi estimate that exposes an assumption (tier B)

**Setup.** A processor has 20 billion transistors and runs at 3 GHz. Assume each transistor switches on 10% of cycles, and each switch costs about 0.5 fJ. (These are illustrative round numbers.) Estimate the dynamic power. Real processors of this size dissipate on the order of 100–300 W. What does the comparison tell you?

**Solution.** Power = transistors × activity × frequency × energy per switch $= 2\times10^{10} \times 0.1 \times 3\times10^9 \times 5\times10^{-16}$ J $= 3000$ W.

The estimate is about 10× too high, so one assumption is badly off. The weakest one is the 10% activity: most transistors in a large chip (cache arrays, idle units, gated clocks) switch far less often. Solving backward for a 250 W chip gives $\alpha = 250/(2\times10^{10} \times 3\times10^9 \times 5\times10^{-16}) = 0.0083$, under 1%. **The estimate points at something real, though it cannot prove it alone:** the 0.5 fJ per switch is uncertain too, and the estimate ignores leakage. Independent evidence from chip power analysis confirms that average switching activity in large chips is low, and that is precisely what clock gating and power gating exploit ([19-06](../../19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)). That is the value of a Fermi estimate: not the number, but the assumption it exposes.

### Example 00-03.4 — A spaced-review schedule (tier B)

**Setup.** A flashcard is first reviewed 1 day after learning, and each successful review multiplies the next interval by 2.5. (a) List the intervals. (b) How many successful reviews does it take for the cumulative time to exceed one year? (c) If you add 3 new cards per day and each card needs about 7 reviews in its first year (the 6 scheduled reviews plus roughly one repeat after a lapse), at about 8 seconds per review, how much daily time does reviewing take in steady state?

**Solution.**

(a) The intervals are 1, 2.5, 6.25, 15.6, 39.1, 97.7 and 244 days.
(b) The cumulative sums are 1, 3.5, 9.75, 25.4, 64.4, 162 and **406** days. Six reviews fall within the first 365 days; the seventh takes the card past one year.
(c) $3 \times 7 = 21$ reviews per day, which at 8 s each is $168$ s $= 2.8$ minutes per day, plus extra reviews for cards you get wrong. The 10–15 minutes budgeted in [STUDY_PLAN.md](../../../STUDY_PLAN.md) is generous.

### Example 00-03.5 — Reading the interleaving study like an analyst (tier B)

**Setup.** In Rohrer & Taylor (2007), blocked practice scored 89% during practice and 20% on the delayed test; mixed (interleaved) practice scored 60% and 63% ([R-021](../../../reference/research-log.md#r-021--learning-science-evidence)). Compute the ratio of delayed-test scores. Then explain why a learner who judges progress by practice-session scores would choose the wrong strategy.

**Solution.** $63/20 = 3.15$: interleaved learners scored more than three times higher a week later. During practice, though, blocked practice "looked" $89/60 = 1.48$ times better. Blocked practice lets you reuse the method from the previous problem without deciding which method applies; the test (like real life) requires that decision. A learner tracking practice scores optimizes the wrong metric. **Lesson for the analyst in you:** measure the outcome you care about (delayed, mixed, unaided performance), not a convenient proxy.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 00-03.2a | current | 0.1935 | A |
| Ex 00-03.2b | load power | 1.686 | W |
| Ex 00-03.2c | current with ideal battery | 0.2 | A |
| Ex 00-03.2d | voltage lost to internal resistance | 3.2 | % |
| Ex 00-03.3a | naive dynamic power estimate | 3000 | W |
| Ex 00-03.3b | implied activity factor for 250 W | 0.0083 | — |
| Ex 00-03.4a | 7th interval | 244 | days |
| Ex 00-03.4b | cumulative days after 7 reviews | 406 | days |
| Ex 00-03.4c | daily review time | 2.8 | min |
| Ex 00-03.5a | ratio of delayed-test scores | 3.15 | — |
| Ex 00-03.5b | ratio of practice scores (blocked/mixed) | 1.48 | — |

*Recomputed by [verify_00_03.py](../verify/verify_00_03.py).*

## 5. Simulate it

The lab ([labs/00-03-lab/](../labs/00-03-lab/README.md)) gives you three tools you will use throughout the curriculum:

1. **A units checker** built on SymPy, which verifies the dimensions of any formula automatically (Example 00-03.1).
2. **A forgetting-and-review simulator**, a toy model comparing massed cramming with spaced review over 90 days.
3. **An error-log template** generator, which creates your personal error-log file.

**Predict, then run.** In the forgetting simulator, predict which strategy has higher recall 60 days later: 6 reviews crammed into the first 2 days, or 6 reviews spread at expanding intervals. Then predict by roughly how much.

## 6. Engineering tradeoffs

Studying has its own tradeoffs:

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| More time on problems, less on reading | Durable, transferable skill (retrieval practice) | Feels slower; early frustration | You |
| Interleave topics instead of blocking them | Long-term retention; choosing the right method | Lower scores during practice; feels harder | You (the checkpoints force it) |
| Longer review intervals | Less review time per card | More forgetting before each review (a harder, but more effective, retrieval) | Anki's scheduler; your retention target |
| Fast track before full depth | Earlier practical fluency for work | Gaps that must be back-filled later | You and your manager's calendar ([STUDY_PLAN.md](../../../STUDY_PLAN.md)) |
| Simulate before deriving by hand | Quick intuition | Risk of trusting tools you can't check | You; make "predict, then run" non-negotiable |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Retrieval practice vs rereading, 1-week recall | 61% vs 40% | [R-021](../../../reference/research-log.md#r-021--learning-science-evidence) |
| Interleaved vs blocked, 1-week test | 63% vs 20% | [R-021](../../../reference/research-log.md#r-021--learning-science-evidence) |
| Reviews to retain a card for a year (ease 2.5) | about 7 | Example 00-03.4 |
| Daily Anki time at about 3 new cards/day | a few minutes | Example 00-03.4 |
| Mastery bar for a chapter | ≥ 80% of [A] and [B] problems unaided | This curriculum |

## 8. Common mistakes

1. **Rereading instead of testing yourself.** It feels productive and isn't.
2. **Reading a solution before attempting the problem.** Once you've seen the answer, you can no longer practice retrieving it.
3. **Cramming before a checkpoint instead of spacing.** It works for the test and fails a month later.
4. **Skipping the checks.** Units, limits and magnitude take a minute and catch most errors.
5. **Substituting numbers too early.** A numerical expression cannot be checked for units or limits.
6. **Measuring progress by how practice feels.** Measure delayed, unaided, mixed performance; the checkpoints do this for you.
7. **Not keeping an error log.** You will make the same mistake again.

## 9. Practitioner lens

### Why this matters at work (as of Nov 2026)

- **FE exam pass rates:** the most recent published first-time FE Electrical & Computer pass rate is **70%**, for recent ABET-program graduates tested within 12 months of graduating (January–June 2026). Across all first-time takers in 2024 it was **62%** ([R-022](../../../reference/research-log.md#r-022--fe-electrical--computer-pass-rates)) **[Established]**. As a self-study candidate you are outside the 70% population. Treat the timed checkpoints seriously.
- **Engineering talent is scarce:** SIA and Oxford Economics project that about 67,000 US semiconductor jobs created by 2030 risk going unfilled, roughly 41% of them engineering roles ([R-023](../../../reference/research-log.md#r-023--us-semiconductor-workforce)) **[Industry estimate]**. Understanding how engineers are trained, and what they find hard, is relevant when you evaluate teams.

### Marketing vs Reality

**"Learn electrical engineering in 30 days."** Compare it with the arithmetic in [STUDY_PLAN.md](../../../STUDY_PLAN.md): ABET requires at least 75 semester credit hours of math, science and engineering topics, thousands of hours of work. A 30-day course can give you vocabulary, not the ability to solve problems. **Sanity check:** ask what the learner can *do* at the end (solve which problems, unaided, timed), not what they have *seen*.

**"I understand this; I've read it twice."** Rereading produces recognition, not recall. **Sanity check:** close the book and solve a problem.

### Questions to ask yourself (and engineering leaders about their teams)

1. **"How do you know you've learned it?"**
   *Strong answer:* "I solved unseen problems, timed, a week later." *Weak:* "It made sense when I read it."
2. **For leaders: "How do new engineers ramp up on your design flow, and how do you know when they're productive?"**
   *Strong:* structured onboarding with real tasks and measured milestones. *Weak:* "They pick it up."
3. **For leaders: "How do you capture lessons from bugs and respins so they don't recur?"**
   *Strong:* a living bug-escape database, root-cause reviews and checklist updates (an organizational error log). *Weak:* "We have good people."

## 10. Concept check

**Q1.** Which two learning techniques did Dunlosky et al. rate "high utility"?

<details>
<summary>Answer</summary>

Practice testing (retrieval practice) and distributed practice (spacing).

</details>

**Q2.** Why might interleaved practice feel worse but work better?

<details>
<summary>Answer</summary>

Mixing problem types forces you to decide which method applies, which is hard during practice but is exactly the skill the delayed test requires. Blocked practice lets you reuse the last method without choosing.

</details>

**Q3.** A derivation produces $\tau = R/C$. Without redoing the algebra, how do you know it is wrong?

<details>
<summary>Answer</summary>

Its units are Ω/F = V²/(A²·s), not seconds.

</details>

**Q4.** What are the three checks at the end of the problem-solving protocol?

<details>
<summary>Answer</summary>

Units (dimensions), limits and special cases, and magnitude (plausibility and sign).

</details>

**Q5.** In the simple forgetting model $R = e^{-t/S}$, what happens to review intervals as reviews succeed, and why?

<details>
<summary>Answer</summary>

They expand: each successful review increases the stability $S$, so recall takes longer to decay to the target level.

</details>

**Q6.** What are this curriculum's criteria for moving on from a chapter?

<details>
<summary>Answer</summary>

All concept-check questions answered from memory; at least 80% of the [A] and [B] problems solved unaided; the key derivation reproduced on a blank page; and the main idea explained aloud in two minutes.

</details>

Now work the problem set: [00-03 problems](../problems/00-03-problems.md) (solutions in [00-03 solutions](../solutions/00-03-solutions.md)).

## 11. Key terms

[Retrieval practice](../../../reference/glossary.md#retrieval-practice) ·
[Spacing effect](../../../reference/glossary.md#spacing-effect) ·
[Interleaving](../../../reference/glossary.md#interleaving) ·
[Illusion of competence](../../../reference/glossary.md#illusion-of-competence) ·
[Spaced repetition](../../../reference/glossary.md#spaced-repetition) ·
[Dimensional analysis](../../../reference/glossary.md#dimensional-analysis) ·
[SI base units](../../../reference/glossary.md#si-base-units) ·
[Fermi estimate](../../../reference/glossary.md#fermi-estimate) ·
[Error log](../../../reference/glossary.md#error-log)

## 12. Connections

- **Builds on:** [00-01](00-01-map-of-electrical-engineering.md), [00-02](00-02-the-abstraction-stack.md).
- **Next:** [00-04 Toolchain Setup Walkthrough](00-04-toolchain-walkthrough.md).
- **Used throughout:** every chapter's problem set, lab and concept check is built on this chapter's study loop. Dimensional analysis first appears formally in [01-01](../../01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md). The term checkpoints in [checkpoints/](../../../checkpoints/README.md) are your spaced, interleaved tests.

## 13. Further study

- **Brown, Roediger & McDaniel, *Make It Stick: The Science of Successful Learning* (2014):** a readable book-length treatment of the research in §3.1.
- **Dunlosky et al. (2013)**, cited in §3.1: the source review. Its summary tables are worth reading directly.
- **Pólya, *How to Solve It* (1945):** the classic problem-solving heuristics behind §3.3.
- **The Anki manual,** on importing CSV decks and adjusting review settings (see [flashcards/README.md](../../../flashcards/README.md)).

## 14. Sources

1. Research log [R-021](../../../reference/research-log.md#r-021--learning-science-evidence): Roediger & Karpicke (2006); Cepeda et al. (2006); Rohrer & Taylor (2007); Dunlosky et al. (2013).
2. Research log [R-022](../../../reference/research-log.md#r-022--fe-electrical--computer-pass-rates): NCEES FE Electrical & Computer pass rates.
3. Research log [R-023](../../../reference/research-log.md#r-023--us-semiconductor-workforce): SIA / Oxford Economics, *Chipping Away* (2023).
4. Research log [R-013](../../../reference/research-log.md#r-013--abet-curriculum-minimums-and-semester-credit-workload): ABET curriculum minimums.
5. The exponential forgetting model in §3.6 is a deliberate simplification for intuition, not a claim about any particular software's algorithm. All text, examples and problems are original.
