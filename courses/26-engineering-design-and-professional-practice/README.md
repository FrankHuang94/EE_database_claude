<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 26 · Engineering Design and Professional Practice

How engineering decisions are made and paid for: requirements and specifications, design reviews and standards bodies, engineering economics from NRE to gross margin, build vs buy vs license, schedule and respin risk, team structures, and engineering ethics.

| | |
|---|---|
| **Term** | 7 |
| **Study hours** | ≈ 42 |
| **University equivalents** | Senior Design / Engineering Professional Practice + Engineering Economics |
| **Textbook alignment** | Ulrich & Eppinger, *Product Design and Development*; Newnan, Eschenbach & Lavelle, *Engineering Economic Analysis* (FE economics review); NSPE Code of Ethics for Engineers (free) |
| **Free courses** | MIT OCW 2.009 / 6.UAP project-course materials (design process) |
| **Prerequisites** | [19 · Digital VLSI Design](../19-digital-vlsi-design/README.md), [20 · Analog and Mixed-Signal IC Design](../20-analog-and-mixed-signal-ic-design/README.md) |
| **FE areas** | Ethics and Professional Practice, Engineering Economics |

## Learning objectives

1. Write measurable requirements and specifications and run a design review.
2. Build a chip business case from NRE, die cost, ASP, volume and gross margin.
3. Analyze build vs buy vs license, node selection, monolithic vs chiplet and ASIC vs merchant-silicon decisions.
4. Identify schedule and respin risks and their mitigations.
5. Apply engineering-ethics frameworks and FE engineering-economics methods.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [26-01 · Requirements, Specifications and the Design Process](chapters/26-01-requirements-and-specifications.md) | 5 | 🏁 reviewed | [problems](problems/26-01-problems.md) · [solutions](solutions/26-01-solutions.md) · [lab](labs/26-01-lab/README.md) · [verify](verify/verify_26_01.py) |
| [26-02 · Design Reviews, Documentation and Standards Bodies](chapters/26-02-design-reviews-and-standards.md) | 4 | 🏁 reviewed | [problems](problems/26-02-problems.md) · [solutions](solutions/26-02-solutions.md) · [lab](labs/26-02-lab/README.md) · [verify](verify/verify_26_02.py) |
| [26-03 · Engineering Economics I: NRE, Die Cost, ASP and Gross Margin](chapters/26-03-engineering-economics-1.md) | 7 | 🏁 reviewed | [problems](problems/26-03-problems.md) · [solutions](solutions/26-03-solutions.md) · [lab](labs/26-03-lab/README.md) · [verify](verify/verify_26_03.py) |
| [26-04 · Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant](chapters/26-04-engineering-economics-2.md) | 8 | 🏁 reviewed | [problems](problems/26-04-problems.md) · [solutions](solutions/26-04-solutions.md) · [lab](labs/26-04-lab/README.md) · [verify](verify/verify_26_04.py) |
| [26-05 · Schedule and Risk: Why Respins Happen](chapters/26-05-schedule-and-respin-risk.md) | 6 | 🏁 reviewed | [problems](problems/26-05-problems.md) · [solutions](solutions/26-05-solutions.md) · [lab](labs/26-05-lab/README.md) · [verify](verify/verify_26_05.py) |
| [26-06 · Engineering Team Structures and Sizing](chapters/26-06-team-structures-and-sizing.md) | 5 | 🏁 reviewed | [problems](problems/26-06-problems.md) · [solutions](solutions/26-06-solutions.md) · [lab](labs/26-06-lab/README.md) · [verify](verify/verify_26_06.py) |
| [26-07 · Engineering Ethics and Professional Responsibility](chapters/26-07-engineering-ethics.md) | 5 | 🏁 reviewed | [problems](problems/26-07-problems.md) · [solutions](solutions/26-07-solutions.md) · [lab](labs/26-07-lab/README.md) · [verify](verify/verify_26_07.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/26-engineering-design-and-professional-practice.csv) · [Equation sheet](../../reference/equation-sheets/26-engineering-design-and-professional-practice.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 26 is planned at about 42 hours: the chapters' own estimates add to 40, plus about 2 hours of review; allow a further 3 hours for the exam. It is the least physical course in the curriculum and the one closest to your day job, so the risk is reading it too quickly. Every chapter turns a judgment call (how many reviewers, which node, when to tape out, how big a team) into a model with a few parameters, and the skill is knowing which parameter drives the answer and how badly the model fails when its assumption does. It draws on several earlier courses:

- Course 01: optimization (01-04) and the geometric series behind the interest factors (01-08);
- Course 03: the binomial and independence (03-02), variance of a sum with correlation and the central limit theorem (03-04), and confidence bounds (03-05);
- Course 06: error budgets for one circuit (06-07), which 26-01 scales up to a product;
- Course 05: traceability and version control for software (05-09);
- Course 14: Amdahl's law (14-01), which 26-04 applies to die area;
- Courses 19 and 25: pre-silicon verification (19-13), dies per wafer, yield and cost per good die (25-04), chiplet packaging cost (25-07), FIT rates (25-09), functional safety (25-10), test cost (25-11), and ECOs, bring-up and respin decisions (25-12);
- Course 22: power usage effectiveness (22-10) for datacenter TCO.

The seven chapters fall into four blocks:

- **Deciding what to build (26-01 and 26-02).** Measurable requirements, duty-cycle and error budgets (worst case against RSS, and what correlation does to them), traceability, the cost of finding an error late, and decision matrices with their tie weights; design reviews as independent detectors, capture–recapture estimates of what remains, and how standards bodies ballot, license essential patents and stack royalties.
- **What it costs and what it earns (26-03 and 26-04).** The cost stack from wafer to good packaged unit, margin and markup, break-even volume, the FE time-value factors, NPV, IRR, payback and what a slip costs; then the sourcing decisions: license against build on a discounted unit stream, per-unit against percentage royalties, node choice through the mix-weighted density gain, chiplets and families, and custom silicon against merchant parts by TCO per unit of throughput.
- **Schedule and people (26-05 and 26-06).** PERT, merge bias and Monte Carlo schedules, expected tape-outs, full respins against metal-only ECOs, the risk register, and the optimal tape-out time from a bug-discovery model; team output with coordination cost, hierarchy, Brooks's law with ramp and mentoring, span of control, and the newsvendor rule for base staff against contractors.
- **Responsibility (26-07).** The NSPE canons and rule II.1.a, licensure and the FE exam's ethics area, fleet-scale risk, FIT budgets, common-cause failure, zero-failure evidence bounds, patents, mask works and trade secrets, and reading the ECCN 3A090 thresholds.

Work at least the [A] and [B] problems of every chapter; the [C] problems are where the models meet a messy decision. The FE exam tests 26-03's interest factors and 26-07's ethics topics directly, so drill those until they are automatic. The labs are Python models imported by their notebooks, all run in CI:

- `reqs.py`: battery-life flow-down, error budgets with a Monte Carlo of correlated and non-Gaussian sources, the escalation model and decision matrices with their tie weights (26-01);
- `reviews.py`: reviewer detection with shared blind spots, the cost-optimal team, a Monte Carlo of capture–recapture bias, ballot checks, royalty stacks and the value of designing to a draft standard (26-02);
- `econ.py`: the cost stack, interest factors, NPV and IRR, the slip model and a tornado sensitivity analysis (26-03);
- `sourcing.py`: license against build, royalty forms, node choice, chiplet families and accelerator TCO (26-04, importing `econ.py`);
- `risk.py`: PERT and beta-PERT Monte Carlo schedules, tape-out counts, the risk register and the optimal tape-out time (26-05);
- `team.py`: flat and hierarchical team output, Brooks finish times and the staffing newsvendor (26-06);
- `safety.py`: fleet risk, FIT budgets, the beta-factor model, rate bounds and TPP classification (26-07).

**What to master cold.** The [equation sheet](../../reference/equation-sheets/26-engineering-design-and-professional-practice.md) collects the relations; these are the ideas behind them:

- a requirement is a quantity, a condition and a verification method; battery life is set by the mode with the largest $d_iI_i$, not the largest current; RSS is a claim of independence, and correlation pushes it back toward worst case (26-01);
- a review's value is the downstream cost it avoids: total cost is linear in the early catch rate, so a few points of detection are worth a great deal when late fixes cost tens of times more (26-01);
- a decision matrix does not make a choice objective; it makes the weights arguable, and the tie weight says which argument matters (26-01);
- independent reviewers have diminishing returns, shared blind spots cap what any number of them can find, and capture–recapture reads low when difficulty varies; diversity beats headcount (26-02);
- standards are made by measurable consensus, and a percentage royalty means nothing until its base is fixed (26-02);
- yields divide accumulated cost, so a loss late in the flow costs more than the same loss early; margin divides profit by price and markup by cost (26-03);
- money has a time value: a slip both discounts every sales year once more and, when the market window is fixed, cuts off the tail, so in Example 26-03.5 a one-year slip costs about seven times a 10% NRE overrun; schedule and price, not engineering budget, dominate a program's value (26-03);
- a per-unit charge is worth $r$ times the discounted unit stream; break-even volumes for licences, nodes and custom silicon all have the same shape, fixed cost over per-unit saving (26-04);
- node choice runs through the mix-weighted (harmonic) density gain, so SRAM and analog that barely shrink cap the benefit of a better logic density (26-04);
- custom silicon is judged by TCO per unit of throughput, not chip price, and a credible custom program caps what the merchant can charge (26-04);
- schedules finish late because of merge bias at joins and because respins come in fab-cycle quanta; a metal-only ECO from held wafers is an option bought in advance with spare cells (26-05);
- the optimal tape-out balances the weekly cost of more verification against the falling probability of a respin-class escape, and it moves earlier when bugs are found faster (26-05);
- coordination cost caps a flat team's useful size near $(1 + 1/c)/2$; hierarchy buys scale at the price of cross-team cost; adding people late helps only while enough work remains to repay their ramp (26-06);
- the public comes first: at fleet scale a tiny per-unit risk becomes an expected number of events, common cause dominates redundancy, and zero failures bound a rate only to about $3/T$ (26-07);
- an export classification is a calculation (TPP and density against the thresholds), and an engineer's statement about it is a professional claim, governed by the canons on truthfulness (26-07).

**After this course.** Course 27 applies these models to whole systems, starting each case study from requirements and a cost model. Course 28 turns them into diligence: building and stress-testing a business case, sizing schedule and respin risk, judging a team and its claims, and asking the questions in each chapter's Practitioner lens. The Term 7 FE checkpoint follows Course 28 and tests the economics and ethics areas again.
