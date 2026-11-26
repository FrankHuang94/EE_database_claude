<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 28 · Technical Diligence and Engineering Leadership Fluency

The practitioner's course: a framework for evaluating a chip company's technology, validating claims, silicon maturity scales, domain question banks, red and green flags, evaluating engineering teams, integration risk, a business↔engineering translation table, and 25+ realistic conversation scenarios with annotated debriefs.

| | |
|---|---|
| **Term** | 7 |
| **Study hours** | ≈ 62 |
| **University equivalents** | No university equivalent. Draws on industry diligence practice. |
| **Textbook alignment** | Curriculum courses 09–27 (this repo); Public company filings, conference papers and technical documentation (cited per chapter) |
| **Prerequisites** | [26 · Engineering Design and Professional Practice](../26-engineering-design-and-professional-practice/README.md), [27 · System Architectures (Case-Study Course)](../27-system-architectures/README.md) |
| **FE areas** | — |
| **Deeper** | Companion repo(s): semiconductor capital equipment; datacenter networking; LLM inference engineering; quantum computing |

## Learning objectives

1. Apply a structured framework to evaluate a chip company's technology and roadmap.
2. Validate performance, efficiency and maturity claims using first-principles checks.
3. Ask domain-specific diagnostic questions and distinguish strong from evasive answers.
4. Assess engineering-team quality and post-acquisition integration risk.
5. Translate between business metrics and engineering metrics in conversation.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [28-01 · A Framework for Evaluating a Chip Company's Technology](chapters/28-01-technology-evaluation-framework.md) | 6 | ✅ verified | [problems](problems/28-01-problems.md) · [solutions](solutions/28-01-solutions.md) · [lab](labs/28-01-lab/README.md) · [verify](verify/verify_28_01.py) |
| [28-02 · Validating Claims: TOPS/W, Benchmarks, Tapeout Status](chapters/28-02-validating-claims.md) | 6 | ✅ verified | [problems](problems/28-02-problems.md) · [solutions](solutions/28-02-solutions.md) · [lab](labs/28-02-lab/README.md) · [verify](verify/verify_28_02.py) |
| [28-03 · Maturity Scales for Silicon](chapters/28-03-silicon-maturity-scales.md) | 4 | ✅ verified | [problems](problems/28-03-problems.md) · [solutions](solutions/28-03-solutions.md) · [lab](labs/28-03-lab/README.md) · [verify](verify/verify_28_03.py) |
| [28-04 · Domain Question Banks I: Digital/CPU, AI Accelerators, Memory, Interconnect and Optics](chapters/28-04-question-banks-digital-ai-memory-interconnect.md) | 6 | ✅ verified | [problems](problems/28-04-problems.md) · [solutions](solutions/28-04-solutions.md) · [lab](labs/28-04-lab/README.md) · [verify](verify/verify_28_04.py) |
| [28-05 · Domain Question Banks II: Analog/Mixed-Signal, RF, Power, Packaging, Embedded](chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md) | 6 | ✅ verified | [problems](problems/28-05-problems.md) · [solutions](solutions/28-05-solutions.md) · [lab](labs/28-05-lab/README.md) · [verify](verify/verify_28_05.py) |
| [28-06 · Red Flags and Green Flags](chapters/28-06-red-and-green-flags.md) | 4 | ✅ verified | [problems](problems/28-06-problems.md) · [solutions](solutions/28-06-solutions.md) · [lab](labs/28-06-lab/README.md) · [verify](verify/verify_28_06.py) |
| [28-07 · Evaluating Engineering Teams](chapters/28-07-evaluating-engineering-teams.md) | 5 | ✅ verified | [problems](problems/28-07-problems.md) · [solutions](solutions/28-07-solutions.md) · [lab](labs/28-07-lab/README.md) · [verify](verify/verify_28_07.py) |
| [28-08 · Post-Acquisition Integration Risk](chapters/28-08-integration-risk.md) | 5 | ✅ verified | [problems](problems/28-08-problems.md) · [solutions](solutions/28-08-solutions.md) · [lab](labs/28-08-lab/README.md) · [verify](verify/verify_28_08.py) |
| [28-09 · The Business ↔ Engineering Translation Table](chapters/28-09-business-engineering-translation.md) | 3 | ✅ verified | [problems](problems/28-09-problems.md) · [solutions](solutions/28-09-solutions.md) · [lab](labs/28-09-lab/README.md) · [verify](verify/verify_28_09.py) |
| [28-10 · Conversation Scenarios](chapters/28-10-conversation-scenarios.md) | 15 | ✅ verified | [problems](problems/28-10-problems.md) · [solutions](solutions/28-10-solutions.md) · [lab](labs/28-10-lab/README.md) · [verify](verify/verify_28_10.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/28-technical-diligence-and-leadership-fluency.csv) · [Equation sheet](../../reference/equation-sheets/28-technical-diligence-and-leadership-fluency.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 28 is planned at about 60 hours: the chapters' own estimates add to 60, plus a few hours of review; allow a further 3.5 hours for the exam. It is the practitioner's course, and it is different in kind from the engineering courses before it. Its subject is not a technology but a judgment: whether a chip company's claims, maturity, team and plans are what they appear to be, and what that means for a deal. Every chapter turns a soft question into numbers that can be checked:

- a scorecard and Bayes' rule in odds form, so evidence moves belief by a stated amount (28-01);
- first-principles checks of TOPS, TOPS/W, benchmarks and tape-out status (28-02);
- a maturity ladder with probabilities, value multipliers, qualification bounds and bug curves (28-03);
- question banks for every domain of Courses 14–27, each built on an identity you can compute (28-04, 28-05);
- flags as diagnostic tests with likelihood ratios, false-alarm rates and thresholds (28-06);
- team evaluation by shrinkage, reference-class schedules, bench depth and retention value (28-07);
- integration risk as synergy timing, migration and delay costs, parallel paths, licenses and registers (28-08);
- a translation table between business and engineering units (28-09);
- and 26 conversation scenarios that put it all to work in real time (28-10).

The course draws on all the technical courses: the roofline and accelerators of Course 14; converters, PLLs and analog scaling of Course 20; PAs and link budgets of Course 21; power conversion of Course 22; memory and HBM of Course 23; SerDes, chiplet links and optics of Course 24; die cost, packaging, reliability and qualification of Course 25; economics, schedules and teams of Course 26; and the product budgets of Course 27.

Work at least the [A] and [B] problems of every chapter; the [C] problems are where a calculation becomes a decision. The labs are Python models imported by their notebooks, all run in CI:

- `dilmodel.py` (28-01): scorecards, score variance, Bayes updates, milestone chains, earn-outs, EVPI and EVSI;
- `claimcheck.py` (28-02): peak and delivered throughput, TPP, energy floors, power boundaries, geometric means and best-of-N;
- `matscale.py` (28-03): value multipliers, acceleration factors, FIT bounds, sample sizes and the Goel–Okumoto fit;
- `qbank.py` (28-04): iso-power requirements, decode on the roofline, memory, link and port power, interview scoring;
- `bankcheck.py` (28-05): converter figures of merit, jitter, PA back-off, converter chains, package yield, battery life and Cpk;
- `flagmodel.py` (28-06): likelihood ratios, false alarms, count thresholds, key-person risk, HHI and funnels;
- `teameval.py` (28-07): Beta posteriors, schedule calibration, bench depth, scorecards and retention;
- `integrate.py` (28-08): synergy timing, migration and delay, parallel paths, royalties, TPP and registers;
- `translate.py` (28-09): die cost and elasticity, area budgets, energy cost, field failures and tornados;
- `convo.py` (28-10): the pocket card of live checks, a debrief scorer, Brier scores and timed drills.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/28-technical-diligence-and-leadership-fluency.md) collects the relations; these are the ideas behind them:

- evidence is worth its likelihood ratio, and a ratio is set by how often the evidence appears when the claim is false (28-01, 28-06);
- every headline number has a boundary and conditions: precision, sparsity, batch, input frequency, back-off, load, temperature, code loop (28-02, 28-04, 28-05);
- physics bounds what is possible: the roofline, the 8kT·SNR ceiling, class-B and Doherty efficiency, the energy floor of an operation (28-02, 28-04, 28-05);
- maturity is a probability and a wait; value rises as both shrink (28-03);
- base rates are low: most chip projects run late and few reach production on first silicon (28-06, 28-07);
- short track records deserve small adjustments, and overruns compound (28-07);
- delay is the silent killer of synergies and products (28-08, 28-09);
- die cost grows faster than area, and the elasticity is largest for big dies (28-09);
- answers that share a cause are one piece of evidence; group before you multiply (28-06, 28-10);
- preparation, live reconciliation and a written debrief are what turn a meeting into evidence (28-10).

**Where this leads.** The capstones put these methods to work on full cases, and the practitioner layer extends them to current industry state. Keep the debrief habit: score your own forecasts with the Brier score, and let your ratios improve with your record.
