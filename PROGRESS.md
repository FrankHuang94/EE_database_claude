# Progress

Build tracker for the Self-Taught BSEE. **Every session starts by reading [CLAUDE.md](CLAUDE.md) and this file, then continues from "Next step".**

## Next step

> **Phase 2 is under way** (the learner asked on 2026-11-12 to continue Phase 2 while pilot feedback is pending).
>
> - Course 00 is complete and audited (🏁).
> - Course 01 is complete and audited (🏁): ten chapters reviewed, exam, flashcards and equation sheet.
> - Course 02 is complete and audited (🏁): ten chapters reviewed, exam, 140 flashcards and equation sheet.
>
> - Course 03: 03-01 ✅ verified.
>
> **Next: write 03-02 · Random Variables and Distributions** (Bernoulli, binomial, Poisson, geometric, uniform, exponential, Gaussian and the Q-function; PMF, PDF and CDF).
>
> - Sourced facts for Course 03's practitioner sections were gathered on 2026-11-18 into the session scratchpad file `c03_facts.md`. 03-01 used the BER targets, zero-error test confidence, qualification sample sizes and Williams–Brown (now R-059 to R-062). Still unused: the KP4 RS(544,514) pre-FEC BER (about 2.4e-4 for 400G optics), the dual-Dirac jitter model (TJ = DJ + 2Q·RJ, 2Q = 14.069 at 1e-12), AEC-Q100/AIAG Cpk thresholds, Six Sigma 3.4 ppm (Q(4.5)), JEDEC FIT and HTOL with the Arrhenius 0.7 eV note, the NIST/SEMATECH e-Handbook, kT0 = −174 dBm/Hz, OFDM PAPR (LTE about 11.65 dB crest factor) and SRAM soft-error rates (AMD UG116). A scratchpad does not survive the session: re-gather them if it is gone, and log each one used as R-063 onward.
> - Natural homes: Q-function, jitter and PAPR in 03-02/03-03; Cpk, Six Sigma, HTOL/Arrhenius and Weibull in 03-05; kT0 and white noise in 03-06.
>
> When pilot feedback arrives, apply it to the pilots and to every chapter written since, before continuing.

## Phase status

| Phase | Scope | Status |
|---|---|---|
| 0 · Scaffold | Structure, CLAUDE.md, CURRICULUM.md, README, STUDY_PLAN, SETUP, env files, CI, tooling, notation | ✅ complete |
| 1 · Pilot | 02-01 and 07-02, complete with problems, solutions, labs, verification; then stop for feedback | ✅ complete — feedback still pending; learner asked to continue meanwhile |
| 2 · Courses | Terms 1 → 7 in prerequisite order; per-course audit; term checkpoints | 🔄 in progress: Courses 00, 01 and 02 🏁; Course 03 started |
| 3 · Capstones and practitioner layer | Capstones C1–C4, practitioner playbooks and case studies, reference files, final STUDY_PLAN | ⬜ not started |
| 4 · Final QA | Full CI pass, glossary/objective/cross-link audits, final report | ⬜ not started |

## Build statistics

<!-- BEGIN STATS (tools/progress_stats.py) -->

*Auto-generated; do not edit by hand. Courses appear once any chapter is written.*

| Course | Chapters | Written | Verified | Reviewed | Words | Problems | Verified numbers | Labs | Notebooks / netlists / testbenches |
|---|---|---|---|---|---|---|---|---|---|
| 00 | 5 | 5 | 5 | 5 | 22,489 | 52 | 229 | 5 | 5 / 3 / 1 |
| 01 | 10 | 10 | 10 | 10 | 57,268 | 162 | 1104 | 10 | 10 / 13 / 0 |
| 02 | 10 | 10 | 10 | 10 | 86,743 | 171 | 1316 | 10 | 10 / 18 / 0 |
| 03 | 6 | 1 | 1 | 0 | 7,569 | 16 | 100 | 1 | 1 / 0 / 0 |
| 07 | 11 | 1 | 1 | 0 | 8,902 | 18 | 149 | 1 | 1 / 6 / 0 |
| **Total** | **307** | **27** | **27** | **25** | **182,971** | **419** | **2898** | **27** | **27 / 40 / 1** |

Glossary terms: **376** · Flashcards: **352**

<!-- END STATS -->

## Course status

| Course | Status | Audit | Notes |
|---|---|---|---|
| 00 | 🏁 audited | ✅ 2026-11-12 | 5 chapters reviewed: 52 problems, 229 machine-checked chapter/lab values, exam (15 questions, 27 keyed values), 56 flashcards, equation sheet. The audit found 4 critical, 11 major and 12 minor items; all were fixed (see session log). |
| 01 | 🏁 audited | ✅ 2026-11-12 | 10 chapters reviewed: 162 problems, 1,104 machine-checked chapter, solution and lab values, 10 lab notebooks and 13 ngspice netlists; exam (15 questions, 128 points, 110 keyed values), 107 flashcards, equation sheet. Three independent reviewers found 5 critical, 25 major and about 40 minor items; all were fixed (see session log). |
| 02 | 🏁 audited | ✅ 2026-11-18 | 10 chapters reviewed: 171 problems, 1,316 machine-checked chapter, solution and lab values, 10 lab notebooks and 18 ngspice netlists; exam (15 questions, 128 points, 210 minutes, 146 keyed values, 18 ngspice checks), 140 flashcards, equation sheet. Four independent reviewers found 1 critical, about 25 major and about 130 minor items; all were fixed (see session log). |
| 03 | 🔄 in progress | — | 03-01 ✅ verified: 16 problems, 100 machine-checked values, Monte Carlo lab notebook, 3 figures; research log R-059 to R-062; 23 flashcards. |
| 07 | 🔄 in progress (pilot) | — | 07-02 ✅ verified: 16 problems, 128 machine-checked values, 6 ngspice netlists, lab notebook. Other chapters planned. |
| all others | ⬜ planned (stubs only) | — | |

Course status values: ⬜ planned · 🔄 in progress · ✅ complete (all chapters verified, exam + flashcards + glossary done) · 🏁 audited (independent review findings fixed).

## Open issues

| # | Issue | Raised | Owner / plan |
|---|---|---|---|
| 1 | **Companion repo URLs unknown.** "Deeper: see companion repo" callouts name the repos (semiconductor capital equipment, datacenter networking, LLM inference engineering, quantum computing) but cannot link them yet. | Phase 0 | Ask the learner for URLs; then link from CLAUDE.md and callouts. |
| 2 | **FE spec read via secondary snippets.** ncees.org was unreachable from the build environment. Question ranges for Linear Systems, Signal Processing, Electronics and Communications were confirmed only via secondary sources citing the July 2020 spec ([R-001](reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). | Phase 0 | Re-check against the NCEES PDF before writing the first checkpoint. |
| 3 | **FE Reference Handbook version.** 10.6 reportedly applies from July 2026; not verified on ncees.org. | Phase 0 | Verify before the first checkpoint; checkpoints cite only formula content, not page numbers. |
| 4 | **Open-source ASIC flow status.** The OpenLane/Sky130 ecosystem has reorganized; installation steps in SETUP.md §6 are deliberately deferred. | Phase 0 | Research and verify when building Course 19. |
| 5 | **Synchrophasor 20 frames/s rate** in IEC/IEEE 60255-118-1:2018 not confirmed ([R-005](reference/research-log.md#r-005--synchrophasor-standards)). | Phase 0 | Only cite rates confirmed for C37.118.1-2011 unless verified. |
| 7 | **Pilot feedback pending.** Rigor, pacing, math level, length and format of 02-01 and 07-02 to be confirmed by the learner. The learner asked to continue Phase 2 meanwhile. | Phase 1 | Learner; apply feedback retroactively to all chapters written since |
| 8 | **Pilot chapters link forward to planned chapters** (e.g., 07-01, 02-02, 06-08) whose stubs exist but are unwritten; pilot chapters restate the needed facts in recap boxes. | Phase 1 | Re-check these cross-references when the linked chapters are written. |
| 6 | **MkDocs Material end of life.** The mkdocs-material build prints that Material for MkDocs reaches end of life on 5 May 2027 and names Zensical as its successor. | Phase 0 | Site still builds; evaluate migration in Phase 4 (content is plain Markdown, so low risk). |
| 9 | **Primary market sources unreachable from the build environment.** wsts.org, semiconductors.org and jeita.or.jp do not resolve here, so the R-016 segment figures and logic growth rates were gathered from search-result excerpts and secondary reproductions. They are tagged [Industry estimate]. | Phase 2 (Course 00 audit) | Re-check against the primary PDFs from a network that reaches them, or ask the learner to allow these hosts. |
| 10 | **00-02 length.** At about 5,900 words, 00-02 exceeds the 4,000-word ceiling for survey chapters. Its derivations (regeneration, Q-function error rates, transmission-line reflections) make it a core-theory chapter in practice. | Phase 2 (Course 00 audit) | Accepted for now; budget raised to 3.5 h. Revisit after learner feedback on length. |
| 11 | **NVIDIA H100 die size (814 mm²)** is from trade-press reproductions of NVIDIA's launch materials; the whitepaper itself was not fetched ([R-015](reference/research-log.md#r-015--lithography-exposure-field-the-reticle-limit)). | Phase 2 (Course 00 audit) | Confirm from NVIDIA's Hopper whitepaper. |
| 12 | **UL benchmark pages unreachable.** benchmarks.ul.com and support.benchmarks.ul.com do not resolve from the build environment, so the 3DMark stress-test method ([R-030](reference/research-log.md#r-030--3dmark-stress-tests-and-frame-rate-stability)) was taken from search-result excerpts. | Phase 2 (02-02) | Re-check against UL's pages from a network that reaches them. |
| 13 | **02-06 length.** At about 10,500 words, 02-06 exceeds the 8,000-word ceiling for core chapters. It carries both the linear-algebra foundations and the matrix form of nodal analysis, plus the arithmetic-intensity material the practitioner layer uses. | Phase 2 (Course 02 audit) | Accepted for now; a split into two chapters would change the curriculum map. Revisit after learner feedback on length. |
| 14 | **Primary sources behind bot checks.** top500.org, hpl-mxp.org, nvidia.com and several standards stores could not be opened by the Course 02 reviewers, so the November 2026 TOP500 and HPL-MxP tables (R-038, R-055) and NVIDIA's Rubin page (R-040) were checked against press coverage. | Phase 2 (Course 02 audit) | Re-check against the primary pages from a network that reaches them. |

## Change log

Changes relative to the original build brief's chapter plan.

| Date | Change | Reason |
|---|---|---|
| 2026-11-12 | Added **05-09 Software Engineering Practices** | FE E&C includes Software Engineering (4–6 questions); not otherwise covered. |
| 2026-11-12 | Added **17-13 Computer Networks Fundamentals** | FE E&C includes Computer Networks (4–6 questions); points to the datacenter-networking companion repo for depth. |
| 2026-11-12 | Expanded Course 22's "brief intro to motors and the power grid" into **22-11 Electric Machines and Drives** and **22-12 Power Systems Fundamentals** | FE E&C includes Power Systems (8–12 questions), the largest area not otherwise covered at exam depth. |
| 2026-11-12 | Course 07 ordering follows the brief (Laplace-domain analysis in 07-04 before sinusoidal steady state in 07-05) | Lets AC steady state be derived as the special case s = jω. Phasors are introduced first in 02-01. |
| 2026-11-12 | Course 10 split: 10-01 diodes · 10-02 MOSFET DC · 10-03 BJT DC · 10-04 small-signal models · 10-05 amplifier fundamentals | Matches the brief's example file name `10-04-small-signal-models.md`. |
| 2026-11-12 | Term 1 study order: Python chapters (05-01–05-04) before Course 01; C chapters (05-05–05-09) at term end | Every lab from 02-01 onward is a Python notebook. |

## Session log

| Date | Session summary |
|---|---|
| 2026-11-18 | Phase 2. 03-01 Probability in EE Language written and verified (axioms, union bound and the e^{-np} rule, counting and birthday collisions, conditioning and total probability, Bayes' rule with base rates and MAP detection, independence and conditional independence, series/parallel/TMR reliability with common-mode failures, Williams–Brown defect level derived from Bayes): 16 problems, 100 keyed values (109 checks), Monte Carlo notebook, 3 figures, 17 glossary terms, 23 flashcards; research log R-059 (PCIe and Ethernet BER targets), R-060 (zero-error BER tests), R-061 (AEC-Q100/JESD47 qualification samples), R-062 (Williams–Brown). |
| 2026-11-18 | Phase 2. **Course 02 completed and audited (🏁).** Wrote the final exam (15 questions, 128 points; solutions, verify script with 146 keyed values, ngspice netlist for the circuit questions), extended the flashcards to 140 cards, wrote the equation sheet and course notes. Four fresh reviewers audited 02-01..02-10, the exam, cards and sheet: 1 critical (02-09 concept check on Euler pole placement), about 25 major, about 130 minor findings, all fixed. Major fixes: 02-03 overshoot formulas restricted to all-pole reference steps (log decrement for load steps), PLL closed-loop zero quantified, target impedance checked across frequency; 02-04 duplication rule, derived build-up envelope, NFC Q criterion (Q ≤ 7.742); 02-05 zero-state vs natural terminology, shifted impulses and sifting, piecewise and periodic inputs, convolution solutions; 02-06 diagonal dominance and threshold pivoting; 02-07 cofactor and rank–nullity derivations, Gram–Schmidt and QR; 02-08 complex SVD for MIMO, Hermitian and unitary matrices, Schur argument; 02-09 linearization and latch metastability; 02-10 full Newton expansion, Jacobian, ngspice and SPICE3 limiting rules, refinement floor κu₆₄; exam trimmed to 210 minutes and reused items replaced. Added 32 problems across the course, R-058 (FIVR, PowerVia), P3109 in R-056. tools/run_verify.py now accepts chapter-style filters and fails when nothing matches. Gathered sourced facts for Course 03. |
| 2026-11-18 | Phase 2. 02-10 Numerical Methods for Engineers written and verified (floating point and AI formats, bisection and Newton, how SPICE solves DC with companion models, limiting and GMIN, Euler/RK/implicit integrators, stability regions and stiffness, conditioning and mixed-precision refinement); all ten Course 02 chapters now verified. Research log R-053 (ngspice defaults and DEVpnjlim from source), R-054 (SPICE/SPICE2 reports), R-055 (HPL-MxP Nov 2026), R-056 (OFP8, bfloat16, binary16), R-057 (Patriot GAO report and Skeel). |
| 2026-11-18 | Phase 2. 02-09 Systems of Linear ODEs and the Matrix Exponential written and verified (state space from circuits, eigenvector and e^At solutions, phase plane, forced response and transfer functions, Foster/Cauer thermal modes, ZOH vs Euler, state-space sequence models): 15 problems, 63 keyed values, notebook and 3 ngspice netlists; research log R-049 (Infineon Foster/Cauer note), R-050 (Moler–Van Loan, expm algorithms; not "best", "one of the most effective"), R-051 (Kalman 1960, battery-gauge models), R-052 (S4 bilinear, Mamba ZOH), checked against saved documents. |
| 2026-11-18 | Phase 2. 02-08 Eigenvalues and Eigenvectors written and verified (Markov chains, complex eigenvalues as poles, spectral theorem, positive definiteness, coupled-resonator normal modes, SVD, low-rank approximation and MIMO): 15 problems, 101 keyed values, notebook and 1 ngspice netlist; research log R-045 (5G NR Type II CSI as eigenvector feedback), R-046 (Litterman–Scheinkman yield-curve factors; method description contested), R-047 (PageRank), R-048 (Eckart–Young), checked against saved pages. |
| 2026-11-18 | Phase 2. 02-07 Determinants, Inverses, Rank and Vector Spaces written and verified (adds least squares and circuit incidence matrices): 15 problems, 121 keyed values, notebook and 1 ngspice netlist; research log R-041 (5G NR MIMO layers), R-042 (Wi-Fi spatial streams; Wi-Fi 7 is 8, not 16), R-043 (LoRA), R-044 (GPS four satellites and least squares), found by a fact-finding subagent and re-checked against the saved pages. |
| 2026-11-18 | Phase 2. 02-06 Vectors, Matrices and Linear Systems written and verified: 15 problems, 165 keyed values, notebook and 2 ngspice netlists (15 simulator checks); research log R-037 (KLU, ngspice solver options), R-038 (HPL, TOP500 Nov 2026), R-039 (TPU v1), R-040 (H100 and Rubin specs), found by a fact-finding subagent and re-checked against the saved primary pages. |
| 2026-11-17 | Phase 2. 02-05 The Laplace Transform for ODEs written and verified: 15 problems, 61 keyed values, notebook (table checks, partial fractions with SymPy and SciPy, pole map, final-value-theorem traps) and 2 ngspice netlists, one simulating H(s) directly with the XSPICE s_xfer block; research log R-036 (Verilog-AMS Laplace filters, ngspice s_xfer), and the research-log index back-filled for R-024 to R-036. |
| 2026-11-17 | Phase 2. 02-04 Forced Response and Resonance written and verified: 15 problems, 116 keyed values, notebook (complex replacement, resonant peak, half-power bandwidth, beats and build-up) and 2 ngspice AC netlists; research log R-034 (ISO/IEC 14443 / NFC) and R-035 (32.768 kHz crystal Q and start-up). |
| 2026-11-12 | Phase 2. 02-03 Second-Order Linear ODEs written and verified: 15 problems, 123 keyed values, notebook (roots and responses, step specifications, energy, PDN design space) and 2 ngspice netlists; research log R-032 (PDN target impedance, Smith et al. 1999) and R-033 (quartz Q, Vig). |
| 2026-11-12 | Phase 2. 02-02 First-Order Linear ODEs written and verified: 15 problems, 104 keyed values, notebook (direction fields and blow-up, Euler/backward Euler/trapezoid, logistic fit, thermal runaway) and 3 ngspice netlists; research log R-029 (JESD51-2A), R-030 (3DMark stability), R-031 (thermal runaway). |
| 2026-11-12 | Phase 2. Course 01 completed: 01-10 written, exam (15 questions), flashcards, equation sheet and course notes. Independent audit by three fresh reviewers (01-01–01-04, 01-05–01-07, 01-08–01-10 plus course materials): 5 critical, 25 major and about 40 minor findings, all fixed. Highlights: Bode-phase slope claim corrected; Newton-ratio explanation fixed (01-04.14); lab 01-07's 60° load now changes R and L (425 W, ngspice-confirmed); duration/convexity analogy corrected; RSS restated in terms of standard deviations; hypotheses added to Newton and L'Hôpital; reciprocal rule derived; new material on hyperbolic functions, logarithmic differentiation, trigonometric substitution (finite-wire field example), completing the square, area/volume/arc length/centroids, limit-comparison/integral/root tests, constant-voltage actuator energy balance, 2-variable Taylor and D-test proof, least-squares and shadow-price proofs, Green's theorem proof, divergence/curl box pictures, orientation rules, curved-surface flux, cylindrical Gauss's law and coax; coordinate-convention callout and vector-field arrows per notation.md; 13 new problems; many missing answer keys added; exam rebalanced (series and divergence-theorem parts; Q11 → A, Q15 → C); new research-log entry R-028 (IEC 62053-21) and power limits added to R-007. Course 01 marked reviewed. |
| 2026-11-12 | Phase 2. Course 00 audit: an independent reviewer found 4 critical, 11 major and 12 minor items, all fixed. The fixes covered: CV² per transition (now ½CV² average); WSTS "Micro" is MPU + MCU + DSP; re-keyed ADI R&D per employee; a sourced and re-tagged logic-growth figure (R-016) and a new EDA-concentration entry (R-024); respin timing reconciled across full-layer, metal-only and firmware cases; a dated fab-cycle and mask-count claim; first-silicon figures leading with the trend; a derivative refresher added to 00-04; floating-point and ngspice-tolerance corrections; the exam rebuilt to 15 questions (3 diligence items, all values keyed); hours re-budgeted (≈17 h). Course 00 marked reviewed. 01-01 written and verified (15 problems, 123 values). |
| 2026-11-12 | Phase 2 start. Course 00 (5 chapters, 52 problems, 5 labs with notebooks, 3 netlists, 1 testbench), exam, flashcards (56), equation sheet, glossary; pushed. |
| 2026-11-12 | Phase 1. Pilot chapters 02-01 (18 problems, 118 machine-checked values) and 07-02 (18 problems, 149 machine-checked values, 6 ngspice netlists) with labs, figures, glossary (48 terms) and flashcards (55). An independent reviewer subagent audited both chapters and found 3 critical, 8 major and ~25 minor issues, all in labels, prose and reasoning rather than computed numbers. All were fixed: an off-by-one term-count label, a wrong 'overshoot' caption, a ±% error, resistor-flyback on-state cost, an ENOB-loss calculation, a rise-time caveat, stronger ngspice coverage (i_C jumps, 72 V switch voltage), PMU standard citation, a rigor gap in the steady-state argument, notation clashes (k, s, V_Th), and added Problems 02-01.18 and 07-02.17–18 (damped exponentials, dependent sources and negative R_Th, two-position switch with u(t)). Stopped for feedback. |
| 2026-11-12 | Phase 0. Repo created; curriculum data model + generators; CLAUDE.md, CURRICULUM.md (29 courses, 307 chapters), README, STUDY_PLAN, SETUP, notation; verification toolkit (answer-key checker, ngspice/HDL/notebook runners, link and structure checkers); CI; smoke tests pass. Research log R-001–R-013. |
